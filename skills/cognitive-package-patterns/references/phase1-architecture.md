# Phase 1 Cognitive Intelligence — Architecture Walkthrough

Built 2026-08-04 from the validated research brief at `/root/HERMES/scratch/research_brief_phase1_validation.md`.

## Canonical constants

| Constant | Symbol | Value | Notes |
|---|---|---|---|
| Base decay rate | Ω₀ | 0.03 | F7 HUMILITY floor |
| Ebbinghaus exponent | λ | 0.10 | Starts conservative |
| Inertia coefficient | η | 0.50 | Higher = high-value memories decay slower |
| Confidence cap | — | 0.90 | Enforced once, in `Receipt.__post_init__` |
| STM bit-width | — | 32 | IEEE-754 float |
| MTM bit-width | — | 8 | 255 uniform levels |
| LTM bit-width | — | 4 | 15 levels |
| Archive bit-width | — | 2 | 3 levels |

Value-factor weights (sum = 1.0, enforced at import):

| Factor | Weight |
|---|---|
| `emotional_intensity` | 0.15 |
| `goal_relevance` | 0.20 |
| `value_alignment` | 0.15 |
| `task_utility` | 0.15 |
| `reliability_history` | 0.10 |
| `usage_count` | 0.15 |
| `creation_recency` | 0.10 |

## Decay formula derivation

```
Base (bare Ebbinghaus):
  Ω_eff = Ω · e^(-λ·Δn)

With inertia (Phase 1 canonical):
  μ(Ω) = 1 - η · V(m)
  Ω_eff = Ω · e^(-λ · Δn · μ(Ω))

With recall reinforcement (Alexander 2026):
  S_new = S_old · (1 + ln(1 + recall_count))
```

The inertia multiplies the exponent so high-value memories get a smaller effective λ, preserving the curve shape. Bare `e^(-λ·Δn)` is too aggressive for benchmarks (Alexander 2026 showed 100% vs 0% foundational recall with interaction-count variant vs bare form).

## Receipt schema

```json
{
  "receipt_id": "rcpt-<uuid12>",
  "module": "memory_decay | causal_tagger | drift_monitor",
  "operation": "compute_decay | tag_causal | detect_drift | ...",
  "timestamp": "ISO-8601 UTC",
  "evidence_type": "OBS_CAUSAL | DER_CAUSAL | INT_CAUSAL | SPEC_CAUSAL | UNKNOWN",
  "confidence": 0.0,
  "verdict": "COMPUTED | DETECTED | DRIFT_SIGNAL | UNKNOWN",
  "data": { ... },
  "source": "what triggered this computation",
  "meta": {}
}
```

Confidence is capped to 0.90 inside `Receipt.__post_init__`. Call sites must not double-cap.

## Drift thresholds

| Score | Level | Recommendation |
|---|---|---|
| ≤ 0.30 | STABLE | CONTINUE |
| > 0.30 | DRIFT_WARNING | REVIEW / COOL_AND_REANCHOR if trend worsens |
| > 0.50 | DRIFT_ALERT | HOLD_AND_REVIEW |

Drift scores from the monitor can reduce the F7 confidence cap: `0.90 · (1 - drift_score)`.

## Causal evidence classification rules

| Type | Evidence pattern | Max confidence |
|---|---|---|
| OBS_CAUSAL | trace/log/measurement/sensor reference in context | 0.90 |
| DER_CAUSAL | multi-source/validated/cross-reference markers | 0.85 |
| INT_CAUSAL | single-source inference markers ("I believe", "likely") | 0.70 |
| SPEC_CAUSAL | no evidence markers | 0.40 |
| UNKNOWN | cue detected, no classification possible | 0.30 |

## Dependency map

```
cognitive/__init__.py
  imports: config (constants), receipt (Receipt, emit_receipt)

cognitive/config.py
  pure constants, no imports

cognitive/receipt.py
  imports: config.CONFIDENCE_CAP
  stdlib only

cognitive/memory_decay/engine.py
  imports: config.*, receipt.*

cognitive/causal_tagger/tagger.py
  imports: config.*, receipt.*
  stdlib only

cognitive/drift_monitor/monitor.py
  imports: config.*, receipt.*
  optional: sentence_transformers
  stdlib fallback: TF-IDF
```

## Test counts (110 total)

| File | Count |
|---|---|
| `test_receipt.py` | 5 |
| `test_memory_decay.py` | 50 |
| `test_causal_tagger.py` | 25 |
| `test_drift_monitor.py` | 30 |
