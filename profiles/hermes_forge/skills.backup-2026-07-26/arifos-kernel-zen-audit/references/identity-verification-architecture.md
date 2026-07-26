# arifOS Kernel Identity Verification Architecture

> Reference for auditing `arif_init` Ed25519 sovereign identity flow.
> Proven 2026-07-11 when wiring MCP `actor_signature`+`nonce` to `_verify_ed25519_proof`.

## Delegation Pattern (Critical for Auditing)

`_arif_session_init` in `tools.py` has TWO code paths:

### Path 1: Delegation (ACTIVE for mode="init")
```
line ~7313: if mode in {"ping","discover","birth","init_light","light","full","audit","init"}:
    → delegates to session.py's arif_init
    → returns immediately (line ~7340)
    → embodied path (Path 2) is NEVER reached for mode="init"
```

### Path 2: Embodied (DEAD CODE for mode="init")
```
line ~7484: if normalized_mode == "init":
    → has its own HMAC + Ed25519 verification (lines ~7518-7594)
    → calls sovereign_verify.verify_sovereign_signature directly
    → NEVER EXECUTED because Path 1 catches "init" first
```

**Audit implication**: Any identity verification fix in the embodied path (Path 2) has ZERO effect on `mode="init"` calls. Fixes must go in the delegation path.

## Two Verification Paths

### Path A: `crypto_auth.verify_init_identity` (used by session.py)
- Location: `arifosmcp/runtime/crypto_auth.py:257`
- Called by: `session.py`'s `arif_init` for mode="init"/"full" (line ~1414)
- Key resolution: `resolve_actor_public_key(actor_id)` — searches PEM files, AAA keys, agent registry, DID registry
- Payload formats tried (first match wins):
  1. `{actor_id}:{nonce}` — crypto_auth canonical
  2. `{actor_id}:{constitution_hash}:{nonce}` — kernel compat
  3. Normalized actor variants + sovereign aliases
- Nonce management: `_consume_actor_challenge` (stored in `_ACTIVE_CHALLENGES` with TTL)
- Actor gate: Only runs for `actor_id in ("arif","888","ariffazil") or is_registered_actor(actor_id)`

### Path B: `governance_identity._verify_ed25519_proof` (governance layer)
- Location: `arifosmcp/runtime/governance_identity.py:113`
- Calls: `sovereign_verify.verify_sovereign_signature`
- Key resolution: `_load_public_key()` — searches `_PUBKEY_CANDIDATES` (cached via `@lru_cache`)
- Payload: `{actor_id}:{constitution_hash}:{nonce}` (single format)
- Nonce freshness: `is_challenge_fresh(nonce, window_sec=60)` — requires `timestamp:random` format
- No actor gate — verifies any actor_id against the sovereign public key

### Key Differences

| Aspect | crypto_auth (Path A) | governance_identity (Path B) |
|--------|---------------------|------------------------------|
| Called by | session.py delegate | tools.py bridge (added 2026-07-11) |
| Payload formats | 2+ (tries multiple) | 1 (constitution_hash required) |
| Nonce format | Challenge store (TTL-based) | `timestamp:random` (60s window) |
| Actor gate | Sovereign aliases + registered | None (any actor_id) |
| Key cache | None (loads each call) | `@lru_cache` |

## Proof Dict Construction

When wiring MCP parameters to `_verify_ed25519_proof`:

```python
proof = {"nonce": nonce, "signature": actor_signature}
_verify_ed25519_proof(actor_id, proof)
```

**Do NOT use `validate_sovereign_proof`** — it requires `["signature", "nonce", "timestamp"]` (3 fields), but `_verify_ed25519_proof` only reads `nonce` and `signature` from the dict.

## Nonce Format

`is_challenge_fresh` parses nonce as `int(challenge.split(":")[0])` — expects Unix timestamp prefix.

Valid: `1783775005:abcdef1234567890`
Invalid: `random-uuid-no-timestamp` → returns False → verification rejected

Generate with: `f"{int(time.time())}:{secrets.token_hex(16)}"`

## Session Update Pattern

After successful verification in the delegation path:

```python
# Update _SESSIONS store
_sess = _SESSIONS[sid]
_sess["actor_verified"] = True
_sess["signature_verified"] = True
_sess["identity_verified"] = True
_sess["authority_level"] = "SOVEREIGN"
_sess["authority"] = "FULL"
_sess["ed25519_governance_verified"] = True  # new flag

# Update result dict for caller
result_dict["session"]["actor_verified"] = True
result_dict["actor"]["identity_verified"] = True
result_dict["actor"]["authority_level"] = "SOVEREIGN"
result_dict["actor_verified"] = True
```

## Verification Test Commands

```bash
cd /root/arifOS && python -c "
import sys, time, base64, secrets
sys.path.insert(0, '.')
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from arifosmcp.runtime.governance_identity import _verify_ed25519_proof
from arifosmcp.runtime.sovereign_signer import get_constitution_hash

with open('/root/.secrets/aaa-identity/keys/arif_private.pem', 'rb') as f:
    priv = serialization.load_pem_private_key(f.read(), password=None)

constitution_hash = get_constitution_hash()
nonce = f'{int(time.time())}:{secrets.token_hex(16)}'
actor_id = 'ariffazil'
payload = f'{actor_id}:{constitution_hash}:{nonce}'.encode()
sig_b64 = base64.b64encode(priv.sign(payload)).decode()

# Valid
assert _verify_ed25519_proof(actor_id, {'nonce': nonce, 'signature': sig_b64}) == True
# Invalid
assert _verify_ed25519_proof(actor_id, {'nonce': nonce, 'signature': base64.b64encode(b'bad'*16).decode()}) == False
# Stale
assert _verify_ed25519_proof(actor_id, {'nonce': '1000000000:abc', 'signature': sig_b64}) == False
print('ALL PASS')
"
```

## Key File Locations

| File | Purpose |
|------|---------|
| `arifosmcp/runtime/tools.py` | `_arif_session_init` — MCP tool handler, delegation at line ~7313 |
| `arifosmcp/tools/session.py` | `arif_init` — session creation, uses crypto_auth |
| `arifosmcp/runtime/governance_identity.py` | `_verify_ed25519_proof`, `validate_sovereign_proof` |
| `arifosmcp/runtime/sovereign_verify.py` | `verify_sovereign_signature`, `is_challenge_fresh` |
| `arifosmcp/runtime/crypto_auth.py` | `verify_init_identity`, `resolve_actor_public_key`, `classify_actor_band` |
| `/root/.secrets/aaa-identity/keys/arif_private.pem` | Ed25519 private key |
| `/root/AAA/IDENTITY/keys/arif_public.pem` | Ed25519 public key (canonical) |
| `/root/compose/sekrits/arifos_sovereign.pub` | Ed25519 public key (alt) |
