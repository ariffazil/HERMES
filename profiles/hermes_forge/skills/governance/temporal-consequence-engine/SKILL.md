---
name: temporal-consequence-engine
description: "Temporal Consequence Engine — implementation spec aligned with AAA architecture. Given a candidate action, compute temporal trajectories and risk surfaces across PAST-PRESENT-FUTURE, using constitutional logs + temporal forecasting, emit L5a VERIFY report (never a verdict). Companion to temporal-constitution skill."
version: 1.1
author: arif
tags: [temporal, consequence, engine, akal, apex, aaa, governance, timesfm]
---

# TEMPORAL CONSEQUENCE ENGINE — IMPLEMENTATION SPEC

Aligned with AAA architecture. Companion to `temporal-constitution` skill.

---

## 1. Purpose

Given a candidate action, compute temporal trajectories and risk surfaces across PAST-PRESENT-FUTURE, using constitutional logs + temporal forecasting, and emit a **L5a VERIFY report** (never a verdict).

**Single sentence:** Hermes computes trajectories, never judges them.

---

## 2. Core Interfaces

### Engine Entrypoint

```typescript
type TemporalConsequenceRequest = {
  action_id: string;              // stable id / hash of proposed action
  action_kind: "deploy" | "seal" | "policy" | "toolchange" | "cooling" | "well" | "wealth" | "arifos" | "other";
  context_snapshot: ContextState; // LIVE+CACHED state at decision time
  horizons: HorizonConfig;        // { short, medium, long } in hours/days — per-organ, see §9
};

type TemporalConsequenceReport = {
  action_id: string;
  trajectories: {
    act_now: Trajectory;
    dont_act: Trajectory;
    alternative: Trajectory[];
  };
  risk: RiskPropagationSummary;
  anomalies: TemporalAnomalySummary;
  entropy: EntropyTrajectorySummary;
  dials: TemporalDialSnapshot;    // τ, λ, κ, α, ΔS_t
  tags: { live: TagSet; cached: TagSet; inferred: TagSet };
  authority: "L5a_VERIFY";        // hard-coded, never L5b
};
```

---

## 3. Data Substrates

### Somatic (read-only, from WELL)

```typescript
type SomaticShadow = {
  vitality_score: number;
  fatigue_score: number;
  hrv: number;
  sleep_hours_24h: number;
  stress_index: number;
  timestamp: string;
};
```

**Source:** `well_validate_vitality`, `well_assess_homeostasis`, `well_health_check`
**Constraint:** REFLECT_ONLY. Never used to override or "optimize" the body.

### Constitutional (from ledgers)

```typescript
type SealEvent = { seq: number; t: string; actor: string; verdict: string; deltaS: number; };
type CoolingEvent = { t: string; kind: string; receipt_id: string; };
type ScarEvent = { t: string; cause: string; scope: string; };
```

**Source:** `arif_seal(mode=ledger)`, cooling ledger, scar ledger
**Constraint:** Append-only. No write paths from this engine.

### Computational (temporal forecasting)

```typescript
type TimeSeries = { t: number[]; y: number[]; label: string; };
type TimesForecast = {
  horizon: number[];                    // future steps
  mean: number[];
  quantiles: Record<string, number[]>;  // { "0.1": [], "0.5": [], "0.9": [] }
};
```

**Source:** TimesFM or equivalent temporal forecaster (pluggable interface)
**Constraint:** All forecasts tagged INFERRED, never presented as LIVE.

---

## 4. Temporal Dials

```typescript
type TemporalDialSnapshot = {
  tau: { short: number; medium: number; long: number }; // hours/days
  lambda: number;                                       // decay rate
  kappa: CadenceProfile;                                // burst/drip/offline
  alpha: AnomalyProfile;                                // drift/spike/gap
  deltaS_t: EntropyProfile;                             // ΔS over horizons
};
```

---

## 5. Pipeline (Internal Steps)

### Step 0 — Classify Inputs

| Tag | Source | Examples |
|-----|--------|----------|
| LIVE | Real-time probes | Current WELL shadow, active ports, latest health checks |
| CACHED | Recent logs | Last N hours of seals, cooling, forge logs |
| INFERRED | Model output | TimesFM forecasts, anomaly scores |

**Rule:** Never confuse INFERRED with LIVE.

### Step 1 — Build Base Time Series Per Organ

| Organ | Series | y-axis |
|-------|--------|--------|
| arifOS | seal timestamps | ΔS, cadence |
| arifOS | cooling timestamps | interval_length |
| A-FORGE | deploy/build timestamps | duration, incidents |
| WEALTH | capital events | risk, NPV |
| WELL | vitality timestamps | readiness score |
| GEOX | observation timestamps | confidence |

### Step 2 — Call Temporal Forecaster

For each relevant series:

- `forecast(series, horizon)` → mean trajectory
- `quantile(series, horizon, q)` → uncertainty bands
- `anomaly(series)` → anomaly scores over past + projected
- `time_to_event(series, target_state)` → time-to-event estimate

**Interface:** `TemporalForecaster` — pluggable backend (TimesFM, statsmodels, or simple exponential smoothing as fallback).

### Step 3 — Construct Trajectories

```typescript
type Trajectory = {
  horizon: { short: number; medium: number; long: number };
  state_path: StatePoint[];      // projected states over time
  cadence: CadenceProfile;
  anomalies: AnomalyProfile;
  entropy: EntropyProfile;
};
```

- **act_now:** Inject action into series (new seal, deploy) and re-forecast.
- **dont_act:** Forecast continuation of current regime.
- **alternative:** Forecast with different action parameters (delay, smaller scope).

### Step 4 — Risk Propagation

```typescript
type RiskPropagationSummary = {
  immediate: RiskVector;
  delayed: RiskVector;
  compounding: RiskVector;
  cascading: RiskVector;
};
```

Derived from:
- Quantile spread widening
- Anomaly likelihood increase
- ΔS_t slope sign and magnitude
- Cadence instability (κ)

### Step 5 — Entropy Trajectory

Compute ΔS over horizons:

- **ΔS_short** — near-term seals/cooling
- **ΔS_medium** — governance rhythm
- **ΔS_long** — structural trends (tool proliferation, scar accumulation)

### Step 6 — Safety Gate (Floors)

Before emitting report, check:

| Floor | Check | Action |
|-------|-------|--------|
| F1 | Reversibility | Mark if trajectory crosses irreversible boundary |
| F2 | Grounding | Ensure forecasts based on real series, not hallucinated |
| F4 | Entropy | Flag if ΔS_t > 0 consistently |
| F11 | Authority | Ensure action within actor's lease |
| F13 | Sovereignty | Mark if sovereign input required |

**No blocking.** Blocking is done by JUDGE, not Hermes. Only flags.

### Step 7 — Emit L5a VERIFY Report

Populate `TemporalConsequenceReport` with:
- Trajectories A/B/C
- Risk summary
- Anomaly summary
- Entropy summary
- Dial snapshot
- LIVE/CACHED/INFERRED tags

**No verdict, no "should/should not".** Only "if X then Y".

---

## 6. Safety Invariants

1. **No judgment** — Engine never outputs normative language; only descriptive/probabilistic.
2. **Somatic read-only** — WELL data never used to override or "optimize" the body; only to flag readiness.
3. **Past immutable** — No write paths to constitutional logs; only append via separate organs.
4. **Dial transparency** — Every forecast must carry explicit τ, λ, κ, α, ΔS_t.
5. **Tagging** — Every datum and every statement tagged LIVE/CACHED/INFERRED.

---

## 7. AAA Alignment

### MCP Tool

```
hermes_temporal_consequence(action_id, action_kind, context, horizons)
→ TemporalConsequenceReport
```

Single tool. No side effects except logs.

### Integration Points

| AAA Component | Integration |
|---------------|-------------|
| arifOS kernel | Reads seal chain, cooling ledger, scar ledger |
| WELL | Reads somatic shadow (read-only) |
| A-FORGE | Reads deploy/build logs |
| WEALTH | Reads capital event logs |
| GEOX | Reads observation logs |
| 888 JUDGE | Consumes report for verdict (separate step) |
| VAULT999 | Consequence ledger (append-only) |

### Consequence Ledger

Every invocation logged to `consequence_ledger.jsonl`:
```json
{
  "ts": "2026-07-13T10:30:00Z",
  "action_id": "abc123",
  "action_kind": "deploy",
  "dials": { "tau": {...}, "lambda": 0.8, "kappa": {...}, "alpha": {...}, "deltaS_t": {...} },
  "risk": { "immediate": {...}, "delayed": {...}, "compounding": {...}, "cascading": {...} },
  "authority": "L5a_VERIFY"
}
```

Append-only. Locked. For future scar and audit.

### TimesFM Pluggability

```typescript
interface TemporalForecaster {
  forecast(series: TimeSeries, horizon: number): TimesForecast;
  anomaly(series: TimeSeries): AnomalyScore[];
  timeToEvent(series: TimeSeries, target: number): number;
}
```

Implementations:
- **TimesFM** (when available) — foundation model for time series
- **Statsmodels** (fallback) — exponential smoothing, ARIMA
- **Simple** (minimal) — moving average + linear extrapolation

Start with Simple. Upgrade to TimesFM when ready.

---

## 8. Buildability Assessment

| Component | Status | Notes |
|-----------|--------|-------|
| Constitutional logs | LIVE | Seal chain, cooling ledger exist |
| WELL somatic shadow | LIVE | `well_validate_vitality` exists |
| Time series builder | LIVE | Reads seal chain → TimeSeries |
| Temporal forecaster | LIVE (Simple) | Moving average + linear extrapolation. StatsModels/TimesFM pluggable. |
| Trajectory constructor | LIVE | Forecaster + state injection |
| Risk propagation | LIVE | Quantile spread + ΔS slope |
| Entropy trajectory | LIVE | ΔS over horizons from seal chain |
| Safety gate | LIVE | Per-organ floor checks on report |
| Consequence ledger | LIVE | Append-only JSONL at /var/arifos/consequence_ledger.jsonl |
| MCP tool | BUILDABLE | Single tool wrapping pipeline |

**Bottom line:** Core engine is LIVE with Simple forecaster. Per-organ thresholds calibrated from first run (2026-07-13). TimesFM upgrade is the next milestone.

---

## 9. Per-Organ Thresholds (from first engine run 2026-07-13)

F4 and F13 thresholds are organ-relative, not absolute. Different organs have different entropy profiles.

| Organ | F4 threshold | F13 threshold | Rationale |
|-------|--------------|---------------|-----------|
| deploy | 0.50 | 0.30 | High-activity, reversible |
| seal | 0.45 | 0.10 | Constitutional, irreversible |
| cooling | 0.25 | 0.50 | Calmest organ, tightest F4 |
| well | 0.80 | 0.20 | Data sparsity expected |
| wealth | 0.90 | 0.40 | Wide ΔS range |
| arifos | 0.55 | 0.30 | Governance, moderate |

**Pattern:** F4 threshold should be calibrated to the organ's observed ΔS range. Cooling at 0.19 is fine (under 0.25). Deploy at 0.42 might be fine too (under 0.50). The threshold catches genuine entropy spikes, not normal operation.

**Tuning method:** Run engine across all organs, observe ΔS ranges, set F4 threshold at 1.2× the observed max for each organ. Review after 10 runs.

---

## 10. Pitfalls (from first implementation)

### Seal Chain Format Quirks
- **Mixed entry types**: Some legacy seal chain entries are plain strings, not dicts. Always check `isinstance(entry, dict)` before processing.
- **Field names**: Seal chain uses `epoch` (not `timestamp`) and `actor` (not `actor_id`).
- **No stored ΔS**: The seal chain does not store deltaS directly. Infer from verdict: `SEAL → -0.01` (entropy decreases), `HOLD → +0.01` (entropy increases), `VOID → 0.0`.
- **Entry count**: As of 2026-07-13, the chain has ~167 entries, ~37 of which are dict-type. The rest are legacy strings.

### Floor Flag Semantics
- **Convention**: `True = compliant (no flag)`, `False = flag/warning`.
- **F13 inversion**: "sovereign_ack" means "sovereign input NOT needed" when True. When False, sovereign input IS needed. This is the opposite of what the name suggests — the flag means "ack received/not needed" not "ack required".

### Cadence Interpretation
- `burst` pattern with avg ~1.5h intervals is normal for active development sessions.
- `drift` or `offline` patterns warrant investigation.
- `steady` pattern indicates healthy governance rhythm.

---

## 10. The Single Sentence

> The Temporal Consequence Engine is the machine that turns the Temporal Constitution into operational reality — it computes trajectories, never judges them, and gives 888 JUDGE the horizon it needs to decide.
