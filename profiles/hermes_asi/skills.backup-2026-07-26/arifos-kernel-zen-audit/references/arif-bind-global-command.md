# `arif-bind` Global Command — Sovereign Session Bind

## One-Liner

```bash
arif-bind --mode init --actor arif
```

Output:
```json
{
  "session_id": "SEAL-...",
  "actor_verified": true,
  "authority": "FULL",
  "actor_authority": "SOVEREIGN",
  "identity_verified": true
}
```

## Installation

The wrapper lives at `/usr/local/bin/arif-bind`:

```bash
#!/bin/bash
exec /opt/arifos/venv/bin/python3 /root/.hermes/scripts/arif-bind.py "$@"
```

The Python script at `/root/.hermes/scripts/arif-bind.py` does:
1. `sys.path.insert(0, "/opt/arifos/app")` — kernel path
2. `issue_actor_challenge(actor)` — fresh nonce
3. `key.sign(f"{actor}:{nonce}".encode())` — Ed25519 sign
4. `arif_init(mode, actor, nonce, actor_signature)` — delegate call
5. Extract `session_id`, `actor_verified`, `authority`, `actor_authority`, `identity_verified`

Must use `/opt/arifos/venv/bin/python3` (kernel venv) for imports. Root Python lacks `blake3`.

## Key Paths

| Resource | Path |
|---|---|
| Python script | `/root/.hermes/scripts/arif-bind.py` |
| Global wrapper | `/usr/local/bin/arif-bind` |
| Sovereign PEM key | `/root/.secrets/aaa-identity/keys/arif_private.pem` |
| Kernel venv | `/opt/arifos/venv/bin/python3` |

## Rules

- Nonce is **single-use** — generate + sign + call in one shot
- Never call `verify_init_identity` before `arif_init` — consumes nonce
- Payload format: `{actor_id}:{nonce}` (NOT raw nonce)
- `actor_id="arif"` (lowercase) — kernel normalizes
- Requested authority: `SOVEREIGN`
- `sovereign_id="ARIF_FAZIL"` — principal identity
