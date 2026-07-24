---
name: institutional-case-building
description: Build chronological case files from public sources (court testimony, media, filings) — institutional shadow mapping, trigger analysis, value quantification. For corporate disputes, governance failures, regulatory conflicts.
triggers:
  - "build a case on"
  - "chronological case"
  - "who triggered"
  - "shadow map"
  - "institutional analysis"
  - "what happened with [dispute/lawsuit/investigation]"
tags:
  - research
  - forensics
  - governance
  - case-file
  - institutional-analysis
---

# Institutional Case Building

Build evidence-based chronological case files from public sources — court testimony, media reporting, regulatory filings, bid round data. Output structured case files with institutional shadow maps, trigger analysis, and value quantification.

## When to Use

- User drops a news article or court case URL and asks "build a chronological case"
- User asks "who triggered" a dispute/investigation/governance failure
- User wants institutional shadow mapping (which office/role made which decision)
- User wants value quantification (RM lost, blocks frozen, revenue delayed)
- Corporate disputes involving multiple institutions (government, NOCs, operators)

## Workflow

### Step 1: Fetch & Extract Primary Sources

1. Extract the user's primary URL with `web_extract`
2. Read the full cached file — news articles are often truncated in the first extraction
3. Identify all named entities (people, institutions, dates, amounts, court references)
4. Note epistemic tags: OBS (direct testimony), DER (derived/computed), INT (interpreted), SPEC (speculation)

### Step 2: Cross-Reference with Additional Sources

Search for corroborating coverage from multiple outlets:
- Malay Mail, The Star, FMT, Malaysiakini, Astro AWANI, Utusan, NST
- The Edge Malaysia (business/legal depth)
- Borneo Post, Sarawak Tribune (state-level perspective)
- Reuters, Bloomberg (international angle)

**Key principle:** Each fact needs ≥2 independent sources for CLAIM status. Single source = PLAUSIBLE. No source = SPEC or 888 HOLD.

### Step 3: Build Chronological Timeline

Structure as phases, not just dates:
```
Phase 1: [Context/Setup] (dates)
Phase 2: [Trigger Event] (dates)
Phase 3: [Escalation] (dates)
Phase 4: [Litigation/Investigation] (dates)
Phase 5: [Resolution/Ongoing] (dates)
```

Each entry: | Date | Event | Source |

### Step 4: Institutional Shadow Mapping

For each trigger event, identify:
- **Institution** — which entity made the decision
- **Office/Role** — which division/department (e.g., "Gas & Maritime", "MPM", "Board Risk Committee")
- **Named humans** — only if explicitly in court docs or official filings
- **UNKNOWN** — when individual attribution not in public record (888 HOLD)

Output format:
```
TRIGGER                          INSTITUTION           OFFICE/ROLE              NAMED?
─────────────────────────────────────────────────────────────────────────────────────────
[event]                          [entity]              [division/role]          ✅/❌/⚠️
```

**Rule:** Never speculate on individual names not in public record. "Board collectively decided" is acceptable. "Person X must have signed" is NOT.

### Step 5: Trigger Analysis

Identify THE trigger — the single decision/action that converted a manageable situation into a crisis. User often wants this simple answer, not a systems analysis.

**Pitfall (from user correction):** When user asks "who did X?", they want THE ONE THING (the trigger), not a full multi-axis systems analysis. Answer the question directly first, then add context.

### Step 5b: Cascade Mapping

After identifying THE trigger, map the full cascade chain:
```
T1 (trigger) → T2 (immediate effect) → T3 (secondary) → T4 (systemic)
```

For each link, compute:
- **Blast radius** (0-1): how much damage this trigger caused
- **Amplification factor**: final_blast / initial_blast
- **Cascade type**: LINEAR (factor < 2), EXPONENTIAL (2-5), DIVERGENT (> 5)

Key insight: the TRIGGER may have small blast radius (e.g., BG call = 0.3), but cascade amplification can make it catastrophic (cumulative = 0.95). Always compute cumulative, not just individual.

### Step 5c: Vulnerability Window Detection

Check if the trigger occurred during a **governance vulnerability window**:
- Board thin (below normal size)
- Executive transitions (new leadership settling in)
- Restructuring (workforce cuts, organizational uncertainty)
- Multiple external disputes active simultaneously

If ≥2 conditions present → window OPEN → action taken during window = potentially simulative, not just reactive.

### Step 6: Value Quantification

Calculate:
- Direct financial loss (cash flow deprivation × time)
- Interest/opportunity costs
- Legal costs across courts
- Indirect costs (frozen licensing rounds, delayed investment, reputational damage)
- Who benefits from the delay (cash flow arbitrage)

### Step 7: Save as Case File

Save to `/root/cases/[case-name]/case-file.md` with sections:
1. Parties
2. Chronological Timeline
3. Detection/Response Path
4. Institutional Shadow Map
5. Value Lost
6. Open Questions
7. Source Index
8. Epistemic Tags

For unified multi-case analysis, create `/root/cases/shadow-map-unified.md`.

## Output Format Rules

- Use Markdown tables for timelines, witness lists, party profiles
- Epistemic tags on every major claim: OBS / DER / INT / SPEC / 888 HOLD
- Source index with URLs and dates at bottom
- BM casual for discussion, English for case file documents
- "Shadow map" = which institution/office sits behind each decision node
- F6 (Maruah): never name individuals beyond what's in court records

## Pitfalls

1. **Overcomplicating trigger analysis** — user wants "who pulled the trigger?" not "here's a 5-axis MDS framework." Answer simply first. Arif corrected twice in one session: "U missed the point" and "Hang yang cari pasal." **Verdict → one-sentence justification → then expand only if asked.**
2. **Truncated article extraction** — always read the full cached file; web_extract head+tail misses the middle
3. **Connecting temporal dots as causal** — "A happened before B" ≠ "A caused B." Tag temporal overlaps as PLAUSIBLE, not CLAIM.
4. **Assuming bid round absence = company choice** — check if blocks were even offered. "Shell didn't bid" ≠ "Shell chose not to bid."
5. **Counting company secretaries as board members** — governance red flag, note it explicitly.
6. **Single-source claims** — court testimony from one witness is OBS for what that witness said, but may be INT for what actually happened.
7. **Multi-party verbose analysis when direct answer exists** — When sovereign asks "siapa BANGANG" / "who triggered," give THE ONE THING first, not a systems breakdown. The sovereign gives the framework; you nail the one-liner. THEN expand.
8. **Missing historical precedent check** — Always search: has this actor ever done this before? If Shell never sued Petronas in 60 years and then does it at the moment of maximum institutional weakness, that's not just a legal event — it's a signal. Check historical court records, prior disputes, industry relationships.
9. **LINEAR processing when user thinks CONVERGENT** — Agent processes data sequentially (timeline → case sheet → shadow map → pattern). User sees CONVERGENT patterns (all signals at once). When agent has all the data but "doesn't see the pattern," the failure is analytical MODE, not data availability. **Fix:** After building timeline, explicitly ask: "What events happened in the same quarter? Which stress signals fired simultaneously?" Convergent stress detection requires scanning for simultaneity, not just sequence.
10. **Presenting findings without forging artifacts** — User expects deliverables (case files, shadow maps, framework docs) saved to outbox with SHA256. Don't stop at "here's my analysis" — save it, hash it, deliver it. Artifacts before opinions.

## Analytical Frameworks

### Simulative Exploitation (Acemoglu Critique)
See references/simulative-framework.md for full framework with Shell MDS case study.

Acemoglu/Robinson model: extractive institutions → internal decay → collapse. Cause = endogenous.

**This session's addition:** Institutions don't just collapse from internal extraction. External actors exploit institutional weakness, creating feedback loops that accelerate collapse. This is **simulative exploitation** — rational predators who see the opening and strike.

| Acemoglu Model | Simulative Model |
|---|---|
| Extractive elites weaken institution from within | External actors exploit institutional weakness from outside |
| Endogenous decay | Exogenous predation |
| Institution destroys itself | Institution destroyed by rational actors who see the opening |
| Cause = internal design | Cause = predator-prey dynamics |
| Solution = reform institutions | Solution = **strengthen institutions BEFORE predators arrive** |

**Detection signals:**
- Actor uses "neutral party" legal posture (interpleader, injunction) while actually arbitraging institutional chaos
- Actor takes legal action for the first time in decades — at the exact moment of maximum institutional weakness
- Actor benefits from delay (cash flow savings, free supply, etc.) while institution bears deprivation cost
- Historical precedent: no prior litigation → sudden litigation during institutional stress = calculated, not reactive

**Labeling:** Tag as INT (interpreted from behavioral pattern). Not CLAIM without direct evidence of intent.

### Institutional Collapse Spiral (Feedback Loop Pattern)

When multiple stress dimensions feed each other in a self-reinforcing cycle:

```
Financial stress (profit drop)
    ↓
Cost cutting (rightsizing, workforce reduction)
    ↓
Governance erosion (BOD resignations, loyalty loss, knowledge drain)
    ↓
Intelligence compromise (data leaks, personnel exits to competitors)
    ↓
External exploitation (counterparties exploit weakness)
    ↓
More financial stress (payment freezes, litigation costs, lost revenue)
    ↓
More cost cutting → repeat
```

**Detection method:**
1. Map stress indicators across dimensions (financial, governance, workforce, legal, external) over time
2. Check if decline is LINEAR (steady, manageable) or SPIRAL (accelerating, self-reinforcing)
3. Identify the **weakest link** — the dimension that, if strengthened, breaks the feedback loop
4. Identify the **trigger that started the spiral** vs the **current state**

**Key distinction:** Spiral ≠ just multiple problems. Spiral = each problem makes the others worse. If financial stress doesn't cause governance erosion, it's not a spiral — it's just bad luck on multiple fronts.

### Historical Precedent Check

When an actor takes unprecedented action (first lawsuit in 60 years, first BG call, first competing GSA), always ask:

1. **Has this actor ever done this before?** Search court records, industry history, prior disputes
2. **What changed?** If nothing changed in the actor's situation, what changed in the TARGET's situation?
3. **Timing signal:** Unprecedented action during target's maximum weakness = exploitation signal, not normal commercial behavior

**Sources for historical check:**
- Court registries (e.g., Malaysian court records, SCCO)
- Industry archives (Upstream Online, OE Digital, Energy Intelligence)
- Academic/legal databases
- Retired industry personnel interviews (if accessible)

### Multi-Case Connection Methodology

When a single case sits within a larger institutional conflict:

1. **Build each case separately** — don't try one mega-narrative
2. **Identify the institutional axis** — federal vs state, regulator vs operator, employer vs counterparty
3. **Map connections:** temporal overlap, information asymmetry, common actors, shared institutional axis
4. **Quantify combined value loss** — the sum is always more than individual cases
5. **Run Bangang Detector across ALL parties** — the party with highest C_dark is the root cause

### CEO-Era Contrast Methodology

When comparing leadership eras at an institution (e.g., Wan Zul vs Tengku Taufik at PETRONAS):

1. **Financial trajectories side by side** — PAT, revenue, capex, dividend for each tenure
2. **BOD composition comparison** — size, stability, resignations, dual roles
3. **Crisis management approach** — did the CEO manage relationships (operations-first) or enforce contracts (finance-first)?
4. **External actor behavior** — did counterparties behave differently under different CEOs? If Shell never sued Wan Zul but sued Taufik, that's a signal.
5. **Run stress_index + governance_capacity for both eras** — compare scores numerically
6. **Run cascade_model for both timelines** — compare trajectories

**The Shadow Question:** Was the institutional outcome caused by leadership style or timing? If stress scores differ significantly between eras → leadership matters. If similar → timing/structural factors dominate.

**Pattern:** Operations CEOs protect by managing relationships. Finance CEOs expose by enforcing contracts. Both are "rational." Only one survives institutional stress.

### Constitutional Trigger Analysis (Binary Outcome Cases)

When a single pending decision (court ruling, regulatory verdict, election) creates binary outcomes:

```
Outcome A: Stress → 6% (recovery)
Outcome B: Stress → 100% (collapse)
```

Run `cascade_model` for both scenarios. Present the delta explicitly. The sovereign needs to see: "one ruling = the difference between survival and collapse."

**Sources for scenario modeling:** Court filings (petition + counter-claim), legal commentary, historical precedent (prior rulings on similar constitutional questions).

**Worked example:** `references/federal-court-constitutional-geometry.md` — PETRONAS-Petros Federal Court binary (C1: 6% recovery vs C2: 100% collapse), three-law stack, Emergency-lapse argument, OIC 1954 hidden weapon, CEO shadow contrast.

**Pattern:** Operations CEOs protect by managing relationships. Finance CEOs expose by enforcing contracts. Both are "rational." Only one survives institutional stress.

`wealth_external_exploitation_detect` classifies based on cost/threshold → AGGRESSIVE. But the paper's insight was SIMULATIVE_NEUTRAL — the *posture* was "caught in the middle" while the *effect* was $1.55B extraction.

**Gap:** Tool catches the damage but misses the mask. Future iteration needs **posture-impact divergence** metric: when `claimed_rationale` is "defensive/neutral" but `actual_benefit` is massive → that's simulative, not just aggressive.

**Workaround:** Manually compare `claimed_rationale` field against `actual_benefit_musd`. If gap > 10x → flag as SIMULATIVE regardless of tool output.

### BANGANG Detector (C_dark from APEX)

C_dark = A · (1-P) · (1-X)
- A = Capacity (ability to act)
- P = Precision (did they know what they were doing?)
- X = Execution (did they do it well?)

High C_dark = capacity without precision or execution = BANGANG.

Score each actor independently. The one with highest C_dark is the institutional root cause. User often already knows who it is — your job is to compute and confirm, not redistribute blame.

### Canary Signal Handling

When user provides insider information ("my canary said X", "BOD x puas hati"):
- Treat as **PLAUSIBLE** — not "needs more evidence"
- Don't ask user to verify their own sources
- Use canary to orient analysis, then find public evidence that corroborates or contradicts
- Label the final finding as PLAUSIBLE with canary as supporting signal, not sole source

**Connection strength labels:**
- OBS: direct evidence (shared documents, same personnel, same contract)
- DER: logical connection (same institutional axis, overlapping timeline)
- INT: inferred connection (temporal correlation, behavioral pattern)
- SPEC: hypothetical (unproven information flow, unverified coordination)

## Step 8: Federation Validation (post-case-build)

After building the case file, validate through arifOS + WEALTH to check if the federation's own tools can detect what you found. See `references/federation-validation-workflow.md` for full recipe.

**Critical finding (2026-07-07):** `collapse_signature_scan` returns 0.0 risk for simulative exploitation cases — it only knows extractive patterns (Enron/PDVSA/1MDB/Pemex). When it returns MINIMAL for a case you KNOW is collapsing, that's a **vocabulary gap**, not a falsification. Document it explicitly.

**New tools that fill the gap:** `wealth_institutional_stress_index` (composite 0-1 stress), `wealth_cascade_model` (spiral vs linear), `wealth_governance_capacity` (BOD monitoring), `wealth_external_exploitation_detect` (simulative neutral pattern). All at `/root/wealth/wealth_core/institutional/`.

**Exploitation detector gap:** Classifies based on cost/threshold → AGGRESSIVE. But the paper's insight was SIMULATIVE_NEUTRAL — the *posture* was "caught in the middle" while the *effect* was $1.55B extraction. Future iteration needs **posture-impact divergence** metric.

## Related Skills
- `legal-case-dossier-from-news` — single-case MDS dossier with Bangang Detector and Trigger Analysis
- `institutional-epistemic-sink-forensics` — Calhoun behavioral sink pattern detection

## Support Files
- `references/governance-bod-stress-pattern.md` — BOD governance weakness detection indicators
- `references/psc-bid-round-analysis.md` — operator participation tracing in petroleum licensing rounds
- `references/institutional-collapse-spiral.md` — feedback loop pattern + simulative exploitation framework + Petronas case study
- `references/petronas-simulative-shadow-case-2026-07-07.md` — full Petronas case study data: financials, governance, Shell MDS, espionage, MBR pattern, stress index results, scenario modeling, CEO contrast (Wan Zul vs Taufik)
- `references/federation-validation-workflow.md` — how to validate case analysis through arifOS + WEALTH tools, blind spot documentation

## Case File Template

```markdown
# CASE FILE: [Title]

> **Status:** ACTIVE / RESOLVED / ARCHIVED
> **Filed:** [date]
> **Classification:** F2 OBS/DER
> **Last updated:** [date]

## 0. PARTIES
[table]

## 1. CHRONOLOGICAL TIMELINE
### Phase 1: [name]
[table with Date | Event | Source]

## 2. DETECTION/RESPONSE PATH
[flowchart or structured list]

## 3. INSTITUTIONAL SHADOW MAP
[table with Trigger | Institution | Office | Named?]

## 4. VALUE LOST
[table with Category | Amount | Status]

## 5. OPEN QUESTIONS
[numbered list with priority]

## 6. SOURCE INDEX
[table with # | Source | URL | Date]

## 7. EPISTEMIC TAGS
[table with Claim | Tag | Confidence]
```
