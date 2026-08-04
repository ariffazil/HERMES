# Configuration Tuner Log — Cognitive Substrate Phase 1

Trial-by-trial record of config changes and what happened. Include when tuning an agent.

## λ (DECAY_LAMBDA)

| Trial | Value | Half-life | REINFORCED survival | Routine decay speed | Verdict |
|-------|-------|-----------|--------------------|--------------------|---------|
| T1 | 0.10 | ~15 turns | 0% (all ARCHIVE by turn 50) | Good — STM→ARCHIVE by turn 45 | FAIL on reinforced |
| T2 | 0.05 | ~30 turns | 0% (still ARCHIVE, just slower) | Good — unchanged pattern | FAIL on reinforced |
| Conclusion | λ=0.05 is correct for routine decay, but λ alone cannot fix sparse reinforcement. Fix must be structural: boost μ(Ω) or Ω_base on recall events. |

## REINFORCED Memory: Why λ Changes Fail

With λ=0.05, Ω₀=0.30, and reinforcement every 25 turns:
- Turn 25: Ω=0.30 (reinforced), after 25 more turns: Ω=0.30 × e^(-0.05×25×V) ≈ 0.07 → ARCHIVE before next recall.
- Inertia μ(Ω) = 1 - 0.5×0.07 = 0.965 — too weak at low Ω.

**Structural fix (Phase 2):** On `reinforce()`, set μ(Ω) = 1 - η_high × Ω where η_high > η, OR directly set Ω_base to 0.90 for reinforced memories so μ stays high.

## Drift Monitor Thresholds

| Backend | WARNING | ALERT | ON_TOPIC false alarms | Result |
|---------|---------|-------|----------------------|--------|
| TF-IDF | 0.30 | 0.50 | 9/10 (90%) | FAIL |
| Sentence-transformers | 0.30 | 0.50 | 0/10 (0%) | PASS |
| TF-IDF fallback | 0.85 | 0.95 | 0/10 | PASS (raised thresholds) |

## Causal Tagger: Semantic Similarity Regression

| Backend | Accuracy | OBS recall | DER recall | SPEC recall | Result |
|---------|----------|-----------|-----------|-------------|--------|
| Regex only | 78.3% | 92% | 40% | 88% | PARTIAL |
| Regex + sentence-transformers | 57.5% | 56% | 8% | 88% | FAIL — semantic embeddings confused OBS vs DER |

**Root cause:** Sentence-transformers see "based on logs and metrics" as semantically similar to "log shows" → misclassify DER as OBS. Semantic similarity ≠ syntactic causal structure. Keep regex-only for Phase 2.
