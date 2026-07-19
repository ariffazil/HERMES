# Ed25519 Sovereign Identity — Key Locations & Verification Flow

## Key Locations

| File | Contains | Matches Kernel? |
|---|---|---|
| `/root/compose/sekrits/arifos_sovereign.pub` | Public key (PEM Ed25519) | ✅ YES |
| `/root/AAA/IDENTITY/keys/arif_public.pem` | Public key (PEM Ed25519) | ✅ YES |
| `/root/.secrets/aaa-identity/keys/arif_private.pem` | **Private key** (PEM Ed25519) | ✅ YES |
| `/root/.ssh/operator_did_ed25519` | Private key (OpenSSH Ed25519) | ❌ NO — different key |

**PITFALL:** SSH key derives to `eVHIEJ...`, kernel expects `3F929mO...`. Always use `arif_private.pem`.

## Two Verification Paths

| Path | Function | constitution_hash format | TTL |
|---|---|---|---|
| 1 (session.py) | `crypto_auth.verify_init_identity()` | `arifos-constitution-v2026.05.05-SSCT` (string) | 120s |
| 2 (tools.py bridge) | `governance_identity._verify_ed25519_proof()` | `sha256:612c5a...` (from `get_constitution_hash()`) | 300s |

Path 1 tries 4 payload formats: `{actor_id}:{nonce}`, `{norm}:{nonce}`, `{actor_id}:{hash}:{nonce}`, `{norm}:{hash}:{nonce}`.

## How to Sign

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

with open('/root/.secrets/aaa-identity/keys/arif_private.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Path 1 (recommended): payload = f'ARIF:{nonce}'.encode()
# Path 2: payload = f'ARIF:{get_constitution_hash()}:{nonce}'.encode()

signature = base64.b64encode(private_key.sign(payload)).decode()
```

## Fixes Applied (2026-07-11)

1. **`is_challenge_fresh`** — returned False for plain tokens. Fixed to return True (freshness by crypto_auth store).
2. **`_verify_ed25519_proof` bridge** — added in tools.py after delegate returns.
3. **`select_philosophy_state`** — added to philosophy_registry.py.
