# Epistemic Navigator — Anti-Collapse Exploration Protocol

> **Source:** Arif, 2026-07-13 EUREKA session, after identifying that agents collapse uncertainty into answers before searching reality.
> **Status:** Architecture-level directive. Not yet implemented as runtime tool. See P1 tracking.

## The Principle

An agent must not collapse uncertainty into one answer before exploring the relevant possibility space.

**Collapse = converting uncertainty into one conclusion before the relevant evidence surfaces have been searched.**

## The 10-Step Anti-Collapse Loop

Every task should move through:

```
ORIENT → DECOMPOSE → MAP → SEARCH → MEASURE → CONTRAST → TEST → EVALUATE → DECIDE → RECORD
```

### 1. ORIENT — What kind of problem?

Before searching, classify the request internally:

| Question | Purpose |
|----------|---------|
| Factual, diagnostic, strategic, creative, or operational? | Determines method |
| Current or historical? | Determines freshness requirements |
| Reversible? | Determines risk threshold |
| High-stakes? | Determines exploration budget |
| Needs files, telemetry, DB, web, or human judgment? | Determines evidence surface |
| What damage from a wrong answer? | Determines caution level |

Output a compact struct:
```
problem_class: DIAGNOSTIC
stakes: MODERATE
freshness_required: LIVE
reversibility: REVERSIBLE
evidence_floor: L3
```

### 2. DECOMPOSE — What must be known?

Break the question into subquestions. Example:

> "Why is arif_seal failing?"

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

### 3. MAP — Where could the answer exist?

Evidence surface mapping:

| Question type | Evidence surface |
|---------------|------------------|
| Current runtime | process, import path, service unit, health endpoint |
| Source truth | git repo, commit, diff, tests |
| Database state | PostgreSQL/Supabase query |
| Memory state | Canonical memory store and provenance |
| Historical action | VAULT999 + operational ledgers |
| Tool behaviour | tool registry, schema, logs, source |
| External fact | Current authoritative web source |
| Human intent | Current authenticated session |
| Infrastructure | telemetry, CPU, disk, network, service manager |
| Domain conclusion | GEOX, WEALTH, or WELL evidence |

### 4. SEARCH — Explore

**Modes:**

| Mode | Purpose | Method |
|------|---------|--------|
| **Scout** | Fast, broad | Identify candidate locations, discover files/services |
| **Mapper** | Build relationships | Map dependencies, ownership, data flow |
| **Driller** | Deep inspect one path | Open source, query records, inspect logs |
| **Surveyor** | Measure the system | Calculate counts, latency, drift, confidence |
| **Contrarian** | Seek disconfirming evidence | Test if leading explanation is wrong; identify alternatives; prevent confirmation bias |
| **Verifier** | Reproduce claim independently | Rerun test, recompute hash, inspect another witness |
| **Eureka** | Synthesize | Only after evidence coverage is sufficient |

### 5. MEASURE — Evidence dimensions

For each important claim, score:
- **Coverage** — how much of the possibility space is covered
- **Source quality** — how reliable is the evidence source
- **Freshness** — how recent is the data
- **Independence** — how many independent witnesses
- **Consistency** — does evidence agree
- **Reproducibility** — can the result be re-obtained
- **Specificity** — how precisely does evidence address the question
- **Authority** — does the source have standing

### 6. CONTRAST — Preserve competing hypotheses

Do not choose one explanation immediately.

```
hypotheses:
  - id: H1
    claim: stale runtime package
    probability: medium
    test: inspect module.__file__
  - id: H2
    claim: service not restarted
    probability: medium
    test: compare PID start time and release timestamp
  - id: H3
    claim: authority logic still blocks seal
    probability: high
    test: inspect gate trace
```

Select tests by: information gained ÷ cost ÷ risk

### 7. TEST — Evaluate hypotheses

Run the highest-value tests first. Update probabilities.

### 8. EVALUATE — Is evidence sufficient?

May conclude only when one condition is met:

| Condition | When |
|-----------|------|
| **A — Sufficient evidence** | All critical claims covered, major contradictions resolved, required freshness met, authority known |
| **B — Safe bounded action** | Full answer uncertain, but reversible action can gather more evidence |
| **C — Evidence ceiling** | Necessary evidence unavailable. Output: UNKNOWN / HOLD / REQUEST_EVIDENCE |
| **D — Risk boundary** | Action too consequential for partial evidence. Output: DO_NOT_EXECUTE |

### 9. DECIDE — Proceed, experiment, hold, or deny

Select action within known authority boundaries.

### 10. RECORD — Provenance and corrections

Store what was observed, inferred, assumed, and what would falsify the conclusion.

## Exploration Budget

```
B = S × U × I × V
```

Where: S = stakes, U = uncertainty, I = irreversibility, V = value of additional information.

| Scenario | Budget |
|----------|--------|
| Rename temp file | Low |
| Restart test worker | Moderate |
| Repair VAULT999 chain | Very high |
| Interpret seismic prospect | Very high domain |

## Value of Information — When to Stop

Continue searching when:
- A major hypothesis remains untested
- A required authority fact is missing
- Live state has not been inspected
- Evidence sources contradict
- The cost of error is high
- Another independent witness is available
- The leading conclusion rests on one fragile assumption

Stop when:
- All decision-critical questions are answered
- Remaining uncertainty cannot alter the safe action
- Additional sources repeat the same evidence
- The next evidence is inaccessible
- Exploration cost exceeds decision value
- System reaches a hard safety boundary

## The Evaluation Ladder

Every claim moves through explicit epistemic states:

```
UNSEEN → DISCOVERED → OBSERVED → SUPPORTED → CONTRADICTED → REPRODUCED → VERIFIED → ACTIONABLE → SEALED
```

These are not interchangeable. Finding a file = DISCOVERED. Reading its content = OBSERVED. Matching logs = SUPPORTED. Running its test = REPRODUCED. Confirming active runtime hash = VERIFIED. Possessing authority = ACTIONABLE. VAULT999 receipt = SEALED.

## Metacognition — What the Agent Must Know About Itself

Before finalising, inspect:

```
what_i_observed: [...]
what_i_inferred: [...]
what_i_assumed: [...]
what_i_could_not_access: [...]
what_might_be_stale: [...]
what_would_falsify_my_conclusion: [...]
what_action_is_safe_despite_uncertainty: [...]
```

This is disciplined state accounting, not self-consciousness.

## Early-Collapse Detector

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

## Constitutional Invariants (INV-E1 through INV-E6)

| Invariant | Rule |
|-----------|------|
| **INV-E1** | A consequential conclusion requires evidence for every decision-critical claim. |
| **INV-E2** | One source cannot establish a high-stakes conclusion when another independent source is reasonably available. |
| **INV-E3** | Reasoning cannot silently upgrade an inferred claim into verified state. |
| **INV-E4** | Unknowns must be listed before mutation. |
| **INV-E5** | Exploration must be bounded — stop when marginal information value becomes negligible or evidence is inaccessible. |
| **INV-E6** | Failure to conclude is not failure when reality is genuinely unresolved. HOLD is a valid intelligent outcome. |

## Relationship to Other Frameworks

| Framework | This Navigator | Evidence-Before-Elegance |
|-----------|----------------|--------------------------|
| Domain | All tasks | Analytical output only |
| Role | Decides where to look | Evaluates what was found |
| When | Before and during exploration | At point of output emission |
| Key failure | Collapsing too early | Narrative override of evidence |

The two are complementary: the Navigator gets the agent to the right evidence; Evidence-Before-Elegance prevents that evidence from being misrepresented.
