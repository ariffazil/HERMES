# AUDIT_RECORD Lane — Deployment Pattern

## Quick Deploy Flow

After editing source files in `/root/arifOS/`, deploy to runtime:

```bash
cd /root/arifOS && make deploy-local
```

What `make deploy-local` does:
1. `rsync` source → `/opt/arifos/app/`
2. `systemctl restart arifos`
3. Conformance spine check (9/9 gates)
4. Verify `drift=false` in the kernel response

## Key Files Modified (2026-07-24/25)

| File | Change |
|------|--------|
| `arifosmcp/schemas/minimum_kernel.py` | Added `constitutional_chain_id`, `judge_state_hash`, `seal_type` to `KernelOutput` |
| `arifosmcp/tools/arif_kernel_intercept.py` | `_verify_sovereign_token()` now does real Ed25519 + free-nonce fallback; `_ACTION_CLASS_POLICY` table; ALLOW path generates `cc_id` + `judge_state_hash`; deterministic AUDIT_RECORD→R2 mapping |
| `arifosmcp/runtime/tools.py` | `_arif_kernel_intercept_tool` handler passes `actor_signature`, `nonce`, `key_id` to kernel |

## Known Gaps After Deploy

1. **Ingress middleware param stripping** — `actor_signature` and `nonce` may be stripped by `IngressToleranceMiddleware` if not in the MCP tool schema. Restart required after param changes.
2. **arif_seal still L5** — `classify_tool()` labels seal as irreversible/L5 regardless of `seal_purpose`. RECORD lane needs separate risk classification.
3. **Direct VAULT write path** — `outcomes.jsonl` can be appended directly. Recovery path needed for governed writes only.