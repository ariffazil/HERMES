# A-FORGE Chain Engine Blueprint — LangGraph Replacement

> **Forged 2026-07-25.** Architectural analysis of LangGraph's core invariants,
> arifOS kernel's current state model, and the blueprint for building a
> constitutionally governed execution graph engine that surpasses both.

---

## 1. LangGraph's Core Invariants (what we replace)

LangGraph is a **stateful directed-graph runtime** (Pregel BSP model) with three primitives:

| Primitive | What it is |
|---|---|
| **StateGraph** | Typed shared state + reducer functions (append, last-write, custom) |
| **Nodes** | Python functions: state → partial update |
| **Edges (conditional)** | Router function reads state → returns next node name |

### Hidden invariants that make LangGraph work:

1. **Bulk-synchronous-parallel (BSP)** — Plan → Execute → Update cycle. Deterministic within a superstep. Inspired by Google's Pregel paper. This is the *only* reason LangGraph scales — concurrent nodes within a step, sequential across steps.

2. **Channel types** — `LastValue`, `BinaryOperatorAggregate`, `Topic` (pub/sub), `EphemeralValue`, `NamedBarrierValue`. Each defines merge semantics at the graph level, not the node level. This is the runtime's only mechanism for preventing state corruption under concurrency.

3. **Checkpoint-per-superstep** — State saved to Postgres/Redis after every superstep. Enables: crash recovery, time-travel debugging, human-in-the-loop pause/resume. The `thread_id` is the workflow instance identifier.

4. **`interrupt()` mechanism** — `GraphInterrupt` exception → checkpointer saves → outer caller sees the pause → `Command(resume=...)` restores from checkpoint and re-enters the interrupted node. This is *mechanical*, NOT constitutional.

5. **Subgraph composition** — A compiled `StateGraph` can be a node in another graph. Hierarchical teams with nested supervisors.

6. **Supervisor/Handoff patterns** — Three multi-agent topologies: Supervisor (central router), Hierarchical Teams (subgraphs), Handoff (agent-to-agent direct).

### Where LangGraph fails:

| Dimension | LangGraph | arifOS requirement |
|---|---|---|
| **Separation of Powers** | None. Same node can think, judge, AND execute. | **Hard-enforced**: think proposes → judge adjudicates → forge executes → seal records |
| **Constitution** | None. Governance is whatever the developer's prompt says. | **13 floors (F1–F13)**. Hard violations = VOID. |
| **Epistemic truth** | All state is equal. No labeling. | **7-rank hierarchy** (SOVEREIGN_CANON → UNTRUSTED) |
| **Entropy** | Not measured. | **ΔS ≤ 0 (F4)** — every output reduces uncertainty |
| **Falsification** | Try-catch at best. | **Kill Matrix K001–K007** + contradiction scan |
| **Human veto** | `interrupt()` — mechanical pause. Any caller can resume. | **F13 SOVEREIGN** — only Arif releases an 888_HOLD. Ed25519-signed. |
| **Immutability** | Checkpoints are mutable (write-overwrite Postgres). | **VAULT999** — append-only, hash-chained JSONL. `chattr +a`. |
| **Health** | Monitor your own graphs. | **9-Signal telemetry** (delta/psi/omega) updated continuously. |

---

## 2. Current arifOS Kernel State Model (what exists NOW)

### State — `KernelInput` → `KernelOutput` (per-call, stateless)

The kernel does NOT have a persistent shared state object like LangGraph's `StateGraph`. Every MCP call is:

```
KernelInput(actor, intent, capability, reversibility, domain, evidence)
  → Interceptor (F1–F13 admissibility check)
  → AdmissibilityVerdict (ADMIT_READ / DENY / 888_HOLD / etc.)
  → KernelOutput(decision, audit_hash, seal_type)
```

Each tool call is **self-contained**. No state carries between `arif_think` and `arif_judge`. "Session state" exists in Redis (L2 via SCT tokens) but it's auth state, not workflow state.

### Actuator — 8 MCP tools + 12-stage forge preflight (no graph runtime)

The actuator is:
1. **Interceptor** (`interceptor.py`): F1–F13 gate on every inbound tool call. Returns `AdmissibilityVerdict`.
2. **Forge Preflight** (`forge_preflight.py`): 12-stage mandatory check before `arif_forge` executes:
   ```
   session-token → actor binding → authority recompute → judge-state retrieval
   → hash recompute → chain validation → vault check → plan binding
   → reversibility → human ack → dry-run → EXECUTE or HOLD
   ```
3. **Tool dispatch** (`tools.py`): Routes to the right handler function.

### The Critical Truth

The 7-stage pipeline (000→111→333→444→555→666→777→999) is a **doctrinal convention in AGENTS.md**. It is NOT a compiled runtime. There is NO:
- **State machine** — no runtime enforces the pipeline order
- **Checkpointing** — no per-step persistence (VAULT999 is for final seals, not intermediate state)
- **Graph composition** — no way to define custom topologies
- **Reducer semantics** — no merge logic for parallel node outputs

**You have constitutional enforcement (F1–F13 on every edge) but no execution graph runtime.**
LangGraph has the inverse — graph runtime but no constitutional enforcement.

---

## 3. A-FORGE Chain Engine Architecture Blueprint

### Layer 1: Forge Chain Definition Language

```python
# arifos/forge/chain.py — THE NEW LAYER

class ChainNode:
    tool: str          # "arif_think" | "arif_judge" | "arif_forge" | "arif_observe"
    mode: str          # the mode parameter
    organ: str | None  # if organ-bound (geox/wealth/well)

class ChainEdge:
    source: str
    target: str | dict[str, str]  # direct or conditional {condition → target}
    floor_gate: list[str]         # F-floors to enforce on this transition

class ForgeChain:
    nodes: dict[str, ChainNode]
    edges: list[ChainEdge]
    state_schema: type[StateModel]
    max_iterations: int
    blower_budget: int
```

Example declaration:
```python
chain = ForgeChain(
    nodes={
        "reason":     ChainNode(tool="arif_think", mode="reason"),
        "judge":      ChainNode(tool="arif_judge", mode="intercept"),
        "research":   ChainNode(tool="arif_forge", mode="query", organ="geox"),
        "synthesize": ChainNode(tool="arif_think", mode="metabolize"),
        "execute":    ChainNode(tool="arif_forge", mode="write"),
    },
    edges={
        "reason": {
            "has_enough_evidence": "judge",
            "needs_more_data": "research"
        },
        "research": "synthesize",
        "synthesize": "reason",         # ← LOOP back
        "judge": {
            "seal": "execute",
            "hold": "reason",
            "void": None
        }
    },
    max_iterations=5,
    blower_budget=100,
)
```

**New MCP tool:** `arif_forge_chain(mode="define" | "run" | "checkpoint" | "resume")`

### Layer 2: Constitutional Gate on Every Edge (NOT optional)

Each edge in the chain executes:
```
1. Read current state from HashedLedger (content-hashed, append-only)
2. Run Tri-Witness on transition (F3)
3. Run reversibility check (F1) — full vs partial vs irreversible
4. If risk ≥ threshold → 888_HOLD
5. Execute target node via MCP
6. Append output + HMAC receipt to HashedLedger
7. Continue to next edge
```

This is the **critical difference** from LangGraph. A LangGraph node can do anything.
An arifOS forge chain node can do only what F1–F13 permit at that position in the chain.

### Layer 3: Hashed State Ledger (not just checkpoints)

| LangGraph way | arifOS way |
|---|---|
| Dumps JSON blob to Postgres after every node | Every state transition emits a content-hashed evidence receipt (HMAC/BLAKE3) |
| Checkpoints are mutable table rows | The state is an **append-only Merkle tree** |
| node A writes → node B sees the new state | If node A claims execution, the resulting state must contain the cryptographically verified receipt of that execution |
| No cross-node provenance | Git-like lineage chain for absolute auditability (F11) |

### Layer 4: Artifact Spine (references over values)

| LangGraph way | arifOS way |
|---|---|
| Passes entire conversation history between nodes → massive token bloat | Graph passes **pointers**, not payloads |
| Context degradation as workflow grows | AAA MCP transport wire manages heavy objects (xarray/zarr for GEOX, DataFrames for WEALTH) |
| Every node sees everything | Nodes pass URIs + validation hashes → execution loop stays lightweight (ΔS < 0) |

### Layer 5: Proxy Tooling (dual-control verification)

| LangGraph way | arifOS way |
|---|---|
| Binds Python functions directly to agent nodes | Agents do NOT execute tools directly |
| No verification that the tool actually did what it claimed | Execution shell proxies calls via MCP layer |
| False-success defect: node claims success, graph trusts it | Node requests → MCP executes → independent verifier confirms outcome before graph proceeds |

### Layer 6: Multi-Agent Supervisor (Governed)

```
Supervisor Node (arif_judge mode=intercept)
  → routes to subchain via arif_route
  → each subchain has its own F1–F13 gate
  → subchains return receipts, not opinions
  → supervisor collates, judges, merges via tri-witness (F3)
```

LangGraph's supervisor delegates then trusts the result.
arifOS supervisor delegates through `arif_judge`, each subchain is constitutionally bounded,
and receipts are cross-verified.

---

## 4. Python-First vs Rust

| Criterion | Python (+ fastmcp) | Rust (native binary) |
|---|---|---|
| **State machine determinism** | Good — async runtime, but GIL limits parallel nodes within a superstep | ✅ Excellent — no GC, true parallel, deterministic channels |
| **Hashed state ledger** | `blake3` bindings exist, but Python dict overhead per step | ✅ Native — zero-copy serialize, SIMD blake3 |
| **Checkpoint I/O** | `asyncpg` to Postgres — has latency tail | ✅ tokio + pgx — lower variance, batch writes |
| **Integration with existing kernel** | ✅ Trivial — import as module, share fastmcp | ⛔ Bridge needed — NATS or subprocess IPC |
| **Deadlock prevention** | Python asyncio — bounded | ✅ Rust type system — Send/Sync + channels |
| **Time to first forge chain** | ✅ Days — wrap existing interceptor | ⛔ Weeks — build IPC, serialization, auth bridge |
| **Memory safety** | OK — but tools.py is 24K lines | ✅ Guaranteed — no buffer overflow in state serialization |
| **Concurrent node execution** | GIL-bound | ✅ rayon/async for true parallel BSP |

### Recommendation: Python first, Rust hot-path later

Reason: The constitutional interceptor IS the bottleneck, and it's already in Python.
Writing the chain engine in Python means:
1. Reuse `forge_preflight.py` directly (all 12 stages)
2. Call the interceptor from every edge — not bridge it over IPC
3. Ship in days, not weeks

The Rust version becomes necessary when:
- Sub-millisecond edge routing is needed (currently not a bottleneck)
- Parallel nodes execute within the same superstep (GIL-bound in Python)
- The chain engine becomes a standalone service on a separate core

---

## 5. Key Invariant: Constitution-before-Topology

LangGraph's invariant: **State is typed. Topology is programmable. Governance is prompt-level.**
arifOS's new invariant: **Constitution is a property of every edge, not every workflow. Topology is programmable within constitutionally bounded regions.**

This means: instead of writing "generate → evaluate → regenerate → judge" from scratch
every time (LangGraph's burden), you declare **"I need a bounded self-improvement loop"**
and arifOS gives you one that's already F1–F13 gated, checkpointed, and seal-chain anchored.

---

## 6. Langfuse → Kabarkan Pattern (same logic)

LangGraph is to execution graphs what Langfuse is to observability:
- Both are **infrastructure layers** that assume the agent is the problem
- Both are **constitutionally neutral** — they don't care WHAT the agent decides, only THAT it executed
- Both can be replaced by absorbing their invariants into the constitutional kernel

Kabarkan replaced Langfuse because arifOS already HAS telemetry (9-signal + VAULT999 + NATS span tree).
The forge chain engine replaces LangGraph because arifOS already HAS constitutional enforcement (F1–F13 interceptor) — it just needs a programmable graph layer on top.
