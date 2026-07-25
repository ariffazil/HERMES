# F13 Execution Binding Gate Pattern

F13 (SOVEREIGN) mandates that every execution trace back to an explicit
authorization from arif_judge. The F13 execution binding gate enforces this
by verifying that when `authorization_id` is present on an execution token,
all binding fields are present and internally consistent.

## Architecture

The F13 gate operates at TWO layers:

```
arif_judge (Python kernel)
   │  issues authorization_id + judge_state_hash + authorized_execution
   ▼
Layer 1: forgeHandler (core.ts) — MCP tool handler gate
   │  verifies: judge_result has authorization_id → judge_state_hash + authorization_consumed + authorized_execution
   ▼
Layer 2: forgeExecute (forge.ts) — execution engine gate
   │  verifies: receipt has authorization_id → candidate_hash + judge_state_hash + authorization_consumed
   ▼
Execution
```

### Layer 1 (MCP Handler Gate)

Location: `src/interfaces/mcp/core.ts` — `forgeHandler()`, after the SEAL verdict check,
before the Landauer gate.

Triggers when `judgeResult.authorization_id` is present. Refuses with
`F13_AUTHORIZATION_INCOMPLETE` if any of `judge_state_hash`, `authorization_consumed`,
or `authorized_execution` is missing.

```typescript
if (judgeResult?.authorization_id) {
  if (!judgeResult?.judge_state_hash || !judgeResult?.authorization_consumed || !judgeResult?.authorized_execution) {
    return {
      content: [{ type: "text" as const, text: JSON.stringify({
        status: "ERROR",
        error_code: "F13_AUTHORIZATION_INCOMPLETE",
        source_layer: "A-FORGE::F13_GATE",
        gate: "F13_EXECUTION_BINDING",
        missing: [
          !judgeResult?.judge_state_hash && "judge_state_hash",
          !judgeResult?.authorization_consumed && "authorization_consumed",
          !judgeResult?.authorized_execution && "authorized_execution",
        ].filter(Boolean),
        reason: "arif_judge returned authorization_id but binding fields incomplete",
      }, null, 2) }],
      isError: true,
    };
  }
}
```

### Layer 2 (Execution Engine Gate)

Location: `src/executor/forge.ts` — `forgeExecute()`, after the SEAL/SABAR verdict
check, before action execution.

Triggers when `receipt.authorization_id` is present. Collects all violations then
returns REFUSED with structured error codes.

```typescript
const f13Errors: string[] = [];
if (receipt.authorization_id && !receipt.authorization_consumed) {
  f13Errors.push("AUTHORIZATION_NOT_CONSUMED");
}
if (receipt.ccId && receipt.authorization_id && !receipt.judge_state_hash) {
  f13Errors.push("JUDGE_STATE_HASH_MISSING");
}
if (receipt.authorization_id) {
  if (!receipt.candidate_hash) f13Errors.push("CANDIDATE_HASH_MISSING");
  if (!receipt.judge_state_hash) f13Errors.push("JUDGE_STATE_HASH_MISSING");
  if (!receipt.authorization_consumed) f13Errors.push("AUTHORIZATION_NOT_CONSUMED");
}
if (f13Errors.length > 0) {
  return {
    receipt, results: [],
    summary: { totalActions: 0, succeeded: 0, failed: 0, totalDurationMs: 0, verdict: "REFUSED" },
    refusalReasons: [`F13 execution binding: ${f13Errors.join(", ")}`],
    timestamp: new Date().toISOString(),
  };
}
```

## Fields (on ExecutorReceipt)

| Field | Type | Required When | Source |
|-------|------|---------------|--------|
| `authorization_id` | `string` (optional) | — | arif_judge response |
| `judge_state_hash` | `string` (optional) | authorization_id present | arif_judge response |
| `candidate_hash` | `string` (optional) | authorization_id present | computed from candidate JSON |
| `plan_id` | `string` (optional) | — | plan reference |
| `authorization_consumed` | `boolean` (optional) | authorization_id present | arif_judge response |
| `target_environment` | `string` (optional) | — | deployment context |

## Backward Compatibility

The F13 gate is **inert** when `authorization_id` is absent. Existing SEAL-only
execution paths (without F13 binding) pass through unaffected. The gate only
activates when the judge explicitly returns an authorization.

## Cross-Cutting Change Pattern

Adding F13 fields follows the same dependency order as any cross-cutting
interface change in A-FORGE (see `references/cross-cutting-interface-change.md`):

1. `src/executor/types.ts` — Add optional fields to `ExecutorReceipt`
2. `src/executor/forge.ts` — Add validation gate consuming those fields
3. `src/interfaces/mcp/core.ts` — Add handler gate + inputSchema + candidate wiring
4. `npm run build` — Verify compilation

## Pitfalls

### Spec vs Interface: Naming Mismatch

The receipt field for constitutional chain ID is `ccId`, NOT `constitutional_chain_id`.
When checking `receipt.ccId && receipt.authorization_id && !receipt.judge_state_hash`,
use `ccId` or the TypeScript compiler will error.

### F13 Gate Ordering

The F13 gate in `forgeHandler()` (Layer 1) must come AFTER the SEAL verdict check
(no point checking authorization on a HOLD/VOID) and BEFORE the Landauer gate
(thermodynamic pre-check should not run on un-authorized executions).

In `forgeExecute()` (Layer 2), the F13 gate must come AFTER the SEAL/SABAR verdict
check and BEFORE action execution.

### Candidate JSON Propagation

When adding F13 fields to the `forge_execute` tool, they must be threaded through:
1. `forgeHandler` destructuring (`authorization_id, judge_state_hash, candidate_hash`)
2. Candidate JSON construction (spread only when present)
3. `inputSchema` registration (zod optional fields)
4. Judge body construction (passed as session_id/actor_id alongside)

Missing any link means the field is accepted but silently dropped.
