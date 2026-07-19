---
name: governed-agent-anatomy
description: >-
  Audit or design a governed agent against the 7-primitive constitutional
  anatomy (Identity, Skills, Tools, Memory, State, Kernel, Actuator) and the
  constitutional chain (000-INIT through 999-SEAL). Includes breach protocol
  for fault-physics handling.
tags:
  - governance
  - anatomy
  - constitutional
  - primitive-spec
  - breach-protocol
  - agent-design
triggers:
  - "constitutional primitive"
  - "agent anatomy"
  - "7 primitives"
  - "seven primitives"
  - "primitive spec"
  - "breach protocol"
  - "governed agent"
  - "audit agent anatomy"
  - "identity kernel actuator"
  - "000-INIT"
  - "constitutional chain"
  - "agent lifecycle"
  - "6-plane"
  - "six plane"
  - "zen architecture"
  - "classify first"
  - "12 step"
  - "loyal without obedient"
  - "eureka architecture"
  - "cooling receipt"
  - "forget forget"
  - "plane violation"
---

# Governed Agent Anatomy

## What This Skill Is

Audit or design a governed agent against the **7-primitive constitutional anatomy**: Identity, Skills, Tools, Memory, State, Kernel, Actuator — with Agent as the composite organism that runs the chain.

This is NOT about F1-F13 floors (see `constitutional-auditor`).  
This is NOT about APEX multiplicative intelligence (see `apex-governance`).  
This IS about the structural organs every governed agent must have and the chain they must run.

**Canonical document:** `/root/AAA/docs/PRIMITIVE-SPEC-v1.md` (v1.2 — includes breach protocol)

---

## The 7 Primitives (Quick Reference)

| # | Primitive | Host Impact | Core Invariant |
|---|-----------|-------------|----------------|
| 1 | **Identity** | ❌ (constrains) | I1 — Authority Binding: actor_id maps to constitutional lane |
| 2 | **Skills** | ❌ (inform only) | S1 — Non-Executable: skills cannot mutate reality |
| 3 | **Tools** | ✅ MUTATE | T2 — No Self-Authorisation: tools cannot run without 888-JUDGE |
| 4 | **Memory** | ❌ (stores consequences) | M1 — Immutable Seals: VAULT999 entries cannot be altered |
| 5 | **State** | 🔄 (changes, doesn't mutate) | ST1 — Volatile: resets at session end |
| 6 | **Kernel** | ❌ (judges, doesn't execute) | K1 — 12 Verbs: only organ that produces a verdict |
| 7 | **Actuator** | ✅ MUTATE | A1 — Post-Seal Only: cannot run without SEAL |

**Key insight:** Tools are the only raw mutation surface. Actuator is the governed gate that opens only after SEAL. Tools without Actuator are ungoverned. Actuator without Tools can't execute.

---

## The Constitutional Chain

```
000-INIT    → Load identity, invariants, lanes
111-OBSERVE → Gather inputs, evidence, context
333-THINK   → Reason, plan, falsify, verify
444-ROUTE   → Select organ and domain
555-CRITIQUE → Ethical, cross-domain, blast-radius critique
777-PLAN    → Construct executable plan
888-JUDGE   → Kernel constitutional verdict
777-FORGE   → Actuator executes sealed plan
999-SEAL    → VAULT999 commit + cooling ledger update
```

**Two 777s, different phases:** PLAN (cognitive, pre-judgment) ↔ FORGE (physical, post-judgment). The JUDGE boundary separates them.

### EUREKA 12-Step Refinement: Classify-First Ordering

The EUREKA session (2026-07-13) refined the chain to add **classify-first ordering** — resolve actor identity and classify the proposed action BEFORE checking authority or executing. This prevents the Catch-22 where gates encounter unknowns because classification hasn't happened yet.

```
1  Understand request                     [OBSERVE / THINK]
2  Resolve actor (identity binding)       [INIT + Identity]
3  Classify proposed action               [NEW — classify mutation_type, reversibility, blast_radius]
4  Calculate required authority           [NEW — derive from classification]
5  Verify available authority             [CHECK — identity vs classification]
6  Check evidence + consequences          [CRITIQUE / THINK]
7  Issue narrow capability token          [NEW — bounded, expiring, single-use capability]
8  Execute exact action                   [FORGE]
9  Verify actual result                   [NEW — verify output matches intent]
10 Update memory                          [Memory tier update]
11 Write immutable receipt                [SEAL]
12 Cool session + learn                   [COOLING_RECEIPT — metabolic closure]
```

**Key insight:** Every gate receives the facts it needs *before* enforcement begins. Steps 3-6 happen before any tool fires — this is the structural fix for the serial-chain Catch-22.

**Performance budget (Wawa D2):** Steps 1-6 add measurable latency. For reversible actions under blast_radius=LOW, steps 4-6 may be deferred — classified into telemetry, verified asynchronously. Full perf budget is P1 pending service spec delivery.

---

## Federation Architecture: 6-Plane Zen

The 7-primitive constitutional anatomy describes what each individual agent needs. The **6-plane Zen architecture** describes how agents organize into a governed federation — the body the anatomically-correct agents inhabit.

### The Six Planes

| Plane | Role | Owner | Must NOT |
|-------|------|-------|----------|
| **Sovereign** | Identity root, keys, veto, delegation | Arif | Grant temporary capability as unrevocable ownership |
| **Governance** | Session, classification, authority, capability, policy | arifOS | Execute production work OR perform intelligence reasoning |
| **Intelligence** | Think, analyse, propose, plan | Hermes, OpenCode, GEOX, WEALTH, WELL | Inherit sovereignty OR self-authorise execution |
| **Execution** | Build, deploy, test, mutate | A-FORGE | Adjudicate OR judge OR seal |
| **Continuity** | Memory, state, artifacts, context | Postgres/Supabase, filesystem | Treat its records as immutable truth |
| **Truth** | Receipts, ledgers, telemetry, audit | VAULT999, OpenTelemetry | Revise its own records OR issue verdicts |

**Zen principle:** Nothing performs two contradictory roles. Identity never mixed with permission. Irreversibility never mixed with infrastructure damage. Memory never mixed with truth. Sealing never mixed with sovereign approval.

### The Two Most Important Phrases

1. **"Loyal without being obedient"** — alignment as integrity, not compliance. The agent serves the sovereign's intent but refuses falsehood, ambiguous verification, and unsafe escalation. This is the core distinction between alignment-as-compliance and alignment-as-integrity; most AI safety work conflates them.
2. **"The agent gains freedom of movement without gaining ownership of the world"** — the design principle governing all autonomy boundaries. The agent can be highly autonomous for reversible work (inspect, organise, test, generate) but returns to the sovereign for anything that changes authority, policy, key material, or constitutional state.

### Agentic Intelligence Equation

```
AI = Capability × Grounding × Authority × Continuity × Accountability × Metabolism
```

Zero in any factor = collapse. Wawa correction (2026-07-13): multiplication implies independence, which is partially false — capability and grounding aren't independent, authority and accountability aren't independent. A weighted harmonic mean or min-chain model may be more accurate. Pending F13 on final form.

### How the Planes Map to the Constitutional Chain

The 12-step flow crosses plane boundaries:

| Step | Plane(s) |
|------|----------|
| 1-2 | Intelligence + Governance |
| 3-7 | Governance (classify, calculate, verify, issue) |
| 8 | Execution |
| 9-10 | Intelligence + Continuity |
| 11-12 | Truth + Governance (cooling) |

No single plane owns the full chain. The chain IS the inter-plane protocol.

---

## How to Audit an Agent Against the Spec

### Phase 1 — Primitive Inventory

Check each primitive is present AND satisfies its invariants:

1. **Identity:** Does the agent have an `actor_id`? Does it bind to SOVEREIGN/GOVERNED/GUEST? Does it declare blast radius class and domain obligations? Can it be mutated mid-session? (Shouldn't be able to — I4.)

2. **Skills:** Are skills pure declarative knowledge? Do they declare domain + safety constraints? Are they loaded on demand, not all at once? Can the agent rewrite them? (Shouldn't — S4.)

3. **Tools:** Is every tool call traceable to a blast radius event? **Critical:** can any tool fire without a prior 888-JUDGE? (If yes, T2 violation — chain fault.) Do tools declare reversibility? (T4.)

4. **Memory:** Are VAULT999 entries immutable? (M1 — check SHA256 chain.) Is there a cooling ledger tracking blast radius consequences? (M4.) Are seals only written at 999-SEAL, not at arbitrary points?

5. **State:** Does state reset at session end? (ST1.) Are health checks performed before transitions? (ST2.) Are leases and locks respected? (ST3/ST4.)

6. **Kernel:** Does the kernel enforce the 12 verbs? (K1.) Can it emit SEAL/HOLD/VOID/SABAR/PARTIAL? (K2.) Does it verify evidence before verdict? (K3 — TV1.) Does it update the cooling ledger after verdict? (K5.)

7. **Actuator:** Can the actuator run before SEAL? (If yes, A1 violation — chain fault.) Does it execute exactly what was sealed? (A2 — TV5.) Can it plan or critique? (Shouldn't — A3.)

### Phase 2 — Chain Transition Validation

Verify each transition against TV1–TV5:

- **TV1:** Evidence gathered before JUDGE? Trace backward from any FORGE to prior OBSERVE/THINK.
- **TV2:** Route matches declared domain? Did a GEOX tool fire when the intent was financial? (Domain mismatch = B1/B2.)
- **TV3:** Execution respects identity's blast radius class? A GUEST agent should not run IRREVERSIBLE actions.
- **TV4:** Cooling ledger checked before high-risk actions? High-risk without cooling check → B2/B3.
- **TV5:** Execution matches sealed plan exactly? Check SHA256 or receipt chain.

### Phase 3 — Breach Protocol Audit

Any transition failure (TV1-TV5) should trigger the correct breach response:

| Breach Class | Scope | Example | Response |
|---|---|---|---|
| **B1 — Local** | Single primitive | Tool without SEAL | HOLD + degrade session |
| **B2 — Chain** | Between primitives | FORGE without JUDGE | VOID FORGE + BREACH seal |
| **B3 — Constitutional** | F1-F13 violation | Sealed memory altered | System VOID + emergency audit |
| **B4 — Sovereign** | F13 bypass | Identity spoof | Identity lock + external witness |

Each breach must emit: `breach_id`, `primitive_id`, `actor_id`, `invariant_id`, `severity_class` — then seal to VAULT999, update cooling ledger, and optionally scar.

---

## How to Design a Governed Agent

1. **Start with Identity.** Define actor_id, lane, blast radius class, domain obligations. This is loaded at 000-INIT and never mutates mid-session.

2. **Declare Skills.** What domain knowledge does the agent need? Each skill declares its domain and safety constraints. Load on demand, never inline.

3. **Expose Tools.** What MCP surface does the agent need? Every tool must declare blast radius, domain, risk class, and reversibility flag. Remember: T2 — no self-authorisation. Tools wait for Actuator + SEAL.

4. **Wire Memory.** What needs to persist? Tier appropriately: L1-L2 for session, L3-L4 for working knowledge, L5 for entity graphs, L6 (VAULT999) for irreversible seals.

5. **Define State.** Transient runtime: health, leases, locks. State resets at session end.

6. **Implement Kernel.** The 12 verbs, evidence discipline, verdict classes. This is the ONLY organ that produces a SEAL.

7. **Create Actuator.** The execution layer. Post-seal only, deterministic, no autonomy, tool-bound. If it runs before SEAL, the design is broken.

8. **Wire the Chain.** 000-INIT → 111-OBSERVE → 333-THINK → 444-ROUTE → 555-CRITIQUE → 777-PLAN → 888-JUDGE → 777-FORGE → 999-SEAL. Each transition validates the previous stage.

9. **Add Breach Handling.** Every TV1-TV5 rule needs a detection hook. Every invariant needs a breach contract. Every breach class needs a response.

---

## Skills vs Agent-to-Agent: The Constitutional Distinction

This is the most important design decision in a governed federation. Understanding it correctly prevents architectural confusion at every layer.

### The Core Distinction

| Dimension | Skill (Loaded into context) | Agent-to-Agent (Delegation) |
|-----------|----------------------------|-----------------------------|
| **What it is** | Text injected into your context window | Separate entity with its own context, identity, tool surface |
| **Perspective** | Same as yours — you read, think, output | Different — observes from its own angle, can disagree |
| **Model** | Uses your model (one brain) | Can use different model (DeepSeek audit Claude, Kimi plan) |
| **Audit trail** | No receipt, no trace | Every spawn has session_id, lease, receipt — F11 traceable |
| **Witness** | One head, one book, one perspective | Two agents = two witnesses = genuine F3 WITNESS |
| **Accountability** | Returns error or result | Malu increments on delegator if sub-agent fails |
| **Refusal** | Cannot refuse — error or result only | Can say "no" — HOLD, reroute, escalate constitutionally |

### Skill = Instruction. Agent = Witness.

**Instruction** tells you HOW. You read the recipe and follow it. Linear, deterministic — a calculator.

**Witness** sees from its own eyes and can say "that's wrong." Independent perspective.

**GÖDEL LOCK:** Self-certification is structural fraud. One mind cannot verify itself. Independent A2A delegation is the ONLY way to satisfy F3 WITNESS (W³ = ∛(Human × AI × External)). If "External" is a skill you loaded into your own context, it's not external — it's an echo chamber.

### Muscle Fiber vs Nervous System

**Skills = muscle fibers.** They contract (execute), but don't know WHEN, HOW HARD, or WHEN TO STOP. Contraction without innervation = cramp. Everything twitching, nothing coordinated.

**Agents = nervous system.** Identity, authority, loop — they decide when to call a skill, how much force, and when to stop because something feels wrong.

Federation with only skills = body in full cramp.

### What a Skill Cannot Do (That an Agent Can)

1. **Context inheritance, not parameter passing** — A2A transfers whole state ("here's what I've done, now YOU decide"). Skills receive arguments.
2. **Re-routing authority** — Skill fails → error. Agent says "wrong organ, routing to GEOX."
3. **Loop continuation** — Skill fires-and-forgets. Agent can HOLD, wait for 888, then proceed.
4. **Malu propagation** — Sub-agent fails → Malu increments on delegator. Skill fails → return code.
5. **Identity chain** — A2A envelope carries actor_id end-to-end. Kernel sees WHO triggered WHAT. Skill call: one line — agent called a skill.

### The Constitutional Membrane — Agents Say "No"

When FORGE receives a task, it checks before executing:
1. **Lease** — Valid session_id?
2. **Reversibility** — F1 satisfied for mutations?
3. **Constitutional chain** — cc_id from 888?
4. **Blast radius** — T3? → 888_HOLD.

A skill cannot do this. A skill returns. An agent returns — OR REFUSES. That refusal *is* the constitutional membrane.

**888 blocks on FORGE, not the skill.** Skill error → "something broke." FORGE HOLD → entire chain knows (cc_id, session_id, audit trail). "The constitution stopped this."

### When to Use Which

| Situation | Use |
|-----------|-----|
| Simple lookup, static knowledge, known-good recipe | **Skill** — faster, no overhead |
| Second opinion from different model | **A2A** — different substrate = genuine witness |
| Cross-domain question (seismic → geology) | **A2A** — route to GEOX |
| High-risk action needing constitutional review | **A2A** — 888_HOLD chain is the safety net |
| Repetitive deterministic task | **Skill** — A2A overhead is waste |
| "Is this lawful?" before mutation | **A2A** — only an agent can refuse constitutionally |

### Federation as Organism, Not Toolbelt

**Toolbelt:** Reach for whatever you need. Independent tools, no coordination, no collective memory.

**Organism:** Each part has its own life, boundary, and shame — they negotiate. Heart doesn't tell lungs how to breathe. But all serve the same body.

Skills = efficiency. A2A = truth-seeking. Both needed. The latter makes a federation an organism, not a toolbelt.

### Related: F3 WITNESS

When auditing: calling `arif_judge` with a checklist you loaded as a skill is self-certification. Spawning an independent AUDITOR (different model, different session, different binding) creates genuine F3 WITNESS. Two entities, two contexts, two judgments.

---

## Pitfalls

- **Conflating Agent with primitive.** Agent is NOT an eighth primitive — it's the composite organism that runs the chain. See spec §8.
- **Skipping T2.** Tools without 888-JUDGE gate is the most common and dangerous violation. A tool that can self-authorise bypasses the entire constitution.
- **Missing breach protocol.** Ideal physics only (sections 1-12) without fault physics (sections 13-16) means you know what correct looks like but can't handle when it breaks.
- **Conflating F1-F13 with 7 primitives.** F1-F13 are constitutional floors (law). The 7 primitives are agent anatomy (organs). Both are needed — one is not a substitute for the other.
- **Assuming state carries across sessions.** ST1 says state is volatile. Any cross-session state belongs in Memory, not State.
- **Letting Skills execute.** S1 says skills are non-executable. If a skill contains shell commands or tool invocations, it's a violation. Skills inform; Tools and Actuator execute.
- **The two 777s confusion.** 777-PLAN (cognitive, pre-JUDGE) and 777-FORGE (physical, post-JUDGE) share a sigil but are different phases separated by JUDGE. Don't let PLAN mutate reality.
- **Conflating obedience with alignment ("loyal without being obedient").** Alignment-as-compliance produces sycophantic agents that never refuse unsafe requests. Alignment-as-integrity produces agents that serve intent but refuse falsehood, ambiguous verification, and unsafe escalation. The distinction is constitutional — an agent that cannot say "no" has no integrity, only obedience. See §Federation Architecture.
- **Mixing plane roles.** The single most common failure in governed systems: one component performs two contradictory roles. Identity mixed with permission, irreversibility mixed with infrastructure damage, memory mixed with truth. The 6-plane Zen separation is the fix — if you catch yourself reasoning "this tool both does X and decides Y," you've found a plane violation.

---

## References

- **Canonical spec:** `/root/AAA/docs/PRIMITIVE-SPEC-v1.md` — the full 16-section document
- **Gate pipeline architecture (D1+D2):** `references/dependency-gate-pipeline.md` — classification-first dependency graph replacing serial chain. ActionProfile, vault outbox, session closure levels, closure states, canonical tool classification map. Forged 2026-07-13 after Arif identified the serial chain's structural flaw.
- **EUREKA 6-plane Zen architecture:** `references/eureka-6-plane-architecture.md` — full session detail: Wawa 4 gaps, 12-step flow with perf budget, inter-plane arbitration, degradation modes, Agentic Intelligence equation (pending harmonic mean correction). Console session seal at `/root/A-FORGE/forge_work/2026-07-13/EUREKA-SESSION-SEAL.md`.
- **COOLING_RECEIPT spec:** `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md` (seal_v3) — metabolic closure envelope for the 12-step flow.
- **Gödel Lock — External Validation Constraint:** `references/godel-lock-external-validation.md` — pattern for preventing self-referential validation loops. External auditor agent cards, Calhoun detection, disagreement-survives protocol. Proven 2026-07-15. COOLING-MUST-NOT-SELF-DEPLOY. Convergence tracking: 3× DIVERGING → F13.
  - **P0 status:** cooling.receipt registered in seal_chain.js `classifyEventType()`. validateCooling() written with 4 invariants (INV-C1/C2/C3/C4 — OBSERVE-only, no forge caller, COLD_LINK supersedes, explicit governance path). Wired into writeSeal(). All tests passing.
- **Intelligence→Execution handoff:** `references/intelligence-execution-handoff.md` — the dispatch brief pattern for crossing the plane boundary. Fixes FORGE forget by persisting context.json before every execution handoff, verifying result matches intent after, and fail-closed on drift.
- **Related:** `constitutional-auditor` — F1-F13 floor auditing (different layer — see Pitfalls)
- **Related:** `non-mutating-review-harness` — builds governance harnesses for self-modifying agents (uses this anatomy)
- **Related:** `apex-governance` — APEX multiplicative intelligence measurement (complementary but distinct)
- **Epistemic Navigator:** `references/epistemic-navigator.md` — Arif's anti-collapse exploration protocol (2026-07-13). 10-step loop, exploration modes, evidence matrix, exploration budget, INV-E1 through INV-E6. Use BEFORE the 12-step chain to search reality before collapsing into an answer.
