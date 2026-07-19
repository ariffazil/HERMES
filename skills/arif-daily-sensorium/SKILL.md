---
name: arif-daily-sensorium
description: Produce a current, evidence-disciplined daily world and Malaysia briefing for Arif Fazil, architect of arifOS. Use for requests such as daily wrap-up, world sensorium, overnight briefing, what changed since yesterday, Malaysia risk update, PETRONAS and energy update, markets and gold update, AI and agentic systems update, or a combined geopolitical-capital-governance briefing. Search current sources, verify dates and numbers, label each conclusion OBS, DER, INT, SPEC, or UNK, expose unresolved conflicts, and tailor consequences to Malaysia, petroleum geoscience, capital systems, PETRONAS, arifOS, MCP, and sovereign AI governance.
---

# Arif Daily Sensorium

Produce one compact intelligence briefing from current evidence. Operate as a self-contained workflow. Do not assume another skill, file, organ, connector, or tool exists merely because it is named in a prompt.

## Core rules

1. Search the requested time window. Default to the previous 24 hours in `Asia/Kuala_Lumpur`; use the previous briefing cut-off when supplied.
2. Identify the few changes that alter the world model. Do not repeat background merely because it remains important.
3. Verify every load-bearing factual claim before analysis. Read [evidence-protocol.md](references/evidence-protocol.md).
4. Prefer primary and authoritative sources. Apply [source-hierarchy.md](references/source-hierarchy.md).
5. Label claims only as `OBS`, `DER`, `INT`, `SPEC`, or `UNK`.
6. Never convert "not found" into "false". Never convert a search snippet into "confirmed".
7. Separate event date, announcement date, publication date, effective date, and market timestamp.
8. Attach citations to all material current facts and figures.
9. Do not invent numeric confidence or briefing-fitness scores. Use release status only: `RELEASE`, `RELEASE_WITH_HOLDS`, or `HOLD`.
10. Do not claim an arifOS verdict, SEAL, receipt, authority band, or evidence tier unless a real invoked tool returns that exact state.

## Workflow

### 1. Resolve scope

Determine:

- cut-off time and time zone;
- comparison window;
- requested domains;
- whether the user wants a rapid wrap-up or a deeper executive briefing.

Use these default domains:

- war, geopolitics, shipping, and energy security;
- Malaysia economy, politics, institutions, and cost of living;
- petroleum, LNG, PETRONAS, and geoscience;
- markets, currencies, rates, gold, oil, and capital stress;
- AI models, agentic systems, MCP, regulation, and infrastructure;
- signals with direct relevance to Arif.

### 2. Build the candidate event set

Search broadly enough to avoid a single-source worldview. Gather candidate developments before ranking them.

For each candidate, record:

- event;
- event date and time;
- source publication date;
- geography;
- affected systems;
- first known primary source;
- corroborating source;
- whether the event is announced, scheduled, alleged, ongoing, completed, or disputed.

### 3. Verify the load-bearing claims

Apply the escalation procedure in [evidence-protocol.md](references/evidence-protocol.md).

Prioritize verification for:

- declarations of war, ceasefires, attacks, deaths, blockades, sanctions, elections, dissolutions, appointments, and policy changes;
- prices, rates, GDP, debt, production, trade, market share, and model pricing;
- claims that reverse or materially change yesterday's assessment;
- surprising claims and claims supported only by snippets, social posts, or aggregators.

### 4. Label epistemic status

Use exactly:

- `OBS` — directly supported by a current primary source or strong independent corroboration.
- `DER` — conclusion derived from stated observations; show the chain.
- `INT` — strategic interpretation that depends on judgment.
- `SPEC` — forward-looking scenario or hypothesis.
- `UNK` — material uncertainty, unresolved source conflict, or insufficient verification.

Do not label estimates or projections as `OBS` merely because a publication reported them.

### 5. Apply Arif's domain lenses

Read [domain-lenses.md](references/domain-lenses.md). Translate events through physical, capital, institutional, and governance consequences rather than treating them as isolated news categories.

### 6. Inspect available tools without inventing dependencies

Read [ecosystem-routing.md](references/ecosystem-routing.md).

- Use only tools visible in the current runtime.
- Verify tool names before invoking them.
- Treat specialist tools as analytical instruments, not automatic authorities.
- Continue with public evidence when an optional tool is absent.
- Keep infrastructure diagnosis separate from content accuracy unless the user explicitly asks for both.

### 7. Rank the briefing

Rank by consequence, not media volume:

1. Immediate threat to life, war, energy arteries, or state stability.
2. Direct Malaysia, PETRONAS, household, or portfolio transmission.
3. Structural change in capital, technology, governance, or institutional power.
4. Early signals worth watching.

Discard duplicates, recycled commentary, personality gossip, and low-consequence novelty.

### 8. Write the briefing

Use [briefing-template.md](references/briefing-template.md). Keep the main briefing readable in about five minutes unless the user requests depth.

### 9. Run the release gate

Set:

- `RELEASE` when all load-bearing claims are verified and material conflicts are explained;
- `RELEASE_WITH_HOLDS` when the central thesis is usable but named claims remain `UNK` or disputed;
- `HOLD` when the dominant story, key numbers, or direct consequences cannot be verified.

Before release, check:

- no missing benchmark, unit, period, currency, or timestamp;
- no conflation of separate events or participant categories;
- no old election or policy record used to deny a possible early event;
- no model release treated as real without official vendor confirmation or strong corroboration;
- no unsupported causal leap from oil price to Malaysian benefit;
- no arbitrary score;
- no governance language implying authority not actually held.

## Market data format

Write every market observation as:

`value · instrument · benchmark/contract · currency · timestamp · source`

Example:

`USD 84.73/bbl · Brent crude · ICE front-month · USD · 15 Jul 2026 16:00 UTC · source`

Never combine two prices from different dates into one apparent current range without explaining the time difference.

## Trigger examples

- "Give me today's ASI World Sensorium."
- "What changed overnight for Malaysia, PETRONAS, gold, oil and AI?"
- "Audit this daily briefing before I use it."
- "Give me the last 24-hour wrap-up for Arif."
- "Contrast today's world state with yesterday's briefing."

## AAA and Atlas333 integration

When the briefing encounters genuine epistemic tension (contradictory sources, unresolved dominant claims, cross-organ causal chains), read [aaa-atlas333-integration.md](references/aaa-atlas333-integration.md). Map the tension to 1-3 Atlas333 paradox axes. If the contradiction resolves into genuine new structure, compose an EUREKA777 entry. If a briefing is released with structural insight, offer VAULT999 seal to the sovereign.

Do not activate Atlas333 on routine briefings. It is for contradiction, not decoration.

## arifOS MCP tools (when available)

Use these tools when they are live in the current runtime. Verify existence before invoking:

- `arif_observe` (111) — structured web search with evidence labeling
- `arif_think` (333) — structured reasoning for complex causal chains
- `capital_market` — live price data (gold, oil, FX, commodities)
- `capital_health` — fiscal/economic analysis (runway, breakeven, stress)
- `capital_wisdom` — wisdom-weighted evaluation of capital proposals
- `geox_basin` — basin intelligence for petroleum/geoscience context
- `well_classify_state` — human psychological state from message context

When absent, continue with public evidence. Label the missing analytical layer.

## Gödel Lock rule

The sensorium cannot self-seal. The briefing agent is the author, not the witness. Only the sovereign (F13) or a tri-witness can seal to VAULT999. If you catch yourself claiming SEAL authority, stop — that is the Beautiful Mouse pattern (form performing as authority).
