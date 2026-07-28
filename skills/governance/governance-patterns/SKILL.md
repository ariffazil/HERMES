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
