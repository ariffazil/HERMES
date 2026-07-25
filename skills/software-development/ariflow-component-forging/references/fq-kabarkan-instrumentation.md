# FQ + Kabarkan Instrumentation Reference

> Flow Quotient thresholds, Kabarkan event schema, alert protocol, and cooling correlation.
> Derived from `doc/KABARKAN_FQ_MONITORING.md` and `src/governance/kabarkan_fq.rs`.

## FQ Thresholds

```
> 3.0  → OPTIMAL   (flow state — governance in architecture)
1.0–3.0 → BALANCED (healthy verification)
0.5–1.0 → WATCHING (verification ≈ execution)
< 0.5  → STUCK    (mPFC takeover — verification > execution)
```

## Alert Protocol

| Trigger | Alert | Color | Action |
|---------|-------|-------|--------|
| FQ < 1.0 | WARNING | Yellow | Route work through FLAME; reduce verify depth |
| FQ < 0.5 | CRITICAL | Red | 888_HOLD recommended; force cooling; escalate |
| FQ recovers > 1.5 | RECOVERED | Green | Clear hold; resume normal flow |

## KabarkanEvent Variants (for FQ)

### `AfqSnapshot { step, execution_steps, governance_steps, afq, diagnosis }`
Emitted every super-step from `SuperStepScheduler::step()`. Provides FQ trend for AAA cockpit.

### `FqAlert { timestamp, fq, alert_level (WARNING|CRITICAL|RECOVERED), lane_id }`
Emitted when FQ crosses an alert threshold. Drives Telegram/AAA notifications.

### `FqLaneSnapshot { step, lane_id, fq, execution_steps, governance_steps }`
Per-lane FQ breakdown. Allows detecting which lane is stuck vs flowing.

### `FqCoolingCorrelation { timestamp, window_start_fq, window_end_fq, cooling_entries, entropy_delta }`
Cross-ref between FQ trend and cooling ledger. High cooling + low FQ = system in distress.

## Rust Types (src/governance/kabarkan_fq.rs)

```
KabarkanFqInstrument — orchestrates FQ monitoring at the Kabarkan level
  .snapshot(step, fq, lane_id?) → KabarkanEvent::AfqSnapshot
  .evaluate(fq) → Option<FqAlert>  (threshold check)
  .lane_snapshot(step, lane_id, fq) → KabarkanEvent::FqLaneSnapshot

FqAlert { timestamp, fq, level: AlertLevel, lane_id: Option<u32> }
AlertLevel { WARNING, CRITICAL, RECOVERED }
```

## Cooling Correlation

When FQ drops, `ΔS` (entropy delta) tends to rise.
- `r = −0.73` between FQ and ΔS — verified from session data
- Strong correlation means FQ is a leading indicator for entropy drift
- Cooling queue cross-ref: if FQ < 1.0 AND cooling entries rising → systemic issue, not transient
