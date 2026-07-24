## DAG Cognition Model — Tri-Layer Architecture (FORGED 2026-07-20)

> **Ontological Baseline:** Agent cognition is NOT a mutable table of facts; it is
> an immutable Directed Acyclic Graph of decisions. This is a structural extension
> to primitives 4 (Memory), 5 (State), and the Truth plane.

**Source:** Reddit r/AgentsOfAI post by u/Square_Light1441 — "I stopped building a database
for my AI agents and just used git" — synthesised with arifOS constitutional constraints
by Arif + Hermes-Prime.

### The Three Layers

| Layer | Role | Stores | Mutable? | arifOS Mapping |
|-------|------|--------|----------|---------------|
| **1 — Execution DAG** | State space | Full execution trails (every turn as a commit, every subagent as a branch) | Yes (rewindable) | A-FORGE subagent leases as branches |
| **2 — Constitutional Ledger** | Arrow of authority | Terminal SHA of subagent execution branches | No (immutable) | VAULT999 — ruling, not debate |
| **3 — Semantic Index** | Retrieval convenience | Vector embeddings derived from DAG | Disposable (rebuildable) | Derived index — never source of truth |

### Critical Boundary

Layer 1 handles **state space** (mutable, branchable, rewindable).
Layer 2 handles **authority arrow** (immutable, linear, append-only).
These govern different temporal domains — complementary, not competing.

### Subagent Pattern: Branch = Lease

- Subagent spawn = child branch off parent tip (`refs/agents/<session>/<subagent>`)
- Subagent work = commits on own branch (zero lock contention)
- Subagent completion = terminal SHA written into parent commit trailer (`Subagent-Result: <sha>`)
- No merge — SHA-linked, no merge conflicts
- The branch IS the lease — authorization + execution + audit in one DAG

### Rewind Pattern: Pointer Shift + Reversion Receipt

Layer 1 shifts head pointer to prior SHA (state mutation).
Layer 2 appends a reversion receipt (not overwriting — appending to history).
F1 satisfied: original branch and all commits after target remain reachable.
F11 satisfied: rewind event is auditable.

### F1/F2/F11 Satisfaction

| Floor | How the DAG model satisfies it |
|-------|-------------------------------|
| F1 AMANAH | Rewind = mathematical pointer shift, not data surgery |
| F2 TRUTH | Every turn = hashed, diffable, timestamped git object |
| F11 AUDIT | Every decision = signable git object with structured trailers |

### Contrast: Traditional Approaches

| Approach | What it stores | Flaw |
|----------|---------------|------|
| Vector DBs (Pinecone, Chroma) | Semantic chunks | Destroys temporal fidelity — know *what*, lose *when* and *why* |
| State blobs (Postgres, JSON) | CRUD tables | Overwriting state is destructive; rewinding requires engineering |
| DAG-as-DB (this model) | Immutable execution tree | No semantic retrieval built in — need Layer 3 |

### Implementation

Kernel module: `/root/arifOS/arifosmcp/runtime/dag_cognition.py`
- `DAGEngine` — create sessions, spawn subagents as branches, commit turns, rewind, export terminal SHA
- `DAGNode` — hashed, diffable turn with structured trailers
- `DAGSession` — session as a DAG of branches
- `TriLayerArchitecture` — boundary dataclass with integrity verification
- `SealEvidencePayload` — VAULT999 bridge: terminal SHA → linear ledger

Tests: `/root/arifOS/tests/test_dag_cognition.py` — 26 tests, all passing.

Commit: `7c7875f1f` on arifOS main (tag: `v2026.07.20`).

### When to Apply This Model

- **Use DAG-as-DB** when: debugging "why did the agent do that" requires seeing the full decision tree, not summaries
- **Use DAG branching** when: you need to explore multiple execution futures from the same past without losing any
- **Use terminal SHA sealing** when: you need VAULT999 to carry full-fidelity subagent trails without polluting the linear ledger
- **Do NOT use** when: the agent's reasoning trail has no forensic value (simple lookups, deterministic transforms)
