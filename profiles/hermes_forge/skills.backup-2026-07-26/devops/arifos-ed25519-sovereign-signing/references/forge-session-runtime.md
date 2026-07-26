# forge_session_runtime — Sovereign Chain Runtime (2026-07-13)

> **Module:** `/root/arifOS/arifosmcp/runtime/forge_session_runtime.py`
> **Wired into:** `authority.py` (both envelope paths), `governance_identity.py` (imports)
> **Status:** Live in production (commit `ec3d313`)
> **Architecture:** EUREKA P1 G4 — Ed25519 chain end-to-end

## What It Does

`forge_session_runtime.py` implements the F13 sovereign verification chain.
Every `arif_init` call now stamps the session with its sovereignty level,
enabling downstream verification that a session was initiated by the sovereign.

This module is **fail-closed by default** — every function returns `False`,
`None`, or an error verdict on any missing parameter, import failure, or
lookup miss. It never guesses `True`.

## Module Surface

| Function | Purpose | Returns | Fail-Closed |
|----------|---------|---------|-------------|
| `sovereign_signal()` | 4-gate sovereignty check | `SovereignVerdict` | `sovereignty=False` |
| `register_session_anchor()` | Stamp session with sovereignty level | `bool` (True = registered) | `False` on duplicate |
| `get_session_anchor()` | Read session's sovereign anchor | `dict` or `None` | `None` on miss/expiry |
| `create_forge_session_proof()` | HMAC-signed proof linking action to session | `ForgeSessionProof` or `None` | `None` on missing anchor |
| `verify_forge_session_chain()` | Trace receipt through session proof chain | `ChainVerdict` | `valid=False` + `broken_at` |
| `verify_forge_session_token()` | 13-check HMAC token verification (imported by `governance_identity`) | `TokenVerdict` | `ok=False` + `code` |
| `verify_session_bound_assertion()` | 11-check assertion verification (imported by `governance_identity`) | `TokenVerdict` | `ok=False` + `code` |

## 4-Gate Sovereignty Check (`sovereign_signal`)

The core function verifies a session was initiated by the sovereign:

```
Gate 1: Parameters exist (session_id or actor_id)
  FAIL → sovereignty=False, method="anonymous", reason="no session_id or actor_id"

Gate 2: actor_id in PROTECTED_SOVEREIGN_IDS
  FAIL → sovereignty=False, method="anonymous", reason="non-sovereign actor"

Gate 3: verified_key_id in SOVEREIGN_KEY_IDS
  FAIL → sovereignty=False, method="session_anchor", reason="key not in SOVEREIGN_KEY_IDS"

Gate 4: verification_method in {"f13_sovereign", "session", "ed25519"}
  FAIL → sovereignty=False, verified=True, method="session_anchor",
          reason="not cryptographically verified"

ALL PASS → sovereignty=True, method="f13_sovereign", reason="sovereign identity + key verified"
```

**Key design decision — ceremony rejected:** The 4-gate check is a single
function call, not a multi-step ceremony. The Ed25519 proof was already
validated by the caller (`governance_identity._verify_ed25519_proof`). The
key match alone is sufficient evidence of sovereignty — requiring another
round-trip would violate the classify-first principle.

## Session Anchor Registration

Every `arif_init` call triggers `register_session_anchor()` via both paths
in `authority.py`:

```
arif_init (MCP)
  → authority_envelope_for_session()
    → register_session_anchor(session_id, actor_id, key_id, method)
      → _SESSION_REGISTRY[session_id] stored with TTL (default 3600s)
```

The registry is in-memory (`_SESSION_REGISTRY` dict with `threading.RLock`).
Each entry stores: `actor_id`, `verified_key_id`, `verification_method`,
`created_at`, `expires_at`, `anchor_type`.

**P2 upgrade:** Replace in-memory dict with Postgres/Supabase for
cross-session persistence.

## HMAC Session Proof Chain

`create_forge_session_proof()` binds a forge action to the session that
authorised it:

```
secret = sha256(f"{session_id}:{actor_id}:forge_session:v1")
action_hash = sha256(json.dumps(action_payload))
proof_token = HMAC(secret, action_hash + session_id)
```

The `ForgeSessionProof` carries:
- `session_id`, `actor_id`, `forge_action`
- `action_hash` (sha256 of payload)
- `session_proof_token` (HMAC)
- `timestamp` (ISO8601)
- `receipt_id` (set after VAULT999 append)

`verify_forge_session_chain()` traces the chain:
1. proof → receipt (session_id, actor_id, action_hash)
2. session anchor exists and was sovereign
3. session_id consistent across proof, anchor, and receipt

## Token Verification (All 13 Checks)

`verify_forge_session_token()` performs exactly 13 checks, in order:

| # | Check | Fail code |
|---|-------|-----------|
| 1 | Token is a dict | `INVALID_FORMAT` |
| 2 | session_id present | `MISSING_SESSION` |
| 3 | actor_id present | `MISSING_ACTOR` |
| 4 | nonce present | `MISSING_NONCE` |
| 5 | signature present | `MISSING_SIGNATURE` |
| 6 | token_version == EXPECTED_TOKEN_VERSION | `VERSION_MISMATCH` |
| 7 | audience == AUDIENCE_FORGE_SESSION | `AUDIENCE_MISMATCH` |
| 8 | issued_at ISO8601 parseable | `INVALID_ISSUED_AT` |
| 9 | expires_at ISO8601 parseable | `INVALID_EXPIRES_AT` |
| 10 | Not expired | `TOKEN_EXPIRED` |
| 11 | Session anchor exists | `NO_SESSION_ANCHOR` |
| 12 | Actor matches anchor | `ACTOR_MISMATCH` |
| 13 | HMAC signature valid (timing-safe) | `SIGNATURE_MISMATCH` |

## Integration Points Already Live

- **`governance_identity.py`** was already importing `verify_forge_session_token` and
  `verify_session_bound_assertion` from a non-existent module. Now resolves.
- **`authority.py`** calls `register_session_anchor()` in both fallback and
  canonical paths. Non-blocking — failures caught silently.
- **Every `arif_init` call** now stamps the session anchor.

## Pitfalls

### PITFALL: verify_forge_session_token hardcodes _SESSION_REGISTRY
The token verifier reads the session anchor from the in-memory registry.
In a multi-process deployment (e.g., gunicorn workers), each process has
its own in-memory registry. A token verified by process A may not be
verifiable by process B. **P2 fix:** persistent store.

### PITFALL: SoyereignVerdict returns sovereignty=True but the session may be OBSERVE_ONLY
Sovereignty verification proves identity. It does NOT grant authority.
The session's `runtime_band` is still set by `authority.py` based on
the lease. `sovereign_signal()` is for verifying who the caller IS, not
what they are ALLOWED TO DO.

### PITFALL: Nonce not part of sovereign_signal
Unlike `arif_init` which has a nonce challenge-response flow,
`sovereign_signal()` does NOT use nonces. It trusts that the session
anchor was registered with a verified key. The nonce proof happened
at `arif_init` time.

## File References

- Module: `/root/arifOS/arifosmcp/runtime/forge_session_runtime.py`
- Wire point (fallback): `/root/arifOS/arifosmcp/runtime/authority.py` (line ~328)
- Wire point (canonical): `/root/arifOS/arifosmcp/runtime/authority.py` (line ~362)
- Importer: `/root/arifOS/arifosmcp/runtime/governance_identity.py` (lines 156-184)
- Spec: `/root/AAA/docs/contracts/SIX_PLANE_EXECUTION_LOOP_v1.md` (§8 G4, §3.2)
