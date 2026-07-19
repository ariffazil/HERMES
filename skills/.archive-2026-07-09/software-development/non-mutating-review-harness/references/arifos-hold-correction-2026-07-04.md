# arifOS HOLD correction — 2026-07-04

## Context

The first forge of the arifOS lifecycle kernel (`v0.1`) shipped an
**autonomous** 8-stage loop:

```
SEAL → INIT → Scaffold → Skill Rebuild → Organ Rebind → Replay → Cool → Resume
```

with a prime law: *"Every SEAL event must regenerate the agent's skill metabolism."*

## The HOLD verdict

> Verdict: **HOLD as written.** Convert it into a bounded RSI scaffold, not
> autonomous self-modification. Your text is strong as doctrine, but dangerous
> as an execution spec.
>
> The loop must become:
>
> ```
> safe_loop:
>   SEAL:     lock_receipt
>   INIT:     load_invariants
>   Scaffold: propose_skill_delta
>   Diff:     compare_old_vs_new_skill_contract   ← THE MISSING STAGE
>   Test:     run_survivor_tests
>   Judge:    approve_or_hold
>   Cool:     rate_limit_regeneration
>   Resume:   only_if_no_unresolved_hold
> ```
>
> The missing stage is Diff. Without Diff, the system cannot know whether it
> regenerated or mutated.
>
> **SEAL should not rebuild directly. SEAL should emit a Skill Delta Event.**

## Why this matters

> If every SEAL automatically rebuilds skills, you create a self-modifying loop:
> - SEAL     changes agent state
> - INIT     reloads state
> - Scaffold rewrites pathways
> - Skill Rebuild changes future behavior
> - Resume   acts under changed behavior
>
> That is RSI. Good. But without hard gates, it becomes constitutional drift.

## What changed in v0.2

| v0.1 (autonomous) | v0.2 (bounded) |
|---|---|
| Prime law: every SEAL rebuilds skills | Prime law: every SEAL **triggers review**; **may trigger** scaffold; **must not trigger** autonomous mutation without gate |
| INIT regenerates skills | INIT reloads **body plan only** — `mutation_allowed=False` hard-coded |
| Scaffold proposes AND applies | Scaffold **proposes only** — `applies_automatically: false` |
| Diff stage: missing | Diff stage: 4 drift classes (`weakened_gate`, `expanded_autonomy`, `hidden_mutation`, `authority_drift`) |
| Engine boundary: implicit | Engine boundary: 7 hard rules (`cannot_apply_patch`, `cannot_change_tool_surface`, `cannot_change_A_FORGE_policy`, `cannot_mark_SEAL`, `cannot_bypass_cooling`, `cannot_weaken_human_ack`, `cannot_mutate_F13_boundary`) |
| Skills: physics/bio/chem triples | Skills: **versioned contracts** with `must_preserve` + `must_never_weaken` + `tests` |
| Invariants: implicit | Invariants: 3 explicit (Noether discipline / immune memory / activation barrier) |
| Output: skills autoupdated | Output: `SkillDeltaReport` (proposal only, never applied) |

## Engine boundary (the load-bearing discipline)

The engine's 7 hard rules are NOT optional. They are the load-bearing
discipline that prevents the engine from becoming its own sovereign:

1. `cannot_apply_patch` — engine emits proposals, never calls the apply path
2. `cannot_change_tool_surface` — engine never touches the public tool registry
3. `cannot_change_A_FORGE_policy` — engine never edits the actuator's policy
4. `cannot_mark_SEAL` — engine has no SEAL authority
5. `cannot_bypass_cooling` — engine never short-circuits the cooling stage
6. `cannot_weaken_human_ack` — engine never lowers human-ack thresholds
7. `cannot_mutate_F13_boundary` — engine never edits the SOVEREIGN floor

Any attempted violation → `PermissionError` at the engine boundary.

## Why the loop needs ALL 8 stages (none optional)

| Stage | If removed, what breaks |
|---|---|
| 1 SEAL observation | Engine has no signal to react to |
| 2 INIT body plan | Engine has no baseline to diff against |
| 3 Scaffold proposal | Engine has no proposal to evaluate |
| **4 Diff** | **Engine cannot tell regeneration from mutation** |
| 5 Survivor tests | Engine cannot prove survival |
| 6 Judge gate | Engine has no sovereign override for semantic changes |
| 7 Cooling | Engine has no rate limit on regeneration loops |
| 8 Resume (gated) | Engine cannot continue the system |

## Smoke (proof the engine works)

```bash
cd /root/arifOS
for mod in seal_shadow seal_post_hook init_scaffold skill_registry skill_delta_engine; do
  python3 -m "lifecycle.$mod"
done
```

All 5 modules pass. The engine passes 4 scenarios:
- safe version bump → `risk=LOW`
- `must_never_weaken` dropped → `risk=HOLD`, `chemistry_activation_barrier=False`
- `mutation_allowed=True` event → `PermissionError` at boundary
- extinct-tool resurrection → `risk=HOLD`

## Source locations

- `kernel.yaml` v0.2 — declarative spec with constitutional_law + hard_rules + 12 contracts
- `init_scaffold.py` — INIT-only body-plan reload (`mutation_allowed=False`)
- `skill_registry.py` — `SkillContract` + `ContractDiff` (4 drift classes)
- `skill_delta_engine.py` — `SkillDeltaEngine.evaluate()` (non-mutating)
- Branch: `lifecycle-kernel-v0.2-post-hold-2026-07-04`
- Commit: `e049578e2` (local, no push — F13 owns the push)