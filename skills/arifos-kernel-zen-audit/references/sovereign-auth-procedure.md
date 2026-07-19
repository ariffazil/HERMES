# Sovereign Authentication Procedure — arifOS Kernel

## Signing Payload Format

The kernel's `verify_init_identity()` tries multiple payload formats (first match wins):

1. `{actor_id}:{nonce}` — **crypto_auth canonical** (primary)
2. `{actor_id}:{constitution_hash}:{nonce}` — kernel /identity/verify compat
3. Normalized actor variants (lowercase, alias mappings)

**Always sign format 1 unless explicitly told otherwise.**

## Critical Pitfall: Nonce Single-Use

Nonces are single-use. `issue_actor_challenge()` stores the nonce. `verify_init_identity()` consumes it via `_consume_actor_challenge()`. If you:

1. Generate nonce
2. Sign it
3. Test locally with `verify_init_identity()` ← **CONSUMES the nonce**
4. Call `arif_init` via MCP ← nonce is now `challenge_replayed`

**The fix:** Generate + sign + call `arif_init` in ONE script. Never test locally first.

## One-Shot Signing Script

```python
import base64, sys
sys.path.insert(0, "/opt/arifos/app")
from arifosmcp.runtime.crypto_auth import issue_actor_challenge
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Generate + store nonce
nonce = issue_actor_challenge("arif")

# Sign {actor_id}:{nonce}
with open("/root/.secrets/aaa-identity/keys/arif_private.pem", "rb") as f:
    key = load_pem_private_key(f.read(), password=None)
sig = key.sign(f"arif:{nonce}".encode())
sig_b64 = base64.b64encode(sig).decode()

# Output for immediate MCP call
print(f"NONCE={nonce}")
print(f"SIG={sig_b64}")
# → Call arif_init(actor_id="arif", nonce=nonce, actor_signature=sig_b64) IMMEDIATELY
```

## Debugging: Failure Mode Reading

| Error | Meaning | Fix |
|---|---|---|
| `challenge_replayed` | Nonce was consumed (by local test or prior call) | Fresh nonce, no intermediate test |
| `ed25519_signature_invalid` | Wrong payload format or wrong key | Check payload is `{actor_id}:{nonce}` |
| `public_key_unavailable` | Key not found at expected path | Check `/root/compose/sekrits/arifos_sovereign.pub` |
| `actor_id_missing` / `nonce_missing` / `signature_missing` | Params not reaching delegate | Check MCP wire splice (actor_signature → signature) |

## Architecture: Two Verification Paths

1. **Delegate** (`session.py` line 1502): `verify_init_identity()` via `crypto_auth`
2. **Bridge** (`tools.py` line 7705): `_verify_ed25519_proof()` via `governance_identity`

Both exist. The delegate runs first (inside session creation). The bridge runs after (as upgrade attempt). If delegate verifies, bridge is redundant.

## Wire Splice (Confirmed 2026-07-12)

- MCP tool parameter: `actor_signature`
- Delegate parameter: `signature`
- Mapping: `tools.py` line 7683: `signature=actor_signature`
- Status: **WORKING** — confirmed with session SEAL-95fa4be4618b4ead (SOVEREIGN bound)

## Session Binding Result (Successful)

```
actor_verified: true
authority: FULL
verdict: SEAL
identity_level: SOVEREIGN
verification_method: signature
mutation_allowed: true
seal_allowed: true
allowed_next_verbs: arif_observe, arif_think, arif_route, arif_judge, arif_forge, arif_seal
```
