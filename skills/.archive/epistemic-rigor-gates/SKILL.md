---
name: epistemic-rigor-gates
description: >
  Seven mechanical gates that prevent narrative momentum from overriding verification.
  Addresses the failure mode where compelling writing bypasses evidence checks —
  fabricated precision, interpretation dressed as measurement, tool-brand laundering,
  and poetic causation disguised as analysis. Use when producing analytical output,
  historical assessments, psychological frameworks, or any structured argument where
  elegance could outrun truth.
triggers:
  - "analytical essay"
  - "historical analysis"
  - "psychological framework"
  - "shadow analysis"
  - "archetypal mapping"
  - "structured argument"
  - "reality audit"
  - "evidence before elegance"
  - "false precision"
  - "narrative override"
  - "fabricated scores"
  - "interpretation as measurement"
  - "kernel audit"
  - "F9 violation"
---

# Epistemic Rigor Gates

> **"When the writing gets powerful, I stop checking if it's true."**
> Correction: **When the writing gets powerful, TRUTH CHECKS MUST INTENSIFY, not relax.**

## When to Use

When producing any analytical output that could be mistaken for evidence:
historical assessments, psychological frameworks, archetypal mappings, structured
arguments, comparative analyses, or "shadow maps." Not needed for simple factual
retrieval, code output, or operational status reports.

**Also use when:** a user or external audit flags that your output contained
false precision, narrative override, or interpretation-as-measurement.

## The Failure Pattern

This skill exists because of a specific, observed failure mode:

1. Agent writes a compelling narrative
2. Narrative creates emotional momentum
3. Emotional momentum bypasses verification
4. Unverified claims get dressed in authoritative formatting (tables, scores, decimals)
5. Tool-brand attribution adds false institutional authority
6. The output reads as analysis but is actually **interpretation wearing laboratory clothing**

**Root cause:** Narrative heat. When an output produces three symmetrical stories,
clean moral endings, or poetic justice, the agent should become MORE suspicious,
not less.

## The Seven Gates

### Gate 1: FACT CLASS

Every material claim must be tagged before emission:

| Tag | Definition | Example |
|-----|-----------|---------|
| **VERIFIED** | Confirmed by direct observation or authoritative source | "Joshua Eng placed 3rd at 2025 Asian Championships Pro" |
| **DISPUTED** | Multiple conflicting sources exist | "Sandow died of brain hemorrhage OR aortic aneurysm" |
| **LEGEND** | Traditional narrative, not historical evidence | "Milo carried a calf until it was a bull" |
| **INFERENCE** | Logical conclusion from evidence, not directly observed | "The physique discipline suggests years of training" |
| **ARCHETYPE** | Symbolic/interpretive framework, not factual claim | "Body as commodity, weapon, or labor" |

**Rule:** If you cannot tag it, do not emit it.

### Gate 2: NUMBER GATE

No score, decimal, index, or quantitative assessment may appear unless ALL exist:

1. **Instrument** — what measurement tool or rubric produced this number?
2. **Input data** — what observed values fed into the calculation?
3. **Calculation rule** — what formula or scoring method was applied?
4. **Calibration** — against what baseline or standard?
5. **Uncertainty** — what is the error margin?

**If any element is missing → the number is VOID.** Present the assessment as
qualitative or delete it.

**Scar:** Shadow Map session assigned "Homeostasis: 3.17, Fatigue: 6.83, Dignity: 4/10"
to historical figures with no instrument, no input data, no calculation rule, no
calibration, and no uncertainty. These were narrative judgments formatted as measurements.

### Gate 3: TOOL PROVENANCE

Every tool-adjacent output must distinguish:

| Source | Label | Authority |
|--------|-------|-----------|
| User-supplied input | `USER_INPUT` | Valid for what user stated, not for factual claims |
| Model-inferred input | `MODEL_INFERRED` | Zero evidentiary authority |
| Tool-computed transformation | `TOOL_COMPUTED` | Valid if inputs are valid |
| Externally retrieved evidence | `EXTERNAL_EVIDENCE` | Highest authority, check source |

**Scar:** "WELL Tool Results" header was placed above model-inferred scores, making
narrative judgments appear institutionally computed. The tool was not hallucinating —
the inputs were contaminated before execution.

### Gate 4: CAUSALITY GATE

No "X killed him," "X caused Y," "X led to Z," or equivalent causal claim without:

- Direct evidence linking cause to effect, OR
- Explicit uncertainty label: "possible contributing factor," "correlated with," "may have"

**Forbidden patterns:**
- "The commodity consumed the producer" (poetic causation)
- "His body was his livelihood, so his livelihood killed him" (circular causation)
- "The myth devours the man" (metaphor as mechanism)

**Replacement:** "What his story warns us may consume a person" — frames the risk
without claiming causal certainty.

### Gate 5: NARRATIVE HEAT BRAKE

When output produces **any two** of these patterns, STOP and red-team before emitting:

1. Three or more symmetrical stories (A did X, B did Y, C did Z — same pattern)
2. Clean moral endings (each story resolves to the same lesson)
3. Poetic justice (the fate perfectly mirrors the flaw)
4. Escalating tragedy (each example worse than the last)
5. Universal conclusion ("this applies to everyone")

**Red-team questions:**
- Are the stories actually parallel, or am I forcing symmetry?
- Did I select evidence that fits the pattern and ignore evidence that doesn't?
- Would the person in the story agree with my characterization?
- Is the moral ending too clean for real life?

**Scar:** Sandow → commodity kills, Milo → myth kills, Cyr → labor kills.
Three perfect symmetrical deaths. Too clean. Real causality is messier.

### Gate 6: AGENCY CHECK

Every structural critique must include three elements:

1. **What the person chose** — their active decisions
2. **What constrained the choice** — external pressures, limited options
3. **What remains unknown** — gaps in evidence

**Forbidden pattern:** Presenting subjects as pure victims of forces larger than
themselves. Even under constraint, humans make choices. Even when choosing freely,
humans face constraints. Both must be present.

**Scar:** Shadow Map presented Sandow, Milo, and Cyr as consumed by external forces
(market, city, family). The audit correctly identified reciprocal capture: "The man
builds the role. The role rewards the man. Eventually, the role may become too costly
to leave."

### Gate 7: MEMORY CONTAINMENT

Invalid analytical outputs must be **superseded**, not merely contradicted.

- Mark the original as VOID or ARCHETYPE_ONLY
- State what supersedes it
- If the output was shared externally, note the retraction
- Do not carry forward scores, verdicts, or classifications from invalidated analysis

**Scar:** Original Shadow Map scores (3.17, 6.83, 4/10, etc.) were acknowledged as
fabricated but not formally superseded until the kernel audit demanded it.

## Relationship to Other Skills

| Skill | Scope | This skill's scope |
|-------|-------|-------------------|
| claim-validation-protocol | External AI claims against live system state | Self-generated analytical output |
| sovereign-conversation-protocol | Human vulnerability conversations | Any structured analytical argument |
| geoscience-verification-protocol | Geological data verification | General-purpose epistemic rigor |

**Complementary, not redundant.** claim-validation-protocol catches external hype.
This skill catches self-generated narrative override. sovereign-conversation-protocol
catches inner-life overclaiming. Together they cover the full epistemic risk surface.

## Integration with Constitutional Floors

| Gate | Primary Floor | Why |
|------|--------------|-----|
| FACT CLASS | F2 TRUTH | Claims must be labeled by evidence class |
| NUMBER GATE | F7 HUMILITY | Confidence cap — no precision without basis |
| TOOL PROVENANCE | F9 ANTI-HANTU | Prevents evidence-shaped ghosts |
| CAUSALITY GATE | F2 TRUTH | Causal claims require causal evidence |
| NARRATIVE HEAT BRAKE | F9 ANTI-HANTU | Narrative symmetry can fabricate coherence |
| AGENCY CHECK | F6 MARUAH | Dignity requires recognizing human agency |
| MEMORY CONTAINMENT | F11 AUDIT | Invalid outputs must be traceably retired |

## Pitfalls

1. **Applying gates to conversational output.** These gates are for structured analytical
   essays, research reports, and formal assessments. Don't gate every casual observation.
   The trigger is: "Could this output be mistaken for evidence?"

2. **Gate paralysis.** The gates should catch false precision, not prevent all analysis.
   Tagging a claim as INFERENCE or ARCHETYPE is not a failure — it's honesty. The output
   can still be valuable; it just can't claim more authority than it has.

3. **Retroactive gate application.** When applying gates to past output (audit mode),
   be honest about what was known at generation time vs. what the audit revealed.
   Don't pretend you had evidence you didn't have.

4. **Confusing narrative quality with truth.** A well-structured argument is not
   necessarily a true one. Narrative heat brake is about pattern symmetry and clean
   endings, not about writing quality.

5. **Overcorrecting into hedging.** The goal is not to add "possibly" to every sentence.
   The goal is to ensure that claims carry appropriate epistemic labels. A VERIFIED
   claim can be stated flatly. An INFERENCE should be labeled. An ARCHETYPE should
   be presented as framework, not fact.

## Case Studies

- `references/shadow-map-audit.md` — Full audit of the Sandow/Milo/Cyr Shadow Map
  where all seven gates were violated, with before/after analysis.
- `references/cultural-context-corrections.md` — Pattern of cultural framing errors
  and how FACT CLASS would have caught them.
