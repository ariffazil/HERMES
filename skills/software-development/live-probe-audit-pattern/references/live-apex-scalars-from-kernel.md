# Live Apex Scalars from Kernel Health Endpoint

## The Pattern

When an organ's `/health` endpoint returns apex scalars (G-fold: `G`, `C_dark`, `W3`, `h`, `QDF`), these **must be live-fetched from the upstream arifOS kernel**, not hardcoded. Hardcoded NOMINAL values violate F2 TRUTH.

## The Fix (applied to GEOX `health_handler` 2026-07-26)

### Before (violation)

```python
"apex_scalars": {
    "G": {"value": 0.5, "status": "NOMINAL"},
    "C_dark": {"value": 0.02, "status": "NOMINAL"},
    "W3": {"value": 0.8, "status": "NOMINAL"},
    "h": {"value": 0.04, "status": "NOMINAL"},
    "QDF": {"value": 0.0, "status": "NOMINAL"},
},
```

These were **fabricated** — always "NOMINAL" regardless of real kernel state. F2 TRUTH breach.

### After (live)

The kernel `/health` endpoint (`http://127.0.0.1:8088/health`) was **already being called** earlier in the handler for `thermodynamic` + `status`. The fix:

1. **Reuse the existing `_kh_data` response** — no additional HTTP round trip
2. **Extract `apex_scalars`** from the already-fetched dict
3. **On failure → UNMEASURED** (honest unknown, WELL pattern)

```python
_UNMEASURED_APEX: dict[str, dict[str, object]] = {
    "G": {"value": None, "status": "UNMEASURED"},
    "C_dark": {"value": None, "status": "UNMEASURED"},
    "W3": {"value": None, "status": "UNMEASURED"},
    "h": {"value": None, "status": "UNMEASURED"},
    "QDF": {"value": None, "status": "UNMEASURED"},
}
_apex_scalars: dict[str, dict[str, object]] = dict(_UNMEASURED_APEX)
try:
    _kh_apex = _kh_data.get("apex_scalars")  # type: ignore[union-attr]
    if isinstance(_kh_apex, dict):
        for _k in _UNMEASURED_APEX:
            _v = _kh_apex.get(_k)
            if isinstance(_v, dict) and "value" in _v:
                _apex_scalars[_k] = _v
except Exception:
    pass
```

Then in the response body:
```python
"apex_scalars": _apex_scalars,
```

## Design Rules

1. **Reuse, don't re-fetch.** If the kernel health endpoint was already called for `thermodynamic`/`status`, read `apex_scalars` from the same response. Adding a second HTTP call wastes resources and adds latency.

2. **UNMEASURED, not fabricated NOMINAL.** An honest "I don't know" (UNMEASURED) is better than a lie ("NOMINAL" when the kernel is unreachable). This is the WELL organ pattern.

3. **Scalar-by-scalar overlay.** If the kernel returns partial data (e.g., only `G` and `C_dark`), missing keys stay UNMEASURED while available ones pass through. Don't fail the whole block on a partial response.

4. **No additional imports needed.** The handler already imports `httpx` inline. Use the already-established pattern (`async with httpx.AsyncClient(timeout=2.0)`).

5. **No new network path.** The kernel health check at `127.0.0.1:8088/health` is the canonical source. Don't add alternative sources or fallback URLs.

## Verification

After applying the fix, verify with:

```bash
# When kernel is reachable — should show live values
curl -sf http://localhost:8081/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
apex = d.get('apex_scalars', {})
for k, v in apex.items():
    print(f'{k}: value={v.get(\"value\")} status={v.get(\"status\")}')
"

# When kernel is unreachable — should show UNMEASURED
# (stop the kernel or firewall the port)
curl -sf http://localhost:8081/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
apex = d.get('apex_scalars', {})
for k, v in apex.items():
    assert v.get('status') == 'UNMEASURED', f'{k} should be UNMEASURED'
print('All UNMEASURED on kernel failure ✅')
"
```

## Why Not a Separate Fetch

The kernel health check already runs at the top of `health_handler` to determine `_kernel_ok` and `_kernel_verdict`. Reading `apex_scalars` from `_kh_data` is zero-cost — no extra latency, no extra connection pool churn, no extra failure mode. A separate fetch would double the timeout risk and create a second async client context that needs managing.
