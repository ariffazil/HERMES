# Phase 1 Tuning Round 1 (2026-08-04) — session record

Concise reproduction recipe for the four surgical fixes that resolved
`SIMULATION_REPORT.md` issues P0–P3. Kept under the cognitive-package-patterns
umbrella because the fix shape is reusable across future Phase-N rounds.

## Simulation findings that drove the fixes

| Phase | Module       | Verdict  | Symptom |
|-------|--------------|----------|---------|
| A     | memory_decay | PARTIAL  | REINFORCED memories (3–5 recalls/200 turns) decay to ARCHIVE — λ=0.10 → ~15-turn half-life, too fast for sparse recall schedule |
| B     | causal_tagger | PASS    | DER_CAUSAL recall 0.40 (15/25 missed); avg conf correct 0.546 < incorrect 0.561 (inverted calibration) |
| C     | drift_monitor | PARTIAL | ON_TOPIC scenario: 9/10 turns flagged DRIFT_ALERT (TF-IDF baseline >0.5 for non-identical sentences even when on-topic) |

## The four fixes

### P0 — Drift monitor backend flip

**Before:** `_build_default_embedder()` returned `TfidfEmbedder()` always.
**After:** try `SentenceTransformerEmbedder("all-MiniLM-L6-v2")`, fall back to TF-IDF on any exception.

```python
def _build_default_embedder() -> Any:
    try:
        return SentenceTransformerEmbedder()
    except Exception:
        return TfidfEmbedder()
```

Trigger condition: the heavy backend is small, already installed, and the deterministic backend produces systematically wrong verdicts on the simulation ground truth. Verify by simulation re-run, not unit tests (unit tests on identical text work for both backends and miss the discrimination gap).

Also relax `tests/test_drift_monitor.py::test_backend_name` to `assert monitor.backend in ("sentence-transformers", "tfidf")`.

### P1 — λ halved

**Before:** `LAMBDA_DECAY = 0.10` in `cognitive/config.py`.
**After:** `LAMBDA_DECAY = 0.05`. Doubles the half-life from ~15 turns to ~30 turns; REINFORCED memories now stay in STM with realistic 3–5 recall cadence over 200 turns. Annotation in `config.py` explains the provenance.

Propagation: works automatically if all consumers import from `config.py`. The simulation harness does. The Phase 2 engine module (`memory_decay/engine.py`) defines its own copy as a default kwarg, so any consumer that imports `LAMBDA_DECAY` from `engine` directly bypasses `config.py` — always import from `config.py` or use `from cognitive.config import LAMBDA_DECAY as _LAMBDA` and pass `_LAMBDA` as the default.

### P2 — DER-before-OBS pattern ordering + DER-pattern expansion

**Before:** `_classify_evidence()` checked `_OBS_PATTERN` first.
**After:** check `_DER_PATTERN` first; multi-source sentences containing trace/log keywords now classify correctly.

```python
if _DER_PATTERN.search(text):
    return "DER_CAUSAL", CAUSAL_DERIVED_CAP
if _OBS_PATTERN.search(text):
    return "OBS_CAUSAL", CAUSAL_OBSERVED_CAP
# ...
```

Also expand `_DER_PATTERN` to cover patterns the original regex missed: `based on .+ and`, `both .+ and .+ show`, `derived from .+ and`, `combination of`, `data from both`, `correlation between .+ metrics`, and BM equivalents (`berdasarkan .+ dan`, `diperoleh .+ dan`).

**Rule of thumb (now codified in the umbrella skill):** check the more-specific tier first. DER (multi-source agreement) is more specific than OBS (single-source trace); INT (single-source inference) is more specific than SPEC (no evidence).

### P3 — Confidence calibration via marker density

**Before:** every match returned the flat per-class cap (`OBS_CAUSAL = 0.90`, `DER_CAUSAL = 0.85`, …).
**After:** weight confidence by marker density:

```python
matches = _OBS_PATTERN.findall(text)
strength = min(len(matches) / 3.0, 1.0)
conf = CAUSAL_OBSERVED_CAP * (0.85 + 0.15 * strength)
```

This is **calibration**, not cap duplication. The flat cap is still enforced by `Receipt.__post_init__`. Per-class base confidence varies below the cap, so correct predictions now score higher than incorrect ones. After the fix the simulation shows "Avg conf correct > Avg conf incorrect" — GOOD calibration.

## The hidden trap: concurrent Phase 2 partial rebuild

While applying P2/P3 to the Phase 1 `causal_tagger/tagger.py` and P1 to `memory_decay/engine.py`, the engine.py and tagger.py were **overwritten** by a parallel Phase 2 rewrite that renamed `MemoryItem → MemoryRecord` and changed the regex vocabulary. The patches landed in the old code, then were replaced.

Recovery strategy applied:

1. Stop applying patches to the Phase 2 code without first reading what version is current.
2. Add backward-compatibility shims at the bottom of the new `engine.py` so the Phase 1 test suite and simulation harness work unchanged:
   - Re-declare old dataclass names (`MemoryItem`, `DecayResult`, `ReinforcementResult`, `QuantizationResult`) as frozen shims.
   - Translate old stateless helpers (`value_score`, `score_dependent_inertia`, `effective_decay`, `reinforce`, `tier_for_strength`, `quantize_strength`) using the new engine math.
   - Pull canonical constants (`Ω₀`, `λ`, `η`, tier thresholds, factor weights) from `cognitive.config` — never duplicate them in the shim.
3. Update `<module>/__init__.py` to re-export both Phase 2 and Phase 1 names.
4. Re-apply P1/P2/P3 fixes to the **new** code surface (the Phase 2 `classify()` function), not the old one.

## Verification commands (run in this order)

```bash
# 1. Unit tests
cd /root/HERMES && python -m pytest cognitive/tests/ -v --no-header

# 2. Syntax check
python -m compileall -q cognitive

# 3. Simulation re-run (writes SIMULATION_REPORT.md)
cd /root/HERMES && python -m cognitive.simulation.run_simulation

# 4. Compare against pre-tune report
diff cognitive/simulation/SIMULATION_REPORT.md{,.bak}
```

Expected post-tune deltas (verified by simulation re-run):

- Phase A REINFORCED: 0% → ≥80% correct.
- Phase B DER_CAUSAL recall: 0.40 → ≥0.85 (DER-before-OBS + pattern expansion).
- Phase B confidence: `correct > incorrect` (calibration).
- Phase C ON_TOPIC: 9/10 false ALERTs → 0 false ALERTs (sentence-transformers backend).

## Lessons encoded back to the umbrella skill

- Embedder "deterministic default" rule got an explicit exception clause for when simulation re-run contradicts the heuristic.
- Confidence cap got an explicit "calibration ≠ duplication" carve-out.
- New pitfall #7: pattern-check order is part of the contract; check the more-specific tier first.
- New section: Compatibility shims for partial Phase-N rebuilds — the recipe for bridging a partially-applied Phase 2 to Phase 1 consumers without rewriting the test suite or simulation.