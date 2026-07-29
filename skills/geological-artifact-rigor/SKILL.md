---
name: geological-artifact-rigor
description: "Standing instruction for all geoscience artifacts — panels, dossiers, maps, cross-sections"
version: 1.2.0
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

### 8. Human Geologist Language (No AI Jargon)
Arif's standing directive: **"Full human geologist cognitive. No AI jargons."** This means:

- Use natural geological language: "batupasir turbidit," "jujukan delta yang progradasi," "perangkap sesar dengan dip closure" — not "the depositional system exhibits a progradational parasequence stacking pattern"
- Avoid corporate/AI-speak: no "leverage insights," "holistic approach," "streamline workflow," "paradigm shift" — say what the rocks do
- Tables and numbered lists beat narrative paragraphs for data
- Every section starts with the key takeaway in one sentence — a working geologist skims before they read
- If Malay terminology fits, use it — especially for Sabah/Sarawak basins. "Sesar normal" is clearer than "extensional fault" for a Malaysian audience
- The artifact should read as if written BY a geologist FOR a geologist — not as if an AI translated a geology textbook through corporate filter
- Self-check: "Would I be embarrassed to hand this to a PETRONAS exploration manager?" If yes, the language is wrong.

### 9. Epistemic Labels: Framework ≠ Finding
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

1. **Probe GEOX first** — call `geox_basin` for the target region. If it returns "Basin data not found" or `LANE_ENFORCEMENT` (governed session required), DON'T retry. Pivot: use `web_search` + `web_extract` for published literature (GSM Bulletins, Springer, AAPG). Note the GEOX gap in output. Published literature is often richer than what GEOX returns for non-standard basins. For PSM-specific deliverables, forward-model burial curves, Ro gradients, and generation timing from published data — the workflow is proven. (2026-07-11: Sarawak Basin — GEOX had no profile, web research produced full strat column + petroleum system. 2026-07-22: Sabah PSM — GEOX LANE_ENFORCEMENT, built complete 6-figure dossier from published data.)
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
| Flat rectangular blocks used as geological layers | Used matplotlib Rectangle patches — violates Rule 2 cartoon geometry | Use wavy polygon helpers with noise (`layer_polygon` pattern); see `references/cross-section-generation.md`. Or use hand-built SVG with bezier curves (`Q`/`C` path commands) for dark-theme federation visuals — see `references/svg-cross-section-generator.md`. |
| Cross-section reads as "infographic" not "scientific figure" | Dark background + smooth sine waves without geological detail | Add fault symbols (thrust sawteeth, normal ticks), Moho lines, depth scale, compass arrows, region labels. White background for journals; dark acceptable for public communication. |
| Epistemic tags on empty content | Tags looked rigorous but wrapped nothing | Rule 9: framework ≠ finding |
| Treated "L-B-P trend" as if it were a block | Conflated structural trend with contractual area | Distinguish trend names from block names explicitly |

## Reference Files

- `references/sabah_strat_data.md` — verified stratigraphic data for NW Sabah deepwater (formations, ages, biostrat, reservoir properties, source rock)
- `references/cross-section-generation.md` — proven Python/matplotlib pattern for generating professional geological cross-sections: wavy layer boundaries, fault symbols (thrust sawteeth, normal ticks), Moho/COB conventions, hatch pattern reference, dark vs light background guidance. Use when creating any code-generated geological visualization.
- `references/sarawak_basin_strat_data.md` — Sarawak Basin geological reference: Baram Delta tectonics, Cycle I–VIII stratigraphy, petroleum system (source/reservoir/seal/trap), Central Luconia carbonate play, SK 309/311 field data, recent Baram Province discoveries (2021–2025). Use for any Sarawak offshore dossier or screening memo.
- `references/psm-figure-patterns.md` — reusable matplotlib patterns for petroleum system modeling deliverables: burial history curves, Ro vs depth plots, hydrocarbon generation timing charts, stratigraphic columns, basin cross-sections, PSM toolchain diagrams. Proven 2026-07-22 GEOX PSM Sabah dossier (6 figures, Mode B dark theme). Use for any PSM showcase or basin modeling artifact.
- `references/svg-cross-section-generator.md` — hand-built SVG geological cross-section rendered to PNG via Playwright. Use when matplotlib/GEOX patterns unavailable or dark-theme federation visuals preferred. Includes lithology pattern SVG templates (granite, saprolite, alluvium, fault zone), wavy formation boundaries, fault motion indicators, water table, depth scale, legend. Proven 2026-07-28 (Lenggeng NS cross-section for Aliff). Alternative to matplotlib for quick visual delivery via chat.

## §11. Agentic Basin Report Generation (Hound-powered)

> **Origin:** 2026-07-29 — Arif requested an "agentic PUNYA version" of Hakimi's 40-page manual Kinabalu Basin report for UTP intern comparison. Full report generated in ~3 min from 6 parallel sources → structured markdown → PDF delivered as MEDIA file.

### 11.1 When to Use

- User asks for a geological basin/field report following a standard academic/industry outline
- User wants an "agentic version" — multi-source, structured, PDF-deliverable
- Intern report, basin screening memo, technical dossier, or literature-backed synthesis
- Requires integration from multiple independent sources, not a single DB query

### 11.2 The Workflow

```
Phase 1: Parallel Search (Hound smart_search × 3 angles)
   ↓
Phase 2: Multi-Source Extraction (Hound smart_fetch — PDF, HTML, official)
   ↓
Phase 3: Cross-Reference + Epistemic Tagging 
   ↓
Phase 4: Structured Report (standard geological outline)
   ↓
Phase 5: PDF Conversion (pandoc + weasyprint) → MEDIA delivery
```

#### Phase 1 — Parallel Search

Run 3 concurrent `mcp__hound__mcp_smart_search` targeting different angles:

| Angle | Pattern | Example |
|---|---|---|
| Basin identity | `"[basin] geology stratigraphy structure tectonic"` | `"Kinabalu Basin geology stratigraphy"` |
| Petroleum system | `"[basin] petroleum geology hydrocarbon"` | `"Kinabalu Basin petroleum"` |
| Recent activity | `"[basin] discovery 202[4-6]"` | `"Kinabalu Basin discovery"` |

Each batch: `max_results=10`, `freshness=year`.

#### Phase 2 — Multi-Source Extraction (parallel fetch)

From results, pick 3-6 most authoritative sources, fetch **all in parallel** via one `mcp__hound__mcp_smart_fetch` call with multiple URLs. Proven up to 6 simultaneous fetches (2026-07-29 Kinabalu dossier: 6 PDFs/HTML in ~3s).

| Source type | Format | Quality signal |
|---|---|---|
| PETRONAS/official portal | HTML → markdown | `content_ok: true` |
| GSM Bulletin PDFs | PDF (auto-extracted) | `quality_score: 1.0` = real text; ≤0.5 = scanned |
| Conference papers (EAGE, EarthDoc) | HTML/PDF | Check `page_type` — "list" = paywalled abstract only |
| Journal articles | HTML/PDF | Fetch preprint from ResearchGate/SemanticScholar if paywalled |
| Encyclopedia | HTML → markdown | Cross-check for citation validity |

**Scanned PDF detection:** `quality_score` ≥0.9 means extractable text. ≤0.5 means image-based — use `vision_analyze` on individual pages instead.

#### Phase 3 — Epistemic Tags

| Tag | When |
|---|---|
| CONFIRMED | ≥2 independent sources agree |
| WELL-ESTABLISHED | Published consensus |
| EMERGING EVIDENCE | Recent, limited verification |
| PLAUSIBLE | Single source, not confirmed |
| ESTIMATE | Quantitative, uncertain |
| INTERPRETATION | Geological judgment |
| UNKNOWN | Gap, unresolved debate |

Build a **source provenance map** (table: source → sections contributed).

#### Phase 4 — Report Structure

Standard outline (override if user provides specific):

1. **Introduction** — Location, significance, scope
2. **Objectives** — 3-5 measurable targets
3. **Geological Setting** — Regional geology, structural setting, stratigraphy
4. **Methodology** — Data sources, workflow, epistemic framework
5. **Results** — Well log, seismic, petrophysical analysis
6. **Discussion** — Tectonic evolution, petroleum systems, regional implications, analogs
7. **Conclusion** — Key findings with evidence level per finding
8. **References** — Min 10, with URLs + years

**Formatting:** tables for comparison data, every section starts with key takeaway, appendix includes source provenance map and epistemic note: "COMPILATION of public sources. Not proprietary data."

#### Phase 5 — PDF Conversion + Delivery

```bash
pandoc REPORT.md -o REPORT.pdf \
  --pdf-engine=weasyprint \
  --metadata title="Title"
```

CSS warnings from weasyprint (`unknown property`, `invalid media type`, `overflow-x: auto`) are **non-critical** — ignore them. File size: 50-200 KB for ~10-page equivalent.

**Delivery channels (in priority order):**

1. **Telegram MEDIA** — `MEDIA:/absolute/path/REPORT.pdf` in response. Native file delivery, best for quick sharing.
2. **Email attachment** — via Brevo API (see `agent-email-transport` skill). If curl returns IP-whitelist error but Brevo token is valid, retry with `python3 -c "import urllib.request, json, os, base64; ..."` — Python's urllib may route differently than curl through the same IP and succeed.
3. **Write to forge_work** — always save the source `.md` and `.pdf` to `forge_work/YYYY-MM-DD/` for audit trail.

### 11.3 Agentic vs Manual

| Aspect | Manual | Agentic |
|---|---|---|
| Research | Read PDFs one at a time | 3-6 sources parallel in <30s |
| Cross-ref | Manual connections | Auto cross-reference between papers |
| Citations | Manually typed | Every claim grounded in live URL |
| Speed | Days-weeks | ~3 min (research + compile + PDF) |
| Uncertainty | May hide gaps | Explicit epistemic tags |
| Update | Full re-edit | Re-fetch + re-compile in minutes |

### 11.4 Pitfalls

- **GEOX MCP session auth** — GEOX returns `SESSION_MISSING` (no session_id), `SESSION_INVALID` (format not SCT/SEAL-*), or `LANE_ENFORCEMENT` (session not governed). **Don't retry** — No amount of retrying fixes auth. Pivot immediately to Hound MCP (smart_search + smart_fetch). If arifOS (port 8088) is healthy, one could request a governed session, but this is T3/888_HOLD territory. As of mid-2026, public-facing literature is richer than GEOX output anyway.
- **Paywalled/abstract-only pages** — EarthDoc returns `page_type: "list"` with only the abstract. Don't re-fetch the same URL. Search for preprints on academia.edu, ResearchGate, Semantic Scholar instead. Fetch direct PDFs when URL ends `.pdf`.
- **Scanned PDFs** — check `quality_score` in smart_fetch response. Use `vision_analyze` if scan-based (quality_score ≤0.5).
- **Scanned PDFs** — check `quality_score` in smart_fetch response. Use `vision_analyze` if scan-based (quality_score ≤0.5).
- **Public ≠ proprietary** — carry explicit disclaimer. Don't fabricate well logs or petrophysics from internal databases.
- **User-provided outline takes priority** — if user gives a specific structure (screenshot, photo, whiteboard), follow that, not the default template.
- **Epistemic tags wrap real content** — Rule 9: framework ≠ finding. Don't let tagging create the impression of rigor the geology doesn't have.
- **BM-English for Malaysian audience** — For UTP intern reports or Malaysian geologist audience: RASA voice — think in receipts, speak in consequences.

### 11.5 Reference Files

- `references/kinabalu_basin_data.md` — research data pack from 2026-07-29 session: 6 sources cross-referenced, source provenance map, petrophysical estimates, tectonic event table, stratigraphic column, production status. Reusable for any future Sabah/NW Borneo basin report.

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
| GEOX tools return LANE_ENFORCEMENT (session_id required) | Tools in reasoning lane need governed session via `arif_init(mode=init)` | Same pivot as "basin not found" — web research + published data. The PSM workflow still works from published data alone (burial curves, Ro gradients, generation timing can be forward-modeled). See references/psm-figure-patterns.md. |
| WEALTH MCP session validator crash | arifosmcp dependency broken in WEALTH organ | Fall back to `web_search` for market/pricing data. Note the WEALTH gap. |
| Dossier output only in chat, not saved | Didn't write to disk | Always write dossiers to `forge_work/YYYY-MM-DD/<BLOCK>-DOSSIER.md` — user will reference later |
