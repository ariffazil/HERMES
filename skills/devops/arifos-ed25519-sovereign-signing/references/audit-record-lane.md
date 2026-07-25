# AUDIT_RECORD Lane & Action Class Policy (2026-07-25)

## The Problem

`arif_judge` with `reversibility_level="FULL"` or any unknown value was silently converted to R4_IRREVERSIBLE, triggering F13. Audit records (evidence seals, report attachments) don't need F13 — they're just appending to VAULT999 without external effect.

## The Fix (NOW DEPLOYED — commit `bbd3a78856c0`)

### 1. Action Class Policy (`_ACTION_CLASS_POLICY` in `arif_kernel_intercept.py`)

```python
"AUDIT_RECORD": {
    "seal_purpose": "RECORD",
    "authority_effect": "NONE",
    "reversibility": "R2",
    "ack_irreversible": False,
    "requires_f13": False,
    "can_retry_autonomously": True,
},
"ACTION_AUTHORIZATION": {
    "seal_purpose": "AUTHORIZE",
    "authority_effect": "EXECUTION_GRANT",
    "reversibility": "R4",
    "ack_irreversible": True,
    "requires_f13": True,
    "can_retry_autonomously": False,
},
```

### 2. Deterministic AUDIT_RECORD normalization

When `action_class == "AUDIT_RECORD"`, the kernel OVERRIDES:
- `reversibility_level = "R2"` (regardless of what caller passed)
- `blast_radius = "ledger"` (or whatever caller passed)
- `seal_purpose = "RECORD"`
- `authority_effect = "NONE"`

This prevents agents from accidentally triggering F13 on audit records.

### 3. Default fallback

`_resolve_action_class()` defaults to AUDIT_RECORD for all non-R4/R5 reversibility values. Unknown reversibility returns CLASSIFICATION_HOLD (not silently converted to R4).

### 4. Canonical judge identity

The ALLOW path now emits:
- `constitutional_chain_id`: `"cc_" + sha256(actor:candidate_hash:judge_state_hash:audit_hash)[:40]`
- `judge_state_hash`: `"sha256:" + sha256(canonical_json(judge_state))`

### 5. Real Ed25519 verification

`_verify_sovereign_token()` now has two paths:
1. **Production** (`ARIFOS_ED25519_ENABLED=true`): Calls `verify_actor_signature()` from `crypto_auth.py`, with a free-nonce fallback that calls `resolve_actor_public_key()` + raw `pubkey.verify()`.
2. **Dev fallback**: Sentinel string comparison (backward compatible).

## How to call (WORKING — tested 2026-07-25)

```python
arif_judge(
    action_class="AUDIT_RECORD",      # ← KEY: triggers R2/RECORD/NONE
    reversibility_level="R2",         # optional, but explicit is better
    seal_purpose="RECORD",            # optional
    authority_effect="NONE",          # optional
    actor_id="arif",
    intent="RECORD SEAL of artifact sha256:8aa47683...",
    session_id="SEAL-...",
    session_token="sct_v1...",
)
```

Returns:
```json
{
    "decision": "ALLOW",
    "constitutional_floor_triggered": null,
    "seal_type": "SEAL_RECORD",
    "seal_purpose": "RECORD",
    "authority_effect": "NONE",
    "requires_human_signature": false,
    "authorized_execution": false,
    "constitutional_chain_id": "cc_5b467fc993b9a95bfc2fcb5e47b416d8472e4724",
    "judge_state_hash": "sha256:bdd5caa7046fc5d7d9eb2f62dd30eefdf2914364cf9f460029622facea68b9eb",
    "audit_hash": "016ed30e450a3e6e"
}
```

## Live Test Results (2026-07-25)

| Test | Result |
|---|---|
| `AUDIT_RECORD` + `R2` → judge → `SEAL_RECORD` | ✅ `ALLOW`, `cc_id` emitted, `judge_state_hash` bound, no F13 |
| `ACTION_AUTHORIZATION` + `R4` + no signature → judge | ✅ `ESCALATE` with `F13` |
| `ACTION_AUTHORIZATION` + `R4` + real Ed25519 sig → judge | ❌ Still `ESCALATE` — ingress middleware strips params, or permission error on DID registry |
| Judge→`arif_seal` with RECORD lane | ❌ F13 blocked — `classify_tool()` treats seal as L5/irreversible regardless of `seal_purpose` |

## Remaining Gaps (P0-P1)

1. **arif_seal ingress L5**: `classify_tool()` still labels `arif_seal` as L5/irreversible regardless of `seal_purpose`. RECORD lane needs ingress policy fix.
2. **Ingress middleware stripping**: `actor_signature` and `nonce` may be stripped if not in the advertised MCP tool schema. The MCP schema for `arif_judge` DOES expose them (confirmed 2026-07-25), but the runtime may still strip them — check with `tools/list` probe.
3. **Direct VAULT999 write path**: `cat >> outcomes.jsonl` bypasses the canonical chain. Must be replaced with governed recovery path.
4. **Permission error on DID registry**: `resolve_actor_public_key()` fails on `/root/secrets/did/registry.json` because the `ariffazil` service user can't traverse `/root/`. Fix: `chmod o+x /root` or add `except PermissionError` in `crypto_auth.py` (patched at line 162).