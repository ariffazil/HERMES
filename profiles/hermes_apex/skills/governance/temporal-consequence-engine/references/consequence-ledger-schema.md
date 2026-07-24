# consequence_ledger.jsonl — Schema Reference

Append-only, locked. Every invocation of `hermes_temporal_consequence` writes one line.

## Entry Schema

```json
{
  "ts": "2026-07-13T10:30:00Z",
  "action_id": "abc123",
  "action_kind": "deploy|seal|policy|toolchange|other",
  "request": {
    "context_snapshot_hash": "sha256:...",
    "horizons": { "short_hours": 4, "medium_hours": 48, "long_hours": 720 }
  },
  "dials": {
    "tau": { "short": 4, "medium": 48, "long": 720 },
    "lambda": 0.85,
    "kappa": { "pattern": "steady|burst|drift|offline", "interval_avg_ms": 12000 },
    "alpha": { "detected": false, "kind": null, "score": 0.0 },
    "deltaS_t": { "short": -0.02, "medium": -0.01, "long": 0.005 }
  },
  "risk": {
    "immediate": { "score": 0.1, "vectors": [] },
    "delayed": { "score": 0.05, "vectors": [] },
    "compounding": { "score": 0.02, "vectors": [] },
    "cascading": { "score": 0.01, "vectors": [] }
  },
  "trajectories": {
    "act_now": { "entropy_delta": -0.02, "anomaly_risk": 0.01 },
    "dont_act": { "entropy_delta": 0.01, "anomaly_risk": 0.05 },
    "alternative_count": 1
  },
  "tags": {
    "live": ["well_vitality", "port_health"],
    "cached": ["seal_chain_last_24h"],
    "inferred": ["forecast_mean", "anomaly_score"]
  },
  "floor_flags": {
    "F1_reversible": true,
    "F2_grounded": true,
    "F4_entropy_ok": true,
    "F11_in_lease": true,
    "F13_sovereign_input": false
  },
  "authority": "L5a_VERIFY",
  "forecaster": "simple|statsmodels|timesfm",
  "duration_ms": 45
}
```

## Field Rules

| Field | Rule |
|-------|------|
| `ts` | ISO 8601 UTC. Server-side clock, not client-supplied. |
| `action_id` | Stable hash of the proposed action. Deterministic for same input. |
| `action_kind` | Enum. `"other"` for anything not in the list. |
| `request.context_snapshot_hash` | SHA256 of the LIVE+CACHED state at decision time. Proves what was known. |
| `request.horizons` | Always in hours. Short ≤ 24h, Medium ≤ 168h, Long ≤ 720h. |
| `dials.tau` | Hours per horizon level. Must match request.horizons. |
| `dials.lambda` | 0.0–1.0. Higher = faster decay. Default 0.85. |
| `dials.kappa.pattern` | Detected cadence pattern. |
| `dials.alpha.detected` | Boolean. If true, kind must be non-null. |
| `dials.deltaS_t` | Per-horizon entropy delta. Negative = clarity increase. |
| `risk.*` | 0.0–1.0 per propagation type. Vectors are string labels. |
| `trajectories.*` | Summary only. Full state_path not stored in ledger (too large). |
| `tags.*` | Lists of signal names in each category. Proves classification. |
| `floor_flags` | Boolean per floor. All true = clean. Any false = flag for JUDGE. |
| `authority` | Always `"L5a_VERIFY"`. Never `"L5b_JUDGE"`. |
| `forecaster` | Which backend was used. For audit trail of model quality. |
| `duration_ms` | Pipeline execution time. For performance monitoring. |

## Floor Flag Rules

| Flag | Meaning | When false |
|------|---------|------------|
| `F1_reversible` | Action is reversible or backed up | JUDGE must review |
| `F2_grounded` | Forecasts based on real series, not hallucinated | Report is invalid |
| `F4_entropy_ok` | ΔS_t not consistently positive | Action increases entropy |
| `F11_in_lease` | Action within actor's lease scope | Action unauthorized |
| `F13_sovereign_input` | Sovereign ack required | Must not proceed |

## Query Patterns

```bash
# Last 10 entries
tail -10 /var/arifos/consequence_ledger.jsonl | jq .

# All entries with high cascading risk
cat /var/arifos/consequence_ledger.jsonl | jq 'select(.risk.cascading.score > 0.5)'

# All entries where F13 flagged
cat /var/arifos/consequence_ledger.jsonl | jq 'select(.floor_flags.F13_sovereign_input == true)'

# Entries by action kind
cat /var/arifos/consequence_ledger.jsonl | jq 'select(.action_kind == "deploy")'

# Entropy trend (ΔS_t over time)
cat /var/arifos/consequence_ledger.jsonl | jq '{ts: .ts, dS: .dials.deltaS_t}'
```

## Integrity

- File: `/var/arifos/consequence_ledger.jsonl`
- Permissions: `644` (read by all, write by engine only)
- Rotation: None. Append-only forever.
- Backup: Included in VAULT999 backup cycle.
- Verification: `sha256sum` of file at each session start.
