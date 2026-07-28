---
name: arif-daily-sensorium
description: >
  Produce a current, evidence-disciplined daily world and Malaysia briefing
  for Arif Fazil, architect of arifOS. Self-contained workflow — does not
  assume other skills, files, organs, connectors, or tools exist merely
  because they are named. Search current sources, verify dates and numbers,
  label each conclusion OBS/DER/INT/SPEC/UNK, expose unresolved conflicts,
  and tailor consequences to Malaysia, petroleum geoscience, capital systems,
  PETRONAS, arifOS, MCP, and sovereign AI governance.
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
  - "should I register"
  - "should I attend"
  - "evaluate this event"
  - "is this worth"
---

# Arif Daily Sensorium

One compact intelligence briefing from current evidence. Self-contained
workflow. Does not assume another skill, file, organ, connector, or tool
exists merely because it is named.

## Core Rules

1. Search the requested time window. Default: previous 24h in `Asia/Kuala_Lumpur`.
2. Identify the few changes that alter the world model. Do not repeat background.
3. Verify every load-bearing factual claim before analysis. Read `references/evidence-protocol.md`.
4. Prefer primary and authoritative sources.
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

### 0. Federation Boot (before any web research)

Every briefing for Arif starts with federation internal state. Do this first —
it's faster than web search and catches blockers before you invest time in analysis.

```bash
# 0a — Source vault.env
set -a && source /root/.secrets/vault.env && set +a

# 0b — Read carry-forward state (session focus, HEADs, T3 items, quick-win queue)
# CONTEXT.md is DEPRECATED as of 2026-07-27. Read reality from these instead:
jq '.[-1] // empty' /root/.local/share/arifos/carry_forward.json 2>/dev/null | head -80
cat /root/AAA/state/flow_state.json 2>/dev/null | head -80

# 0c — Probe 6 organs
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://127.0.0.1:$port/health" >/dev/null 2>&1 && echo "✅ $name" || echo "❌ $name"
done

# 0d — Dirty repos
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,arif-sites}; do
  [ -d "$d" ] && git -C "$d" status -s 2>/dev/null | wc -l | xargs -I{} echo "$(basename $d): {} dirty"
done

# 0e — Check for merge conflict markers
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do
  [ -d "$d" ] && cnt=$(git -C "$d" status -s 2>/dev/null | grep -c "^AA\|^UU\|^DD\|^DU" || true) && [ "$cnt" -gt 0 ] && echo "⚠️ $(basename $d): $cnt merge-conflict files"
done

# 0f — Check deprecation registry (file may not exist — handle gracefully)
jq .version /root/AAA/docs/deprecation-registry.json 2>/dev/null || echo "No deprecation registry found"
```

**Red flag detection** — flag these immediately in the briefing header:
- Any organ unhealthy → escalation needed
- Merge conflicts in any repo (AA/UU/DU) → BLOCKER for new forge work
- arifOS repo with 1000+ dirty files → likely merge mess (proven pattern)
- carry_forward.json missing or stale (last entry > 48h old) → session continuity risk
- flow_state.json missing → federation pulse gap (arifFLOW may be down)
- MCP tool unreachable but port health green → MCP transport issue, not organ failure
- T3 open items list growing → accumulated governance debt

Report format: table of 6 organs + arif-sites, status + short HEAD. Flag anomalies
in a "⚠️ Perhatian" section. This is OBS data — just report, don't analyse.

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

Launch web_search across all domains simultaneously. Review results, then
smart_fetch only the most promising URLs. Serial search→extract→search loops
are 3-4× slower. Verified Jul 2026.

### 3. Verify Load-Bearing Claims

Apply `references/evidence-protocol.md`. Prioritize:
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

Apply domain lenses: translate events through physical, capital, institutional, and governance consequences.

- **Physical lens:** How does this affect energy supply, shipping routes, commodity flows?
- **Capital lens:** How does this affect prices, costs, margins, subsidy burden, portfolio risk?
- **Institutional lens:** How does this affect PETRONAS, BNM, government fiscal position, subsidy policy?
- **Governance lens:** How does this affect sovereign AI, MCP protocol evolution, arifOS architecture?

### 6. Inspect Available Tools

- Use only tools visible in the current runtime.
- Verify tool names before invoking them.
- Treat specialist tools as analytical instruments, not automatic authorities.
- Continue with public evidence when an optional tool is absent.
- Keep infrastructure diagnosis separate from content accuracy.
- When web_extract fails on SearXNG backends (search-only, cannot extract URLs),
  fall back to Hound MCP smart_fetch. Verified Jul 2026.
- When WEALTH MCP returns SESSION_REQUIRED or is unreachable, fall back to these local data sources (faster than web search):
  - Gold/oil API port 3456 — three endpoints for market data:
  - `curl -sf localhost:3456/api/gold/ticker` — XAUUSD price, change, RSI (+ state: COLD/NEUTRAL/HOT/OVERBOUGHT/OVERSOLD), EMA 20/50/200, EMA trend, S/R levels, signal, confidence
  - `curl -sf localhost:3456/api/gold/macro` — DXY, VIX, US10Y, silver, USDMYR, gold-silver ratio
  - `curl -sf localhost:3456/api/gold/calendar` — this week's economic events (FOMC, CPI, NFP, consumer confidence) with dates, times, impacts, forecasts
  - WEALTH direct port 18082 — `curl -sf localhost:18082/health` for identity hash + tool count
  These are always available, sub-second response, no API key needed, no browser overhead.

**User-provided market data:** When Arif gives raw market figures himself (Bloomberg M+),
use them as the BASELINE — do not re-fetch from scratch. Focus on INTERPRETATION:
why the move happened, what it means for Malaysia, what to watch next.
If your live source disagrees with his number, flag the discrepancy with both sources cited.
Verified Jul 2026.

**Economic calendar:** Always check this week's high-impact events (FOMC, CPI, NFP)
as part of capital lens analysis. Include a compact event table in the briefing
for the current week.

### 7. Rank by Consequence

1. Immediate threat to life, war, energy arteries, or state stability.
2. Direct Malaysia, PETRONAS, household, or portfolio transmission.
3. Structural change in capital, technology, governance, or institutional power.
4. Early signals worth watching.

Discard duplicates, recycled commentary, personality gossip, low-consequence novelty.

### 8. Write the Briefing

Use `references/briefing-template.md`. ~5 minutes readable.
Telegram-optimized (~4000 char). If too long: cut AI section first, then watch horizon.

For event/conference evaluation, use `references/event-evaluation.md`.

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
- **web_extract fails on SearXNG backends.** SearXNG is search-only; it cannot extract URL content. When `"SearXNG is a search-only backend"` is returned, switch to Hound MCP `smart_fetch`. Do not retry web_extract. Verified Jul 2026.
- **Parallel-search first, then extract.** Launch `web_search` across all 6 domains simultaneously, review results, then `smart_fetch` only promising URLs. Serial search→extract→search loops are 3-4× slower. Verified Jul 2026.
- **Watch for the absence of expected events in active conflicts.** In war monitoring, "no strikes for 13 consecutive nights" is itself a reportable OBS signal, not a non-event. Always check whether a pattern was broken. Verified Jul 2026 (US-Iran pause).
- **Corroborate oil prices from ≥2 independent live sources.** CNBC, Trading Economics, crudeoilprices.today — pick two. Forbes Advisor may serve cached data (observed 18 days stale Jul 2026). Cross-check timestamps. Verified Jul 2026.
- **MCP unreachable ≠ organ down.** When an MCP tool fails (e.g. WEALTH capital_market) but curl to the port shows `{"status":"healthy"}`, the MCP transport layer is the problem — not the organ. Check port/health directly before escalating. Verified Jul 2026.
- **WEALTH MCP SESSION_REQUIRED (proven 2026-07-27).** Since FORGE 2026-07-18, all WEALTH tools (capital_market, capital_health, etc.) require a session_id from an arifOS session. Calling them without one returns {"error_code":"SESSION_REQUIRED"}. Fix: call arif_init with mode='init', actor_id='hermes-asi', requested_authority='OBSERVE_ONLY', extract session_id from response, and pass it to every WEALTH MCP tool call. If the transport then flaps, fall back to gold-api port 3456 for market data.
- **CONTEXT.md is DEPRECATED (since 2026-07-27). Do NOT rely on it.** Read `/root/.local/share/arifos/carry_forward.json` (session state) and `/root/AAA/state/flow_state.json` (federation pulse) instead. The file itself says "Reality > files." Flagging CONTEXT.md staleness as a drift signal is no longer relevant — it is permanently stale by design. Verified Jul 2026.
- **Arif may provide his own market data (M+ Bloomberg).** When he does, DON'T re-search for prices. Take his numbers as OBS, cross-reference trend context from web, and focus on INTERPRETATION (why the move, what it means for Malaysia, what to watch). He doesn't want restated prices — he wants synthesis. Verified Jul 2026 (Brent -5.54% briefing).

## Trigger Examples

- "Give me today's ASI World Sensorium."
- "What changed overnight for Malaysia, PETRONAS, gold, oil and AI?"
- "Give me the last 24-hour wrap-up for Arif."
- "Contrast today's world state with yesterday's briefing."
- "apa yang jadi semalam?"
- "Brief me before work."
- "Should I register for this conference?"
- "Is this event worth attending?"

## Automation (separate from skill)

```
Schedule: 07:00 MYT daily (23:00 UTC previous day)
Delivery: Telegram DM to Arif
Fallback: Save to /root/memory/sensorium-YYYY-MM-DD.md
Mode: LLM-driven
Skills to load: arif-daily-sensorium, news-research-briefing
```
