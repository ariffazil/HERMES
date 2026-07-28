# APEX G Falsification Methodology — Session Record (2026-07-28)

> **Epistemic tag:** VERIFIED (by Arif F13 correction). This document captures the session where Arif corrected the APEX G mathematical foundation from "canonical formula" to "conjecture that must survive falsification."

## The Three Categories (Arif's Key Distinction)

| Category | What it is | What kills it |
|----------|-----------|---------------|
| **Model / Conjecture** | "the world behaves like this" | One counterexample from reality |
| **Theorem** | "this follows from these axioms" | One counterexample within the axiom set |
| **Empirical Validation** | "the data matches the model" | One measurement that contradicts prediction |

**Before this session:** G = (A×P×E×X)^(1/4) was treated as Level 6 (Production implementation) without passing Level 2-4.

**After this session:** The formula is recognized as Level 2-3 (Axiom set + Proof sketch), aiming for Level 5 after falsification tests.

## The Falsification Tests (Arif's 3)

Arif challenged: "Adakah arithmetic mean, harmonic mean, or weighted geometric mean also satisfy the same axioms?"

| # | Test | Pass/Fail | Why |
|---|------|-----------|-----|
| 1 | Arithmetic mean (A+P+E+X)/4 | **FAIL** — violates A1 | Nash Collapse: (0,1,1,1) → 0.75 ≠ 0 |
| 2 | Harmonic mean 4/(1/A+1/P+1/E+1/X) | **FAIL** — violates A6 | Multiplicativity: G(x·y) ≠ G(x)·G(y) |
| 3 | Weighted GM A^a·P^b·E^c·X^d | **FAIL** — violates A7 | Equal Dignity: unequal weights need constitutional justification |

**Result:** All 3 alternative formulas refuted. G = (A×P×E×X)^(1/4) survives. The formula is not yet refuted.

## The Missing Axiom That Made It Work

Before Arif's correction, the axiom set had no **multiplicativity** axiom. This meant the harmonic mean was a valid counterexample — it satisfied ALL stated axioms. The missing axiom:

> **A6 (Multiplicativity):** G(x₁·y₁, x₂·y₂, x₃·y₃, x₄·y₄) = G(x₁, x₂, x₃, x₄) · G(y₁, y₂, y₃, y₄)

This came from Nash 1950 bargaining theory: the geometric mean is the unique function satisfying symmetry + multiplicative separability + normalization.

## The Complete Axiom Set (APEX G)

| Axiom | Statement | Why needed |
|-------|-----------|------------|
| A1 (Nash Collapse) | Any dial ≤ 0 → G = 0 | Rules out arithmetic mean |
| A2 (Permutation Symmetry) | G is invariant under dial permutation | Rules out weighted GM with unequal weights |
| A3 (Monotonicity) | G strictly increasing in each dial (d > 0) | Ensures improvement ≠ degradation |
| A4 (Dial Range) | Each dial d ∈ [0, 1], unitless ratio-scale | Scale constraint |
| A5 (Normalization) | G(k, k, k, k) = k for any k ∈ [0, 1] | Identity property |
| A6 (Multiplicativity) | G(x·y) = G(x) · G(y) | Rules out harmonic mean |
| A7 (Equal Dignity of Dials) | w_A = w_P = w_E = w_X = 1/4 | Rules out any weighted version |
| A8 (F8 Threshold) | G ≥ 0.80 = Genius | Policy choice, not mathematically derivable |

## Proof of Uniqueness

```
1. Axioms A6 (multiplicativity) + A5 (normalization)
   → By Aczél's characterization theorem, G must be a weighted geometric mean
   → G(d₁, d₂, d₃, d₄) = ∏ d_i^(w_i) where ∑ w_i = 1

2. Axiom A7 (equal dignity of dials)
   → w_A = w_P = w_E = w_X = 1/4
   → No dial is constitutionally privileged

3. Therefore G = (A · P · E · X)^(1/4)

4. Verify A1 (Nash collapse): any d_i = 0 → ∏ d_i = 0 → G = 0 ✓
5. Verify A2 (symmetry): multiplication is commutative ✓
6. Verify A3 (monotonicity): all exponents positive ✓
7. Verify A4 (range): GM of [0,1] values ∈ [0,1] ✓
```

## Truth Ladder Status (After Session)

```
Level 0 — Idea                     ✅
Level 1 — Conjecture               ✅
Level 2 — Axiom set formalized     ✅ (8 axioms)
Level 3 — Proof sketch             ✅ (4 theorems proven)
Level 4 — Counterexample search    ✅ (3 falsification tests)
Level 5 — Machine verified proof   🔄 (OpenCode building ts)
Level 6 — Production patches       🔄 (OpenCode applying)
Level 7 — Empirical validation     ❌ (requires live federation data)
```

## Geological Analogy

The Popperian falsification approach maps naturally to geology:

| Geology concept | APEX Math concept |
|----------------|-------------------|
| Stratigraphic principles (superposition, cross-cutting) | Axioms (A1-A8) |
| Expected formation boundary | Theorem (G formula) |
| Drilling a test well | Falsification test (try all alternative formulas) |
| Core sample contradicts model → REFUTE | Test fails → formula is wrong |
| Revise stratigraphic model | Add/change axioms to close gap |

**Arif's words:** "Macam geologist fikir — 1 outcrop boleh refute regional model. 1 counterexample boleh refute mathematical claim."

---

## Comprehensive Update (2026-07-28, Second Session)

### What Changed

A second falsification session formalized the complete axiom set, tested all 7 axioms against 4 aggregators, produced the log-space Cauchy uniqueness proof, and formalized G-space and J-space.

### Corrected Proof Chain

The earlier proof chain ("A6 + A5 → weighted GM → A7 → equal weights") was **imprecise**. The actual Aczél characterization uses **symmetry (A2)**, not normalization (A5), as the partner to multiplicativity. The correct chain:

```
A2 (Symmetry) + A6 (Multiplicativity) + continuity
  → log-space: g(x+y) = g(x) + g(y)   (Cauchy additivity)
  → symmetry + additivity: g(x) = c·Σx_i
  → back-transform: G(d) = (∏d_i)^c
  → A7 (Uniform Identity): G(a,a,a,a) = a → c = 1/4
  → THEREFORE G = (A·P·E·X)^(1/4) uniquely
```

**Key difference:** A2 (symmetry), not A5, is the primitive that forces the linear form. Normalization (A7) is needed only to fix c = 1/4. The minimal sufficient set is {A2, A6, A7} + continuity.

### G-Space and J-Space Added

The new document formalizes:
- **G-space** = [0,1]^4 with log-Euclidean metric
- **Trajectories:** improving, degrading, level, collapsing paths
- **Attractors:** Nash collapse boundary, SEAL surface, fixed point, uniform diagonal
- **Log-space duality:** GM in G-space = AM in log-space
- **J-space framing:** 5 open questions about judgement as an operator from G-space to actions

### Full Document

The comprehensive falsification document (736 lines, 28 KB) lives at:

`/root/A-FORGE/forge_work/2026-07-28/APEX-G-FALSIFICATION.md`

All numerical counterexamples verified via Node.js execution.

### Updated Related Files

- `/root/A-FORGE/forge_work/2026-07-28/APEX-G-FALSIFICATION.md` — Full falsification analysis (this session's work)
- `apex-verification-pipeline` skill → `references/apex-g-uniqueness-proof-2026-07-28.md` — Concise reference to the proof published 2026-07-28
- This file — Updated to point to the comprehensive document

## The Failure That Triggered This Session

The previous automated sweep (OpenCode, deleg_ca287a6d) produced `/root/A-FORGE/forge_work/2026-07-28/APEX_ALIGNMENT_SWEEP.md` which treated G = (A×P×E×X)^(1/4) as the "canonical formula." It was treated as Level 6 truth without passing Level 2-4 verification.

Arif responded with ChatGPT's mathematical truth framework and 3 falsification tests that proved the axiom set was incomplete. The harmonic mean satisfied all stated axioms — meaning the formula was NOT uniquely determined.

**Lesson:** Every formula claiming to be "canonical" must be tested against alternatives. The formula is not a theorem until uniqueness is proved.

## Related Files

- `/root/A-FORGE/forge_work/2026-07-28/APEX_ALIGNMENT_SWEEP.md` — Initial sweep report (before correction)
- `/root/arifOS/docs/APEX_MATH_CANON.md` — Axiom foundation + theorem proofs (OpenCode building)
- `/root/A-FORGE/test/apex_falsification.test.ts` — Falsification test suite (OpenCode building)
- This reference file — Session record of Arif's correction
