# NOC/IOC Financial Analysis — Multi-Loop Refinement Methodology

> Proven: 2026-07-13 — PETRONAS 1H FY2026 prediction (3 loops, 12 figures, analyst-grade PDF, BM/English mix)

---

## When to Use

When the user asks for financial prediction, earnings forecast, or segment-level analysis of a National Oil Company (NOC) or International Oil Company (IOC). Also applies when the user says "predict their results," "what will they report," "analyst-grade forecast," "deep dive on [company] financials," "redo another loop," "refine the forecast," "final loop," or "unified analysis."

## The Multi-Loop Pattern

Single-pass forecasts are optimistic because they start from the most accessible data (commodity price) and build outward. Reality lives in second and third derivatives — FX, hidden corporate costs, structural adjustments. The discipline is to keep asking "what did I miss?" until corrections stop being material.

### Loop 1: Commodity-Price Model (Fast, Incomplete)

**Input:** Historical financials + commodity price assumption + volume growth
**Output:** Revenue/EBITDA/PATAMI projection based on price elasticity
**Typical accuracy:** ±10-15% on revenue, ±20-30% on PATAMI
**What it misses:** FX, hidden corporate costs, structural adjustments, segment-level drag

```
Revenue growth = Σ(segment_weight × commodity_yoy) + volume_yoy + fx_drag
EBITDA growth = revenue_growth × operating_leverage + opex_discipline
PATAMI growth = ebitda_growth × tax_passthrough
```

### Loop 2: Structural Adjustments (Corporate Dissection)

**Trigger:** After Loop 1, ask: "What hidden costs does the corporate structure carry?"
**Process:**
1. Identify loss-making subsidiaries inside "Corporate & Others" segment
2. Break out capex by strategy tag (core vs new business vs transition)
3. Model rightsizing/restructuring net impact (savings minus severance)
4. Add consolidation changes (M&A, full ownership transitions)
5. Add write-down risk for assets under sale consideration
6. Tighten operating leverage assumption (cost base already cut = less remaining fruit)

**Typical correction:** -5-15% from Loop 1 PATAMI

### Loop 3: External Validation (Reality Check) — CRITICAL

**Trigger:** After Loop 2, validate ALL assumptions against live external data
**Process:**
1. Check FX against central bank reference rates (BNM, MAS, etc.)
2. **Check commodity prices against LIVE market data** (TradingEconomics, CME futures, lngpriceindex.com, EIA STEO) — NOT assumed trajectories
3. Check peer Q1 results already published
4. Check geopolitical trajectory (ceasefires, sanctions, supply disruptions)
5. Check interest rate environment (affects MYR/USD cross)
6. CORRECT any assumption that doesn't match reality

**Typical correction:** -3-10% from Loop 2 PATAMI

**CRITICAL LESSON (2026-07-13):** In the PETRONAS 1H 2026 prediction, **JKM Q2 actual was $16.5/MMBtu** (observed via TradingEconomics Jul 10: $16.52). Loops 1-2 assumed $12. That single $4.5/MMBtu error = **+RM 2.3bn G&M PAT uplift** when corrected. The meta-lesson: **commodity price input matters more than segment elasticity model**. Always validate spot prices against live market data BEFORE accepting the model result.

**Procedure:**
1. Build model with assumed commodity prices
2. Before accepting, validate ALL commodity inputs against live data
3. If any input differs by >10% from live data, re-run the model
4. Publish the loop history in the deliverable (shows calibration discipline)

---

## Key Analytical Patterns

### Pattern 1: The Corporate Shadow

When a company reports "Corporate & Others" as a segment, ALWAYS ask:
- What subsidiaries are inside it?
- Which ones are loss-making?
- What % of group capex goes to Corporate?
- Is there a "transition arm" (renewables, hydrogen, EV) that burns capex at negative ROI?

**Proven example — PETRONAS Gentari:**
- IR2025: "Corporate and Others comprises primarily the renewables, hydrogen and green mobility businesses"
- This = Gentari Sdn Bhd (100% PETRONAS-owned, launched June 2022)
- Gentari estimated FY2025: ~RM 3.0bn capex, ~RM 1.25bn PAT loss
- Corp & Others without Gentari: +RM 790m PAT (positive!)
- Corp & Others with Gentari: -RM 460m LAT
- **Gentari = 270% of segment drag**
- Breakeven target: FY2028-29 at ~7-8 GW installed capacity
- Cumulative losses since inception (2022-2025): ~RM 3-4bn
- IR2025 confirmed segment = "primarily renewables, hydrogen and green mobility" — translation: Gentari burn rate

**Why this matters:** The "Corporate & Others" segment in any NOC/IOC report is a **disclosure shadow** by design. It hides loss-making transition bets, treasury volatility, and one-time items. Always decompose it before accepting the segment PAT as given.

### Pattern 2: FX as the Silent Killer

For any company that reports in local currency but earns in USD:
1. Check the central bank reference rate (not spot — use the official fixing)
2. Compare 1H avg to prior year 1H avg
3. Calculate drag on USD-denominated revenue portions
4. Model per-segment FX exposure (upstream = high, domestic marketing = low)

**Proven example:** PETRONAS — MYR strengthened from 4.65 (1H25) to 4.425 (1H26 avg) = 4.8% appreciation. 86% of borrowings are USD (RM 104.9bn). Translation effect on revenue: ~RM 0.5bn drag on upstream PAT. Interest expense: ~RM 0.3bn benefit from USD debt translation. Net P&L effect: modest but real.

### Pattern 3: Rightsizing = Bangang (Usually)

When a company announces "rightsizing" (layoffs), check:
- What structural problems does it NOT solve?
- What is the severance cost vs annual savings?
- Does it cut the right workforce quadrant?
- Is the biggest loss-maker being protected?

**APEX formula applied:**
```
BANGANG ∝ A × (1-P) × (1-X)
```
Where A = capacity (high for NOCs), P = precision (low if cuts without redesign), X = focus (low if scattered across transition bets).

**Proven example — PETRONAS:**
- Cut upstream domestic headcount + central IT layers
- But Kasawari CCS capex UP (RM 1.5-2bn/yr), Gentari capex ramping (RM 4.5bn 2026E)
- Gentari — the actual drag — untouched
- Senior knowledge capital lost to competitors (MISC, Sapura, Hess Asia)
- Downstream LAT structural (not bloat) — cutting 1,000 people saves RM 100m/yr but LAT stays at -RM 1.9bn

**Template analysis:**
```
Annual savings = headcount × avg_loaded_cost
Net Year 1 = annual_savings - severance_payout
Net Year 3 = annual_savings × 3 - severance - rehire_cost
Deferred cost = knowledge_capital_loss × years_to_rebuild
```

### Pattern 4: The Transition Arm Tax

NOCs/IOCs increasingly have "transition" or "new energy" arms (Gentari, Shell New Energies, Aramco Sustainability). These typically:
- Burn capex at 5-10x the intensity of core business
- Generate negative PAT for 5-10 years
- Are politically protected (ESG narrative, talent retention)
- Never break out standalone P&L

**The analytical move:** Estimate the drag from capex allocation × negative margin. Present it as an explicit line item in the segment map, not buried in "Corporate."

**Gentari unit economics (proven 2026-07-13):**

| Metric | Gentari | C&O ex-Gentari | Upstream (ref) |
|---|---|---|---|
| FY25 CapEx (RMm) | 3,000 | 2,681 | 19,597 |
| FY25 Revenue (RMm) | 2,000 | 11,200 | 111,900 |
| FY25 PAT (RMm) | -1,250 | +790 | +26,211 |
| Revenue/CapEx | 0.67x | 4.18x | 5.71x |

### Pattern 5: Segment Capex Efficiency Comparison

Always build a capex efficiency table:

| Segment | Capex/Rev | Capex/PAT | Payback |
|---|---|---|---|
| Upstream | x | y | z months |
| Gas/LNG | x | y | z months |
| Downstream | x | y | z months |
| Transition arm | x | negative | never |

This reveals the structural truth: where money goes vs where money comes from.

### Pattern 6: Subsidiary Read-Through (When Parent Reports Half-Yearly)

When the parent group reports half-yearly but listed subsidiaries report quarterly:
1. Collect listed-subs Q1 actuals (from Bursa/stock exchange filings)
2. Identify segment mapping — which subs contribute to which group segments
3. Apply segment elasticities to project Q2 (using commodity price assumptions)
4. Sum segments + inter-segment eliminations = group H1 estimate
5. Cross-check against peer benchmarks

**Pitfall:** Listed subs are only PARTIAL read-through. The parent has unlisted operations (Upstream is typically unlisted in NOCs). Subsidiary read-through covers Downstream + Gas Infrastructure + Marketing, but NOT the largest segment.

---

## Probability Assignment

For NOC/IOC forecasts, use geopolitical-informed probabilities:

| Scenario | Typical P | Trigger |
|---|---|---|
| Base | 45-55% | Most likely macro trajectory |
| Bull | 20-30% | Geopolitical upside (supply disruption, price spike) |
| Bear | 25-30% | Demand destruction, rapid resolution |

Adjust probabilities based on LIVE geopolitical state, not static assumptions. Example: if ceasefire collapsed yesterday, raise Bull probability.

---

## Falsification Tests (Mandatory)

Every NOC/IOC forecast MUST include falsification tests. Define explicitly:
1. What FX level would break the model
2. What commodity price would break the model
3. What corporate event would break the model
4. What geopolitical event would break the model
5. **What domestic-fiscal risk would break the model** (NOC-specific: royalty disputes, federal dividend pressure, subsidy reform)

---

## Accuracy Calibration Framework (Mandatory)

Define BEFORE the company reports:
1. What PATAMI range = "model validated"
2. What PATAMI = "bull case materialised"
3. What PATAMI = "bear case materialised"
4. List assumptions to verify against disclosure

---

## RASA-Compliant Output for Malaysian Analysis

When producing financial analysis for a Malaysian sovereign user (BM/English mix):
- Lead with meaning, not data. "G&M kini penyumbang utama" > "Gas & Maritime contributed 52%"
- Use BM for context/framing, English for technical precision
- Name the shadow directly. "Gentari sorang drag 270%"
- Never hide behind jargon
- The RASA rule from AGENTS.md applies: Think in receipts. Speak in consequences.

---

## Pitfalls

- **FX assumptions are the #1 correction source.** ALWAYS validate against live central bank data. Don't assume direction — check.
- **"Capacity" ≠ "operational."** When a company says "30-40 GW target," ask how much is COD vs under construction vs pipeline. The headline number is almost always inflated.
- **OPEX already cut = less leverage.** If OPEX dropped 16% last year, don't model 1.5x operating leverage. Use 1.25x or lower.
- **Peer benchmarking must note reporting currency.** Aramco reports in SAR (pegged to USD). Shell reports in USD. PETRONAS reports in MYR. FX differences make YoY comparisons misleading without normalization.
- **Don't model FX tailwind without checking.** The most dangerous assumption is "MYR will weaken" without checking the central bank rate and recent trajectory.
- **NOC dividend is political, not financial.** NOC dividends to government are set by political negotiation, not payout ratio formulas. Model as "max dividend at 40-45% payout" but acknowledge the political override.
- **Gentari-type entities never have standalone P&L.** You must infer from capex allocation + capacity disclosures + Integrated Report narrative. Be explicit about epistemic class (INT, not OBS).
- **Commodity price validation is MORE important than segment elasticity.** A $4.5/MMBtu JKM error moved PETRONAS group PAT by RM 2.3bn. The elasticity model was stable — the input was wrong. Always validate against live market data before accepting.
- **Don't deliver "Q[1-4] [NOC] financial result" without naming the cadence mismatch.** PETRONAS, many GLCs report half-yearly. If user asks for a period not published, open with scope correction, then deliver subsidiary read-through + model projection.
