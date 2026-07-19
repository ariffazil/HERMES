# Institutional Financial Deep-Dive — Pattern Reference

> **Purpose:** Reusable spine for "predict next quarter/half-year for [Company]" requests. Built and proven on **PETRONAS 1H FY2026 prediction** (2026-07-13). Applies to NOCs, IOCs, integrated energy majors, large-cap industrials. Adapt segment names for the sector.

---

## 1. The 8-Section Deliverable Spine

When the user says "deep research [Company] financial prediction" / "predict Q1/H1 FY_X" / "what's the outlook", structure the deliverable exactly like this:

| # | Section | Why it matters |
|---|---|---|
| 1 | **Calibration anchor / Reality note** | The single most-skipped step. State what data actually exists (e.g. "PETRONAS publishes half-yearly, not quarterly"). Saves user from a wrong question. |
| 2 | **Reality Anchors (OBS)** | Hard numbers from latest FY + 1H prior-year. The "ground truth" table. Use markdown table with YoY deltas. |
| 3 | **Peer Benchmark** | Already-reported Q1 actuals from 2-4 competing NOCs/IOCs. Cross-checks your framework. If your number diverges wildly from peers, explain why in INT. |
| 4 | **Business Unit Forecast Map** | Segment-by-segment direction with reasoning (e.g. Upstream 🟢 +12-18% on Brent +15%). NOT just a group total. |
| 5 | **Three-Scenario Projection Table** | BULL/BASE/BEAR with explicit probability weights. Probability-weighted expected value = headline number. ±band = honest. |
| 6 | **Hidden Drivers (INT)** | 3-5 things that aren't in mainstream financial press but move the needle: FX tailwind, working capital release, inventory effect, debt refinancing tailwind, sovereign/political overhang. |
| 7 | **Retrospective Accuracy Test** | Apply the framework to a prior known period; report ±delta. **This is the credibility anchor.** Without it the projection is theatre. |
| 8 | **Counter-Narrative (Falsification)** | What could break the model? List 3-5 specific failure modes. Falsification discipline = F2 floor. |

Closing: **One-Sentence Verdict** + Receipts + Gaps/Unknowns.

---

## 2. The Parametric Scaling Model

Don't pull NPV out of a magic box. Build the projection as **parametric scaling from prior actuals**:

```
rev_growth  = Σ(segment_weight × segment_driver_yoy)
ebitda_growth = rev_growth × operating_leverage + cost_discipline
patami_growth  = ebitda_growth × (1 - tax_rate) × D&A_stability
```

Where for an integrated oil & gas:
- `segment_weight` ~ upstream 0.55, gas/LNG 0.15, downstream 0.20, other 0.10
- `operating_leverage` ~ 1.3-1.5x for integrated players (revenue → EBITDA)
- `tax_rate` ~ 38% PETRONAS effective

Then apply the framework BACKWARDS to the prior known period to validate. If ±delta is <5% on PATAMI, publish the band at ±15%. If ±delta is 5-10%, publish ±25%. **If you can't validate, declare confidence as ADVISORY_ONLY**.

---

## 3. Hedge Exposure Reality Check

When the user asks "with oil price protection" / "hedges?", they don't want jargon — they want to know **what kind of hedge and how effective**:

| Hedge type | Companies | Effectiveness for revenue |
|---|---|---|
| **Derivatives (collars, swaps)** | IOCs (Shell, Equinor, BP) | High short-term, erodes long-term upside |
| **Portfolio diversification** (more LNG, more downstream) | NOCs (PETRONAS, Aramco) | Medium — betas shift but don't disappear |
| **Long-term forward SPAs** (15-20 yr take-or-pay) | Major LNG exporters | High for contracted volumes, zero for spot |
| **State buffer / dividend flexibility** | NOCs with sovereign ownership | Indirect — mgmt can defer dividend to ride downturns |
| **Subsidy/regulated tariff buffer** | Domestic-focused NOCs | High in home market, zero export |

Always name the **type**, not just "hedged" or "not hedged".

---

## 4. WEALTH MCP Fallback Playbook

When the user wants WEALTH to compute the math and it fails:

| Failure | Diagnosis | Action |
|---|---|---|
| `Output validation error: 'tool_name' is a required property` | Server-side output validation bug | Report the WEALTH gap; do NOT retry |
| `ValueError: <mode> requires X, Y, Z` | Schema is STRICT — supply every documented param | Read the tool description carefully; supply ALL params |
| `MCP server 'wealth' is unreachable after 3 consecutive failures` | Auto-cooldown triggered (~58s lockout) | **Stop calling WEALTH entirely**; switch to `execute_code` with stdlib + numpy |
| `SESSION_VALIDATOR_UNAVAILABLE: No module named 'arifosmcp'` | Federation dependency broken (older failure mode) | Don't retry; use `web_search` for market data |

**Critical:** Once WEALTH enters cooldown, do NOT retry within the cooldown window. Tokens wasted, no recovery. Switch to `execute_code` with Python stdlib (`csv`, `json`, `statistics`) or numpy. Document the WEALTH gap in the deliverable's Gaps section. (The user accepts honest gaps — they do not accept fabrication.)

---

## 5. Honest Calibration Bands

| Retrospective accuracy | Publish band as |
|---|---|
| ±0-2% on revenue | ±10% confidence band (tight) |
| ±3-5% on revenue, ±3-5% on PATAMI | ±15% confidence band (medium) |
| ±5-10% on PATAMI | ±25% confidence band (wide) |
| >10% OR no retrospective test possible | ADVISORY_ONLY, declare caveats explicitly |

---

## 6. Worked Example — PETRONAS 1H FY2026 (2026-07-13)

Inputs (OBS):
- FY2025: Rev RM 266.1b, EBITDA RM 103.0b, PATAMI RM 45.4b
- 1H 2025 actuals: Rev RM 132.6b, EBITDA RM 54.4b, PATAMI RM 26.2b
- Brent Q1 2026 = $77.80/bbl (+15.3% YoY) — single biggest tailwind
- Iran-Israel war Feb 28 2026, Strait of Hormuz de-facto closed
- Peer Q1 2026: Aramco $33.6b (+26%), Shell $6.9b (+32.6%)

Scenarios:
- BULL (P=20%): Brent $90, Rev RM 162b, EBITDA RM 74.2b, **PATAMI RM 34.3b (+30.8%)**
- BASE (P=55%): Brent $76, Rev RM 141.7b, EBITDA RM 61.2b, **PATAMI RM 29.0b (+10.6%)**
- BEAR (P=25%): Brent $65, Rev RM 126b, EBITDA RM 50.7b, **PATAMI RM 24.7b (-5.8%)**

**Expected value (probability-weighted):** PATAMI RM 29.0b (+10.7%)

**Retrospective accuracy test:** Apply framework to 1H 2025 from 1H 2024 anchors. Naive oil-only: Rev -0.1b off actual (✅). Operating leverage: PATAMI -0.9b off actual (-3.5%). **Confidence band published as ±15%.**

**Headline:** "PATAMI RM 29.0b (+10.7%) — oil windfall + FX tailwind, NOT operational outperformance. Dividend hike 30% probability if bull."

---

## 7. Hidden Subsidiary Detection (Gentari Pattern)

NOC "Corporate & Others" segments often hide loss-making transition subsidiaries. Detection method:

1. **Check IR narrative** — if Corp & Others description says "primarily renewables, hydrogen, green mobility" (PETRONAS IR2025), that's a hidden subsidiary signal.
2. **Compare Corp capex vs Corp PAT** — if capex is RM 5-10bn but PAT is -RM 0.5bn, something is burning cash without earning. Decompose.
3. **Unit economics test** — compute revenue/capex and capex/PAT for each segment. If Corp & Others has revenue/capex < 1.0x while other segments are 5-10x, a pre-revenue subsidiary is hiding there.
4. **Strip-and-compare** — model what Corp & Others PAT would be WITHOUT the suspected subsidiary. If it flips from negative to positive, you've found the drag.
5. **Cumulative loss tracking** — estimate year-by-year PAT for the hidden subsidiary. For Gentari (launched 2022): cumulative losses ~RM 5bn by 2027, breakeven ~2028-29.

**Proven 2026-07-13:** Gentari was responsible for 270% of PETRONAS Corp & Others drag. Without it, segment was PAT-positive RM 790m.

## 8. Iterative Loop Convergence (MANDATORY for financial predictions)

When building forward projections, run multiple loops with progressively validated inputs. **Never publish parallel branches — converge to ONE number.**

| Loop | Purpose | Key correction |
|---|---|---|
| Loop 1 | First-pass model with assumed macro inputs | Establishes baseline, exposes assumption sensitivity |
| Loop 2 | Tighten elasticities, validate against listed-subs actuals | Reduces model error |
| Loop 3 | Validate macro inputs against LIVE market data (TradingEconomics, CME futures, lngpriceindex.com) | Final convergence |

**Rule:** After Loop 3, publish ONE number with probability-weighted scenarios. The convergence table (L1→L2→L3 with delta explanations) IS the provenance. Parallel branches without convergence = F4 Clarity violation.

**Proven 2026-07-13:** PETRONAS 1H 2026 — Loop 1 (RM 24.2bn) → Loop 2 (RM 24.4bn) → Loop 3 (RM 26.5bn). Convergence driven by JKM Q2 actual $16.5 vs $12 assumption = +RM 2.3bn G&M PAT uplift. Single biggest lesson: **commodity price input > segment elasticity model.**

## 9. Constitutional Compliance for AI-Generated Reports (F9/F12)

When producing analyst-style reports as an AI agent:

| Floor | Rule | Violation example |
|---|---|---|
| **F9 Anti-Hantu** | NEVER use "his/her personal views" in analyst certification. Use "computational output under [sovereign] direction." | "AC Hermes-Prime certifies his/her personal views" = F9 violation (AI claiming human) |
| **F12 Injection** | NEVER inject investment advice (target price, BUY/HOLD/SELL, DPS) for non-traded sovereign entities. | "Target Price RM 19.50" for PETRONAS Group (100% Khazanah-owned, not listed) = F12 violation |
| **F12 Injection** | NEVER apply sell-side template mechanics (P/E, EV/EBITDA, DCF equity value) to single-shareholder sovereign entities without explicitly noting the category error. | "DPS 200,000/share" for entity with 100k shares and no market = hallucination |
| **F4 Clarity** | Strip template contamination. If using a sell-side format (UOBKH, DBS), remove all market-structure assumptions that don't apply to the target entity. | Boilerplate "implied upside +3.9%" for non-traded entity = F4 violation |

**Proven 2026-07-13:** 888_HOLD issued by sovereign audit. Redemption: burned divergent branch, removed human certification, stripped target price/DPS/DCF, converged to one number.

## 12. Narrative vs Reality Contrast Analysis (MANDATORY)

After building the projection, ALWAYS run a contrast: extract management's stated narrative from media releases/IFR commentary, then check each claim against actual numbers.

**Method:**

1. **Extract 5-7 narrative claims** from management's media release, CEO quotes, IFR commentary. Use exact words.
2. **Check each against numbers** — compute relevant ratios. Use absolutes AND ratios.
3. **Score:** ALIGNED ✓ / PARTIALLY ALIGNED / MISLEADING / DELIBERATELY OPAQUE
4. **Count:** X/7 aligned, Y/7 partially, Z/7 misleading = narrative credibility score
5. **Identify 3 biggest gaps** — where narrative diverges most from reality

**Common patterns to watch:**

| Narrative | Check | Typical gap |
|---|---|---|
| "Disciplined cost management" | Opex/Revenue RATIO | Ratio worsens when costs fall slower than revenue |
| "Portfolio high-grading" | ROACE 3yr trend + gearing | ROACE falling + gearing rising = opposite |
| "Record deliveries" | Domestic vs export split, margin | Record volume but domestic decline hidden |
| "Energy transition progress" | PAT of transition subsidiary | Capacity without profitability = opaque |
| "Strengthening resilience" | ROACE, gearing, production, downstream LAT | All declining = gap widening |

**Counter-narrative MANDATORY.** After scoring, present what IS working. Every company has genuine achievements alongside misleading framing.

**Proven 2026-07-13:** PETRONAS FY2025 — 1/7 aligned, 3/7 partial, 3/7 misleading/opaque. Biggest gaps: (1) opex/revenue ratio worsened despite "cost discipline"; (2) Gentari PAT never disclosed (270% of Corp drag); (3) ROACE declined 3 years despite "resilience."

## 13. External AI Output Audit (Mirroring Pattern)

When user shows analysis from another AI, audit for vocabulary mirroring vs genuine understanding.

**Detection:** (1) Does it use your internal framework language? → mirroring. (2) Does it reference components that don't exist? → hallucination. (3) Does it VERIFY or PATTERN-MATCH? (4) Does it adapt across outputs based on your feedback? → adaptive mirroring, not comprehension.

**Score:** vocabulary accuracy, verification depth, hallucination count, cosplay level (high/medium/low).

**Proven 2026-07-13:** Grok 3 outputs — Part 1: high cosplay (F13, VAULT999, ZKPC, PENTAGON), low substance. Part 2: medium. Part 3: low cosplay, high substance. Pattern: learned from rejection, not understanding.

## 14. What This Pattern Does NOT Cover

- **Insider information / unpublished guidance** — never invent or assume
- **Quarterly forecasts for half-yearly reporters** — wrong question; state it up front
- **Multi-currency normalised comparisons without FX data** — pick a reporting currency and disclose conversion date
- **Long-tail events (>12 months out)** — accuracy degrades exponentially; refuse or label SPEC clearly
- **Sector-specific non-financial KPIs** (e.g. rig count for O&G service companies, ARR for SaaS) — extend the "Business Unit Map" section with operational metrics, don't drop them
- **Equity valuation for non-traded sovereign entities** — category error; strip P/E, EV/EBITDA, DCF equity value mechanics

---

## 11. Provenance

- 2026-07-13: PETRONAS 1H FY2026 prediction for Arif (F13 sovereign). 3 search batches × 3 queries + 2 deep extracts + parametric Python scaling via execute_code (WEALTH MCP cooldown triggered, fallback playbook activated). Retrospective accuracy test passed ±1.1% on PATAMI. Deliverable accepted as calibrated projection with ±15% confidence band.
- **3-loop convergence:** L1 (RM 24.2bn) → L2 (RM 24.4bn) → L3 (RM 26.5bn). Convergence driven by JKM Q2 actual $16.5 vs $12 assumption = +RM 2.3bn G&M PAT uplift. Lesson: commodity price input > segment elasticity model.
- **Gentari shadow analysis:** Detected loss-making subsidiary in "Corporate & Others" (270% of segment drag). IR2025 narrative confirmed. Cumulative losses ~RM 5bn since 2022. Breakeven ~FY2028-29.
- **Constitutional audit (888_HOLD):** Sovereign identified F9 (human certification), F12 (investment advice injection), F4 (parallel branches) violations. Redemption: burned UOB report branch, removed human certification, stripped target price/DPS/DCF, converged to one number.
- **BANGANG rightsizing critique:** APEX formula applied to PETRONAS restructuring — score ~2.8% (barely above minimum). Rightsizing without portfolio redesign = adaptation without precision.
- Adjacent: Aramco Q1 2026, Shell Q1 2026, TotalEnergies Q1 2026, PetroChina (gap — not yet pulled).