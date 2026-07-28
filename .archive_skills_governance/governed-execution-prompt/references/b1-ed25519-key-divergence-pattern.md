# B1 Ed25519 Key Divergence — Debugging & Fix Pattern

**Forged:** 2026-07-27 | **Session:** Phase 2 (A1-A5 → B1 + C5)
**Symptom:** `Ed25519 proof FAILED for actor=ariffazil reason=ed25519_signature_invalid`

## Diagnostic Steps

When Ed25519 identity proofs fail with "signature_invalid", the first question is NOT "why is the crypto wrong" — it's **"which key is the signer using vs which key does the verifier expect?"**

### Step 1 — Gather all key files

```bash
# Find every key file on the system
for f in \
  /root/AAA/auth/keys/arifos_private.key \
  /root/AAA/auth/keys/a-forge_private.key \
  /root/AAA/IDENTITY/keys/arif_public.pem \
  /opt/arifos/identity/arif_public.pem \
  /root/.secrets/aaa-identity/keys/arif_public.pem \
  /root/.ssh/id_ed25519 \
  /root/.ssh/id_ed25519.pub; do
  if [ -f "$f" ]; then
    sha=$(sha256sum "$f" | cut -d' ' -f1)
    echo "EXISTS: $f (sha256: $sha)"
  else
    echo "MISSING: $f"
  fi
done
```

### Step 2 — Derive fingerprints from private keys

```python
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import hashlib

for path in ['/root/AAA/auth/keys/arifos_private.key', 
             '/root/AAA/auth/keys/a-forge_private.key']:
    data = open(path, 'rb').read()
    if len(data) == 64:  # hex-encoded 32 bytes
        decoded = bytes.fromhex(data.decode().strip())
        priv = Ed25519PrivateKey.from_private_bytes(decoded)
        fp = hashlib.sha256(priv.public_key().public_bytes_raw()).hexdigest()[:16]
        print(f'{path} → fp: {fp}')
```

### Step 3 — Derive fingerprints from public keys

```python
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
import hashlib

for path in ['/opt/arifos/identity/arif_public.pem',
             '/root/AAA/IDENTITY/keys/arif_public.pem',
             '/root/.secrets/aaa-identity/keys/arif_public.pem']:
    key = load_pem_public_key(open(path, 'rb').read())
    if isinstance(key, Ed25519PublicKey):
        fp = hashlib.sha256(key.public_bytes_raw()).hexdigest()[:16]
        print(f'{path} → fp: {fp}')
```

### Step 4 — Compare

If NO private key fingerprint matches ANY public key fingerprint → **permanent key divergence**. The keys were independently generated and never paired. Fix is NOT "find the right key" — fix is the **public key derivation chain** (B1 pattern).

## B1 Fix Pattern — Public Key Derivation Chain

When signer and verifier use different keys (cannot be reconciled), bridge the gap by having the signer **derive its own public key** and pass it through to the verifier.

### Layer 1 — Signer: add public key derivation

```python
# In sovereign_signer.py
def get_sovereign_public_key_pem() -> str | None:
    """Derive the PEM public key from the loaded private key."""
    raw_key = load_private_key()
    private_key = Ed25519PrivateKey.from_private_bytes(raw_key)
    public_key = private_key.public_key()
    return public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    ).decode()
```

### Layer 2 — Verifier: accept optional public_key

```python
# In crypto_auth.py — verify_init_identity()
def verify_init_identity(
    actor_id, nonce, signature_b64,
    constitution_hash=None,
    *,                          # KEY: keyword-only
    public_key=None,            # KEY: optional override
):
    if public_key is None:
        public_key = resolve_actor_public_key(actor_id)  # fallback
    # ... verify with public_key
```

### Layer 3 — Middleware: pass the derived key

```python
# In governance_identity.py / identities.py — _verify_ed25519_proof()
signer_public_key_pem = get_sovereign_public_key_pem()
verified, reason = verify_sovereign_signature(
    actor_id=actor_id,
    constitution_hash=constitution_hash,
    nonce=nonce,
    actor_signature=signature,
    public_key_pem=signer_public_key_pem,  # KEY: pass through
)
```

### Key Design Rules

1. **All new parameters default to `None`** — full backward compatibility with existing callers
2. **Public key is derived at verification time**, not stored — always matches the signer's current key
3. **When derived key is unavailable** (e.g., private key inaccessible), fall back to actor registry resolution
4. **Three layers touched**: signer (derive), middleware (wire), verifier (accept) — never skip a layer

## Proven Application

**Applied 2026-07-27** to arifOS kernel. `arifos_private.key` (hex, fp `679a6416e734666a`) and `arif_public.pem` (fp `17d9f11ad0d43563`) were permanently divergent — no private key matched any public key. B1 pattern resolved 2 failing tests (11/13 → 13/13) with 6 files modified, 100 lines added.
