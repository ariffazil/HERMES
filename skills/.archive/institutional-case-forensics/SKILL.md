---
name: institutional-case-forensics
description: "Build forensic case files from public sources — chronological timelines, MDS case sheets, institutional shadow maps, trigger analysis. For legal, corporate, and governance disputes."
triggers:
  - user shares news article and asks to build chronology or timeline
  - user asks 'who triggered' or 'siapa bangang' or 'who is responsible'
  - user asks to map institutional actors behind an event
  - user asks to build case sheet or shadow map
  - user references court filings, PSC awards, governance disputes
  - user asks about corporate espionage, bank guarantee disputes, bid round patterns
---

# Institutional Case Forensics

Build forensic case files from public sources. Chronological timelines, MDS case sheets, institutional shadow maps, trigger analysis.

## WHEN TO USE

- User shares news article(s) about legal/corporate/governance dispute → build chronology
- User asks "who triggered" or "siapa bangang" → identify THE trigger, not distribute blame
- User asks to map institutional actors → shadow map (role-level, not individual unless named in court)
- User asks about bid round patterns, PSC awards, governance changes → pattern analysis
- User references court cases, bank guarantee disputes, corporate espionage → full case file

## WORKFLOW (MANDATORY SEQUENCE)

### Step 1: Source Extraction (BEFORE building anything)
- Extract ALL user-provided URLs FIRST
- Search for related articles (same case, same parties, earlier/later coverage)
- Build source index: URL, date, outlet, what it covers
- **NEVER build a timeline from one source.** Minimum 3 sources per key date.

### Step 2: Chronological Timeline
- Extract every dated event from all sources
- Cross-reference dates across sources (≥2 sources per date = OBS)
- Present as table: Date | Event | Source | Confidence label
- **PITFALL:** Do NOT include editorial interpretation in timeline. Timeline = facts only.

### Step 3: MDS Case Sheet
Standard fields (see references/mds-case-template.md):
- ACTOR (named individuals + their roles)
- COUNTERPARTY (who they acted against)
- VECTOR (how the action happened — email, court filing, BG call, etc.)
- PAYLOAD (what was at stake — document, money, contract rights)
- TIMELINE (from Step 2)
- CHARGE / LEGAL FRAMEWORK (statutes, court jurisdiction)
- DEFENSE (what the other side argues)
- EFFECT (quantified where possible)
- OPEN THREADS (what we don't know yet)
- CONFIDENCE (OBS/DER/INT/SPEC breakdown)

### Step 4: Institutional Shadow Map
- Map WHO sits behind each trigger at ROLE level (institution + office)
- Named individuals ONLY where public court record or official announcement names them
- Otherwise = role/institution + **888 HOLD** (insufficient evidence for individual attribution)
- **NEVER speculate on individual blame without public evidence.** F6 MARUAH violation.

### Step 5: Trigger Analysis
- Identify THE trigger — the single decision/action that set the cascade in motion
- **CRITICAL PITFALL:** Do NOT distribute blame across multiple actors when user asks "who triggered." User wants THE trigger, not a balanced analysis.
- Map cascade: Trigger → immediate effect → secondary effects → systemic impact
- Compute value lost where possible (cash flow, opportunity cost, institutional damage)

## STYLE RULES (LEARNED FROM SESSION CORRECTIONS)

### "Direct answer" means DIRECT
- User says "direct answer" → lead with the answer in ONE sentence, then support
- Do NOT build elaborate multi-actor blame distribution when user asks "siapa yang bangang"
- User wants THE trigger identified, not a balanced "everyone shares responsibility" analysis
- **Pattern:** User asks X → Answer X first → Then provide context

### Don't over-explain the obvious
- If user already knows the framework, don't re-explain it
- If user gives you insider information, USE it — don't treat it as speculation to be verified
- "Canary" signals from user = PLAUSIBLE, not "needs more evidence"

### BM casual for analytical discussion
- Technical analysis in English OK, but conversational framing in BM
- User prefers Penang BM-English mix for analytical back-and-forth
- Formal English only for artifact files (case sheets, shadow maps)

## ANALYTICAL FRAMEWORKS

### "Simulative" (Arif's extension of Acemoglu)
See references/simulative-framework.md for full explanation.

Core insight: Acemoglu says institutions collapse from internal extractive design. "Simulative" adds: institutions also collapse when external actors ACUTE-EXPLOIT institutional weakness — not slow extraction, but targeted attack during vulnerability window.

Pattern: Institution weakened (BOD thin, resignations, internal crisis) → external actor sees opportunity → takes action they wouldn't dare during normal state → cascade damage exceeds what the weakness alone would cause.

**Key diagnostic question:** "Would this actor have done this when the institution was at full strength?" If NO → simulative.

### MDS (Multi-Dimensional Scenario)
Structured case analysis across multiple axes. Each node = trigger/event. Each edge = causal link. Each attribute = institution/office/evidence/confidence.

### BANGANG Detector (C_dark from APEX)
C_dark = A · (1-P) · (1-X)
- A = Capacity (ability to act)
- P = Precision (did they know what they were doing?)
- X = Execution (did they do it well?)

High C_dark = capacity without precision or execution = BANGANG.

## CONFIDENCE LABELS (F2 TRUTH)
- **OBS**: Verbatim from ≥2 public sources (dates, charges, named individuals)
- **DER**: Derived from court logic or computation (financial impact calculations)
- **INT**: Interpretive from patterns (motive, institutional behavior)
- **SPEC**: Hypothesised (document content, detection mechanisms, causal links without direct evidence)
- **888 HOLD**: Insufficient evidence for individual attribution — stop at role/institution level

## OUTPUT FORMAT
- Case sheets: Markdown with tables, saved to outbox
- Shadow maps: ASCII diagram + node-by-node table
- All artifacts: SHA256 hash + byte count for audit trail
- Connected cases: cross-reference by case_id in header

## PITFALLS
1. **Distributing blame when user wants THE trigger** — User asks "siapa bangang?" = identify ONE primary trigger, not a balanced multi-party analysis
2. **Building timeline from single source** — always cross-reference ≥2 sources per date
3. **Naming individuals without court record** — F6 MARUAH violation. 888 HOLD unless named in court filings or official announcements
4. **Over-explaining frameworks user already knows** — if user references Acemoglu, don't explain Acemoglu back to them
5. **Missing temporal overlaps** — always check: what else happened in the same quarter/month? Coincidences in institutional forensics are signals, not noise
6. **Ignoring insider signals** — user's "canary" information = PLAUSIBLE, not "needs verification"
7. **Treating every actor equally** — in trigger analysis, there's usually ONE actor whose decision was the pivot. Find it.
