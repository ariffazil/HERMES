---
name: apex-verification-pipeline
description: >
  APEX Verification Pipeline — runtime computation of G = A·P·E·X·Φ
  with measurement laws for each primitive. Canonical formula, one
  implementation, seven axioms enforced. Falsifiable at execution time.
triggers:
  - "apex compute"
  - "apex intelligence"
  - "G score"
  - "G-score"
  - "apex verification"
  - "apex gate"
  - "forge_evaluate"
  - "governance score"
  - "F8 GENIUS"
  - "apex G"
  - "G-fold"
  - "G fold"
  - "universal vital sign"
  - "pre-action gate"
  - "G flow"
  - "G flow doctrine"
  - "how G propagates"
  - "organ G source"
  - "live G probe"
  - "G stale stub"
version: "1.0.0"
sealed: "2026-07-13"
sovereign: "ARIF (F13)"
tags:
  - G-fold
  - APEX
  - F8 GENIUS
  - multimodal
  - tri-witness
  - constitutional
related_skills:
  - delta-omega-psi-multimodal-cognition
  - tri-witness-specification
---

# APEX Verification Pipeline

## The Canonical Formula (SEALED)

```
G_raw  = A · P · E · X · Φ
C_dark = A · (1-P) · (1-X)
dS/dt  ≤ 0
```

## Primitive Measurement Laws

### A — Authority
A = (valid_leases / total_leases) · (floor_compliance / 13)
- valid_leases = active, non-expired, non-revoked execution leases
- floor_compliance = number of floors F1–F13 satisfied
- If any floor violated → A = 0
- If F13 sovereign override → A = 1 for that action only

### P — Physics
P = w_well · P_well + w_seis · P_seis + w_geo · P_geo
- P_well = 0.99 (observed, somatic, irreversible)
- P_seis = 0.50 (interpreted, reversible)
- P_geo = 0.70 (model-derived, reversible)
- If well contradicts seismic → P = P_well

### E — Evidence
E = (clarity / (1 + uncertainty)) · reversibility
- clarity = signal-to-noise ratio normalized to [0,1]
- uncertainty = Ω₀ band (min 0.03)
- reversibility = 1 if Merkle chain intact, 0 if broken

### X — Execution
X = (successful_steps / total_steps) · consequence_stability
- consequence_stability = exp(-|ΔS_t|)
- If ΔS_t > threshold → X = 0
- If forge_evaluate fails → X = 0

### Φ — Witness (Tri-Witness Gate)
Φ = ∛(H · AI · Ext)
- H = human witness (WELL vitality, dignity, somatic signals)
- AI = internal witness (arifOS judge, floors, lineage)
- Ext = external witness (GEOX/WEALTH/AAA, civilizational mesh)
- If any witness = 0 → Φ = 0 (any missing witness collapses the gate)
- Minimum thresholds: H ≥ 0.42, AI ≥ 0.32, Ext ≥ 0.26
- Full measurement laws per witness: see skill `tri-witness-specification`
- GENESIS/056: Tri-Witness Specification — modality maps, conflict protocol, edge cases

## Verdict Matrix

| Condition | Verdict |
|-----------|---------|
| G ≥ 0.80 AND C_dark < 0.30 AND dS ≤ 0 | SEAL |
| G ≥ 0.50 AND C_dark < 0.30 | SABAR |
| C_dark ≥ 0.30 | HOLD |
| G = 0 (any primitive = 0) | VOID |

## Seven Axioms

1. **Multiplicativity** — zero in any primitive collapses G
2. **Five-sufficient** — three pairs + one witness = minimal complete
3. **Nash bargaining** — G = ∏ p_i because veto = multiplicative gate
4. **Shadow** — C_dark = A·(1-P)·(1-X) < 0.30
5. **Conservation** — dS/dt ≤ 0
6. **Tri-witness** — Φ = ∛(H·AI·Ext) ≥ 0.70
7. **F13 veto** — only sovereign overrides G

## Implementation

```python
# arifosmcp/runtime/apex_canonical.py
# 35 tests: tests/runtime/test_apex_canonical.py
```

## Reference Files

- `references/live-measurement-methodology.md` — **Live G-score computation from apex_metrics.db.** Governance-verdict classification (critical: failure codes include HOLD/SEAL/SABAR/VOID which are NOT errors), primitive derivation from `success/has_evidence/within_lease` columns, the P bottleneck diagnosis, trend bucketing, charting, and the two computation path warning (`apex_primitives.py` deprecated — counts governance verdicts as failures → G ≈ 0.10 instead of 0.71).
- `references/apex-axiom-proofs-and-variant-mapping.md` — full axiom proofs, 4-variant mapping, A=Authority rationale, measurement laws, gate layer separation
- `references/market-prediction-application.md` — APEX applied to market prediction: primitive→market mapping, CLARITY/CHAOS/STABLE states, verdict matrix, volume integration, real XAUUSD example
- `references/g-fold-flow-doctrine.md` — **G-fold as the federation's universal vital sign.** Crystallised flow doctrine (2026-07-25): circulatory path (contributors → kernel → consumers), nine-signal translation, compass property, organ-level G access, delta table (current vs doctrine). If you need to understand G as a federation-wide signal rather than a single computation, start here.
- `references/g-fold-organ-consumption-pattern.md` — **How any organ fetches and consumes live G from the kernel.** Implementation template, C-class threshold matrix, graceful degradation rules, verification checklist. WELL is the first production deployment (2026-07-26). If you need to wire G-fold into an organ's pre-action gate, start here.

## Related Doctrine

- **Skill `delta-omega-psi-multimodal-cognition`** — Δ·Ω·Ψ multimodal cognition doctrine: how multimodal perception becomes cognition through constitutional metabolism. Every modality → G primitive. GENESIS/054.
- **Skill `tri-witness-specification`** — Full measurement laws for H/AI/Ext witnesses: modality maps, conflict resolution, edge cases, nine-signal integration. GENESIS/056.
- **GENESIS/054**: `/root/arifOS/GENESIS/054_DELTA_OMEGA_PSI_MULTIMODAL_COGNITION.md`
- **GENESIS/056**: `/root/arifOS/GENESIS/056_TRI_WITNESS_SPECIFICATION.md`

- **Note:** The Jacobian Cognition Kernel (forged 2026-07-25 at `/root/A-FORGE/src/domain/cognition/`) computes G = (A·P·X·E²)·(1-h) from task execution state. This is the **deprecated V1 formula** (missing Φ, E² inflation). The two G values serve different planes (operational efficiency vs constitutional permission) but the formula gap should be tracked. See `governed-execution-substrate/references/jacobian-cognition-kernel-2026-07-25.md`.

## Deprecation

- V1 (A×P×X×E²) — DEPRECATED (missing Φ, E² inflation)
- V2 (A·P·E·X·Φ) — CANONICAL SEALED
- V3 ((1-h) embedded) — DEPRECATED (humility is gate, not primitive)
- V4 (H×√(S×U)×E²) — DEPRECATED PERMANENTLY (6-primitive hybrid)
