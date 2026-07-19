---
name: scientific-pdf-generation
description: "Generate publication-quality PDFs with reportlab + matplotlib — four modes: Mode A (academic, white/serif), Mode B (intelligence dossier, dark/gold), Mode C (sell-side analyst report, navy/light/UOBKH/CIMB house style), Mode D (trading signal, dark/OANDA-style candlestick charts). Two-column layout, proper typography, figure styling, references."
triggers:
  - "scientific pdf"
  - "publication quality document"
  - "academic paper pdf"
  - "geology report pdf"
  - "research paper"
  - "synthesis document"
  - "analyst-grade pdf"
  - "analyst report"
  - "UOB-style report"
  - "CIMB-style report"
  - "broker report"
  - "sell-side format"
  - "equity research note"
  - "institutional report"
  - "give me full pdf [report]"
  - "Kenanga style"
  - "HLIB style"
  - "RHB style"
  - "Maybank IB style"
  - "PublicInvest style"
  - "Affin Hwang style"
  - "refer to UOB"
  - "trading signal pdf"
  - "gold signal pdf"
  - "pitch deck pdf"
  - "marketing pdf"
  - "proposal pdf"
  - "dark theme pitch"
tags:
  - pdf
  - reportlab
  - matplotlib
  - sell-side
  - equity-research
  - broking-format

# Related: `daily-trading-signal-briefing` (trading/) — uses this skill's
# reportlab + matplotlib stack for daily gold/trading signal PDFs.
# That skill has its own one-page layout spec (navy/gold/teal/red palette)
# and a proven chart template in templates/gold_signal_chart.py.
---

# Scientific PDF Generation

## When to Use

When producing documents meant to look like real publications — four modes:

- **Mode A (academic)**: journal papers, technical reports, white/serif/two-column
- **Mode B (intelligence dossier)**: field briefings, professional impression pieces, dark/gold/Helvetica
- **Mode C (sell-side analyst report)**: UOBKH / CIMB / Maybank IB / Kenanga / RHB / HLIB / PublicInvest style broker reports, equity research, sector forecasts, NAV / DCF / SOTP valuation decks. **Light background, navy/gold accent, recommendation banner, scenario tables, peer-comp boxes.**
- **Mode D (trading signal)**: Daily trading signal PDFs with candlestick charts, EMA overlays, buy/sell zones, R:R visualization. **Dark theme (OANDA-style), candlestick-first, mobile-readable, landscape format.** → `references/financial-trading-signal-charts.md`

**Choose based on audience and venue, not on topic.** A geological deep-dive for an analyst audience = Mode C. The same deep-dive for an academic conference = Mode A. For a competitive intel dossier to share with a peer in the field = Mode B. For a daily trading signal with candlestick chart = Mode D.

## Mode A: Academic / Publication (Default)

**White background, serif fonts, muted colors.** For journal papers, technical reports, formal deliverables.

## Mode C: Sell-Side Analyst Report

**Light background, navy/gold accent, sans-serif headers, recommendation banner.** This is the format every Malaysian broker (UOB Kay Hian, CIMB, Maybank IB, Kenanga, RHB, HLIB, PublicInvest, Affin Hwang) publishes daily. Use when the user says "analyst-grade", "UOB-style", "broker report", "sell-side", "equity research pdf", or after `deep-research` produces an institutional financial deep-dive.

**Proven 2026-07-13:** PETRONAS 1H 2026 sector forecast — 15 pages, 8 figures (matplotlib), 14 tables (navy header + gold accent). Standard spine:
1. Cover with recommendation banner (HOLD / BUY / SELL colour-coded)
2. Sector recap table + 6 key takeaway bullets
3. UOBKH-style highlights table (16-row time-series)
4. Segment deep-dive with figures
5. Earnings revision + valuation (SOTP, peer multiples)
6. Brent × JKM sensitivity heatmap
7. ROACE trajectory
8. Peer benchmark (Q1 net income + margin)
9. Key risks (deep-dive on the single largest unpriced risk)
10. What would change our call (upgrade / downgrade triggers + catalyst calendar)
11. Governance / ESG / sovereign
12. Credit profile
13. Appendix A — 5-year forecasts
14. Appendix B — DCF framework + WACC
15. Disclaimers + analyst certification

See `references/sell-side-analyst-style.md` for the full visual specification and `templates/sell_side_analyst_report.py` for the working reportlab scaffold (proven this session — 780 KB output).

### Mode C Color Palette

```
Background:  #ffffff (white)
Navy:        #003366 (recommendation banner, section headers, table header rows)
Gold:        #C5A572 (BUY/SELL accent rule, key takeaways, premium callouts)
Teal:        #2A9D8F (bullish signal markers, sector +EV callouts)
Red:         #C73E1D (bearish signal markers, downside triggers)
Light grey:  #F3F4F6 (alternating table row background)
Dark grey:   #374151 (body text)
Med grey:    #6B7280 (captions, source attribution, footer text)
Header bar:  navy solid bar 1.2pt thick + 0.4pt gold accent rule
```

### Mode C Typography

```
Headings:    Helvetica-Bold, 14pt H1 (navy), 11.5pt H2 (navy), 10pt H3 (dark grey)
Body:        Helvetica 8.8pt, dark grey, JUSTIFY, leading 11.5pt
Captions:    Helvetica 7.8pt, med grey, centred under figures
Tables:      Alternating row (white / #F3F4F6), header row navy + white text
Recommendation banner: 4-column table, top row navy/white, bottom row colour-coded by rating:
  - BUY = teal background, white "BUY" text + target price
  - HOLD = gold background, white "HOLD" text + target price
  - SELL = red background, white "SELL" text + target price
```

### Mode C Standard Spine

When generating a sector/company broker report, follow this 15-section spine — proven to match what Malaysian brokers publish daily:

1. **Cover** — date, recommendation banner (4-col: rating | last price | target | upside), 6 bullet takeaways
2. **Highlights table** — 12-16 rows × 5-7 columns, historical 2H/1H/FY + projection + YoY %
3. **Stock impact — segment deep-dive** — one subsection per business unit
4. **Earnings revision** — prior vs new estimate, % change, FY new, FY+1
5. **Valuation** — methodology (DCF / SOTP / PBV / DDM), implied value, peer multiples comparison
6. **Target price rationale** — discount/premium to peer average, walk to TP
7. **Scenario analysis** — bear / base / bull + probability weighting, sensitivity heatmap
8. **ROACE / production trajectory** — multi-year chart
9. **Peer benchmark** — same-period quarterly comparison (always in USD)
10. **Listed-subs / comparable companies** — YTD performance chart
11. **Key risks** — single largest unpriced risk deep-dive (sovereign / political / regulatory)
12. **What would change our call** — upgrade triggers + downgrade triggers + catalyst calendar
13. **Governance / ESG / credit** — sovereign positioning, credit profile
14. **Appendices** — 5-year forecast group + segment, DCF framework
15. **Disclaimers + analyst certification** — standard CMSA / Bursa language

### Mode C Recommendation Banner Pattern

```python
def make_recommendation_banner(rating, current_price, target_price, upside_pct):
    """Top recommendation banner — 4 columns, colour-coded by rating."""
    rating_bg = {'BUY': TEAL, 'HOLD': GOLD, 'SELL': RED}[rating]
    data = [
        [rating, 'Last Traded Price', 'Target Price (12-mth)', 'Implied Upside'],
        [f'RM {current_price:.2f}', f'RM {target_price:.2f}', f'+{upside_pct:.1f}%']
    ]
    t = Table(data, colWidths=[3.0*cm, 4.5*cm, 4.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (0,1), rating_bg),
        ('TEXTCOLOR', (0,1), (0,1), colors.white),
        ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (0,1), 18),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (1,1), (-1,1), 11),
        ('FONTNAME', (1,1), (-1,1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1,1), (-1,1), NAVY),
        ('GRID', (0,0), (-1,-1), 0.4, colors.grey),
        ('BOX', (0,0), (-1,-1), 1.2, NAVY),
    ]))
    return t
```

### Mode C Page Template (reportlab)

```python
def header_footer(canvas, doc):
    """Standard broker page header + footer."""
    canvas.saveState()
    # Header rule + text
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.2)
    canvas.line(1.5*cm, 28.0*cm, 20.0*cm, 28.0*cm)
    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 7.5)
    canvas.drawString(1.5*cm, 28.2*cm, "UOB KAY HIAN  |  EQUITY RESEARCH  |  MALAYSIA DAILY")
    canvas.setFillColor(MED_GREY)
    canvas.setFont('Helvetica', 7)
    canvas.drawRightString(20.0*cm, 28.2*cm, "Monday, 13 July 2026  |  Hermes-Prime (Federated Research)")
    # Footer
    canvas.setLineWidth(0.4)
    canvas.line(1.5*cm, 1.2*cm, 20.0*cm, 1.2*cm)
    canvas.setFillColor(MED_GREY)
    canvas.setFont('Helvetica', 6.5)
    canvas.drawString(1.5*cm, 0.8*cm, "Refer to last page for important disclosures. AC: Hermes-Prime certifies independent views.")
    canvas.drawRightString(20.0*cm, 0.8*cm, f"Page {doc.page}")
    canvas.restoreState()
```

### Mode C Figure Defaults (matplotlib — light theme)

```python
NAVY = '#003366'
GOLD = '#C5A572'
TEAL = '#2A9D8F'
RED = '#C73E1D'
GREY = '#6B7280'
LIGHT_GREY = '#D1D5DB'
BLUE_LIGHT = '#9DC3E6'

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'text.color': '#374151',
    'axes.labelcolor': '#374151',
    'xtick.color': '#6B7280',
    'ytick.color': '#6B7280',
    'axes.edgecolor': '#6B7280',
    'grid.color': '#D1D5DB',
    'grid.alpha': 0.3,
    'font.family': 'DejaVu Sans',  # sans-serif for sell-side (matches Helvetica)
    'font.size': 10,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
```

### Mode C Required Disclaimer Block

Standard CMSA / Bursa Malaysia text — copy-paste, never modify substantively:

> This report is prepared for general circulation. It does not have regard to the specific investment objectives, financial situation and the particular needs of any recipient. Advice should be sought from a financial adviser regarding the suitability of any investment product. This report is confidential and may not be published, circulated, reproduced or distributed in whole or in part by any recipient to any other person without the prior written consent of the publisher. The information or views in the report has been obtained or derived from sources believed to be reliable; however, no representation is made as to the accuracy or completeness of such sources or the information. Past performance is not indicative of future results. FORWARD-LOOKING STATEMENTS DISCLOSE MATERIAL UNCERTAINTY.

The Analyst Certification (AC) block — required at the end of every Malaysian broker report:

> AC: Each research analyst of [Broker] who produced this report hereby certifies that (1) the views expressed in this report accurately reflect his/her personal views about all of the subject corporation(s) and securities in this report; (2) the report was produced independently by him/her; (3) he/she does not carry out, whether for himself/herself or on behalf of [Broker] or any other person, any of the Subject Business involving any of the subject corporation(s) or securities referred to in this report; and (4) he/she has not received and will not receive any compensation that is directly or indirectly related or linked to the recommendations or views expressed in this report.

For federated research agents (Hermes-Prime): substitute "Hermes-Prime (Federated Research)" for the broker name and disclose the kernel alignment. The disclaimer language is non-negotiable — don't rewrite it.

## Stack

Three rendering paths — choose based on document type:

| Path | Best for | Speed | Setup |
|------|----------|-------|-------|
| **pandoc→xelatex** | Text-heavy docs with tables, TOC, cross-refs | Fast (seconds) | pandoc + texlive-xetex |
| **weasyprint** | HTML-driven layout, Mode C analyst reports (closest to broker format) | Medium | pip install weasyprint |
| **reportlab** | Programmatic control (headers/footers/page templates), Mode A & B proven, Mode C pattern in template | Slow (coding) | pip install reportlab |

### Path 1: pandoc→xelatex (FASTEST for text-heavy scientific documents)

Use when the document is primarily text + tables + references and you need a professional PDF fast.

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V mainfont="DejaVu Serif" \
  -V monofont="DejaVu Sans Mono" \
  -V colorlinks=true \
  -V linkcolor=blue \
  --toc \
  --toc-depth=3 \
  -V toc-title="Contents"
```

**Proven:** 2026-07-05, APEX Theory Review v2 (24 pages, 15 tables, 45 references). Rendered in <5 seconds.

**Key flags:**
- `--pdf-engine=xelatex` — supports Unicode, system fonts, complex tables
- `--toc` — auto-generate table of contents from markdown headers
- `-V mainfont="DejaVu Serif"` — serif body text (check `fc-list | grep -i serif` for available fonts)
- `-V geometry:margin=1in` — standard academic margins

**Pitfalls:**
- If xelatex is not installed: `apt install texlive-xetex` (or `texlive-latex-recommended` for pdflatex)
- Wide tables may overflow — use `pandoc -V geometry:margin=0.8in` or restructure as lists
- Unicode math symbols (`×`, `→`, `≥`) render correctly with xelatex but may fail with pdflatex

### Path 2: weasyprint (HTML→PDF)

**Recommended for Mode C sell-side reports.** Use when you need CSS-driven layout (multi-page tables, recommendation banners, peer-comp side-by-side, scenario probability distributions, sensitivity bands, methodology & limitations section, sources/disclaimer).

```python
from weasyprint import HTML
HTML(filename='manuscript.html', base_url='/tmp/figures/').write_pdf('output.pdf')
```

**Proven 2026-07-13:** PETRONAS analyst-grade report (14 pages, 8 figures, peer-comp + scenario tables, retrospective calibration block all rendered cleanly with HTML+CSS).

### Path 3: reportlab (programmatic)

Use when you need canvas-level control (running headers, page templates, dynamic content).

- **reportlab** — PDF assembly (platypus flow: paragraphs, images, tables, page templates)
- **matplotlib** — figure generation (set `figure.facecolor: white`, `font.family: serif`)

## Mode B: Intelligence Dossier / Field-Ready

**Dark background, gold/amber accents, sans-serif headers.** For intelligence briefings, field dossiers, modern technical presentations, documents meant to impress in professional settings.

Use Mode B when:
- Document is an intelligence briefing, competitive intel, or domain dossier
- Audience is a working professional (geologist, engineer, executive) in a field/social setting
- The dark theme signals modernity and technical sophistication
- Arif says "dossier", "briefing", "impress", or "wow"

### Mode B Color Palette
```
Background:  #0d1117 (GitHub dark)
Panel:       #161b22 (slightly lighter, for header/footer bars)
Gold accent: #f0a500 (headlines, section markers, accent lines)
Amber:       #ffa657 (subheadings, secondary emphasis)
Green:       #3fb950 (positive signals, key findings)
Blue:        #58a6ff (info, data points, figures)
Red:         #f85149 (warnings, critical signals, risk flags)
Teal:        #39d2c0 (conversation starters, quotes)
Text:        #e6edf3 (body — near-white, NOT pure white)
Dim:         #8b949e (captions, references, footer text)
Border:      #30363d (table grid lines, separators)
```

### Mode B Typography
```
Body:        Helvetica, 10pt, #e6edf3, JUSTIFY
Headings:    Helvetica-Bold, 18pt H1 (#f0a500) / 14pt H2 (#ffa657) / 11pt H3 (#3fb950)
Tables:      Alternating row backgrounds (#161b22 / #1a1f28), header row #1a2332
Captions:    Helvetica-Oblique, 8pt, #8b949e, center-aligned
Quotes:      Helvetica-Oblique, 10pt, #ffa657, gold border, dark panel background
```

### Mode B Page Template (reportlab BaseDocTemplate)

```python
def draw_background(canvas, doc):
    canvas.saveState()
    # Dark background
    canvas.setFillColor(HexColor('#0d1117'))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Header bar
    canvas.setFillColor(HexColor('#161b22'))
    canvas.rect(0, A4[1] - 12*mm, A4[0], 12*mm, fill=1, stroke=0)
    # Gold accent line
    canvas.setStrokeColor(HexColor('#f0a500'))
    canvas.setLineWidth(1.5)
    canvas.line(0, A4[1] - 12*mm, A4[0], A4[1] - 12*mm)
    # Header text (title left, classification right)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(HexColor('#f0a500'))
    canvas.drawString(2*cm, A4[1] - 9*mm, 'DOCUMENT TITLE')
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(HexColor('#8b949e'))
    canvas.drawRightString(A4[0] - 2*cm, A4[1] - 9*mm, 'CONFIDENTIAL')
    # Footer bar
    canvas.setFillColor(HexColor('#161b22'))
    canvas.rect(0, 0, A4[0], 10*mm, fill=1, stroke=0)
    canvas.setStrokeColor(HexColor('#f0a500'))
    canvas.setLineWidth(0.5)
    canvas.line(0, 10*mm, A4[0], 10*mm)
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(HexColor('#8b949e'))
    canvas.drawString(2*cm, 4*mm, 'Source attribution')
    canvas.drawRightString(A4[0] - 2*cm, 4*mm, f'Page {doc.page}')
    canvas.restoreState()
```

### Mode B Matplotlib Figure Defaults
```python
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#0d1117',
    'text.color': '#e6edf3',
    'axes.labelcolor': '#e6edf3',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'axes.edgecolor': '#30363d',
    'grid.color': '#21262d',
    'font.family': 'DejaVu Sans',
    'font.size': 10,
})
```

Use accent colors (#f0a500 for highlights, #3fb950 for positive, #f85149 for risk) in figures. Use `matplotlib.patheffects.withStroke(linewidth=3, foreground='#0d1117')` for text labels that need to be readable over colored fills.

### Mode B Document Structure (Intelligence Dossier)

1. **Cover page** — title (large, gold), subtitle (amber), prepared-for line, date, description of contents, key references
2. **Table of contents** — numbered sections with dim text
3. **Numbered sections** — each with H1 (gold) + H2 (amber) + body + figures + tables
4. **Conversation starters** — in teal-bordered boxes with dark green background (#0d1f0d)
5. **References** — numbered, dim text, hanging indent
6. **Disclaimer** — center-aligned, dim, gold rule above

**Proven:** 2026-07-07 — Block P Deepwater Sabah Geological Dossier (10 pages, 6 figures, 946 KB). Dark theme with gold accents. Delivered as professional intelligence document.

### Mode B — Marketing Pitch Deck (sub-pattern)

For personal pitch decks, product proposals, and lifestyle-brand documents targeting a single person or small group. Uses **direct canvas construction** (no BaseDocTemplate/Platypus) — each page is a standalone composition. Landscape A4. Card-based layouts, flow diagrams, before/after comparison panels.

→ Full spec with code patterns: `references/mode-b-marketing-deck.md`

**Proven:** 2026-07-14 — Abang Sado × AI trading agent pitch deck (6 pages, landscape A4, dark/gold theme, card layouts, zigzag flow diagram, before/after lifestyle panels). 12KB output, all pages visually verified.

## Mode D: Trading Signal (Candlestick Chart)

**Dark background, candlestick-first, OANDA-style.** For daily trading signals, forex/commodity charts, technical analysis PDFs.

→ Full spec: `references/financial-trading-signal-charts.md`

**Critical lessons (4 user rejections before success):**
1. **ZOOM IN.** Show only relevant price range. If price is $4,000, show $3,970-$4,080 — not $3,800-$4,800. User: "jangan la zoom out sangat."
2. **Big candles.** Chart is the hero. Candles must fill 80%+ of chart area.
3. **No inline boxes on chart.** Labels go on Y-axis (right side). Boxes block candles.
4. **Buy/Sell zones CLOSE to current price.** "Syed nak position yang berdekatan dengan market price."
5. **Real candlestick coloring.** Red filled = bearish, green hollow = bullish. NOT trend-colored.
6. **Mark patterns.** H=Hammer, D=Doji, SS=Shooting Star, BE=Bearish Engulfing.
7. **EMA 20 + EMA 50 always.**
8. **Strategy table below chart**, not as subplot.
9. **Landscape A4**, chart fills most of page.
10. **Mobile-first.** Minimum 10pt labels, 13pt key levels.

**Color palette (Mode D):** Same as Mode B (dark theme). `BG=#0d1117`, `GOLD=#f0a500`, `GREEN=#3fb950`, `RED=#f85149`, `TEAL=#39d2c0`.

**Stack:** reportlab + matplotlib. Manual Rectangle patches for candlesticks (NOT mplfinance). `landscape(A4)` page orientation.

## Style Defaults (Mode A — apply unless user overrides or Mode B selected)

### Typography
```
Body:        serif (Times-Roman / Liberation Serif), 10pt, 14pt leading, JUSTIFY
Headings:    sans-serif (Helvetica-Bold), 13pt section / 11pt subsection
Captions:    serif, 9pt, italic, dark gray (#666666)
References:  serif, 9pt, hanging indent (leftIndent=1cm, firstLineIndent=-1cm)
```

### Colors
```
Text:        #1a1a1a (near-black, NOT pure black)
Accent:      #2c5f8a (muted blue) for section heads, NOT neon
Epistemic:   OBS=#2e7d32, INT=#e65100, SPEC=#6a1b9a (muted, distinguishable)
Rules:       #cccccc (light gray)
Background:  white (#ffffff)
```

### Layout
```
Page:        A4
Margins:     2.5cm sides, 3.0cm top, 2.5cm bottom
Columns:     Two-column for body text (col_width = (text_width - gap) / 2)
Header:      Running header with document title + year, thin rule below
Footer:      Centered page number (— N —), thin rule above
```

### Figures (matplotlib)
```
facecolor:   white (#ffffff) or #fafafa
font:        serif (DejaVu Serif / Liberation Serif)
edgecolor:   #666666
grid:        #cccccc, alpha=0.3
colors:      Muted palette — #2c5f8a, #8b2500, #2e7d32, #e65100, #6a1b9a, #00695c
markers:     edgecolors="black", markeredgewidth=0.8
legend:      framealpha=0.9, edgecolor="#cccccc"
dpi:         200
```

## Document Structure (Mode A standard)

1. **Title page** — title, subtitle, author/org, date, epistemic band table, provenance note
2. **Abstract** — centered label, indented body (2cm L/R), keywords line
3. **Numbered sections** — 1. Introduction, 2–N body, Conclusions, References
4. **Figures** — full-width (15.5cm), caption with bold "Figure N." + epistemic label in italics
5. **References** — hanging indent, journal names in italics
6. **Provenance table** — source, type, epistemic label

## Two-Column Pattern (reportlab)

```python
from reportlab.platypus import Table, TableStyle

col_gap = 0.5 * cm
col_width = (text_width - col_gap) / 2
t = Table([[left_paras, right_paras]], colWidths=[col_width, col_width])
t.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (0,0), 0),
    ("LEFTPADDING", (1,0), (1,0), col_gap),
    ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ("TOPPADDING", (0,0), (-1,-1), 0),
    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
]))
```

## Page Template Pattern (reportlab)

Use `BaseDocTemplate` with two `PageTemplate`s:
- `TitlePage` — minimal footer only
- `ContentPage` — running header + footer via `onPage` callback

```python
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate

def header_footer(canvas, doc):
    canvas.saveState()
    # header rule + text
    canvas.setStrokeColor(RULE_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(margin_left, page_h - margin_top + 0.8*cm, ...)
    canvas.setFont("Times-Italic", 8)
    canvas.drawString(margin_left, ..., "Document Title")
    # footer
    canvas.drawCentredString(page_w/2, margin_bottom - 1.0*cm, f"— {doc.page} —")
    canvas.restoreState()

doc = BaseDocTemplate(...)
doc.addPageTemplates([
    PageTemplate(id="TitlePage", frames=[...], onPage=title_footer),
    PageTemplate(id="ContentPage", frames=[...], onPage=header_footer),
])
# In story: NextPageTemplate("ContentPage") before first PageBreak
```

## Pitfalls

- **Choose mode based on audience and venue, not topic.** A geological deep-dive for an analyst = Mode C. Same deep-dive for academic conference = Mode A. Competitive intel dossier for peer in the field = Mode B. Don't default to one mode for everything.
- **Dark theme (Mode B) is for intelligence dossiers only.** For academic/publication work (Mode A) or sell-side analyst reports (Mode C), start with white. Use Mode B ONLY when the document is an intelligence briefing, field dossier, or professional impression piece. If unsure between A and C, ask: "Is the audience going to look this up on Bloomberg (C) or cite it in a paper (A)?"
- **Monospace fonts look like code.** Use serif for body (Mode A), sans-serif for body (Mode B & C — Helvetica works well).
- **Unicode symbols may not render.** Use "P"/"R"/"K" for PASS/REVIEW/KILL in kill matrices instead of ✓/?/✗ — DejaVu Serif may lack these glyphs. For Mode C, use "▲"/"▼" arrows (U+25B2/U+25BC) for up/down indicators — they render in DejaVu Sans.
- **Font availability varies.** Always check `fc-list | grep -i serif` before assuming Times-Roman exists. Fallback chain: Times-Roman → DejaVu Serif → Liberation Serif → Helvetica.
- **reportlab Image() needs absolute paths.** Use `str(OUT_DIR / "fig.png")`, not relative.
- **Media delivery directory restrictions.** OpenClaw message tool restricts `media=` to allowed directories. If `/root/forge_work/` is blocked, copy to `/var/arifos/artifacts/outbox/` or use direct Bot API (`curl -X POST .../sendDocument`).
- **weasyprint HTML figure paths MUST match filesystem location (silent failure).** If figures live in `figs/fig01.png` (subdirectory) but HTML uses `<img src="fig01.png">`, weasyprint emits `URLError: <urlopen error [Errno 2] No file or directory>` per missing image and continues — you get a PDF with NO figures rendered and NO fatal error to abort. Recover with `sed -i 's|src="fig|src="figs/fig|' manuscript.html` before rendering, OR keep figures and HTML in the same directory, OR pass `base_url='/tmp/<project>/figs/'` to `HTML()`. Proven 2026-07-13 PETRONAS analyst report — 8 figures silently missing on first render, recovered with sed one-liner. Always `pdftotext | grep "Figure "` after render to verify figures embedded.
- **`Paragraph(<b>...<b>...</b></b>)` nested bold tags crash reportlab with `Parse error: saw </b> instead of expected </para>`.** Pattern proven 2026-07-13 PETRONAS analyst PDF: outer `<b>...</b>` with a literal `<b>...</b>` substring inside causes the parser to mis-parse. Fix: ensure the OUTER `<b>` tag is closed BEFORE any inner `<b>` tags. The safe pattern: `<b>Outer text</b> middle text <b>inner highlight</b>.` (close outer first, then open inner). Or use span-level ParagraphStyle with `fontName='Helvetica-Bold'` for outer emphasis and inline `<b>...</b>` only for inline highlights.
- **Use `weasyprint` HTML for analyst-grade (UOB/CIMB/kenanga-style) sell-side reports.** HTML+CSS gives the closest match to institutional format: cover rating box, colored callouts, multi-section TOC, side-by-side peer-comp tables, scenario probability distribution, sensitivity bands, methodology & limitations section, sources/disclaimer. **Proven 2026-07-13 PETRONAS 1H 2026 report — 14 pages, 8 figures, peer-comp + scenario tables, retrospective calibration block all rendered cleanly.** Standard spine: cover → TOC → 12 numbered sections → sources → disclaimer. Triggers: "UOB-style", "CIMB-style", "analyst-grade", "institutional sell-side format", "broker report", or naming any ASEAN broker (UOB KayHian, Kenanga, CIMB, Maybank IB, RHB, Affin Hwang, PublicInvest).
- **`reportlab` IS viable for Mode C when paired with the proven template.** Pure Python gives you programmatic control over the recommendation banner colour, page template header/footer, and table styling. Slightly more verbose than weasyprint HTML but no CSS escape pain. Trade-off: weasyprint for 14+ page reports with complex tables; reportlab for 8-12 page reports where you need exact pixel control. **Proven 2026-07-13:** PETRONAS analyst PDF generated via reportlab — 15 pages, 780 KB, 8 figures, 14 tables, recommendation banner colour-coded.
- **DejaVu Serif registration required for reportlab (Mode A only).** reportlab does NOT recognize "DejaVu Serif" (with space) as a built-in font. You must register TTF files explicitly before using them. **For Mode C (sell-side) skip this step entirely** — use Helvetica and DejaVu Sans (both built-in) throughout. Proven 2026-07-07 for Mode A; 2026-07-13 confirmed Mode C doesn't need any font registration.
- **TableStyle TEXTCOLOR per-row requires separate commands.** You cannot pass a list of colors to a single TEXTCOLOR command for different rows. This crashes with `AssertionError` in `colors.toColor`. Use one command per row. Proven 2026-07-07.
- **`ax.broken_barh` does NOT accept a `(color, hatch_string)` tuple in `facecolors`.** It crashes with `ValueError: Invalid RGBA argument: '//'`. Workaround: use `ax.barh()` with `hatch='//'` (hatch is a separate kwarg). Proven 2026-07-09.
- **PYROLITE.MPLSTYLE warning is cosmetic, not fatal.** Every matplotlib call prints `Bad key legend.bbox_to_anchor in file /root/.config/matplotlib/stylelib/pyrolite.mplstyle, line 27 ('legend.bbox_to_anchor : (1, 1)')`. Ignore — figures still render correctly.
- **`mplstyle` warnings can be silenced** by setting `MPLCONFIGDIR=/tmp/.mpl` before importing matplotlib, or explicitly call `plt.style.use('default')`.
- **`execute_code` sandbox does NOT have matplotlib** even when system `python3` does. The hermes_tools sandbox uses a different venv from `/usr/bin/python3`. Symptom: `ModuleNotFoundError: No module named 'matplotlib'`. Fix: switch to a terminal `python3` invocation with `MPLCONFIGDIR` set, instead of using `execute_code`. Proven 2026-07-09.
- **`pip install --break-system-packages --quiet <pkg>` is the correct install pattern on this VM.** PEP 668 blocks system pip with `error: externally-managed-environment`. `--break-system-packages` is the documented escape hatch and is what was used successfully to install reportlab + matplotlib for the PETRONAS analyst PDF (2026-07-13). For new installs of reportlab, matplotlib, weasyprint, or similar in this environment, prefix the install with this flag.

## Proven: Multi-Figure Weasyprint Pipeline (12 figures, single PDF)

For deliverables with many embedded figures (10+), this pipeline is faster and more reliable than reportlab. **Proven 2026-07-09, MBR 2026 GEOX bid proposal: 12 figures, 2.9 MB, ~5 sec render.**

### Step 1 — Generate figures as PNGs to a single directory
```python
import os
os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'  # silence pyrolite warning
import matplotlib
matplotlib.use('Agg')  # no display
import matplotlib.pyplot as plt

OUT = Path('/tmp/mbr2026_figures')
OUT.mkdir(exist_ok=True)
# ... generate fig1.png, fig2.png, ... fig12.png at 200 dpi
plt.savefig(OUT / 'figN_name.png', dpi=200, facecolor='white')
```

### Step 2 — Write HTML manuscript with `<img src="figN.png">` references
All figures live in the same directory as the HTML. Inline CSS for academic style — see `templates/weasyprint_manuscript.html` (path proven 2026-07-09, MBR 2026).

### Step 3 — Convert to PDF
```bash
cd /tmp/mbr2026_figures
weasyprint manuscript.html MBR2026-GEOX-ARTIFACTS.pdf 2>&1
ls -la MBR2026-GEOX-ARTIFACTS.pdf
```

**Key flags:** none required. The default `weasyprint html output.pdf` works. `base_url` only matters when HTML is in a different directory than the figures — if they're co-located, no `base_url` needed.

### Step 4 — Deliver via artifact-courier.sh
```bash
bash /root/.hermes/scripts/artifact-courier.sh \
  /var/arifos/artifacts/outbox/$(date +%Y-%m-%d)/MBR2026-GEOX-ARTIFACTS.pdf \
  --caption "MBR2026 GEOX Geological Artifacts — 12 figures: ..."
```

Returns SHA256 receipt + Telegram message_id. The courier handles: source retention (F1 AMANAH), hash governance (F2 TRUTH), audit log (F11 AUDIT), F13 SOVEREIGN routing to ARIF chat only.

### Pitfall: weasyprint ignores `box-shadow`
`box-shadow: 0 2px 4px rgba(0,0,0,0.1)` is silently dropped. Harmless warning. Don't fix.

- **`padding-top: 15vh` invalid value**
weasyprint rejects `vh` units in some contexts. Use `padding-top: 200px` or omit. Harmless warning, but figure it out before treating the warning as no-op.

- **Unicode emojis (🔥⚠️🔻✅🔍) do NOT render in PDF fonts.** Both pandoc→xelatex and weasyprint silently drop emoji characters. Replace with text equivalents before converting: 🔥→"CRITICAL", ⚠️→"WARNING", 🔻→"COLLAPSING", ✅→"POSITIVE", 🔍→"UNDER WATCH". Proven 2026-07-11, civic briefing PDF.

- **For dark-themed HTML→PDF via weasyprint**, see `executive-intelligence-briefing` skill's `references/dark-theme-html-template.md` — complete CSS component library (signal boxes, color-coded tables, epistemic tags, summary strips) for intelligence dossiers. That template uses weasyprint; this skill's Mode B uses reportlab. Choose based on whether you need programmatic control (reportlab) or fast styled layout (weasyprint HTML).

## Mobile-First Financial Charts (LESSON LEARNED 2026-07-14)

When generating trading signal PDFs or financial charts for mobile consumption:

**Critical rules (proven by 4 user rejections):**
1. ONE chart per page. Never stack 3+ charts unless text is 14pt+.
2. Font minimum: 10pt labels, 13pt key levels, 15pt current price.
3. Box annotations (BUY ZONE, STOP LOSS) must be 13-14pt bold with filled background.
4. Figure size: 11×7 inches minimum for single chart. DPI 150 (not 200).
5. PDF image width: 19cm (near full page). Minimal margins.
6. Strategy table goes BELOW chart in PDF (reportlab Table), NOT as matplotlib subplot.

**What fails on mobile:**
- Multi-panel gridspec layouts (3 timeframes + RSI + R:R) — too dense
- 8pt text on chart annotations — invisible on phone
- Complex figure structures with 6+ subplots — clipping, rendering issues
- Strategy data as separate matplotlib chart — user can't connect chart to numbers

**What works:**
- Single candlestick chart, 11×7, dark BG, big labels
- R:R as a simple box in chart corner
- Strategy table below chart using reportlab Table
- Dark theme (#0d1117 BG) for trading/financial content

**See `trading-signal-chart` skill for the full candlestick chart template.**

## Verification

After generating:
1. Check file size (should be 500KB–2MB for 8 figures)
2. Open in PDF viewer — verify the mode was applied correctly
3. Check page count matches expectations
4. Verify figure captions are present and properly formatted
5. For Mode C: verify recommendation banner is colour-coded correctly (BUY=teal, HOLD=gold, SELL=red)
6. For Mode C: verify disclaimer + AC block are present on final pages
7. Run `pdftotext | grep "Figure "` to confirm all figures embedded (catches weasyprint silent image failures)

## References

- `templates/scientific_report.py` — Mode A scaffold: title page, abstract, sections, figures, references. Copy and modify.
- `templates/geological_dossier.py` — Mode B scaffold: domain intelligence report with reportlab + matplotlib, DejaVu font registration, info tables, callout boxes, epistemic bands. Proven 2026-07-07.
- `templates/sell_side_analyst_report.py` — Mode C scaffold: UOBKH/CIMB/Maybank IB-style broker report with reportlab, navy/gold house style, recommendation banner, segment tables, scenario analysis, AC disclaimer. Proven 2026-07-13 (PETRONAS 1H 2026 report).
- `references/figure-white-theme-patterns.md` — matplotlib white-theme rcParams, muted color palette, figure patterns (tectonic map, cross-section, cooling path, kill matrix), Unicode glyph pitfalls.
- `references/figure-dark-theme-patterns.md` — matplotlib dark-theme rcParams for Mode B intelligence dossiers.
- `references/sell-side-analyst-style.md` — Mode C visual specification: UOBKH/CIMB/Maybank IB house style, color codes, table patterns, recommendation banner, scenario probability distributions, peer-comp boxes, AC disclaimer language. Proven 2026-07-13.
- `references/financial-trading-signal-charts.md` — Mode D visual specification: candlestick OHLC rendering, EMA overlays, buy/sell zones, R:R visualization, dark theme OANDA-style, zoom-to-relevance, mobile-first chart layout, data sources. Proven 2026-07-14.
- `references/geological-dossier-figures.md` — 5 reusable matplotlib figure patterns for geological intelligence dossiers: regional map, stratigraphic column, timeline, play types, hub-and-spoke strategy.
- `references/tectono-stratigraphic-panels.md` — multi-column × multi-row geological evolution diagrams: grid layout, color semantics for lithologies, polygon fills, process arrows, depth panels. Proven 2026-07-07 (NSPW mud canopy evolution, 5 stages × 3 panels).
- `references/deepwater-sabah-geology.md` — domain reference bank: verified PSC blocks, three toe-thrust trends, NSPW mud canopy, crustal architecture, PTTEP competitive intelligence, reservoir architecture, petroleum system risks, bilingual talking points, coordinate verification protocol. Use when generating geological dossiers for NW Sabah.
- `references/mode-b-marketing-deck.md` — Mode B sub-pattern for marketing pitch decks: direct canvas construction, card layouts with numbered circles, flow diagrams with color-coded boxes, before/after comparison panels, landscape A4 orientation, pdftoppm visual verification. Proven 2026-07-14.
- `references/geological-artifact-figures.md` — reusable matplotlib patterns for **geological deliverable figures**: well correlation panels, 5-track petrophysical log panels, structural cross-sections with trap analysis, well penetration summaries, play fairway thickness maps. Proven 2026-07-09, MBR 2026 GEOX bid proposal.

## Related Skills

- `deep-research` — research methodology that feeds Mode C reports (especially `references/institutional-financial-deep-dive.md` for NOC / half-yearly cadence handling).
- `professional-intelligence-briefing` — rapid social-mode briefing, no PDF output. For PDF, use THIS skill Mode C instead.
- `executive-intelligence-briefing` — weekly/country/domain news briefings in dark-themed PDF (Mode B). Use that for news/politics, THIS skill Mode C for equity/sector research.
- `trading-signal-chart` (trading/) — candlestick OHLC charts with EMA overlays, buy/sell zones, R:R visualization. Uses this skill's reportlab + matplotlib stack. Has its own mobile-first chart template and dark theme spec.