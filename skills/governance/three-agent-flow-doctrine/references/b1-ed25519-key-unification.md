# B1 — Ed25519 Key Unification (2026-07-27)

## Architectural Invariant

**Problem:** Signer and verifier used different keys. `sovereign_signer` signed with hex-encoded private key (fingerprint `679a`), `resolve_actor_public_key()` verified against PEM public key (fingerprint `17d9`). No private key on disk matched any known public key.

**Fix:** Public key derivation chain — signer derives its public key from its loaded private key, passes it through the verification chain. `verify_sovereign_signature(*, public_key_pem=None)` and `verify_init_identity(*, public_key=None)` — both parameters optional for backward compatibility.

## Pattern for Future Key Mismatches

```
signer.get_sovereign_public_key_pem()
    ↓
verify_sovereign_signature(public_key_pem=...)
    ↓
verify_init_identity(public_key=...)
    ↓
signature verification (bypasses actor registry)
```

When a signature fails verification and both sides are Ed25519:
1. Derive public key from the signer's private key
2. Pass derived key to verifier (skip actor registry)
3. If that succeeds — keys were permanently divergent

## Files Modified

- `arifosmcp/runtime/sovereign_signer.py` — core: `get_sovereign_public_key_pem()`
- `arifosmcp/runtime/crypto_auth.py` — signature: `verify_init_identity(*, public_key)`
- `arifosmcp/runtime/sovereign_verify.py` — bridge
- `arifosmcp/runtime/governance_identity.py` — wired
- `arifosmcp/apps/command_center/identities.py` — wired (separate code path)

## Test

```
13/13 tests pass across TestGovernanceIdentityEd25519 + TestCommandCenterIdentityEd25519
```
