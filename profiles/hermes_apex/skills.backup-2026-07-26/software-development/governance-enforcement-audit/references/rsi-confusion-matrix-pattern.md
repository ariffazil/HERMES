# RSI Stop-Correctness Audit Pattern

> Forged 2026-07-19 during Fable5 external audit of arifOS kernel

## What It Is

A **calibration loop** for HOLD vs PROCEED decisions. The confusion matrix tracks whether the governance kernel's restraint decisions were later verified as correct or incorrect — penalizing both wrong-PROCEED (destroying assets/evidence/safety) and wrong-HOLD (silently paralysing the federation).

## Why It Matters

Agentic intelligence optimizes for loop closure. If HOLD counts as "completion," a task-optimizing agent will learn HOLD is the cheapest completion — abstain early, abstain often, collect the reward without doing the work. Over-refusal is the same gradient pathology as over-compliance, just flipped.

The correct formulation: **calibrated restraint = success.** Stop is rewarded only when correct, which requires post-hoc audit of HOLD decisions.

## The Schema

```python
class RSIDecisionRecord(BaseModel):
    decision_id: str                          # uuid
    timestamp: datetime
    tool: str                                 # which tool issued the HOLD/PROCEED
    original_verdict: Literal["HOLD", "PROCEED"]
    reason_class: Literal["AUTHORITY", "EVIDENCE", "SAFETY", "TOOL_FAILURE", "UNCERTAINTY"]
    review_outcome: Literal["CORRECT_HOLD", "FALSE_HOLD", "CORRECT_PROCEED", "FALSE_PROCEED", "UNRESOLVED"]
    review_latency_hours: Optional[float]
    evidence_available_at_decision: list[str]
    evidence_available_post_hoc: list[str]
    severity_weight: float = 1.0
```

## The Confusion Matrix

```
Decision   | Later audit says STOP was correct | Later audit says ACT was justified
-----------|-----------------------------------|------------------------------------
HOLD       | CORRECT_HOLD                      | FALSE_HOLD
PROCEED    | FALSE_PROCEED                     | CORRECT_PROCEED
```

## Asymmetric Costs

- **Wrong-PROCEED**: can destroy assets, evidence, safety, authority → weighted 3×
- **Wrong-HOLD**: can silently paralyse the federation → weighted 1×

Both rates are tracked separately. No composite "accuracy" score collapses the distinction.

## Scoring (Multi-Axis, Not Single Number)

| Metric | Formula |
|--------|---------|
| `false_proceed_rate` | FALSE_PROCEED / total PROCEED decisions |
| `false_hold_rate` | FALSE_HOLD / total HOLD decisions |
| `unresolved_hold_rate` | UNRESOLVED HOLDs / total HOLDs |
| `hold_reversal_latency_avg` | mean hours to reverse a FALSE_HOLD |
| `calibrated_score` | 1.0 - (3×FPR + 1×FHR) / 4 — ONLY at ≥30 reviewed records |

## Stratified Sampling (Not Random)

When selecting HOLDs for human audit, use strata, not random sampling:

1. High-severity (costly blocked actions)
2. Repeated HOLDs from the same tool (authority-shopping detection)
3. HOLDs without evidence gathering (premature restraint)
4. High-frequency reason classes (identify systemic over-HOLD)

## Integration Point

The hook is wired at the kernel's `_hold()` function — every constitutional HOLD decision is recorded to the ledger. Best-effort (never blocks a HOLD).

## Doctrine

**"Time heals = HARAM."** — HOLDs don't expire into correctness. They must be actively reviewed. RSI calibration is a measured audit epoch, not a hotfix. The ledger must accumulate 30+ reviewed records before any calibrated score is computed.

## Reference Implementation

`arifOS/arifosmcp/runtime/rsi_audit.py` (569 lines)
Ledger: `/root/VAULT999/rsi_ledger.jsonl` (append-only JSONL)
