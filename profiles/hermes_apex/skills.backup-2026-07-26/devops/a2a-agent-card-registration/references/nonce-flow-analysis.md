# Nonce Flow Analysis — Ed25519 Sovereign Identity (2026-07-13)

> **Crisis:** `challenge_replayed` error when authenticating as sovereign.
> **Root cause:** `verify_init_identity` was being called BEFORE `arif_init`, consuming the nonce. `arif_init` then tried to use the same nonce → REPLAYED.
> **Fix confirmed:** Kernel ordering is ALREADY correct. Bug was in a specific caller path.

## The Correct Flow

```
RIGHT:  nonce → arif_init(nonce) → stores nonce as pending → verify(nonce, sig) → FULL
WRONG:  nonce → verify(nonce, sig) → CONSUMES nonce → arif_init(nonce) → REPLAYED
```

## Kernel Code Paths (All Correct)

The arifOS kernel has the nonce verification INSIDE `arif_init`:

1. **`tools/session.py:1234` (light mode)** — `verify_init_identity` called inside `_light_session_init` which IS `arif_init`
2. **`tools/session.py:1519` (full mode)** — inside `_init_session_full`
3. **`runtime/tools.py:7928` (HMAC path)** — inside inline `arif_session_init`
4. **`runtime/tools.py:7963` (Ed25519 path)** — inside inline `arif_session_init`

All four paths verify identity INSIDE session initialization, not before it.

## The Bug Path (Caller Issue)

The `challenge_replayed` error occurred because a specific caller flow:

```python
# 1. Generate nonce
nonce = generate_nonce()

# 2. Call verify_init_identity FIRST — BUG: consumes nonce
verify_init_identity(nonce=nonce, signature=sig)

# 3. Call arif_init — nonce already consumed, REPLAYED
arif_init(nonce=nonce)
```

The fix: ensure `arif_init` is called first (it handles nonce internally), OR use the `actor_signature` parameter of `arif_init` which correctly chains the verification:

```python
# CORRECT: single call, nonce handled internally
result = arif_init(
    actor_id="ARIF",
    nonce=nonce,
    actor_signature=signature,
    mode="init"
)
```

## SOVEREIGN_KEY_IDS

Located at `/root/arifOS/arifosmcp/runtime/governance_identity.py:44`:
```python
SOVEREIGN_KEY_IDS: set[str] = {
    # Empty by design — sovereign must explicitly populate
    # Inject the DID public key fingerprint here
}
```

The check in `authority.py:95`:
```python
from arifosmcp.runtime.governance_identity import SOVEREIGN_KEY_IDS
# ...
if state.actor.verified and verified_key_id and verified_key_id in SOVEREIGN_KEY_IDS:
    # This actor is SOVEREIGN (F13 authority)
```

**Empty SOVEREIGN_KEY_IDS = no actor gets SOVEREIGN band = all actors are OPERATOR.** Fix by injecting the DID key fingerprint from `arif-fazil.com/.well-known/did.json`.

## Quick Test

```bash
# Test nonce flow
python3 -c "
from arifosmcp.runtime.tools import _init_identity
# Call arif_init FIRST, nonce handled internally
result = _init_identity(mode='init', actor_id='ARIF')
print(f'Nonce: {result.get(\"nonce\",\"N/A\")}')
"
```

## The Sovereign Chain (Complete)

```
000 (arif-fazil.com/000/)
  └─ DID document (/.well-known/did.json)
       └─ Ed25519 public key
            └─ SOVEREIGN_KEY_IDS (kernel config)
                 └─ arif_init(nonce, signature) → FULL authority
                      └─ Actions sealed at 999 (arif-fazil.com/999/)
                           └─ VAULT999 (seal_chain.jsonl, seq=61)
```

Any break in this chain → OBSERVE_ONLY authority. All links must be live for SOVEREIGN.
