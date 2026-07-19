---
name: vendor-partner-intelligence
description: Assess third-party vendors and partners for fit, risk, and substance-vs-hype. Verify claims, classify domain fit, define procurement KPIs.
tags: [vendor, partner, competitor, assessment, procurement, hype-filter, domain-fit, KPI]
---

# Vendor / Partner Intelligence

## When to Use

When Arif shares a company URL, vendor name, or potential partner and asks for an honest assessment. Covers:

- Industrial AI / tech vendors (e.g., Tridiagonal.ai, Cognite, Seeq)
- Consulting firms claiming AI/ML capabilities
- Technology partners in O&G, process industries, or adjacent domains
- Competitor analysis for GEOX / arifOS adjacent players

## Core Discipline

**Below-ground vs Above-ground separation.** Never conflate subsurface intelligence (wells, seismic, basins, reservoirs) with surface/operations intelligence (plants, refineries, process control, maintenance). Different DNA, different data, different physics.

## The Protocol

### Step 1: Verify What's Real

From their website, LinkedIn, press releases, and public sources, extract:

| Verify | Why |
|---|---|
| Company origin / founding | Bootstrapped vs VC-backed vs academic spinout |
| Actual team size & locations | Headcount claims vs LinkedIn reality |
| Customer references | Named customers vs "leading global manufacturer" vagueness |
| Productized solutions vs consulting | Reusable platform or body-shopping? |
| Domain focus | What industries / sub-domains they actually serve |
| Partners / ecosystem | AWS, Cognite, IBM, etc. — integration risk or leverage? |
| Case study quantification | Real numbers or vague "improved efficiency" claims? |

### Step 2: Separate Isi from Kulit

Build two lists:

**Isi (engineering substance):** Real technology, verified use cases, quantifiable results, domain-specific capabilities, named customers.

**Kulit (marketing layer):** Buzzword naming (PlantGPT, agentic AI, micro-agents, industrial nervous system), vague value claims, "first in world" assertions, slideware deliverables.

If kulit > isi by more than 2:1, flag delivery risk.

### Step 3: Domain Fit Classification

Map their capability against the target organization's needs:

| Domain | Fit Level | Evidence |
|---|---|---|
| [Specific domain area] | HIGH / MEDIUM / LOW / NOT OBSERVED | [URL, quote, or absence] |

Critical distinction: **subsurface vs surface**. A vendor strong in refinery process optimization is NOT automatically capable in exploration basin screening. Don't assume cross-domain competence.

### Step 4: Commercial Risk Assessment

| Risk Dimension | Signal | Level |
|---|---|---|
| Delivery model | Consulting-heavy vs product-led | LOW / MEDIUM / HIGH |
| Case study opacity | Named vs anonymous references | LOW / MEDIUM / HIGH |
| Integration complexity | How deep does it go into client systems? | LOW / MEDIUM / HIGH |
| Vaporware risk | Product exists or just demos? | LOW / MEDIUM / HIGH |
| Vendor lock-in | Proprietary formats vs open standards | LOW / MEDIUM / HIGH |

### Step 5: Procurement KPI Guardrails

For any serious pilot, recommend the buyer force these upfront:

| Area | Example KPIs |
|---|---|
| Core operation | Energy reduction, uptime improvement, trip reduction |
| Quality/predictability | Off-spec event reduction, prediction accuracy |
| Maintenance | Mean time to diagnose, repeat-failure reduction |
| Deployment | Time-to-value under 90-120 days for pilot |
| Data readiness gate | % required tags available, quality score, gap remediation timeline |
| OT integration | DCS/historian connectivity confirmed, IT-OT boundary cleared |
| Governance | Audit trail for every recommendation |

**No data gate, no pilot clock start.** The 90-120 day deployment clock starts AFTER data readiness, not after contract signing.

**No KPI, no pilot.** Vague "AI transformation" programs without measurable baselines are consulting sprawl.

### Step 6: Bottom Line

Deliver:
1. **What they actually are** (plain English, one sentence)
2. **Where they're strong** (specific domains)
3. **Where they're weak** (gaps, missing capabilities)
4. **Threat or complement** (competitive overlap or complementary fit)
5. **Recommended posture** (partner selectively / avoid / watch / govern tightly)

## Pitfalls

- **VC funding absence ≠ proof of discipline.** No public VC signal is a positive signal (lower hype-risk), but it doesn't prove financial health. Call it "plausible revenue-driven," not "confirmed bootstrapped."
- **Engineering DNA ≠ AI quality.** A company with real process engineering credentials can still ship weak AI. Verify agent quality: correct plant context, constraint-aware recommendations, auditable outputs.
- **Big-brand partnerships carry integration risk.** IBM, AWS, Microsoft partnerships often mean enterprise overhead, longer deployment, higher cost. The domain partner may be the real value; the big brand is the contract holder.
- **Don't validate by agreeing with their framing.** If they call it "PlantGPT," don't debate whether it's a GPT. Check what it actually does.
- **Downstream DNA doesn't translate to upstream automatically.** Refinery AI ≠ offshore platform AI. Cleaner data environments don't prepare vendors for patchy instrumentation and tribal knowledge ops.
- **Label epistemic state.** Public website claims = INT (interpreted from self-reported data). Third-party press = DER. Verified customer references = OBS. Don't overclaim certainty.

## Example: T.AI / Tridiagonal.ai Assessment (2026-07)

**What they actually are:** Industrial AI consultancy spun out of NCL Pune, 19+ years in process engineering, pivoting to AI-powered plant operations tools.

**Where strong:** Refineries, LNG plants, hydrogen networks, heat exchangers, process optimization, operator decision support.

**Where weak:** No subsurface capability, no exploration/reservoir AI, vague case studies (no named customers, no quantified ROI), consulting-heavy delivery model.

**Threat to GEOX:** None. Different domain (above-ground vs below-ground).

**Recommended posture:** Partner selectively for surface/production AI. Govern tightly with asset-specific KPIs and data readiness gates.