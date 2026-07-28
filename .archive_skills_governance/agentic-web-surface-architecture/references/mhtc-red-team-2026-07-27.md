# MHTC Red Team Case Study — 2026-07-27

> **Target:** Malaysia Healthcare Travel Council (malaysiahealthcare.org)
> **Method:** 5-step Agentic Red Team methodology
> **Domain:** Medical tourism
> **Proposed counter-architecture:** Agentic WELL medical tourism site

## Step 1 — Surface Crawl Results

| Metric | Finding |
|---|---|
| Pages crawled | 8 (of 23 discovered) |
| Content per page | ~300-1300 chars of marketing prose |
| JS dependency | Heavy SPA — HTTP fetch yields near-zero structured data |
| JSON-LD | Absent. No schema.org structured data. |
| llms.txt | Not present |
| MCP endpoint | Not present |
| Machine-readable data | ZERO — AI agents get marketing fluff only |

## Step 2 — Invariants Extracted (What MHTC Does Right)

These become requirements for the counter-architecture:

1. **Patient Journey** — Pre-Treatment → Special Lane (visa) → Treatment → Recovery → Aftercare. Clear funnel.
2. **Special Lane Immigration** — Structured visa facilitation: appointment letter → MHTC support letter → medical eVISA → print & travel.
3. **Centres of Excellence branding** — Group hospitals by specialty (Oncology, Cardiology, Fertility, Ortho), not by hospital name.
4. **Concierge Service** — Human touchpoint from airport to discharge.
5. **Accreditation Emphasis** — JCI, MSQH, ACHS, Temos as trust signals.
6. **Recovery Tourism** — "Discover Malaysia while you heal" positioning.
7. **Government Backing** — MHTC under Ministry of Health = legitimacy.

## Step 3 — Anti-Patterns Identified (What NOT to Do)

| # | Anti-Pattern | Severity | Detail |
|---|---|---|---|
| 1 | JS-heavy SPA → invisible to AI agents | CRITICAL | HTTP crawl returns ~300 chars per page. AI agents cannot read hospital lists, prices, or doctor data. |
| 2 | Zero machine-readable data | CRITICAL | No llms.txt, no JSON-LD, no MCP endpoint, no API, no structured hospital data. |
| 3 | No pricing transparency | HIGH | Claims "cost benchmarks available" but never shows prices. Patient must contact → wait → get quote. |
| 4 | "Find Hospital" is broken | HIGH | /find-hospital-filter redirects to generic prose page. Hospital search fully JS-dependent. |
| 5 | No doctor profiles | HIGH | Cannot search by doctor name, specialty, experience, or languages spoken. |
| 6 | Marketing prose only, no structured data | MEDIUM | Every page: "world-class expertise... patient-centric care..." Zero comparison data. |
| 7 | No outcomes/success rates | MEDIUM | Claims to publish success rates but none visible on site. |
| 8 | No personalization | LOW | Same experience for knee replacement patient and IVF patient. |
| 9 | No agent handoff/API | CRITICAL | Travel agents, insurers, overseas hospitals must use WhatsApp/phone — no automated integration. |

## Step 4 — Derived Architecture Requirements

| Anti-Pattern | → Requirement |
|---|---|
| SPA invisible to AI | → llms.txt + JSON-LD + MCP endpoint |
| No pricing | → Published price brackets per treatment per hospital |
| No doctor profiles | → Structured doctor directory with credentials, languages, experience |
| No outcomes | → Verified outcome data with VAULT999 sealing |
| No personalization | → Patient-to-hospital matching engine (condition + budget + location) |
| No API | → MCP tools: match, compare, estimate, dignity_check |

## Step 5 — Counter-Architecture (Agentic WELL Medical Tourism)

### Static Layer (invariants — data layer)

- Hospital registry: name, location, accreditation, beds, specialties, languages
- Doctor profiles: name, specialty, years, qualifications, languages, procedures/yr
- Treatment price brackets: per-hospital, per-procedure, min-max, what's included
- Visa process: country-specific medical eVISA requirements
- MARUAH floor: no fake testimonials, honest complication rates, verified outcomes

### Agent Surface (machine-readable — 3 layers)

| Layer | Format | Purpose |
|---|---|---|
| L1 | llms.txt / llms-full.txt | AI agent discovery |
| L2 | JSON-LD (schema.org) | Structured data per page |
| L3 | MCP endpoint | Tool-callable matching |

### MCP Tool Suite (proposed)

| Tool | Input | Output |
|---|---|---|
| medical_tourism_match | condition, budget, location, language | Ranked hospitals + reasons |
| medical_tourism_compare | hospital_ids, treatment | Side-by-side comparison |
| medical_tourism_estimate | treatment, hospital, origin_country | Total package cost (treatment + travel + stay) |
| medical_tourism_dignity_check | hospital_id | MARUAH floor verification |

### Organ Mapping

| Function | Organ | Tool |
|---|---|---|
| Ethics/dignity | WELL | well_guard_dignity |
| Patient readiness | WELL | well_assess_homeostasis |
| Hospital reliability | WELL | well_assess_reliability |
| Price comparison | WEALTH | capital_health |
| Total costing | WEALTH | capital_primitive |
| Forex/market | WEALTH | capital_market |
| Booking | A-FORGE | forge execute |
| Truth enforce | arifOS | arif_judge |
| Immutable record | arifOS | arif_seal → VAULT999 |

## Key Metric

MHTC handled RM 2.72 billion revenue from ~1.6 million medical tourists in 2024. The gap: zero agentic surface means zero automated AI referrals. This is the market opportunity.
