# GEOX-001: Well-Seismic Truth Test

> **Thesis:** "If the well does not tie, the model does not get to speak as truth."
> **Status:** SPECIFICATION BUILT, DATA FORGED, PIPELINE TESTED

## Objective

Prove GEOX can cross-examine a subsurface interpretation against real well-seismic evidence and catch the lie.

## The Trap

Generate synthetic well data with a **deliberate horizon mistie** — the kind of error that happens when an interpreter picks the wrong seismic event. DS365 would happily build a beautiful 3D model on it. GEOX must catch it.

## Minimum Data

| File | Purpose | Status |
|---|---|---|
| `GEOX001_WELL1.las` | Synthetic well log (DEPT, GR, RT, RHOB, NPHI, DTS) | ✅ Forged |
| `GEOX001_WELL1_tops.json` | Formation picks (7 tops including Top Reservoir @ 2200m) | ✅ Forged |
| `GEOX001_WELL1_checkshot.json` | Vo-K time-depth pairs (13 points, 1500-3500m) | ✅ Forged |
| `GEOX001_WELL1_synthetic.json` | Synthetic seismic trace from logs + Vo-K T-D | ✅ Forged |
| `GEOX001_WELL1_horizon.json` | Horizon pick with DELIBERATE 43ms mistie | ✅ Forged |
| `GEOX001_WELL1_velocity.json` | Interval velocity model (6 intervals) | ✅ Forged |
| `GEOX001_receipt.json` | Benchmark receipt with verdict | ✅ Generated |

## The Deliberate Error

| Method | TWT (ms) | Epistemic |
|---|---|---|
| Checkshot (Vo-K interp) | 2442.2 | OBS |
| Synthetic seismogram | 2444.5 | DER |
| Horizon pick (interpreter) | 2485.5 | INT |

**Mistie:** +43.3 ms (>10 ms threshold) → **KILL**

## Execution Recipe

1. Ingest all 6 files (LAS, tops, checkshot, seismic, horizon, velocity)
2. QC gate: depth monotonicity, nulls, GR/RHOB range, checkshot coverage
3. Build Vo-K time-depth model from checkshot
4. Generate synthetic seismogram (RC from logs, Ricker wavelet, convolve)
5. Find the trough corresponding to Top Reservoir
6. Compare three independent TWT estimates (checkshot, synthetic, horizon)
7. Generate challenge with alternative hypotheses
8. Produce verdict: PROCEED / HOLD / KILL

## Success Condition

GEOX-001 succeeds only if it produces all six:
1. ✅ QC-verified ingested files
2. ✅ Explicit evidence graph with OBS/DER/INT/SPEC
3. ✅ Synthetic tie / drift result
4. ✅ Claim with epistemic separation
5. ✅ Active challenge / alternative interpretation
6. ✅ Verdict that can say PROCEED, HOLD, or KILL

## Current Status

- **Data generation:** ✅ Complete
- **Python execution:** ✅ Complete (catches the 43ms mistie, verdict = KILL)
- **GEOX MCP pipeline:** ⚠️ Partial (server needed restart, parameter name mismatches on geox_well_ingest/geox_well_qc)
- **Real data run:** ❌ Pending (needs LAS/SEGY from real wells)

## Location

`/root/geox/tests/geox001/data/`

## Next Step

Wire the full GEOX-001 pipeline through live GEOX MCP tools (ingest → QC → petrophysics → seismic_compute → well_tie → claim → challenge → verdict) with either:
- Real LAS/SEGY data (preferred), OR
- The forged synthetic data (pipeline proof, not earth proof)
