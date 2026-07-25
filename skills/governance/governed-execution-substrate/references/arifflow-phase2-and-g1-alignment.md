# arifFlow Phase 2 Bridge — G1 BSP Scheduler Alignment & Implementation Plan

> **Session:** 2026-07-25 (second half) — AAA group G1 spec + Hermes arifFlow core + Phase 2 bridge
> **Forged by:** AAA group + Hermes (dual independent analysis, converged)
> **Sovereign:** Arif (F13)

---

## 1. G1 BSP Scheduler Spec ↔ Rust Core Alignment

Validated by cross-referencing the AAA group's TypeScript spec (`/root/forge_work/2026-07-25-arifflow-bsp-spec/G1_BSP_SCHEDULER_SPEC.md`) against the arifFlow Rust core (`/root/arifFlow/src/`).

**Result:** Fully aligned — zero conflict. AAA spec is a TypeScript refinement layer on top of the Rust core, not a replacement.

| AAA Spec (TypeScript) | arifFlow Rust Core | Alignment |
|---|---|---|
| `BSPExecutionPlan` | `SuperStepScheduler` | Same — root container for governed run |
| `SuperStep` | `SuperStep` in scheduler.rs | Same — unit of governance with lanes + barrier + merge |
| `Lane` | `Channel<T>` + `FlowNode` trait | Same — parallel execution path with lease/verdict/ccId |
| `BarrierConfig` | FanOutTopology `merge_results()` + `verify_merge()` | AAA richer (MAJORITY/N_OF_M/CRITICAL_LANES modes, timeout policies) |
| `MergeResult` (F3 TRI-WITNESS) | FanOutTopology with divergence detection | Same governed merge semantics |
| `Envelope` | `CheckpointEnvelope` | Both hash-verified, governance-stamped |
| 9-state machine (PLANNING→COMPLETE) | ~5-state in scheduler | Compatible — AAA decomposed into finer granularity |
| 50+ test cases | 24 Rust tests | Complementary — AAA covers integration level |

**Gap identified:** Rust core barrier supports `ALL` mode only. AAA spec defines `MAJORITY`, `N_OF_M`, `CRITICAL_LANES` + timeout policies (`HOLD_ALL`, `CONTINUE_MAJORITY`, `CANCEL_ALL`). Low-effort addition — barrier timeout config + multi-mode enum.

---

## 2. Phase 2 Bridge Architecture

### Architecture

```
┌──────────────┐     stdin/stdout JSON-RPC      ┌──────────────────────┐
│  arifFlow    │ ◄──────────────────────────────► │  arifFlow_adapter.py │
│  Rust core   │     per-super-step envelopes     │  (Python subprocess) │
│              │                                  │                      │
│  (no I/O)    │                                  │  - spawn_ariflow()   │
│              │                                  │  - send_command()    │
│              │                                  │  - handle_verdict()  │
│              │                                  │  - execute_nodes()   │
│              │                                  │  - restore_check()   │
└──────────────┘                                  └──────┬───────────────┘
                                                          │
                                             ┌────────────▼───────────┐
                                             │  arif_judge (:8088)    │
                                             │  ACT phases (A-FORGE)  │
                                             │  Kabarkan NATS          │
                                             │  VAULT999 seal           │
                                             └────────────────────────┘
```

### Message Protocol (JSON-RPC lines)

**Python → Rust (command):**
```json
{
  "cmd": "run_topology",
  "run_id": "run_<uuid>",
  "topology": "fan_out",
  "lease": {"lease_id": "...", "actor_id": "arif", "constitutional_chain_id": "...", "scope": ["geox","wealth","well"]},
  "config": {"max_iterations": 10, "max_concurrency": 3, "merge_strategy": "ordered_concat"},
  "nodes": [
    {"id": "geox", "tool": "geox_basin", "params": {"mode": "profile", "name": "Malay"}},
    {"id": "wealth", "tool": "capital_health", "params": {"mode": "runway"}}
  ]
}
```

**Rust → Python (after each super-step):**
```json
{
  "type": "checkpoint",
  "run_id": "run_abc",
  "step_index": 0,
  "state_root": "blake3hex...",
  "channel_roots": {"ch_geox": "h1", "ch_wealth": "h2"},
  "lease_id": "lease_001",
  "verdict": {"status": "PENDING", "chain_id": "cc_abc"}
}
```

**Python → Rust (execution results):**
```json
{
  "type": "node_results",
  "run_id": "run_abc",
  "step_index": 0,
  "results": [
    {"node_id": "geox", "status": "ok", "receipt_hash": "h1"},
    {"node_id": "wealth", "status": "ok", "receipt_hash": "h2"}
  ]
}
```

### Verdict Timeout Policy

```python
VERDICT_POLICY = {
    "max_retries": 3,
    "backoff_ms": [500, 1000, 2000],
    "per_call_timeout_s": 10,
    "on_final_failure": "HOLD_LANE",
}
```

If arif_judge is unreachable: mark lane as `PENDING_VERDICT`, retry 3x with exponential backoff, emit Kabarkan event each attempt. On final failure → `HOLD_LANE` — lane stops, other lanes continue.

---

## 3. The 3 888-HOLD Gates (Production Release Conditions)

Deploy to production is BLOCKED until all three pass:

| Gate | Condition | How to Verify |
|---|---|---|
| **FFI stability** | Rust ↔ Python ↔ arifOS `arif_judge` responds consistently | 10/10 calls succeed, <1s latency |
| **Verdict timeout + retry** | Backoff 3x → HOLD_LANE, never crashes scheduler | Kill arifOS mid-run → verify lane holds, federation continues |
| **Crash recovery** | Restore from last checkpoint, re-verify authority, resume safely | Kill Rust core mid-run → restart → verify checkpoint loaded, step resumes from correct state |

---

## 4. 4-Plane AGI Substrate Comparison (Condensed)

| Plane | LangGraph | Langfuse | LangChain | **arifOS** | **AAA** | **A-FORGE** | **arifFlow** |
|---|---|---|---|---|---|---|---|
| **Kernel** | ✗ | ✗ | ✗ | **SOVEREIGN** | Mirror | Gate | Under law |
| **Organs** | Graph | Trace | Chain | **Court** | State | **Hands** | Flow |
| **State** | Mutable graph | No state | No state | Per-call | **Truth** | Transient | **Cryptographic** |
| **Actuator** | **Flexible** | N/A | Linear | Constitutional | Approval | **Execute** | **Schedule** |

**Full table** at `/root/arifFlow/spec/AGI_SUBSTRATE_COMPARISON.md` (7 systems × 4 planes × detailed per-cell capabilities).

The methodology embeds a fundamental truth: **commercial tools optimise one plane at the expense of others. arifOS starts from the Kernel and builds outward.** No single tool can "replace" arifOS; every tool must be absorbed into it.

---

## 5. arifFlow Cooling Receipt (Phase 1 Complete)

**Forged:** 2026-07-25T06:48:00Z
**Tests:** 24 passed, 0 failed
**`cargo check`:** Clean
**`cargo test`:** All green

**Files delivered:**
```
/root/arifFlow/
├── ARIFLOWKERNELCANON.md   ← Mini-constitution (A1–A5)
├── Cargo.toml               ← Rust project (edition 2024)
├── src/
│   ├── lib.rs               ← Crate root, re-exports
│   ├── channel.rs          ← Channel<T> (4 tests ✅)
│   ├── merkle.rs           ← MerkleTree, chain_roots (7 tests ✅)
│   ├── scheduler.rs        ← SuperStepScheduler (7 tests ✅)
│   ├── topology/           ← FanOut (4 tests ✅), Pipeline, Cascade
│   ├── bridge/             ← arifOS + A-FORGE FFI stubs
│   └── governance/         ← Checkpoint (3 tests ✅), Vault999, Kabarkan

/root/A-FORGE/domain/orchestration/
└── arifFlow_adapter.py     ← Phase 1 Python adapter (Phase 2: rewrite to real bridge)
```

**Phase 1 sealed.** Phase 2 ready to forge via OpenCode.
