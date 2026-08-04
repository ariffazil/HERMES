# Simulation Test Harness — Session Findings 2026-08-04

Specific lessons from rebuilding three cognitive modules (memory_decay, causal_tagger, drift_monitor) from scratch with sentence-transformers (all-MiniLM-L6-v2) backend and pytest.

## Import Path Discipline

**Symptom**: Pyright/LSP shows `ImportError: cannot import name 'X' from 'cognitive.module.engine'` even though the module exists and exports X.

**Root cause**: An old `__init__.py` at any level (the package's, OR the parent cognitive's) is still importing old names. The new engine.py works in isolation, but `from cognitive.module import X` fails at the `__init__.py` line.

**Workaround**:
1. Always update BOTH `engine.py` AND `<module>/__init__.py` AND any `cognitive/__init__.py` that re-exports.
2. Clear `__pycache__/` after every rewrite: `rm -rf */__pycache__/` (the .pyc shadow can mask __init__.py changes).
3. After writing the new __init__.py, run a smoke test BEFORE pytest:
   ```bash
   PYTHONPATH=/root/HERMES python3 -c "from cognitive.module.engine import NewClass; print('OK')"
   ```
4. Run pytest with `cwd=/root/HERMES` AND `PYTHONPATH=/root/HERMES` set:
   ```bash
   cd /root/HERMES && PYTHONPATH=/root/HERMES python -m pytest cognitive/module/test_*.py -v
   ```

## sentence-transformers Lazy Singleton

**Pattern that works reliably**:

```python
_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def _embed(texts: List[str]):
    model = _get_model()
    return model.encode(texts, normalize_embeddings=True)
```

**Critical detail**: Always pass `normalize_embeddings=True`. This makes cosine_sim equivalent to dot product, so distance is `1 - dot(a, b)` and bounded in [0, 2]. Without normalization, norms differ and the distance becomes meaningless.

**Pre-compute template embeddings at first use, not at module load**:

```python
_template_embeddings = None

def _get_template_embeddings():
    global _template_embeddings
    if _template_embeddings is None:
        _template_embeddings = _embed(_TEMPLATE_TEXTS)
    return _template_embeddings
```

This avoids the ~10s model load being wasted if the templates never get used.

## all-MiniLM-L6-v2 Cosine Distance Calibration

**Empirical findings** (measured on 50+ short conversation turns):

| Pair type | Typical cosine distance |
|---|---|
| Identical sentence | 0.0 |
| Near-paraphrase ("deploy app" vs "deploy app v2") | 0.05–0.15 |
| Related short sentences (same topic, different angle) | 0.30–0.70 |
| Topic shift within same domain (CI test vs deployment) | 0.55–0.80 |
| Hard jump (deployment vs medieval history) | 0.85–1.00 |

**Implication for drift monitors**: Spec thresholds of 0.30 (warning) / 0.50 (alert) cause 100% false-alarm rate on normal short conversations. Recalibrate to **0.55 / 0.75** for short-message drift detection. Document the calibration explicitly in the report — don't pretend the spec numbers worked.

**Implication for causal taggers**: Semantic similarity scores from MiniLM cluster at 0.0–0.3 for most sentences (since the embedding space is dominated by domain signals, not causal structure). The classifier must rely on regex marker bias + semantic top-1 choice, not on raw similarity magnitudes.

## Regex Pattern Gotchas

- `\bcauses?\b` matches "cause" and "causes" but NOT "caused" or "causing". Use `\bcaus(?:e[ds]?|ing)\b`.
- `\blog\s+show` does NOT match "log shows" because `\b` after "log" requires a word boundary, and the space counts as one. Test: `_compile_group([r"\blog\b", r"\bshows?\b"])` (separate patterns) matches "log shows" via either pattern. Combine with `_re_observed.search(s)` returning either match.
- For Malay: `\bmenyebabkan\b`, `\bmengakibatkan\b`, `\bmenunjukkan\b` are the high-yield causal/observational markers. Add `\bpemantauan\b` (monitoring) for OBS_CAUSAL on Malay.
- Always test regex against actual sentences via `python3 -c "..."` before assuming a pattern works.

## Metric Computation Discipline

**Binary metrics helper that's reusable**:

```python
def _binary_metrics(predicted, actual, label):
    tp = sum(1 for p, a in zip(predicted, actual) if p == label and a == label)
    fp = sum(1 for p, a in zip(predicted, actual) if p == label and a != label)
    fn = sum(1 for p, a in zip(predicted, actual) if p != label and a == label)
    tn = sum(1 for p, a in zip(predicted, actual) if p != label and a != label)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr       = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr       = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": precision, "recall": recall, "fpr": fpr, "fnr": fnr, "f1": f1}
```

**Macro-F1 vs Micro-F1**: For imbalanced multi-class sets (e.g., 12 OBS_CAUSAL examples + 5 DER_CAUSAL examples), macro-F1 weights every class equally and exposes minority-class failures. Report both. Don't just print overall accuracy — a 90% accuracy can hide 0% recall on a small class.

## Marker Bias + Semantic Combo (Causal Tagger)

When combining regex markers with semantic similarity:

```python
W_SEM = 0.6   # semantic weight
W_MRK = 0.4   # marker weight
combined[label] = W_SEM * semantic_norm[label] + W_MRK * marker_bias[label]
```

**Critical**: normalize semantic scores from `[-1, 1]` to `[0, 1]` via `(sim + 1.0) / 2.0` BEFORE combining. Otherwise raw cosine similarities are mostly negative and dominate the combined score wrongly.

**Marker bias structure**:
- `causal` marker present + no evidence type markers → small SPEC bias (0.05), let semantic decide
- `causal` + `observed` → strong OBS bias (0.6)
- `causal` + `derived` → strong DER bias (0.5)
- No `causal` marker + `inferred` → small INT bias (0.3)
- No `causal` marker + no evidence → strong UNKNOWN bias (0.5)

## Tests-as-Discovery Pattern

The most valuable pattern: **write tests that ASSERT properties from the spec, then let failures teach you the spec's actual semantics**.

Examples from this session:
- Asserting "high-value memory survives 200 cycles" — caught an inverted `μ(Ω)` formula immediately.
- Asserting "OBS_CAUSAL ground truth misclassified as X" — forced expansion of Malay observation markers.
- Asserting "false alarm rate < 0.50 on normal conversation" — exposed the 0.30/0.50 threshold mismatch with all-MiniLM-L6-v2 and forced honest recalibration.

**Honest reporting pattern**: When tests fail, the report should say:
- WHAT the test expected
- WHAT the actual computed value was
- WHY the failure happened (root cause)
- HOW it was fixed OR why the spec threshold was wrong

Don't hide failures. Don't pretend a fix is "correct" without re-running the test.

## Test Architecture for Multi-Module Suites

For each module, use FOUR test classes:
1. **`Test<X>Math`** — unit tests for pure math functions (deterministic, no I/O).
2. **`Test<X>Integration`** — runs the actual simulation across N iterations/turns.
3. **`Test<X>Metrics`** — computes precision/recall/F1 from ground truth.
4. **`Test<X>EdgeCases`** — empty inputs, boundary values, language mixing.

Run with `-s` to see print() reports and `-v` for individual test names. Always run from `/root/HERMES` with `PYTHONPATH=/root/HERMES` set.
