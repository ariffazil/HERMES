# APEX G Math Unification — Proof-Theoretic Falsification Session

**Date:** 2026-07-28  
**Scope:** arifOS + A-FORGE (2 repos, 9 files, 10 drift sites)  
**Canonical:** `G = (A × P × E × X)^(1/4)` — F13-ratified  

## What Was Built

### 1. Axiomatic Proof System
File: `/root/arifOS/docs/APEX_MATH_CANON.md`
- 5 axioms (A1-A5): Nash Collapse, Geometric Aggregation, Four Dials Only, Dial Range, F8 Threshold
- 5 definitions (D1-D5): Dial, Proof, Counterexample, Refutation, Proof Obligation
- 4 inference rules (IR1-IR4): Substitution, Monotonic Inference, Commutative Symmetry, Dimensionality Matching
- 7 theorems (T1-T7) with formal derivations from axioms
- 3 corollaries (C1-C3) with enforcement directives
- Geological analogies for Arif (geologist)

### 2. Falsification Test Suite
File: `/root/A-FORGE/test/apex_falsification.test.ts`
- 43 tests across 15 suites
- All 5 axiom property tests (Nash Collapse, Geometric Aggregation, 4 Dials, Range, Threshold)
- All theorem verification tests (Monotonicity T3, Symmetry T4)
- Falsification tests with explicit counterexamples (E² T5, Φ T6, Product T7)
- A6 Multiplicativity verification (GM property proved, arithmetic/harmonic refuted)
- A7 Equal Dignity (weighted GM refuted)
- Cross-implementation consistency verification
- Corollary enforcement (C1-C3)

### 3. Patches Applied

| File | Fix | Type |
|------|-----|------|
| `apexDials.ts:518` | `GM(A,P,E)×X` → `GM(A,P,E,X)` | Runtime |
| `apexDials.ts:288` | equation string to canonical | Display |
| `apexDials.ts:540` | equation string to canonical | Display |
| `genius.py:15` | `A·P·E·X·Φ` → `(A×P×E×X)^(1/4)` | Docstring |
| `genius.py` APEXDials | Removed PHI field | Type |
| `genius.py` cluster | Removed PHI computation | Runtime |
| `genius.py` PCA | Removed PHI computation | Runtime |
| `apex_g_standardization.test.ts` | Product→GM expectations | Test |
| `AGENTS.md:228` | E²·(1-h) → canonical F8 | Doc |
| `CLAUDE.md:159` | E²/5-root → canonical | Doc |
| `APEX_CANON.md:5` | E²/5-root → canonical | Doc |
| `APEX_FALSIFIABILITY_PROTOCOL.md:62` | Product → canonical | Doc |

## Key Insights

### Floating Point in Axiom Tests
When testing the A6 multiplicativity axiom (`G(x·y) = G(x)·G(y)`), rounded implementations fail `strictEqual` because intermediate rounding at 4dp introduces ±0.0001 differences. **Fix:** For rounded comparisons, use `Math.abs(actual - expected) <= 0.0002`. Only raw (unrounded) GM gives exact equality.

### Non-Uniform Counterexamples
Uniform inputs can accidentally give equal results for different formulas:
- `(0.8^5)^(1/5) = 0.8` and `(0.8^4)^(1/4) = 0.8` are equal for uniform 0.8
- But `(0.8·0.8·0.5·0.8)^(1/4) ≈ 0.712` vs `(0.8·0.8·0.5·0.5·0.8)^(1/5) ≈ 0.664`
- Always use non-uniform inputs in falsification tests

### Floor Semantics Mismatch
The `floorsToDials` function interprets `f9_antihantu` and `f12_injection` as SCORES (0=bad, 1=good), not as violation flags. Tests that assumed 0 = "clean" failed because zero values cascade through the geometric mean to collapse E and X dials.

### TaskJacobian is Not Canonical G
`computeGFromJacobian` is documented as a local actuator estimate using product-style A·P·E·X·(1-humilityCap). This is NOT canonical G. It should NOT match the canonical formula. Cross-implementation tests must skip this function or explicitly note its different role.
