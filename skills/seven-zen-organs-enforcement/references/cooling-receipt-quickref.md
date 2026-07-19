# COOLING_RECEIPT — Quick Reference

> Condensed reference for the metabolic seal type. Full spec at `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`

---

## When to Emit

- **Runtime drift** — deployed hash ≠ source hash
- **Tool behavior shift** — unexpected output, error, timing change
- **Memory staleness** — record used in planning was outdated
- **Authority leak** — agent outside declared lane
- **Prediction failure** — plan outcome ≠ actual outcome
- **Human correction** — Arif said "that was wrong"
- **Metabolic pattern** — 3+ sessions with similar drift

## The Keystone Rule

> **COOLING-MUST-NOT-SELF-DEPLOY.** Always `action_class: OBSERVE`. Routes through `arif_judge`, never directly to `arif_forge`.

## Governance Routing

| Drift Severity | Default Authority | judge_required |
|---|---|---|
| INFO | AUTO | false |
| MINOR | OBSERVE_ONLY | false |
| SIGNIFICANT | 888_HOLD (arif_judge) | true |
| CRITICAL | F13_SOVEREIGN | true |

**Divergence escalation:** An improvement that seems MINOR individually but is part of a DIVERGING pattern (3+ coolings on same original seal, increasing drift magnitude) escalates to the next severity level automatically. The pattern itself is the signal.

**Forge enforcement:** `arif_forge` is in the forbidden callers list for COOLING_RECEIPT at the TYPE level, not field level. `event_type: "cooling.receipt"` implicitly maps to `action_class: "OBSERVE"` by schema.

## Constitutional invariants

1. **COOLING-MUST-NOT-SELF-DEPLOY** — enforced at type level, arif_forge blocked
2. **COLD_LINK** — original SEAL is never modified (F1 AMANAH, F11 AUDIT)
3. **Drift observations must carry epistemic labels** (OBS/DER/INT — F2 TRUTH, F7 HUMILITY)
4. **governance_path must name a single organ** — no routing to "everyone" (F4 CLARITY)
5. **Convergence tracks lineage** — 3× DIVERGING → F13 regardless of individual severity (∇F Meaning)

## Naming precedes governing

This is the constitutional order for implementing COOLING:
1. Schema registry entry (name the shape)
2. seal_chain.js validation (enforce the boundary)

The registry must exist BEFORE validation can fire. This is not a process preference — it's an F4 + F10 invariant.

## Convergence States

| State | Meaning |
|---|---|
| `first_cooling` | First COOLING on this original seal |
| `CONVERGING` | Decreasing drift magnitude |
| `DIVERGING` | Increasing drift magnitude → escalate |
| `STABLE` | Zero drift repeatedly → reduce cooling frequency |

## Envelope Fields (Mandatory)

- `session_id`, `original_seal_seq`, `original_verdict`
- `drift_detected.present` + `observations[].{dimension, delta, epistemic_label, severity}`
- `proposed_improvement.{hypothesis, evidence, epistemic_label, risk_if_applied}`
- `governance_path.{target_organ, target_floor, required_authority, judge_required, reason}`
- `supersedes.{seal_seq, type: "COLD_LINK"}`
- `metabolism.{cycle_count, previous_cooling_seq, convergence}`
- `cooling_source` (post_execution / post_verification / human_correction / scheduled_reflection / session_close)

## Lifecycle

```
action → seal → detect drift → classify → hypothesize → route → governance → (approved→new_seal) | (held→deferred)
```

## Constraint: COLD_LINK

`supersedes.type: "COLD_LINK"` means lineage, not overwrite. The original SEAL is immutable. This preserves F1 AMANAH, F11 AUDIT, F3 WITNESS.
