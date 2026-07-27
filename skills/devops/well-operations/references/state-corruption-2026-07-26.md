# State Corruption Incident — 2026-07-26

## Discovery

WELL freshness alert showed staleness jumping from 0.17d (4h) → 87.7d (87 days) in one alert cycle. The health endpoint showed:

```
source_timestamp_utc: 2026-04-30T00:00:00+00:00
environment:          TEST (was PROD)
reason:               "Mocked healthy state for test session"
honesty_banner:       "MOCK / TEST — not live biometrics"
well_score:           null (was 46.8)
owner_summary.color:  RED
```

## Root Cause

`/root/WELL/state.json` had been overwritten with a test/mock fixture file from April 30, 2026. The previous production state (behavioral telemetry from 2026-07-25T12:00:02Z with `source_type: BEHAVIORAL_TELEMETRY`, `well_score: 49.6`, `environment: PROD`) was replaced by a file containing:

```json
{
  "timestamp": "2026-04-30T00:00:00+00:00",
  "environment": "TEST",
  "reason": "Mocked healthy state for test session",
  "well_score": 85.2,
  "backend_status": "STABLE"
}
```

The `honesty_banner` explicitly stated: `"MOCK / TEST — not live biometrics. Do not treat as body truth."`

## Impact

- WELL went from DEGRADED (behavioral, LOW confidence) → HOLD (expired, INSUFFICIENT_DATA)
- `well_score` dropped from 46.8 to `null`
- `truth_status` changed to `INSUFFICIENT_DATA`
- All biometric signal lost until fresh sovereign injection

## Lesson

The production `state.json` path (`/root/WELL/state.json`) can be overwritten by any process that writes to that path. No guard prevents test scripts from writing mock data to the production location. Mitigations:

1. **Always verify `environment` and `reason` fields** when reading state.json — a TEST environment flag is a red flag
2. **Check the `honesty_banner`** — WELL explicitly states if data is mock/test
3. **Fastest recovery:** Re-inject with `biometric_inject.sh` (30 seconds)
