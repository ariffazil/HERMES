# Sell-Side Analyst Report — Mode C Visual Specification

**Proven 2026-07-13:** PETRONAS 1H 2026 sector forecast — 15 pages, 8 figures (matplotlib), 14 tables, 780 KB.

The Malaysian sell-side broker format follows a tight visual contract. Every house (UOBKH, CIMB, Maybank IB, Kenanga, RHB, HLIB, PublicInvest, Affin Hwang) uses a near-identical spine. This document captures the visual specification for Mode C generation.

## House Style Comparison

| Broker | Header bar | Accent | Body font | Notes |
|---|---|---|---|---|
| **UOB Kay Hian** | Navy + gold rule | Navy #003366, Gold #C5A572 | Helvetica sans-serif | Daily research, most institutional feel |
| **CIMB** | Orange + navy rule | Orange #FF6600 | Helvetica sans-serif | Often slightly more colourful callouts |
| **Maybank IB** | Blue + yellow rule | Blue #003C9D | Helvetica sans-serif | Most data-table heavy |
| **Kenanga** | Yellow + black rule | Yellow #FECB00 | Helvetica sans-serif | Lighter feel, more retail-skewed |
| **RHB** | Red + navy rule | Red #C8102E | Helvetica sans-serif | More aggressive recommendation language |
| **HLIB** | Teal + navy rule | Teal #006D75 | Helvetica sans-serif | Mid-market positioning |
| **PublicInvest** | Green + navy rule | Green #2E7D32 | Helvetica sans-serif | Smaller cap specialist |
| **Affin Hwang** | Burgundy + grey rule | Burgundy #6E0F1A | Helvetica sans-serif | Boutique feel |

For our default Mode C, use the **UOB Kay Hian** scheme — it's the most institutional and the most widely-imitated format.

## Mode C UOB Kay Hian Visual Specification

### Page Layout
- **A4 portrait** — 21.0 × 29.7 cm
- **Margins:** 1.5 cm sides, 1.0 cm top, 1.5 cm bottom
- **Header:** Navy solid bar 1.2pt thick at y=28.0cm, gold accent rule 0.4pt at y=27.0cm (cover only)
- **Content area:** ~18.0 × 27.0 cm
- **Footer rule:** Light grey 0.4pt at y=1.2cm

### Header Bar Pattern (content pages)
```
y=28.2cm: "UOB KAY HIAN  |  EQUITY RESEARCH  |  MALAYSIA DAILY"  (navy, 7.5pt bold)
y=28.2cm: date | "Hermes-Prime (Federated Research)"  (right-aligned, med grey 7pt)
y=28.0cm: navy rule 1.2pt
```

### Footer Pattern
```
y=1.2cm: med grey rule 0.4pt
y=0.8cm: "Refer to last page for important disclosures. AC: Hermes-Prime certifies independent views."
y=0.8cm: "Page {doc.page}"  (right-aligned)
```

### Cover Page Layout
```
y=27.5-30.0cm: navy solid bar
y=27.0-27.4cm: gold accent rule
y=4.5cm spacer
y=4.0cm: "MALAYSIA DAILY"  (med grey 8pt)
y=3.5cm: TITLE (Helvetica-Bold 22pt navy)
y=2.7cm: SUBTITLE (Helvetica 11pt dark grey)
y=2.3cm: HRFlowable 1.5pt navy
y=1.8cm: recommendation banner (4-col table)
y=0.8cm: Sector Recap table
y=-0.5cm: Key Takeaways bullets (6 items, ▸ prefix)
```

### Color Palette (Mode C — UOBKH)

```python
NAVY       = '#003366'  # recommendation banner, section headers, table header rows
GOLD       = '#C5A572'  # accent rule, BUY/SELL callouts, premium signals
TEAL       = '#2A9D8F'  # BUY rating background, bullish signal markers
RED        = '#C73E1D'  # SELL rating background, bearish signal markers
LIGHT_GREY = '#F3F4F6'  # alternating table row background
DARK_GREY  = '#374151'  # body text
MED_GREY   = '#6B7280'  # captions, source attribution, footer text
```

### Typography

```python
H1: Helvetica-Bold, 14pt, NAVY, leading 16pt
H2: Helvetica-Bold, 11.5pt, NAVY, leading 14pt
H3: Helvetica-Bold, 10pt, DARK_GREY, leading 12pt
H4: Helvetica-Oblique, 8.5pt, MED_GREY, leading 10pt
Body: Helvetica, 8.8pt, DARK_GREY, JUSTIFY, leading 11.5pt
Bullet: Helvetica, 8.8pt, leftIndent 10pt, leading 11.5pt
Caption (under figures): Helvetica, 7.8pt, MED_GREY, centre
Table header: Helvetica-Bold, 7.8pt, white on navy
Table cell: Helvetica, 7.6pt, DARK_GREY
Table row alt bg: LIGHT_GREY / white
```

### Recommendation Banner Pattern

A 4-column table that sits at the top of the cover page. The first column is the rating chip, colour-coded:

| Rating | Background | Text | Meaning |
|---|---|---|---|
| **BUY** | TEAL #2A9D8F | White bold "BUY" | Expected total return > 15% over 12 months |
| **HOLD** | GOLD #C5A572 | White bold "HOLD" | Expected total return −15% to +15% |
| **SELL** | RED #C73E1D | White bold "SELL" | Expected total return < −15% |

Top row of the table is navy with white headers: `[Rating] [Last Traded Price] [Target Price (12-mth)] [Implied Upside]`

Bottom row carries the values, with the rating chip (column 0) coloured by rating.

### Sector Recap Table Pattern (Cover Page)

2-column table, Field/Detail rows, navy header row. Alternating field column backgrounds (every other Field row is light grey) for visual scanning. Used to compress:
- Sector name
- Last price reference (index + date)
- Recommendation summary
- Outlook (one line)
- Key catalyst
- Single largest risk

### Key Takeaways Bullets

6 bullets max, each starting with `▸` (U+25B8 black right-pointing small triangle — renders in DejaVu Sans). Bold lead phrase, then regular body. Keep total to 6 lines.

### Highlights Table (UOBKH signature)

This is the signature table that appears after the cover. 12-16 rows × 5-7 columns. Pattern:

| Metric (RM bil unless stated) | 2H 2025A | 1H 2025A | FY 2024A | FY 2025A | 1H 2026E | YoY % | vs FY25A |

Always include:
- Revenue (3P)
- EBITDA
- Operating Profit
- PAT (Continuing)
- CapEx
- CFFO
- ROACE (%)
- Production (kboed)
- Brent avg (USD/bbl)
- JKM avg (USD/MMBtu)
- MYR/USD
- DPS-equivalent

### Segment Deep-Dive Sub-sections

Each business unit gets one subsection with:
- H2 heading with parenthetical weight (e.g., "Upstream (60% of FY25 capex)")
- 2-paragraph narrative covering model + structural read
- "Earnings revision: nil. Catalyst: ..." closing line

### Earnings Revision Table

| Metric | Prior 1H 26E | New 1H 26E | % Change | FY 2026E (new) | FY 2027E |

Always include this — it's how analysts track model revisions across reports.

### Valuation Table (SOTP)

| Subsidiary | Code | Stake | Mkt Cap (RM bn) | Methodology | Implied Value (RM bn) |

Roll up to total PETRONAS Group SOTP, then bridge: − Net debt + Cash + Associates = Equity Value → per share equivalent.

### Peer Multiples Comparison Table

| Company | EV/EBITDA (NTM) | P/E (FY26F) | Div Yield | ROACE |

5-7 peer rows. Always include the target company. End with "Asian O&G avg" row for reference.

### Scenario Analysis Table

| Scenario | Brent (USD/bbl) | JKM (USD/MMBtu) | Prod (MMboed) | FY2026E PAT (RM bn) | YoY % | Probability |

Bear / Base / Bull + at least one Tail Risk row. Probability column adds up to 100%. Then state probability-weighted expected PAT in body text.

### Sensitivity Heatmap (matplotlib)

2D heatmap showing FY PAT (RM bn) sensitivity to two drivers (Brent × JKM, Brent × MYR, etc.). Colour scale `RdYlGn`. Annotate cells with the numeric value. Highlight the base case with a blue circle overlay. Annotated `Base case` callout.

### Risks Table

8-10 risks. Columns: `Risk | Description | Probability`. Use word "Probability" not "P" or single letter (avoids ambiguity).

### Triggers Section (Upgrade / Downgrade)

Two sub-sections: "UPGRADE triggers" and "DOWNGRADE triggers". Each is a 5-bullet list with specific thresholds (RM X / $Y / %Z) so the trigger is testable.

### Catalyst Calendar Table

| Date | Event | Expected Impact | Threshold for revision |

Date + event + impact assessment + at what threshold we'd revise. Forward 6-12 months.

### Credit Profile Table

| Metric | FY2024A | FY2025A | FY2026E | Comment |

Net debt/EBITDA, Adjusted EBITDA/Interest, FCF/Debt, Bond yields (USD 10y), Credit rating (S&P/Moody's).

### Appendix A — 5-Year Forecast

Two tables: Group-level (Revenue, EBITDA, OP, PAT, Production, CapEx, CFFO, FCF, Dividend, Net Debt, Gearing, ROACE) + Segment-level (Revenue + PAT per segment, with margin %).

### Appendix B — DCF Framework

Parameter table: WACC, Risk-free, ERP, Beta, Tax rate, CapEx/D&A ratio, Terminal growth, Implied terminal value, EV, Net debt, Other, Equity value. Followed by Key Modeling Assumptions bullet list (8-10 assumptions).

### Standard Disclaimer Block (REQUIRED)

Place on the final page(s). Two paragraphs:

1. **Disclaimer** — Standard CMSA / Bursa Malaysia language. Non-negotiable — don't rewrite substantively.
2. **AC (Analyst Certification)** — Hermes-Prime substitute disclosure for federated research.

Both should be 6.5pt med grey, justified, leading 8pt. See `templates/sell_side_analyst_report.py` `make_disclaimer_block()` for the canonical text.

## Matplotlib Figure Defaults (Mode C)

```python
NAVY = '#003366'
GOLD = '#C5A572'
TEAL = '#2A9D8F'
RED = '#C73E1D'
GREY = '#6B7280'
LIGHT_GREY = '#D1D5DB'
BLUE_LIGHT = '#9DC3E6'

plt.rcParams.update({
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
    'text.color':        '#374151',
    'axes.labelcolor':   '#374151',
    'xtick.color':       '#6B7280',
    'ytick.color':       '#6B7280',
    'axes.edgecolor':    '#6B7280',
    'grid.color':        '#D1D5DB',
    'grid.alpha':        0.3,
    'font.family':       'DejaVu Sans',
    'font.size':         10,
    'axes.spines.top':   False,
    'axes.spines.right': False,
})
```

## Common Figure Patterns (Proven)

### Pattern 1: Grouped/Stacked Bar with Highlight

For "X by Y category over time":
- Bars coloured by category
- Period being analysed highlighted with gold/red bar
- Annotation arrow pointing to highlight with one-line context

### Pattern 2: Comparison Bar with Bubble Overlay

For "Q1 NI (USD bn)" peer comparison:
- Bar = NI
- Bubble overlay = margin % (size scaled to margin)
- Different colours per company, navy for target

### Pattern 3: Waterfall / Comparison Bar

For "1H 25A vs 1H 26E segment PAT":
- Side-by-side bars
- Positive values navy, negative values red
- Annotations calling out key shifts (e.g., "G&M now 54% of group PAT")

### Pattern 4: Time Series with Event Annotation

For "Brent quarterly":
- Quarterly bars coloured by phase (gray for normal, gold for projection, red for shock)
- Annotation arrow pointing to event (e.g., "US-Iran strike Feb 28, Hormuz closure")
- Horizontal reference line at threshold (e.g., "sub-$70 baseline")

### Pattern 5: Sensitivity Heatmap

For "Brent × JKM = PAT":
- 2D heatmap with `cmap='RdYlGn'`
- Cell values annotated
- Base case highlighted with blue circle overlay
- Annotated callout

### Pattern 6: Multi-Year Trajectory Line/Bar

For "ROACE FY21-FY28E":
- Bar chart, FY25+ in gold (projection)
- Reference line at threshold
- Annotations for major events

## Verification Checklist (Before Delivering)

Run these checks on every Mode C report before sending to the user:

1. **Recommendation banner colour matches rating** (BUY=teal, HOLD=gold, SELL=red)
2. **Cover banner** has navy bar + gold rule at top
3. **All page headers** read "UOB KAY HIAN | EQUITY RESEARCH | MALAYSIA DAILY" + date
4. **All page footers** have disclaimer pointer + page number
5. **6 key takeaway bullets** on cover, each starting with `▸`
6. **Highlights table** has ≥12 rows × ≥5 columns
7. **Earnings revision** table present (Prior vs New vs % Change)
8. **Peer multiples** table present with ≥4 peers
9. **Scenario analysis** table present with ≥3 scenarios + probabilities summing to 100%
10. **Key risks** table present with ≥6 risks
11. **Upgrade / downgrade triggers** both present
12. **Catalyst calendar** table present with ≥5 future events
13. **5-year forecast** in Appendix
14. **DCF framework** with WACC in Appendix
15. **Standard disclaimer + AC block** on final page(s)
16. **Forward-looking statement** explicitly disclosed
17. **Confidence band** stated (e.g., ±15-20%)
18. **All figures embedded** (verify with `pdftotext | grep "Figure "` after render)
19. **All sources cited** with URLs (in footnotes under tables or in body text)
20. **File size** between 500KB-2MB for ~8 figures + 14 tables

## Common Mistakes to Avoid

- **Don't quote prices for non-listed entities.** PETRONAS Group is single-shareholder (Khazanah). The "price" is illustrative for the SOTP only.
- **Don't show YoY % on gross revenue** — gross includes inter-segment, double-counts. Use 3P (third-party) revenue.
- **Don't compare quarterly subs to annual Group** — mismatched cadence breaks comparability. Always label cadence.
- **Don't hide segment elasticity assumptions** — they ARE the model. Show them or admit you're guessing.
- **Don't write a Group "Q1" without saying it's a projection** — labelling as actual is F9 violation.
- **Don't use ▼▲ emojis in body text** — they render but look unprofessional in serif body. Use `▸` for bullets, `+`/`−` for signs.
- **Don't put disclaimer language in 14pt** — it's 6.5pt standard. The disclaimer is meant to be skimmed, not read.
- **Don't omit the AC certification.** Without it, Malaysian compliance framework treats the report as non-research.
- **Don't stretch a 6-page finding into 14 pages with padding.** If you have less substance, write a 6-page report. Brokers publish 4-page "Updates" too.

## Reference Bank — Sector-Specific Spine Variations

### Energy / Oil & Gas Spine (used 2026-07-13 PETRONAS)
Adds: Brent × JKM sensitivity heatmap, Production trajectory (Mboed), ROACE trend, Peer NI comparison with margin bubble overlay

### Banking / Financial Spine
Adds: NIM (net interest margin) trend, Loan book breakdown, Asset quality (NPL/GIL), Capital ratios (CET1, Tier 1), Loan growth vs deposit growth

### Plantation Spine
Adds: CPO price × volume matrix, FFB yield trend, Land bank maturity, ESG certification table

### Healthcare Spine
Adds: Hospital occupancy trend, Beds / admissions / surgical cases, Medical tourism breakdown by source country, Insurance mix

### Tech / Digital Spine
Adds: ARPU trend, Subscriber net adds, Capex intensity, Content cost, EBITDA margin progression

Always check the sector spine when adapting the template — don't force-feed an oil & gas template onto a banking report.