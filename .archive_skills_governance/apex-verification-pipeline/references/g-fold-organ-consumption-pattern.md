# G-Fold Organ Consumption Pattern

**Date:** 2026-07-26  
**Author:** Hermes  
**Status:** SEALED — deployed in WELL (sleep+fatigue), GEOX (/health proxy), and A-FORGE (4-layer forge gate Layer 2). Live pattern, reusable.  

---

## What This Is

The canonical pattern for any arifOS federation organ to consume live G from the arifOS kernel and use it to gate high-criticality decisions. Implemented first in WELL (`well_assess_homeostasis`) — reusable across GEOX, WEALTH, A-FORGE, and Hermes itself.

Closes the gap identified in `g-fold-flow-doctrine.md` §5: **"No organ currently queries the kernel's live G before acting."**

---

## Architecture

```
Organ action
  ↓
_get_live_G()
  → GET http://localhost:8088/health
  → extract apex_scalars.G.value
  → returns (float|"UNMEASURED", note_or_None)
  ↓
G over threshold? (default 0.50)
  ↓                   ↓
YES                  NO
  ↓                  if C4/C5 + PROCEED → downgrade to DEFER
PROCEED              with routing_note explaining G insufficiency
```

## Implementation Template

### 1. Helper Function

```python
# Module-level constant — SABAR threshold from apex-verification-pipeline
_G_FOLD_SABAR_THRESHOLD = 0.50

def _get_live_G() -> tuple[float | str | None, str | None]:
    """Fetch G from arifOS kernel health endpoint.

    Returns:
        (G_value_or_UNMEASURED, note_or_None)
    """
    try:
        import httpx as _httpx

        resp = _httpx.get("http://localhost:8088/health", timeout=5.0)
        resp.raise_for_status()
        body = resp.json()
        apex_g = body.get("apex_scalars", {}).get("G", {})
        g_val = apex_g.get("value")
        if g_val is not None:
            return float(g_val), None
        # G present but value is None → UNMEASURED
        return "UNMEASURED", "G exists in apex_scalars but value is None."
    except Exception as exc:
        return "UNMEASURED", f"arifOS kernel unreachable: {exc}"
```

### 2. Fetch Once at Function Entry

```python
_live_g_value, _live_g_note = _get_live_G()
```

Fetch once per call. Do NOT re-fetch per mode or per code path.

### 3. G-Fold Override — C4/C5 Downgrade

Place after existing routing/threshold logic, before statistical/meta analysis:

```python
if (
    isinstance(_live_g_value, (int, float))
    and float(_live_g_value) < _G_FOLD_SABAR_THRESHOLD
    and route_signal == "PROCEED"
    and decision_class_upper in ("C4", "C5")
):
    route_signal = "DEFER"
    g_float = float(_live_g_value)
    routing_note = (
        f"PROCEED downgraded to DEFER: live G={g_float:.3f} < "
        f"SABAR threshold ({_G_FOLD_SABAR_THRESHOLD}). "
        f"Insufficient governance capacity for {decision_class_upper} <task-context>."
    )
```

**isinstance guard rationale:** When kernel is unreachable, `_live_g_value` = string `"UNMEASURED"`. The guard prevents `TypeError: '<' not supported between instances of 'str' and 'float'`. Never coerce UNMEASURED to 0.0 — that would silently treat a failed fetch as G=0.0, which is wrong.

### 4. Expose G in Output

```python
_data_payload = {
    # ... existing fields ...
    "live_G": _live_g_value,
}
if _live_g_note is not None:
    _data_payload["live_G_note"] = _live_g_note
```

Conditional note: only add `live_G_note` when non-None (successful fetch returns None note).

---

## C-Class Threshold Matrix Reference

| Class | Description | G-fold behavior |
|-------|-------------|-----------------|
| C1 | Trivial | Unaffected |
| C2 | Routine | Unaffected |
| C3 | Standard | Unaffected |
| C4 | Critical | **G < 0.50 → PROCEED downgraded to DEFER** |
| C5 | Sovereign | **G < 0.50 → PROCEED downgraded to DEFER** |

Only C4/C5 warrant governance scalar gating. C1-C3 are never blocked by G.

---

## Placement Priority

1. **Data provenance cap** (telemetry honesty) — if already CAUTION, G-fold has nothing to downgrade
2. **G-fold override** — if G < 0.50 and C4/C5, PROCEED → DEFER
3. **Statistical/SAF analysis** — secondary checks

Ordering: "Is data real?" → "Is governance healthy?" → "Is data statistically sound?"

---

## Graceful Degradation

| Kernel state | G value | Behavior |
|-------------|---------|----------|
| Responds with value | float | Normal logic |
| G=None in response | "UNMEASURED" | Informational — no downgrade |
| Connection timeout | "UNMEASURED" | Informational — no downgrade |
| Connection refused | "UNMEASURED" | Informational — no downgrade |
| Non-JSON response | "UNMEASURED" | Informational — no downgrade |

**Rule:** UNMEASURED is informational only. Never block/downgrade because kernel is unreachable — governance being offline means the organ proceeds with best available evidence.

---

## Verification Checklist

- [ ] `_get_live_G()` returns `(float, None)` on healthy kernel with G value
- [ ] `_get_live_G()` returns `("UNMEASURED", note)` on unreachable kernel — never raises
- [ ] G < 0.50 + C4/C5 + PROCEED → DEFER downgrade
- [ ] G ≥ 0.50 + C4/C5 + PROCEED → unchanged
- [ ] C1-C3 + any G → unchanged
- [ ] G = "UNMEASURED" + C4/C5 → no crash, no downgrade
- [ ] `live_G` present in all data payload paths
- [ ] `live_G_note` present only when note is non-None
- [ ] isinstance guard protects the float comparison

---

## Deployment Record

| Date | Organ | File | Scope |
|------|-------|------|-------|
| 2026-07-26 | WELL | `server.py` | `well_assess_homeostasis` — sleep + fatigue modes |
| 2026-07-26 | GEOX | `src/geox_mcp/server.py` | `/health` endpoint — kernel proxy replaces hardcoded stub |
| 2026-07-26 | A-FORGE | `GovernanceBridge.ts` + `evaluate.ts` | `fetchCanonicalG()` + `computeGateWithKernelG()` — 4-layer forge gate Layer 2 |
| (next) | WEALTH | — | Before wisdom synthesis |
| (next) | AAA | — | Before agent card validation |
