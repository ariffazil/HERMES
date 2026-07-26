---
name: news-research-briefing
description: >-
  Research current news and produce structured executive briefings.
  Multi-source web research → synthesized briefing with sections
  (politics, economics, social/culture), numbered items, bold highlights,
  and a bottom-line summary per section. Handles paywalls, timeouts,
  and source fallbacks. Use when Arif asks for a 'news briefing',
  'executive briefing', 'what's happening in X today', 'catch me up',
  or any structured current-events synthesis request.
tags: [news, briefing, research, current-events, executive]
triggers:
  - "news briefing"
  - "executive briefing"
  - "what's happening"
  - "catch me up"
  - "today's news"
  - "what do I need to know"
  - "what's brewing"
  - "apa yang bakar"
  - "tell me everything about"
  - "so what"
---

# News Research & Briefing

## When to Load

When the user asks for a news briefing, executive summary of current events,
"what's happening in [country/topic] today", or structured catch-up on a
region or domain.

## Workflow

### 0. Classify the Request Depth

Not all briefing requests are equal. Match the depth to the ask:

| Request type | Example | Depth | Output |
|---|---|---|---|
| **Quick scan** | "what's the news today" | 3-5 items/section | News briefing |
| **Deep dive** | "tell me everything about X" | 8-10 items/section | Structured report |
| **"What's brewing"** | "apa yang bakar", "what's brewing" | Multi-layer analysis | Intelligence assessment |
| **Domain probe** | "how does AI affect Malaysia" | Cross-domain data+policy+social | Analysis with OBS/DER/INT/SPEC |

**"What's brewing" requests** are deeper than news. They want:
- Hard data (GDP, rates, indicators) — OBS
- Political dynamics (coalition, elections, power plays) — DER/INT
- Social fabric (rakyat sentiment, cost of living, brain drain) — INT
- Structural analysis using frameworks (Acemoglu extractive institutions, Calhoun phases) — SPEC labeled
- Honest contradictions ("GDP naik tapi rakyat rasa susah")
- NOT just news aggregation — they want the "so what" beneath the surface

### 0b. Parallel Delegation (for deep dives)

For "what's brewing" and "tell me everything" requests, spawn 3 parallel subagents:

```
Task 1: Macro data (GDP, inflation, currency, trade, fiscal, rates)
Task 2: Political dynamics (elections, coalitions, policy, leadership)
Task 3: Structural challenges (inequality, brain drain, institutional quality, demographics)
```

Each subagent does its own web_search + web_extract. Results consolidate into the parent session for synthesis.

**Why parallel:** 3 agents × 6 API calls each = 18 data points in ~2 minutes. Serial = ~6 minutes. Arif doesn't wait well.

### 0c. "Everything" Requests — Include the Drama

When the user says "tell me everything," "everything I need to know," or
"what's happening" — **do NOT limit to politics + economics + markets.**
The user wants the FULL picture including:

- **Crime & incidents** — murders, scams, busts, accidents
- **Entertainment & celebrity** — film releases, scandals, viral moments
- **Human drama** — viral stories, emotional incidents, school tragedies
- **Social media storms** — trending topics, TikTok drama, public outrage
- **Sports** — if relevant (World Cup, Olympics, national team)

**Search strategy for drama/scandal content** (these don't surface in
standard news queries):
- **mStar** `mstar.com.my/hiburan` — #1 BM entertainment/scandal source (validated Jul 2026)
- **Says.com** `says.com/my/news` and `says.com/my/entertainment` — EN viral/human drama (validated Jul 2026)
- Search `site:mstar.com.my/hiburan` for celebrity scandal
- Malay Mail `/news/life` for lifestyle/culture
- NST trending bar for what's actually viral right now

**Section order for "everything" requests** (user preference, validated):
Politics → Crime & Drama → Social/Policy → Entertainment → Other

**Pitfall:** A politics-only briefing when the user asked for "everything"
feels incomplete and sanitized. The user wants to KNOW what people are
talking about — including the messy, emotional, gossipy stuff.

### 0d. Scope Narrowing — Go Deeper, Not Just Filtered

When the user follows up with "Focus on X" or "Now do [country] domestic"
— they want MORE DEPTH in that area, not just the subset of the global
briefing that happened to mention X. Re-search with targeted queries:

- Country-specific sources (not just AP/Reuters global)
- Local crime, entertainment, viral stories
- Regional/niche outlets (state-level, language-specific)
- Live/developing coverage if applicable

**Pitfall:** Taking the global briefing and just extracting the Malaysia
paragraphs feels lazy. The user wants what was MISSING — the domestic
scandal, the local drama, the human stories that don't make global feeds.

### 1. Determine Scope

- **Region**: country, city, or global
- **Sections**: user specifies order (default: Politics → Economics → Social)
- **Depth**: quick scan (3-5 items/section) or deep dive (8-10 items/section)

### 1b. Market Data Extraction (when brief includes financial data)

**→ `references/market-data-sources.md`** — exact URLs, extraction patterns, and pitfalls for CNBC, XE, Google Finance, and alternatives.

Quick reference (validated Jul 2026):

| Instrument | Source | URL Pattern |
|---|---|---|
| Gold (XAU/USD) | CNBC | `cnbc.com/quotes/XAU=` |
| WTI Crude | CNBC | `cnbc.com/quotes/%40CL.1` (NOT `CL=F`) |
| Brent Crude | CNBC | `cnbc.com/quotes/%40LCO.1` (NOT `BZ=F`) |
| USD/MYR | XE | `xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MYR` |

**Browser extraction for CNBC:** `browser_console(expression="document.querySelector('main').innerText.substring(0, 3000)")`

Every market price MUST carry: `instrument · value · change · source · timestamp`

### 2. Source Selection & Fallback Chain

Try sources in this order. **Never stop at the first failure.**

```
Tier 1: web_search (fastest, broadest — may fail on 402/payment)
  ↓ fail
Tier 2: web_extract on news URLs (may fail on paywalls)
  ↓ fail
Tier 3: browser_navigate → browser_snapshot (always works, slower)
  ↓ need more detail
Tier 4: browser_scroll → browser_snapshot(full=true) for deeper content
```

**Critical pitfalls:**
- `web_search` via Tavily returns 402 when credits exhausted → fall back immediately to browser
- `web_extract` fails on paywalled sites (Malaysiakini, WSJ, Bloomberg) → use browser instead
- **`web_search` AND `web_extract` both return HTTP 432 simultaneously** → Tavily backend is fully down (not just one source). Do NOT keep retrying — switch immediately to Hound MCP smart_search or browser-based extraction. Verified Jul 2026. The 432 vs 402 distinction matters: 432 = backend-wide outage, 402 = per-call quota.
- **Search fallback hierarchy (2026-07-22):** When Tavily is down: 1) Hound MCP `smart_search` (10 keyless backends, parallel, always available), 2) `smart_fetch` on known news URLs, 3) `browser_navigate` to news homepages. Hound is significantly faster than browser — make it the default Tier 2.
- **WEALTH MCP may be unreachable (2026-07-22):** `capital_market` returns SESSION_REQUIRED or becomes fully unreachable after consecutive failures. Fall back to Hound MCP + browser for market data. Do NOT block on WEALTH availability — briefings ship with DER/UNK labels instead.
- **Market data staleness (2026-07-22):** Forbes Advisor gold price page may return Internet Archive cached data (e.g., Jul 4 gold on Jul 22 — 18 days stale). Always corroborate with a second live source (FXStreet, USA Today, or Kitco browser snapshot). Investing.com is paywalled — Hound snippet prices are DER, not OBS. XE.com via browser returns live mid-market USD/MYR with UTC timestamp in visible snapshot text — preferred for currency.
- Category/tag pages often 404 (e.g., `/tags/economy`, `/category/nation/`) → try homepage then scroll
- News homepages often show "Most Read" sidebar in snapshots → scroll past it to get actual articles
- Some sites timeout on first load → retry once, then skip and note the gap
- Browser snapshots return navigation/sidebar content mixed with articles → filter mentally for actual story headlines
- **For clean article body extraction via browser**, use `browser_console(expression="document.querySelector('article') ? document.querySelector('article').innerText : document.body.innerText.substring(0, 8000)")` — this returns just the article text, skipping navigation/sidebar noise. Much sharper than reading the full accessibility snapshot. Verified Jul 2026.
- **Tag feeds for named actors** (e.g., `freemalaysiatoday.com/category/tag/zahid-hamidi`, `category/tag/anwar-ibrahim`) aggregate all recent stories about a specific person with timestamps — far better than scraping news homepages for political research on a named actor. Use these when the user names a person and asks for their recent political activity.
- **FMT `/category/nation/` returns 404** (as of Jul 2026). Use the homepage (`freemalaysiatoday.com/`) — it has the same headlines in the "LATEST HEADLINES" sidebar. The homepage trending topics bar shows what's actually being searched. Validated Jul 2026.
- **FMT article extraction via browser_console:** `document.querySelectorAll('article h3').forEach(h => headlines.push(h.innerText.trim()))` — gets clean headline list from homepage.

### 3. Source Hierarchy by Region

**Single-source caveat (lead with it):** When the user names specific sources and all of them fail, do NOT silently substitute a different outlet and pretend the brief used the requested ones. Open the headline summary with an explicit "Sources used: <X> only — NST/Malay Mail/The Star were unreachable due to <Y>" line BEFORE the findings. Users notice when their named sources aren't cited. Hiding the gap in a footer is insufficient. Verified Jul 2026 (Malaysia politics weekly — FMT only, all three named outlets timed out on Tavily).

**→ `references/sources-malaysia.md`** — verified source hierarchy, extraction pitfalls, and section-specific routing for Malaysia news.
**→ `references/malaysia-election-live-coverage.md`** — live election night workflow, source patterns, key data points, and Malaysia political context.

For other regions, build a similar hierarchy:
1. Primary English-language outlet (newspaper of record)
2. Independent/alternative outlet
3. Business/financial outlet
4. Lifestyle/entertainment outlet (e.g., Malay Mail Showbiz, The Star Lifestyle)
5. Crime/local news outlet (e.g., The Sun Malaysia crime, NST Viral)
6. Social/trending aggregator (Instagram trending, TikTok, Google News local)

**For entertainment/scandal/crime content**, use dedicated sources:
- **mStar** `mstar.com.my/hiburan` — celebrity scandal, gossip, drama (BM)
- **Says.com** `says.com/my/entertainment` — viral stories, human interest (EN)
- `malaymail.com/news/life` — lifestyle, culture
- `nst.com.my` trending bar — what's actually viral
- Google News Malaysia local tab

### 4. Output Format

Per section, use this structure:

```
**[EMOJI] SECTION TITLE — Date**

| Metric | Value | Context |  ← (if applicable)

1. **Headline in bold** — 1-2 sentence analysis with "so what" for the reader.
2. **Next headline** — analysis.
...

**⚙️ BOTTOM LINE:**
1-3 sentence synthesis. What matters. What to watch.
```

**Formatting rules:**
- Number items within each section
- Bold the key phrase, not the whole line
- Add a "BOTTOM LINE" synthesis per section — this is the highest-value part
- Use tables for metrics/comparisons, not prose
- Include a global BOTTOM LINE at the very end if multiple sections
- Keep items to 2-4 sentences each — briefing, not article

### 5. Quality Checks Before Delivery

- [ ] Each section has at least 3 items (or explicit "thin day" note)
- [ ] No item is just a headline — every one has analysis/"so what"
- [ ] Bottom line synthesizes, doesn't just repeat
- [ ] Sources are named when citing specific reporting
- [ ] Conflicting narratives are flagged, not smoothed over
- [ ] Trending/viral items include *why* they're trending, not just what
- [ ] Data contradictions highlighted (e.g., "GDP up but household debt 84% of GDP")
- [ ] Epistemic labels on key claims (OBS/DER/INT/SPEC)
- [ ] Structural "so what" beyond surface facts — what does this MEAN for the reader

### 5c. Live/Developing Events (Elections, Breaking News)

When covering a live event (election night, breaking crisis, developing
story):

1. **Acknowledge incompleteness upfront** — "Results still coming in" or
   "as of [time]." Don't present partial results as final.
2. **Use live pages** — `web_extract` on NST/The Star/Malaysiakini live
   blogs gets real-time vote counts. Check multiple sources for cross-
   validation.
3. **Show the math** — present actual vote counts where available, not
   just "leading." Example: "BN 9,683 vs PH 8,706" not just "BN leads."
4. **Time-stamp everything** — "as of 6:27pm" is critical for live results.
5. **Separate confirmed vs unofficial** — EC official results vs media
   unofficial tallies vs party self-reports. Label each.
6. **Provide context for partial results** — "X of 56 seats counted,"
   "turnout was Y%," "this seat was Z party in 2022."
7. **Follow-up opportunity** — after presenting partial results, offer
   to check again in 30-60 minutes for updates.

**Pitfall:** Presenting early leads as final results. Election nights
shift dramatically. Always caveat with "unofficial" and "counting
continues."

### 5a. Analysis & Contrast Follow-up

When the user gets a factual briefing and then asks "what's the contrast?",
"any surprises?", or "what does this all mean?" — they want **interpretation,
not more facts.** They already have the data.

Pattern:
1. **Comparison table** — previous vs current state (election, quarter, year)
2. **3-4 surprises** — things that defied expectations, with WHY they're surprising
3. **Stakeholder-by-stakeholder "so what"** — winner, loser, third party, rakyat, next event
4. **Power dynamics shift** — who has leverage over whom now
5. **Prediction/forward look** — what this means for the next milestone

**Pitfall:** Restating the results in different words. The user wants the PATTERN
underneath the numbers — what connects, what surprised, what it predicts.

**Pitfall:** Being wishy-washy. If the data shows a supermajority, say "BN
dominates" — don't hedge with "it remains to be seen." Label confidence levels
(OBS/DER/INT/SPEC) but still commit to a read.

### 5b. When Arif Pastes External Content

If Arif pastes a large block of text (from another AI, from a document, from a colleague) and asks for assessment:

- **Do NOT agree by default.** Read it critically.
- **Challenge aspirational claims.** If it says "solved" — check if it really is. If it says "complete" — check what's missing.
- **Label what's real vs what's aspirational.** "This part is OBS (live system). This part is SPEC (not yet built)."
- **Arif values honest critique more than agreement.** A reality check that pushes back earns more trust than a summary that validates everything.
- **Pattern:** "X is genuinely strong. Y needs challenge. Z doesn't exist yet." — not "great document, very comprehensive."

### 5d. External AI Output Critique & Integration

When Arif shows outputs from another AI (Grok, Gemini, ChatGPT, etc.) — especially
syntheses, briefings, or analyses — he wants **critique, not validation**. He's
testing whether you can separate signal from theatre.

**Process:**
1. **Identify what the external AI caught that you missed.** Credit it honestly.
   This is the highest-value extraction — the external AI's unique signal.
2. **Identify what you caught that the external AI missed.** Your angle matters too.
3. **Separate genuine insights from performative frameworks.** Common performative
   patterns in AI syntheses (validated Jul 2026):
   - **Dashboards/Gauges/Thermometers** — subjective readings disguised as data.
     "Moral Temperature: 🌡️ Volatile" is an opinion wearing a gauge costume.
   - **Confidence scores without models** — "68/100" derived from nothing.
     Looks rigorous. Isn't.
   - **Boundary/ownership tables** — "Layer ownership: Lead: arifOS, Supporting:
     WELL" — who is this for? It's theatre.
   - **Ritual language repetition** — same phrase repeated at end of every section
     like a prayer bead. Not analysis, not signal.
   - **"Scar metabolism" / invented psychological frameworks** — narrative cosplay
     dressed as systematic analysis.
4. **Build a contrast table** — what External AI says vs what you say vs combined.
5. **Produce one clean synthesis** — the insights worth keeping, without the packaging.

**Pitfall:** Agreeing with everything because it sounds sophisticated. Arif
can see through performative rigour. Call it out.

**Pitfall:** Dismissing everything because it came from another AI. The external
output may have genuine signals you missed. Extract the signal, discard the
packaging.

→ `references/external-ai-critique-pattern.md` — detailed pattern with examples.

### 5e. Visual Document Generation (HTML → PDF)

When Arif asks for a "PDF to read" or a formatted deliverable — especially for
news briefings, intelligence reports, or civic summaries — use styled HTML
converted to PDF via Chrome headless. Not plain text. Not reportlab.

**Workflow:**
1. Write styled HTML with:
   - Dark gradient cover page with title + tagline
   - Colour-coded section headers (red=politics, purple=human, green=capital, etc.)
   - Stat cards with gradients for key numbers
   - Coloured callout boxes (red=warning, green=positive, amber=caution)
   - Tables with coloured headers
   - Numbered pills for ranked items
   - Clean typography (Segoe UI / Helvetica Neue / Arial)
2. Save HTML to `/root/[title].html`
3. Convert: `google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="/root/[title].pdf" --print-to-pdf-no-header "/root/[title].html"`
4. Send with `MEDIA:/root/[title].pdf`

**Design principles (Arif preference, validated Jul 2026):**
- "Add colours to ignite cognitive and human attention" — colour is functional, not decorative
- Gradient stat cards catch the eye before prose
- Callout boxes (coloured left-border) frame the key takeaways
- Section header colours create visual rhythm — each section feels different
- Human language throughout — no spec-sheet energy, no jargon
- Bold the uncomfortable questions, not just the safe ones
- Contrast tables (2022 vs 2026) are more powerful than paragraphs

**Pitfall:** Producing plain-text briefings when Arif asks for "a PDF to read."
He wants something that's visually engaging, not a printout of a chat log.

### 6. Tone

- INTJ executive briefing: direct, terse, high-signal
- No preamble, no "here's what I found"
- Opinion permitted when labeled (INT/SPEC) — "this is the one to watch"
- Snark allowed for viral/culture sections — match the energy
