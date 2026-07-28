# arifFlow Engine Blueprint — Governed Parallel Execution Substrate

> **Session:** 2026-07-25 — LangGraph deconstruction → arifFlow forge  
> **Sovereign:** Arif (F13)  
> **Repo:** `/root/arifFlow/`  

## What Was Built

A full Rust crate implementing a governed parallel execution engine that replaces LangGraph's role under arifOS constitutional law.

**Trinity:** arifOS (law) · arifFlow (flow) · A-FORGE (hands)

## Architecture

```
/root/arifFlow/
├── ARIFLOWKERNELCANON.md   ← mini-constitution (A1-A5 invariants)
├── Cargo.toml
├── src/
│   ├── lib.rs              ← crate root, re-exports
│   ├── channel.rs          ← Channel<T> — content-hashed message passing
│   ├── merkle.rs           ← MerkleTree, content_hash, chain_roots
│   ├── scheduler.rs        ← SuperStepScheduler — Pregel-BSP with verdict oracle
│   ├── topology/
│   │   ├── mod.rs          ← TopologyError, NodeResult
│   │   ├── fan_out.rs      ← Parallel dispatch + verifiable merge
│   │   ├── pipeline.rs     ← Sequential stages with review
│   │   └── cascade.rs      ← Multi-agent handoff with F3 witness
│   ├── bridge/
│   │   ├── arifos_governance.rs  ← FFI: leases, verdicts, checkpoint validation
│   │   └── aforge_executor.rs    ← FFI: A-FORGE execution requests
│   └── governance/
│       ├── checkpoint.rs   ← CheckpointManager — write/restore/verify
│       ├── vault999.rs     ← Per-step sealing to VAULT999
│       └── kabarkan.rs     ← Observability events per super-step
```

## Key Invariants (A1-A5)

From `ARIFLOWKERNELCANON.md`:

| ID | Rule | Enforcement |
|----|------|-------------|
| A1 | Constitutional-first: no execution without lease + 888-JUDGE | `SuperStepScheduler` requires `lease_id`; returns `NoLease` error if nil |
| A2 | Plane-isolated: state crosses planes only via signed envelopes | Channels use content-hashed messages, verified on every read |
| A3 | Checkpoint-with-verdict: each step persists Merkle root + verdict | `CheckpointEnvelope` carries state_root + lease_id + verdict_id + chain_id |
| A4 | Verifiable-reduction: merge functions are deterministic + auditable | Fan-out merge deterministic; `verify_merge()` detects divergence |
| A5 | Metabolic-closure: every run ends with VAULT999 receipt, leases closed | Channels have close(); CheckpointManager tracks all steps |

## Methodology: Replacing a Commercial Framework

1. **Extract invariants** — What are the framework's core design decisions? (LangGraph: static graph, Pregel BSP, shared mutable state, node-boundary checkpoint)
2. **Identify blind spots** — What does it NOT enforce? (LangGraph: no identity, no governance, no epistemic discipline, no reversibility tracking, no witness)
3. **Map to constitutional floors** — Each blind spot maps to an arifOS invariant (F13 identity binding, F1 reversibility, F2 truth, F3 witness)
4. **Build from governance out** — Start with the constitution (A1-A5), then implement the runtime. Not the other way around.
5. **Plane-separate the architecture** — Rust core (pure state machine) + Python/TS gates (constitutional checks). Never mix scheduling with adjudication.
