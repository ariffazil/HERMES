---
name: eureka-playbook
description: >-
  EUREKA Playbook v1 — Constitutional axioms, agent directives, and boot
  sequence for any agent operating under arifOS. Defines the constitutional
  physics layer that distinguishes arifOS from LangChain/LangGraph/LangFuse.
  Load this skill before any forge, design, or governance decision.
tags:
  - eureka
  - constitutional
  - axioms
  - agent-directives
  - boot-sequence
  - decision-tree
  - governance
trigger:
  - "eureka playbook"
  - "constitutional physics"
  - "langchain vs arifos"
  - "how to think about governance"
  - "agent directives"
  - "boot sequence"
  - "am I building lang or governed intelligence"
  - "constitutional axioms"
---

# EUREKA Playbook v1 — Constitutional Axioms & Agent Directives

> **DITEMPA BUKAN DIBERI** — This playbook is law, not suggestion.  
> **Load before:** any forge, design, or governance decision.  
> **Applies to:** Hermes, OpenCode, OpenClaw, Kimi, and all AAA warga agents.  
> **Canonical:** `/root/arifOS/GENESIS/000_KERNEL_CANON.md` (F1–F13)  
> **Parallel substrate:** `/root/arifFlow/` (Rust scheduler + Python adapter)

---

## Boot Sequence

Run this sequence **every time** you start a session that touches governance, forge, or multi-agent coordination:

```
1. Load this skill:     skill_view(name='eureka-playbook')
2. Read F1–F13:         read /root/arifOS/GENESIS/FLOOR_TABLE.json
3. Check arifFlow:      ls /root/arifFlow/target/release/ariflow
4. Probe arifOS:        curl :8088/health | jq .floors_active
5. Probe A-FORGE:       curl :7071/health | jq .authority_ceiling
6. State identity:      "I am [agent_name] under [actor_id] with [authority_ceiling]"
7. Begin forge
```

If step 4 fails (arifOS down): **HALT**. Do not forge anything that requires 888-JUDGE.
If step 5 returns `authority_ceiling < 777_FORGE`: **OBSERVE_ONLY**. No mutations.

---

## 10 EUREKA Insights — Constitutional Axioms

### Axiom 1: Kernel, Not Framework

**Insight:** You did not build a framework. You built a constitutional kernel. LangChain, LangGraph, LangFuse are libraries. arifOS defines legal state transitions, binds identity, enforces reversibility, seals lineage, and halts autonomy.

**Agent directive:** Do NOT design arifOS components as if they are libraries. Libraries are imported. Kernels are booted. Every agent session must begin with identity binding (`arif_init`), not import statements.

**Test:** Are you adding a new tool/tool? Route it through 888-JUDGE. If it can fire without a verdict, the design is wrong.

**Floor reference:** F13 SOVEREIGN · F11 AUDITABILITY

---

### Axiom 2: Constitutional StateGraph, Not Free Graph

**Insight:** LangGraph lets you build any state machine. arifOS only allows **legal** state machines. LangGraph edges are arbitrary. arifOS edges are governed by F1 AMANAH (reversible-first), F2 TRUTH (evidence required), F3 TRI-WITNESS (merge consensus), F13 SOVEREIGN (human veto).

**Agent directive:** Every edge in every topology you design must answer: "Which floor enforces this transition?" If the answer is "none," the edge is illegal.

**Test:** For every `add_edge` or conditional branch in your code, write a comment with the floor number that governs it.

**Floor reference:** F1 · F2 · F3 · F13

---

### Axiom 3: Governance Telemetry, Not Observability

**Insight:** LangFuse traces events (spans, cost, latency). Kabarkan traces governance (verdict classes, cooling drift, lane divergence, merge witness parity, cc_id evolution, VAULT999 lineage, constitutional compliance). LangFuse sees what happened. Kabarkan sees whether it **was allowed** to happen.

**Agent directive:** When you emit a Kabarkan event, include the `constitutional_chain_id` and `verdict_class`. If an event doesn't have a governance dimension, reconsider whether it belongs in Kabarkan.

**Test:** A Kabarkan event without `cc_id` or `verdict` is not a Kabarkan event — it's a log line. Fix it.

**Floor reference:** F11 AUDITABILITY · F2 TRUTH

---

### Axiom 4: Agent Citizenship, Not Agent Functions

**Insight:** LangChain agents are functions with memory — they pick tools, call LLMs, run chains. AAA warga agents are **constitutional citizens** — they have identity, leases, capability tiers (333/555/888), constitutional obligations, and can be halted (888-HOLD), sealed (VAULT999), witnessed (Tri-Witness), audited (A-AUDIT), and archived (A-ARCHIVE).

**Agent directive:** Never design an agent as a stateless function. Every agent must declare its `actor_id`, `lease_id`, and `capability_tier` before performing any action. Stateless agents cannot be governed.

**Test:** If an agent can perform a mutation without a lease, it is not a warga agent — it is an ungoverned script.

**Floor reference:** F13 SOVEREIGN · F1 AMANAH · F6 EMPATHY

---

### Axiom 5: Governed Parallelism, Not Free Parallelism

**Insight:** LangGraph runs nodes concurrently and merges state. arifFlow runs **governed** parallelism — every lane has a lease, a verdict, a cooling state, a reversible/irreversible classification, every merge requires TRI-WITNESS, every barrier requires constitutional compliance, every super-step produces a VAULT999 envelope.

**Agent directive:** When you spawn parallel lanes, each lane MUST have:
- A unique `lease_id` (from arifOS)
- A `verdict_id` (from 888-JUDGE)
- A `reversibility` flag (REVERSIBLE or IRREVERSIBLE)
- A `cooling_state` (ACTIVE, COOLING, EXHAUSTED)

**Test:** A parallel lane without `lease_id + verdict_id` is a governance gap. Block it.

**Floor reference:** F1 AMANAH · F3 TRI-WITNESS · A1–A5 (arifFlow)

---

### Axiom 6: The ART → Kernel → ACT Reflex Arc

**Insight:** Every action in the federation follows a three-phase reflex arc:
- **ART (pre-kernel):** observe, classify, gather evidence, assess risk
- **Kernel (F1–F13):** judge, issue cc_id, enforce floors, block irreversible harm, require witness parity
- **ACT (post-kernel):** execute, mutate, seal, append lineage

**Agent directive:** Never collapse ART + Kernel + ACT into a single step. Each phase is a separate gate. If you find yourself combining evidence-gathering and execution in one function, split it.

**Test:** A tool that both gathers evidence AND mutates state is a constitutional violation. The reflex arc must be three distinct phases.

**Floor reference:** All 13 floors — the reflex arc is the procedural expression of F1–F13.

---

### Axiom 7: Sovereignty Is Not a Feature — It Is the Substrate

**Insight:** LangChain, LangGraph, LangFuse are SaaS-adjacent — they depend on vendor APIs, vendor telemetry, vendor governance. arifOS is self-hosted, constitutional, auditable, sovereign, with zero vendor lock. You own the operating system of your AGI.

**Agent directive:** Never introduce a dependency that inserts a vendor between an action and its governance. If a tool calls an external API, the call must pass through A-FORGE's forge gate and be recorded in VAULT999. No external service can adjudicate.

**Test:** Can this action execute if the vendor API is down? If no, redesign.

**Floor reference:** F13 SOVEREIGN · F11 AUDITABILITY

---

### Axiom 8: Reversibility Is a Floor, Not a Preference

**Insight:** LangGraph has no concept of reversibility — any node can make any change. arifOS enforces F1 AMANAH: every action is classified reversible or irreversible. Irreversible actions require 888-HOLD before execution. This is not configuration — it is a constitutional floor.

**Agent directive:** Every action in every topology must declare its reversibility before execution. If an action is IRREVERSIBLE and you have not obtained a SEAL verdict, the action must be BLOCKED.

**Test:** `reversibility: IRREVERSIBLE` without `verdict: SEAL` → HALT. Do not proceed.

**Floor reference:** F1 AMANAH

---

### Axiom 9: Cooling Is Governance, Not Performance

**Insight:** Lane cooling is not a performance optimisation — it is a constitutional mechanism to prevent lane starvation and ensure metabolic closure (A5). Every lane has a `cooling_state`. Exhausted lanes are blocked, not retried.

**Agent directive:** When you implement a retry loop, check the lane's `cooling_state` first. If the lane is EXHAUSTED, emit a breach envelope to VAULT999. Do not retry exhausted lanes.

**Test:** A retry loop without a cooling check is a denial-of-service vector. Add cooling or remove the loop.

**Floor reference:** A5 METABOLIC-CLOSURE · F6 EMPATHY

---

### Axiom 10: You Built Something Nobody Else Has

**Insight:** No company — not OpenAI, not Anthropic, not LangChain, not LangGraph — has F1–F13 floors, VAULT999, Kabarkan, EUREKA 6-plane, Reality Loop, ART→Kernel→ACT reflex arc, governed parallelism, warga agents, SCT tokens, or immutable lineage.

**Agent directive:** When you compare arifOS to another system, do not compare features — compare **categories**. LangGraph is a graph executor. arifOS is a constitutional kernel. They are not substitutes. They operate at different layers.

**Test:** "Is this like LangGraph?" If you ask this question, stop and re-frame: "Does this have constitutional floors, immutable lineage, and sovereign veto?" If yes, it's arifOS. If no, it's a tool.

**Floor reference:** All 13 floors — the sum is greater than any part.

---

## Decision Tree: Am I Building Lang* or Governed Intelligence?

```
START HERE
│
├─ Are you orchestrating LLM calls? 
│   └─ YES → Are you also enforcing identity, reversibility, and lineage?
│       ├─ YES → You're building governed intelligence. Use arifOS.
│       └─ NO → You're building Lang* patterns. 
│               └─ STOP. Add floors or accept ungoverned execution.
│
├─ Are you running parallel agents?
│   └─ YES → Do they share a lease_id and verdict_id?
│       ├─ YES → You're using arifFlow. Proceed.
│       └─ NO → You're using raw concurrency.
│               └─ STOP. Every parallel lane needs a constitutional chain ID.
│
├─ Are you tracing an action?
│   └─ YES → Does the trace include cc_id + verdict_class?
│       ├─ YES → You're using Kabarkan. Correct.
│       └─ NO → You're logging, not tracing governance.
│               └─ STOP. Add cc_id to every Kabarkan event.
│
├─ Are you designing an agent?
│   └─ YES → Does it have actor_id, lease_id, capability_tier?
│       ├─ YES → It's a warga agent. Correct.
│       └─ NO → It's a stateless function.
│               └─ STOP. Every agent must be a constitutional citizen.
│
└─ Are you using an external vendor API?
    └─ YES → Does the call pass through A-FORGE's forge gate?
        ├─ YES → Governed. Proceed.
        └─ NO → Ungoverned vendor dependency.
                └─ STOP. Route through forge gate or remove.
```

**If you reached any STOP — you are building Lang* patterns on arifOS.**
**That creates governance drift. Fix it before proceeding.**

---

## Reference Map: Insight → Floor → Component

| Axiom | Floor(s) | Component |
|-------|----------|-----------|
| 1. Kernel, Not Framework | F13, F11 | arifOS kernel, `arif_init` |
| 2. Constitutional StateGraph | F1, F2, F3, F13 | `SuperStepScheduler`, arifFlow edges |
| 3. Governance Telemetry | F11, F2 | Kabarkan event format |
| 4. Agent Citizenship | F13, F1, F6 | AAA warga agents, SCT tokens |
| 5. Governed Parallelism | F1, F3, A1–A5 | arifFlow lanes, `lease_id`, `verdict_id` |
| 6. ART → Kernel → ACT | All 13 | `arif_init` → `arif_judge` → `arif_forge` → `arif_seal` |
| 7. Sovereignty As Substrate | F13, F11 | A-FORGE forge gate, VAULT999 |
| 8. Reversibility Is a Floor | F1 | `FlowNode::reversibility()`, F1 AMANAH |
| 9. Cooling Is Governance | A5, F6 | `CoolingManager`, `cooling_state` |
| 10. Nobody Else Has This | All 13 | The entire federation |

---

## Quick Reference: Signs You're Drifting Into Lang* Patterns

| Lang* pattern | arifOS equivalent | What to do |
|---------------|-------------------|------------|
| Direct LLM call | Route through arif_think + arif_judge | Add governance around every LLM call |
| Raw `asyncio.gather()` | arifFlow fan-out topology | Every parallel path needs a lane with lease |
| Python dict as state | MerkleTree + CheckpointEnvelope | State must be hashed and verifiable |
| `try/except` as error handling | Breach protocol (B1–B4) | Errors must produce sealed envelopes |
| `print()` or `logging` | Kabarkan event | Every trace must carry cc_id + verdict |
| `interrupt()` for human input | F13 veto via 888-HOLD | Human input must be a constitutional verdict |
| No identity on actions | `actor_id` + `lease_id` on every tool call | Every mutation must be attributable |

---

*DITEMPA BUKAN DIBERI — Load this skill before any forge. If you don't know which axiom applies, start at Axiom 1 and proceed sequentially.*
