# Biometric Signal Map — WELL Sensor Fields

> **Purpose:** Complete specification of biometric sensor fields WELL expects for a meaningful H_WELL readiness assessment. When WELL reports "no_biometric_data" or "substrate_only readiness=0.30", these are the fields that are missing.

## Sovereign Self-Report Fields (Operator-Provided)

| Field | Type | Scale | Purpose | Example |
|-------|------|-------|---------|---------|
| `sleep_hours` | float | 0-12 | Hours slept last night | 7.0 |
| `sleep_quality_score` | float | 0-10 | Subjective sleep quality | 8.5 |
| `sleep_debt_days` | float | 0-14+ | Accumulated sleep deprivation days | 0.5 |
| `cognitive_clarity` | float | 0-10 | Mental clarity / focus | 7.0 |
| `decision_fatigue` | float | 0-5 | Decision fatigue level (lower=better) | 1.2 |
| `stress_load` | float | 0-10 | Subjective stress level | 4.0 |
| `pain_level` | float | 0-10 | Current pain/discomfort | 1.0 |
| `energy_level` | float | 0-10 | Self-rated energy | 6.0 |
| `duty_load` | float | 0-10 | Perceived task burden | 5.0 |
| `emotional_state` | string | — | Current emotion descriptor | "neutral", "calm", "tired" |
| `hrv_status` | string | — | Heart rate variability regime | "normal", "elevated", "depressed" |
| `chronic_fatigue` | bool | — | Flag if fatigue is chronic/debilitating | false |
| `restlessness` | float | 0-10 | Agitation / inability to settle | 0.0 |
| `chronic_elevation_days` | int | 0-30+ | Consecutive days of elevated stress | 0 |

## arifOS Thermodynamic Biometrics (Sovereign)

These are the core biometric fields referenced in the MCP tool biometric block (all null = no sovereign data injected):

| Field | Type | Scale | Purpose | Example |
|-------|------|-------|---------|---------|
| `peace2` | float | 0-1 | Inner peace / calm measure | 0.7 |
| `delta_s` | float | -1 to 1 | Entropy delta (negative=order, positive=chaos) | -0.05 |
| `kappa_r` | float | 0-1 | Resilience coefficient | 0.6 |
| `rasa` | string | — | Emotional tenor | "ok", "calm", "fatigued" |
| `amanah` | float | 0-1 | Trust/integrity measure | 0.8 |
| `clarity` | float | 0-10 | Cognitive clarity (same as cognitive_clarity) | 7.0 |

## Behavioral Telemetry Fields (Auto-Generated)

The `well_auto_keepalive.py` script generates these as LOW-confidence substitutes when sovereign data is missing:

| Field | Source | Confidence | Notes |
|-------|--------|------------|-------|
| `circadian` | machine_human_substrate | LOW | Inferred from system clock ("WAKING" / "SLEEPING") |
| `sleeping` | machine_human_substrate | LOW | Boolean from circadian inference |
| `substrate_only readiness` | machine_human_substrate | LOW | Computed from non-biometric signals, typically 0.30 |

## MCP Tool Output: Where to Find Biometric Gaps

When using WELL MCP tools for diagnosis, check the following locations for null/missing biometric fields:

### well_validate_vitality (readiness mode)
```
observation.readiness_envelope.biometric
  - peace2: null
  - delta_s: null
  - kappa_r: null
  - rasa: null
  - clarity: null
  - sleep_hours: null

observation.vitality_gate.H_WELL.evidence
  → "no_biometric_data; substrate_only readiness=0.30"

observation._memory
  - class: "CACHED_MEMORY"
  - last_verified: timestamp
  - is_fresh: false   ← stale because no new data to update with
```

### well_assess_reliability (health mode)
```
observation.layer_3_domain_truth
  - has_telemetry: false
  - truth_status: "INSUFFICIENT_DATA"
  - freshness: "fresh" (state files are fresh, but content is empty of biometrics)
```

### well_assess_homeostasis (fatigue mode)
```
Biometric override fields are passed as parameters to the tool:
  - sleep_hours, cognitive_clarity, decision_fatigue
  - stress_load, hrv_status, emotional_state
  - chronic_fatigue, accumulated_session_fatigue
```

## Injection Interface

### Via script (VPS-local)
```bash
/root/WELL/scripts/biometric_inject.sh --non-interactive \
  --delta-s 0.3 --peace2 0.7 --kappa-r 0.6 --amanah 0.8 --rasa "ok"
```

### Via state.json direct write
```json
{
  "timestamp": "2026-07-28T00:00:00+00:00",
  "operator_id": "arif",
  "metrics": {
    "sleep": {"last_night_hours": 7.0, "sleep_debt_days": 0.0, "quality_score": 8.5},
    "cognitive": {"clarity": 6.0, "decision_fatigue": 1.2},
    "stress": {"subjective_load": 4.0, "restlessness": 0.0, "chronic_elevation_days": 0},
    "metabolic": {"perceived_stability": 6.0, "hydration_status": "OK"},
    "structural": {"pain_level": 0.0, "sedentary_hours_continuous": 0.0}
  },
  "daily_input": {"energy_level": 6.0, "hours_slept": 7.0, "duty_load": 5.0, "stress_level": 4.0, "pain_level": 0.0},
  "environment": "PROD",
  "source_type": "OPERATOR_REPORTED"
}
```

### Via well_assess_homeostasis (MCP tool)
```
well_assess_homeostasis(
  mode="fatigue",
  sleep_hours=7.0,
  cognitive_clarity=6.0,
  decision_fatigue=1.2,
  stress_load=4.0,
  hrv_status="normal",
  emotional_state="neutral",
  chronic_fatigue=false
)
```

## Freshness Decay Timeline

| Elapsed | Status | Readiness Quality | Confidence |
|---------|--------|-------------------|------------|
| < 1h | FRESH | Full | HIGH |
| 1-4h | FRESH (ageing) | Diminishing | MODERATE |
| 4-24h | STALE | Reduced | LOW |
| 24-168h | EXPIRED | Minimal | VERY LOW |
| > 168h | EXPIRED_CEILING | Zero (awaiting inject) | NONE |

Beyond 168h (7 days) with no sovereign injection, WELL enters `biometric_state_expired_168h_ceiling` and the MCP tool cached memory becomes `is_fresh: false`.
