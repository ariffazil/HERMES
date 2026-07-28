# A-FORGE Execution Binding Contract

## Cross-repo authorization contract

After `arif_judge` returns `ALLOW` with F13 authorization, A-FORGE must verify these bindings before executing.

## Contract fields

| Field | Source (arifOS kernel) | Consumer (A-FORGE) | Required |
|---|---|---|---|
| `constitutional_chain_id` | `KernelOutput.constitutional_chain_id` (`cc_<sha256>`) | `ExecutorReceipt.ccId` | Always |
| `judge_state_hash` | `KernelOutput.judge_state_hash` (`sha256:<hash>`) | `ExecutorReceipt.judge_state_hash` | When `authorization_id` present |
| `authorization_id` | `meta.authorization_id` from `arif_judge` / `verify_judge_signature()` result | `ExecutorReceipt.authorization_id` | When F13 was required |
| `authorization_consumed` | True after `verify_judge_signature()` succeeds | `ExecutorReceipt.authorization_consumed` | When `authorization_id` present |
| `candidate_hash` | `sha256(candidate_string)` computed in judge gate | `ExecutorReceipt.candidate_hash` | When `authorization_id` present |
| `authorized_execution` | True when `authority_effect == "EXECUTION_GRANT"` | Verified in `forgeHandler` | When `authorization_id` present |

## Enforcement points

### 1. `forgeHandler` (core.ts, after SEAL check)

Rejects with `F13_AUTHORIZATION_INCOMPLETE` when:
- `authorization_id` is present but `judge_state_hash` is missing
- `authorization_consumed` is false or absent
- `authorized_execution` is false or absent

### 2. `forgeExecute` (forge.ts, receipt validation gate)

Rejects with `F13 execution binding:` + error list when:
- `authorization_id` present and `authorization_consumed` is falsy (`AUTHORIZATION_NOT_CONSUMED`)
- `authorization_id` present and `judge_state_hash` is missing (`JUDGE_STATE_HASH_MISSING`)
- `authorization_id` present and `candidate_hash` is missing (`CANDIDATE_HASH_MISSING`)

### 3. `forge_execute` input schema (core.ts)

New optional params for the TypeScript MCP tool:
- `authorization_id: z.string().optional()`
- `judge_state_hash: z.string().optional()`
- `candidate_hash: z.string().optional()`

## Backward compatibility

When `authorization_id` is NOT present (existing R0-R3 SEAL-only path):
- No F13 enforcement triggers
- Existing behavior preserved: `ccId` + SEAL verdict is sufficient
- A log warning is emitted to audit trail

## Files changed (A-FORGE repo)

| File | Change |
|---|---|
| `src/executor/types.ts` | Added 6 optional fields to `ExecutorReceipt` |
| `src/executor/forge.ts` | F13 gate after existing verdict check |
| `src/interfaces/mcp/core.ts` | F13 gate after SEAL check + new schema params + candidate enrichment |

Branch: `feat/f13-execution-binding`
Build: `npm run build` passes
