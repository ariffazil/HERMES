# Per-Organ Horizon Policy & F4 Thresholds

Based on first engine run across all 6 organs (2026-07-13).

## Horizon Policy (τ)

| Organ | Short | Medium | Long | Rationale |
|-------|-------|--------|------|-----------|
| deploy | 4h | 48h | 7d | Operational cadence, fast feedback |
| seal | 1h | 24h | 7d | Constitutional, needs tight horizon |
| cooling | 1h | 12h | 3d | Rhythmic, predictable |
| well | 1d | 7d | 30d | Somatic, slow signals |
| wealth | 7d | 30d | 90d | Financial, long cycles |
| arifos | 1h | 12h | 3d | Governance, fast feedback |

## F4 Thresholds (ΔS_t)

Based on observed ΔS ranges from first run:

| Organ | ΔS observed | F4 threshold | Rationale |
|-------|-------------|--------------|-----------|
| deploy | 0.40–0.42 | 0.50 | High-activity organ, allow higher entropy |
| seal | 0.38–0.40 | 0.45 | Constitutional, slightly tighter |
| cooling | 0.09–0.19 | 0.25 | Calmest organ, tightest threshold |
| well | 0.55–1.00 | 0.80 | Data sparsity expected, allow higher |
| wealth | -1.00 to +1.00 | 0.90 | Wide range, most permissive |
| arifos | 0.45–0.47 | 0.55 | Governance, moderate |

## F13 Threshold (Cascading Risk)

| Organ | F13 threshold | Rationale |
|-------|---------------|-----------|
| deploy | 0.30 | Reversible, lower threshold OK |
| seal | 0.10 | Irreversible, very sensitive |
| cooling | 0.50 | Low risk, higher threshold |
| well | 0.20 | Somatic, sensitive |
| wealth | 0.40 | Financial, moderate |
| arifos | 0.30 | Governance, moderate |

## Implementation Notes

- F4 threshold is per-organ, not absolute
- F13 threshold is per-organ, based on reversibility and risk profile
- Thresholds are conservative — err on the side of flagging
- Review after 10 more runs to calibrate

## Source

First engine run: 2026-07-13T12:52:58Z
Ledger: /var/arifos/consequence_ledger.jsonl
Engine: temporal_consequence_engine.py (Simple forecaster)
