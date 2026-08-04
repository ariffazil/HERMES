# Simulation Test Harness — Pitfalls and Calibration Findings

Concrete pitfalls discovered while validating the Phase 1 cognitive modules (memory decay, causal tagger, drift monitor). Each pitfall includes the root cause and the workaround.

## Memory Decay: Half-life vs Sparse Recall

**Symptom**: "Reinforced" memories end up in ARCHIVE tier by turn 200, even though they were recalled 3-5 times.

**Root cause**: With λ=0.10 and value=0.5 (typical for moderate-importance memories), inertia = 1 - 0.5×0.5 = 0.75. Effective decay over gap N is `exp(-0.10 × N × 0.75)`. Half-life ≈ ln(2)/(0.075) ≈ 9 turns. After 15 turns without reinforcement, strength drops to ~0.32 (LTM tier). After 20 turns, ~0.22 (LTM). The decay model as designed means memories die within ~20 turns of any reinforcement gap.

**Workarounds**:
- Tune λ from 0.10 → 0.05 to extend half-life to ~18 turns
- Schedule reinforcement at least every 8 turns for STM retention
- For TASK-tier memories expecting long persistence, use periodic implicit recall (don't expect passive survival)

## Drift Monitor: TF-IDF Baseline Is High

**Symptom**: On-topic conversation gets flagged as DRIFT_ALERT on 90% of turns.

**Root cause**: TF-IDF cosine distance is computed on small-vocabulary short sentences. The intent has 6 unique tokens, a typical turn has 7, only ~2 overlap. With normalization, cosine distance is dominated by vocabulary novelty. Any new term in the output produces distance >0.6.

**Verification**: Unit test `test_no_drift_identical` shows identical sentences score 0.0. `test_major_drift_alert` shows unrelated topics score 1.0. So TF-IDF distinguishes identical vs unrelated but is poor at grading intermediate similarity.

**Workarounds**:
- Use sentence-transformers backend (all-MiniLM-L6-v2) for production — produces graded distances in [0, 0.6] for natural conversation
- If TF-IDF must be used, tighten thresholds to 0.85 (warning) / 0.95 (alert)
- Test RELATIVE behavior (off-topic > on-topic by Δ) rather than absolute thresholds

## Causal Tagger: Pattern Priority Collisions

**Symptom**: DER_CAUSAL recall is low (~40%) — sentences get classified as OBS_CAUSAL or NON_CAUSAL instead.

**Root cause**: The `_classify_evidence` function checks patterns in priority order: OBS → DER → INT → SPEC. Many DER sentences also match OBS patterns (e.g., "Based on metrics from Prometheus and Grafana, X caused Y" — matches OBS pattern via "from the data"). When both match, OBS wins.

**Workarounds**:
- Add explicit DER-pattern precedence (look for "multiple sources", "validated by both", "derived from" FIRST)
- Lower OBS pattern specificity (currently matches "data" and "log" which are too broad)
- Consider pattern exclusivity: a sentence is DER iff DER markers present AND no OBS-only markers

## Memory Decay: Zero-Strength Trap

**Symptom**: Once strength drops near zero, reinforcement doesn't recover the memory.

**Root cause**: `reinforce(strength, recall_count)` computes `strength * (1 + log(1 + recall_count))`. If strength = 0.0001, post-reinforce = 0.0001 × ~2 = 0.0002 — still effectively dead. There's no resurrection mechanism.

**Workarounds**:
- Floor strength at some minimum (e.g., 0.05) so reinforcement has a base to amplify
- Add explicit "resurrect" verb that resets strength to 0.5 when recalled from ARCHIVE
- Track whether a memory has been fully decayed and treat recall as re-injection

## Drift Monitor: Sliding Window Trend Is Unreliable

**Symptom**: "WORSENING" trend declared on first non-identical turn with no prior data.

**Root cause**: `_trend` returns "WORSENING" if mean_delta > 0.02, but with 2 points, a single increase counts as the mean. The 5-window size in production smooths this; the simulation uses 5-point windows so this isn't usually a problem.

**Workarounds**:
- Require minimum 3 points before emitting trend
- Weight recent observations more heavily than older ones
- Add `confidence` field on trend based on window size and variance

## General: Always Test Negative Controls

**Insight**: Every classification/detection module needs a non-causal / on-topic / negative control set. False positive rate is often the most critical metric for production deployment — a detector that fires 90% of the time is useless even with 100% recall.

**Recommended ratio**: 15-20% of dataset should be negative controls. Test that the module returns the right "no-signal" answer on them.
