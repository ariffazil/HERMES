# Unified arifFlow Spec v1 — Reference Summary

**Date:** 2026-07-25
**Structure:** Rust (execution substrate) → Python (governance conduit) → TypeScript (governance wrapper)

## Three-Layer Rule

- **Rust** = compute — scheduler, channel, merkle, topology merge. Never judges.
- **Python** = conduit — stdin/stdout bridge, arif_judge FFI, VAULT999 seal, Kabarkan emit.
- **TypeScript** = surface — build plan, enforce floors, display traces. Never schedules.

## Rust Gaps Closed (3 gaps, ~2 days)

1. **Barrier timeout policy** — `BarrierConfig` struct with `condition(ALL|MAJORITY|N_OF_M)`, `timeout_ms`, `policy_on_timeout(HoldAll|ContinueMajority|CancelAll)`. Integrated into `step()`.
2. **Lane cooling queue** — `CoolingManager` in `src/governance/cooling.rs`. `check_lane()` → `record_execution()` → `tick()`. Auto-cooling after `max_executions_before_cooling`.
3. **F1 per-lane reversibility** — `Reversibility::Reversible|Irreversible` in `FlowNode` trait. IRREVERSIBLE blocks at dispatch without 888 pre-approval. Approvals cleared on HOLD/VOID.

## Test Count: 44+ (was 24)

- 5 barrier timeout, 4 cooling, 3 F1 per-lane, 8 misc additions from original 24

## E2E Test: 7/7 passing

`/root/A-FORGE/domain/orchestration/test_ariflow_e2e.sh`
Tests: configure→seed→step→need_verdict, verdict→step_result, multiple steps, HOLD, AFQ field, stop→cooling

## Architecture

```
AAA TypeScript (build plan, enforce floors)
    → JSON-L topology
    → Python adapter (spawn Rust, pipe stdin/stdout, call arif_judge)
    → Rust binary (execute super-steps)
    → stdout envelopes
    → Python adapter (seal VAULT999, emit Kabarkan)
    → AAA (update state, display traces)
```

## Key Integration Points

- `forge_parallel` → becomes BSP plan wrapper (not A2A spawn)
- `DAG executor` → each DAG depth = 1 super-step
- `PipelineCoordinator` → pipeline phases = sequential super-steps
- `ConvergenceEngine` → merge strategy evaluator
- `FloorEnforcer` → F1 per-lane check
- `Kabarkan` → new span types: super_step, lane_spawn, barrier, merge
- `VAULT999` → new receipt types: SUPER_STEP, MERGE_WITNESS, LANE_BREACH, COOLING_METABOLIC

## Location Reference

| Component | Path |
|-----------|------|
| Rust core | `/root/arifFlow/` — compiled binary at `target/release/ariflow` |
| Python adapter | `/root/A-FORGE/domain/orchestration/ariflow_adapter.py` |
| TS wrappers | `/root/AAA/src/ariflow/` — `ariflow.ts` + `ariflow_client.ts` |
| E2E test | `/root/A-FORGE/domain/orchestration/test_ariflow_e2e.sh` |
| Flow state | `/root/AAA/state/flow_state.json` |
