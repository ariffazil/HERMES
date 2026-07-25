# Seal Architecture and MCP Ingress Debugging (2026-07-24)

## Summary

This session implemented the RECORD vs AUTHORIZE seal separation across the arifOS kernel intercept, and diagnosed the MCP ingress parameter stripping bug that prevents Ed25519 signature verification from working through the public MCP surface.

## What Was Fixed

### 1. Action Class Policy Table

Added `_ACTION_CLASS_POLICY` to `arif_kernel_intercept.py`:

```python
_ACTION_CLASS_POLICY = {
    "AUDIT_RECORD": {"seal_purpose":"RECORD", "authority_effect":"NONE",
                     "reversibility":"R2", "ack_irreversible":False,
                     "requires_f13":False, "can_retry_autonomously":True},
    "EVIDENCE_ATTESTATION": {...same RECORD...},
    "VAULT_RECEIPT": {...same RECORD...},
    "ACTION_AUTHORIZATION": {"seal_purpose":"AUTHORIZE", "authority_effect":"EXECUTION_GRANT",
                             "reversibility":"R4", "ack_irreversible":True,
                             "requires_f13":True, "can_retry_autonomously":False},
    "CONSTITUTIONAL_AMENDMENT": {"seal_purpose":"AUTHORIZE", "authority_effect":"SOVEREIGN_CHANGE",
                                 "reversibility":"R5", "ack_irreversible":True,
                                 "requires_f13":True, "can_retry_autonomously":False},
}
```

### 2. `_resolve_action_class` (arif_kernel_intercept.py)

New function that maps action_class → policy dict. Explicit class wins, then seal_purpose/authority_effect inference, then reversibility fallback, then defaults to AUDIT_RECORD.

### 3. RECORD Seal Bypass in Vault Seal

The `_arif_vault_seal` function had a direct return for RECORD seals, bypassing the constitutional_chain_id gate. This was replaced with proper chain enforcement — RECORD seals still need cc_id + judge_state_hash, only the F13 check is skipped.

### 4. Ed25519 Direct Verification Path

`_verify_sovereign_token` now does direct Ed25519 verification:

```python
try:
    from arifosmcp.runtime.crypto_auth import resolve_actor_public_key
    from cryptography.exceptions import InvalidSignature
    pubkey = resolve_actor_public_key(actor_id)
    if pubkey is not None:
        sig_bytes = _b64.b64decode(actor_signature)
        payload = f"{actor_id}:{nonce}".encode()
        pubkey.verify(sig_bytes, payload)
        return True
except InvalidSignature:
    logger.warning("F13_ED25519: signature_invalid")
except Exception as e:
    logger.warning("F13_ED25519: verify_exception=%s", e)
```

### 5. Free-Nonce Support in crypto_auth.py

Added `ARIFOS_ALLOW_FREE_NONCE=1` check in `verify_init_identity` to allow signatures without pre-issued challenges.

## What Remains: MCP Ingress Bug

The kernel intercept works correctly when called directly (returns ALLOW with cc_id + js_hash). Through the MCP surface, `actor_id` is stripped by the filter pipeline and `actor` becomes "anonymous".

### Root Cause

`_LEGACY_PARAM_ALIASES["arif_judge"] = {"actor_id": "actor"}` renames `actor_id` to `actor`. The wrapper now has BOTH as named parameters. After renaming, `actor_id` is NOT in filtered kwargs (was renamed). The wrapper's kwarg translation sees `actor_id=None` and falls to "anonymous".

### Attempted Fix

```python
if actor is None or actor == "anonymous":
    actor = actor_id or kwargs.pop("actor_id", None) or "anonymous"
```

But this fix may not have fully propagated to all 4 deployment locations or the .pyc cache may be stale.

### Exact Test That Works (direct kernel)

```python
import asyncio
result = await _arif_kernel_intercept(
    actor="ARIF", reversibility_level="R4",
    action_class="ACTION_AUTHORIZATION",
    actor_signature=sig, nonce=nonce)
# Returns: decision=ALLOW, cc_id=cc_..., js_hash=sha256:...
```

## Key Files

| File | Path | Purpose |
|------|------|---------|
| arif_kernel_intercept.py | `/root/arifOS/arifosmcp/tools/` | Policy table, verify, ALLOW cc_id |
| crypto_auth.py | `/root/arifOS/arifosmcp/runtime/` | Free-nonce support |
| tools.py | `/root/arifOS/arifosmcp/runtime/` | Wrapper, filter, aliases |
| vault_seal handler | tools.py line ~18782 | RECORD bypass |
| boot_attestation.py | `/opt/arifos/app/arifosmcp/runtime/` | BOOT gate demotion fix |

## Environment Vars

| Var | Purpose |
|-----|---------|
| `ARIFOS_ED25519_ENABLED=true` | Enable Ed25519 path (default: true) |
| `ARIFOS_ALLOW_FREE_NONCE=1` | Allow non-pre-issued challenges (dev) |
| `ARIFOS_ARIF_PUBLIC_KEY_PATH` | Path to Arif's Ed25519 public key PEM |
| `ARIFOS_SOVEREIGN_KEY` | Legacy env sentinel (dev-only fallback) |
