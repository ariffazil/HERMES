# Research Pattern for MakcikGPT Articles

## Parallel Research Dispatch (recommended)

For complex topics (economy, politics, social fabric), dispatch 3 parallel subagents:

1. **Macro data** — GDP, inflation, currency, fiscal deficit, trade data
2. **Political dynamics** — elections, coalitions, policy changes, power shifts
3. **Structural challenges** — brain drain, inequality, institutional decay, social fabric

Each subagent uses web_search + web_extract. Results return as consolidated summaries.

## Synthesis Rule

Wait for ALL subagents to complete before writing. Don't write while research runs.

The synthesis step finds the **hidden thread** connecting all three research streams. This is the article's thesis.

## Source Hierarchy

| Priority | Source | Evidence Class |
|----------|--------|---------------|
| 1 | Official data (BNM, DOSM, BNM EMR) | OBS |
| 2 | Peer-reviewed (ISEAS, World Bank, IMF) | OBS/DER |
| 3 | Quality journalism (SCMP, Reuters, Bloomberg, EAF) | OBS |
| 4 | Malaysian media (The Edge, FMT, NST, Malay Mail) | OBS/INT |
| 5 | Social media / viral content | INT/SPEC |

## Key Sources for Malaysia Topics

- **Economy:** BNM EMR, DOSM, Trading Economics, World Bank Malaysia
- **Politics:** East Asia Forum, ISEAS, RSIS, Fulcrum.sg, SCMP
- **Social:** EMIR Research, KRI (Khazanah), UNICEF Malaysia, TalentCorp
- **PETRONAS:** Annual reports, The Edge Malaysia, Reuters
- **AI/Tech:** ISEAS, WEF, PwC AI Barometer, Layoffs.fyi

## Evidence Tagging

Every data point in the article carries:
- OBS = observed (official data, reported fact)
- INT = interpreted (analysis, pattern recognition)
- SPEC = speculated (projection, forecast)
- SHADOW = human intention (not provable, but pattern-strong)
