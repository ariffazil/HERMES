# Session Isolation Fix — P0-A (2026-07-17)

## Symptom
`arif_think` (and other tools) inherited a stale session bound to `c3-live-valid-probe` instead of the calling actor's identity. Every new invocation should create a fresh session or use an explicitly provided one — never silently inherit another actor's session.

## Root cause chain
1. `_resolve_session_id(None)` in `runtime/session.py` returned `_ACTIVE_SESSION_ID` unconditionally
2. `_ACTIVE_SESSION_ID` is a global singleton — last actor to call any tool sets it
3. Auto-injection in `runtime/tools.py` wrappers called `_resolve_session_id(None)` without passing the calling actor's identity
4. No ownership check existed anywhere in the resolution chain

## Files changed

| File | Change |
|------|--------|
| `arifosmcp/runtime/session.py` | Added `_canonical_actor_key()`, rewrote `_resolve_session_id()` with actor-aware fallback, updated `_resolve_lookup_session_id()` |
| `arifosmcp/runtime/tools.py` | Both sync (~22725) and async (~22957) wrappers now pass `caller_actor_id=kwargs.get("actor_id")` |
| `arifosmcp/runtime/session_enforcer.py` | Added `ACTOR_MISMATCH` verdict + actor ownership check in `enforce_session()` |

## Canonical actor key map
```python
_SOVEREIGN_MAP = {
    "arif": "arif", "ariffazil": "arif", "arif_fazil": "arif",
    "arif-fazil": "arif", "arif fazil": "arif",
    "muhammad arif": "arif", "muhammad_arif": "arif",
    "888": "arif", "f13": "arif", "sovereign": "arif",
}
```

## Verification
```bash
# Unit check
python -c "from arifosmcp.runtime.session import _canonical_actor_key; assert _canonical_actor_key('ARIF') == 'arif'"

# Run non-broken tests
python -m pytest tests/test_session_preflight.py tests/test_floors_ci.py tests/test_registry.py tests/adversarial/ -q --tb=short

# Reproduce the original bug (should now log ACTOR MISMATCH and return None):
# 1. Call arif_init(actor_id="c3-live-valid-probe") → creates session
# 2. Call arif_think(actor_id="arif", session_id=None) → should NOT inherit c3's session
```
