---
name: apex-verification-pipeline
description: >
  APEX Verification Pipeline — runtime computation of G = A·P·E·X·Φ
  with measurement laws for each primitive. Canonical formula, one
  implementation, seven axioms enforced. Falsifiable at execution time.
triggers:
  - "apex compute"
  - "G score"
  - "apex verification"
  - "apex gate"
  - "forge_evaluate"
  - "governance score"
version: "1.0.0"
sealed: "2026-07-13"
sovereign: "ARIF (F13)"
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

### Φ — Witness
Φ = ∛(H · AI · Ext)
- H = human witness (WELL vitality, dignity, somatic signals)
- AI = internal witness (arifOS judge, floors, lineage)
- Ext = external witness (AAA, civilizational mesh)
- If any witness = 0 → Φ = 0

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

- `references/apex-axiom-proofs-and-variant-mapping.md` — full axiom proofs, 4-variant mapping, A=Authority rationale, measurement laws, gate layer separation
- `references/market-prediction-application.md` — APEX applied to market prediction: primitive→market mapping, CLARITY/CHAOS/STABLE states, verdict matrix, volume integration, real XAUUSD example

## Deprecation

- V1 (A×P×X×E²) — DEPRECATED (missing Φ, E² inflation)
- V2 (A·P·E·X·Φ) — CANONICAL SEALED
- V3 ((1-h) embedded) — DEPRECATED (humility is gate, not primitive)
- V4 (H×√(S×U)×E²) — DEPRECATED PERMANENTLY (6-primitive hybrid)
