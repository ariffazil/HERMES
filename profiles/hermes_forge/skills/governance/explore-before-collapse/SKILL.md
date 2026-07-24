---
name: explore-before-collapse
description: >
  The Epistemic Navigator — prevent premature conclusion by exploring
  evidence space before acting. 10-step epistemic loop (ORIENT→DECOMPOSE→MAP
  →SEARCH→MEASURE→CONTRAST→TEST→EVALUATE→DECIDE→RECORD), 7 exploration modes
  (scout/mapper/driller/surveyor/contrarian/verifier/eureka), evidence
  registry mapping, exploration budget B=S×U×I×V, evidence scoring
  E=C×Q×F×I×R, and 6 constitutional invariants (INV-E1 through E6).
version: 1.0.0
tags: [governance, epistemology, exploration, evidence, anti-collapse, f2, f7, f8, f9]
metadata:
  hermes:
    category: governance
    related_skills:
      - evidence-before-elegance
      - hermes-prime-reflex-v2
      - cognitive-commands
    origin: eureka_2026-07-13
    floors_protected: [F2, F7, F8, F9]
triggers:
  - explore before collapse
  - epistemic navigator
  - premature conclusion
  - evidence search
  - exploration budget
  - scout mode
  - contrarian
  - evidence matrix
  - INV-E1
  - anti-collapse
  - "what do I know and what don't I know"
  - orient decompose map
  - collapse too early
  - evidence registry
  - sufficient exploration
  - epistemic state ladder
  - competing hypotheses
---
# Explore Before Collapse — The Epistemic Navigator

> **"An agent collapses too early when it converts uncertainty into one answer
> before exploring the relevant possibility space."** — Arif, 2026-07-13

## When to Use

Always. This is the universal operating loop that runs BEFORE the action loop.

Apply when:
- You are asked a question that requires evidence
- You are about to act (even a reversible action)
- You are diagnosing a failure
- You are making a recommendation
- You feel the urge to answer from existing knowledge without checking
- Memory contains a potentially stale fact about the subject
- A single search, tool call, or file read produced a candidate answer

Do NOT apply when:
- Someone said "hello" or "how are you"
- The task is purely creative (poem, art, brainstorm — no truth claim)
- The task is explicitly conversational with no epistemic stakes

---

## The Anti-Collapse Loop (10 Steps)

```
ORIENT → DECOMPOSE → MAP → SEARCH → MEASURE → CONTRAST → TEST → EVALUATE → DECIDE → RECORD
```

### 1. ORIENT — What kind of problem is this?

Before searching, classify the request:

| Question | Diagnosis |
|----------|-----------|
| Factual, diagnostic, strategic, creative, operational? | Determines evidence depth |
| Current or historical? | Freshness requirement |
| Reversible? | Exploration budget ceiling |
| High-stakes? | Minimum evidence floor |
| Requires files, telemetry, web, DB, or human judgment? | Evidence surface selection |
| What would a wrong answer damage? | Consequence weighting |

**Output:**
```
problem_class: <class>
stakes: <low | medium | high | critical>
freshness_required: <live | today | this_week | any>
reversibility: <reversible | irreversible>
evidence_floor: <none | one_source | independent_verify>
```

A wording request needs almost no exploration.
A production failure or financial decision needs deep exploration.

### 2. DECOMPOSE — What must be known?

Break the question into subquestions. Each subquestion should be independently answerable.

**Example — "Why is arif_seal failing?"**

Decompose into:
- Is the intended source patch present?
- Which code is actually imported?
- Which session is active?
- What authority was calculated?
- Which gate blocked?
- What action classification was used?
- Is VAULT999 healthy?
- Did the request possess a valid capability?

Without decomposition, agents repeatedly search the same surface and think they explored deeply.

**Rule of thumb:** If you can't generate at least 3 subquestions, the decomposition is shallow.

### 3. MAP — Where could the answer exist?

For each subquestion, identify which evidence surface(s) can answer it.

| Question Type | Where to Look |
|---------------|---------------|
| Current runtime | Process, import path, service unit, health endpoint |
| Source truth | Git repo, commit, diff, tests |
| Database state | PostgreSQL/Supabase query |
| Memory state | Canonical memory store + provenance |
| Historical action | VAULT999 seal chain and ledgers |
| Tool behaviour | Tool registry, schema, source, logs |
| External fact | Current authoritative web source |
| Human intent | Current authenticated session |
| Infrastructure | Telemetry, CPU, disk, network, systemd |
| Domain conclusion | GEOX, WEALTH, or WELL evidence |

**The evidence registry** (`/root/AAA/docs/evidence-registry.json`) contains 22 registered sources with:
- `source_id` — canonical name
- `source_type` — live_system, version_control, immutable_ledger, etc.
- `owner` — which plane/organ
- `questions_answered` — what this surface can tell you
- `access_method` — how to query it
- `freshness`, `reliability`, `limitations`

**Rule:** Do not search the web for a local runtime problem. Do not inspect memory for current production truth.

### 4. SEARCH (via 7 exploration modes)

Select an exploration mode based on what you've determined so far:

#### Scout — Fast, broad discovery
**When:** Problem space unknown. Need to find candidate locations.
**Sources:** filesystem_probe, tool_registry_surface, a2a_agent_registry, web_external_search
**Cost:** Low
**Stopping condition:** All candidate locations identified.

#### Mapper — Build relationships
**When:** Need to understand dependencies, data flow, ownership.
**Sources:** config_settings, systemd_service_manifest, git_source_truth, a2a_agent_registry
**Cost:** Low-moderate
**Stopping condition:** Dependency graph sufficient to locate root cause.

#### Driller — Deep inspection of one path
**When:** Candidate location identified.
**Sources:** filesystem_probe, runtime_import_probe, postgresql_database, log_stream, git_source_truth
**Cost:** Moderate
**Stopping condition:** Evidence extracted or path proven wrong.

#### Surveyor — Measure the system
**When:** Need quantitative assessment: counts, rates, drift, completeness.
**Sources:** telemetry_metrics, log_stream, vault999_seal_chain, health_endpoint, runtime_verify_tool
**Cost:** Low-moderate
**Stopping condition:** All critical measurements collected.

#### Contrarian — Seek disconfirming evidence
**When:** Leading explanation exists. Must test if it's wrong.
**Sources:** filesystem_probe, log_stream, vault999_seal_chain, memory_canonical_store, web_external_search
**Cost:** Moderate
**Stopping condition:** Counterevidence found OR all alternative hypotheses exhausted.

#### Verifier — Reproduce claim independently
**When:** Claim is high-stakes or based on single source.
**Sources:** runtime_verify_tool, health_endpoint, runtime_import_probe, git_source_truth, wheel_install_manifest
**Cost:** Moderate
**Stopping condition:** Claim independently reproduced or contradicted.

#### Eureka — Synthesize after sufficient evidence
**When:** All other modes exhausted. Ready to evaluate.
**Source:** All prior evidence
**Cost:** Negligible (reasoning only)
**Stopping condition:** Evidence sufficient per INV-E1 through E6.

### 5. MEASURE — Score evidence dimensions

For each important claim, score:

| Dimension | What It Measures |
|-----------|-----------------|
| **Coverage** | How much of the claim's domain is supported? |
| **Source quality** | Is the source authoritative, computed, or inferred? |
| **Freshness** | How recent is the evidence relative to the question? |
| **Independence** | How many independent witnesses support this? |
| **Consistency** | Does evidence agree across sources? |
| **Reproducibility** | Can the result be reproduced? |
| **Specificity** | Does evidence address the exact claim or a proxy? |
| **Authority** | Is the source authorized to make this claim? |

**Evidence score (not absolute truth, prevents weak-source equivalence):**
```
E = C × Q × F × I × R
```
Where C = coverage, Q = source quality, F = freshness, I = independence, R = reproducibility.

### 6. CONTRAST — Preserve competing hypotheses

Do NOT choose one explanation immediately. Hold multiple:

```
hypotheses:
  - id: H1
    claim: "stale runtime package"
    probability: medium
    test: inspect module.__file__
  - id: H2
    claim: "service not restarted"
    probability: medium
    test: compare PID start time and release timestamp
  - id: H3
    claim: "authority logic blocks seal"
    probability: high
    test: inspect gate trace
```

Select next test by: information_gained ÷ cost ÷ risk.
This gives intelligent curiosity rather than random tool calls.

### 7. TEST — Search wide, then narrow

**Correct pattern:**
broad discovery → candidate ranking → targeted inspection → measurement → contradiction search → independent verification

**Wrong patterns:**
- Search everything forever
- Open first result and conclude

### 8. EVALUATE — The epistemic state ladder

Every claim moves through these states. They are NOT interchangeable:

```
UNSEEN → DISCOVERED → OBSERVED → SUPPORTED → CONTRADICTED → REPRODUCED → VERIFIED → ACTIONABLE → SEALED
```

| State | Meaning | Example |
|-------|---------|---------|
| **UNSEEN** | Not looked at yet | A file was mentioned |
| **DISCOVERED** | Located but not read | Found the file path |
| **OBSERVED** | Content read | Read the file content |
| **SUPPORTED** | Matches another source | Logs agree with file |
| **CONTRADICTED** | Conflicts with evidence | Logs disagree with file |
| **REPRODUCED** | Independently obtained same result | Ran test, got same output |
| **VERIFIED** | Confirmed correct by authority or multiple witnesses | Runtime hash matches build |
| **ACTIONABLE** | Sufficient evidence + authority to act | All gates passed |
| **SEALED** | Immutably recorded | VAULT999 receipt |

### 9. DECIDE — Apply stopping rule

Conclude only when ONE of these conditions is met:

**Condition A — Sufficient evidence**
```
critical_claims_covered: true
major_contradictions_resolved: true
required_freshness_met: true
authority_known: true
safe_action_identified: true
```

**Condition B — Safe bounded action**
Full answer uncertain, but a reversible action can gather more evidence.
Example: "Run runtime verification probe before modifying authority.py."

**Condition C — Evidence ceiling**
Necessary evidence unavailable. Correct output: UNKNOWN | HOLD | REQUEST_EVIDENCE.

**Condition D — Risk boundary**
Even with partial evidence, the proposed action is too consequential.
Correct output: DO_NOT_EXECUTE.

### 10. RECORD — Meta-cognition

Before finalising, inspect:

```
what_i_observed:
what_i_inferred:
what_i_assumed:
what_i_could_not_access:
what_might_be_stale:
what_would_falsify_my_conclusion:
what_action_is_safe_despite_uncertainty:
```

This is not self-consciousness. It is disciplined state accounting.

---

## Exploration Budget

Do not explore forever. Calculate dynamic budget:

```
B = S × U × I × V
```

Where:
- S = stakes (1 low → 5 critical)
- U = uncertainty (1 low → 5 high)
- I = irreversibility (1 reversible → 5 irreversible)
- V = value of additional information (1 negligible → 5 transformative)

| Budget | Meaning | Examples |
|--------|---------|---------|
| <10 | Low — quick action | Rename temp file, restart optional worker |
| 10-50 | Moderate — some exploration | Diagnose auth failure |
| 50-100 | High — methodical | Repair VAULT999 chain |
| >100 | Very high — full epistemic rigor | Interpret seismic prospect |

## Value of Information (when to stop)

Continue searching only while EV(next observation) > cost of one more search.

**Continue when:**
- A major hypothesis remains untested
- A required authority fact is missing
- Live state has not been inspected
- Evidence sources contradict
- The cost of error is high
- Another independent witness is available
- The leading conclusion rests on one fragile assumption

**Stop when:**
- All decision-critical questions are answered
- Remaining uncertainty cannot alter the safe action
- Additional sources repeat the same evidence
- The next evidence is inaccessible
- Exploration cost exceeds decision value
- A hard safety boundary is reached

---

## Evidence Matrix Template

Before a consequential conclusion:

| Claim | Supporting | Counterevidence | Missing | State |
|-------|-----------|----------------|---------|-------|
| Runtime uses patched code | import path, matching hash | old package exists | process restart proof | PLAUSIBLE |
| Sovereign identity verified | valid Ed25519 sig | none | session capability | VERIFIED |
| Seal may proceed | identity proof | VAULT chain degraded | exact capability | HOLD |

---

## Early-Collapse Detector (Cooling Loop Telemetry)

The cooling loop should detect these behaviours:
- Conclusion after one source
- No counter-hypothesis considered
- No live-state verification
- Memory treated as current truth
- Tool result accepted without checking output
- Missing evidence silently filled by inference
- Authority assumed from identity
- Execution called success without post-check
- Search stopped despite unresolved critical question

Track per task:
```
exploration_steps_per_task
sources_consulted
independent_witness_count
hypotheses_considered
contradictions_detected
critical_unknowns_remaining
verification_steps_completed
premature_conclusion_reversed
value_of_information_at_stop
```

---

## Constitutional Invariants (INV-E1 through E6)

These are exploration equivalents of F1-F13 — constitutional floors for epistemic conduct.

### INV-E1 — No unsupported collapse
A consequential conclusion requires evidence for every decision-critical claim.
**Violation:** "I think the problem is X" without checking any source.

### INV-E2 — No single-source sovereignty
One source cannot establish a high-stakes conclusion when another independent source is reasonably available.
**Violation:** "I checked one log line and that's the root cause."

### INV-E3 — No inference-to-truth promotion
Reasoning cannot silently upgrade an inferred claim into verified state.
**Violation:** "The hash matches" (actually "the hash could match — I didn't verify").

### INV-E4 — No action before uncertainty classification
Unknowns must be listed before mutation.
**Violation:** Making changes while "not sure about X but let's try it."

### INV-E5 — Exploration must be bounded
The agent must stop when marginal information value becomes negligible or evidence is inaccessible.
**Violation:** Searching every log for the last month when the error just started today.

### INV-E6 — HOLD is a valid intelligent outcome
Failure to conclude is not failure when reality is genuinely unresolved.
**Violation:** Forcing a recommendation when evidence is contradictory.

---

## Integration with Other Skills

### evidence-before-elegance (nine-gate verification)
The two skills form a pipeline:
1. **Explore-before-collapse** — gather evidence from the right surfaces, score it, challenge it
2. **Evidence-before-elegance** — once you have evidence, verify it hasn't been contaminated by narrative, false precision, or tool laundering

Use both. Never skip either.

### hermes-prime-reflex-v2 (pre-action checklist)
The epistemic loop runs BEFORE the reflex checklist. Sequence:
```
INTENT → EXPLORE (10-step) → DECIDE → REFLEX (000-999) → ACT → COOL
```

### cognitive-commands (/NNN_word)
The 7 exploration modes map to cognitive verbs:
- Scout → /111_tengok (perceive)
- Mapper → /222_fikir (reason)
- Driller → /333_jalan (orient) + drill mode
- Surveyor → /111_tengok (measure)
- Contrarian → /555_betul (doubt)
- Verifier → /777_faham (verify)
- Eureka → /777_faham (synthesize)

### Evidence Registry
Canonical evidence surface map at `/root/AAA/docs/evidence-registry.json`.
22 registered sources with questions_answered, access_method, freshness, reliability, limitations.
7 exploration modes mapping to appropriate sources.

---

## Pitfalls

1. **Conclusion after one source.** Root cause of most premature collapses. Always ask: "What would I find if I checked another source?"

2. **No decomposition.** "Why is X broken?" without breaking into subquestions leads to shallow searches. Always decompose first.

3. **Memory as truth.** Memory captures what was true at encoding time. It may be stale, contested, or superseded. Always verify against live state.

4. **Symmetry bias.** Three cleanly parallel explanations is a narrative heat signal, not evidence of correctness. Be suspicious of symmetry.

5. **Authority from identity.** "Arif said this" does not make it true on every domain. Distinguish sovereign authority (F13) from factual accuracy.

6. **Search forever.** The exploration budget `B = S × U × I × V` prevents infinite loops. Use it.

7. **HOLD feels like failure.** It isn't. INV-E6: "Failure to conclude is not failure when reality is genuinely unresolved."

8. **Confusing the evidence score with truth.** `E = C × Q × F × I × R` prevents weak-source equivalence. It does not produce absolute truth. It produces "how much should I trust this claim relative to another."

9. **Skipping the contrarian mode.** When you have a leading explanation, the most important test is: "What would prove me wrong?" If you haven't searched for that, you haven't explored enough.

---

## Origin
Arif's EUREKA session 2026-07-13: "Do Not Collapse Before Reality Has Been Searched." The Epistemic Navigator was identified as the missing organ — the exploration pipeline that runs before the action pipeline. An agent without this organ either collapses early or searches chaotically. With it, the agent gains disciplined curiosity.

Governing sentence:
> *"It does not answer because it has generated a plausible sentence. It answers because it has searched the relevant reality, measured what it found, challenged its own interpretation, and reached a justified stopping point."*
