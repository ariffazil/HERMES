# APEX G Cross-Repo Empirical Verification (2026-07-28)

**Context:** Validated the canonical APEX T-000 theorem `G = (A·P·E·X)^(1/4)` against implementations in A-FORGE (TypeScript, `apexDials.ts`) and arifOS (Python, `genius.py`).

## Canonical Spec

| Property | Value |
|----------|-------|
| **Formula** | `G = (A · P · E · X)^(1/4)` — geometric mean (Nash bargaining product) |
| **Each dial** | Normalized [0, 1] |
| **G ≥ 0.80** | SEAL |
| **0.70 ≤ G < 0.80** | SABAR |
| **G < 0.70** | HOLD |
| **VOID** | Reserved for hard floor breach (F13, F9, F10, F12) |
| **C_dark** | `A · (1-P) · (1-X)`; threshold < 0.30 |

## Key Implementation Files

| Repo | File | Role |
|------|------|------|
| A-FORGE | `src/domain/governance/apexDials.ts` | Canonical runtime implementation |
| A-FORGE | `src/domain/cognition/taskJacobian.ts:303` | Local actuator estimate (self-declared non-canonical) |
| arifOS | `core/enforcement/genius.py` | PCA + fallback cluster dial derivation |
| arifOS | `governance/_t000_evaluator/compute_apex.py` | Evaluator script (uses E²/5th root — non-canonical) |

## Critical Finding: Zero-Handling Divergence

The **most important finding** was a semantic divergence in how zero values are handled:

| Implementation | Code | Zero Behavior |
|---------------|------|---------------|
| **A-FORGE** `geometricMean()` | `values.filter(v => v > 0)` | **Filters out zeros silently** — a dial of 0 is ignored, producing inflated G |
| **arifOS** Python `geometric_mean()` | `any(s <= 0.0) → return 0.0` | **Returns 0 on any zero** — mathematically correct Nash collapse |

**Implication:** A floor score of 0.0 (complete failure) in A-FORGE is silently dropped from the geometric mean, meaning G does not collapse. This undermines the "weakest-link" property the canonical formula was designed for.

## Legacy E² References Found

### A-FORGE (runtime code)

| File:Line | Reference | Severity |
|-----------|-----------|----------|
| `taskJacobian.ts:303` | `const G = A * P * X * E * E * (1 - humilityCap)` | MEDIUM — uses E×E, self-aware legacy |
| `apexDials.ts:430` | Comment: "6 dials (A,P,H,S,U,E) → G" | LOW — stale comment |
| `AgentEngine.ts:879` | Comment: "K777_APEX §10.4: G = A × P × X × E²" | LOW — stale comment |

### arifOS (runtime code)

| File:Line | Reference | Severity |
|-----------|-----------|----------|
| `genius.py:14` | Docstring: `G = A × P × X × E²` | **HIGH** — misleading header on active runtime file |
| `core/laws.py:201` | `"F8": "Genius - G = (A × P × X × E²) × (1 - h)"` | **HIGH** — wrong law description |
| `core/shared/laws.py:827,852` | Formula definition + logging with E² display | HIGH — wrong canonical formula |
| `core/shared/physics.py:698,705,714,773` | F8 Genius defined as E² formula | MEDIUM — 4 stale references |
| `compute_apex.py:3,130` | `G = (A·P·E²·X)^(1/5)` | MEDIUM — evaluator uses non-canonical formula |
| `replay_apex_comparison.py:42,64` | `g(t)=A*P*H*S*U*E²` | LOW — self-labelled legacy comparison |
| `engineer.py:338,433` | Prompt templates reference E² | LOW |
| `tools.py:4541` | Registry entry with V4 hybrid | LOW |

## C_dark Status

C_dark (`A · (1-P) · (1-X)`) is:
- ✅ Defined in docs (okf, docs, GENESIS)
- ✅ Implemented in `arifOS/commands/scripts_deploy/recursive_governed_loop.py:152-159`
- ❌ **NOT computed** in A-FORGE's runtime APEX path (`apexDials.ts`, `calculateGeniusFromFloors`, `computeApex10Gates`)
- ✅ F9 (Anti-Hantu) floor acts as runtime proxy for C_dark

## Empirical Test Vectors

### Nash Collapse (all pass math, but impl diverges)
- `gm([1,1,1,0])` → A-FORGE: **1.0** (zero filtered), arifOS: **0.0** (Nash collapse)
- `gm([0,1,1,1])` → A-FORGE: **1.0**, arifOS: **0.0**
- `gm([0.5,0.5,0.5,0.5])` → **0.5** (both)
- `gm([0,0,0,0])` → A-FORGE: **0** (empty filter), arifOS: **0.0**

### Monotonicity (all pass)
- `gm([0.8,0.8,0.8,0.8])` → 0.8
- `gm([0.9,0.8,0.8,0.8])` → 0.824 > 0.8 ✓
- `gm([0.7,0.8,0.8,0.8])` → 0.774 < 0.8 ✓

### C_dark
- `A=0.8, P=0.8, X=0.8` → 0.032 (< 0.30, safe)
- `A=1.0, P=0.1, X=0.1` → 0.81 (≥ 0.30, hallucination risk)
- `P=1.0 or X=1.0` → 0.0 regardless of A

## Verification Pattern

When validating a canonical formula across two repos:

1. **Grep all repos** for the old formula variable names (H, S, U, E², "E*E") — some are in comments, docstrings, law definitions, and runtime code
2. **Test known mathematical properties**: zero boundary, monotonicity, uniform values
3. **Test companion formulas** (C_dark) even if they're not in the main impl path
4. **Check for semantic divergence** in utility functions (e.g., geometricMean filtering zeros vs returning 0)
5. **Verify build** passes on the canonical repo
6. **Compile results** into a PASS/FAIL table per test case
