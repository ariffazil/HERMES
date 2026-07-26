# Ed25519 Identity Setup for arifOS Sovereign Authority

> **Purpose:** The exact workflow for generating, registering, and using Ed25519 identity to get SOVEREIGN authority in arifOS sessions.

---

## The Problem

`arif_init` returns `OBSERVE_ONLY` authority for all sessions. To get `SOVEREIGN` authority (required for VAULT999 seals, irreversible mutations, constitutional changes), the kernel requires Ed25519 identity verification.

## What's Already in the Kernel

| Component | Location | Status |
|---|---|---|
| Ed25519 exempt actors | `session_auth.py:55` | `arif` = sovereign, `a-forge` = operator |
| `verify_init_identity()` | `crypto_auth.py:257` | Verifies `{actor_id}:{nonce}` signature |
| `classify_actor_band()` | `crypto_auth.py:359` | arif + verified = SOVEREIGN |
| `resolve_actor_public_key()` | `crypto_auth.py` | Reads from agent_identities.json |
| Agent registry | `/root/A-FORGE/data/agent_identities.json` | arif registered with Ed25519 public key |

## Step-by-Step Setup

### 1. Generate Ed25519 Keypair

```bash
mkdir -p /root/A-FORGE/IDENTITY/keys/arif
openssl genpkey -algorithm Ed25519 -out /root/A-FORGE/IDENTITY/keys/arif/arif_ed25519_private.pem
openssl pkey -in /root/A-FORGE/IDENTITY/keys/arif/arif_ed25519_private.pem -pubout -out /root/A-FORGE/IDENTITY/keys/arif/arif_ed25519_public.pem
chmod 600 /root/A-FORGE/IDENTITY/keys/arif/arif_ed25519_private.pem
```

### 2. Register Public Key in agent_identities.json

```python
import json
from pathlib import Path

registry_path = Path("/root/A-FORGE/data/agent_identities.json")
registry = json.loads(registry_path.read_text())
pubkey_pem = Path("/root/A-FORGE/IDENTITY/keys/arif/arif_ed25519_public.pem").read_text().strip()

registry["arif"] = {
    "agent_id": "arif",
    "agent_type": "sovereign",
    "role": "sovereign_principal",
    "identity_proof": {"type": "ed25519", "public_key_pem": pubkey_pem},
    "trust_tier": "OBSERVED"
}
registry_path.write_text(json.dumps(registry, indent=2))
```

### 3. Sign Challenge Nonce

```python
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

with open("/root/A-FORGE/IDENTITY/keys/arif/arif_ed25519_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Payload format: {actor_id}:{nonce}
payload = f"arif:{nonce}".encode()
signature_b64 = base64.b64encode(private_key.sign(payload)).decode()
```

### 4. Call arif_init with Nonce + Signature

```
arif_init(actor_id="arif", nonce="<nonce>", actor_signature="<signature_b64>")
```

## CRITICAL PITFALL (2026-07-11)

**`arif_init` MCP tool defaults to "light" mode regardless of parameters.**

The `actor_signature` and `nonce` parameters are accepted but NOT processed — the tool always takes the "light" path which mints an OBSERVE_ONLY SCT.

**What's needed:** `arif_init` tool must call `verify_init_identity()` when `actor_signature` is provided. One-line wiring fix.

**Current state:**
- Keypair: generated at `/root/A-FORGE/IDENTITY/keys/arif/`
- Registry: arif registered with Ed25519 public key
- crypto_auth: `classify_actor_band("arif", True)` returns SOVEREIGN
- Tool wiring: `arif_init` does NOT call `verify_init_identity()` on MCP path

## Verification

```bash
ls -la /root/A-FORGE/IDENTITY/keys/arif/
python3 -c "import json; r=json.load(open('/root/A-FORGE/data/agent_identities.json')); print(r['arif']['identity_proof']['type'])"
python3 -c "from arifosmcp.runtime.crypto_auth import classify_actor_band; print(classify_actor_band('arif', True))"
```

---

*Created 2026-07-11. Keypair generated and registered. Tool wiring pending.*
