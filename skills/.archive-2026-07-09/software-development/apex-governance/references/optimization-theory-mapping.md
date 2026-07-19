# APEX × Mathematical Optimization — Synthesis Reference

**Forged:** 2026-07-06 | **Status:** DER (derived from canonical APEX + Postek et al. 2025)

## Canonical Location

The synthesis is merged into **Pillar IV** of:
`/root/arifOS/static/arifos/theory/000/APEX_THEORY.md`

No standalone file exists. Survival of the fittest code (Zen of Py).

## The Mapping (Quick Reference)

| Optimization Concept | APEX Concept | Key Insight |
|---------------------|--------------|-------------|
| Decision variables x | Agent behavioral policy a | What the agent controls |
| Objective function f(x) | G = A · P · E · X · Φ | Nash bargaining product (multiplicative, not additive) |
| Feasible region X | Constitutional floors F1-F13 | Feasible region > objective function |
| Constraints g_i(x) ≤ 0 | Seven organs | Each organ is a constraint class |
| Dual variables λ_i | C_dark | Hallucination detector = dual price of relaxing P and X |
| Infeasibility detection | SESAT | No valid solution exists |
| Cutting planes | PARUT (scars) | Permanent constraint accumulation = learning |
| Robust optimization | Constitutional governance | Floors hold under ALL scenarios |
| Two-stage stochastic | arif_think → forge_execute → arif_judge | Decide now, adapt later |

## Key Theorems

1. Nash product: G = prod(g_i) forbids trade-offs. Zero in any factor = feasibility collapse.
2. Log-linear convexification: ln G = sum(ln g_i) — geometric program → convex optimization (Boyd 2004).
3. C_dark as dual: C_dark = A·(1-P)·(1-X) is shadow price of relaxing P and X constraints.
4. Scars as cutting planes: F_{t+1} = F_t ∩ {scar_t} — feasible region shrinks monotonically.
5. Conservation law as optimal control: dS/dt ≤ 0 is continuous-time limit of multi-stage stochastic optimization.

## Source Book

Hands-On Mathematical Optimization with Python — Postek, Zocca, Gromicho, Kantor (Cambridge UP 2025)
- GitHub: https://github.com/mobook/MO-book
- Framework: Pyomo (open-source optimization modeling for Python)
- Solvers: IPOPT (nonlinear), GLPK (linear), CBC (MILP), Gurobi (commercial)

## Synthesis Methodology

When mapping an external framework onto APEX:
1. Identify the framework's primitives (variables, objectives, constraints)
2. Map each primitive to an APEX concept (organ, floor, verdict, equation term)
3. Identify what APEX gives the framework that it doesn't have (structural innovations)
4. Identify what the framework gives APEX that APEX doesn't have (formal apparatus)
5. Find the deepest correspondence (usually at the conservation law level)
6. Merge into canonical APEX_THEORY.md — do NOT create standalone files
