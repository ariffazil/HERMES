# APEX Four-Dial Integration Map (2026-07-11)

## Architecture

AKAL is one of four constitutional dials. All four exist in the kernel. The wiring connects them through AKAL's five hooks.

```
PRESENT ──────→ akal_pre_think()     (reality classification boosts friction)
ENERGY-ENTROPY → akal_pre_seal()     (Landauer cost blocks seals)
AMANAH ────────→ akal_pre_forge()    (reversibility upgrades actions)
AKAL ──────────→ all 5 hooks         (friction, shadow, novelty, values, latency)
```

## PRESENT Dial — Reality Attestation

**Wired into:** `akal_pre_think()` in `arifosmcp/core/akal_wiring.py`

**Functions called:**
- `sensing_protocol.classify_truth_class(SenseInput)` — classifies query into 7 truth lanes
- `attestation_verifier.AttestationVerifier().honesty_ratio()` — organ liveness

**Effect on friction:**
- `truth_class in ("unknown", "ambiguous_query")` → friction +0.15
- `honesty_ratio < 0.5` → friction +0.10
- `present_state.search_required` flagged for time-sensitive queries

**Known issue (2026-07-11):** `sensing_protocol.py` has broken import (`philosophy_registry.select_philosophy_state` doesn't exist). The try/except catches it — PRESENT is advisory. Fix: 1-line change in sensing_protocol.py.

## ENERGY-ENTROPY Dial — Thermodynamic Cost

**Wired into:** `akal_pre_seal()` in `arifosmcp/core/akal_wiring.py`

**Functions called:**
- `thermodynamics_hardened.check_landauer_bound(compute_ms, tokens_generated, entropy_reduction)` — Landauer bound check
- `entropy_governor.get_entropy_governor().compute_score()` — 10-dimension entropy scoring

**Effect on seal:**
- Landauer bound violated → `proceed = False`, reason includes ENERGY tag
- Entropy ratio > 0.70 → `proceed = False`, too much chaos for SEAL
- `energy_state.cost_checked = True` when thermodynamics evaluated

## EXPLORATION-AMANAH Dial — Custody & Reversibility

**Wired into:** `akal_pre_forge()` in `arifosmcp/core/akal_wiring.py`

**Functions called:**
- `reversibility_engine.classify_action(tool_id, params)` — classifies reversibility (TRIVIAL→CRITICAL)
- `amanah_gate.AmanahGate().check(text)` — HARAM pattern detection

**Effect on forge:**
- `reversibility in ("irreversible", "critical")` → action upgraded from PROCEED to HOLD
- HARAM pattern detected → `custody_ok = False`, action forced to HOLD
- `amanah_state.requires_888` flagged for irreversible actions

## Middleware Pattern (server.py)

For tools that don't use the embodied pipeline (critique, judge, seal), AKAL is wired via middleware wrappers in `server.py`:

```python
def _akal_wrap_critique(handler):
    @functools.wraps(handler)
    async def wrapped(*args, **kwargs):
        result = await handler(*args, **kwargs)
        # I2: Validate shadow trace from result
        if isinstance(result, dict) and "result" in result:
            inner = result["result"]
            if isinstance(inner, dict):
                trace = akal_post_critique(...)
                result.setdefault("akal", {})
                result["akal"]["shadow_valid"] = trace["valid"]
        return result
    return wrapped

_CANONICAL_HANDLERS["arif_critique"] = _akal_wrap_critique(_CANONICAL_HANDLERS["arif_critique"])
```

**Key design decisions:**
- Advisory, not blocking — try/except around all AKAL calls
- Middleware wraps, doesn't modify — original handler untouched
- Internal only — zero references in public_surface.py
- `result["akal"]` dict added to response — agents see it but it's not a tool parameter

## Pitfall: Don't Build Before Auditing

The kernel has 735+ modules across 327KB. Before building any new "dial" or "physics layer", search for existing implementations:

```bash
# Check if the physics already exists
find arifosmcp -name "*.py" | xargs grep -l "thermodynamic|reversib|attestation|entropy"
```

We almost built three new modules before discovering PRESENT (168KB), ENERGY-ENTROPY (61KB), and AMANAH (47KB) already existed. The fix was wiring, not building.

*DITEMPA BUKAN DIBERI*
