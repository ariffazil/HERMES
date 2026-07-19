# A-FORGE Authority Binding Audit — 2026-07-18

## Context

Federation Receipt Proof v1 mission. Goal: prove one governed task can travel through the full arifOS federation (session → GEOX → judgment → A-FORGE → VAULT999 → independent verification) and produce a cryptographically verifiable receipt.

P0-D audit of A-FORGE's authority binding against 8 required fields.

## Findings

### Required Fields vs Current State

| # | Required Field | Status | Implementation | Gap |
|---|---------------|--------|----------------|-----|
| 1 | Actor | ✅ | `ExecutorReceipt.authority.actorId`, `AAEV1.actor_id`, `LeaseRecord.agent_id` | — |
| 2 | Session | ⚠️ PARTIAL | `ExecutorReceipt.authority.sessionId` only | NOT in AAE v1 envelope. Lease has no session binding. |
| 3 | Exact Operation | ✅ | `ExecutorReceipt.toolName`, `actionClassifier.ts` 8-tier | — |
| 4 | Arguments Hash | ✅ | `ExecutorReceipt.inputHash`, `AAEV1.intent_hash` (BLAKE3) | intent_hash covers intent but not exact arguments |
| 5 | Expiry | ✅ | All 3 systems enforce. `forge.ts:163`, `amanahEnvelope.ts:220`, `forgeTools.ts:477` | — |
| 6 | Reversibility Class | ✅ | `ExecutorReceipt.bounds.reversible`, `AAEV1.reversibility` (0.0–1.0) | — |
| 7 | Judgment Reference | ❌ MISSING | No field binds execution to the specific judgment verdict | `ccId` is chain reference, not verdict reference |
| 8 | Single-Use Nonce | ❌ CRITICAL | `AAEV1.nonce` generated but never tracked | No nonce store — replay attacks undetected |

### Critical Gap 1: Nonce Replay

- **Location**: `src/domain/governance/amanahEnvelope.ts` (line 44,168,263)
- **Problem**: Nonce is generated and signed but functionally decorative. No code checks whether a nonce has been used before.
- **Fix needed**: NonceStore class (in-memory Set with TTL or file-backed), check in McpPolicyGate Layer 1b/5, check in lease validation.
- **Files**: `amanahEnvelope.ts`, `McpPolicyGate.ts`, `forgeTools.ts`

### Critical Gap 2: Judgment Reference

- **Location**: `src/executor/types.ts` (ExecutorReceipt), `src/domain/governance/amanahEnvelope.ts` (AAEV1)
- **Problem**: Execution tokens can't prove which judgment authorized them. `ccId` is a chain reference, `seal_verdict_id` exists only on forge_skill forge.
- **Fix needed**: Add `judgment_reference` field to ExecutorReceipt and AAEV1, validate in `forge.ts` validateReceipt() and McpPolicyGate.
- **Files**: `types.ts`, `forge.ts`, `amanahEnvelope.ts`, `McpPolicyGate.ts`

### Session Binding Gap

- AAE v1 has no `session_id` field — session binding missing from AAE
- Leases have no session binding (lease can outlive session)
- Local fallback leases (`LCL-*`) bypass kernel authority

## Three Systems That Bind Authority

1. **ExecutorReceipt** (`src/executor/types.ts` + `src/executor/forge.ts`) — strongest binding surface, 12 hard-fail validation checks
2. **AAE v1** (`src/domain/governance/amanahEnvelope.ts`) — 13-field signed envelope with HMAC-SHA256, BLAKE3 intent hash
3. **Lease System** (`src/interfaces/mcp/forgeTools.ts`) — minted by arifOS kernel, validates scope/revocation/expiry

## Related

- Skill: `arifos-interceptor-patching` — session isolation fix (P0-A)
- Mission: Federation Receipt Proof v1 (2026-07-18)
