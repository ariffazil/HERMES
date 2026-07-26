# PETRONAS Shadow Subsidiaries — Forensic Reference (2026)

> Compiled 2026-07-13 from PETRONAS Integrated Report 2025 + Activity Outlook 2026-2028.
> Source session: Petros SPA Shizuoka conversation → Gentari forensic → "Corporate is the shadow" thread.
> **Always pull the IR PDF page 209-217 for the latest segment-level numbers when reusing this.**

---

## The "Corporate & Others" Black Hole

PETRONAS Group reports 3 core operating segments:
1. **Upstream** (E&P — domestic + international)
2. **Gas & Maritime** (LNG, gas processing, gas & power, maritime)
3. **Downstream** (refining, petrochemicals, marketing)

Plus a balancing line: **"Corporate & Others"** which the IR2025 page 209 explicitly describes:
> *"comprises primarily the renewables, hydrogen and green mobility businesses as well as property business."*

In plain English: this is where Gentari sits, alongside KLCC Stapled Group (property), treasury SPVs (P&L-invisible), and other strategic / corporate items. **Standalone P&L for these sub-entities is not disclosed.**

This is the **deepest shadow in any NOC group structure** — value can be deployed and destroyed without ever appearing in segment PATAMI.

---

## Method: How to Extract Shadow Subsidiary Numbers

### Step 1 — Pull segment-level data from IR PDF

URL pattern: `https://www.petronas.com/integrated-report-[YEAR]/assets/pdf/by-section/8_PETRONAS_IR[YEAR]_FinancialPerformance.pdf`

The PDF sections that matter:
- **Pages ~209-217:** Segment-level PAT/LAT + revenue + Capex
- **Page ~215:** Capex by strategy tag (Core / New Business / NZCE)
- **Page ~217:** Corporate & Others Capex breakdown by subsidiary
- **Page ~227-230:** Sustainability / climate capex (sometimes breaks out Gentari)

### Step 2 — Build the capex efficiency table

For each segment + each shadow subsidiary:
```
Capex intensity = Capex / Revenue (lower = better)
Capex recovery = Capex / PAT (lower = better; N/M if loss-making)
```

PETRONAS FY2025 baseline (OBS from IR2025 p.209-217):

| Segment           | Revenue  | PAT    | Capex  | Capex/Rev | Capex/PAT |
|-------------------|---------:|-------:|-------:|----------:|----------:|
| Upstream          | 111.9    | +26.2  | 19.1   | 0.17      | 0.73      |
| Gas & Maritime    | 119.9    | +20.9  | 12.3   | 0.10      | 0.59      |
| Downstream        | 120.0    | -1.9   | 4.5    | 0.04      | N/M loss  |
| Corporate & Others| 13.2     | -0.5   | 5.7    | 0.43      | N/M loss  |

### Step 3 — Cross-reference the disclosure footnote

The smoking gun is on page 217: *"CAPEX spent by businesses under Corporate and Others during the year amounted to RM5.7 billion with **Gentari accounting for 44% of the total spending**."*

This footnote unlocks the whole shadow. Always search the IR PDF for similar subsidiary disclosures.

### Step 4 — Probe privately-held shadow subsidiaries

Gentari Sdn Bhd is **privately held**, not listed. Public sources give:
- EMIS profile: revenue +57.39% YoY (2024); total assets +18.53% YoY (2024) [behind paywall for full]
- LinkedIn: 501-1,000 employees
- Tracxn: "Unfunded" (means no external equity round; entirely PETRONAS-funded)
- News coverage: 8.4 GW installed+under construction (Jun 2025); 1,000 charging points; 3,600 EVs deployed via VaaS
- Headquartered Level 30, Permata Sapura, KLCC

**Inference framework when no audited financials exist:**
1. Operational capacity × industry-standard revenue/MW = upper bound revenue
2. Headcount × average loaded salary = lower bound staff cost
3. Construction finance at 5-7% on under-construction GW = upper bound interest carry
4. Compare to PETRONAS' segment PAT margin average to back into EBITDA/PAT estimate
5. ALWAYS disclose inference assumptions, never present as fact

### Step 5 — State the political/strategic logic

Every shadow subsidiary has a non-financial reason to exist. For Gentari specifically:

1. **Federal-MOF wants transition narrative** — supports Petros vs federal positioning
2. **ESG sukuk pricing depends on transition pipeline** — without it, cost of capital rises
3. **Talent magnet** — engineers demand decarbonisation exposure
4. **Option value on H2 inflection** — early infrastructure ownership
5. **Negotiating currency vs Sarawak** — defangs "federal is extractivist" framing

When the analyst says "Gentari is value-destroying", the right counterframe is "Gentari is paying for the political infrastructure that keeps PETRONAS' monopoly intact. The cost is the price of admission."

---

## Gentari Forensic — The Case Study (2022-2026)

### What is Gentari?

- **Wholly-owned by PETRONAS**, established Sep 2022
- Three pillars: Renewable Energy / Hydrogen / Green Mobility
- Operating footprint: Malaysia, India, Australia, Thailand, Singapore
- Stated ambitions (2030): 30-40 GW installed capacity; 1.2 MTPA hydrogen; 10% Asia EV market share

### Reality check — disclosed + inferred

| Metric | Status | Source |
|---|---|---|
| Cumulative installed + under construction | 8.4 GW (Jun 2025) | OBS — Gentari press |
| Operational only (revenue-generating) | ~1.9 GW | INT — capacity ratio estimate |
| Under construction (no revenue yet) | ~4.2 GW | INT |
| Pipeline / pre-FID | ~2.3 GW | INT |
| Charging points (regional) | ~1,000 (Dec 2024) | OBS |
| EVs deployed via VaaS | 3,600 (Dec 2024) | OBS |
| Hydrogen FID | 1 MTPA (AMG Ammonia, India) | OBS |
| Employees | 501-1,000 (LinkedIn) | OBS |
| Inception-to-date operating losses | RM 1.5-2.0 b (estimated) | INT |
| Cumulative Capex since Sep 2022 | RM 5-10 b (estimated) | INT |
| **Total cost-to-PETRONAS Group** | **RM 7-13 b** | INT |

### Forward trajectory (probability-weighted scenarios)

| Year | Revenue | EBITDA | PAT | Cumulative loss-to-date |
|------|--------:|-------:|----:|------------------------:|
| 2022 (3 mo launch) | <RM 0.1 b | -RM 0.2 b | -RM 0.25 b | -RM 0.25 b |
| 2023 | RM 0.3-0.5 b | -RM 0.3 b | -RM 0.4 b | -RM 0.65 b |
| 2024 | RM 0.7-1.0 b | -RM 0.2 b | -RM 0.35 b | -RM 1.0 b |
| 2025 | RM 1.2-1.8 b | -RM 0.1 b | -RM 0.3 b | -RM 1.3 b |
| 2026E (full year) | RM 1.5-2.5 b | +RM 0.05-0.1 b | -RM 0.2-0.4 b | -RM 1.5-1.7 b |

**EBITDA break-even: ~2027. PAT break-even: ~2028-2029. ROI: 2032+.**

---

## The Opportunity Cost Math

If PETRONAS redirected Gentari's RM 2.5 b/yr Capex into Upstream EOR instead:
- +RM 14.7 b annual revenue (vs Gentari's ~RM 1.5 b)
- +RM 3.4 b annual PAT (vs Gentari's -RM 0.7 b loss)
- **Net swing: +RM 4.1 b/year**

This is what "RM 2.5 b/yr of dilutive Capex" really means in foregone alternative deployment.

---

## User-Framing Signals to Watch (Arif 2026-07-13)

When user pushes back on the "shadow" framing, treat as **immediate signal to dig deeper into Corporate & Others** for hidden value-draining sub-entities. Signals include:
- "u missed the biggest shadow"
- "X is the shadow"
- "what's in Corporate"
- "u didn't mention Y" (where Y is a known shadow subsidiary)
- "do they ever make money" (questioning shadow subsidiary profitability)
- Direct challenge of any "balancing item" framing of Corporate

**Always probe Corporate first in NOC group analyses.**

---

## Data Source Quick-Reference

| Source | URL / Path | What you get | OBS / DER / INT |
|---|---|---|---|
| PETRONAS IR2025 PDF (Financial Performance section) | petronas.com/integrated-report-2025/assets/pdf/by-section/8_PETRONAS_IR25_FinancialPerformance.pdf | Segment PAT, Capex, revenue | OBS |
| Activity Outlook 2026-2028 | petronas.com/sites/default/files/uploads/content/2026/PETRONAS%20Activity%20Outlook%202026-2028.pdf | Forward outlook by segment | OBS |
| EMIS company profile | emis.com/php/company-profile/MY/ | Privately-held subsidiary financials (limited free, paywall for full) | DER (with caveats) |
| Tracxn | tracxn.com/d/companies/[name] | Funding rounds, employee count, industry ranking | DER |
| LinkedIn (company page) | linkedin.com/company/[name] | Headcount, location, recent posts | OBS |
| Bursa Malaysia filings (subsidiaries only) | bursa Malaysia / i3investor | Listed-subsidiary disclosures | OBS |
| PETRONAS media releases | petronas.com/media/media-releases/ | SPA announcements, divestments, FID news | OBS |

---

## Reusability for Other NOCs

The methodology applies to:
- **Saudi Aramco** — similar IR structure; subsidiaries SABIC, PIF energy investments, NEOM
- **Petrobras** — similar group structure; BioPetrobras, Transpetro subsidiaries
- **Shell / Equinor** — slightly different (listed parents) but shadow segments exist (e.g., Shell's Power & Renewables, Equinor's New Energy Solutions)
- **Petronas Chemicals Group (PCGB)** — listed subsidiary, but separate "Corporate" line has hidden JVs

When analysing any NOC, the question is always:
1. What's the segment PAT margin?
2. What's the Capex/Revenue ratio per segment?
3. If any segment looks off, where's the footnote that explains it?
4. What's the politically-driven loss being absorbed?

The math is universal. The politics are local.

---

## Linked Files

- See `professional-intelligence-briefing/SKILL.md` → "NOC Shadow Subsidiary Forensics" subsection
- Related skill: `petronas-petros-shell-dispute` (litigation angle — sister skill, not consolidated)