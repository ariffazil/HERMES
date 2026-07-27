# Sensorium Briefing Template

## Header

```
**ASI WORLD SENSORIUM**
<day> <date> · <time> MYT
Release: RELEASE | RELEASE_WITH_HOLDS | HOLD
```

Use emoji dividers between sections: `━━━━━━━━━━━━━━━━━━━━━━━`

## Section Template — Federation Health (top section, always present)

Title: **✅ FEDERATION STATE** or **⚠️ FEDERATION STATE** (if any red flags)

Format: compact table of 6 organs. Include any anomalous repos.

```
| Organ | Port | Status |
|-------|------|--------|
| arifOS | 8088 | ✅ |
| A-FORGE | 7071 | ✅ |
| AAA | 3001 | ✅ |
| GEOX | 8081 | ✅ |
| WEALTH | 18082 | ✅ |
| WELL | 18083 | ✅ |
```

Docker infra status: one-liner — postgres ✅ · qdrant ✅ · redis ✅ · etc.

**⚠️ Perhatian:** bullet list of any active red flags detected during Federation Boot
(dirty repos with merge conflicts, T3 items stacking up, CONTEXT staleness, MCP transport issues).

If everything is green, no Perhatian section needed. Green is silent.

## Section Template — War / Geopolitics

Title: **⚔️ WAR / GEOPOLITICS / ENERGY**

Content: Chronological or consequence-ranked events. Each event:
1. **What happened** — 1-2 sentences with date
2. **Epistemic label** — (OBS/DER/INT)
3. **Sources** — outlet(s) + date

Key market data at bottom of section:
```
`$98.37/bbl · Brent crude · spot · USD · 25 Jul · Source`
```

Bottom line: 1-3 sentence synthesis of what this changes for Arif's model.

## Section Template — Malaysia

Title: **🇲🇾 MALAYSIA**

Cover in order of priority:
1. **Macro data** — GDP, inflation, fiscal, ringgit (latest official releases)
2. **Cost-of-living transmission** — fuel prices, subsidy policy, food, electricity
3. **Politics & elections** — campaign, coalitions, power dynamics, appointments
4. **Institutional** — GLCs, PETRONAS policy, regulatory changes
5. **Security** — domestic, maritime, border

Bottom line: synthesis that connects macro to household impact.

## Section Template — Oil / Gas / PETRONAS

Title: **🛢️ OIL / GAS / PETRONAS**

Cover:
- Price action (Brent, WTI, spread)
- Supply disruption signals (Hormuz, Red Sea, OPEC)
- PETRONAS deals (LNG SPAs, PSCs, upstream activity)
- Malaysia policy interface (subsidy, dividend, fuel price pass-through)

Always use the dual-analysis template (see SKILL.md Malaysia Oil Analysis Template).

## Section Template — Markets / Gold / Currencies

Title: **💹 MARKETS / GOLD / CURRENCIES**

Format: one line per instrument with full five-field data format.

After data, one-line INT assessment of what the cross-asset picture tells you.

## Section Template — AI / Agentic Systems

Title: **🤖 AI / AGENTIC SYSTEMS**

Cover:
1. **MCP/Protocol changes** — specification releases, breaking changes, ecosystem shifts
2. **Frontier models** — new releases, delays, pricing changes, regulatory moves
3. **Agentic infrastructure** — tooling, hosting, MCP server ecosystem
4. **Sovereign AI** — regulation, government access controls, Malaysia AI policy

Bottom line: what changes for arifOS and Arif's deployment decisions.

## Section Template — Watch Horizon

Title: **👁️ WATCH HORIZON**

Numbered list of the 3-7 things to watch in the next 72 hours. Each item:
- What it is
- Why it matters
- ⚠️ marker if it's breaking/urgent

## Footer

```
━━━━━━━━━━━━━━━━━━━━━━━
**Epistemic summary:** <one-line quality assessment>
```

## Telegram-Optimized Rules

- ~4000 characters total (about 500-600 words)
- One line between sections (blank line)
- Market data in code backticks for legibility
- Epistemic labels inline with claims, not footnoted
- Bold the verdict phrase, not the entire line
- No "here's what I found" or "let me walk through" — direct delivery
