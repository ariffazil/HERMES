## AKAL Kernel Diagnostic — 2026-07-11

Live audit of arifOS kernel against all five cognitive invariants.

### Test Setup
- Session: `SEAL-4b547b309d2b4508` (OBSERVE_ONLY, actor_verified=False)
- Provider: MiniMax-M3 (for arif_critique)
- Kernel epoch: 2026-07-03

### Results

| # | Invariant | Status | Evidence |
|---|---|---|---|
| I1 | Friction | PARTIAL | `arif_think` runs 2-step reasoning (inductive→deductive) with `transition_candidates` (3 branches) and `uncertainty_chain`. No explicit friction scoring — escalation is confidence-threshold based. |
| I2 | Shadow | PARTIAL | `arif_critique(mode=shadow)` exists but hit `llm_schema_violation` — MiniMax-M3 returned empty reasoning/answer. Scaffolding present, content generation broken. |
| I3 | Novelty | MISSING | No source-vs-synthesis splitting, novelty scoring, or regurgitation detection. |
| I4 | Dual Eval | EXISTS | `arif_judge` correctly enforced `888_HOLD` — blocked due to LOW authority, not SOVEREIGN. L5a/L5b split architecturally present. |
| I5 | Latency | PARTIAL | `transition_candidates` (3 branches) and `confidence_trajectory` exist organically. No mandatory cooling time, no two-pass minimum, no blast-radius gating. |

### Score: 1 EXISTS, 3 PARTIAL, 1 MISSING

### Key Kernel Structures Found
- `reasoning_trace` with steps, confidence trajectories, axiom citations
- `transition_candidates` — multiple paths before converging
- `uncertainty_chain` — confidence change tracking
- `anomalous_contrast` — deviation detection
- `metacognition` block with confidence_band, assumptions, failure_modes
- `constitutional_check` with floor_passed, hold_required, agency_level
- `nine_signal` with delta/psi/omega planes

### Fixes Applied
1. `arifosmcp/core/akal.py` — 735 lines, all five invariants (already existed)
2. `arifosmcp/core/akal_wiring.py` — thin hooks wiring AKAL into organs
3. Verified all five hooks end-to-end

### Irreversible Action Test Result
```
I1 friction=low (simple query) — HIGH would force deep pipeline
I2 shadow valid, no violations
I3 novelty PASS (1/2 chunks synthesized)
I4 requires_sovereign=True for irreversible
I5 cooling=300s, branching=True, second_look=True, immediate=False
```
