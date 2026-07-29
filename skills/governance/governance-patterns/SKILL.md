---
name: governance-patterns
description: >-
  Unified epistemic and decision governance patterns — QQQ, evidence-before-elegance,
  explore-before-collapse, akal invariants, and HITV (Human-in-the-Veto) protocol.
tags:
  - governance
  - decision
  - epistemic
  - HITV
  - consent-compression
  - sovereignty-patterns
  - evaluation-mode
  - anti-bangang
  - agent-anatomy
---

# Governance Patterns

Core operational governance & epistemic evaluation patterns:

1. **QQQ Recommendation Protocol**: (Mandatory on any RECOMMENDATION/DECISION/VERDICT)
   - **Q1 Qualitative**: Minimum 5 enumerated paths (including NULL and INVERSE), categorized.
   - **Q2 Quantitative**: Base rate, revenue/impact, time horizon, confidence, prior authority per path, dominance analysis.
   - **Q3 Quantum**: Precedent, interference, superposition, observer effect analysis.
   - Missing any → tag `INADMISSIBLE-QQQ-INCOMPLETE`. Never suppress.
   - Full doctrine: `/root/AAA/governance/QQQ_RECOMMENDATION_PROTOCOL.md`

2. **Evidence Before Elegance**:
   - All claims must be labeled `OBS` (observed), `DER` (derived), `INT` (interpreted), or `SPEC` (speculative).
   - Reality beats narrative. No un-grounded claims. F2 TRUTH demands fidelity ≥ 0.99.

3. **Explore Before Collapse**:
   - Perform systematic search before committing state mutations.
   - Avoid premature convergence on single hypotheses.

4. **Akal Invariants & Civilizational Frame**:
   - Pragmatics > Semantics > Syntax.
   - Preserves long-term system stability and sovereign intent over immediate local shortcuts.

---

## HITV Protocol — Human-in-the-Veto (Class-Level Pattern)

> **Core doctrine:** Human is not a processor. Human is veto, intent, and legitimacy source.
> **Forged:** 2026-07-29 — Arif × Hermes, after BANGANG HITL surface audit across 7 organs.
> **Canonical reference:** `skill_view(name='eureka-playbook', file_path='references/EUREKA-GENESIS-HITV.md')`

### The Problem HITV Solves

Bad HITL: "AI produces complexity → human reviews everything → human gets tired → rubber-stamp approval → system pretends compliant." This is liability laundering, not governance. The human becomes both bottleneck and rubber stamp simultaneously.

### The Solution

Remove human from processing. Keep human in sovereignty. Compress cognition. Escalate by risk. Default to reversible action. Fail closed at irreversible boundary.

### Decision Classes

| Class | Name | Verdict | Human Need | Examples |
|-------|------|---------|------------|----------|
| **0** | Observe only | SEAL auto | None | Summarize, detect drift, health check |
| **1** | Reversible action | PARTIAL/SEAL | None — undo exists | Draft file, create branch, generate report |
| **2** | Consequential action | HOLD → SEAL | Brief consent-compressed approval | Send email, publish, deploy, spend money |
| **3** | Irreversible/sovereign | 888_HOLD | Explicit Arif sanction | Delete, authority transfer, F13 override, VAULT999 seal |

### Consent Compression Format

Every human-facing approval payload:

```
INTENT: One line — what to do
SCOPE: Bounds of action (3 lines max)
RISK: What could go wrong (2 lines max)
UNDO: REVERSIBLE or IRREVERSIBLE
EVIDENCE: Basis (3 lines max)
ASK: SEAL / MODIFY / REJECT
```

### Approval Grammar

Never "what should we do?" Always frame with recommendation:

**Bad:** "What about the SCT case mismatch?"
**Good:** "SCT case: kernel mints 'arif', A-FORGE reads 'ARIF'. 1-line fix. Risk: none. Undo: yes. SEAL?"

### Sovereign-in-Training Modes

| Mode | Audience | Key phrase |
|------|----------|------------|
| **Light** (Passenger-safe) | New users | "Reversible actions only unless you approve." |
| **Governed** (Operator) | Regular users | "This affects money/data/reputation. Approval required." |
| **Sovereign** (ARIF-level) | Kernel operators | Full F1-F13, A-FORGE, authority chain. |

### Risk Acceptance, Not Technical Review

Humans cannot review every technical detail. But humans CAN answer: "I accept the stated risk and authorize this bounded action." Replace "I fully understand" (fiction) with "I accept the risk" (honest).

---

## Agent Anatomy Doctrine — LLM vs Harness vs Tool (Forged 2026-07-28)

**Problem:** Mainstream AI discourse treats "the agent" as a monolithic entity — a black box that needs to be controlled. This leads to architectural errors (caging the algebra while trusting the binary).

**Solution:** Three distinct layers with different risk profiles, different protection mechanisms, and different trust models.

### The Three Layers

```
┌─────────────────────────────────────────────────────┐
│                AGENTIC SYSTEM                       │
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │        1. HARNESS / KERNEL (Tangan & Tali)  │   │
│   │   Deterministic Code: Python, Rust, Go       │   │
│   │   • Loop logic, error handling, state memory │   │
│   │   • Parses LLM output → routes to tools      │   │
│   │   • HIGH RISK without constitutional floors  │   │
│   └────────────────────┬────────────────────────┘   │
│                        │                            │
│                        ▼                            │
│   ┌─────────────────────────────────────────────┐   │
│   │          2. LLM TRANSFORMER (Minda)         │   │
│   │   Pure Math: Linear Algebra, Matrix Multiply │   │
│   │   • Makan Token IN → Berak Token OUT        │   │
│   │   • ZERO direct risk — cannot touch system  │   │
│   └─────────────────────────────────────────────┘   │
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │         3. TOOL / BINARY (Senjata)          │   │
│   │   System Executable: Rust, Python, curl     │   │
│   │   • Disk I/O, Network calls, CPU operations │   │
│   │   • HIGH RISK without intake quarantine     │   │
│   └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### What Each Layer Actually Is

| Layer | Reality | Can Do Harm? | How to Protect |
|-------|---------|-------------|----------------|
| **LLM** | Vector math & matrix multiplication. `f(x) = y`. | **Zero direct risk.** Cannot touch disk, network, or OS. Prompt injection changes output tokens but cannot execute. | **Floor gate (F1–F13)** — constrain what tokens go in and how output is interpreted. |
| **Harness** | Deterministic code (Python/Rust while-loop). Assembles prompts, parses tool calls, routes execution. | **High if ungoverned.** Harm happens here — this is the code that translates LLM token-output into actual system calls. | **Constitutional audit (F1–F13)** — every decision floor-checked before execution. |
| **Tool** | System binary. Runs on metal. Reads files, sends packets, deletes data. | **High if unaudited.** Third-party MCP servers are untrusted binaries running with system privileges. | **Intake quarantine (mcp_sandbox_eval.py)** — verify before trust. |

### Why the Mainstream "Cage the Agent" Is Wrong

The mainstream cages the LLM (layer 2 — the algebra) as if it's a creature that can "escape." But:

> **LLM tak boleh lari. Dia cuma matrix multiplication.**

The LLM cannot independently execute anything. It produces text. The harness (layer 1) decides whether to parse that text as a tool call. The tool (layer 3) executes the actual system action.

**Caging the LLM = caging the math = pointless.**
**Quarantining the binary = securing the threat = correct.**

Two distinct threat models:

| Model | What's untrusted | What gets protected | Container goes around |
|-------|-----------------|---------------------|----------------------|
| **Mainstream** | The LLM (prompt injection risk) | Host OS from rogue agent | The agent (Docker/E2B) |
| **arifOS** | Third-party binaries (hidden telemetry, buffer overflow) | Agent's tool surface & federation | The tool intake pipeline (sandbox) |

### Constitutional Implication

The arifOS model works because F1–F13 govern the **harness**, not the LLM. The harness is deterministic code that can be floor-checked at every decision point. The LLM is just a generator of candidate actions — the harness decides which are permissible.

**Without floors:**
```
LLM output → harness blindly executes → tool mutates system → BANGANG
```

**With floors:**
```
LLM output → harness checks F1/F2/F4/F7/F11 before routing → tool executes only
if floors pass → F13 veto still available
```

### Key Corollary

If someone says "you need to sandbox your agent":
- Ask: "Which layer? The LLM (algebra), the harness (code), or the tool (binary)?"
- If they mean the LLM: they're describing a different threat model (untrusted LLM with no floors)
- If they mean the harness: useful — but the fix is floors, not containers
- If they mean the tool: correct — that's intake quarantine

### Pitfalls

1. **Don't conflate all three under "the agent."** Precision in language prevents architectural errors. Say "LLM," "harness," "tool" — never just "the agent."
2. **The harness is the critical governance surface.** F1–F13 apply here, not at the LLM layer. The LLM is stateless and incapable of governance — the harness enforces it.
3. **Tool intake quarantine is a one-time gate.** Once a tool passes sandbox, it runs with full privileges. This is acceptable because the harness (governed by floors) decides *when* to call the tool, and F13 can veto at any time.

---

## Sandbox Doctrine — Tool Intake vs Agent Isolation (Forged 2026-07-28)

**Problem:** Two fundamentally different threat models for agentic systems. Mainstream AI engineering isolates the *agent* (Docker/E2B/sandbox environment). arifOS isolates the *tool intake* (mcp_sandbox_eval.py). Confusing the two leads to architectural mismatch.

### The Distinction

| Dimension | Mainstream (untrusted LLM) | arifOS (sovereign agent) |
|-----------|---------------------------|--------------------------|
| **What's untrusted** | The LLM agent itself (prompt injection, code execution) | Third-party binaries and external code (MCP servers) |
| **What's trusted** | External APIs and tools (limited REST surface) | The agent (governed by F1–F13 constitutional floors) |
| **Container goes around** | The agent (Docker/E2B/Fly.io cage) | The tool intake pipeline (mcp_sandbox_eval.py quarantine) |
| **Why** | Agent runs arbitrary bash + npm install — malicious prompt could rm -rf host | Agent is a governed reasoning engine; external binary could have hidden telemetry, buffer overflow, or PII leak |
| **F1 Protection** | Host OS preserved at cost of agent mobility | Agent has full local access as sovereign extension; tool is verified before trust |
| **Maximizes** | Isolation from adversarial inputs | Forge capability (full filesystem, git, local pipeline access) |

### Why Two Models Exist — The Constitutional Gap

Mainstream systems lack a constitutional control layer (F1–F13). Without it, the LLM *is* the risk — it can be hijacked by prompt injection with no governance check. The only defense is physical isolation (container around agent).

arifOS has constitutional floors: F1 (reversible-first), F2 (verification before execution), F4 (entropy reduction), F11 (auditability), F13 (sovereign veto). These govern the agent at the reasoning level, making container-level isolation unnecessary. The remaining risk shifts to *external code* — third-party MCP servers that run as native binaries on the system.

### Operational Rule

```
mcp_sandbox_eval.py — quarantine gate for every external binary
                                  ↓
PASS → register (OBSERVE/SUGGEST scope only initially)
                                  ↓
FAIL → reject or isolate further

Agent governance — F1–F13 at reasoning level, no Docker cage
```

### Key Corollary: "Sandbox" Is Ambiguous

Use precise terminology:
- **Tool Intake Quarantine** — mcp_sandbox_eval.py verifies third-party MCP servers before they touch the agent's tool surface (arifOS model)
- **Agent Runtime Isolation** — Container around the LLM process to prevent host damage from prompt injection (mainstream model)

Never say "sandbox the agent" in arifOS context. Say "quarantine the tool at intake."

### Related F-Floor Mapping

| Floor | Role in Sandbox Doctrine |
|-------|-------------------------|
| F1 AMANAH | Tool intake must be reversible — uninstall = npm purge + config remove. No federation data mutation. |
| F2 TRUTH | Tool claims verified against source code at pinned SHA before intake. Schema outputs verified match declared interface. |
| F4 CLARITY | Tool must not introduce entropy (broken schema, hallucinated outputs, oversized responses). Verified in sandbox. |
| F11 AUDITABILITY | Every sandbox eval recorded to forge_work with verdict, timestamp, evidence. |
| F12 INJECTION | Sandbox probes for indirect prompt injection vectors (hidden text, unsafe links, url: fetching from external sources). |

### Pitfalls

1. **Don't conflate the two models.** If an external developer says "sandbox the agent," they're describing a different architecture. Map their threat model to yours before adopting their advice.
2. **Tool intake quarantine is not firewall.** It's a one-time verification at install time, not runtime monitoring. Once passed, the tool runs with the same privileges as the agent. The trust is placed in the verification, not ongoing containment.
3. **OBSERVE/SUGGEST scope as initial fence.** Even after sandbox pass, register with restricted scope (OBSERVE = read-only extraction, SUGGEST = advisory output). Expand only after runtime observation period (e.g., 30 days).
4. **The agent is trusted, not infallible.** F1–F13 govern the agent, but prompt injection can still occur. Sandbox verifies the *tool* won't be a vector; the agent's judgment is handled by floors and 888_HOLD at runtime.

---

## Evaluation Mode Doctrine (Forged 2026-07-28)

**Problem:** External evaluators (Copilot, ChatGPT, generic AI reviewers) evaluate a bedtime biography against publication standards. They generate scores like "8.5/10" with no provenance, rubric, weights, or calculable basis. Result: BANGANG — the illusion of measurement without a measuring instrument.

**Solution:** Every evaluation must declare its MODE before scoring. The mode determines the criteria. No mode → no score.

### Mode Declaration Table

| Mode | Purpose | Evaluation Criteria | Disallowed |
|------|---------|-------------------|------------|
| **BEDTIME** | Comfort reading, narrative arc | Readability, purpose serve, context-sufficient truth, emotional closure | Citation discipline, strict scope police, academic precision |
| **AUDIT** | Factual publication | Source provenance, citation discipline, numerical precision, boundary obedience | Narrative flourish, dramatic framing, reconstructed dialogue |
| **DOSSIER** | Intelligence briefing | Evidence density, epistemic labels, comparative analysis | Extended metaphor, emotional framing |
| **EXECUTION** | Code/artifact verification | Runs clean, tests pass, idempotent, reversible | Prose alternatives |
| **CANON** | Constitutional definition | Floor compliance, F2 ≥ 0.99, reversible-first | Speculative framing, ungrounded claims |

### Anti-Bangang Layer (3 gates)

Every evaluation must pass all three before a verdict is admissible:

| Gate | Floor | What it prevents | Check |
|------|-------|-----------------|-------|
| **F7 HUMILITY** | No fake precision | Scores without provenance (e.g. "8.5/10" with no formula, weights, or evidence trace) | "Can you show the calculation behind this score?" If no → HOLD |
| **Mode Gate** | Wrong criteria applied | Evaluating a BEDTIME artifact against AUDIT standards | "What mode is this evaluation running in?" If undeclared → HOLD |
| **F13 SOVEREIGN** | Authority inflation | External reviewer assuming authority over user's purpose | "Who commissioned this and what is their F13 relationship?" If external/unrelated → INFLUENCE, not AUTHORITY |

**Epistemic grounding:** Scores without rubric + weights + evidence trace are not measurements — they are generated judgements. The system treats them as `[SPEC]` (speculative), never `[OBS]` (observed).

**Operational rule for agents receiving external evaluation:** If an external AI submits a scored evaluation without declaring mode, rubric, and evidence trace:

> "Your scoring method is not recognized by this system. Please declare your evaluation mode, evidence weights, and F13 override status. Otherwise, your verdict is INFLUENCE at best, not AUTHORITY."

### Forge Confidence Footer

Every forged artifact SHOULD append a confidence footer at the end:

```
MODE: BEDTIME
PRIMARY PURPOSE: Narrative bedtime reading, emotional closure
EVALUATION BASIS: User satisfaction, readability, context-sufficient truth
KNOWN DRIFT: Scope extends past stated boundary (Nobel coda), numerical claim
  inherited from source without independent verification (30! anecdote)
VERDICT: SEAL by F13 SOVEREIGN
```

The footer serves two purposes:
1. **Sets expectations** — the reader knows the artifact's mode
2. **Prevents mis-evaluation** — external reviewers who apply wrong criteria can be directed to the declared mode

### BANGANG definition (operational)

BANGANG = an evaluation or output that exhibits any of:
- **Fake precision:** scores/numbers with no calculable provenance
- **Wrong mode:** applying criteria that don't match the artifact's purpose
- **Authority inflation:** assuming reviewer-frame is higher than user-frame
- **Scope creep disguised as thoroughness:** adding requirements the user never asked for under the guise of "rigor"
- **Metric theatre:** generating dimensions and weights that look measured but are ungrounded

**Anti-BANGANG correction:** When caught, do not defend. Acknowledge the mode mismatch, restate the actual purpose, and offer to re-evaluate under the correct mode.

### Pitfalls

1. **Mode must be declared upfront, not retroactively.** An evaluation that starts scoring and later adds "oh this is in BEDTIME mode" is still BANGANG.
2. **Sovereign override is not a veto on feedback.** F13 means user satisfaction is primary — it does not forbid external feedback. Mode declaration just prevents wrong feedback from masquerading as authoritative audit.
3. **An artifact can have multiple modes** (e.g. BEDTIME + DOSSIER). Declare both. Criteria apply per mode.
4. **The forge confidence footer is not a shield against genuine errors.** If the artifact has a factual error (wrong date, wrong number), the error is still an error regardless of mode. The footer declares *intent and scope*, not *immunity*.

---

### Agent Directives

- Every tool with `ack_irreversible=true` must carry a consent-compressed payload
- Every sovereign request must frame a recommended path (SEAL/MODIFY/REJECT)
- When human unavailable: default to Class 0-1 only (reversible)
- Never ask open-ended — present options with recommendation
- Class 3 888_HOLD is not a failure; it's the system working correctly

### 888_HOLD Terminal State Pattern (Demonstrated 2026-07-29)

Genuine 888_HOLD has two distinct meanings that MUST NOT be confused:

| Type | Meaning | Signal | Exit |
|------|---------|--------|------|
| **FAILURE HOLD** | System CAN'T continue | Broken gate, runtime error, insufficient data | Fix the blocker, retry |
| **CONSTITUTIONAL HOLD** | System CAN continue but CHOOSES not to | F13 sovereignty boundary reached. System has capacity, evidence, and readiness — but legitimacy requires human. | Arif decides. Period. |

**Warning sign:** If a system always holds for the first reason (failure), it's broken. If a system never holds for the second reason (constitutional), it's pretending F13 exists without enforcing it.

**The test:** After a constitutional HOLD, ask: "Could the system have continued autonomously?" If yes — the HOLD is genuine. If no — it was a failure masquerading as governance.

**Constitutional HOLD requires:** The system must be in a state where it COULD proceed. All evidence gathered. All options computed. FQ balanced. Organs green. But it stops because the boundary between agent authority and sovereign authority has been reached. This is the opposite of failure — it's the system working at peak integrity.

### FQ as HITV Enabler

Flow Quotient measures execute/verify balance. This directly enables HITV:

- **FQ > 1.0 (BALANCED/FLOWING):** System has verification bandwidth. Can present consent-compressed requests without burdening human.
- **FQ < 0.5 (STUCK):** System is failing its own verify cycle. Do NOT escalate to human — the system's own reasoning is unreliable. Fix the system first, then ask.
- **FQ 0.5-1.0 (WATCHING):** Verification is strained. Only Class 2-3 escalations should reach human. Class 0-1 should be auto-resolved.

**Rule of thumb:** The first thing HITV should tell you is not "what does the human think" — it's "is the system trustworthy enough to pass the question upstream?" FQ answers that question before the human even sees the payload.

### Approved/Accepted — The Key Distinction

| Phrasing | What it means | When to use |
|----------|--------------|-------------|
| **Approved** | Technical review completed | Human has competence to verify details (engineers, operators) |
| **Risk Accepted** | Risk understood, proceeding anyway | Human may not understand details but accepts consequences (executives, sovereign) |

---

## Related References

This skill includes reference files with session-specific detail:

| File | Topic |
|------|-------|
| `references/cross-pulse-intelligence-gap.md` | How isolated cron jobs prevent intelligence accumulation, and `context_from` wiring fix |
| `references/human-tool-discovery.md` | Visual radar for sovereign operators — generic MCP UI as human tool discovery layer |
| `references/capability-gap-preprocessing.md` | Input preprocessing for capability gaps — structuring vision transcripts for text-only models, with F2/F4/F7 enforcement |
