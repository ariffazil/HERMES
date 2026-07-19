# A-FORGE MCP Tool Registration Pattern

> A-FORGE uses TypeScript + @modelcontextprotocol/sdk with a hexagonal architecture.
> Unlike Python FastMCP servers, A-FORGE has a 3-step tool registration flow plus
> automatic FloorEnforcer gating. Every tool is constitutionally gated by F1–F13
> before reaching the handler.
>
> **Last verified:** 2026-07-13 (EUREKA P1)
> **Stack:** Node.js 22, TypeScript, McpServer SDK, Zod schemas

---

## 3-Step Registration Flow

### Step 1: Classify the Tool

File: `/root/A-FORGE/src/domain/governance/actionClassifier.ts`

Add the tool name to the appropriate action class set:

```typescript
// For read-only tools (most common for new OBSERVE tools):
const OBSERVE_TOOLS = new Set([
  // ... existing tools ...
  "forge_runtime_verify",     // runtime hash verification — read-only, OBSERVE
  "forge_cool_drift",         // cooling receipt drift — read-only, OBSERVE
  "forge_cool_pattern",       // cooling receipt pattern — read-only, OBSERVE
]);
```

Action class determines what governance gates fire (OBSERVE = no lease required,
EXECUTE_REVERSIBLE = lease + session, IRREVERSIBLE = 888_HOLD).

**Rule of thumb:** If your tool does not mutate filesystem/network/vault, it's OBSERVE.
Unknown tools default to OBSERVE (fail-safe). Only add to the explicit set for
documentation — classification still works without it.

### Step 2: Create the Tool Implementation

File: `/root/A-FORGE/src/interfaces/mcp/<toolName>.ts`

Pattern (OBSERVE-class tool):

```typescript
import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

export function registerMyTool(server: McpServer): void {
  server.tool(
    "forge_my_tool",           // tool name — must start with forge_
    "Description of what this tool does. Appears in tools/list.",
    {
      // Zod schema — all params documented with .describe()
      param1: z.string().describe("What this param is for"),
      param2: z.number().optional().describe("Optional param"),
    },
    async (params) => {
      try {
        // Handler logic
        const result = { status: "SEAL", data: "..." };
        return {
          content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
        };
      } catch (err: any) {
        return {
          content: [{ type: "text" as const, text: JSON.stringify({
            verdict: "HOLD", error: err.message
          }, null, 2) }],
          isError: true,
        };
      }
    }
  );
}
```

Key conventions:
- Tool names start with `forge_` (OBSERVE tools) or `forge_` (all tools)
- Return `{ content: [{ type: "text" as const, text: JSON.stringify(...) }] }`
- Error responses use `isError: true` + HOLD verdict
- Use `as const` on type literals (`"text" as const`) — TypeScript strict mode requires it
- Zod schemas must inline `.describe()` on every field for MCP tools/list output
- The FloorEnforcer auto-injects `_epistemic` and `authority_header` to JSON responses

### Step 3: Wire Into core.ts

File: `/root/A-FORGE/src/interfaces/mcp/core.ts`

Two edits:

**Import the registration function:**
```typescript
import { registerMyTool } from "./myTool.js";  // Note .js extension for TS imports
```

**Call the registration function** (after isomorphism tools, before verdict interceptor):
```typescript
// ── My Feature Description ─────────────────────────────────────────────
registerMyTool(server);
```

Registration order matters for tool listing — insert in a logical section.
The FloorEnforcer wrappers are applied automatically to all tools registered
via `server.tool()` — no additional gating needed.

---

## ESM vs CJS Pitfall

A-FORGE's `package.json` has `"type": "module"`, which means Node treats `.js` files as ES modules.

**If you create a standalone script that uses `require()`:**
```
❌ script.js    → ERR_REQUIRE_ESM (because "type": "module")
✅ script.cjs   → works with require()
```

The metabolism tracker (`scripts/metabolism-tracker.cjs`) demonstrates the pattern.

**If you create a TypeScript file under `src/`:**
- TypeScript compiles to `.js` files in `dist/`
- The imports use ES module syntax (`import`/`export`)
- This works fine because TypeScript handles the module resolution

**Diagnostic:**
```bash
# Check the root package.json
grep '"type"' /root/A-FORGE/package.json
# → "type": "module"

# Scripts > 200 lines are CJS -> rename to .cjs
# Scripts < 200 lines can use .mjs (import) or .cjs (require)
```

---

## Epistemic Tagging

Every JSON response from A-FORGE tools gets an auto-injected `_epistemic` tag
and `authority_header` in `core.ts`. The tag is derived from tool name patterns:

| Tool Name Pattern | output_class | authority_claim |
|---|---|---|
| `forge_*` (default) | DETERMINISTIC | ADVISORY |
| `forge_*_seal`, vault, lease, approval | GOVERNANCE_TEMPLATE | EXECUTIVE |
| `forge_*_plan`, `forge_*_dry_run`, `forge_*_status` | DOMAIN_COMPUTATION | ADVISORY |
| `forge_*_execute`, `forge_*_run`, `forge_*_commit` | DETERMINISTIC | EXECUTIVE |

The `authority_header` is computed by `computeAuthorityHeader()` in core.ts:

| Tool Pattern | authority_mode | reversibility |
|---|---|---|
| Contains `_seal`, vault | SEAL | irreversible |
| Contains `_ratify`, `_approve`, `_human` | RATIFY | irreversible |
| Contains `_execute`, `_run`, `_commit`, `_shell` | EXECUTE | reversible |
| Contains `_draft`, `_plan`, `_dry_run`, `_status` | DRAFT | reversible |
| Default (OBSERVE tools) | OBSERVE | reversible |

---

## Governance Gates Applied Automatically

All tools registered via `server.tool()` pass through:
1. **A-THINK Guard** — classify → budget → affordance → permission
2. **Session + Lease validation** (for MUTATE/IRREVERSIBLE tools)
3. **FloorEnforcer** — F1–F13 constitutional gating
4. **Epistemic tag injection** — `_epistemic` + `authority_header` on every JSON response
5. **Schema strictification** — `additionalProperties: false` auto-applied to inputSchema
6. **Actuator description enrichment** — tool descriptions prefixed with `[ACTUATOR]`

You do NOT need to add these individually to each tool — they're applied in the
`server.tool()` wrapper in core.ts.

---

## Build & Verify

```bash
# Build (TypeScript compilation)
cd /root/A-FORGE && npm run build  # tsconfig strict mode

# Verify the tool appears in live listTools
# (if MCP server running)
curl -s -X POST http://localhost:7072/mcp \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' 2>/dev/null | \
  python3 -c "import json,sys; data=json.load(sys.stdin); [print(t['name']) for t in data.get('result',{}).get('tools',[])]" | \
  grep forge_my_tool
```

---

## Sequence Diagram

```
Developer writes:
  1. actionClassifier.ts  (classify the tool)
  2. myTool.ts            (tool implementation)
  3. core.ts              (import + register)

At server start:
  core.ts → server.tool("forge_my_tool", schema, handler)
           → FloorEnforcer wraps handler
           → Epistemic injector wraps response
           → Tool registered in MCP SDK

At tool call:
  MCP request → FloorEnforcer.checkAll()
              → A-THINK Guard
              → Session + Lease check (if MUTATE)
              → Handler runs
              → _epistemic injected
              → Response returned
```

---

## Full Example: forge_runtime_verify

Reference the implementation at:
- `src/interfaces/mcp/runtimeVerify.ts` — 250 lines
- `src/domain/governance/actionClassifier.ts` — OBSERVE_TOOLS addition
- `src/interfaces/mcp/core.ts` — import + registration

The tool reads git commit, pip package, and Python import path, compares
all three, and returns MATCH/DRIFT/UNKNOWN with detailed evidence.
