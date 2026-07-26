# A-FORGE MCP Tool Wiring Pattern

## How to register a new tool in A-FORGE's MCP surface

File: `src/interfaces/mcp/core.ts`

Pattern: `server.tool(name, description, zodSchema, async handler)`

### Minimal example

```typescript
server.tool(
  "forge_my_tool",
  "Description of what this tool does. Constitutional basis.",
  {
    mode: z.enum(["validate_only", "full_loop"]).default("full_loop"),
    input_field: z.string().describe("What this field does"),
    session_id: z.string().optional(),
    actor_id: z.string().optional(),
  },
  async (args) => {
    const startedAt = Date.now();
    await telemetryInvoke("forge_my_tool");
    try {
      // ... tool logic ...
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (err) {
      await telemetryFailure("forge_my_tool", startedAt, err);
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ error: err instanceof Error ? err.message : String(err) }, null, 2),
        }],
        isError: true,
      };
    }
  }
);
```

### Cross-organ routing via callMCP

```typescript
// Route to arifOS kernel for judgment
const judgeResult = await callMCP("arifos.arif_judge", {
  intent: "my_intent",
  domain: "my_domain",
  reversibility_level: "reversible",
  blast_radius: "low",
  evidence: [context],
});

// Route to WELL for operator state
await callMCP("well.well_assess_homeostasis", {
  mode: "sleep",
  subject: "operator",
});

// Route to VAULT999 for sealing
const sealResult = await callMCP("arifos.arif_seal", {
  mode: "seal",
  payload: JSON.stringify(data),
});
```

### Key imports already available in core.ts

- `z` from `"zod"`
- `server` (McpServer instance)
- `callMCP` from `"./client.js"`
- `telemetryInvoke`, `telemetryFailure` (telemetry wrappers)
- `verdict`, `sealVerdict`, `errorVerdict`, `holdVerdict` from `"../../domain/governance/verdict-envelope.js"`
- `consultScars` from `"../../domain/forge/skill/index.js"` (note: different signature than ForgeVisualQA's internal `consultScars`)

### Pitfalls

1. **Don't re-import modules already imported at the top of core.ts.** Check the existing imports before adding new ones. `consultScars`, `listScars`, etc. may already be imported.

2. **Return format:** Always return `{ content: [{ type: "text" as const, text: JSON.stringify(...) }] }`. The `as const` on `"text"` is required for TypeScript.

3. **telemetryInvoke/telemetryFailure:** Always wrap the handler body. `telemetryInvoke` at start, `telemetryFailure` in catch.

4. **Error format:** On error, set `isError: true` on the return object.
