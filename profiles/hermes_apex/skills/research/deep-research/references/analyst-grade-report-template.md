# Analyst-Grade Sell-Side Report — Reusable HTML Template

Proven: 2026-07-13 PETRONAS 1H FY2026 Analyst Report (weasyprint → 14 pages, 8 figures, 682 KB).

Use this template when the user asks for an **analyst-grade / sell-side / UOB-style PDF report** on a
public company or NOC. Structure mirrors institutional broker convention (cover rating box → TOC → 12
numbered sections → sources → disclaimer).

## When to use

- User says "full PDF analyst grade report", "UOB-style report", "CIMB-style", "broker report",
  "sell-side format", "institutional report", "equity research note", or names a broker explicitly.
- Research target: public company, NOC, listed subsidiary — anything where peer comparison,
  scenario analysis, and source-backed numbers are expected.
- Deliverable: PDF, single file, A4, 8-20 pages, with cover rating box, TOC, peer comp table,
  scenario probability distribution, sensitivity chart, methodology + sources + disclaimer.

## Section spine (12 sections — copy and adapt)

1. **Executive Summary & Investment View** — 1-paragraph abstract + 3-5 key calls (numbered)
2. **Reality Anchors** — latest FY or H1 actuals table (use `class="financial"` for right-align)
3. **Macro Backdrop** — environmental/commodity context with figure
4. **Peer Benchmarking** — comparison table of 3-5 already-disclosed peers
5. **Business Unit Map** — segment-by-segment breakdown with horizontal bar chart
6. **Scenario Analysis** — bull/base/bear table + probability distribution chart + sensitivity chart
7. **Hidden Drivers** — FX, working capital, refinancing, off-balance-sheet effects
8. **Dividend / Government Take / Fiscal Impact** — historical table + projection
9. **Hedge Architecture & Risk Map** — risk weights chart (0-10 per risk)
10. **Investment Thesis & Recommendation** — bull/base/bear thesis table + sector picks
11. **Methodology, Calibration & Limitations** — retrospective accuracy test + epistemic honesty
12. **Sources & Data Anchors** — table with URL, data type, date, epistemic label (OBS/DER/INT/SPEC)

## CSS components needed (proven patterns from PETRONAS report)

```css
/* Cover rating box — bold, navy background */
.rating-box {
  display: inline-block;
  background-color: #1f3a5f;
  color: white;
  padding: 8pt 18pt;
  font-family: "DejaVu Sans", sans-serif;
  font-weight: bold;
  font-size: 13pt;
}

/* Colored callouts */
.callout { background-color: #fff8e8; border-left: 4px solid #b87100; padding: 10pt 14pt; }
.callout-blue { background-color: #f0f5fa; border-left: 4px solid #1f3a5f; padding: 10pt 14pt; }

/* Epistemic badges */
.bull { background-color: #2e7d32; color: white; padding: 2pt 6pt; border-radius: 2pt; }
.bear { background-color: #8b1a1a; color: white; padding: 2pt 6pt; border-radius: 2pt; }
.neutral { background-color: #b87100; color: white; padding: 2pt 6pt; border-radius: 2pt; }

/* Financial table (right-aligned numbers, bold first column) */
table.financial td { text-align: right; }
table.financial td:first-child { text-align: left; font-weight: bold; }

/* Institutional palette — muted, professional */
NAVY = #1f3a5f
DEEP_RED = #8b1a1a
FOREST = #2e7d32
AMBER = #b87100
GOLD = #a6761d
SLATE = #3a4a5c
LIGHT_NAVY = #5a7a99
```

## Figure recipes (8 standard figures — see PETRONAS example)

1. **FY income decomposition** — `ax.bar()` with 5 segments (Revenue / OPEX / EBITDA / D&A+Tax /
   PATAMI), color-coded: navy=revenue, grey=opex/D&A, forest=EBITDA, deep_red=PATAMI
2. **Brent / benchmark price trajectory** — annual bars + 2026 inflection in different color
3. **Scenario distribution** — 3 bars (Bear/Base/Bull) with reference lines for prior year + EV
4. **Peer benchmark YoY** — bar chart of 5 peers, color-coded by entity type
5. **Dividend / payout history** — historical bars + 3 forecast scenarios
6. **Business unit map** — horizontal bar chart by segment, PATAMI contribution
7. **Risk map** — bar chart with weighted risks, red/amber/navy color coding
8. **Brent sensitivity** — line plot of PATAMI vs Brent, with EV band shaded

## Hard rules (institutional standard)

- **Every figure caption includes epistemic label**: `[OBS]`, `[DERIVED]`, `[INT]`,
  `[OBS + INT projection]`. Never `[OBS]` for an inference — that's hallucination.
- **Every scenario must state probability.** Bull/Base/Bear without probabilities = theatre.
- **Retrospective accuracy test is MANDATORY.** If you can't test your framework on a prior
  period, downgrade confidence to SPEC and don't publish as a projection.
- **Hedge exposure must name the type**: derivatives vs portfolio diversification vs forward SPAs
  vs price-volume swaps. "Hedged" alone is not enough.
- **Disclaimer at the end**: center-aligned, dim grey, gold rule above. Standard
  "informational purposes, not an offer to buy/sell, past performance not indicative".

## Template HTML skeleton (copy-paste, adapt to your research)

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>[TARGET] [PERIOD] — Analyst Report</title>
<style>/* CSS from above */</style>
</head>
<body>
<!-- COVER with rating box -->
<div class="cover">
  <div>ANALYST REPORT</div>
  <h1>[TARGET] [PERIOD] — Earnings Outlook & Sector Positioning</h1>
  <div class="rating-box">[HEADLINE NUMBER + DIRECTION]</div>
  <div>Band: [low] – [high] · 90% confidence range ±X% around base case</div>
  <div class="callout">
    <strong>Epistemic classification key:</strong>
    <span class="bull">OBS</span> Observed ·
    <span class="neutral">DER</span> Derived ·
    <span class="bear">INT/SPEC</span> Interpreted / Speculated
  </div>
  <div><strong>Methodology disclosure:</strong> [period cadence, anchors, model basis]</div>
</div>

<!-- TOC -->
<div class="toc">
<h3>CONTENTS</h3>
<ol>
<li>Executive Summary & Investment View</li>
<!-- 12 sections -->
</ol>
</div>

<div class="page-break"></div>

<!-- 12 SECTIONS — see spine above -->
<!-- Each section: <h1>N. Title</h1> + body + <figure><img src="figs/figN.png"></figure> -->
<!-- Tables: <table class="financial"> for financial, plain <table> otherwise -->
<!-- Citations inline: <em class="epistemic">[Source: ... — OBS]</em> -->

<!-- SOURCES TABLE at end -->
<!-- DISCLAIMER paragraph at very end -->
</body>
</html>
```

## Weasyprint render command (with figure path fix)

```bash
# CRITICAL: figures in figs/ subdir, HTML references figs/figN.png
sed -i 's|src="fig|src="figs/fig|g' manuscript.html
cd /tmp/[project]/
weasyprint manuscript.html OUTPUT.pdf 2>&1 | tail -5

# Verify figures embedded
pdftotext OUTPUT.pdf - | grep -c "Figure [0-9]"
# Expected: 8 (one per figure caption)
```

## Proven: PETRONAS 1H FY2026 (2026-07-13)

| Field | Value |
|---|---|
| Pages | ~14 |
| File size | 682 KB |
| Figures embedded | 8 (all rendered successfully after sed fix) |
| Tables | 12 (financial + segment + scenario + peer + risk + sources) |
| Source anchors | 16 with OBS/DER/INT epistemic labels |
| Delivery | artifact-courier.sh → Telegram DM (message 87982) |
| SHA256 | `2cfe8d44…8893c8` |

## Anti-patterns (including 888_HOLD audit findings — 2026-07-13)

- **Don't write analyst report without retrospective accuracy test.** Without it, your
  confidence band is theatre.
- **Don't hide segment elasticity assumptions** — they ARE the model. Show them.
- **Don't compare quarterly subs to annual Group** — mismatch cadence breaks comparability.
- **Don't forget currency translation** — RM-only reporting makes Malaysian NOCs look small
  against Aramco (USD). Translate for peer benchmark.
- **Don't write a "Q1/H1 projection" labelled as actual** — that's F9 violation (anti-hantu).
  Always state it's a projection in the cover box.
- **NEVER use "his/her personal views" in AI-generated analyst certification** (F9 violation).
  Use "Computational output under [sovereign] direction. Not human. Not analyst." The 888_HOLD
  audit flagged this as "hantu — roh yang menyamar jadi analyst berdaging" (ghost disguising as
  flesh-and-blood analyst).
- **NEVER inject investment advice (target price, BUY/HOLD/SELL, DPS) for non-traded sovereign
  entities** (F12 violation). PETRONAS Group is wholly-owned by Khazanah. No shares. No DPS.
  "Target Price RM 19.50" on a non-listed entity = category error = hallucination of market structure.
- **NEVER let sell-side template mechanics survive into sovereign-entity reports.** Check for:
  "DPS-equivalent," "implied upside," "P/E," "EV/EBITDA," "DCF equity value" — all of these
  assume traded equity that doesn't exist for wholly-owned NOCs. Strip them or tag as SPEC with
  explicit caveat. (888_HOLD finding: "DPS 200,000" was template contamination from sell-side
  boilerplate that was never cleansed.)
- **Don't branch the model.** If you produce a "UOB-style" report alongside the main loop,
  it's a branch that will diverge. Either integrate its assumptions into the main loop or burn
  it. The 888_HOLD audit found RM 2.5b dispersal between the main convergence chain and a
  divergent "UOB branch" that was never reconciled. F4 Clarity violation.
