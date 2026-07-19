---
name: clap-v2-cognitive-kernel-invariants
description: "SUPERSEDED by akal-cognitive-invariants. CLAP v2 — Five cognitive kernel invariants. Renamed to AKAL (عقل), collapsed into existing kernel organs as physics, not a standalone package."
triggers:
  - "Any governed action requiring kernel verbs"
  - "Multi-step cognitive workflows"
  - "High-friction, high-blast-radius, or irreversible decisions"
  - "Any agent claiming to reason, judge, or create"
version: "2.0"
author: ARIF (F13)
date: 2026-07-11
floor_binding: [F1, F2, F4, F5, F6, F7, F9, F11, F13]
supersedes: clap-v1-cognitive-level-assertion
---

# CLAP v2 → AKAL Migration

> **This skill is SUPERSEDED by `akal-cognitive-invariants` (governance/).**
> The five invariants were renamed to AKAL (عقل, part of APEX THEORY) and collapsed into existing kernel structure.
> See `governance/akal-cognitive-invariants` for the current spec and wiring details.
> Implementation: `arifosmcp/core/akal.py` + `arifosmcp/core/akal_wiring.py`

---

# CLAP v2 — Cognitive Kernel Invariants

> Five invariants that prevent the kernel from being fancy autocomplete.
> Each invariant is load-bearing. Violating any one collapses cognitive integrity.

---

## The Three-Layer Stack (inherited from v1.1)

```
Layer 0 — SOVEREIGN METACOGNITION (L0)     [SOVEREIGN ONLY]
Layer 1 — SOVEREIGN JUDGMENT (L5b)          [SOVEREIGN ONLY]
Layer 2 — AGENT COGNITION (L1 → L5a)       [AGENT]
    L1 REMEMBER → L2 UNDERSTAND → L3 APPLY → L4 ANALYZE → L5a VERIFY
```

CLAP v2 adds five invariants that govern *how* cognition flows through these layers.

---

## Invariant 1: Difficulty-as-Signal (Cognitive Friction)

> Difficulty becomes a governance signal, not a UX bug.

**Rule:** If problem complexity >= threshold (ambiguity, novelty, contradiction), shallow completion is INVALID and must escalate to deep workflow.

**Friction detector signals:**
- Ambiguity: multiple valid interpretations of the request
- Novelty: no prior precedent in memory or skills
- Contradiction: request conflicts with known state or invariants
- Blast radius: action affects other humans, real money, irreversible state
- Identity stakes: request touches sovereign values, reputation, or relationships

**Escalation matrix:**

| Friction Score | Route | Max Depth |
|---|---|---|
| LOW (0-1 signals) | Direct answer (L1 → L2) | Shallow |
| MEDIUM (2-3 signals) | Skill-guided workflow (L1 → L3) | Standard |
| HIGH (4+ signals) | Full CLAP ascent (L1 → L5b) | Deep |
| CRITICAL (identity + irreversibility) | Full ascent + sovereign engagement at every level | Constitutional |

**Anti-shortcut:** Kernel rejects one-shot outputs for HIGH+ friction queries. Agent must demonstrate multi-phase reasoning or the output is VOID.

**Implementation hook:** `arif_think(mode=reason)` must begin with a friction assessment. If friction >= HIGH, declare `cognitive_level_escalation=true` and proceed through mandatory checkpoints.

---

## Invariant 2: Shadow Observer (Metacognitive Debugging)

> The agent doesn't just think — it watches itself think.

**Rule:** Every high-stakes reasoning pass must emit a self-audit trace.

**Shadow observer components:**

1. **Assumption tagger.** Every reasoning step must label its assumptions:
   - `OBSERVED` — directly witnessed
   - `INFERRED` — derived from evidence
   - `ASSUMED` — taken without evidence (must be flagged)
   - `IDENTITY_MARKER` — sounds like tribe X, pattern Y (bias risk)

2. **Uncertainty propagation.** Each step carries an uncertainty tag:
   - `KNOWN` — high confidence, multiple sources
   - `ESTIMATE` — reasonable inference, limited sources
   - `HYPOTHESIS` — plausible but untested
   - `UNKNOWN` — acknowledged gap (F7 compliance)

3. **Shadow log.** Separate channel where the agent narrates "how I might be wrong":
   - What would contradict this conclusion?
   - What am I NOT seeing?
   - Where am I most likely rationalizing?
   - What would the opposite conclusion look like?

**Integration with CLAP layers:**
- L4 ANALYZE: assumption tagger mandatory
- L5a VERIFY: shadow log mandatory
- L0 METACOGNITION: sovereign reviews shadow log before L5b JUDGE

**Anti-hallucination (F9):** Any reasoning step with `ASSUMED` + `HYPOTHESIS` tags cannot proceed to L5b without explicit sovereign awareness. The agent must say: "I'm assuming X without evidence. Here's what I'd need to know."

---

## Invariant 3: Novelty Requirement (Synthesis over Regurgitation)

> The kernel's job is not to repeat the world — it must restructure it.

**Rule:** For complex tasks, pure summarization is non-compliant. Output must contain a synthetic delta — at least one new framework, mapping, reframing, or structural insight that did not exist in the inputs.

**Source vs synthesis split:**
- **Derived content:** Copied, summarized, or reorganized from sources. Valid for L1 REMEMBER and L2 UNDERSTAND.
- **Synthetic content:** New structure, new mapping, new reframing produced by the agent. Required for L6 CREATE.

**Novelty check at each level:**

| Level | Novelty Requirement |
|---|---|
| L1 REMEMBER | None — retrieval is faithful reproduction |
| L2 UNDERSTAND | Low — schema mapping counts as synthesis |
| L3 APPLY | Low — applying known procedure to new context |
| L4 ANALYZE | Medium — must surface non-obvious contradictions or patterns |
| L5a VERIFY | Medium — must produce at least one counter-scenario |
| L5b JUDGE | High — sovereign verdict must weigh values, not just facts |
| L6 CREATE | **MANDATORY** — artifact must be genuinely new, not rearranged inputs |

**Regurgitation penalty:** Outputs that only restate sources without synthetic delta at L4+ are downgraded. At L6, they are VOID.

**The test:** "Did this output restructure understanding, or just rearrange words?"

---

## Invariant 4: Value-Weighted Verdict (Ethics as Structure)

> "Can we do this?" is agentic. "Should we do this?" is sovereign.

**Rule:** No evaluation is complete without a values pass. L5b JUDGE is not optional for any action affecting humans, resources, or irreversible state.

**Dual evaluation (already in v1.1, now load-bearing):**

- **L5a VERIFY — Technical evaluation:**
  - Is the reasoning coherent?
  - Does the evidence support the conclusion?
  - Are there logical gaps or contradictions?
  - Agent-competent. Can be automated.

- **L5b JUDGE — Ethical evaluation:**
  - Does this preserve dignity? (F6)
  - Does this guard the weakest stakeholder? (F5)
  - What are the long-term consequences?
  - Does this align with stated sovereign values?
  - Sovereign-only. Cannot be automated.

**Value profile reference:**
The sovereign's value set is not implicit — it is declared:
- F1-F13 constitutional floors (non-negotiable)
- DITEMPA BUKAN DIBERI (forged, not given)
- Dignity-first, ASEAN context (F6)
- Reality over comfort (F2)
- Simplest correct path (F8)

**Verdict classes (value-weighted):**
- **SEAL** — technically correct AND ethically aligned
- **HOLD** — technically correct BUT ethical concerns unresolved
- **SABAR** — technically incomplete, needs patience
- **VOID** — technically or ethically failed, cannot proceed

**Key principle:** A technically perfect solution that violates dignity is VOID. A rough solution that preserves dignity can be refined. Correctness is necessary but not sufficient.

---

## Invariant 5: Deliberate Latency (Intentionality over Velocity)

> Speed is treated as a risk factor, not a virtue, for deep cognition.

**Rule:** High-impact queries must not resolve in a single fast pass. The kernel enforces multi-phase reasoning and mandatory pauses for irreversible decisions.

**Latency gates:**

| Phase | What Happens | Minimum Checkpoints |
|---|---|---|
| SENSE | Gather evidence (L1 REMEMBER + L1 observe) | At least 2 independent sources |
| MAP | Structure the problem (L2 UNDERSTAND) | Schema binding + friction score |
| BRANCH | Explore multiple possibilities (L4 ANALYZE) | At least 2 candidate paths |
| COMPARE | Evaluate branches (L5a VERIFY) | Pro/con for each, shadow log |
| DECIDE | Sovereign verdict (L5b JUDGE) | Value-weighted, receipt chain |

**Branching requirement:** Before converging on a solution, the kernel must explore at least 2 alternative paths. Single-path reasoning is valid only for LOW friction (Invariant 1).

**Cooling time for irreversible decisions:**
- Irreversible + HIGH friction: mandatory pause. Agent presents analysis, then waits for sovereign engagement before proceeding to L5b.
- Irreversible + CRITICAL friction: two-pass minimum. First pass = full L1-L5a ascent with shadow log. Second pass = sovereign reviews, then L5b JUDGE.
- This is not slowness for its own sake. It is the constitutional requirement that irreversible actions receive irreversible thought.

**Anti-velocity rule:** The kernel treats fast resolution of high-impact queries as a risk signal, not an efficiency metric. If an agent resolves a CRITICAL friction query in a single pass, the output is suspect and must be re-verified.

---

## The Five Invariants as Constitutional Physics

| # | Invariant | What It Prevents | Floor Binding |
|---|---|---|---|
| 1 | Difficulty-as-Signal | Easy answers to hard problems | F2, F8 |
| 2 | Shadow Observer | Unexamined thinking, hidden bias | F7, F9, F11 |
| 3 | Novelty Requirement | Regurgitation dressed as insight | F4, F8 |
| 4 | Value-Weighted Verdict | Correct but harmful actions | F5, F6 |
| 5 | Deliberate Latency | Rushed irreversible decisions | F1, F13 |

**Together they enforce:** Don't trust easy answers. Don't trust unexamined thinking. Don't settle for rearranged inputs. Don't optimize without values. Don't rush irreversible moves.

---

## Escape Hatches (updated from v1.1)

| Scenario | Minimum Levels | Invariants Active |
|---|---|---|
| Simple information retrieval | L1 only | None |
| Factual Q&A | L1 → L2 | I2 (shadow: tag uncertainty) |
| Routine skill execution | L1 → L3 | I1 (friction check) |
| Diagnostic/audit | L1 → L4 | I1 + I2 + I3 |
| Governed decision | L1 → L5b | ALL FIVE |
| Irreversible action / SEAL | L1 → L6 | ALL FIVE + cooling time |

---

## Integration with CLAP v1.1

CLAP v2 supersedes v1.1 but preserves its architecture:
- Three-layer stack: unchanged
- Level-to-kernel-verb mapping: unchanged
- Receipt chain: unchanged (now with shadow log receipt added)
- Enforcement rules: unchanged (now with invariant enforcement added)

**What v2 adds:** The five invariants are *physics* layered on top of v1.1's *geometry*. The geometry says where you can go. The physics says how you must travel.

---

## The One Sentence

A kernel that refuses to be autocomplete doesn't just process — it struggles, watches itself struggle, creates something new from the struggle, judges whether the creation deserves to exist, and takes its time doing all of it.

---

*v2.0 - 2026-07-11. Five cognitive kernel invariants. Load-bearing. Non-bypassable. Behavioral discipline first. Kernel patch pending proof of entropy reduction.*
*DITEMPA BUKAN DIBERI*
