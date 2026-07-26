---
name: governance-feedback-loops
description: "Implement ECHO/PaW-style prediction-observation feedback loops in constitutional governance systems — closing the loop between verdict predictions and observed reality."
version: 1.0.0
author: Hermes Agent
---

# Governance Feedback Loops

Implement the ECHO/PaW pattern (from Cameron Wolfe's "Agentic World Models" survey) in constitutional agent governance systems. The core insight: **observation tokens that standard RL throws away are the cheapest, densest source of training signal.** In a governance context, this becomes: the delta between what the judge predicted and what reality produced is a learning gradient.

## When to Use

- Implementing a new constitutional feedback primitive in arifOS
- Adding prediction-observation scoring to any governance pipeline
- Closing a loop where a system makes predictions that can later be verified against reality
- User describes a "prediction → reality → gap" pattern that needs hardening

## The Four-Component Architecture

Every governance feedback loop MUST have all four components. A write path without a read path is an audit trail, not a learning system.

### 1. Write Path (Predicted State)
Embed a `predicted_state` snapshot in every consequential action's seal/persist payload. The prediction captures what the system **expects** reality to look like at the time of the decision:
- Key system metrics (well_score, vitals, drift status)
- Constitutional state (floors_checked, floors_violated)
- Timestamp of prediction

### 2. Read Path (Gradient Injection)
Before the next forward pass, query past prediction deltas and inject them into the deliberation context. The historical error signal conditions the next verdict so the model calibrates its confidence. **Storing the delta is useless if the judge doesn't see it during the next pass.**

### 3. Circuit Breaker (Delta Threshold Interrupt)
Implement a divergence threshold (Δ_max). If the delta between prediction and observation exceeds this limit, block the feedback loop and escalate. **A hallucination is not a learning gradient** — it's an epistemic failure requiring sovereign override.
- Default Δ_max = 0.30 (30% deviation)
- Trigger: `aggregate_score < (1.0 - Δ_max)`
- Response: HOLD + escalate to 888_JUDGE, do NOT silently log

### 4. Schema Parity (Strict Key Mapping)
Prediction keys and observation keys MUST use identical deterministic names. No semantic translation layers (`memory_usage` → `mem_util_pct`). If schemas diverge, raise SCHEMA_DRIFT — do not compute garbage deltas silently.
- Define a canonical `PREDICTION_SCHEMA` and `OBSERVATION_SCHEMA`
- Use a `SCHEMA_BRIDGE` dict only as a fallback, not the default
- Validate parity before every delta computation

## Concrete Implementation Checklist

When implementing in arifOS (see `references/arifos-echo-paw-implementation.md` for the session-specific details):

- [ ] Extend seal payload with `predicted_state` field
- [ ] Add `score_prediction` mode to memory tool
- [ ] Implement structured delta computation (numeric, boolean, list, string types)
- [ ] Add aggregate score with exponential decay
- [ ] Wire post-seal auto-indexing hook
- [ ] Implement `_query_prediction_gradient()` for read path
- [ ] Inject gradient context into evidence before deliberation
- [ ] Add Δ_max threshold with HOLD escalation
- [ ] Define canonical schema keys (prediction + observation surfaces)
- [ ] Add `_validate_schema_parity()` with drift detection
- [ ] Write tests for the feedback loop
- [ ] Commit with conventional commit message

## Pitfalls

- **Write path without read path**: Storing deltas in L3 without injecting them into the next forward pass. The gradient exists but the model never sees it. The read path (`_query_prediction_gradient()`) must query arif_memory for past L2-tier prediction deltas and inject them into `_evidence["gradient_context"]` before the verdict deliberation.
- **No circuit breaker**: Logging large deltas as "learning gradients" instead of blocking them. A 70% divergence means the world model is broken — not "learning." The threshold is DELTA_MAX = 0.30 (forged 2026-07-21). Delta is computed as normalized absolute difference: `abs(pred - obs) / max(|pred|, |obs|, 0.001)`. Non-numeric values use binary match (0.0 same, 1.0 different). A single key breaching the threshold triggers F1/F2 HOLD_888.
- **Schema mismatch**: Prediction uses `"memory_usage"` but observation returns `"mem_util_pct"`. The delta path now requires semantic translation (ΔS > 0), which introduces hallucination risk. SCHEMA_DRIFT is a **hard exception**, not a soft warning — the `score_prediction` mode rejects unknown prediction keys before any delta computation. Keys must be a subset of `JUDGE_PREDICTION_SCHEMA`.
- **Interrupted subagent delegation**: If `opencode run` or `delegate_task` returns `[Orphan recovery: interrupted...]` twice for the same task, stop retrying. Implement directly with `patch()` / `write_file()` / `terminal()`. Direct patching is faster than waiting for a coding agent that keeps getting rate-limited. Proven 2026-07-21: two OpenCode attempts interrupted → direct patching completed all three loop-closure additions in one session.
- **Subagent self-reported "done"**: Subagents may report completion but miss the circuit breaker or schema parity enforcement. Always verify with `git diff --stat`, re-read the diff against the specification, and run imports/tests before accepting.
- **Uncommitted changes**: Subagents may leave changes in the working tree without committing. Check `git status` after completion. The arifOS surface-gate hook (`FORGE_SURFACE_GATE_STRICT=1`) runs on commit — it pins live MCP tools against surface-map declarations, catching phantom tool drift before push. If the surface gate fires red, fix the surface map or tool registration before retrying the commit.

## Verification

After implementation, verify the full loop:
1. Trigger a verdict that includes predicted_state
2. Wait for reality to diverge or converge
3. Call score_prediction against the seal entry
4. Confirm delta is computed, scored, and stored
5. Confirm gradient_context appears in next verdict's evidence
6. Force a large divergence and confirm circuit breaker triggers HOLD
7. Confirm schema parity validation catches key mismatches
