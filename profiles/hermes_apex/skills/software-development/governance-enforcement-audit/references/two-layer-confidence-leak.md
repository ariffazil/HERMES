# Two-Layer Confidence Leak — Engine Fix, Wrapper Miss

> Forged 2026-07-19 during Fable5 v2 live kernel probe

## The Defect

When a governed system has **two layers** that independently compute confidence — an engine layer (the tool implementation) and a wrapper layer (the MCP envelope constructor) — fixing the engine alone does NOT fix the public surface. The wrapper has its own default that never consults the inner state.

## Symptoms

- Engine-layer tests pass: confidence is correctly capped at 0.20 when reasoning is empty
- Live public-surface probe still shows `confidence: 0.65, evidence_strength: "medium"` over empty facts/inferences
- The wrapper code has a hardcoded fallback default (e.g., `confidence or 0.65`) that fires when the payload traverses a different code path

## The Fix

Three components, one invariant:

### 1. Engine-layer cap (source)
```python
# Template fallback must return honest confidence
synthesis_dict = {
    "overall_confidence": 0.15,  # not 0.65
    "confidence_provenance": "COMPUTED_NOT_OBSERVED",
}
```

### 2. Structural guard (impossible, not discouraged)
```python
if not facts and not inferences and confidence > 0.20:
    confidence = 0.20
    provenance = "REASONING_EMPTY_FORCED_CAP"
```

### 3. Wrapper derivation (never default)
```python
# The wrapper must READ the inner state, not assume it
_inner_result = payload.get("result", {})
_inner_provenance = _inner_result.get("confidence_provenance", "")
_inner_state = _inner_result.get("reasoning_state", "")
_evidence_empty = (not facts) and (not inferences)

if _evidence_empty and _inner_provenance in DEGRADED_PROVENANCES and conf > 0.20:
    conf = 0.20
```

## The Test That Catches It

Engine-layer tests are insufficient. You need a **public MCP surface test** — feed the wrapper the same hollow payload the engine produces, and assert the envelope's metacognition reflects the inner state:

```python
def test_wrapper_confidence_capped_when_inner_reasoning_empty():
    hollow_payload = {
        "confidence": 0.15,
        "confidence_provenance": "COMPUTED_NOT_OBSERVED",
        "reasoning_state": "REASONING_EMPTY",
        "facts": [],
        "inferences": [],
        "result": {
            "confidence": 0.15,
            "reasoning_state": "REASONING_EMPTY",
        },
    }
    envelope = ensure_standard_mcp_output("arif_think", hollow_payload)
    assert envelope["metacognition"]["confidence"] <= 0.20
    assert envelope["metacognition"]["evidence_strength"] == "low"
```

## The Pattern (reusable)

When auditing any governed system with layered confidence computation:

1. Fix the inner layer first (engine/tool implementation)
2. Add engine-layer tests — they WILL pass
3. **Probe the public surface** — curl the live endpoint or call the public wrapper function
4. If the public surface shows different confidence than the engine, the wrapper has an independent default
5. Trace the wrapper's confidence derivation chain — every `or DEFAULT` is a candidate leak
6. Add a regression test at the wrapper layer, not just the engine

## Precedent

This exact defect survived two arifOS kernel fixes (commits `2fb517ef5` and `6193c4732`) before being caught by a live MCP surface probe. The engine and the test suite both reported correct behavior. The wrapper silently defaulted to its own confidence value.
