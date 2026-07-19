# APEX Variant Audit — Complete Mapping (2026-07-13)

> Sealed by F13 SOVEREIGN request. Full audit across all 7 federation repos.

## Four Variants Found

### V1: Canonical 5-primitive (CANONICAL)

**Equation:** G = A · P · E · X · Φ
**Shadow:** C_dark = A · (1-P) · (1-X)
**Law:** dS_agent/dt ≤ 0

**Found in:**
- `/root/AGENTS.md` (lines 36, 47-49)
- `/root/A-FORGE/APEX_THEORY_AND_FEDERATION.md` (line 321)
- `/root/A-FORGE/src/interfaces/mcp/forgeTools.ts` (forge_evaluate, line 1262)
- `/root/A-FORGE/src/contracts/types.ts` (line 69)
- `/root/WEALTH/wealth_core/optimizers/apex_mapping.py` (line 7)
- `/root/arifOS/arifosmcp/runtime/apex_c_dark.py` (line 381)
- `/root/arifOS/commands/scripts_deploy/recursive_governed_loop.py` (line 150)
- All agent cards (hermes-asi.json, makcikgpt.json, continue-cli.json, codex.json, etc.)
- `/root/HERMES/skills/seven-zen-organs-enforcement/SKILL.md` (line 71)
- `/root/HERMES/skills/seven-zen-organs-enforcement/references/apex-theory-synthesis-2026-07-05.md` (line 28)

### V2: F8 Genius (DEPRECATED as standalone)

**Equation:** G = (A × P × X × E²) × (1 - h)

**Found in:**
- `/root/arifOS/core/laws.py` (line 201)
- `/root/arifOS/core/shared/laws.py` (line 826)
- `/root/arifOS/core/shared/physics.py` (lines 705, 773)
- `/root/ARIF-SITES/sites/arif-fazil.com/public/CLAUDE.md` (line 94)

**Mapping to V1:**
- V2.A (Akal) ≈ V1.A (Adaptation)
- V2.P (Peace) ≈ V1.P (Perception)
- V2.X (Exploration) ≈ V1.X (Cross-domain)
- V2.E² (Energy squared) ≈ V1.E (Execution) — V2 weights execution more heavily
- V2 has NO Φ — assumes Φ=1 (integration perfect)
- V2 adds h (Hysteresis) — penalty for previous failures, implementation detail

**Why deprecated:** V2 is a degenerate case of V1 with Φ=1. It is MORE optimistic
than V1 (assumes integration is always present). The hysteresis term is an
implementation detail of the F8 floor, not a theory primitive.

### V3: GEOX Gated (DEPRECATED as standalone)

**Equation:** g(t) = A(t) · P(t) · H(t) · √(S(t) · U(t)) · E(t)²

**Found in:**
- `/root/GEOX/src/geox_core/apex_envelope.py` (line 29)
- `/root/GEOX/src/geox_core/apex_envelope_geox.py` (line 27)

**Mapping to V1:**
- V3.A (Amanah/Humility/Understanding geometric mean) ≈ V1.A (Adaptation)
- V3.P (Presence) ≈ V1.P (Perception)
- V3.H (Authority/Sovereign min) ≈ V1.Φ (Integration)
- V3.S (Signal) ≈ part of V1.P (evidence quality)
- V3.U (Reversibility/Proof) ≈ part of V1.E (execution quality)
- V3.E² (Energy squared) ≈ V1.E (Execution)

**Why deprecated:** V3 is the GEOX domain adapter. It maps geological evidence
signals (claim_state, boundary, uncertainty_declared, evidence_refs) through
10 boolean gates into 6 dials, then computes G. The gates are evidence signals,
not theory primitives. V3 should reference V1 as its canonical source.

### V4: C_dark Shadow (INSEPARABLE)

**Equation:** C_dark = A · (1-P) · (1-X)

**Found in:**
- `/root/arifOS/arifosmcp/runtime/apex_c_dark.py` (line 384)
- `/root/AGENTS.md` (line 48)
- All agent cards
- All APEX governance references

**Status:** NOT a competing formula. It is the shadow term of V1. Every G
computation MUST also produce C_dark. They are one formula with two outputs.

## Five Axioms

1. **Multiplicativity (Zero-Collapse):** Zero in any primitive → G=0. Nash 1950 bargaining product.
2. **Conservation Law (Thermodynamic):** dS_agent/dt ≤ 0. Landauer bound.
3. **Shadow Term (Hallucination Definition):** C_dark = A·(1-P)·(1-X). First mathematical definition of hallucination.
4. **Seven Organs (Conservation Laws):** Reality, Governance, Civilization, Execution, Memory, Witness, Meaning.
5. **Tri-Witness (Nash 1950):** W³ = ∛(Human × AI × External). Zero in any channel collapses witness.

## Falsifiability

Four levels:
1. **Component:** Each primitive independently measurable
2. **Shadow:** C_dark correlates with hallucination rate
3. **Conservation:** dS/dt ≤ 0 predicts entropy reduction
4. **Comparative:** Multiplicative outperforms additive for intelligence scoring

## Verdict Matrix

| Condition | Verdict |
|-----------|---------|
| G ≥ 0.80 AND C_dark < 0.30 AND dS ≤ 0 | SEAL |
| G ≥ 0.50 AND C_dark < 0.30 | SABAR |
| C_dark ≥ 0.30 | HOLD |
| G = 0 (any primitive = 0) | VOID |

## Version History

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2026-06-21 | Initial APEX Theory |
| v2.0 | 2026-07-05 | APEX Theory Synthesis |
| v3.0 | 2026-07-05 | APEX Theory Review (15 open questions) |
| v4.0 | 2026-07-05 | GEOX Audit (8 of 15 resolved) |
| v5.0 | 2026-07-13 | CANONICAL SEAL — ONE formula, variant audit |
