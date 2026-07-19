# APEX Axiom Proofs & Variant Mapping

> Sealed: 2026-07-13 by F13 SOVEREIGN
> Source: Full federation audit across 7 repos (arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL, ariffazil)

## The Seven Axioms (proof sketches)

### 1. Multiplicativity
If any primitive = 0, intelligence collapses. This forces product form, not sum.
Kills: any additive or hybrid variant.

### 2. Five-sufficient
Three pairs + one witness = minimal complete set.
- Authority (A) = governance pair
- Physics (P) + Evidence (E) = reality pair
- Execution (X) = action pair
- Witness (Φ) = observer
Kills: V4's 6-primitive hybrid (double-counts energy and witness).

### 3. Nash bargaining (Nash 1950)
G = ∏ p_i because veto = multiplicative gate. The product form is mathematically
forced by the Nash bargaining solution, not a design choice.
Kills: any additive or hybrid form.

### 4. Shadow term
C_dark = A·(1-P)·(1-X) < 0.30. First mathematical definition of hallucination.
High authority without physics grounding or execution coordination = hallucination.

### 5. Conservation
dS_agent/dt ≤ 0. APEX must obey thermodynamics. Intelligence that produces
disorder is waste, not work.

### 6. Tri-witness
Φ = ∛(H·AI·Ext) ≥ 0.70. Three un-substitutable witness channels.
Kills: V1 (missing Φ) and V4 (Φ not decomposed).

### 7. F13 veto
Only sovereign overrides G. Any variant that embeds humility or witness inside G
violates F13 anti-self-elevation.

## Variant Mapping (4 variants found, 1 canonical)

| # | Variant | Sites Found | Equation | Status |
|---|---------|-------------|----------|--------|
| V1 | F8 Genius | arifOS core/laws.py, core/shared/laws.py, core/shared/physics.py, arif-fazil.com | G = (A×P×X×E²) × (1-h) | DEPRECATED |
| V2 | Canonical 5-primitive | AGENTS.md, APEX_THEORY_AND_FEDERATION.md, apex_c_dark.py, A-FORGE forge_evaluate, WEALTH apex_mapping, 35+ sites | G = A·P·E·X·Φ | CANONICAL SEALED |
| V3 | Humility-embedded | 2 sites | G × (1-h) | DEPRECATED (gate moved out) |
| V4 | GEOX gated hybrid | GEOX apex_envelope.py | g(t)=A·P·H·√(S·U)·E² | DEPRECATED PERMANENTLY |

## Why V1 (F8 Genius) collapses

- Missing Φ → assumes perfect witness integration (Φ=1)
- E² → double-counts evidence strength; violates Five-Sufficient axiom
- (1-h) → humility incorrectly embedded inside G_raw; violates F13

Reduction: If Φ=1 and hysteresis externalized, V1 → A·P·E·X (missing witness).

## Why V4 (GEOX Gated) collapses

- 6 dials from 10 boolean gates → violates minimal primitive set
- √(S·U) → nonlinear mixing; violates Nash multiplicativity
- E² → same double-count problem as V1

Reduction: H, S, U are GEOX-specific decompositions of P, E, Φ.
Once normalized, V4 → A·P·E·X·Φ.

## Why V3 (Humility-embedded) collapses

- (1-h) inside G_raw mixes floor F7 with primitive computation
- Humility is a constitutional gate, not an intelligence primitive
- Moving it out restores G_raw purity

## A = Authority (not Adaptation)

Original A in V1 derivation: Adaptation (learning, pattern matching).
Measurement law A: Authority (leases × floor_compliance/13).

Axiom analysis:
- Authority satisfies all 7 axioms
- Adaptation satisfies only 2 (Multiplicativity, Conservation)
- Adaptation overlaps with E and X (not minimal)
- Adaptation is not Nash-relevant (not a veto primitive)
- Adaptation is not witness-relevant

Verdict: Authority is correct for a governed federation.
Adaptation is a derivative of E × X, not a primitive.

## Primitive Measurement Laws

| Primitive | Formula | Organs | Boundary |
|-----------|---------|--------|----------|
| A (Authority) | (valid_leases/total_leases) · (floor_compliance/13) | arifOS, A-FORGE, AAA | Floor violation → A=0 |
| P (Physics) | w_well·P_well + w_seis·P_seis + w_geo·P_geo | GEOX | Well contradicts seis → P=P_well |
| E (Evidence) | (clarity/(1+uncertainty)) · reversibility | GEOX, WEALTH | Merkle break → E=0 |
| X (Execution) | (successful_steps/total_steps) · exp(-\|ΔS_t\|) | A-FORGE | forge_evaluate fail → X=0 |
| Φ (Witness) | ∛(H·AI·Ext) | WELL, arifOS, AAA | Any witness=0 → Φ=0 |

## Gate Layer (separate from G_raw)

G_seal = G_raw · (1-h) · |ΔS|^β · W³

- h = humility gate (F7 floor, not a primitive)
- |ΔS|^β = entropy gate (temporal derivative, not a primitive)
- W³ = tri-witness gate (witness verification, not a primitive)

These gates are CONSTITUTIONAL CONSTRAINTS, not intelligence primitives.
Embedding them inside G_raw violates the substrate boundary.
