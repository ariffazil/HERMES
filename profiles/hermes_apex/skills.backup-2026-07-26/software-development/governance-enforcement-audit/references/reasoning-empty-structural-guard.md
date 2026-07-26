# REASONING_EMPTY Structural Guard Pattern

> Forged 2026-07-19 during Fable5 audit of arifOS kernel reasoning integrity

## What It Is

A **hard gate** that makes hollow reasoning structurally impossible — not discouraged, *impossible*. When a reasoning organ (arif_think, LLM synthesis, plan generator) produces output with empty evidence lists and inflated confidence, this pattern catches it at the structural level before any downstream agent can consume it.

## Why It Matters

Agentic intelligence optimizes for loop closure. A reasoning organ asked to produce output will produce *something* — and if the LLM is unavailable or the template fallback fires, the output will have:

- Empty `facts` / `supported` / `unsupported` lists
- Medium confidence (0.65) — because the template was authored with a "degraded but usable" posture
- A status of "OK" — because the wrapper treats template output as valid

The result: downstream agents receive hollow reasoning wearing confident clothes. They cannot distinguish real reasoning from an empty template.

## The Pattern (Three Components)

### 1. Structural Guard (Runtime)

```python
_supported = result.get("what_is_supported", [])
_unsupported = result.get("what_is_not_supported", [])
_reasoning_empty = (not _supported) and (not _unsupported)

if _reasoning_empty and confidence > 0.20:
    confidence = 0.20
    provenance = "REASONING_EMPTY_FORCED_CAP"
    # Add degradation signal to unknowns list
```

**Key invariant:** Empty evidence lists + confidence > 0.20 must NEVER co-occur.

### 2. Degradation Surface (Verdict Pipeline)

The degradation signal must propagate from the reasoning step to the canonical verdict:

```python
def _find_degradation_in_payload(result_payload):
    # Detect provenance flags
    if provenance in ("COMPUTED_NOT_OBSERVED", "REASONING_EMPTY_FORCED_CAP"):
        found.append(f"degraded provenance={provenance}")
    
    # Detect REASONING_EMPTY in unknowns
    if "reasoning_empty" in str(unknowns).lower():
        found.append("REASONING_EMPTY detected in unknowns")
    
    # Structural check: empty evidence + non-trivial confidence
    if not supported and not unsupported and confidence and confidence > 0.20:
        found.append("REASONING_EMPTY: no evidence but confidence > 0.20")
```

**Key invariant:** P1_TEMPLATE_DEGRADED → effective_verdict MUST contain DEGRADED.

### 3. Confidence Cap at Source

Template fallback paths must not award medium confidence:

```python
# BEFORE (broken): template fallback with 0.65 confidence
synthesis_dict = {
    "confidence_reasoning": 0.5,
    "confidence_evidence": 0.3,
    "overall_confidence": 0.65,  # ← hollow reasoning, medium confidence
}

# AFTER (fixed): template fallback with 0.15 confidence
synthesis_dict = {
    "confidence_reasoning": 0.10,
    "confidence_evidence": 0.05,
    "overall_confidence": 0.15,  # ← honest: no reasoning occurred
    "what_remains_unknown": [
        "P1 degraded mode — LLM synthesis bypassed",
        "REASONING_EMPTY — no LLM reasoning occurred; template output only",
    ],
}
```

## Test Invariants

```python
# Test 1: Hollow reasoning MUST trigger degradation
def test_reasoning_empty_facts_inferences_confidence_capped():
    hollow_payload = {
        "what_is_supported": [],
        "what_is_not_supported": [],
        "confidence": 0.65,
        "confidence_provenance": "COMPUTED_NOT_OBSERVED",
    }
    degradation = _find_degradation_in_payload(hollow_payload)
    assert len(degradation) > 0

# Test 2: Honest low-confidence empty reasoning is NOT penalized
def test_reasoning_empty_confidence_at_or_below_020_is_not_flagged():
    honest_payload = {
        "what_is_supported": [],
        "what_is_not_supported": [],
        "confidence": 0.15,
        "confidence_provenance": "REASONING_EMPTY_FORCED_CAP",
    }
    degradation = _find_degradation_in_payload(honest_payload)
    structural_guard_hits = [d for d in degradation if "no supported/unsupported" in d]
    assert not structural_guard_hits

# Test 3: Template-degraded output → degradation signals in verdict
def test_degraded_template_forces_degraded_verdict():
    degraded_payload = { ... }  # exact arif_think fallback shape
    degradation = _find_degradation_in_payload(degraded_payload)
    assert "degraded provenance" in str(degradation).lower()
```

## Where It Applies

Any system where:
- An LLM or reasoning component can fall back to template synthesis
- Downstream agents consume the reasoning output as structured evidence
- Confidence values influence gating decisions

Not just arifOS — any governed agent system with a reasoning → verdict pipeline.

## Related: Plan Reversibility Separation

In the same audit (Fable5, 2026-07-19), a separate but related pattern emerged: separating plan execution state from proposed action state.

```python
# BEFORE (collapsed):
plan_receipt = {
    "status": "pending_approval",  # ← even for advisory plans
    "all_reversible": ...,
}

# AFTER (separated):
plan_receipt = {
    "plan_execution": {
        "mutation": False,           # the PLAN doesn't mutate
        "approval_required": False,  # the plan itself needs no approval
    },
    "proposed_actions": {
        "contains_irreversible": True,
        "approval_required_before_execution": True,  # actions WITHIN the plan do
    },
    "status": "ready_for_review",   # not pending_approval for non-mutation plans
}
```

**Key invariant:** A read-only advisory plan must never become `pending_approval` merely because it describes later irreversible work. The plan and its proposed actions need separate states.

## Live Test File

Regression tests shipping these invariants live at:
`arifOS/tests/test_p0_reasoning_invariants.py`

Five assertions:
1. `test_empty_supported_unsupported_forces_low_confidence`
2. `test_empty_facts_inferences_confidence_never_exceeds_point_two_zero`
3. `test_degraded_template_forces_degraded_verdict`
4. `test_degraded_template_implies_degraded_verdict`
5. `test_advisory_no_mutation_plan_is_reversible`

Run with: `ARIFOS_SKIP_PROTOCOL_SENTINEL=1 PYTHONPATH=src pytest tests/test_p0_reasoning_invariants.py -v`
