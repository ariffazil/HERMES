# A-FORGE Shadow Judiciary Audit (2026-07-28)

## Summary

A-FORGE contains a **dual shadow judiciary** — both a Python and TypeScript implementation of local tool-permission checking that should exist ONLY in arifOS (the kernel judge). Every MCP tool call through A-FORGE's gateway is gated locally by `aThinkGuard.ts` before any request reaches `arif_judge` at arifOS:8088. This is an F13 Separation of Powers violation.

## Violations

### V1: Python a_think/ Directory (10 files)

**Path:** `/root/A-FORGE/a_think/`

| File | Lines | Function | Severity |
|------|-------|----------|----------|
| `mcp_guard.py` | 47-50 | `DecisionStatus` enum (ALLOW/DENY/HOLD) | 🔴 |
| `mcp_guard.py` | 126-343 | `MCPGuard` class — full gated call flow | 🔴 |
| `affordance.py` | 107-229 | `AffordanceRegistry` — local HARAM/HOLD judgment | 🔴 |
| `router.py` | 1-506 | `route()`, `classify_task()`, `should_stop()` | 🔴 |
| `affordances.yaml` | 498 lines | 39KB local affordance/tool database | 🔴 |
| `organ_affordances.yaml` | — | Local organ governance data | 🔴 |
| `organ_authority_ceilings.yaml` | — | Local authority ceilings | 🔴 |
| `federation_alignment_registry.json` | — | 144KB local governance registry | 🔴 |
| `budgets.yaml` | — | Local budget enforcement | 🔴 |
| `tests.py` | — | Tests for shadow judiciary | 🔴 |

### V2: TypeScript aThinkGuard.ts (555 lines)

**Path:** `/root/A-FORGE/src/domain/governance/aThinkGuard.ts`

**Lines 1-555** — Complete TypeScript port of the Python shadow judiciary. Includes:
- `classifyMode()` (line 146) — local mode classification (FAST/THINK/GOVERN)
- `checkAffordance()` (line 246) — local ALLOW/HOLD/DENY
- `AThinkGuard.check()` (line 341) — full permission gate with budget enforcement
- Session state tracking (lines 364-387)

**ACTIVE INTEGRATION:** Called from `/root/A-FORGE/src/interfaces/mcp/core.ts`:
- Line 584: `const aThinkVerdict = aThinkCheck(name, aThinkUserInput, aThinkSessionId);`
- Line 717: Same call in a second handler path

Both call sites return aThinkErrorResponse if verdict is not allowed — blocking the tool BEFORE any kernel session check or arif_judge call occurs.

### Clean Organs (for reference)

These organs were checked and have NO a_think/ directory:
- `/root/arifOS/a_think/` — **DOES NOT EXIST** ✅ (arifOS IS the judge, uses `arif_think` MCP tool)
- `/root/WEALTH/a_think/` — **DOES NOT EXIST** ✅
- `/root/geox/a_think/` — **DOES NOT EXIST** ✅
- `/root/WELL/a_think/` — **DOES NOT EXIST** ✅
- `/root/AAA/a_think/` — **DOES NOT EXIST** ✅

## Fix

The entire `/root/A-FORGE/a_think/` directory must be deleted. The `aThinkGuard.ts` file must be hollowed to a thin HTTP bridge to `arif_judge` at arifOS:8088.

### Files to DELETE

```
/root/A-FORGE/a_think/                           ← ENTIRE DIRECTORY
├── __init__.py
├── mcp_guard.py                                 ← Shadow judiciary code
├── affordance.py                                ← Local judgment code
├── router.py                                    ← Local classification
├── budgets.yaml                                 ← Local budget enforcement
├── affordances.yaml                             ← Local affordance DB (39KB)
├── organ_affordances.yaml                       ← Local organ governance
├── organ_authority_ceilings.yaml                ← Local authority data
├── federation_alignment_registry.json           ← Local governance DB (144KB)
└── tests.py                                     ← Tests for deleted code
```

### Files to HOLLOW

`/root/A-FORGE/src/domain/governance/aThinkGuard.ts` — Replace all local enforcement with:

```typescript
export function aThinkCheck(
  toolName: string,
  userInput?: string,
  sessionId?: string,
): AThinkVerdict {
  // HTTP bridge to arif_judge — NOT local enforcement
  try {
    const response = await fetch("http://127.0.0.1:8088/arif/judge?mode=intercept", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ intent: userInput, tool_name: toolName, session_id: sessionId }),
      signal: AbortSignal.timeout(5000)
    });
    return await response.json();
  } catch (e) {
    // Fail-open for connectivity issues (arifOS is the judge; if unreachable, allow but log)
    return { allowed: true, status: "ALLOW", reason: "BRIDGE_FALLBACK: arif_judge unreachable", mode: "GOVERN" };
  }
}
```

### Verification

After fix, verify:
```bash
# No a_think directory exists
test -d /root/A-FORGE/a_think/ && echo "STILL EXISTS" || echo "DELETED ✅"

# No local judiciary in aThinkGuard
grep -c "DENY\|HOLD" /root/A-FORGE/src/domain/governance/aThinkGuard.ts
# Should show 0 or only pass-through references
```
