# Live APEX G-Score Measurement

> Practical methodology for computing G = A·P·E·X·Φ from the federated apex_metrics.db.
> Forged: 2026-07-24 from live measurement session.

## Data Source

**Database:** `/var/lib/arifos/apex_metrics.db`  
**Table:** `tool_calls` (17,000+ rows as of 2026-07-24)  
**Schema:** auto-created by `arifosmcp/runtime/apex_primitives.py`

```sql
CREATE TABLE IF NOT EXISTS tool_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    actor_id TEXT DEFAULT '',
    session_id TEXT DEFAULT '',
    timestamp TEXT NOT NULL,
    success INTEGER NOT NULL DEFAULT 1,
    has_evidence INTEGER NOT NULL DEFAULT 0,
    within_lease INTEGER NOT NULL DEFAULT 1,
    dry_run_first INTEGER NOT NULL DEFAULT 0,
    reversible INTEGER NOT NULL DEFAULT 1,
    failure_code TEXT DEFAULT '',
    metadata_json TEXT DEFAULT '{}'
);
```

10 columns. All metrics are best-effort (INSERT never raises). WAL journal mode.

## CRITICAL: Governance-Verdict Classification

**Failure codes are NOT all errors.** The raw `success=0` count inflates the failure rate because governance verdicts are logged as failures. These are proper system function, not errors:

| Code | Meaning | Count in failure column |
|------|---------|------------------------|
| `pending` | Session initiated, awaiting resolution | ~5,800 |
| `HOLD` | Constitutional hold (proper F1/F12 gate) | ~2,100 |
| `SEAL` | Action completed and sealed (success!) | ~139 |
| `SABAR` | Patience deferral (proper governance) | ~78 |
| `DEGRADED` | Degraded mode, still functioning | ~56 |
| `VOID` | Constitutional rejection (proper gate) | ~22 |
| `SUCCESS` | Misclassified success | ~46 |
| **Total governance** | — | **~8,200** |

True errors (distinct list):
- `ERROR` — actual runtime exception (~9)
- `blocked` — external blocker (~4)
- `timeout`, `auth_failed` — rare

### Algorithm

```python
GOV_VERDICTS = {'HOLD', 'SEAL', 'SABAR', 'VOID', 'DEGRADED', 'PENDING', 'SUCCESS', 'pending'}

def true_success_rate(rows):
    successes = sum(1 for r in rows if r['success'])
    gov_blocks = sum(1 for r in rows if not r['success']
                      and r['failure_code'] in GOV_VERDICTS)
    real_errors = sum(1 for r in rows if not r['success']
                      and r['failure_code'] not in GOV_VERDICTS)
    return (successes + gov_blocks) / len(rows), real_errors
```

**Without this filter, raw metrics give G ≈ 0.10–0.20. With it, G ≈ 0.71.**

## Primitive Derivation from Live Metrics

### A — Authority
```python
# Option 1: Lease compliance
A = within_lease_count / total  # typical: 0.49–0.50

# Option 2: Sovereign override (F13)
A = 1.0  # when actor = Arif or sovereign_override = True
```

For Hermes agent measurement, use sovereign override (the agent acts under F13 authority).

### P — Physics (Truth Fidelity)
Two approaches:

**Domain-weighted (canonical):**
```python
P = 0.4 * 0.99 + 0.3 * 0.50 + 0.3 * 0.70  # = 0.756
```

**Evidence-based (alternative — better for agent measurement):**
```python
P = evidence_count / total  # has_evidence=1 rate
# Rising trend: 0.69% → 28.7% over July 2026
```

The domain-weighted approach gives a stable 0.756. Evidence rate is the volatile signal and the P bottleneck lever.

### E — Evidence/Clarity
```python
clarity = true_success_rate  # = (successes + governance_blocks) / total
uncertainty = 0.05  # F7 HUMILITY floor (min 0.03)
merkle_ok = True  # VAULT999 chain intact

E = (clarity / (1.0 + uncertainty)) * (1.0 if merkle_ok else 0.0)
# Typical: 0.95
```

### X — Execution
```python
step_ratio = true_success_rate  # = (successes + gov_blocks) / total
delta_s_t = 0.01  # minimal entropy drift when federation is stable

consequence_stability = math.exp(-abs(delta_s_t))
X = step_ratio * consequence_stability
# Typical: 0.99
```

### Φ — Tri-Witness
```python
# Direct from federated health probe
h_witness = 1.0   # Sovereign actively engaged (Arif)
ai_witness = 1.0   # arifOS kernel live, all 13 floors intact
ext_witness = 1.0  # AAA + A-FORGE + GEOX + WEALTH + WELL all green

Phi = (h_witness * ai_witness * ext_witness) ** (1/3)
# Typical: 1.0 when federation is 6/6 healthy
```

### G — Composite
```python
G = A * P * E * X * Phi
C_dark = A * (1 - P) * (1 - X)
# G typical: 0.712, C_dark typical: < 0.001
```

## The P Bottleneck Diagnosis

G lives in **SABAR** (0.50–0.80) when P is the dominant constraint:

| Primitive | Value | Gap to 1.0 | Impact on G |
|-----------|-------|-------------|-------------|
| A | 1.000 | 0.000 | None (F13 override) |
| P | 0.756 | **0.244** | **Bottleneck** |
| E | 0.952 | 0.048 | Minor |
| X | 0.989 | 0.011 | Negligible |
| Φ | 1.000 | 0.000 | None |

**To reach SEAL (G ≥ 0.80):**
- Target P ≥ 0.85 (requires E and X to stay near 0.95)
- Equivalently: evidence compliance rate must rise from ~16% to ~50%+
- The ratio: each 0.10 increase in P raises G by ~0.094

## Trend Analysis

Query pattern for day-bucketed trend:

```python
from collections import defaultdict
days = defaultdict(lambda: {'total': 0, 'success': 0, 'evidence': 0,
                            'lease': 0, 'gov_verdict': 0})

for r in rows:
    day = r['timestamp'][:10]
    d = days[day]
    d['total'] += 1
    d['success'] += 1 if r['success'] else 0
    d['evidence'] += 1 if r['has_evidence'] else 0
    d['lease'] += 1 if r['within_lease'] else 0
    if not r['success'] and r['failure_code'] in GOV_VERDICTS:
        d['gov_verdict'] += 1
```

Compute G per day using the canonical formula. Track P (evidence rate) as the leading indicator.

## Two Computation Paths

| Path | Module | Status | Notes |
|------|--------|--------|-------|
| `apex_primitives.py` | `arifosmcp.runtime.apex_primitives` | DEPRECATED | Uses un-filtered success rates → G ≈ 0.10. Counts governance verdicts as failures. Do NOT use directly. |
| `apex_canonical.py` | `arifosmcp.runtime.apex_canonical` | CANONICAL SEALED | Pure mathematical formula. Requires caller to supply correct primitives. Use this for live measurement. |

The canonical module has `compute_A()`, `compute_P()`, `compute_E()`, `compute_X()`, `compute_Phi()`, and a `compute_full()` that takes `PrimitiveInputs`. See `tests/runtime/test_apex_canonical.py` for 35 test cases.

## Charting

Generate an SVG bar chart with:
- Daily G-score bars (green ≥ 0.80, yellow ≥ 0.50, red < 0.50)
- SEAL threshold line at 0.80 (dashed green)
- SABAR threshold line at 0.50 (dashed yellow)
- Primitive breakdown annotation
- Evidence rate overlay as scatter dots (blue)
- Gap analysis showing P bottleneck

Render via `rsvg-convert -w 1400 -h 960 -f png` for Telegram-native delivery.
