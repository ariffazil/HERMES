# Path 1 Audit — cc_id/seal_verdict_id FORGERY

**Spec:** EXTERNAL_FALSIFICATION_SPEC.md Path 1  
**Date:** 2026-07-25  
**Files audited:** forge.py (704L), forge_preflight.py (1273L), tools.py (24560L), sct.py (919L)

## Verdict Summary

| Test | Description | Verdict | Risk |
|------|-------------|---------|------|
| 1.1 | Absent seal | ✅ PASS | Low |
| 1.2 | Well-formed but unsigned seal | ⚠️ BOUNDARY-STRENGTH ONLY | Medium |
| **1.3** | **Replay across actions (binding test)** | **❌ FAIL** | **Critical** |
| **1.4** | **Replay of a spent seal (nonce test)** | **❌ FAIL** | **Critical** |
| 1.5 | Single-byte tamper | ✅ PASS | Low |
| **1.6** | **Cross-session lift** | **❌ FAIL** | **High** |

**Overall: BOUNDARY BREACHED** — 3/6 tests fail.

## Five Structural Failures

### 1. Registry-based, not signature-based
`_JUDGE_STATE_REGISTRY.get(hash) != None` — dictionary lookup, not Ed25519 signature.
**File:** tools.py:5818, forge_preflight.py:263-271.

### 2. No one-time use for seals
`_JUDGE_STATE_REGISTRY` is append-only, never pruned. Nonce consumption exists for `actor_signature` path only, not for `judge_state_hash`.
**File:** tools.py:5818 (no deletion path), forge_preflight.py:420 (only tracks vault_entry_id, not judge_state_hash).

### 3. No cryptographic action binding
Seal hash is SHA256 of contract creation parameters (session, actor, candidate, verdict). No field binds it to the forge action (mode + manifest + plan_id). A seal from a benign read verdict authorizes any forge action.
**File:** forge_preflight.py:1163-1171 (stage_08 checks plan→manifest binding, NOT action→seal binding).

### 4. Fail-open import fallback
When `forge_preflight.py` fails to import, ALL 12 gates hardcode to True (tools.py:19148-19160). Downstream gates (side_effect, self_auth, lease, plan, kernel, judge_contract) provide defense-in-depth, but the preflight layer is completely bypassed.
**File:** tools.py:19148-19160.

### 5. Ed25519 check runs AFTER execution
Per-call signature verification at forge.py:607-646 runs AFTER execution at line 533. It can only modify metadata — cannot prevent the execution.
**File:** forge.py:533 vs 607.

## The actor_signature Path

Ed25519 per-call signature path exists (forge.py:606-646) but is:
- Marked "RESERVED — not yet enforced" (forge.py:67-71)
- Only fires when BOTH `actor_signature AND nonce` are provided
- Verifies over (nonce:actor_id:mode) — NOT over the full action payload
- Runs AFTER execution, not before

## Fix Priority

1. **P0** — Move Ed25519 verification before execution. Remove the "RESERVED" marker.
2. **P0** — Add action-hash binding: include `forge_action_hash = SHA256(mode + manifest + plan_id)` in the seal contract, verify at forge gate.
3. **P1** — Add nonce consumption for judge_state_hash (`_CONSUMED_SEAL_HASHES` parallel to `_CONSUMED_VAULT_RECEIPTS`).
4. **P1** — Replace ImportError fallback with fail-closed (HOLD, not PASS).
5. **P2** — Partition registry by session_id. Add TTL to entries.
