# AUDIT_RECORD Lane — Action Class Policy (2026-07-25)

## What it is

The `_ACTION_CLASS_POLICY` table in `arif_kernel_intercept.py` separates **record seals** (audit evidence, R2, autonomous) from **authorization seals** (execution grants, R4/R5, requires F13 Ed25519).

## The policy table

```python
_ACTION_CLASS_POLICY = {
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
    "CONSTITUTIONAL_AMENDMENT": {
        "seal_purpose": "AUTHORIZE",
        "authority_effect": "SOVEREIGN_CHANGE",
        "reversibility": "R5",
        "ack_irreversible": True,
        "requires_f13": True,
    },
}
```

## Resolution logic

`_resolve_action_class(action_class, reversibility_level, seal_purpose, authority_effect)`:

1. **Explicit action_class wins** — if `action_class` is in `_ACTION_CLASS_POLICY`, use it
2. **seal_purpose inference** — if `seal_purpose == "AUTHORIZE"` or `authority_effect != "NONE"`, → `ACTION_AUTHORIZATION`
3. **Reversibility fallback** — R4/R5/IRREVERSIBLE/SOVEREIGN → `ACTION_AUTHORIZATION`
4. **Default** — everything else → `AUDIT_RECORD` (R2, autonomous, no F13)

## Two paths

### AUDIT_RECORD (autonomous, no F13)

```
arif_judge(action_class="AUDIT_RECORD", reversibility="R2")
→ ALLOW + SEAL_RECORD
→ arif_seal(ack_irreversible=False, seal_purpose="RECORD")
→ VAULT999
```

### ACTION_AUTHORIZATION (requires F13 Ed25519)

```
arif_judge(reversibility="R4")
→ ESCALATE + F13
→ Ed25519 sign → arif_judge → SEAL_AUTHORIZATION
→ arif_seal(ack_irreversible=True)
→ VAULT999
```

## Files involved

| File | What to patch |
|---|---|
| `/root/arifOS/arifosmcp/tools/arif_kernel_intercept.py` | `_ACTION_CLASS_POLICY`, `_resolve_action_class`, `_verify_sovereign_token`, ALLOW path (cc_id + judge_state_hash) |
| `/root/arifOS/arifosmcp/runtime/tools.py` | `_arif_kernel_intercept_tool` (kwarg extraction), `_arif_vault_seal` (RECORD bypass), `_elicit_irreversible_ack` (seal_purpose handling) |

## Known gaps

1. **Ingress middleware stripping:** `actor_signature`, `nonce`, `key_id` may be stripped by MCP middleware if not in the advertised tool schema. Workaround: Use `authority_token` parameter instead, or call via REST API directly.

2. **Editable install:** Python loads from `/root/arifOS/` (source), NOT `/opt/arifos/app/` (deployment). Patches to `/opt/arifos/app/` are silently ignored. Always patch the source tree at `/root/arifOS/`.

3. **Nonce must be pre-issued:** `verify_actor_signature` calls `_consume_actor_challenge` which requires the nonce to be issued by `issue_actor_challenge()`. Free-standing nonces are rejected.

## Test results (2026-07-25)

| Test | Result |
|---|---|
| `AUDIT_RECORD` + `R2` → arif_judge → ALLOW, SEAL_RECORD | ✅ |
| `AUDIT_RECORD` → arif_seal(ack_irreversible=False) → VAULT999 | ✅ |
| `R4` old behavior → ESCALATE F13 | ✅ |
| `R4` + Ed25519 signature → ALLOW (direct call) | ✅ |
| `R4` + Ed25519 signature → ESCALATE (via MCP, middleware stripping) | ⚠️ |