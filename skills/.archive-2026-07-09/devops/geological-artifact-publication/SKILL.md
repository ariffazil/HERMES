---
name: geological-artifact-publication
description: Produce publication-quality geological artifacts — to-scale cross-sections, 3D block diagrams, and citation-rich PDF reports — for arifOS / GEOX federation output. Use when Arif asks for a "real block diagram", "publication PDF", "geological model diagram", "deep research paper" on a tectonic/stratigraphic topic, or wants a Sabah/Malay Basin/Borneo deliverable with provenance and SHA256 receipts.
---

# Geological Artifact Publication

## Trigger
Arif asks for any of:
- "Make a real block diagram" / "publication-quality cross-section" / "geological model diagram"
- "Full PDF with deep research" / "scientific report on [basin/tectonic topic]"
- "Geological model with real data" / "to-scale stratigraphic column"
- Sabah / Kinabalu / Malay Basin / Borneo / SE Asia tectonic deliverable
- Any request that needs both a visual artifact (PNG) AND a written artifact (PDF)

## The Pattern (proven 2026-07-03, Kinabalu Two-Oceanics, 15-page PDF + 5 figures)

### Step 1 — Research before drawing (F2 TRUTH honored)
1. Check local archives FIRST: `/root/GEOX/forge_work/`, `/root/GEOX/docs/eureka_insights/`, `/root/forge/`, `/root/HERMES/cron/output/`. The arifOS box has 5+ years of sealed briefs, falsification capsules, and eureka audits. If the topic is Kinabalu/Sabah, expect to find `GEOX-LC-001` and Sabah strat ontology (`geox://resources/ontology/sabah_basin_strat.yaml`).
2. Web search/extract (Tavily) is often down (HTTP 402) — don't burn 4+ calls assuming it's up; one probe and pivot.
3. Pull existing claim/audit receipts from GEOX EGS if a prior session left one (claim IDs are 16-hex like `935be7ceb54241c2`).
4. Build the citation list FIRST. Aim for 8-20 real papers, not "et al." placeholders. Canonical Kinabalu references: Hall (2013) J. Asian Earth Sci. 76:399-411; Balaguru & Hall (2009) AAPG #30084; Gilligan et al. (2026) nBOSS; Krebs (2011) PETRONAS; Franke et al. (2008) Mar. Petrol. Geol. 25:606-624; Cottam et al. (2013) J. Geol. Soc. 170:805-816; Sidek & Hamzah (2018); Tongkul (1994) Tectonophysics 235:131-147; Rangin et al. (1990); Taylor & Hayes (1983).

#### Path B: SVG→Playwright→PNG (for schematic/interpretive cross-sections)

Use when the cross-section is **interpretive** (not tied to exact well data) and you need precise control over geological symbology — patterns, annotations, strain arrows, depth-partitioned layers.

**Proven:** 2026-07-05, Sabah NE-SW cross-section (Semporna → Dangerous Ground).

```html
<!-- 1. Build HTML/SVG file with geological cross-section -->
<!--    - Use <pattern> for lithology fills (sediment lines, granite dots, mantle diagonals) -->
<!--    - Use <marker> for arrow heads (compression, extension, drip) -->
<!--    - Use <path> for Moho surface and layer boundaries -->
<!--    - Serif fonts (Times New Roman / DejaVu Serif) -->
<!--    - White background, muted earth-tone palette -->
<!--    - Legend, depth scale bar, horizontal scale bar -->
<!--    - Epistemic labels (OBS/DER/INT) on annotations -->
```

```python
# 2. Render SVG to PNG via Playwright (headless Chromium)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    page.goto('file:///root/cross_section.html')
    page.wait_for_timeout(1000)
    page.screenshot(path='/root/cross_section.png', full_page=True)
    browser.close()
```

**Why SVG over matplotlib for schematic cross-sections:**
- Precise control over geological patterns (hatching, stippling, grain fills)
- Native support for complex annotations (rotated text, curved arrows, callout boxes)
- Easy to iterate (edit HTML, re-render — no matplotlib state management)
- Output is crisp at any resolution (vector source → rasterized at render time)

**Why matplotlib over SVG for data-driven cross-sections:**
- Real coordinate data (well picks, seismic horizons, GPS vectors)
- Programmatic geometry (Gaussian peaks, spline interpolation)
- Integration with scientific Python stack (numpy, scipy)

**The decision rule:** If you're drawing from a model/data → matplotlib. If you're drawing from a concept/interpretation → SVG.

#### Step 2a (matplotlib path) — Topography
3. **Crustal surfaces (to scale):**
   - Moho: `24 + 8*exp(-((x-130)/40)**2) - 2*exp(-((x-260)/40)**2)` (thick Crocker, thinned Kinabalu per Gilligan 2026)
   - Ophiolite basement top: 5-7 km, Vp 5.0-6.5 km/s
   - Jurassic carbonate décollement: continuous 12-21 km depth band
4. **Stratigraphic units (in age order, with Sabah ontology Vp ranges):**
   - Panas Fm 40-28 Ma, Vp 3.8-4.3 (Crocker turbidites wedge)
   - Gomantong Limestone 23-16 Ma, Vp 4.0-5.5
   - Labang Shale 16-12 Ma, Vp 2.8-3.5 (**PRIMARY REGIONAL SEAL** — call this out in legend)
   - Sandakan Fm 12-2.6 Ma, Vp 2.0-2.8
5. **Pluton:** Kinabalu granite as inverted teardrop, peak 4.095 km, root to -15 km, ρ=2.64 g/cm³, color #e07a5f. Add heat halo (3 ellipses with decreasing alpha) to show metamorphic aureole.
6. **Subduction arrows:**
   - Proto-SCS relict slab (west, depth 15-60 km): downward arrow curving south, label "Past Proto-SCS subduction → S" with stroke path effect
   - Celebes Sea oceanic crust (east, x>300): rollback arrows in red (#c0392b) curving south
   - Sulu Arc: label + northward arrow at x=345
7. **Scale bar + 1:1 VE note + legend** (ncol=2, framealpha=0.92, edgecolor earth-tone)
8. **Label every geographic feature** with `path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]` so text reads on any background.

### Step 3 — Build the regional tectonic map (matplotlib, 2D)
NOT a true 3D block — a top-down tectonic map with:
- Bathymetry polygons (South China Sea, Celebes Sea, Sulu Sea) in light blue (#a8d0e6, #7eb5d6, #5a9bc4)
- Land masses (Borneo brown #c9a574, Dangerous Grounds hatched yellow #e8c890, Sulu Arc purple #5a4a8a, Philippines #8a7aaa)
- Mt Kinabalu as red star marker (markersize=40, edgecolor black, zorder=10) + white-text red-box label
- A-A' cross-section line as thick red line
- Subduction/rollback arrows with kinematic labels
- North arrow, scale bar, legend (place legend in lower-RIGHT to avoid covering sea polygons — common pitfall)
- Coordinates: longitude/latitude degrees, grid lines, ticks every 2°

### Step 4 — Build the timeline (matplotlib)
1. Backbone: horizontal line 40→0 Ma
2. Tick marks at 40, 30, 20, 15, 8, 7, 0 with bold labels
3. 3 horizontal bars (steps) with hatch patterns:
   - Step 1: `#8b6a3a`, hatch `//` (Crocker / subduction)
   - Step 2: `#e07a5f`, hatch `xx` (rollback / melting)
   - Step 3: `#3d6e4f`, hatch `..` (isostatic uplift)
4. Key event markers: scatter triangles at 15 Ma (collision) and 7.5 Ma (granite emplaced)
5. Hide top/right/left spines; bottom spine in earth-tone
6. Place a "FALSIFIED" red callout over the continental-subduction hypothesis

### Step 5 — Build the rock-physics contrast (matplotlib, bar charts)
1. Use 5 subplots (Vp, Vs, ρ, Δt, Vp/Vs) in one row
2. Bars colored: granite `#d05050`, sediment `#a8845a` (or per-spec)
3. Add delta annotation in yellow-box on each subplot: "+66%", "+78%", etc.
4. Footer with interpretation (seismic detectable, crystalline, silica-rich)
5. Vp/Vs < 2.0 → felsic granite; > 2.0 → sedimentary/metamorphic

### Step 6 — Build the model comparison table (matplotlib)
1. NOT a real matplotlib `table()` — use manual rect+text grid (avoids header-overlap bug)
2. 5 model rows × 6 element columns
3. Header row in dark blue (#1e3a5f) with white bold text
4. Model name column in deep blue (#0a4d8c) white bold
5. Cells colored green (#c8e6c9 = match), yellow (#fff9c4 = partial), red (#ffcdd2 = falsified)
6. Use `bbox=dict(boxstyle='square,pad=0.3', fc=color, ec='gray', alpha=0.85)` for every cell
7. Legend at bottom: ✔ YES / ✓ partial / ✘ NO
8. Calculate cell coordinates with `x_start + sum(col_widths[:c])` pattern

### Step 7 — Visual audit loop (CRITICAL — proven necessary 2026-07-03)
**Always visually inspect each figure with `vision_analyze` before assembling the PDF.** Pitfalls caught:
- Title blocks overlapping Kinabalu labels → move title to upper-LEFT corner
- Annotation labels overlapping filled polygons → add `bbox=dict(fc='white', ec='black', alpha=0.9)`
- Laya-laya Fault Zone rotated text getting clipped → place label horizontally to the SIDE
- Legends in `loc='lower left'` covering sea polygons on regional maps → use `loc='lower right'` with `bbox_to_anchor=(0.99, 0.02)`
- Header rows in matplotlib tables overlapping data cells → use manual rect+text grid with proper coordinate calculation
- Common matplotlib typo: `bboxdict=None` — the correct kwarg is just `bbox=dict(...)` (no `bboxdict` key)

### Step 8 — Save all figures
```python
plt.savefig('/tmp/kinabalu_pdf_figures/figN_name.png', dpi=200, bbox_inches='tight', facecolor='white')
```
Use `dpi=200` for sharp prints. Facecolor='white' ensures no transparency in PDF embedding.

### Step 9 — Build the PDF

**Two paths — pick based on deliverable type:**

| Deliverable | Tool | Why |
|---|---|---|
| White-theme scientific PDF (publication) | **weasyprint** | HTML-driven, two-column prose, `<table>` layout, CSS `@page` |
| Dark-themed intelligence dossier | **reportlab** | Programmatic canvas control, `onPage` dark background, gold accents, precise header/footer |

**weasyprint path** (white-theme scientific):

`reportlab` is **not** installed in the GEOX venv (PEP 668 blocks system pip; venv pip often restricted too). The proven stack on this box:

| Tool | Status | Use for |
|---|---|---|
| `weasyprint` (system: `/usr/local/bin/weasyprint`, v68.1) | ✅ available | **HTML → PDF** — the working path |
| `pandoc` (`/usr/bin/pandoc`) | ✅ available | Markdown → HTML, then weasyprint |
| `google-chrome` (v150, headless) | ✅ available | `chrome --headless --print-to-pdf=out.pdf` — second option |
| `matplotlib` (3.11+, GEOX venv) | ✅ available | All scientific figures |
| `PIL` (Pillow 12.3+) | ✅ available | Image preprocessing |
| `reportlab` (4.4+) | ✅ available | Dark-themed dossiers, programmatic page templates |

The pattern that works (proven 2026-07-03, 15-page Kinabalu PDF, 1.5 MB):

```bash
# 1. Build all figures as matplotlib PNGs (to /tmp/kinabalu_pdf_figures/)
# 2. Write HTML manuscript at /tmp/.../manuscript.html with <img src="figN.png">
# 3. Convert to PDF — base_url resolves relative image paths:
weasyprint /tmp/kinabalu_pdf_figures/kinabalu_two_oceanics_manuscript.html \
           /root/kinabalu_two_oceanics_full.pdf
```

Or programmatically:
```python
from weasyprint import HTML
HTML(filename='/tmp/.../manuscript.html',
     base_url='/tmp/kinabalu_pdf_figures/').write_pdf('/root/output.pdf')
```

**CSS tips for scientific PDFs (weasyprint 68.1):**
- `@page { size: A4; margin: 2cm 1.8cm; @top-center { ... } @bottom-center { content: counter(page) " / " counter(pages); } }`
- `box-shadow` is **ignored** by weasyprint — harmless warning, don't fix
- Inline images with `<img src="fig.png">` and `max-width: 100%` so 3971×964 wide aspect ratios fit A4
- `column-count: 2` works for prose compression
- `page-break-before: always` on section headers to force clean page breaks
- Use `<table>` with `border-collapse: collapse` and explicit `th { background: #1e3a5f; color: white; }`
- Footer motto via `@bottom-right { content: "DITEMPA BUKAN DIBERI"; }`

PDF structure (proven 15-page template, Kinabalu Two-Oceanics 2026-07-03):
1. **Cover** — title, subtitle, author, GEOX claim ID, abstract in yellow box, keywords
2. **§1 Core Eureka** — contrast score table (4-5 rows: hypothesis, score, violations, status)
3. **§2 Regional Context** — Figure 1 regional tectonic map
4. **§3 Cross-Section A-A'** — Figure 2 to-scale block diagram + red "Geophysical discriminator" box
5-6. **§4 Rock-Physics** — Figure 3 (5-panel bar chart) + detailed table + Vp/Vs interpretation
7. **§5 Three-Step Evolution** — Figure 4 timeline with Steps 1-2-3 + "Falsified" callout
8. **§6 Jurassic Carbonate Décollement** — mechanism + KT-7 Franke RC reconciliation
9. **§7 Biostratigraphic Tie** — 12-row NN-zone table (NN10A–NN11A = 8.6–7.7 Ma)
10-11. **§8 Falsification Framework** — GEOX-LC-001 4-hypothesis table + killer tests + acquisition sequence
12. **§9 Model Contrast** — Figure 5 (5×6 model comparison matrix)
13-14. **§10-11 Receipts & Conclusions** — SHA256 + GEOX claim + arifOS judgment chain + 6 conclusions
15. **§12 References + Footer** — 14 citations + DITEMPA BUKAN DIBERI + arifOS Federation signature

### Step 10 — Verify and deliver
```bash
# Verify PDF
pdfinfo /root/output.pdf | grep -E "Pages|File size"
sha256sum /root/output.pdf
pdftotext /root/output.pdf - | head -20   # confirm content

# Render a page to PNG for visual audit
pdftoppm -png -r 100 -f 5 -l 5 /root/output.pdf /tmp/preview/p5
vision_analyze(image_url="/tmp/preview/p5-05.png", question="...")
```

Standard deliverable:
- 1 high-res PDF (1-2 MB, 10-20 pages) with full text + tables + audit trail
- SHA256 receipt embedded in §10 of the PDF
- 5 figure PNGs at 200 dpi (~200-440 KB each, total ~1.5 MB)
- Optionally: Telegram-friendly PNG variants (≤ 600 KB)

## The v3 → v4 Falsification-Discipline Lesson (Learned 2026-07-03, ChatGPT Review)

The Kinabalu Two-Oceanics v3 manuscript was internally audited by a peer reviewer (ChatGPT, 2026-07-03) and the verdict was **PARTIAL EUREKA — overclaimed**. Four specific overclaims were caught:

| Overclaim (v3) | Correction (v4) |
|---|---|
| "Continental crust never subducted" — absolute, falsifiable-and-wrong | "Continental crust did not behave like active dense slab subduction — it collided, underthrusted at shallow depth, shortened, and jammed the system" |
| "Jurassic carbonate décollement" stated as fact | Stated as **HYPOTHESIS**, with explicit killer tests pending |
| "Kinabalu uplift = granite density contrast alone" | Multicausal: extension + lithospheric drip/delamination + isostasy + erosion + pluton buoyancy |
| "Active oceanic slab today beneath Sabah" | "Post-subduction interference overprint on a frozen Proto-SCS geometry" |

**The rule:** Before publishing any geological claim as fact, run this falsification checklist:
1. Does the headline use absolute language ("never", "always", "all", "none")? → Reframe to "did not behave like X" or "is not active Y".
2. Is the mechanism reduced to a single cause? → Multicausal framing is almost always more honest.
3. Are the rival hypotheses named? → If not, the claim is overclaimed.
4. Are the killer tests named? → If not, the claim is unfalsifiable.
5. Has a peer reviewer (human or LLM) critiqued it post-draft? → If not, treat v1 as draft.

**In v4, the GEOX claim `7103fbb9394b4f23` was created with this discipline applied from the start:** 10 evidence attachments including 4 marked `supporting=False` (the corrections), and a `geox_egs_claim_challenge` from `reviewer_chatgpt_2026-07-03` as a permanent piece of provenance. Confidence dropped from 0.72 → 0.50. That drop is **strength, not weakness** — a lower-confidence claim with clean falsification tests is more valuable than a high-confidence myth.

**The institutional pattern (per ChatGPT's Calhoun/Universe-25 translation, validated as institutional metaphor):** Resources + committees + career dependency + citation hierarchy + operational pressure − falsification courage = epistemic sink. The cure is **institutions that require falsification tests before budget**, not the absence of institutions. The GEOX-LC-001 4-hypothesis matrix is exactly this discipline. Your v4 manuscript should embed a §0 Falsification section that names the rivals and the killer tests BEFORE the narrative, not after.

## Step 1b — Data-Driven Cross-Section (from existing document)

When the source is a **document** (PDF, synthesis paper) rather than raw well/seismic data, use the data-driven pattern: `pdftotext` → extract structural elements → `np.piecewise` arrays → `fill_between` layers. See `references/data-driven-crosssection-pattern.md` for full workflow and pitfalls (especially: don't call piecewise functions from piecewise functions — compute arrays independently, then combine with `np.minimum`/`np.maximum`).

## Step 0b — GEOX Audit (when auditing a scientific document's claims)

When Arif asks to "audit" or "review" a document using GEOX tools, use the 7-step methodology: forbidden_claims_scan → contrast_detect → rock_physics → seismic_compute → deep_time_state → evidence → biostrat_ruling_check. See `references/geox-audit-methodology.md` for the full pipeline and which GEOX tools implement which APEX Theory claims.

## Dark-Themed Intelligence Dossier (reportlab)

When the deliverable is an **internal dossier** (not a publication for external review), use a dark theme instead of white-background scientific style.

**When to use dark theme:** Intelligence briefings, competitive analysis, "impress a colleague" deliverables, anything screen-first (Telegram, dashboards).
**When to use white theme:** Journal publications, conference submissions, formal scientific reports for external stakeholders, anything printed.

### reportlab Dark Dossier Pattern (proven 2026-07-07, Block P Sabah, 10 pages, 946 KB)

**Color palette (geological dark):**
```python
DARK_BG = HexColor('#0d1117'); PANEL_BG = HexColor('#161b22')
GOLD = HexColor('#f0a500'); AMBER = HexColor('#ffa657')
GREEN = HexColor('#3fb950'); BLUE = HexColor('#58a6ff'); RED = HexColor('#f85149')
TEXT_LIGHT = HexColor('#e6edf3'); TEXT_DIM = HexColor('#8b949e'); BORDER = HexColor('#30363d')
```

**Page template:** Use `BaseDocTemplate` with `onPage=self.draw_background` that draws dark rect + gold-accent header/footer bars. Frame margins: 2cm sides, 2.5cm top, 2cm bottom.

**Key style patterns:**
- Title: fontSize=28, GOLD, centered
- H1: fontSize=18, GOLD, spaceBefore=8mm
- Body: TEXT_LIGHT, justified, fontSize=10, leading=14
- Quote boxes: AMBER text, GOLD border, '#1a1500' backColor (gold-tinted highlight)
- Talk boxes: GREEN text, GREEN border, '#0d1f0d' backColor (conversation starters)
- Tables: ROWBACKGROUNDS alternating PANEL_BG / '#1a1f28', header '#1a2332'

**Figure generation for dark theme:**
```python
plt.rcParams.update({'figure.facecolor': '#0d1117', 'axes.facecolor': '#0d1117',
                     'text.color': '#e6edf3', 'axes.edgecolor': '#30363d', 'grid.color': '#21262d'})
# ALWAYS use path_effects for label readability:
ax.text(x, y, label, path_effects=[pe.withStroke(linewidth=3, foreground='#0d1117')])
```

**Dossier structure (10-page template):** Cover → TOC → 6 content sections (each with figure + table + insight) → Talking Points (green callout boxes) → References.

**Pitfall:** reportlab Helvetica-Bold must be hyphenated (not 'Helvetica Bold' — space breaks it). For CJK/Arabic, fall back to weasyprint.

## Tectono-Stratigraphic Multi-Panel Layout

When presenting **multi-stage tectonic evolution**, use a 2D grid: columns = time slices, rows = vertical scale levels.

**Proven layout (2026-07-07, NW Sabah PSCS→NSPW→Rotan):** 5 columns × 3 rows:
- Row 0: Lithosphere (mantle + slab) — plate-scale geometry
- Row 1: Crust/Wedge — structural style, detachments, mobile shales
- Row 2: Basin/Stratigraphy — reservoir, seal, charge, facies

Each cell is a mini cross-section showing that level at that time step. Consistent colors across all cells (NSPW always green, fossil slab always brown, reservoirs always gold). See `references/tectono-strat-panel-pattern.md` for the full implementation and NW Sabah example.

**Style:** No axes ticks (conceptual, not to-scale). Stage titles with age + event. Row labels for vertical scale. `fill_between` with Gaussian profiles for structural shapes. `path_effects` stroke on all labels. Time arrow at figure bottom.

### v2: Epistemic-Labeled Governance-Grade Panel (proven 2026-07-07)

The v2 panel adds **epistemic confidence tags per cell** (CLAIM/PLAUSIBLE/ESTIMATE/HYPOTHESIS/SCHEMATIC) with source citations and a color-coded legend. This makes the panel suitable for EGS governance and board-level decks. Implementation and full color system in `references/tectono-strat-panel-pattern.md` §v2.

**The epistemic labels:**
| Label | Color | Meaning |
|---|---|---|
| CLAIM | Green #3fb950 | Well supported by published data |
| PLAUSIBLE | Blue #58a6ff | Consistent, not uniquely constrained |
| ESTIMATE | Amber #d29922 | Timing/numbers approximate |
| HYPOTHESIS | Red #f85149 | Conceptually sound, not proven at scale |
| SCHEMATIC | Gray #8b949e | Simplified cartoon |

**888_HOLD pattern:** HYPOTHESIS boxes should be flagged `requires_888_hold: true` in the JSON model, with a reason explaining what needs human confirmation before irreversible decisions.

**GEOX-EGS integration:** After building the visual panel, mint each cell as a GEOX-EGS JSON object for governance. See `references/geox-egs-claim-minting.md` for the full workflow: 15 boxes → JSON → EGS claim registration → evidence attachment. The visual panel is the human front-end; the JSON is the queryable model; EGS is the governance backbone.

## E&P Bid Round / Licensing Round Artifacts (new 2026-07-09)

When Arif asks for a geological bid assessment for a licensing round (e.g. Malaysia Bid Round, Indonesia bidding, SE Asia exploration offers), produce **5 standard figures** using the `templates/mbr_figures.py` script:

| # | Figure | Purpose | Epistemic |
|---|---|---|---|
| 1 | Synthetic seismic section | Show target play geometry (anticline, strat trap, etc.) | DER_SYNTHETIC |
| 2 | Synthetic well log panel | 4-track log (GR, Vp, Density, Porosity) with reservoir picks | DER_SYNTHETIC |
| 3 | Stratigraphic correlation panel | Multi-well tie across basin with play element annotations | DER_INTERPRETED |
| 4 | Rock physics crossplot | Vp/Vs vs Density with reservoir/seal/source clusters | DER_SYNTHETIC |
| 5 | Play fairway map | Basin extent with play zones, block locations, DROs | SCHEMATIC |

**Workflow:**
1. Run `templates/mbr_figures.py /tmp/figures/` to generate all 5 PNGs.
2. Embed in HTML manuscript via `<img src="figN.png">` with figure captions.
3. Convert with weasyprint → PDF (dark theme, epistemic labels).
4. Deliver via artifact courier.

**Pitfalls:**
- Never label synthetic seismic as "real" or "acquired" — always DER_SYNTHETIC.
- Play fairway maps are SCHEMATIC — coordinates are NOT to PSC boundary scale.
- Well log panels use DEMO_WELL_A/B LAS files as basis — not real wells.
- Rock physics parameters should trace back to actual GEOX tool output (geox_egs_rock_physics).
- WEALTH economic primitives (EMV, EVOI, Kelly, bid_surface) go in the text tables, not the figures.
- Arif wants **visuals** not text tables — "Give me the visual here" is a recurring signal. If the PDF is text-only, generate figures first.

---

## Pitfalls

0. **VERIFIED COORDINATES ONLY — NEVER plot geological features from memory.** This is the cardinal sin in GEOX. Wrong location = wrong well = dry hole = USD 50-100M burned. Every feature on a geological map must have coordinates sourced from: GeoNames (cities), published PSC maps (block boundaries), peer-reviewed literature (structural features), or GEOX tools (deep_time_state, basin_profile). If you cannot verify a coordinate, DO NOT PLOT IT — leave a gap and note "UNVERIFIED" rather than placing it from memory. Proven lesson 2026-07-07: NSPW domain was plotted ~1-2° south and east of its real position; West Baram Line was placed at 5.5°N instead of ~4°N; Ranau was shifted 0.8° east. All from memory, all wrong. Additionally: NEVER relabel PSC blocks without verifying which operator/field is actually in which block (Block P ≠ Block K ≠ Block H — each has different operators, different discoveries, different coordinates). When in doubt, search for PETRONAS MPM PSC boundary maps or ask Arif.
   - **Coordinate verification is MANDATORY** before plotting any geological feature on a map. "Roughly correct" = dry hole = millions lost. Every coordinate must have a **source**: GPS measurement, published paper with coordinates, Wikipedia/geonames, or official PSC block map.
   - **Block/field/feature name verification is MANDATORY** before building analysis. If a user says "Block P", verify it exists as a real PSC designation in published literature. Don't assume user-provided names are confirmed — search PETRONAS MPM bid rounds, OE Digital, Offshore Energy, published PSC lists.
   - **The epistemic tag on coordinates matters as much as the number.** OBSERVED = has GPS data or published coordinates. ESTIMATE = read from published map figure. SPECULATED = from memory or mental model. Never tag memory-derived coordinates as OBSERVED.
   - **What happened:** Plotted Lipad MV 0.5° longitude off (118.0 vs actual 118.5), Maliau Basin 0.67° latitude off (5.5 vs actual 4.83), Ranau 0.34° longitude off. Built entire dossier with unverified block name "Block P" — when challenged, concluded it didn't exist, but `references/sabah-deepwater-psc-blocks.md` already listed Block P as a real Murphy Sabah Oil block. Lesson: **check own reference files before concluding a name doesn't exist.**
   - **Verification workflow:**
     1. Search Wikipedia/geonames for city/landmark GPS coordinates
     2. Search published papers (ResearchGate, OnePetro, Academia) for geological feature coordinates
     3. Search PETRONAS/OE Digital/Offshore Energy for PSC block names and boundaries
     4. Tag every coordinate with source: `Wiki`, `GPS`, `paper_name`, `approx_from_map`, `SPECULATED`
     5. If source is unavailable, label the point as `UNVERIFIED` on the figure and in the caption
   - **The Arif rule:** "Location location location!!! That's the foundation for Geox. Can you imagine u ai give wrong drill location!!!"
   - Full reference: `references/coordinate-verification-protocol.md`

1. **Vertical exaggeration must be 1:1 in the cross-section** — anything else makes the diagram scientifically misleading. State this in the panel label.
2. **Don't fabricate Vp values or paper citations.** Every number must trace to either the Sabah ontology (real) or a real paper (real). Use OBS/DER/INT/SPEC epistemic labels.
3. **Web search is often down (Tavily HTTP 402).** Probe once, then pivot to local archives (`/root/GEOX/forge_work/`). The arifOS box has a deep archive of sealed briefs and audits.
4. **reportlab IS available** (installed 2026-07-07 via pip). Both weasyprint and reportlab work — pick the tool that matches the workflow:
   - **weasyprint** → HTML-driven scientific PDFs (white theme, two-column prose, `<table>` layout)
   - **reportlab** → programmatic dark-themed dossiers, custom page templates with `onPage` canvas drawing, precise header/footer/gold-accent control. See "Dark-Themed Intelligence Dossier" section above.
   - If neither is available: `python3 -m pip install reportlab` installs cleanly.
5. **matplotlib rc style overrides** (e.g. pyrolite.mplstyle) print warnings on first save. Ignore them — they're cosmetic.
6. **The `path_effects` with stroke is essential for label readability** over multi-color geology. Use `pe.withStroke(linewidth=2.5, foreground="white", alpha=0.85)` consistently.
7. **Don't skip the visual audit loop.** Always `vision_analyze` each figure BEFORE assembling the PDF. Caught: 4 overlapping labels on first cross-section pass; legend covering sea polygon on regional map; matplotlib `table()` header-overlap bug.
8. **3D block diagram is a fence, not a true 3D model.** State this in the caption. It illustrates geometry, not strain field.
9. **PDF metadata matters** — set `title` via `<title>` tag in HTML (visible in file properties). For reportlab: `doc = SimpleDocTemplate(OUT, title='...', author='...', subject='...')`.
10. **search_files glob traps:** When searching for a file by prefix, the pattern MUST end with `*` (e.g. `kinabalu*`). Patterns like `kinabaluscar*` only match if the literal substring `kinabaluscar` appears. If `search_files` returns 0 hits, verify with `ls /root/*.png` or `find /root -maxdepth 4 -iname "prefix*"` before declaring a file absent.
11. **Wide-aspect figures (4:1, e.g. 3971×964 px cross-section) need explicit `max-width: 100%` in HTML img CSS or they overflow the A4 page** and render as blank page or cut off.
12. **GEOX Earth Graph claims are session-scoped to the running daemon.** A claim created in one session (`935be7ceb54241c2`) may return `GEOX_404_DATA` in a later session if the daemon restarted, was upgraded, or its storage was ephemeral. **Mitigation:** treat the claim_id as a receipt, not a permanent handle. If you need to "update" a previous claim's conclusions, **create a new claim** with a v4-suffixed title and attach the corrective evidence as `supporting=False` items + a `geox_egs_claim_challenge` with `challenger=reviewer_chatgpt_<date>`. The v4 claim `7103fbb9394b4f23` was created this way after v3's `935be7ceb54241c2` was no longer reachable.
13. **The "federation-wide" blast radius = ESCALATE = F13 SOVEREIGN signature required.** This is correct behavior, not a bug. Don't fight it; report to Arif and wait. The v4 manuscript's arifOS verdict was ESCALATE → F13 required, which the constitution honors.

## Cross-References
- `geox-federation-mcp-driver` — produces the claim/evidence audit that backs the PDF
- `scientific-manuscript-forge` — the full pipeline (YELLOW band tightening discipline, GEOX claim registration)
- `institutional-epistemic-sink-forensics` — when the manuscript's meta-pattern is the Calhoun institutional sink (e.g. pairing the Kinabalu two-oceanics model with the Petronas epistemic-sink diagnosis, validated 2026-07-03)
- `federation-organ-liveness-probe` — confirms GEOX is alive before pulling data
- `/root/GEOX/forge_work/KINABALU-LAYANG-BASEMENT-FALSIFICATION-LC001-2026-06-29.md` — falsification matrix to cite
- `/root/GEOX/docs/eureka_insights/KL2_KINABALU_2026_06_03.md` — KL2 dataset specs to cite
- `/root/HERMES/cron/output/kinabalu_eureka_audit_2026-07-03.md` — most recent live audit to cite

## Files
- `references/kinabalu-strat-ontology.md` — condensed Sabah Vp/age table (Panas, Gomantong, Labang, Sandakan, Ophiolite) + crustal architecture + 4-hypothesis matrix
- `references/hall-2013-citations.md` — citation cards for Hall 2012/2013, Balaguru 2009, Gilligan 2026, Krebs 2011, Franke 2008, Cottam 2013, Sidek 2018, Tongkul 1994, Rangin 1990, Taylor 1983
- `references/weasyprint-pdf-template.md` — full HTML template + CSS for scientific PDFs (15-page Kinabalu model)
- `references/v3-to-v4-tightening-pattern.md` — the peer-review correction workflow (v3 overclaim → v4 GEOX + manuscript patch). Reusable for any future claim that needs falsification hardening.
- `references/data-driven-crosssection-pattern.md` — building cross-sections from existing document data (pdftotext → numpy piecewise → matplotlib fill_between). Includes Sabah Semporna→Dangerous Ground example.
- `references/sabah-crosssection-svg-template.md` — SVG→Playwright→PNG template for schematic/interpretive cross-sections. Pattern fills, arrow markers, depth-partitioned layers, Playwright rendering recipe. Proven: Sabah NE-SW cross-section (2026-07-05).
- `references/geox-audit-methodology.md` — 7-step GEOX tool pipeline for auditing scientific documents (forbidden_claims_scan, contrast_detect, rock_physics, seismic_compute, deep_time_state, evidence, biostrat_ruling_check). Includes APEX Theory claims → GEOX tool mapping.
- `references/tectono-strat-panel-pattern.md` — 5-column × 3-row tectono-stratigraphic panel layout (NW Sabah PSCS→NSPW→Rotan example). Matplotlib implementation, color coding, cell-by-cell construction guide. Includes v2 epistemic labeling system (CLAIM/PLAUSIBLE/ESTIMATE/HYPOTHESIS/SCHEMATIC) and GEOX-EGS integration pointers.
- `references/geox-egs-claim-minting.md` — Workflow for converting visual geological models to machine-readable GEOX-EGS claim objects. JSON schema, claim registration, evidence attachment, 888_HOLD flagging. Proven: NW Sabah tectono-strat model (2026-07-07).
- `references/nw-sabah-deepwater-framework.md` — Condensed NW Sabah deepwater geological framework: PSCS, NSPW, structural trends, reservoir architecture, petroleum system, PTTEP Block K intelligence. Source material for Block P dossiers and Sabah deepwater work. Includes Pilia 2023 lithospheric drip model (HYPOTHESIS) and mud volcanism ≠ igneous distinction.
- `references/sabah-deepwater-psc-blocks.md` — Verified Sabah PSC block reference: operators, fields, coordinates, structural features, cities, mud volcano locations. CRITICAL: use this file when plotting ANY geological feature in Sabah. Never plot from memory. Proven lesson 2026-07-07.
- `templates/cover_block.py` — starter: cross-section + 3D block + timeline in one figure
- `templates/full_pdf.py` — starter: reportlab PDF builder (programmatic header/footer control)