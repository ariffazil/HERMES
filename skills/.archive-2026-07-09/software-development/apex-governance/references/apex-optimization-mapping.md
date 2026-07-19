# APEX × Mathematical Optimization — Condensed Mapping

> Source: Postek et al. "Hands-On Mathematical Optimization with Python" (Cambridge UP 2025)
> Merged into canonical: `arifOS/static/arifos/theory/000/APEX_THEORY.md` Pillar IV
> Date: 2026-07-06

## Core Correspondence

| Optimization | APEX |
|-------------|------|
| Decision variables $x$ | Agent behavioral policy $a$ |
| Objective $f(x)$ | $G = A \cdot P \cdot E \cdot X \cdot \Phi$ |
| Feasible region $\mathcal{X}$ | Constitutional floors F1–F13 |
| Constraints $g_i(x) \leq 0$ | Seven organs |
| Dual variables $\lambda_i$ | $C_{\text{dark}}$ (partial) |
| Infeasibility detection | SESAT |

## Key Theorems

1. **Nash product structure**: $G = \prod g_i$ forbids trade-offs. Zero in any factor = infeasibility, not just bad objective.
2. **Log-linear convexification**: $\ln G = \sum \ln g_i$ — geometric program → convex optimization (Boyd 2004).
3. **$C_{\text{dark}}$ as dual**: shadow price of relaxing P and X constraints. Hallucination = dual pathology.
4. **PARUT as cutting-plane**: scar accumulation = permanent constraint addition. Feasible region shrinks monotonically = learning.
5. **Constitutional governance = robust optimization**: floors hold under ALL scenarios, not just expected.
6. **Conservation law = optimal control**: $dS/dt \leq 0$ is continuous-time multi-stage stochastic optimization.

## Organ-to-Constraint Map

| Organ | Constraint Type | Formulation |
|-------|----------------|-------------|
| Reality ΔR | Bound | $E(a) \geq E_{\min}$ |
| Governance ΔG | Entropy | $\Delta S(a) \leq 0$ |
| Civilization I_sys | Coupling (network flow) | Flow conservation |
| Execution W | Inequality | $W(a) \geq W_{\min}$ |
| Memory ∂M/∂t | State-dependent (recourse) | $M_{t+1} = M_t + \Delta M_t$ |
| Witness Ω | External verification | $W^3 = \sqrt[3]{H \cdot AI \cdot Ext} \geq \tau$ |
| Meaning ∇F | Gradient direction | $\nabla F(a) \neq 0$ |

## MALU-Gödel ↔ Optimization Repair

SESAT = infeasibility detection → MALU = infeasibility certificate → HOLD = solver stop → GÖDEL LOCK = undecidable from inside → SAKSI = constraint addition → TEBUS = objective cost → PARUT = permanent constraint pool update → LURUS = re-solve with augmented constraints.

## Book Chapters → APEX Domains

- Ch. 2-3 (Linear/MILP): Basic optimization + integer decisions (F1 reversibility is binary)
- Ch. 4 (Network): A2A mesh, $I_{\text{sys}}$ flow conservation
- Ch. 5 (Convex/SVM): Φ integration as semidefinite constraint
- Ch. 8 (Robust): Constitutional governance = min-max over uncertainty set
- Ch. 9 (Stochastic): Expected G across scenarios
- Ch. 10 (Two-stage): `arif_think(plan)` → `forge_execute` → `arif_judge`. MALU-Gödel = recourse action.
