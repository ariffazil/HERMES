# Institutional Financial Deep Dive — NOC / NOC-Listed-Subsidiaries

Proven pattern: PETRONAS Group 1H 2026 + Q1 2026 read-through (2026-07-13).
Use when research target is a **sovereign-backed or state-owned enterprise** that publishes
**half-yearly consolidated financials**, where **listed subsidiaries publish quarterly**, and
the user asks for a period that hasn't been disclosed yet.

## When to use

- Target: National oil company, sovereign wealth fund vehicle, state-owned utility,
  government-linked conglomerate with mixed listed/unlisted structure
- User asks for a period that doesn't exist yet ("Q1 2026 [GROUP]") — flag the scope
  error FIRST, then deliver two artifacts:
  1. **Read-through from listed subsidiaries** that DO report quarterly
  2. **Model-based projection** of the unannounced period with confidence band
- Macro environment features price shocks (Brent, JKM, FX) the model must propagate

## Step 1: Scope correction up front (NON-NEGOTIABLE)

If the user asks for a period the Group doesn't report, name the category error in
the FIRST line of your reply. Do not deliver the requested number and footnote the
issue — flag the constraint and offer the right deliverables.

Pattern proven 2026-07-13: User asked "Q1 2026 PETRONAS Group financial result".
Correct reply opened with: "PETRONAS Group does NOT report quarterly — it reports
half-yearly (MFRS 134). There IS no PETRONAS Group Q1 2026 yet."

Then immediately deliver:
- **(A) Subsidiary read-through** — Q1 2026 actuals from listed subs (PGB/PCG/PETDAG for PETRONAS)
- **(B) 1H 2026 projection** — model Group half-year from sub Q1 + macro + segment elasticities

## Step 2: Source hierarchy (in order)

1. **Group consolidated financials** — annual report PDF, half-year report PDF
   (e.g., PETRONAS Group IFR for FY2025 = 26 Feb 2026 release)
2. **Listed subsidiary quarterly reports** — Bursa Malaysia / HKEx / SGX filings
   (e.g., PGB 19 May 2026, PCG 21 May 2026, PETDAG 29 May 2026)
3. **Macro price deck** — EIA STEO, Reuters polls, JKM/TTF/HH futures
4. **Peer Q1 2026 results** — same period comparables (Aramco, Shell, TotalEnergies,
   PetroChina, Sinopec). Look for direct press release URLs, not analyst summaries
5. **Industry context** — IEA monthly oil report, OPEC MOMR, IGU LNG reports

**Pitfall — Cloudflare-wrapped local press (BHarian, TheStar) often block `web_extract` and
`browser_navigate`.** Fall back to the company press release on its official site + peer
international coverage. The story is usually identical.

## Step 3: Segment elasticity framework

For a vertically-integrated NOC, model segments independently with these price
elasticities (rule-of-thumb — verify against each Group's prior year disclosures):

| Segment | Revenue driver | PAT elasticity to driver | Notes |
|---|---|---|---|
| Upstream | Brent + production | ~0.8 to Brent | 50% oil / 50% LNG sensitivity |
| Gas & Maritime | JKM + gas price + LNG volume | ~0.5 to JKM | Volume from LNG Canada / FLNG ramp |
| Downstream | Product spreads (MOPS, gasoline crack) | Inverse — high oil hurts margin | PCG chemicals follows Asia margin |
| Corporate & Other | FX + derivatives + financing | Mixed | Bond issuance cost matters |

**Realized price = benchmark − lag/discount.** For PETRONAS: realized oil ≈ Brent − $3-5/bbl,
realized LNG ≈ JKM − $1-2/MMBtu (slope-based contracts). Use the spread from prior half.

## Step 4: Translate macro deltas into segment shifts

Build a single ΔS table:

```
Δ Brent (Q1 26 vs H1 25) = +8.6%
Δ JKM (Q1 26 vs H1 25)   = +20.8%
Δ MYR/USD                  = +5.7% (USD weakens vs MYR)
```

Apply each segment:

```
Upstream PAT H1 26 estimate = H1 25 PAT × (1 + 0.5 × Δprod + 0.5 × Δrealized_oil) × FX_adj
G&M PAT H1 26 estimate     = H1 25 PAT × (1 + 0.4 × Δvolume + 0.55 × ΔJKM) × (1 + impairment_continuation)
Downstream PAT             = H1 25 PAT × margin_compression_factor + listed_sub_Q1_share
Corp & Other               = H1 25 PAT × (1 + derivative_normalization)
```

## Step 5: Subsidiary read-through scale-down

Listed subsidiary Q1 2026 numbers should be **weighted into segment estimates** by
their share of segment revenue/PAT. For PETRONAS:

- **PCG** ≈ 50% of Downstream chemicals weight
- **PETDAG** ≈ 35% of Downstream marketing weight
- **PETGAS** ≈ 90% of Gas & Maritime (gas processing + transportation + regasification)

If a subsidiary Q1 contradicts segment trajectory, investigate — likely an FX or
one-off item (PETDAG commercial segment -87% PBT from Jet A1 MOPS lag, for example).

## Step 6: Backtest the model BEFORE publishing

Pick a prior period where you have actuals. Apply the model backwards. Compare:

```
1H 2024 actual PAT: RM32.4bn
Apply -17% Brent shock → model estimate: RM28.1bn
1H 2025 actual PAT: RM26.2bn
Model error: +6.7% (over)
```

**Confidence band = max(|model − actual|/actual) over backtest runs.** For PETRONAS,
±15-20% is honest. State the band explicitly in the deliverable.

If the backtest error is >30%, **don't publish the projection without disclaimers** —
either tune the elasticities or flag the call as speculative.

## Step 7: Falsification checklist (mandatory)

Every projection MUST include a risk table with:
- **Risk name** (what would invalidate the call)
- **Impact** (in RM/USD bn or % PAT)
- **Probability** (Low / Low-Med / Medium / Medium-High / High)

For sovereign NOCs specifically, ALWAYS include:

| Risk | Why it's specific to NOCs |
|---|---|
| **Domestic fiscal dispute** (Petros-Sarawak type) | Sovereign vs state-level royalty fights that can disrupt the gas book. Often hidden from sell-side models. |
| **Project completion guarantee / DSU covenants** | NOCs often carry project finance with completion deadlines. Extension is a yellow flag. |
| **Sovereign dividend demand** | Federal government may push for larger dividend if Group PAT looks strong. |
| **Political pricing pressure** | Domestic fuel subsidies, controlled retail prices — political cycle effects. |
| **State-level ownership restructuring** | Like Eni JV in Indonesia/Malaysia — can reclassify assets as held-for-sale and trigger impairment. |

## Step 8: Deliverable structure (sector + NOC variant)

Adapted from the existing `deep-research` sector+company structure:

1. **Scope correction** — what the user asked for vs what exists
2. **Subsidiary Q1 actuals table** (read-through)
3. **Macro price deck** (Brent, JKM, FX)
4. **Group segment FY baseline** (from latest annual report)
5. **1H projection** with ΔS table + segment breakdown
6. **Peer benchmark table** — same period, real numbers, all in USD
7. **Backtest accuracy check**
8. **Falsification checklist**
9. **Bottom-line real read** — what's the story, not the numbers

## Pitfalls specific to NOC financial research

- **Don't extrapolate annual report** — use the half-yearly cadence. PETRONAS publishes
  1H report in late August, FY report in late February. Annual figures are SUM of halves.
- **Don't confuse gross vs third-party revenue.** PETRONAS reports gross (with
  inter-segment) AND third-party. YoY % on gross double-counts. Use third-party for
  group comparables, gross for segment decomposition.
- **Don't treat "record volume" as bullish PAT signal.** Volume up + price down =
  flat-to-negative PAT. PETDAG's "record 17.1bn liter sales" came with -3.5% PAT YoY
  because MOPS price increases crushed commercial margins.
- **Watch for discontinued operations.** Engen divestment (May 2024) materially
  changed PETRONAS Downstream FY2024 figures. Always check "continuing operations" line.
- **Petronas-style MYR reporting hides USD reality.** Translate to USD before peer
  benchmark. A "10% YoY PAT growth" in RM is roughly +15% in USD when MYR strengthens.
- **Effective tax rate swings are real.** 2H 2025 had 35% ETR (impairment losses),
  full year was 33%. Tax expense isn't a fixed % of profit.
- **Federal/state royalty cash payments** are in Related Party Transactions. RM10bn
  to government in FY2025. Track this as a real cash leak, not just dividend.

## Artifact pattern

Save the full deep-dive to `/root/A-FORGE/forge_work/<target>/<TARGET>-<PERIOD>-DEEP-RESEARCH.md`
as a sealed receipt, then surface the human-readable summary in Telegram. Include:
- Sources table (with URLs)
- Macro inputs (with timestamps)
- Segment model parameters (elasticities, lags, FX assumptions)
- Backtest error
- Falsification risks with probability

If the user is benchmarking their own analysis (e.g., a trader testing their model
against the LLM), the artifact is also the **scorable benchmark** — they can score
prediction vs actual when the period actually reports.

## Anti-patterns

- **Don't deliver numbers without sources.** Every figure must trace to a URL or
  a derived calculation shown step-by-step.
- **Don't hide the segment elasticity assumptions** — they ARE the model. Show them.
- **Don't compare quarterly subs to annual Group.** Mismatched cadence breaks comparability.
- **Don't forget to translate to USD for peer comparison.** RM-only reporting makes
  Petronas look small against Aramco (USD), but they're closer in margin and
  integrated economics.
- **Don't write a Group "Q1" without saying it's a projection** — labelling as
  actual is F9 violation (anti-hantu / hallucination).

## Closing loop

When the actual period reports (e.g., 1H 2026 PETRONAS in late Aug 2026), backfill
the prediction with reality. Note model error. If error >25%, document why in the
deep-research skill pitfall list. Pattern lives, library evolves.