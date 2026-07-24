# Vendor / Competitor Intelligence Research Pattern

Proven: 2026-07-09 — Tridiagonal.AI assessment for PETRONAS TriCipta AI JDA.

## When to Use

User drops a company URL and asks "how good or bad is this?" — or wants a full intelligence read on a vendor, competitor, or partner in a specific industry.

## Workflow (4-Phase)

### Phase 1: Site Inspection (What They Say About Themselves)

```
web_extract(url="[company homepage]")
web_extract(url="[company about-us]")
```

Capture: claimed capabilities, founding story, team size, revenue (if disclosed), partner logos, product names, target industries, case studies, geographic presence.

Tag everything as INT (company claim) unless independently verified.

### Phase 2: External Validation (What Others Say)

```
web_search(query="\"[company name]\" reviews reputation founder")
web_search(query="\"[company name]\" funding revenue startup [country]")
web_search(query="\"[company name]\" [partner name] [major client]")
```

Look for: Crunchbase/Tracxn profiles, LinkedIn company page, news coverage, customer case studies, partner announcements, GitHub presence (or lack thereof), founder background.

### Phase 3: Competitive Context (Who They're Up Against)

```
web_search(query="\"[company name]\" vs [competitor] [industry]")
web_search(query="[industry] AI vendors landscape 2025 2026")
```

### Phase 4: Classification + Verdict

Output structure:

| Section | Content |
|---|---|
| **What they are** | Company type, origin, size, revenue tier |
| **What they actually do** | Stripped of marketing — plain English capability |
| **Verified claims** | Table: claim → status (Verified / Claim only / Not observed) |
| **Good** | Real strengths with evidence |
| **Concerns** | Gaps, risks, unproven claims |
| **Classification** | entity, type, market, strength, weakness, threat-to-X |
| **Verdict** | One-line honest read |

## Key Discipline Rules

1. **Company claims ≠ evidence.** Tag everything. "19+ years experience" = INT until cross-referenced.
2. **No GitHub = proprietary shop.** Shift diligence from "show me code" to "show me receipts under NDA."
3. **Separate body from kulit.** Real engineering underneath ≠ marketing layer on top. Classify both independently.
4. **Domain boundary matters.** A process-optimization AI firm for refineries is NOT a subsurface AI firm. Don't conflate.
5. **Funding opacity is a signal, not proof.** No VC disclosed = plausibly bootstrapped, not proven disciplined.
6. **Force KPI framing for procurement.** If the user works at the buyer org, provide the KPIs they should demand upfront (baseline → target → timeline → sign-off).

## Pitfalls

- **Don't over-index on a single press release.** Triangulate: company site + news + LinkedIn + partner sites.
- **Don't confuse consulting engagement count with product maturity.** "2,500+ consulting engagements" ≠ 2,500 deployed products.
- **Cloudflare blocks many corporate sites.** Use web_search mirrors (KLSE Screener, Bursamalaysia, industry portals) when direct fetch fails.
- **Agentic AI / PlantGPT naming is marketing soup.** Strip the names, look at what the tool actually does.
- **IBM/Microsoft/Oracle partnerships add integration overhead.** Note it as a risk, not a benefit.