# APEX G Uniqueness Proof — {A2, A6, A7} → Geometric Mean

> **Pointer to the comprehensive falsification document.**
> Read this BEFORE relying on the proof chain in any APEX computation.
>
> **Status:** All numerical counterexamples verified via Node.js · 2026-07-28

## Source

The full falsification analysis — including the 7-axiom definition matrix, the 4-aggregator × 7-axiom falsification table, the log-space Cauchy uniqueness proof, G-space formalization (metric, trajectories, attractors), and J-space framing — lives at:

**`/root/A-FORGE/forge_work/2026-07-28/APEX-G-FALSIFICATION.md`**

## Key Results

### Uniquely Proved

The geometric mean `G = (A·P·E·X)^(1/4)` is uniquely characterized by:

| Axiom | Property | Role |
|-------|----------|------|
| **A2** | Symmetry (permutation invariance) | Eliminates unequal-weight WGM |
| **A6** | Multiplicativity (G(x·y) = G(x)·G(y)) | Eliminates AM and HM |
| **A7** | Uniform identity (G(a,a,a,a) = a) | Fixes exponent to 1/4 |
| **Continuity** (or strict monotonicity) | Makes Cauchy additivity tractable | Closes the functional equation |

### Alternatives Disproven

| Aggregator | Formula | Killed by | Counterexample |
|------------|---------|-----------|----------------|
| Arithmetic Mean | (A+P+E+X)/4 | A3, A5, A6 | AM(0,1,1,1) = 0.75 ≠ 0 |
| Harmonic Mean | 4/(1/A+1/P+1/E+1/X) | A6 | HM(x)·HM(y) ≈ 0.1916 ≠ 0.1855 |
| Weighted GM (unequal) | A^wA·P^wP·E^wE·X^wX | A2 | WGM(d) = 0.478 ≠ 0.363 after permutation |
| Weighted GM (equal) | = GM | **Survives** | This IS the unique survivor |

### Previously Incorrect Chain

The old skill said: "A5 + A6 → weighted GM → A7 → equal weights." This was wrong. The correct chain is:

```
A2 (Symmetry) + A6 (Multiplicativity) + continuity
  → log-space: g(x+y) = g(x) + g(y) (additivity from multiplicativity)
  → symmetry + additivity: g(x) = c·Σxᵢ
  → back-transform: G(d) = (∏d_i)^c
  → A7 (uniform identity): G(a,a,a,a) = a → c = 1/4
  → G = (A·P·E·X)^(1/4) uniquely
```

A2 (symmetry), not A5 (normalization), is the property that forces the linear form `g(x) = c·Σxᵢ`. Normalization (now A7) is needed only to fix the constant `c`.

### J-Space as Open Question

The falsification document closes with the J-space framing: can judgement be modelled as an operator J: G-space → actions? Five hard questions are posed:

1. Is judgement continuous or discrete?
2. Is action space linear or a poset?
3. Does judgement compose per-dial?
4. Is there a J-equivalent of multiplicativity?
5. What is the topology of J-space?

These remain **UNSOLVED** — framed for future work.
