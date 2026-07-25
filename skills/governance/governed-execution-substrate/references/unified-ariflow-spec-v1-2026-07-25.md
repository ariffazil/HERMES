# Unified Spec v1 — arifFlow
## Rust (substrate) → Python (conduit) → TypeScript (wrapper)

**Forged:** 2026-07-25 | **Context:** G1 BSP Scheduler forge readiness
**Session:** Arif corrected a TypeScript-only AAA G1 spec when a compiled Rust core with 24 tests already existed at `/root/arifFlow/target/release/ariflow`

---

## Architecture

```
AAA TypeScript (governance surface)
    ↓ JSON-L topology via adapter
Python adapter (governance conduit)
    ↓ stdin/stdout JSON-RPC
Rust arifFlow (execution substrate)
```

## Rust Core (existing — 24 tests, compiled)

| Module | Key types | Tests |
|--------|-----------|-------|
| `channel.rs` | `Channel<T>`, `Message<T>`, `ChannelMode::{Bounded,Unbounded}` | 4 |
| `merkle.rs` | `MerkleTree`, `MerkleRoot`, `content_hash()`, `chain_roots()` | 7 |
| `scheduler.rs` | `SuperStepScheduler`, `CheckpointEnvelope`, `VerdictClass`, `TopologyKind` | 5 |
| `topology/fan_out.rs` | `FanOutTopology`, `MergeStrategy::{OrderedConcat,MerkleRoot}` | 4 |
| `topology/pipeline.rs` | Pipeline topology | — |
| `topology/cascade.rs` | `CascadeTopology`, `CascadeStep`, `CascadeConfig` | 0 |
| `bridge/arifos_governance.rs` | `ArifOSGovernanceBridge`, `extern "C" FFI` | — |
| `bridge/aforge_executor.rs` | `AForgeExecutorBridge`, `ExecutionRequest` | — |
| `governance/kabarkan.rs` | `KabarkanTracer`, 5 event types | — |
| `governance/vault999.rs` | `Vault999Sealer`, `SealReceipt` | — |
| `governance/checkpoint.rs` | `CheckpointManager`, `CheckpointState` | 3 |
| `lib.rs` | Re-exports + version | 1 |

## Rust Gaps (3 — ~2 days)

### G1: Barrier timeout policy
- Add `BarrierConfig` struct (condition: All/Majority/NOfM/CriticalLanes, timeout_ms, policy: HoldAll/ContinueMajority/CancelAll/ContinueCritical)
- Modify `step()` to accept optional `BarrierConfig`
- After execution, check completion count vs condition
- On timeout → apply policy
- 5 tests needed

### G2: Lane cooling queue
- New module `src/governance/cooling.rs`
- `CoolingManager` with `check_lane()`, `record_execution()`, `tick()`, `cooling_lanes()`
- Integration: scheduler calls `CoolingManager::check_lane()` before dispatch
- 4 tests needed

### G3: F1 per-lane reversibility
- Add `Reversibility` and `BlastRadius` enums to scheduler
- Add `reversibility()` and `blast_radius()` to `FlowNode` trait
- Block IRREVERSIBLE lanes without 888 verdict
- 3 tests needed

## Python Adapter (ariflow_adapter.py)

```
class AriflowAdapter:
  - start(topology, lease_id, actor_id, chain_id)
  - seed(channel, data)
  - step(nodes) → need_verdict | step_result
  - submit_verdict(class, verdict_id, hash)
  - stop() → cooling receipt
  - restore(checkpoint)
```

Pattern:
```
need_verdict → call arif_judge() via FFI
step_result  → seal to VAULT999
execution_held → emit Kabarkan event
stop()       → close forge lease
```

## TypeScript Wrappers (ariflow.ts)

Data models ONLY — no executor logic:
- `BSPExecutionPlan` — root container
- `SuperStep` — lanes + barrier + merge
- `Lane` — organ, tool, lease_id, verdict_id, ccId
- `BarrierConfig` — condition + timeout
- `Envelope` — cross-plane message
- `MergeResult` — TRI_WITNESS output

Governance enforcement (thin):
```
enforceFloorF1(lane) → HOLD if IRREVERSIBLE without verdict
enforceFloorF3(merge) → HOLD if divergence > 0.6
```

## Forge Order

1. Rust gaps (2 days): G3 → G1 → G2
2. Python adapter (1 day): spawn → pipe → verdict → seal
3. TypeScript wrappers (1 day): data models → client → governance
4. Integration (0.5 day): forge_parallel → BSP, PipelineCoordinator → BSP

**Total: ~4.5 days.** Not 10-15.

## Key lesson from this session

**Before writing any execution engine spec, probe for existing compiled implementations.** The AAA G1 spec proposed a TypeScript BSP scheduler from scratch. But `/root/arifFlow/target/release/ariflow` already existed with 24 tests. The correct architecture was:

- Rust stays as execution substrate
- Python adapter bridges governance
- TypeScript wraps as governance surface

One spec. Three layers. Zero confusion. ~2 days of gaps to fill, not 10-15 days of rewrite.