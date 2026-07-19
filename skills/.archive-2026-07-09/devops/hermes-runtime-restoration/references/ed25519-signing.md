# Ed25519 Signing for Key Rotation

## The Trap

Ed25519 does NOT support explicit digest selection. Using `openssl dgst -sha256 -sign` with an Ed25519 key fails:

```
Error: ed25519_digest_signverify_init:invalid digest
Explicit digest not allowed with EdDSA operations
```

## The Fix

Use `openssl pkeyutl` instead — Ed25519 handles its own hashing internally:

```bash
# Sign
openssl pkeyutl -sign -inkey private.key -in document.json -out document.sig

# Verify
openssl pkeyutl -verify -pubin -inkey public.key -in document.json -sigfile document.sig
```

## Key Generation

```bash
openssl genpkey -algorithm ed25519 -out private.key
openssl pkey -in private.key -pubout -out public.key
```

## Key Rotation Workflow

1. Generate new keypair
2. Quarantine old key (rename with `.COMPROMISED_PEM_EXPOSED` suffix)
3. Sign rotation_event.json with new private key
4. Re-sign AGENTS.md with new key
5. Update MANIFEST.md with new public key location + sha256
6. Append rotation seal to VAULT999
7. Verify: `openssl pkeyutl -verify` must return "Signature Verified Successfully"

## Signature Size

Ed25519 signatures are always 64 bytes regardless of input size.

## Reference

- OpenSSL EdDSA docs: `openssl pkeyutl -help`
- Rotation policy: `/root/A-FORGE/governance/KEY_ROTATION_POLICY.md`
- Rotation event schema: `/opt/arifos/secrets/rotation_event_2026-07-05.json`
