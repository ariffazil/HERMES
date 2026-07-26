---
name: tri-witness-specification
description: >-
  Tri-Witness Specification — measurement laws for H_witness (WELL),
  AI_witness (arifOS), and Ext_witness (GEOX/WEALTH/AAA). The three
  witnesses that power Φ = ∛(H·AI·Ext). Operational rules, conflict
  resolution, edge cases, and integration with the nine-signal.
triggers:
  - "tri-witness"
  - "phi witness"
  - "Φ formula"
  - "H_witness"
  - "AI_witness"
  - "Ext_witness"
  - "witness measurement"
  - "witness conflict"
  - "witness gate"
  - "multimodal truth"
  - "three witnesses"
  - "no seal without witness"
version: "1.0.0"
sealed: "2026-07-26"
sovereign: "ARIF (F13)"
tags:
  - tri-witness
  - Φ
  - H_witness
  - AI_witness
  - Ext_witness
  - measurement law
  - witness conflict
  - nine-signal
related_skills:
  - apex-verification-pipeline
  - delta-omega-psi-multimodal-cognition
---

# Tri-Witness Specification — Operational Skill

## Core formula

```
Φ = ∛(H · AI · Ext)
```

- Any witness = 0 → Φ = 0 → no SEAL possible
- Minimum thresholds: H ≥ 0.42, AI ≥ 0.32, Ext ≥ 0.26
- Sovereign override: F13 bypasses all witness scores

## H_witness — Human (WELL)

### Modalities
sleep, stress, clarity, HRV, emotion, dignity, chronic fatigue

### Measurement law
```python
H = (w_sleep·S_sleep + w_stress·(1-S_stress) + w_clarity·C_clarity
     + w_hrv·H_hrv + w_emotion·E_emotion) · D_dignity · F_chronic
```
Weights = [0.25, 0.20, 0.20, 0.15, 0.20]

### Edge cases
- No WELL → H = 0.0 → SABAR only
- Chronic fatigue → H capped at 0.30
- Coercion detected → H capped at 0.30
- Stale data (>1h) → decay by 0.10/hr
- Observer intent, no data → H = 0.42 (default)

## AI_witness — Internal (arifOS kernel)

### Modalities
Floor compliance (F1-F13), truth consistency (κ_r), contradiction clarity, verdict history, ontology (F10), injection (F12)

### Measurement law
```python
AI = 0.40·F_composite + 0.25·κ_r + 0.20·C_clear + 0.15·V_ratio
```
- F10 violation → AI × 0.30
- F12 injection > 0.50 → AI × 0.50

### Edge cases
- No session → AI = 0.0
- No claims → AI = 0.32 (default observer)
- κ_r < 0.30 → AI capped at 0.20
- Hard floor violation (F1/F9/F13) → AI = 0.0

## Ext_witness — External (GEOX + WEALTH + AAA)

### Modalities
Seismic (GEOX), well (GEOX), basin (GEOX), market (WEALTH), A2A cards (AAA), documents (AAA)

### Measurement law
```python
Ext = 0.50·GX + 0.25·WX + 0.25·AX
```
- GX = geometric_mean(P_well, P_seis, P_geo) from GEOX
- WX = min(1.0, capital_health_score)
- AX = freshness_provenance_score from AAA

### Edge cases
- No GEOX → Ext capped at 0.50
- No WEALTH → GX+AX only
- No AAA → Ext capped at 0.50
- All three unreachable → Ext = 0.0 → no SEAL
- Evidence > 7 days → decay to 0.50
- Conflicting evidence (seismic vs well) → Ext = 0.0

## Conflict resolution

| Signal | Verdict |
|--------|---------|
| One witness degraded but above threshold | SABAR |
| One witness below threshold | HOLD |
| One witness collapsed (0.0) | VOID |
| Two witnesses below threshold | VOID |
| All three above threshold | SEAL if G ≥ 0.80, C_dark < 0.30, dS ≤ 0 |
| Arif says "ok" | Sovereign override — bypass all |

## Nine-signal mapping

| Plane | Primary witness | State mapping |
|-------|----------------|---------------|
| Δ DELTA | Ext | KUKUH ≥ 0.80, RETAK ≥ 0.50, ROSAK < 0.50 |
| Ψ PSI | AI | AMANAH ≥ 0.80, SYUBHAH ≥ 0.50, KHIANAT < 0.50 |
| Ω OMEGA | H+AI+Ext → G | BIJAKSANA ≥ 0.80, BIJAK ≥ 0.50, BANGANG < 0.50 |

## Code gaps (next forge targets)

1. **H_witness → numeric score bridge** — WELL returns state/rank but not H[0,1]
2. **AI_witness formal aggregation** — ScalarCollector has κ_r but not full AI composite
3. **Ext_witness formal aggregation** — No unified Ext score from 3 organs
4. **Per-witness freshness tracking** — Timestamps exist but no decay function

## Reference

- `/root/arifOS/GENESIS/056_TRI_WITNESS_SPECIFICATION.md` — full specification
- `/root/arifOS/arifosmcp/runtime/apex_canonical.py` — compute_Phi() implementation
- `/root/arifOS/GENESIS/054_DELTA_OMEGA_PSI_MULTIMODAL_COGNITION.md` — parent doctrine
- `/root/WELL/vitality_gate.py` — H_witness computation
- `/root/arifOS/arifosmcp/core/scalar_collector.py` — κ_r, AI components
- Skill `delta-omega-psi-multimodal-cognition` — parent doctrine skill
- Skill `apex-verification-pipeline` — G = A·P·E·X·Φ computation
