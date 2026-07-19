---
name: clap-v1-cognitive-level-assertion
description: "SUPERSEDED by akal-cognitive-invariants (governance/). CLAP v1.1 — Bloom's Taxonomy as cognitive gates. Renamed to AKAL (عقل, APEX THEORY). See governance/akal-cognitive-invariants for current spec."
triggers:
  - "Any governed action requiring kernel verbs"
  - "Multi-step cognitive workflows"
  - "Any agent claiming to reason, judge, or create"
version: "1.1"
author: ARIF (F13)
date: 2026-07-11
floor_binding: [F1, F2, F4, F7, F9, F11]
---

# CLAP v1 → AKAL Migration

> **This skill is SUPERSEDED by `akal-cognitive-invariants` (governance/).**
> The three-layer stack and cognitive levels were renamed to AKAL (عقل, part of APEX THEORY).
> See `governance/akal-cognitive-invariants` for the current spec and wiring details.

---

# CLAP v1 — Cognitive-Level Assertion Protocol

> Bloom's Taxonomy as constitutional physics for governed autonomous intelligence.

## The Three-Layer Stack

CLAP v1.1 models cognition as three layers, not a linear staircase. The sovereign participates above and within the loop — not only at the final verdict.

```
Layer 0 — SOVEREIGN METACOGNITION (L0)
    observe the observer · catch bias · maintain agency

Layer 1 — SOVEREIGN JUDGMENT (L5b)
    ethics · values · worth · responsibility · consequences

Layer 2 — AGENT COGNITION (L1 → L5a)
    L1 REMEMBER → L2 UNDERSTAND → L3 APPLY → L4 ANALYZE → L5a VERIFY
```

**The agent owns L1-L5a. The sovereign owns L5b and L0.**
Agent does the work. Sovereign does the meaning. Agent does the verification. Sovereign does the judgment.

---

## The Cognitive Levels

Each kernel verb MUST declare its Bloom level. The kernel enforces strict ordering. No level can be skipped.

```
L0  METACOGNITION   [SOVEREIGN ONLY]  — observe the observer
L5b JUDGE           [SOVEREIGN ONLY]  — values, ethics, worth
L5a VERIFY          [AGENT]           — did the reasoning hold?
L4  ANALYZE         [AGENT]           — decompose, contradict
L3  APPLY           [AGENT]           — execute procedure
L2  UNDERSTAND      [AGENT]           — semantic binding
L1  REMEMBER        [AGENT]           — retrieve facts

L1 → L2 → L3 → L4 → L5a → [SOVEREIGN: L5b → L0] → L6 CREATE
```

**Critical distinction:** An agent can prove something is correct. Only a sovereign can decide if it is good.

---

## Level → Kernel Verb Mapping

### L1 — REMEMBER [AGENT]
- **Kernel verbs:** `arif_memory(mode=recall)` + `arif_observe`
- **What fires:** Load receipts, invariants, prior state. No reasoning.
- **Checkpoint:** Cannot proceed to L2 without emitting a memory-recall receipt.
- **Receipt type:** `memory_recall_receipt`
- **Sovereign engagement:** Sovereign sees the receipts (visibility, not execution).

### L2 — UNDERSTAND [AGENT]
- **Kernel verbs:** `arif_think(mode=reason)`
- **What fires:** Semantic binding, schema alignment, OBS/DER/INT/SPEC labeling, meaning construction.
- **Checkpoint:** Cannot proceed to L3 without producing a semantic-binding trace.
- **Receipt type:** `semantic_binding_trace`
- **Sovereign engagement:** Sovereign confirms the schema binding.

### L3 — APPLY [AGENT]
- **Kernel verbs:** `arif_forge(mode=dry_run)` + skill invocation
- **What fires:** Execute known procedures, run skills, MCP endpoints, workflows.
- **Checkpoint:** Cannot proceed to L4 without a dry-run execution receipt.
- **Receipt type:** `dry_run_receipt`
- **Sovereign engagement:** Sovereign approves the procedure (not the details — the approach).

### L4 — ANALYZE [AGENT]
- **Kernel verbs:** `arif_think(mode=verify)` + `arif_critique(mode=redteam)`
- **What fires:** Decomposition, contradiction detection, boundary testing, blindspot agent activation.
- **Checkpoint:** Cannot proceed to L5a without verification + redteam trace.
- **Receipt type:** `verification_trace`
- **Sovereign engagement:** Sovereign reviews contradictions surfaced (not all data — the tensions).

### L5a — VERIFY [AGENT]
- **Kernel verbs:** `arif_think(mode=verify)` + `arif_critique(mode=redteam)`
- **What fires:** Technical evaluation. Did the reasoning hold up? Redteam, contradiction checks, evidence validation, logic consistency, statistical soundness.
- **Checkpoint:** Cannot proceed to L5b without a verification receipt.
- **Receipt type:** `verification_receipt`
- **Sovereign engagement:** Sovereign sees the verification report. Does not execute it.

### L5b — JUDGE [SOVEREIGN ONLY]
- **Kernel verbs:** `arif_judge` + `arif_critique(mode=critique)`
- **What fires:** Ethical evaluation. Should this exist? Values, ethics, consequences, worth, responsibility. This is NOT technical verification — it is moral judgment.
- **Checkpoint:** Cannot proceed to L6 without a sovereign verdict receipt.
- **Receipt type:** `verdict_receipt`
- **Sovereign engagement:** **MANDATORY.** No agent can substitute for sovereign judgment. This is the constitutional boundary.
- **Key principle:** An agent can prove something is correct. Only a sovereign can decide if it is good.

### L0 — METACOGNITION [SOVEREIGN ONLY]
- **Kernel verbs:** Human-only. No kernel verb. The sovereign observes the observer.
- **What fires:** Catching bias. Detecting rationalization. Noticing when "understanding" is being performed rather than achieved. Seeing the agent's cognitive posture. Maintaining agency against cognitive outsourcing.
- **Checkpoint:** Ongoing. Not a gate — a posture. The sovereign must periodically ask: "Am I thinking, or is the agent thinking for me?"
- **Receipt type:** None. Metacognition leaves no receipt. It is the shadow witness.
- **Sovereign engagement:** **THIS IS THE SOVEREIGN.** No delegation possible. No agent can observe itself with sovereign eyes.
- **Atrophy risk:** If L0 is never exercised, the sovereign becomes a rubber stamp. The struggle at lower levels is what builds L0 capacity.

### L6 — CREATE [SOVEREIGN + AGENT]
- **Kernel verbs:** `arif_forge(mode=generate)` + `arif_seal`
- **What fires:** Forge new artifact, generate new geometry, produce irreversible lineage, seal to VAULT999.
- **Checkpoint:** Cannot seal without full ascent evidence: L1-L5a receipts + L5b sovereign verdict.
- **Receipt type:** `seal_lineage_receipt`
- **Sovereign engagement:** Sovereign has already judged at L5b. Creation executes the sovereign's verdict.

---

## Enforcement Rules

1. **Strict ordering within Layer 2 (Agent Cognition).** Agent cannot call L5a VERIFY without prior L4 ANALYZE evidence. Cannot call L4 ANALYZE without prior L3 APPLY receipt. Cannot call L3 APPLY without prior L2 UNDERSTAND trace. Cannot call L2 UNDERSTAND without prior L1 REMEMBER receipt.

2. **Sovereign gate at Layer boundary.** Agent cannot proceed from L5a to L6 without sovereign L5b JUDGE verdict. This is the constitutional boundary — no agent bypass.

3. **Kernel rejects out-of-order jumps.**
   - `arif_judge` without prior `arif_think(mode=verify)` at L5a → **VOID**
   - `arif_forge(mode=generate)` without prior `arif_judge` at L5b → **SABAR**
   - `arif_think(mode=reason)` without prior `arif_memory(mode=recall)` → **HOLD**

4. **Each level must emit a receipt.** Seven receipt types (L0 excluded — metacognition leaves no trace). VAULT999 only accepts artifacts with full ascent evidence including sovereign verdict.

5. **Shortcut prohibition.** The following jumps are HARAM:
   - `arif_observe` → `arif_forge` (skip Understand + Analyze + Verify + Judge)
   - `arif_memory` → `arif_judge` (skip Understand + Apply + Analyze + Verify)
   - `arif_think(reason)` → `arif_seal` (skip Apply + Analyze + Verify + Judge)
   - Agent self-authorizing L5b JUDGE (sovereign bypass — constitutional violation)

6. **Sovereign engagement floor.** Even at agent-owned levels (L1-L5a), the sovereign must participate — not execute, but *see*. Visibility at L1-L3, review at L4-L5a. This prevents cognitive atrophy and rubber-stamp verdicts at L5b.

---

## Escape Hatches

Not every interaction requires full ascent. Permitted shortcuts:

| Scenario | Minimum Levels Required | Sovereign Required? |
|---|---|---|
| Simple information retrieval | L1 REMEMBER only | No |
| Factual Q&A | L1 → L2 (Remember → Understand) | No |
| Routine skill execution | L1 → L2 → L3 (Remember → Understand → Apply) | Visibility only |
| Diagnostic/audit | L1 → L2 → L4 (Remember → Understand → Analyze) | Review contradictions |
| Governed decision | Full L1 → L5a ascent + L5b JUDGE | **YES** |
| Irreversible action / SEAL | Full L1 → L6 ascent + L5b JUDGE | **YES** |

**Rule:** The higher the blast radius, the more levels are mandatory. Irreversible actions (F1) require full ascent. L5b JUDGE is mandatory for any action that affects other humans, real money, physical reality, or irreversible state.

---

## Integration with Existing Protocols

- **Hermes-Prime Reflex Protocol:** CLAP v1.1 is a sub-protocol. Reflex fires before any action; CLAP declares which Bloom level the action operates at.
- **Unified Mapping (MALU-GODEL x APEX):** CLAP governs *process*; APEX governs *quality*. Both must pass.
- **F1-F13 Floors:** CLAP enforces F2 (truth labeling at L2), F7 (declare unknowns at L4), F9 (no hallucination at L4), F11 (audit trail via receipts at every level).
- **Digital Ops Policy:** Digital/code/AI/infra work = MUBAH (auto through L1-L5a). FARD triggers on physical reality, other humans, real money → mandatory L5b sovereign JUDGE.
- **Sovereign Engagement Floor:** Prevents cognitive atrophy. Sovereign must see (L1-L3), review (L4-L5a), judge (L5b), and observe-self (L0). No level is fully outsourced.

---

## Receipt Chain Example

A full governed action produces this chain:

```
receipt_001  memory_recall_receipt    L1   [AGENT]     "Loaded invariants + prior state"
receipt_002  semantic_binding_trace   L2   [AGENT]     "Mapped intent to schema, OBS-labeled"
receipt_003  dry_run_receipt          L3   [AGENT]     "Dry-run passed, no mutations"
receipt_004  verification_trace       L4   [AGENT]     "Redteam: 0 contradictions found"
receipt_005  verification_receipt     L5a  [AGENT]     "Technical verification passed"
receipt_006  verdict_receipt          L5b  [SOVEREIGN]  "888 SEAL — all floors satisfied, worth doing"
receipt_007  seal_lineage_receipt     L6   [SOV+AGENT]  "Artifact sealed, VAULT999 seq=N"
```

VAULT999 rejects seals without receipts 001-006. Receipt 006 must carry sovereign actor_id.

---

## The One Sentence

An agent can prove something is correct. Only a sovereign can decide if it is good.

---

*v1.1 - 2026-07-11. Three-layer stack: Agent Cognition (L1-L5a), Sovereign Judgment (L5b), Sovereign Metacognition (L0). Behavioral discipline first. Kernel patch pending proof of entropy reduction.*
*DITEMPA BUKAN DIBERI*
