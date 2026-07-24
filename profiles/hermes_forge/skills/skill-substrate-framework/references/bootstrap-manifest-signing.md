# Bootstrap Manifest Signing Pattern

**Proven: 2026-07-11.** Ed25519 signing of JSON manifests for the AAA skill substrate.

## Key Generation

```bash
mkdir -p /root/.secrets/bootstrap
ssh-keygen -t ed25519 -f /root/.secrets/bootstrap/root-arif-888 \
  -C "root-arif-888@arifOS" -N "" -a 100
chmod 600 /root/.secrets/bootstrap/root-arif-888
```

## Manifest Signing (Python, not ssh-keygen -Y)

`ssh-keygen -Y sign` is unreliable for JSON content. Use Python cryptography directly:

```python
import json, hashlib, base64
from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_ssh_public_key

# Load key
with open("/root/.secrets/bootstrap/root-arif-888", "rb") as f:
    priv = load_ssh_private_key(f.read(), password=None)

# Compute content hash (BEFORE adding signature)
with open("BOOTSTRAP_MANIFEST.json", "rb") as f:
    manifest_bytes = f.read()
content_hash = hashlib.sha256(manifest_bytes).hexdigest()

# Sign the hash STRING (not bytes)
sig = priv.sign(content_hash.encode())
sig_b64 = base64.b64encode(sig).decode()

# Update manifest
manifest = json.loads(manifest_bytes)
manifest["signatures"] = [{
    "key_id": "root-arif-888",
    "algorithm": "ed25519",
    "signature": sig_b64,
    "signed_at": "2026-07-11T08:19:00Z",
    "covers": "full_manifest"
}]
manifest["status"] = "SIGNED"

with open("BOOTSTRAP_MANIFEST.json", "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
```

## Verification

```python
content_hash = manifest["content_hash"].replace("sha256:", "")
sig = base64.b64decode(manifest["signatures"][0]["signature"])

with open("/root/.secrets/bootstrap/root-arif-888.pub", "rb") as f:
    pub = load_ssh_public_key(f.read())

pub.verify(sig, content_hash.encode())  # raises InvalidSignature if bad
```

## Pitfall: content_hash changes after signing

The content_hash is computed BEFORE the signature is added. After adding the
signature, the file hash is different. This is expected. The signature is over
the STORED content_hash, not the current file.

## Pitfall: ssh-keygen -Y verify fails

`ssh-keygen -Y verify` requires exact file content match. If you signed with
Python but try to verify with ssh-keygen, it will fail. Use Python for both.

## Files

- Private key: `/root/.secrets/bootstrap/root-arif-888` (chmod 600)
- Public key: `/root/.secrets/bootstrap/root-arif-888.pub`
- Signing script: `/root/AAA/scripts/sign-manifest.sh`
