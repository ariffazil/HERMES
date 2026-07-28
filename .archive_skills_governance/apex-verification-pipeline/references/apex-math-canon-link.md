# APEX Math Canon — Quick Reference

**Source of truth:** `/root/arifOS/docs/APEX_MATH_CANON.md`
**Falsification tests:** `/root/A-FORGE/test/apex_falsification.test.ts` (43 tests)
**Last updated:** 2026-07-28

## Canonical Formula

```
G = (A × P × E × X)^(1/4)
```

## The 8 Axioms (Constitutional Foundation)

| # | Name | Key Insight |
|---|------|-------------|
| A1 | Nash Collapse | Any dial ≤ 0 → G = 0. Arithmetic mean refuted. |
| A2 | Permutation Symmetry | Multiplication is commutative. Order doesn't matter. |
| A3 | Monotonicity | ∂G/∂d = G/(4d) > 0 for d > 0. |
| A4 | Dial Range | All d ∈ [0, 1]. |
| A5 | Normalization | G(k,k,k,k) = k. Uniform inputs preserved. |
| A6 | Multiplicativity | G(x·y) = G(x)·G(y). Nash bargaining axiom. |
| A7 | Equal Dignity | w = 1/4 for all dials. |
| A8 | F8 Threshold | G ≥ 0.80 → Genius. Policy axiom. |

## Uniqueness Proof (One-paragraph)

A5 + A6 → by Aczél characterization, G must be a weighted geometric mean
G = A^wA · P^wP · E^wE · X^wX with wA + wP + wE + wX = 1.

A7 (equal dignity) → wA = wP = wE = wX = 1/4.

Therefore G = A^(1/4)·P^(1/4)·E^(1/4)·X^(1/4) = (A·P·E·X)^(1/4).

A1 (zero collapse), A2 (commutativity), A3 (monotonic), A4 ([0,1] closure)
all verify. This is the UNIQUE function satisfying all axioms. ∎

## The Four Counterexample-Refuted Formulas

| Formula | Refuted By | Counterexample |
|---------|-----------|----------------|
| (A+P+E+X)/4 | A1 (Nash) | (0,1,1,1) → 0.75 ≠ 0 |
| 4/(1/A+1/P+1/E+1/X) | A6 (Mult) | H(x·y) ≠ H(x)·H(y) |
| A^0.4·P^0.3·E^0.2·X^0.1 | A7 (Dignity) | Unequal weights produce different G |
| A·P·E·X·Φ | A7 + A1 | 5-dial ≠ 4-dial; Φ is HARAM |

## Truth Ladder

| Level | Status | What |
|-------|--------|------|
| 0 | ✅ Idea | Geometric mean might uniquely satisfy constitutional axioms |
| 1 | ✅ Conjecture | Formal conjecture: no other aggregator satisfies all axioms |
| 2 | ✅ Axioms | 8 axioms formalized in APEX_MATH_CANON.md |
| 3 | ✅ Proofs | 4 theorems with Aczél characterization |
| 4 | ✅ Falsification | 6 falsification tests survive counterexample search |
| 5 | ✅ Machine-verified | node --test: 43/43 pass |
| 6 | ✅ Production | All code paths patched to canonical formula |
| 7 | ❌ Empirical | Requires live federation data |

## Geological Framing

Treat G like a geological hypothesis:
- Axioms = stratigraphic principles (superposition, cross-cutting)
- Theorems = expected formations
- Counterexample search = drilling a test well
- Core contradicts model → REFUTE and rebuild
- Don't retrofit model to match core — bad science
