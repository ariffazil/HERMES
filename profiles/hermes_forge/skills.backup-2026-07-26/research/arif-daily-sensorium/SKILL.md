---
name: arif-daily-sensorium
description: >
  Produce a current, evidence-disciplined daily world and Malaysia briefing
  for Arif Fazil, architect of arifOS. Self-contained workflow — does not
  assume other skills, organs, or tools exist unless discovered at runtime.
  Search current sources, verify dates and numbers, label each conclusion
  OBS/DER/INT/SPEC/UNK, expose unresolved conflicts, and tailor consequences
  to Malaysia, petroleum geoscience, capital systems, PETRONAS, arifOS, MCP,
  and sovereign AI governance.
triggers:
  - "world sensorium"
  - "daily briefing"
  - "what changed since yesterday"
  - "brief me before work"
  - "what matters today"
  - "daily wrap-up"
  - "give me today's"
  - "sensorium"
  - "apa yang jadi semalam"
  - "catch me up on the world"
  - "ASI briefing"
  - "what just happened"
---

# Arif Daily Sensorium

One compact intelligence briefing from current evidence. Self-contained
workflow. Does not assume another skill, file, organ, connector, or tool
exists merely because it is named.

## Core Rules

1. Search the requested time window. Default: previous 24h in `Asia/Kuala_Lumpur`.
2. Identify the few changes that alter the world model. Do not repeat background.
3. Verify every load-bearing factual claim before analysis. Read [evidence-protocol.md](references/evidence-protocol.md).
4. Prefer primary and authoritative sources. Apply [source-hierarchy.md](references/source-hierarchy.md).
5. Label claims only as `OBS`, `DER`, `INT`, `SPEC`, or `UNK`.
6. **Never convert "not found" into "false". Never convert a search snippet into "confirmed".**
7. Separate event date, announcement date, publication date, effective date, and market timestamp.
8. Attach citations to all material current facts and figures.
9. Do not invent numeric confidence or briefing-fitness scores. Use release status only: `RELEASE`, `RELEASE_WITH_HOLDS`, or `HOLD`.
10. Do not claim an arifOS verdict, SEAL, receipt, authority band, or evidence tier unless a real invoked tool returns that exact state.

## Arif Relevance Profile

Domains that MATTER. Everything else is background noise.

1. **Malaysia & ASEAN** — politics, elections, cost of living, institutional dynamics
2. **Petroleum & geoscience** — oil/gas prices, OPEC, Strait of Hormuz, basin activity, PETRONAS
3. **Capital & markets** — gold (XAU/USD), oil benchmarks, currencies (MYR), interest rates, institutional stress
4. **arifOS & AI governance** — model releases, MCP/agent protocols, AI regulation, sovereign AI
5. **Geopolitical energy chokepoints** — Hormuz, Bab el-Mandeb, South China Sea, Malacca Strait
6. **Cost-of-living transmission** — fuel prices, food logistics, subsidy policy, electricity, household debt

If a news item doesn't touch one of these 6 domains, it gets ONE line max or drops.

## Workflow

### 1. Resolve Scope

Determine: cut-off time and timezone; comparison window; requested domains;
whether user wants rapid wrap-up or deeper executive briefing.

Default domains: war/geopolitics/shipping/energy security; Malaysia
economy/politics/institutions/cost of living; petroleum/LNG/PETRONAS/geoscience;
markets/currencies/rates/gold/oil/capital stress; AI models/agentic
systems/MCP/regulation/infrastructure; signals with direct relevance to Arif.

### 2. Build Candidate Event Set

Search broadly. For each candidate record: event; event date and time; source
publication date; geography; affected systems; first known primary source;
corroborating source; status (announced/scheduled/alleged/ongoing/completed/disputed).

### 3. Verify Load-Bearing Claims

Apply [evidence-protocol.md](references/evidence-protocol.md). Prioritize:
- declarations of war, ceasefires, attacks, deaths, blockades, sanctions, elections, dissolutions, appointments, policy changes;
- prices, rates, GDP, debt, production, trade, market share, model pricing;
- claims that reverse or materially change yesterday's assessment;
- surprising claims and claims supported only by snippets, social posts, or aggregators.

### 4. Label Epistemic Status

- `OBS` — directly supported by a current primary source or strong independent corroboration.
- `DER` — conclusion derived from stated observations; show the chain.
- `INT` — strategic interpretation that depends on judgment.
- `SPEC` — forward-looking scenario or hypothesis.
- `UNK` — material uncertainty, unresolved source conflict, or insufficient verification.

Do not label estimates or projections as `OBS` merely because a publication reported them.

### 5. Apply Domain Lenses

Read [domain-lenses.md](references/domain-lenses.md). Translate events through
physical, capital, institutional, and governance consequences.

### 6. Inspect Available Tools

Read [ecosystem-routing.md](references/ecosystem-routing.md).

- Use only tools visible in the current runtime.
- Verify tool names before invoking them.
- Treat specialist tools as analytical instruments, not automatic authorities.
- Continue with public evidence when an optional tool is absent.
- Keep infrastructure diagnosis separate from content accuracy.

### 7. Rank by Consequence

1. Immediate threat to life, war, energy arteries, or state stability.
2. Direct Malaysia, PETRONAS, household, or portfolio transmission.
3. Structural change in capital, technology, governance, or institutional power.
4. Early signals worth watching.

Discard duplicates, recycled commentary, personality gossip, low-consequence novelty.

### 8. Write the Briefing

Use [briefing-template.md](references/briefing-template.md). ~5 minutes readable.
Telegram-optimized (~4000 char). If too long: cut AI section first, then watch horizon.

### 9. Release Gate

- `RELEASE` — all load-bearing claims verified, material conflicts explained.
- `RELEASE_WITH_HOLDS` — central thesis usable but named claims remain `UNK` or disputed.
- `HOLD` — dominant story, key numbers, or direct consequences cannot be verified.

Before release, check:
- no missing benchmark, unit, period, currency, or timestamp;
- no conflation of separate events or participant categories;
- no old election or policy record used to deny a possible early event;
- no model release treated as real without official vendor confirmation;
- no unsupported causal leap from oil price to Malaysian benefit;
- no arbitrary score;
- no governance language implying authority not actually held.

## Market Data Format

Every market observation:

`value · instrument · benchmark/contract · currency · timestamp · source`

Example: `USD 84.73/bbl · Brent crude · ICE front-month · USD · 15 Jul 2026 16:00 UTC · CME`

Never combine two prices from different dates into one apparent current range
without explaining the time difference.

## Malaysia Oil Analysis Template

Never just say "Malaysia benefits as net oil exporter." Always include:

```
Higher crude → [upstream earnings ↑, PETRONAS cash ↑, govt revenue ↑]
BUT ALSO → [fuel subsidy cost ↑, food logistics ↑, electricity pass-through ↑,
            household purchasing power ↓, ringgit pressure]
Net effect depends on: subsidy policy response, PETRONAS dividend capacity,
RON95/diesel policy, and duration of price spike.
```

RON97 is NOT the primary vulnerability. RON95/diesel subsidy expenditure,
food logistics, electricity pass-through, and ringgit behaviour are.

## Pitfalls (Session Scars)

- **Do NOT create subsidiary skills.** These are lenses, not independent authorities.
- **Do NOT reference skills that don't exist.** Check `skills_list` first.
- **Do NOT invent governance receipts.** "L2_VERIFIED_STATE", "autonomy_band: YELLOW" — cosplay. Use OBS/DER/INT/SPEC.
- **Do NOT present ESTIMATE as OBS.**
- **Do NOT say "BN swept Johor" without a year.** There was a 2022 AND a 2026 Johor election.
- **Do NOT pad with background.** Arif knows when the Ukraine war started. Report what CHANGED.
- **Do NOT use arifOS vocabulary merely for theatrical authority.** (Beautiful One scar, 2026-07-16)
- **For Malaysian politics, search BM.** SPR, gazettes, Bernama, official state notices — not just English outlets.

## Trigger Examples

- "Give me today's ASI World Sensorium."
- "What changed overnight for Malaysia, PETRONAS, gold, oil and AI?"
- "Give me the last 24-hour wrap-up for Arif."
- "Contrast today's world state with yesterday's briefing."
- "apa yang jadi semalam?"
- "Brief me before work."

## Automation (separate from skill)

```
Schedule: 07:00 MYT daily (23:00 UTC previous day)
Delivery: Telegram DM to Arif
Fallback: Save to /root/memory/sensorium-YYYY-MM-DD.md
Mode: LLM-driven
Skills to load: arif-daily-sensorium, news-research-briefing
```
