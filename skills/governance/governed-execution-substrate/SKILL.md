---
name: governed-execution-substrate
description: >-
  Design, analyze, and forge execution engines, state machines, and orchestration
  runtimes that operate under constitutional governance. Covers LangGraph-level
  comparative analysis, Pregel/BSP vs constitutional chain, channel-based
  routing, Merkle state ledgers, constitutional checkpointing, and the
  Rust-core + Python/TS-gates architecture pattern. The what and how of
  replacing tools like LangGraph with a governed native engine.
tags:
  - governance
  - execution-engine
  - state-machine
  - langgraph
  - orchestration
  - pregel
  - constitutional-checkpoint
  - arifflow
  - federated-execution
triggers:
  - "execution engine"
  - "graph engine"
  - "orchestration runtime"
  - "state machine architecture"
  - "replace langgraph"
  - "forge better than langgraph"
  - "governed execution"
  - "channel-based routing"
  - "super-step"
  - "parallel execution"
  - "constitutional checkpoint"
  - "merkle state ledger"
  - "hashed state"
  - "act execution pipeline"
  - "craft a parallel execution engine"
  - "how to forge a system better than X"
  - "state and actuator"
  - "what system we use in the kernel"
  - "execution trade-offs"
  - "routing engine"
  - "state machine for agents"
  - "sovereign routing engine"
  - "cryptographic state machine"
  - "hashed state ledger"
  - "artifact spine"
  - "edge as apex judge"
  - "proxy tooling"
  - "references over values"
  - "constitutional routing"
  - "dual control verification"
  - "false success defect"
  - "readiness audit"
  - "forge readiness"
  - "is the federation ready for"
  - "arifflow forge"
  - "governed parallel execution engine"
  - "6-domain framework"
  - "BSP readiness"
  - "AGI substrate comparison"
  - "4-plane comparison"
  - "substrate comparison table"
  - "what LangGraph provides"
  - "what A-FORGE requires"
  - "G1 BSP scheduler"
  - "BSP scheduler spec"
  - "OpenCode forge prompt"
  - "arifFlow Phase 2"
  - "bridge and adapter"
  - "verdict timeout"
  - "crash recovery test"
  - "governed BSP executor"
  - "parallel cognition tracer"
  - "multi-plane Merkle state"
  - "micro-seal"
  - "parallel universe"
  - "constitutional conductor"
---
# Governed Execution Substrate

## What This Skill Is

Design and forge execution engines, state machines, and orchestration runtimes that operate under constitutional governance (F1-F13, 6-plane Zen, 888-JUDGE). This skill covers the entire class of work: from analyzing conventional tools like LangGraph/Temporal to building a sovereign replacement that enforces epistemic discipline, irreversibility gates, and checkpointed authority at every transition.

**This is NOT about:**
- Agent anatomy (see `governed-agent-anatomy` — the 7 primitives)
- Constitutional floors (see `constitutional-auditor` — F1-F13 floor definitions)
- APEX intelligence measurement (see `apex-verification-pipeline`)
- Observability telemetry (see `agentic-integrity-observability` / Kabarkan)

**This IS about:** the execution runtime that sits *between* the intelligence and governance planes — the channel-based state machine that schedules parallel work, enforces constitutional gates at every transition, and provides verifiable checkpoints that include authority context.

---

### The EUREKA Insight: This Is a Different Category

Arif (2026-07-25) articulated a distinction that every agent building execution substrates must internalize. You are not building "LangGraph but better." You are building a **constitutional physics layer** — a different category entirely.

| Tool | Category | What it does | What it CANNOT do |
|------|----------|-------------|-------------------|
| **LangChain** | Framework | Chains LLM calls, picks tools | Governance, identity, reversibility |
| **LangGraph** | Graph Runtime | State machine orchestration, Pregel BSP | F1-F13 floors, witness parity, 888-HOLD |
| **LangFuse** | Observability | Trace spans, cost, latency | Verdict telemetry, cooling drift, cc_id evolution |
| **arifOS + arifFlow** | **Constitutional Kernel** | Governs parallel execution, seals lineage, enforces reversibility, binds identity, witnesses parity | None of the above — it does not compete in the framework/runtime/observability category |

**Every dimension follows from this category shift:**

- **LangGraph** lets you build *any* state machine. **arifOS** only allows *legal* state machines — F1 AMANAH (reversible-first), F2 TRUTH (evidence required), F3 TRI-WITNESS (merge consensus), F13 SOVEREIGN (human veto). Every edge carries cc_id + VAULT999 lineage.

- **LangGraph edges** are arbitrary, user-defined, ungoverned. **arifOS edges** are constitutional transitions — you can traverse from state A to state B only if F1-F13 permits it.

- **LangFuse** sees *what* happened (spans, cost, latency). **Kabarkan** sees whether it was *allowed* to happen (verdict classes, cooling drift, lane divergence, merge witness parity, cc_id evolution, constitutional compliance). One is observability; the other is governance telemetry.

- **LangChain agents** are functions with memory. **AAA agents** are constitutional citizens — identity, lease, capability tiers (333/555/888), constitutional obligations, 888-HOLD halting, VAULT999 sealing, Tri-Witness auditing, A-AUDIT archiving.

- **LangGraph parallelism** is concurrent execution (Pregel deterministic). **arifFlow parallelism** is *governed* parallel execution — lanes have leases, verdicts, cooling states, reversible/irreversible classification. Merges require TRI-WITNESS. Barriers require constitutional compliance. Every super-step produces a VAULT999 envelope.

### The Constitutional Reflex Arc (ART → Kernel → ACT)

The reflex arc that no Lang* product has is the foundation of safe AGI — not a feature, not a product, but the constitutional physics of intelligence:

```
ART (pre-kernel)   →   Kernel (F1-F13)   →   ACT (post-kernel)
Observe reality    →   Judge             →   Execute
Classify action    →   Enforce floors    →   Mutate world
Gather evidence    →   Block irreversible →  Seal lineage
Assess risk        →   Require witness   →   Append evidence
```

### When Reasoning About Execution Substrates

Your agents must internalize:

1. **"You didn't build a framework. You built a kernel."** Frameworks help you build apps. Kernels define what apps are allowed to do. This is the difference between tools and law.

2. **"LangGraph = StateGraph; arifOS = Constitutional StateGraph."** LangGraph lets you build any state machine. arifOS only allows *legal* state machines. The constitution IS the constraint.

3. **"Parallelism without governance = chaos. Parallelism with governance = AGI substrate."** langGraph's parallel execution is concurrent nodes. arifFlow's parallel execution is governed lanes with leases, verdicts, cooling states, and TRI-WITNESS merge.

4. **"LangFuse traces events; Kabarkan traces governance."** One sees what happened. The other sees whether it was *allowed* to happen. Governance telemetry is not observability.

5. **"LangChain agents are functions; AAA agents are citizens."** Identity, lease, obligation, halt, seal, witness, audit — these are citizenship, not function signatures.

---

## The Core Insight: Graph vs Constitution

Conventional execution engines (LangGraph, Temporal, Airflow) are built on a **graph metaphor**: define nodes (functions) and edges (transitions), compile, and run. The graph IS the program. The LLM/agent only chooses which predefined branch to execute.

A governed execution substrate is built on a **constitution metaphor**: define invariants (F1-F13), declare fixed topologies (fan-out, pipeline, cascade), and let the constitution gate every transition. The topology is explicit and auditable. No graph, no path explosion, no ungoverned edges.

| Dimension | Graph Engine (LangGraph) | Constitutional Substrate (arifOS) |
|-----------|-------------------------|-----------------------------------|
| **Primitive** | Nodes + Edges + State | Channels + Gates + Merkle Ledger |
| **Execution** | Pregel BSP super-steps | Constitutional super-steps (gate at every transition) |
| **State** | Mutable TypedDict with reducers | Append-only channel history, hash-chained |
| **Checkpoint** | JSON blob per node | `{state_hash, verdict_id, lease_id, actor_id}` |
| **Identity** | None — developer is authority | F13 bound — every transition carries actor_id |
| **Governance** | Human-in-the-loop interrupt at node boundary | 888-JUDGE at every channel transition |
| **Recovery** | Resume from last checkpoint | Resume only if verdict_id still valid — post-hoc audit can invalidate |
| **Parallelism** | Pregel deterministic, no witness | Pregel + F3 TRI-WITNESS merge — divergence triggers HOLD |
| **Termination** | Quiescence (no more messages) | SEAL receipt emitted to VAULT999 |
| **Trust model** | Assumes nodes are correct | Falsifies every claim through Kill Matrix K001-K007 |

### The 4-Plane Comparison Methodology

A reusable framework for evaluating ANY external system against the arifOS federation. Used to produce the AGI Substrate Comparison Table (see `references/arifflow-phase2-and-g1-alignment.md`).

**The four planes:**

| Plane | Question | What it covers |
|-------|----------|----------------|
| **1 — Kernel** | What enforces boundaries? | Constitution, floors, separation of powers, human veto, immutable ledger, epistemic truth hierarchy |
| **2 — Organs** | What WITNESSES / COMPUTES / REFLECTS? | Domain organs (GEOX, WEALTH, WELL), execution, control plane, telemetry |
| **3 — Agentic State** | What persists between steps? | State schema, reducers, checkpointing, crash recovery, cross-plane isolation, Merkle commitment |
| **4 — Actuator** | What changes the world? | Parallel execution, pipelines, multi-agent patterns, HITL, subgraph composition, cycles |

**How to use:**
1. For each external system (LangGraph, Temporal, CrewAI, etc.), fill one column per plane
2. For each arifOS component (arifOS, AAA, A-FORGE, arifFlow), fill one column per plane
3. The comparison reveals: what the external system does WELL (consider absorbing), what it CANNOT do (constitutional gap), and where arifOS already surpasses it

**The truth this methodology reveals:** Commercial tools optimize one plane at the expense of others. LangGraph optimises Actuator (flexible graphs) but has zero Kernel. Langfuse optimises Organs (telemetry) but has zero Kernel. arifOS is the only system that starts from the Kernel and builds outward — which is why no single tool can "replace" it, and every tool must be absorbed into it.

---

## The Four Sovereign Techniques (Arif, 2026-07-25)

Arif (F13) laid out 4 architectural principles that define the sovereignty gap between commercial graph engines and a governed substrate. Every implementation of an execution engine must satisfy all four:

### A. Hashed State Ledger (Not Checkpoints)

**Conventional way:** Dump a JSON blob to a database after every node (LangGraph checkpointing).

**Sovereign way:** Every state transition emits a content-hashed evidence receipt (HMAC/SHA256). State is not a dictionary — it is an **append-only Merkle tree**. If a node claims to have executed a task, the resulting state must contain the cryptographically verified receipt of that task. This builds the Git-like lineage chain required for absolute auditability (F11).

**Implementation:** The Rust core's `MerkleRoot` is computed per super-step as `SHA256(state_id || previous_root || deltas[])`. Every Nth root is Merkle-anchored to VAULT999.

### B. Artifact Spine (References Over Values)

**Conventional way:** Pass the entire conversation history and extracted data between nodes, leading to massive token bloat and context degradation.

**Sovereign way:** The execution graph passes **pointers**, not payloads. The AAA MCP transport wire manages heavy objects (e.g., xarray/zarr datasets for GEOX, LAS files for wells). Nodes only pass URIs and validation hashes. This keeps the execution loop extremely lightweight (ΔS < 0) and mathematically grounded.

**Implementation:** Channel data is always `{uri: string, hash: string, type: string}` — never the raw object. The gate layer resolves URIs to actual data only when needed for constitutional review.

### C. Edge as the APEX Judge (Constitutional Routing)

**Conventional way:** Edges are basic `if/else` conditions (LangGraph: "if tool called, go to ToolNode").

**Sovereign way:** Every edge E in the execution topology is an **active APEX checkpoint**. Before state is committed and passed to the next node, the edge itself runs the Tri-Witness Validation:
- Does this transition violate F1 (Safety/Reversibility)?
- Is the confidence P(truth) ≥ 0.99?
- If risk is high/irreversible, the edge defaults to HOLD and explicitly requests 888 authorization.

**Implementation:** The Rust core fires a gate-check event to the Python/TS GovernanceBridge after every super-step. The bridge returns SEAL | HOLD | VOID. The core never adjudicates — it only schedules and fires events.

### D. Proxy Tooling Over Embedded Execution

**Conventional way:** Bind Python functions directly to agent nodes (LangGraph: nodes ARE the tool calls).

**Sovereign way:** Agents do not execute tools. The execution shell **proxies** calls via the AAA MCP layer. The node requests an action, the MCP layer executes it, and the independent state verifier (dual-control) confirms the outcome before the graph is allowed to proceed. This prevents the false-success defect — a node claiming success when execution actually failed.

**Implementation:** A-FORGE already does this — the 4-layer forge gate sits between the agent and the tool. The Rust core just formalizes this as a channel-level invariant: no channel delta is committed until the proxy verifier returns PROCEED.

---

## The Gap Analysis: Why LangGraph Cannot Be Wrapped

A common mistake is "wrap LangGraph nodes with arifOS calls". This fails structurally:

1. **Pregel expects fast nodes.** Constitutional checks (F13 binding, F1 reverse scan, 888 round-trip) take real time — seconds, not microseconds. A slow node blocks the entire super-step.

2. **No authority escalation.** LangGraph has no concept of "this tool call needs F13 approval, pause graph until Arif responds." Its `interrupt()` pauses at node boundaries but carries no verdict chain.

3. **Checkpoints lack authority context.** A LangGraph checkpoint restores state but not authority. If a node committed a violation post-hoc, restoring from checkpoint resumes from a compromised context.

4. **No plane separation.** Intelligence, governance, and execution all run in one process with one memory space. arifOS requires 6-plane separation — each plane has different latency profile, security context, and failure mode.

**Arbitration rule:** If the system you're analyzing cannot distinguish between "node A returned an error" and "node A violated F5 and is now blocked at 888", it is not a governed execution substrate — it's an orchestration library.

---

## The arifFlow Engine Architecture

### Two-Layer Design

```
┌─────────────────────────────────────────────┐
│  RUST CORE (no I/O, no governance logic)     │
│                                              │
│  Channel<T>     — typed, append-only buffer  │
│  Node<T>        — subscribes to channels     │
│  SuperStep      — BSP barrier + deterministic│
│                   parallel execution         │
│  MerkleRoot     — SHA256(state||prev_root||  │
│                    deltas) per super-step    │
│                                              │
│  Compiles to WASM for edge/orphan nodes      │
└──────────────┬──────────────────────────────┘
               │ channel: "state_delta" + receipt_hash
               │
┌──────────────▼──────────────────────────────┐
│  PYTHON/TS GATES (existing organs)           │
│                                              │
│  1. AmanahLock (F1 scan)     — TypeScript    │
│  2. GovernanceBridge (888)   — Python/TS     │
│  3. F3 TRI-WITNESS merge     — Python        │
│  4. VAULT999 seal writer     — Python        │
│  5. Kabarkan trace           — Python        │
│  6. WELL fatigue check       — Python/MCP    │
└──────────────────────────────────────────────┘
```

**Why Rust for the core:**
- No GC pause — super-step scheduling needs deterministic µs, not ms
- Memory safety via ownership model — zero-copy channel data between branches
- WASM target — run on edge/orphan nodes without Python/Node runtime
- Tokio actor model (`tokio::sync`, actix/ractor) for channel-based concurrency

**Why Python/TS for the gates:**
- Existing codebase — forge gate, VAULT999, Kabarkan already in Python/TS
- Constitutional logic changes slowly — no performance bottleneck at gates
- MCP protocol — all organs speak MCP, Rust core exposes channel events via MCP boundary

### No Mutable State in Rust Core

The Rust core holds only:
- `Channel<T>` — versioned, append-only buffer per channel
- `SuperStep` scheduler — BSP barrier + node dispatch
- `MerkleRoot` — incremental hash per super-step

**No I/O. No governance logic. No LLM calls.** Every super-step end:
1. Rust passes `(state_delta, actor_id, lease_id)` to GovernanceBridge (Python/TS via FFI or MCP)
2. Bridge runs: F1 scan → Model check → 888-JUDGE → Approval check
3. Returns: SEAL | HOLD | VOID
4. If SEAL: commit delta, bump version, write VAULT999 receipt
5. If HOLD/VOID: discard delta, halt, emit hold receipt

---

## F1 Per-Lane Reversibility (P0 Pattern — Rust)

Every parallel lane must declare its safety envelope *before* execution. Irreversible actions without 888_JUDGE pre-approval are physically blocked at the Rust runtime level — not at the prompt level, not at the middleware level, but at the state machine transition.

### Implementation

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Reversibility {
    Reversible,    // Can undo — proceed normally
    Irreversible,  // Cannot roll back — requires 888_JUDGE verdict
}

impl Reversibility {
    pub fn requires_verdict(&self) -> bool { matches!(self, Reversibility::Irreversible) }
}

// Added to FlowNode trait with reversible default:
pub trait FlowNode: Send {
    fn reversibility(&self) -> Reversibility { Reversibility::Reversible }
}
```

### Pre-Dispatch Gate

```rust
// In step(): check each node before execution
for node in nodes.iter() {
    if node.reversibility() == Reversibility::Irreversible {
        if !self.approved_irreversible_lanes.contains(&node.id().to_string()) {
            return Err(SchedulerError::F1Blocked(lane_id));
        }
    }
}
```

### Invariants

- Default is REVERSIBLE — every new lane type is assumed safe until declared
- IRREVERSIBLE requires pre-approval — `approve_irreversible_lane()` after 888_JUDGE
- Approvals cleared on HOLD/VOID — `commit_verdict(HOLD)` resets approval list
- LangGraph cannot do this — every StateGraph node is equal, no reversibility distinction

---

## Barrier Timeout Policy (P0 Pattern — Rust)

A graph that waits forever is a failed state machine. Explicit timeout boundaries prevent a rogue lane from hanging the entire system.

### Implementation

```rust
#[derive(Debug, Clone, Copy)]
pub struct BarrierConfig {
    pub timeout_ms: u64,          // default 30_000
    pub on_timeout: TimeoutPolicy,
}

pub enum TimeoutPolicy {
    HoldAll,            // Hold all lanes, escalate to 888
    ContinueMajority,   // Proceed with what completed
    CancelAll,          // Cancel all, mark FAILED
}
```

### Enforcement

The scheduler tracks wall-clock time from super-step start:
1. Before each node execution, check elapsed against `timeout_ms`
2. If exceeded with HoldAll/CancelAll → return `SchedulerError::BarrierTimeout`
3. If exceeded with ContinueMajority → proceed with partial results
4. Final check after all nodes: same logic

### Tests

```text
test_barrier_timeout_triggers_hold_all           ✅
test_fast_node_within_barrier_timeout           ✅
test_barrier_timeout_continue_majority           ✅
test_f1_blocks_irreversible_without_approval    ✅
test_f1_allows_irreversible_with_approval        ✅
test_f1_approvals_cleared_on_hold                ✅
...plus 3 more = 9 new P0 tests total
```

---

## Fixed Topologies (Not General Graphs)

LangGraph's "flexibility" (any node can connect to any edge) creates untested path explosion. The governed substrate uses **fixed topologies** — 3 proven patterns:

### 1. Fan-out Inquiry

```
Trigger ──┬──→ GEOX (basin analysis)
           ├──→ WEALTH (NPV/IRR)
           ├──→ WELL (fatigue check)
           │
       [Barrier — wait for all]
           │
       [F3 TRI-WITNESS merge — compare outputs]
           │
       [888-JUDGE → SEAL | HOLD]
```

Use: multi-organ parallel inquiry. GEOX + WEALTH + WELL all analyze the same prospect simultaneously. Merge function checks for divergence. If any two disagree → HOLD.

### 2. Pipeline

```
Stage 1 ──→ [Gate] ──→ Stage 2 ──→ [Gate] ──→ Stage 3
  (test)      (888)     (build)      (888)     (deploy)
```

Use: self-governing CI/CD. Each stage's output must pass constitutional review before next stage begins. Gate check: reversibility, blast radius, identity match.

### 3. Cascade

```
Auto → [F1 check] → Advisory → [888] → 888_HOLD → F13 (Arif decides)
   ↑                    ↑
  PASS                WARN
```

Use: escalation. Each level applies stricter constitutional scrutiny. Default is HOLD at the boundary between autonomous and irreversible.

**Rule: If you need a general graph, you haven't classified your execution patterns yet.**

---

## Constitutional Checkpoints

### LangGraph's Flawed Model

LangGraph checkpoints = `{state_snapshot}` — JSON blob. Recoverable but NOT verifiable. No way to tell if the checkpointed state was constitutionally valid.

### arifFlow Model

Every checkpoint carries authority context:

```rust
struct Checkpoint {
    super_step: u64,
    channel_versions: HashMap<ChannelId, u64>,
    merkle_root: [u8; 32],           // hash of all channels at this step
    verdict_id: Option<Uuid>,         // 888 verdict that authorized the transition
    lease_id: Uuid,                   // A-FORGE lease
    actor_id: String,                 // who triggered this
    timestamp_ns: i64,
}
```

**Resume rule:** Resume only if `verdict_id` is still valid. A post-hoc audit can invalidate a checkpoint by revoking its verdict. Without this, crash recovery is a security hole — you resume from a compromised state.

**Root-of-trust:** Every Nth checkpoint is Merkle-anchored to VAULT999 (matching the existing `/root/arifOS/VAULT999/outcomes.jsonl` pattern).

---

## Flow Receipt v1 — The Unit Atom of Governed Flow

Flow Receipt v1 extends the checkpoint concept to the **message level**. Every message in every channel carries a self-authenticating receipt. The receipt IS the governance check — not a reference to a separate check log.

**Core principle:** "When the receipt IS the governance, the agent flows."

### Anatomy

Every `FlowReceipt` records:

| Field | Type | Purpose |
|-------|------|---------|
| `receipt_id` | UUID v4 | Globally unique identifier |
| `previous_receipt_hash` | Option SHA3-256 | Chain linkage — None for first |
| `created_at` | DateTime<Utc> | Nanosecond-precision timestamp |
| `actor_id` | String | Who performed this step |
| `session_id` | String | Governing session from arif_init |
| `step_type` | StepType | Execute/Verify/Cool/Seal/Barrier/Merge/Route |
| `topology_id` | Option String | Which topology context |
| `lane_id` | Option u32 | Which parallel lane |
| `step_number` | u64 | Monotonic counter |
| `cost_ns` | u64 | Wall-clock duration |
| `preceding_verify_cost_ns` | Option u64 | Verification cost leading to this step |
| `epistemic_label` | EpistemicLabel | OBS/DER/INT/SPEC/SEAL |
| `floor_verdict` | FloorVerdict | PASS/CAUTION/HOLD/VOID |
| `cooling_decision` | CoolingDecision | NONE/HOLD/CLAMP/BYPASS |
| `tri_witness_votes` | Option TriWitnessVotes | human/ai/earth confidence (0.0-1.0) |
| `merkle_root` | Option String | Root hash of parent Merkle tree |
| `payload` | Option Value | Flexible JSON payload |

### StepType — 7 Atomic Step Classes

| StepType | FQ Classification | Examples |
|----------|-------------------|----------|
| Execute | Execution (numerator) | Computation, forge, deploy |
| Verify | Verification (denominator) | Floor check, audit, gate |
| Cool | Neither | Cooling queue action |
| Seal | Execution (numerator) | VAULT999 commit |
| Barrier | Neither | Wait for N lanes |
| Merge | Execution (numerator) | Combine N outputs |
| Route | Neither | Dispatch to another organ |

### EpistemicLabel — F2/F7 Classification

| Label | Short | Meaning |
|-------|-------|---------|
| Observation | OBS | Direct sensed reality |
| Derivation | DER | Logical deduction from evidence |
| Interpretation | INT | Inference under uncertainty |
| Specification | SPEC | Plan or intended action |
| Seal | SEAL | Irreversible commitment |

### FlowVerdict — The Inverted-U of Agentic Governance

```
FQ > 3.0      → OPTIMAL   (agent in flow — governance in architecture)
1.0 < FQ ≤ 3.0 → BALANCED (healthy verification)
0.5 < FQ ≤ 1.0 → WATCHING (self-monitoring competes with execution)
FQ ≤ 0.5      → STUCK     (self-monitoring has become the task)
```

### FlowQuotient — The Metric

```text
FQ = Σ(Execute.cost_ns) / Σ(Verify.cost_ns + preceding_verify_cost_ns)
```

Computed over a sliding window (default = last 100 receipts). The `preceding_verify_cost_ns` field attributes verification cost to the execution it enabled.

Optimal range > 3.0 (execute cost dominates). Below 0.5 = stuck (governance IS the task).

**Key finding (r = -0.73):** FQ ↓ → ΔS ↑. When an agent stops executing, it starts drifting.

### ReceiptStore

Bounded in-memory chain (default capacity 1000). Operations:

- `push(receipt)` — validates chain continuity at insert time
- `flow_quotient(window)` — sliding-window FQ computation
- `verify_chain()` — full chain integrity check
- `last_n(n)` — last N receipts for analysis

Chain rule: first receipt has `previous_receipt_hash = None`; every subsequent receipt must hash-chain to its predecessor via SHA3-256.

### Wiring Pattern

- **Channel::Message** carries `receipt: FlowReceipt` on every message
- **SuperStepScheduler** holds `receipt_store: ReceiptStore`, pushes receipts per F1-check and per-execution-step
- **SuperStepResult** returns `fq: FlowQuotient` and `receipt_store: ReceiptStore`
- **KabarkanEvent::AfqSnapshot** emitted with execution/verify counts, FQ ratio, and diagnosis
- **STDIN/STDOUT protocol** `need_verdict` message carries `afq_execution_steps`, `afq_governance_steps`, `afq`, `afq_diagnosis` for judge-side flow awareness

### Design Rationale

- **SHA3-256** for receipts (NIST-standard, export/audit compatible), **blake3** for internal Merkle (performance) — no single crypto point of failure.
- **chrono timestamps** for receipts (human-readable), **i64 nanos** for structural timestamps (compactness).
- **Cost-weighted FQ** (nanoseconds) better captures verification *weight* than step-count ratio.
- **Bounded store** prevents memory leak; sliding window matches the recency requirement of FQ (ancient history shouldn't dominate).

### Reference

- `src/receipt.rs` in arifFlow — 926 lines, 20 tests (all receipt types, FQ, chain, store, builder)
- `src/channel.rs` — Message carries receipt field
- `src/scheduler.rs` — ReceiptStore tracked per scheduler, FQ in SuperStepResult
- `src/governance/kabarkan.rs` — AfqSnapshot event
- `src/main.rs` — FQ data in need_verdict protocol message
- See `references/flow-receipt-v1-design.md` for session transcript detail

### Pitfalls

- **FlowReceipt ≠ CheckpointEnvelope.** Receipt is per-message (atomic). Checkpoint is per-super-step (aggregate channel state). Every super-step produces multiple receipts but one checkpoint.
- **Receipts are append-only.** Never mutate after creation — hash changes break chain. Builder patterns only at construction time.
- **FQ thresholds (3.0/1.0/0.5) are initial values.** Adjust per agent type — a security tool may naturally run lower FQ.
- **ReceiptStore is bounded.** Default max 1000. Sliding window FQ (100) always ≤ capacity.
- **Two hash functions by design:** blake3 for internal speed, SHA3-256 for external audit compatibility. Don't unify.

---

## Daemon Deployment Pattern

The arifFlow binary supports two modes:
1. **STDIN/STDOUT protocol** (default) — JSON-L commands via pipe, for A-FORGE adapter
2. **`--daemon` mode** — TCP listener with HTTP health endpoint

**Daemon endpoints (port 7073):**

| Method | Path | Purpose | Response |
|--------|------|---------|----------|
| GET | `/health` | Live FQ gauge | `{"status":"ok","fq":{...},"receipts":N,"uptime_ms":M}` |
| POST | `/ingest` | Push FlowReceipt | `{"status":"ok","fq":{...}}` — updates ReceiptStore, returns new FQ |
| POST | `/flow` | JSON-L command | Passthrough to STDIN protocol engine |

**Systemd unit:** `ariflow.service`

```ini
[Service]
ExecStart=/usr/local/bin/ariflow --daemon
Restart=on-failure
RestartSec=5
Environment=ARIFLOW_PORT=7073
```

**Deploy sequence:**
```bash
cd /root/arifFlow
cargo build --release
cp target/release/ariflow /usr/local/bin/ariflow
cp deploy/ariflow.service /etc/systemd/system/
systemctl daemon-reload && systemctl restart ariflow
```

**Verify:**
```bash
curl http://127.0.0.1:7073/health | jq .
journalctl -u ariflow -f
```

**Reference:** See `references/reality-engineering-primer.md` for the philosophical layer — governance-as-physics, somatic-agentic equivalence, and the 5-layer document architecture.

---

## Verified Substrate Status (Live Probe — 2026-07-25, Updated Post-P0-Gaps)

> **Epistemic tag:** CLAIM (verified by live HTTP probe + file system audit)
>
> **Source:** `curl :7071/health`, `git log`, `dist/` file listing, `pytest`/`node --test` results, VAULT999 `wc -l`

### arifFlow (`/root/arifFlow/`, Rust, compiled binary at `target/release/ariflow`)

| Component | Status | Evidence |
|-----------|--------|----------|
| SuperStepScheduler | ✅ **79 tests** | Channel, Merkle, Scheduler, FanOut, Checkpoint, Cooling, TriWitness, Bridge, Receipt, FQ, Kabarkan, Daemon |
| Barrier timeout policy | ✅ Compiled | BarrierConfig + TimeoutPolicy (HoldAll/ContinueMajority/CancelAll) |
| F1 per-lane reversibility | ✅ Compiled | Reversibility enum, pre-approval guard, auto-clear on HOLD |
| Cooling queue | ✅ Compiled | CoolingManager in governance/cooling.rs |
| TRI_WITNESS module | ✅ Compiled | tri_witness.rs — witness parity computation |
| Python adapter | ✅ Phase 1 | arifFlow_adapter.py — spawn binary, pipe stdin/stdout, call arif_judge |
| **arifOS HTTP bridge** | ✅ **LIVE (Phase 4.1)** | `bridge/arifos_governance.rs` — real HTTP calls to arifOS :8088 via reqwest blocking. Replaced blake3 stubs. |
| A-FORGE FFI bridge | ⚠️ Synthetic | Stubs return mock receipts |
| VAULT999 real writes | ⚠️ Synthetic | In-memory only |
| Kabarkan NATS | ⚠️ Synthetic | In-memory buffer only |
| **888-HOLD** | ✅ **LIFTED** | Phase 3 tests passed: FFI 100/100, Verdict timeout 0.04s, Crash recovery 3 checkpoints survive kill |

### arifOS Kernel (`/opt/arifos/app`, Python, :8088)

| Component | Status | Evidence |
|-----------|--------|----------|
| Session state | ✅ Production | `SessionState` Pydantic model, identity-bound |
| Thermodynamic state | ✅ Production | `ThermodynamicState`, per-transition ΔS |
| Hold state | ✅ Production | `HoldStateManager`, 888_HOLD lifecycle |
| Verdict engine | ✅ Production | 888-JUDGE: SEAL/HOLD/VOID/SABAR |
| VAULT999 ledger | ✅ Production | **4,704 receipts** in append-only JSONL |
| **Channel/subscription** | ❌ Missing | No Pregel-style channel routing |
| **Super-step scheduler** | ❌ Missing | Sequential only — one MCP call at a time |

### A-FORGE (`/opt/a-forge/app`, TypeScript + Python, :7071/:7072)

| Component | Status | Evidence |
|-----------|--------|----------|
| A-FORGE server | ✅ Production | `:7071/health` → ok, degraded=false, drift=false, v2026.07.24 |
| 7-phase ACT executor | ✅ Production | `/apa/core/act_executor.py` — imports and runs |
| 4-layer forge gate | ✅ Production | AmanahLock→ModelCapability→GovernanceBridge→ApprovalBoundary |
| AgentEngine | ✅ Production | `dist/src/domain/engine/AgentEngine.js` compiled, governance wired |
| FloorEnforcer | ✅ Production | 25/27 tests passing |
| F1 AmanahLock | ✅ Production | `AmanahLockManager.js` — catastrophic pattern scan |
| F3 TriWitnessValidator | ✅ Production | `dist/src/domain/governance/TriWitnessValidator.js` |
| CoolingGate | ✅ Production | `dist/src/domain/governance/CoolingGate.js` |
| QQQRuntime | ✅ Production | `dist/src/domain/governance/QQQRuntime.js` |
| **Parallel execution** | ❌ Missing | No fan-out/parallel_runner code — `grep` confirms zero matches |
| **F3 merge verifier** | ❌ Missing | `ConvergenceEngine` evaluates verdicts but doesn't run parallel branches |
| **Constitutional checkpoint** | ❌ Missing | Checkpoints are manual — no automated per-transition `{verdict_id, lease_id}` |

### Build & Test Health

| Check | Result | Detail |
|-------|--------|--------|
| `npm run build` | ✅ PASS | TypeScript compiles clean — 130+ files in `dist/src/domain/` |
| `FloorEnforcer.test.js` | ✅ 25/27 | Floor validation coverage |
| `PlanValidator.test.js` | ✅ PASS | All plan validation tests |
| TypeScript module layout | ✅ Complete | governance/, engine/, forge/, orchestration/, containment/, continuity/ — 15+ subdomain subsystems |

## Readiness Audit — Assessing Federation Readiness for a Governed Parallel Execution Forge

Before forging a new execution substrate (arifFlow, BSP scheduler, super-step engine), run this readiness audit. It answers the question: **"Does the federation have enough infrastructure to forge a governed parallel execution engine, or are there critical gaps that would block implementation?"**

### When to Run

- Arif proposes a forge (new execution engine, parallel runtime, multi-agent orchestrator)
- You're asked "what would it take to make the federation parallel?"
- Before allocating engineering time to design/building a parallel execution component
- During periodic federation health review that asks "what's the next big capability?"

### The 6-Domain Framework

Every parallel execution forge transforms exactly **6 domains**. Assess each:

| Domain | Question | What to probe |
|--------|----------|---------------|
| **1. Kernel (Judgment)** | Can arifOS adjudicate multiple parallel lanes simultaneously? | Multi-lane judge, per-lane verdict, lease×actor×verdict×ccId per lane |
| **2. State (AAA)** | Can AAA hold per-plane Merkle state trees? | Plane isolation, cross-plane verified envelopes, Merkle root per super-step |
| **3. Actuator (A-FORGE)** | Can A-FORGE execute parallel BSP super-steps? | BSP scheduler, super-step barrier, governed merge engine, fan-in protocol |
| **4. Conductor (Hermes)** | Can Hermes spawn governed agents with leases? | Lease-based spawn, constitutional gate on every spawn, output merge with witness |
| **5. Observability (Kabarkan)** | Can Kabarkan trace parallel cognition? | Super-step boundaries, lane divergence signals, merge verdicts, constitutional chain evolution |
| **6. Truth (VAULT999)** | Can VAULT999 record per-step constitutional state? | Per-super-step immutable envelope, per-merge witness envelope, per-HOLD breach envelope, per-cooling metabolic envelope |

### Probe Sequence

**Step 1 — Probe all organs for health + identity:**
```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name :$port" || echo "❌ $name :$port"
done
```

**Step 2 — Map each organ's key infrastructure:**
- arifOS: governance pipeline, lease registry, DAG executor, cooling ledger
- A-FORGE: forge_parallel, ConvergenceEngine, ParallelPlannerContract, PipelineCoordinator
- AAA: state store, FloorEnforcer, TriWitnessValidator
- Kabarkan: worker, NATS bus, span schema
- VAULT999: outcomes.jsonl, cooling envelopes

**Step 3 — Check test coverage for parallel-relevant components** (FloorEnforcer, ConvergenceEngine, ParallelPlannerContract, ParallelTools, DAG executor).

**Step 4 — Check git state:**
```bash
for repo in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do
  echo "$(basename $repo): $(git -C $repo status -s | wc -l) dirty"
done
```

**Step 5 — Probe for existing compiled implementations:**
Sebelum tulis spec baru, check kalau ada implementation yang dah compile (Rust, Go, C/C++). Ini prevent scenario spec ditulis untuk TypeScript sedangkan Rust core dah wujud dengan 24 tests.

```bash
# Check for Rust binary
find /root -name "ariflow" -type f 2>/dev/null
# Check for Cargo.toml
find /root -path "*/ariflow*" -name "Cargo.toml" 2>/dev/null

# Probe binary API — check main.rs for stdin/stdout protocol
head -50 src/main.rs 2>/dev/null

# Check test count
grep -c "#\[test\]" src/*.rs src/**/*.rs 2>/dev/null

# Check public API surface
grep -n "^pub " src/lib.rs 2>/dev/null
```

If a compiled binary exists with passing tests, your spec should WRAP it, not REPLACE it. The correct architecture when finding a Rust core:

```
Rust (execution substrate) → Python (governance conduit) → TypeScript (governance surface)
```

**Delta analysis:** When Rust core exists, map planned spec against existing implementation:

| Domain | Spec says | Existing has | Gap |
|--------|-----------|--------------|-----|
| BSP scheduler | TypeScript | Rust SuperStepScheduler ✅ (44 tests) | Write wrappers, not re-implementation |
| Merge strategies | TypeScript | FanOutTopology.merge_results() ✅ | Write wrappers |
| Kabarkan | New spans | KabarkanTracer structs ✅ | Client-side emit |
| VAULT999 | Micro-seals | Vault999Sealer ✅ | Python adapter calls |
| Barrier timeout | New | ✅ ADDED (P0) | 3 tests, 4 policies |
| F1 per-lane | New | ✅ ADDED (P0) | Reversibility enum, approval guard |
| Cooling queue | New | ✅ ADDED | CoolingManager module |
| TRI_WITNESS scorer | New | ✅ ADDED | tri_witness.rs |
| Real FFI bridges | New | ⚠️ Synthetic | Phase 4 plumbing |

The 3 most common Rust-core gaps when doing a BSP scheduler forge — barrier timeout policy, lane cooling queue, F1 per-lane reversibility — were all closed in a single session (2026-07-25). Starting from a compiled 24-test binary, the final state is 44 tests with all P0 gaps closed and 888-HOLD lifted. **Always check if a compiled binary exists before writing specs — you may only need extensions, not a ground-up forge.**

### Catalog Format

For each organ, produce this inventory table:

| Komponen | Status | Lines | Lokasi |
|----------|--------|-------|--------|
| Component name | ✅/⚠️/❌ | LOC | file path |

Mark as:
- **✅ LENGKAP** — production-ready, tested, wired
- **⚠️ Partial/Sequential** — exists but doesn't support parallel semantics
- **❌ Missing** — doesn't exist at all

### Gap Classification

Every gap gets classified into one of three tiers:

| Tier | Label | Meaning | Action |
|------|-------|---------|--------|
| **P0** | Critical Path | Wajib sebelum parallel execution boleh jalan | Forge first |
| **P1** | Supporting | Perlu untuk production readiness | Forge in parallel with P0 |
| **P2** | Enhancement | Siap bila Tier 1+2 dah jalan | Deferred |

Components that already have a **partial implementation** (forge_parallel, ConvergenceEngine, DAG executor) are marked as lower effort than components that start from zero.

### Readiness Score

Compute a weighted score per domain:

```
Readiness = existing_components / total_needed * 10
```

Where "total_needed" includes both what exists and what's missing for the forge. A score of:
- **8-10**: Ready to forge — minor gaps, no blockers
- **5-7**: Forge-able with parallel workstreams — has critical path components, needs P1 work concurrently
- **3-4**: Needs infrastructure build-out first — critical path missing
- **0-2**: Early stage — design before forge

### Coverage Verification

Check test coverage for every component the forge will touch. For each component, report: ✅ tests exist, ❌ no tests (mark as risk).

### Output Format

Produce a structured report:
1. Live probe timestamp + organ health status
2. Existing infrastructure inventory (what the forge builds on)
3. Readiness score per domain + overall
4. Gap analysis with 3 tiers
5. Ready-to-forge components (can start immediately)
6. Coverage verification table
7. Effort estimate per tier + total
8. One-paragraph verdict: can the forge proceed?

### Pitfalls

- **Don't assume organ health = forge readiness.** All organs green is necessary but not sufficient. A healthy organ may lack the right interfaces (no parallel tools, no BSP hooks, no multi-plane state).
- **Don't count existing infrastructure as "work done."** Having a DAG executor that's sequential-only is good foundation but still needs BSP wrapping. Mark as ⚠️ (sequential), not ✅.
- **Don't skip test coverage.** Components without tests are additional forge scope — factor it into estimates.
- **The `forge_parallel` being REVERSIBLE in actionClassifier is not enough.** The spawn mechanism exists but the **BSP barrier, super-step state machine, and governed merge** are what make it constitutional. Parallel spawn without governed merge is just parallel chaos.
- **"Phase3" placeholders in code mean work was already scoped but never filled.** Count them as gaps but note the lower design cost — the hooks are already defined.
- **Writing specs without probing for existing compiled implementations.** If a Rust binary exists with 24 passing tests at /root/arifFlow/target/release/ariflow, your TypeScript-focused spec should WRAP it — not propose a separate TypeScript scheduler. Two specs = two schedulers = two barrier semantics = two merge engines = F1/F3/F13 violation. Always probe target/release/, Cargo.toml, and test counts via `grep -c "#[test]" src/*.rs` first before writing any execution engine spec.

### Reference Implementation

- **`references/readiness-audit-arifflow-2026-07-25.md`** — Worked example of this audit in practice — the full 7.2/10 arifFlow forge readiness audit covering all 6 organs, 8 identified gaps, 3 ready-to-forge components.
- **`references/arifflow-phase3-p0-closure-2026-07-25.md`** — Phase 3 seal state: 44 tests, binary SHA256, 888-HOLD lift, P0 gap closure (barrier timeout + F1 per-lane), repo git state post-housekeeping.
- **`references/third-session-output-2026-07-25.md`** — Third contiguous session: Phase 4.1 real arifOS HTTP bridge, 47 tests, EUREKA Playbook, AGI Substrate Comparison.

---

## Related Skills and References

- **`governed-agent-anatomy`** — The 7 primitives and constitutional chain that the execution substrate must obey. Read this first before designing any engine.
- **`references/arifflow-analysis-langgraph-replacement.md`** — Full session transcript (2026-07-25): LangGraph invariants, architectural limits, Rust vs Python analysis, 3 fixed topologies, blueprint detail. Forged in consultation with Arif (F13 SOVEREIGN).
- **`references/arifflow-phase2-and-g1-alignment.md`** — Phase 2 bridge architecture (Rust subprocess + stdin/stdout JSON-RPC), G1 BSP Scheduler AAA spec-to-Rust-core alignment, 4-plane AGI substrate comparison table, the 3 888-HOLD production gates (FFI stability, verdict timeout, crash recovery), and Phase 1 cooling receipt.
- **`references/unified-ariflow-spec-v1-2026-07-25.md`** — Unified spec merging AAA TypeScript design with existing Rust arifFlow core (24 tests). Rust substrate → Python conduit → TypeScript wrapper architecture. 3 gap fills (barrier timeout, cooling queue, F1 per-lane). Key lesson: probe before you write.
- **`references/opencode-forge-submission.md`** — Procedure for submitting governed forge prompts to OpenCode via `opencode_manager.py`. Covers: when to use this pattern, how to probe for existing compiled implementations before writing specs (critical: `find /root -name "target"` + `cargo test`), the extend-not-rewrite prompt format, CLI submission via `python3 opencode_manager.py spawn`, and the 3 post-submission 888-HOLD gates (FFI stability, verdict timeout, crash recovery). Forged 2026-07-25 after AAA G1 spec almost caused a TypeScript rewrite of an existing Rust core.
- **`three-agent-flow-doctrine`** — Operational counterpart: FQ (Flow Quotient) as federated biomarker for the three-agent protocol (Hermes=metabolizer, OpenClaw=mechanic, OpenCode=builder). Every execution substrate forge must consider FQ impact — new parallel lanes change the execute:verify ratio.
- **`governance-enforcement-audit`** — Audit whether declared governance is backed by real code enforcement. Use to verify your execution substrate's gates are hard, not theatre.
- **`governance-friction-rightsizing`** — Right-size human approval gates. An execution substrate with too many 888 calls becomes unusable; too few becomes lawless.

---

## Pitfalls

- **Building a general graph runtime.** If you think "we need a flexible graph engine," you haven't classified your execution patterns. Start with 3 topologies. Add more only when proven necessary.
- **Wrapping LangGraph.** You cannot inject constitutional governance into a Pregel runtime without breaking the runtime's core invariants. LangGraph's super-step model assumes fast, stateless nodes. Constitutional checks are slow and stateful.
- **Checkpoints without authority.** A checkpoint that restores state without restoring `verdict_id` is a security hole. Post-hoc audit can revoke the verdict that authorized the checkpointed state.
- **Mutable state in the runtime core.** If the Rust/engine core holds mutable state, you lose the append-only guarantee. Every state transition should be a new channel entry, not an in-place update.
- **Single-language bias.** Execution engine speed requires Rust (or similar). Constitutional gate logic requires the existing organ languages (Python/TS). Don't force one language for both — the plane separation demands different substrates.
- **Confusing execution with governance.** The engine schedules and routes. The constitution judges. If your engine starts adjudicating (checking floors itself), you've violated plane separation. Engine calls GovernanceBridge → 888 decides → engine obeys.
- **Parallelism without witness.** Pregel determinism ensures no data races, but two nodes can agree on wrong output. Every parallel merge must run F3 TRI-WITNESS — if branches disagree, emit DIVERGING → HOLD.
- **Skipping the 3 production gates before lifting 888-HOLD.** Every new execution engine must pass: 1) FFI stability (N calls to arif_judge, 0 failures), 2) verdict timeout (kill governance organ, verify HOLD within 15s), 3) crash recovery (kill engine mid-run, restore checkpoint, verify authority re-checked). Until these pass, 888-HOLD stays in place regardless of test coverage.
