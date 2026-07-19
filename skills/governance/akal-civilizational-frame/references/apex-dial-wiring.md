# APEX Dial Integration — Wiring Pitfalls & Actual Code

## Critical Pitfalls (discovered 2026-07-11 during live integration)

### Pitfall 1: `sensing_protocol.py` broken import
`sensing_protocol.py` imports `select_philosophy_state` from `philosophy_registry.py`, but that function didn't exist. **Fix:** added `select_philosophy_state()` to `arifosmcp/runtime/philosophy_registry.py` — returns dict with `confidence_cap`, `locks_active`, `entropy_dS`, etc.

### Pitfall 2: Wrong function name for truth classification
The correct function is `classify_truth_class(SenseInput)` — NOT `classify_evidence_class(str)`. Takes a `SenseInput` object, not a plain string.

### Pitfall 3: `SenseInput` constructor
```python
# WRONG — SenseInput has no 'query' parameter
si = SenseInput(query="What is X?")

# CORRECT
from arifosmcp.runtime.sensing_protocol import InputSpec, InputType, SenseInput, SensingMode
si = SenseInput(input=InputSpec(type=InputType.QUERY, value="What is X?", mode=SensingMode.GOVERNED))
```

### Pitfall 4: `reversibility_engine.classify_action` return keys
```python
rev = classify_action("arif_forge", {"mode": "generate", "query": "rm -rf /"})
# Returns:
# {
#   "reversibility": "irreversible",    # NOT "reversibility_class"
#   "requires_arif_approval": True,     # NOT "requires_888_hold"
#   "may_proceed": False,
#   "verdict": "HOLD",
#   "reason": "IRREVERSIBLE pattern matched: \\brm\\s",
# }
```

### Pitfall 5: `thermodynamics_hardened.check_landauer_bound` signature
```python
check_landauer_bound(
    compute_ms: float,           # estimated compute time
    tokens_generated: int,       # estimated tokens
    entropy_reduction: float,    # assumed positive
    bits_per_token: int = 16,
    actual_joules: float | None = None,
    verified_compute_ms: float | None = None,
) -> dict  # {"pass": bool, "reason": str, ...}
```

### Pitfall 6: Middleware pattern in server.py
AKAL hooks are applied as `functools.wraps` wrappers around `_CANONICAL_HANDLERS` entries. The wrappers add an `akal` dict to the tool response — they never block execution. Pattern:
```python
def _akal_wrap_critique(handler):
    @functools.wraps(handler)
    async def wrapped(*args, **kwargs):
        result = await handler(*args, **kwargs)
        # Add AKAL metadata to result
        result.setdefault("akal", {})
        result["akal"]["shadow_valid"] = trace["valid"]
        return result
    return wrapped
```

## Actual Integration Code (akal_wiring.py additions)

### PRESENT → akal_pre_think()
```python
present_state = {"evidence_class": "unknown", "honesty_ratio": None, "grounded": False}
try:
    from arifosmcp.runtime.sensing_protocol import InputSpec, InputType, SenseInput, SensingMode, classify_truth_class
    if query:
        si = SenseInput(input=InputSpec(type=InputType.QUERY, value=query, mode=SensingMode.GOVERNED))
        tc = classify_truth_class(si)
        present_state["evidence_class"] = tc.truth_class.value
        if tc.truth_class.value in ("unknown", "ambiguous_query"):
            result.score = min(result.score + 0.15, 1.0)
        if tc.search_required:
            present_state["search_required"] = True
except Exception:
    pass  # PRESENT is advisory
```

### AMANAH → akal_pre_forge()
```python
amanah_state = {"reversibility_class": "unknown", "requires_888": False, "custody_ok": True}
try:
    from arifosmcp.core.reversibility_engine import classify_action
    rev = classify_action("arif_forge", {"mode": "generate", "query": output_text[:200]})
    amanah_state["reversibility_class"] = rev.get("reversibility", "unknown")
    amanah_state["requires_888"] = rev.get("requires_arif_approval", False)
    if amanah_state["reversibility_class"] in ("irreversible", "critical"):
        if action == "PROCEED":
            action = "HOLD"
except Exception:
    pass  # AMANAH is advisory
```

### ENERGY → akal_pre_seal()
```python
energy_state = {"landauer_ok": True, "entropy_delta": 0.0, "cost_checked": False}
try:
    from arifosmcp.core.physics.thermodynamics_hardened import check_landauer_bound
    est_tokens = passes_completed * 2000
    est_compute_ms = passes_completed * 100.0
    landauer = check_landauer_bound(compute_ms=est_compute_ms, tokens_generated=est_tokens, entropy_reduction=1.0)
    energy_state["landauer_ok"] = landauer.get("pass", True)
    energy_state["cost_checked"] = True
except Exception:
    pass  # ENERGY is advisory
```

## Verified Test Results (2026-07-11)

```
PRESENT: class=time_sensitive_fact  grounded=True   search=True   (Brent crude query)
AMANAH:  action=HOLD                reversibility=irreversible     (rm -rf query)
ENERGY:  proceed=True               cost_checked=True              (irreversible seal)
```

All four dials: AKAL ✅ PRESENT ✅ ENERGY ✅ AMANAH ✅
