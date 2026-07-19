---
name: geological-artifact-rigor
description: "Standing instruction for all geoscience artifacts — panels, dossiers, maps, cross-sections. Born from Raja Ridhuan's feedback: 'tak cukup geology.' 8 hard rules ensuring real geological substance, not just epistemic tagging."
version: 1.1.0
author: arif-sovereign
tags: [geology, GEOX, rigor, standing-instruction, F2-truth]
related: [hermes-prime-identity, explorer-dispatch-protocol, measure-before-acting, evidence-before-elegance]
---

# Geological & Technical Artifact Rigor

> **Origin:** A working PETRONAS exploration geologist reviewed a tectono-stratigraphic panel and said "tak cukup geology" — not enough geology. The artifact had epistemic-confidence tagging and stylized cartoon cross-sections but lacked actual technical substance. This skill prevents that failure mode.

## Trigger

Any time you produce or revise a geoscience, reservoir, or subsurface artifact: panels, dossiers, maps, cross-sections, stratigraphic columns, well correlations, seismic interpretations, prospect assessments.

## Hard Rules

### 1. Epistemic Tags Are Not a Substitute for Content
Confidence labeling (CLAIM/HYPOTHESIS/etc.) is a wrapper around a claim, not the claim itself. Every tagged item must carry the actual data point, number, reference, or mechanism — not just a label and a schematic shape.

### 2. No Cartoon Geometry for Technical Audiences
Do not render generic sine-wave "basin" shapes, blob "anticlines," or arrow-only "overpressure" icons as interpretation. If real seismic character, well logs, structure/isopach maps, or published figures exist, reference or reproduce their actual geometry and cite the figure. If no real data exists, say so explicitly — do not fill the gap with a schematic that looks authoritative.

### 3. Quantitative Claims Need the Supporting Curve
Any timing claim (e.g. "oil expelled early, gas expelled late") must be backed by the actual maturity indicator (Ro, Tmax, burial history) or flagged as UNSUPPORTED ASSUMPTION. Any reservoir/seal/trap claim needs closure area, net-to-gross, or volumetric range — not just a geometric cartoon of "reservoir here."

### 4. Terminology Precision Check
Cross-check every named geological entity, terrane, or structural term against its established usage in the cited literature. Flag any term used in a way that could conflate two distinct concepts (e.g. a named crustal block vs. the process acting on it). State the check was done.

### 5. State What Data Would Upgrade Each Hypothesis
For every item tagged HYPOTHESIS or PLAUSIBLE, name the specific dataset, well, or measurement that would move it to CLAIM. A reader should know exactly what's missing, not just that something is missing.

### 6. Age/Stage Precision Must Match Actual Resolution
Do not present a stage duration more narrowly than the underlying dataset resolves. If the number is an onset age bounding a longer process, say so — don't let stage boxes imply false precision.

### 7. Self-Check Before Delivery
Before presenting any geoscience artifact, run this test:
> "Would a subsurface geologist with access to real well/seismic data accept this as technical content, or would they say this is dressing without depth?"
If the honest answer is the latter, add real data, cite the actual figure/table, or explicitly scope the artifact as conceptual framing only — labeled as such up front.

### 8. Distinguish Framework from Finding
Epistemic tagging (CLAIM/PLAUSIBLE/HYPOTHESIS/ESTIMATE/SCHEMATIC) is a valuable governance layer for tracking confidence over time — keep it. But it governs geological content; it does not generate geological content. Never let the elegance of the tagging system create the impression of rigor that the underlying geology doesn't have.

## Coordinate Verification (supplementary)

- Every coordinate must have a verified source (GPS, published map, GeoNames)
- "From memory" = SPECULATED, never OBSERVED
- Plotting wrong coordinates in geoscience = wrong well = dry hole
- Lipad/Tabin: actual 5.188°N, 118.502°E (GPS verified)
- Maliau Basin: actual 4.830°N, 116.900°E (Wikipedia)

## The GEOX Wedge — Intelligence vs. Workflow

GEOX competes on a different axis than DS365/Petrel:
- **DS365/Petrel:** Workflow engines, visualization, data management, multi-user interpretation
- **GEOX:** Intelligence layer — tests whether an earth claim is defensible, falsifiable, and evidence-grounded

The wedge sentence: "DS365 tells you where your model lives. GEOX tells you whether your model deserves to live."

When building artifacts, GEOX should not try to be Petrel. It should:
- Read from incumbent systems (Petrel exports, LAS, SEGY)
- Audit interpretations for consistency with evidence
- Classify uncertainty with OBS/DER/INT/SPEC separation
- Keep alternative hypotheses alive
- Produce verdicts that can say KILL when the earth story doesn't hold

See skill: `geox-competitive-intelligence` for full benchmark design and competitive positioning.

## Block vs Structure Names (supplementary)

- PSC block names (Block G, H, K, N, X, R) = operator/PETRONAS designations
- Structural trend names (L-B-P, M-La-S, Pg-Lt-U) = geological labels
- Field names (Limbayong, Bestari, Kikeh, Rotan) = discovery names
- These are NOT interchangeable. Verify before using.

## Artifact Workflow (from session failures)

Before building any geoscience artifact, execute this sequence:

1. **Probe GEOX first** — call `geox_basin` for the target region. If it returns "Basin data not found," DON'T retry. Pivot: run `geox_map_context_scene` for spatial context, then use `web_search` + `web_extract` for published literature (GSM Bulletins, Springer, AAPG). Note the GEOX gap in output. Published literature is often richer than what GEOX returns for non-standard basins. (2026-07-11: Sarawak Basin — GEOX had no profile, web research produced full strat column + petroleum system.)
2. **Research first** — search for actual published data (formation names, ages, properties). Never start with a template and fill in "TBD."
3. **Verify every entity name** — cross-check block names, structural trend names, field names against published literature. "Block P" was used for a structural feature that isn't a PSC block. This wasted an entire dossier iteration.
4. **Verify every coordinate** — GPS/published map only. "From memory" coordinates were 0.34–0.67° off (Lipad, Maliau, Ranau). In geoscience, this = wrong well = dry hole.
5. **Build with data, not shapes** — start with the stratigraphic column, reservoir properties, source rock parameters. Add the structural framework on top. Not the reverse.
6. **Self-check (rule 7)** — would Raja accept this? If "tak cukup geology," the answer is no.
7. **Label epistemic bands AFTER content exists** — tags wrap claims; they don't generate them.

### Dossier Pattern (Proven 2026-07-11)

When the user asks for a geological/economic dossier on a block or field:

1. **Parallel probe:** GEOX basin + deep_time_state + map_context + WEALTH market data — all in one batch
2. **GEOX fallback:** If basin not loaded, immediately pivot to 3 parallel web searches (stratigraphy, petroleum system, recent activity)
3. **Source extraction:** Pull the 3 most authoritative published papers/reports (GSMBulletin, Springer, PETRONAS press releases)
4. **Structure:** Asset overview → Regional geology → Petroleum system → Economics → Blind spots / what they missed → Recommended actions → Confidence labels per claim
5. **The "what they missed" section is the value-add.** Don't just summarize what's known — analyze what the operator might have overlooked. Use adjacent discoveries, alternative play concepts, and structural/stratigraphic reasoning.
6. **Write to disk:** Save as `forge_work/YYYY-MM-DD/<BLOCK>-DOSSIER.md`. Don't just output to chat — the user will want to reference it later.

### Blind Spots Analysis (Operator Intelligence — Proven 2026-07-11)

When producing a dossier on an operated block, the highest-value section is **"What the operator likely missed."** This separates an intelligence dossier from a summary. Five categories:

1. **Adjacent play blind spot** — plays proven in neighbouring blocks/provinces the operator hasn't tested (e.g., carbonate buildups beneath clastics at the Baram Delta / Luconia transition)
2. **Deeper target blindness** — operators who inherited assets continue the inherited geological model. What's deeper than current producing intervals?
3. **Trap-type bias** — if all discoveries are structural, investigate stratigraphic traps (channel sands, pinch-outs, incised valleys). Modern seismic resolves what vintage 2D couldn't.
4. **Bypassed resource in existing fields** — low-permeability flank zones, unswept compartments, gas-displaced oil beneath gas caps
5. **Adjacent discovery analogues** — recent discoveries in neighbouring blocks prove the petroleum system extends. If the operator hasn't drilled analogous structures, that's a blind spot.

Each blind spot needs: geological reasoning, evidence basis, test data required, epistemic label (SPEC/INT/DER). The blind spots section is always SPEC/INT — its value is generating testable hypotheses.

## Failure Modes Observed (2026-07-07)

| Failure | Root Cause | Fix |
|---|---|---|
| Used "Block P" (doesn't exist) | Assumed user's informal name = PSC designation | Verify block names against published PSC lists |
| Mapped Limbayong→Block G, Bestari→Block X without verification | Assumed structural features map 1:1 to blocks | Only state what's confirmed; leave unconfirmed blank |
| Plotted all coordinates from memory | Didn't search for GPS data first | Search before plot; tag as SPECULATED if no source |
| Built cartoon cross-sections as "interpretation" | Started with template shapes, not data | Start with strat column; add structure on top |
| Epistemic tags on empty content | Tags looked rigorous but wrapped nothing | Rule 8: framework ≠ finding |
| Treated "L-B-P trend" as if it were a block | Conflated structural trend with contractual area | Distinguish trend names from block names explicitly |

## Reference Files

- `references/sabah_strat_data.md` — verified stratigraphic data for NW Sabah deepwater (formations, ages, biostrat, reservoir properties, source rock)
- `references/egs_claim_workflow.md` — GEOX EGS claim registration workflow (create → attach evidence → challenge)
- `references/sarawak_basin_strat_data.md` — Sarawak Basin geological reference: Baram Delta tectonics, Cycle I–VIII stratigraphy, petroleum system (source/reservoir/seal/trap), Central Luconia carbonate play, SK 309/311 field data, recent Baram Province discoveries (2021–2025). Use for any Sarawak offshore dossier or screening memo.

## Output Requirement

Any geoscience artifact must be reviewable by a working geologist without them needing to ask "where's the geology?" — the tagging system sits on top of real technical substance, not replaces it.

## §9. Bid Round / Pre-DR Screening Discipline

> **Origin:** MBR 2026 PETRONAS bid round (Feb 10-11 2026 launch, deadline Oct 1 2026). The deliverable was a 9-block + 6-DRO screening memo built entirely without data room access. A working PETRONAS exploration geologist reviewed it and produced feedback that should anchor every pre-bid screening artifact from now on.

### 9.1 The Synthetic Filter Principle

Synthetic seismic, synthetic well logs, and synthetic rock-physics crossplots are **forward models**, not observations. They are acceptable for **pre-bid screening** (ranking, comparative risk, conceptual filter) as long as every artifact carries an explicit `DER_SYNTHETIC` / `DER_SCREEN` / `SCHEMATIC` epistemic label and a prose statement of what was computed vs measured. They are **NOT** acceptable for drilling location sign-off, full EMV, or any decision where a single wrong answer costs a dry hole.

**Wedge sentence for synthetic-vs-real framing:** *"From a human geologist's POV: acceptable for pre-bid screening. Not sufficient for final subsurface sign-off. No one should sign a drilling location on this alone."*

### 9.2 Per-Artifact Honesty Template

Embed this in every figure caption for a pre-bid screening artifact:
```
Figure N. <description>. [<epistemic label> — <what was modeled vs measured>.]
```
Examples:
- `[DER_SYNTHETIC — not a measured seismic section; forward model from Group E-F impedance + Ricker wavelet]`
- `[INT — simulated log response based on published Malay Basin reservoir properties (Bishop 2002)]`
- `[SCHEMATIC — interpretation based on TGS APGCE 2024 pseudo-3D; not a real seismic line]`

### 9.3 Geological Insights That Work in Pre-Bid Screening

- *"This is the only play in MBR 2026 where all four petroleum system elements (reservoir, seal, charge, trap) are simultaneously supported by physics-based evidence."* — defensible within the synthetic/DER frame you set, but **state the frame**.
- *"Trap integrity is the key subsurface risk"* — always name the specific risk (SGR, fault throw vs sand thickness, seal breach at unconformity) and the data needed to falsify it.
- Charge asymmetry (NW gas-prone vs SE oil-prone) tied to coal/coaly-shale + syn-rift shales — realistic, not generic "good kitchen" language.

### 9.4 What a Working Geologist Will Demand Before Backing BID

State these as "Next Steps" in the proposal. Their absence is the giveaway that the author doesn't know what they're asking a bidder to commit to:

1. Real 2D/3D seismic over the candidate blocks to confirm: anticline closure against faults, crest amplitude behavior (true bright spot vs tuning/noise), gas chimney continuity
2. At least one analogue well with: pressure data in target reservoir, real Vp/Vs and density logs to validate rock-physics clusters
3. Fault seal analysis (SGR, shale smear, fault throw vs sand thickness) on actual mapped faults, not conceptual

### 9.5 Risk Register — The Right Dragons to Name

Each named risk is a potential 888_HOLD signal in the federation. Omit them and the deck reads as marketing:

- Fault seal
- Overpressure
- Gas chimney ambiguity
- Data gaps
- HPHT engineering

### 9.6 "NO BID" Defensibility — Pre-Data Room

A geologist will accept NO BID calls that cite:
- *"Frontier basin — no well control, high dry hole risk, no analogue well data"*
- *"Deepwater block with limited existing seismic coverage — data acquisition cost would exceed capital budget"*
- *"HPHT >4000m with limited HPHT track record"*

Geological humility (admitting the basin isn't calibrated) is a **strength**, not a weakness. Pretending to understand an uncalibrated basin is a **liability**.

### 9.7 The Upgrade Path (Post-Data Room)

What a working geologist will push you to do next once the data room opens:

1. Tie synthetic models to real analogs — use 1-2 real fields to show that synthetic trends reproduce known behavior
2. Quantify uncertainty in synthetic models — show how sensitive bright spots / gas chimneys are to changes in Vp/Vs, porosity, or gas saturation
3. Link accommodation simulation directly to observed stratigraphy — one cross-section or log tie to a real field elevates it from "forward model" to "calibrated forecast"

## §10. Coordinate Verification — Bid Round Specific

> **Pre-data-room constraint:** Real PSC block boundaries are confidential until the data room opens. Coordinates in any pre-bid artifact are **approximate to basin level** unless you have explicit data room access. Tag every block coordinate with `BBOX_FROM_PUBLIC_MBR_LISTING` not `GPS_VERIFIED` or `DATA_ROOM_VERIFIED`. Differentiate "PM447 is in the Malay Basin" (defensible) from "PM447's NW corner is at 104.45°E, 5.20°N" (requires data room).

## Failure Modes Observed (Updated 2026-07-09)

| Failure | Root Cause | Fix |
|---|---|---|
| (Scar #1-6 from prior session) | See table above | See §9.4 for the universal pre-bid fix |
| Synthetic seismic used as if it were a real observation | Forgot to label the epistemic status in the caption | Always use the §9.2 honesty template; one-line `[DER_SYNTHETIC — not measured]` is enough |
| Cartoon cross-section labeled "interpretation" | Started with shapes instead of strat column + log | §9.4 step 1-3: real seismic + analogue well + fault seal first |
| "NO BID" without geological rationale | Risk register omitted | §9.5: name the dragons or admit the basin isn't calibrated |
| "Comprehensive bid" with no data room access implied | Pretended to have real block coordinates | §10: tag every coordinate source, never claim `GPS_VERIFIED` from MBR listing |
| GEOX basin "not found" for target region | GEOX registry doesn't have all basins loaded (Sarawak, Balingian, etc.) | Don't retry. Pivot to `geox_map_context_scene` + web research. Note gap in output. Published literature often richer anyway. |
| WEALTH MCP session validator crash | arifosmcp dependency broken in WEALTH organ | Fall back to `web_search` for market/pricing data. Note the WEALTH gap. |
| Dossier output only in chat, not saved | Didn't write to disk | Always write dossiers to `forge_work/YYYY-MM-DD/<BLOCK>-DOSSIER.md` — user will reference later |
