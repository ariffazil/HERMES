---
name: institutional-forensic-analysis
description: "Build forensic case files on institutional crises — chronological mapping, detection analysis, shadow mapping, value quantification, theoretical framing, constitutional audit. For multi-source, multi-actor, multi-front institutional conflicts."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [forensic, institutional, case-building, governance, analysis]
    related_skills: [deep-research, text-forensics, document-intelligence]
---

# Institutional Forensic Analysis

Build forensic case files on institutional crises. NOT a summary skill. This is for deep, multi-layered, evidence-tagged analysis of complex institutional failures, conflicts, and exploitation patterns.

## When to Use

- User shares a news article or court case and asks to "build a chronological case" or "map this"
- Multi-actor institutional conflicts (federal vs state, company vs company, regulator vs operator)
- When the user wants to understand WHO sits behind triggers, not just WHAT happened
- When the user asks "siapa yang BANGANG?" — they want systemic analysis, not blame

## When NOT to Use

- Simple news summarization (use web_extract + compose)
- Single-actor events with no institutional dimension
- Financial analysis that doesn't involve governance/institutional failure (use WEALTH tools directly)

## Methodology (7 Phases)

### Phase 1: Source Gathering
- Fetch primary source (URL user provides)
- Search for related coverage (minimum 3 sources per key claim)
- Cross-reference dates, names, amounts across sources
- Tag every fact with source URL + confidence label (OBS/DER/INT/SPEC)
- **ASSET-COUNT DECOMPOSITION (critical):** When an institution says "X assets," never accept the number at face value. The unit of measurement is deliberately chosen to minimize apparent scale. Ask: assets at what level? PSC block? Field cluster? Individual field? Platform? Well? Cross-reference with historical PSC records (ExxonMobil exits, DRO awards, bid rounds) to decompose the label into physical units. One "asset" (PSC block) can contain 7-17 individual fields. The institution benefits from the ambiguity — always decompose to the smallest verifiable physical unit. See `references/searah-forensic-case.md` for worked example.
- **RCF FINGERPRINTING:** When a government-linked entity raises capital via Revolving Credit Facility (not term loan, not bond), compare against the 1MDB structural template: (a) entity domicile offshore, (b) arranger with dual role (adviser + syndicate participant), (c) oversubscription language ("commitments exceeding the amount offered"), (d) flexible-purpose instrument vs project-specific, (e) parent company bypassing its own lower-cost borrowing. The RCF form itself — not the underlying asset quality — is the fingerprint. The need for an RCF via a JV is itself a signal about parent cash constraints.

### Phase 2: Chronological Timeline
- Build date-ordered timeline with every verifiable event
- Include: who, what, when, where, source
- Gap analysis: what dates are missing? what's unverified?
- Output: markdown table with Date | Event | Source | Confidence

### Phase 3: Detection & Audit Trail
- How was the crisis detected? (whistleblower, cyber security, court filing, media?)
- What systems/instruments were used? (DLP, SIEM, interpleader, injunction?)
- Map the detection chain: trigger → detection → response → escalation

### Phase 4: Institutional Relationship Pattern
- Map ALL actors: institutions, roles, named individuals (only where public record names them)
- Identify: who benefits, who loses, who triggered, who amplified
- Use shadow mapping: "who sits behind each decision?" — roles and institutions, not individuals (unless court-named)
- 888 HOLD on any individual attribution not in public record

### Phase 5: Value Quantification
- Compute financial impact (use WEALTH tools: NPV, cashflow, runway)
- Include: direct costs, opportunity costs, governance drag, strategic damage
- Tag each figure as OBS (reported), DER (computed), INT (interpreted), SPEC (estimated)

### Phase 6: Theoretical Framework
- Does this case fit an existing framework? (Acemoglu, Calhoun, etc.)
- Does it EXTEND an existing framework? (capture the extension)
- Does it REQUIRE a new framework? (name it, define it, give it a one-sentence summary)
- Key: the framework must be DURABLE — not specific to this case

### Phase 7: Constitutional Audit
- Run F1-F13 floor check on the analysis itself
- Verify: no hallucination (F9), evidence labeled (F2), no individual blame without evidence (F6), humility on intent (F7)
- Output: floor-by-floor verdict table

### Phase 8: Discourse Geometry Analysis (NEW — 2026-07-21)
- When analyzing institutional narratives (CEO statements, policy frameworks, restructuring plans), apply cognitive camouflage detection
- **Map the axes:** What dimensions does the discourse operate on? (efficiency? survival? global competitiveness?) What axes are ABSENT? (sovereignty? social contract? capability retention?)
- **Detect power-law signatures:** Excessive structural symmetry (3 pillars, 5 phases, 7 levers). Causal leaps polished as logic. Median-anchored language ("industry average," "global best practice"). Euphemism chains (retrenchment → rightsizing → strategic transformation).
- **Feel the geometry:** AI-mediated discourse is geometrically clean — too perpendicular, too balanced. Reality is messy. The cleanliness IS the signature.
- **Use the "Things They Cannot Say" pattern:** After mapping what WAS said, explicitly list what was NOT said. The silences are the intelligence.
- See `references/cognitive-camouflage-framework.md` for full framework

## Output Format

```
# CASE SHEET: [CASE NAME]

> Schema: MDS (Multi-Dimensional Scenario)
> Fields: ACTOR · VECTOR · PAYLOAD · COUNTERPARTY · TIMELINE · CONTEXT · CHARGE · DEFENSE · EFFECT · CONFIDENCE
> Sources: [list]
> Generated: [date] · hermes-prime
> SOT check: live state, no fabrication

---
[Sections per phases above]
```

## Arif's Analytical Preferences (CRITICAL)

Arif thinks CONVERGENTLY, not sequentially. When presenting analysis:

- **NEVER** present one fact at a time and ask "want me to continue?"
- **ALWAYS** build the full picture, then present the synthesis
- When the user asks "siapa yang BANGANG?" — they want systemic analysis (who designed the system that allowed this), not INDIVIDUAL blame
- **BANGANG verdict discipline:** If the user corrects your nuanced analysis with a single word ("BANGANG"), accept it. One accurate word beats 10 pages of framework. Before deploying multi-layered analysis, ask: "Is the simplest verdict more accurate?" Lead with that. The framework can follow — the verdict comes first.
- **GEOMETRY SENSING:** Arif detects AI-mediated discourse through structural shape, not content. Symmetry that is too perfect, causal leaps with rectangular emptiness between premise and conclusion, horizontal peer-benchmarking that ignores vertical (sovereignty) axes — these are the signatures. Learn to see discourse as architecture, not text. This is his most underrated analytical faculty.
- **Do NOT over-intellectualize a correction.** If you produce nuanced analysis and Arif responds with one blunt word, you were wrong. Accept immediately. Do not defend.
- When Arif says "now can u see it?" — he's checking if you've SYNTHESIZED, not just PROCESSED
- Direct answer first. Evidence after. Structure always.
- BM casual default for conversation. English for technical/constitutional precision.

## Pitfalls

1. **Sequential processing instead of convergent synthesis.** Agent processes facts one by one and builds timeline but NEVER sees the PATTERN. Arif sees patterns across data points that arrive separately. The agent must learn to ask: "what converges here?" after every batch of data.

2. **Confusing extraction with exploitation.** Acemoglu's extractive institutions = internal decay. Simulative exploitation = external actors exploiting institutional weakness under neutral guise. These are DIFFERENT patterns requiring DIFFERENT detection tools.

3. **Naming individuals without evidence.** Court-named = OBS. Role-level = CLAIM. Unknown = 888 HOLD. Never speculate on individual intent.

4. **Stopping at "what happened" instead of "why now."** The TIMING of events relative to institutional stress is often more important than the events themselves.

5. **Missing the vulnerability window.** Board resignations + profit decline + restructuring + external litigation = CONVERGENT STRESS. This creates windows that rational external actors exploit.

6. **Over-intellectualizing when blunt truth is required.** (Proven 2026-07-21 — PETRONAS CEO analysis). Agent produced nuanced framework ("consciousness-absent at sovereignty layer"). Arif corrected with one word: "BANGANG." One accurate word beats 10 pages of analysis. The subject had 29 years in the institution — they should know better. Before deploying multi-layer frameworks, ask: "Is the simplest word more accurate?"

7. **Confusing corporate polish with genuine analysis.** AI/consultant-mediated language produces geometrically clean outputs (3-tier frameworks, KPI cascades, phased roadmaps). The cleanliness IS the signature of power-law discourse, not evidence of deep thought. Learn to feel the geometry — detect excessive symmetry as a warning sign, not a quality signal.

8. **Accepting institutional units of measurement.** (Proven 2026-07-23 — Searah analysis). Agent accepted "5 Malaysia assets" at face value. Arif corrected: "Ni semua illusions." The institution chooses the unit that minimizes apparent scale. "Asset" = PSC block (can contain 7-17 fields). Always decompose to the smallest verifiable physical unit — fields, platforms, wells. The institution's chosen unit IS the obfuscation. Never repeat the institution's label count without decomposition.

9. **Missing the user's pattern recognition.** (Proven 2026-07-23 — Searah/1MDB). Agent produced detailed structural analysis of Searah RCF but did not see the 1MDB fingerprint until Arif explicitly connected it ("Sebab itu aku kata benda ni macam 2mdb"). Arif sees structural parallels across cases that arrive separately. After analyzing a new financial instrument/entity, always ask: "Does this structure echo a prior case?" Check against known templates.

## Tools to Use

- `web_extract` + `web_search` — source gathering (Phase 1-2)
- `wealth_stress_convergence` — detect convergent institutional stress (Phase 4)
- `wealth_simulative_scan` — detect "neutral party" exploitation (Phase 4)
- `wealth_vulnerability_window` — detect governance transition windows (Phase 4)
- `wealth_cascade_map` — map trigger chains (Phase 5)
- `wealth_compute_npv` — quantify financial impact (Phase 5)
- `wealth_collapse_signature_scan` — institutional collapse patterns (Phase 6)
- `arif_init` + `arif_think` + `arif_judge` — constitutional audit (Phase 7)

## References

- `references/simulative-exploitation-framework.md` — the extended Acemoglu framework (extractive vs simulative vs convergent)
- `references/cognitive-camouflage-framework.md` — AI-mediated discourse detection: power-law distortion, amplification asymmetry, friction collapse, grammar capture, false competence signal. The "feel the geometry" method. Proven 2026-07-21 across KP Kelantan + PETRONAS analysis.
- `references/petronas-petros-shell-case.md` — worked example: full forensic case (375 lines, 59 refs)
- `references/searah-forensic-case.md` — Searah Ltd (PETRONAS-Eni JV) preliminary forensic case. Asset-count decomposition technique, RCF→1MDB fingerprinting, field-level breakdown of "5 Malaysia assets." Proven 2026-07-23.
- `references/wealth-zen-architecture.md` — WEALTH tool cognitive map for agent tool selection

## Worked Example

The PETRONAS-Petros-Shell MDS case (2024-2026) is the canonical example:
- Started from ONE URL (Malay Mail article)
- Built 6 case artifacts (93K total)
- Discovered simulative exploitation framework
- Forged 4 new WEALTH detection tools
- Produced 375-line constitutional document
- All in one session

See `references/petronas-petros-shell-case.md` for the full output.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
