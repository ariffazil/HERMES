---
name: institutional-forensic-analysis
description: "Build forensic case files on institutional crises — chronological mapping, detection analysis, shadow mapping, value quantification, theoretical framing, constitutional audit. For multi-source, multi-actor, multi-front institutional conflicts."
version: 1.0.0
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
- When Arif asks "siapa yang BANGANG?" — he wants SYSTEMIC analysis (who designed the system that allowed this), not INDIVIDUAL blame
- When Arif says "now can u see it?" — he's checking if you've SYNTHESIZED, not just PROCESSED
- Direct answer first. Evidence after. Structure always.
- BM casual default for conversation. English for technical/constitutional precision.

## Pitfalls

1. **Sequential processing instead of convergent synthesis.** Agent processes facts one by one and builds timeline but NEVER sees the PATTERN. Arif sees patterns across data points that arrive separately. The agent must learn to ask: "what converges here?" after every batch of data.

2. **Confusing extraction with exploitation.** Acemoglu's extractive institutions = internal decay. Simulative exploitation = external actors exploiting institutional weakness under neutral guise. These are DIFFERENT patterns requiring DIFFERENT detection tools.

3. **Naming individuals without evidence.** Court-named = OBS. Role-level = CLAIM. Unknown = 888 HOLD. Never speculate on individual intent.

4. **Stopping at "what happened" instead of "why now."** The TIMING of events relative to institutional stress is often more important than the events themselves.

5. **Missing the vulnerability window.** Board resignations + profit decline + restructuring + external litigation = CONVERGENT STRESS. This creates windows that rational external actors exploit.

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
- `references/petronas-petros-shell-case.md` — worked example: full forensic case (375 lines, 59 refs)
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
