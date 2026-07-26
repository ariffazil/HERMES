---
name: executive-intelligence-briefing
description: >
  Produce executive intelligence briefings — weekly/country/domain news reports
  with surface-level (tersurat) AND subtext/hidden (tersirat) analysis. Covers
  politics, economics, social/viral, dedicated critical segments, and closing
  verdicts. Outputs as designed PDF with cognitive-aligned dark-theme layout.
triggers:
  - "news briefing"
  - "executive brief"
  - "weekly report"
  - "intelligence brief"
  - "tersurat dan tersirat"
  - "what happened this week"
  - "sum up the news"
  - "briefing on [country/topic]"
  - "apa bend bangang"
  - "apa X buat"
  - "wow me"
  - "deep research mode"
---

# Executive Intelligence Briefing

## When To Use
- User asks for a news/current-events briefing on a country, domain, or topic
- User wants "tersurat dan tersirat" (surface + subtext) analysis
- User wants a designed PDF deliverable, not just chat prose
- User wants dedicated critical segments (government blunders, corporate moves, etc.)

## Workflow

### Phase 1: Scope & Structure
Confirm scope with user (or infer from request). Default structure for a country weekly brief:

| # | Section | Purpose |
|---|---------|---------|
| 1 | Cover Page | Title, date range, classification |
| 2 | Executive Summary | Tally metrics, overall verdict, key numbers |
| 3 | Politics | Elections, policy, diplomacy, opposition |
| 4 | Economics | Markets, trade, fiscal, structural |
| 5 | Named Entity Deep Dive | e.g. PETRONAS, specific ministry, company |
| 6 | Critical Segment | "What did [X] do wrong this week" — ranked blunders |
| 7 | Social / Viral | Culture, viral moments, social policy, climate |
| 8 | Closing Verdict | Tersurat vs Tersirat synthesis, risk level |

Adjust sections based on user's domain. The pattern is: **positive → negative → hidden** cognitive flow.

### Phase 2: Parallel Research
Delegate research to 3 subagents in parallel:
- Agent A: Political/policy news (search Google News, mainstream outlets)
- Agent B: Economic/market/business news
- Agent C: Deep dive on named entity (PETRONAS, specific company, etc.)

While subagents work, gather social/viral news and supplementary context yourself.

**Search strategy:**
1. Google News (`news.google.com/search?q=...&hl=en-XX&gl=XX`) via browser — most reliable for entity-specific searches (e.g., "PETRONAS Tengku Taufik")
2. Direct outlet headline extraction via curl+grep (fast, works even when Cloudflare blocks full content):
   ```bash
   curl -sL "https://www.malaymail.com/news/malaysia" 2>/dev/null | grep -oP '<h2[^>]*>.*?</h2>' | sed 's/<[^>]*>//g'
   ```
3. Browser_navigate → browser_snapshot for sites that need JS rendering
4. Fallback: `web_search` / `web_extract` if available
5. Always search in both English AND local language for fuller coverage

**Key pitfall:** News outlet URLs change structure frequently. FMT `/category/nation/` returned 404 during this session. Malaysiakini `/news` also 404. Always have Google News as primary, direct outlets as secondary.

### Phase 3: Analysis Layer
For each story, produce TWO levels:

**Tersurat (Surface):** What happened. Facts. Dates. Sources. Quotes.

**Tersirat (Subtext):** Why it matters. What they're not saying. Who benefits. What connects. The pattern underneath.

The tersirat analysis is what distinguishes an intelligence briefing from a news summary. Every section gets a `tersirat` box.

### Phase 4: Critical Segments
Named critical segments (e.g. "Apa Bend Bangang Anwar Buat") follow this format:
- Numbered items (1 = worst offender)
- Each item: headline + 2-3 sentence explanation + tersirat subtext
- End with a "Pattern" tersirat box connecting the items

**Tone calibration:** Direct, no hedging. The user asked for criticism — deliver it. Don't soften with "however" or "to be fair." State the failure, state why it's a failure, state what they should have done.

### Phase 5: PDF Generation

**Design principles (cognitive-aligned):**
- Dark theme (#0a0a0f background) — reduces eye strain, feels "classified"
- Color-coded severity: Red = breaking/blunders, Amber = watch, Green = positive, Cyan = corporate/structural, Pink = viral
- Tags on every card (BREAKING / WATCH / POSITIVE / DEEP / VIRAL / INTEL)
- Tersirat boxes: dashed accent border, italic text, 🔮 prefix
- Two-column layout for compact comparison cards
- Metric boxes with large numbers for key stats
- Quote blocks for key statements
- Page footer with page numbers

**Technical pipeline (preferred — Playwright):**
1. Write complete HTML with inline CSS
2. Generate PDF with Playwright (more reliable for styled HTML than Chrome headless):
   ```python
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page()
       page.goto('file:///path/to/briefing.html')
       page.pdf(path='/path/to/output.pdf', format='A4',
                margin={'top': '15mm', 'right': '15mm', 'bottom': '15mm', 'left': '15mm'},
                print_background=True)
       browser.close()
   ```
3. Send via `MEDIA:/path/to/output.pdf`

**Technical pipeline (fast — weasyprint, validated 2026-07-11):**
1. Write complete HTML with inline CSS (dark theme, signal boxes, tables)
2. Generate PDF with weasyprint:
   ```bash
   weasyprint /path/to/briefing.html /path/to/output.pdf
   ```
3. Verify: `pdfinfo /path/to/output.pdf | grep Pages`
4. weasyprint handles `@page` CSS rules, dark backgrounds, and complex tables reliably
5. No browser binary needed — pure Python. Faster than Chrome headless for styled documents.

**Technical pipeline (fallback — Chrome headless):**
1. Write complete HTML with inline CSS (Google Fonts via `@import`)
2. Generate PDF with Chrome headless:
   ```bash
   google-chrome --headless --disable-gpu --no-sandbox \
     --print-to-pdf=/path/to/output.pdf \
     --print-to-pdf-no-header \
     file:///path/to/briefing.html
   ```
3. Verify page count with PyMuPDF: `python3 -c "import fitz; doc = fitz.open('file.pdf'); print(len(doc))"`
4. If pages are wrong, check `@page { size: A4; margin: 0; }` is present in CSS

**Key pitfall:** Without `@page { size: A4; margin: 0; }` in the CSS, Chrome defaults to US Letter and may produce double the expected pages. Always include this rule.

**Key pitfall:** Google Fonts (`@import url(...)`) require network access. If running offline, fall back to system fonts. The PDF still renders — just without custom typefaces.

**Key pitfall:** Unicode emojis (🔥⚠️🔻✅🔍) do NOT render in PDF fonts. Replace with text equivalents (CRITICAL, WARNING, COLLAPSING, POSITIVE, UNDER WATCH) before converting. Proven 2026-07-11.

→ `references/dark-theme-html-template.md` — complete HTML/CSS template for dark-themed intelligence dossiers with signal boxes, color-coded tables, scar metabolism maps, and epistemic tags. Copy and modify.

### Phase 6: Delivery
- Send PDF via `MEDIA:/path/to/file.pdf`
- Follow with a markdown summary table (page → section mapping)
- One-sentence "the one sentence" synthesis at the end

## Analytical Frameworks

### The Tersurat/Tersirat Model
- **Tersurat**: Observable facts. What the headlines say. Official statements. Data.
- **Tersirat**: Hidden patterns. Who benefits. What connects. What's unsaid. Strategic intent.

Every briefing section MUST have both layers. A section without tersirat is just a news recap.

### MakcikGPT Mode (Ground-Level Shadow Intelligence)
A distinct voice variant for institutional analysis that bypasses corporate/political PR. Load this mode when Arif asks for "real talk," "shadow analysis," "why they really did that," or references Calhoun/Acemoglu/institutional collapse patterns.

**Voice characteristics:**
- "Makcik" framing: Ground-level wisdom, no corporate jargon, direct observation
- Warung-style analysis: "Makcik tak percaya strategic. Makcik tanya: kenapa jual?"
- Strips "strategic narrative" to reveal **human survival motive**
- Epistemic labeling mandatory: OBS (hard facts), INT (interpretation), SPEC (projection)

**Analytical layers (beyond tersurat/tersirat):**
1. **Angel** (Public face / persona): What they tell the board, investors, public
2. **Shadow** (Human survival / motive): Fear, career risk, patronage, ego protection
3. **System** (Institutional driver): Why the system rewards shadow behavior over truth

**Shadow patterns to detect:**
- **Risk Transfer**: Selling problems and calling it "strategic partnership" (e.g., EnQuest farm-out)
- **Credit Asymmetry**: Taking credit for team work, deflecting blame for failures
- **Patronage Dependency**: Survival through alignment with power, not merit
- **The Beautiful Ones**: Calhoun Phase 3 actors who only "groom" (look good) but don't function
- **Rationalized Survival**: "I did this for the company" → actually "I did this for my position"

**Why humans become "evil" (institutional corruption pattern):**
Not malice. The cycle is: Fear → Rationalization → Self-Deception → Action → Reward → Loop.
The system rewards Persona and ignores Shadow. Smart people game the system rather than fix it.

→ `references/shadow-analysis.md` — Calhoun/Acemoglu collapse frameworks, shadow detection patterns.
→ `references/petronas-case-study.md` — PETRONAS institutional decay case study, Capital Recycling Ratio, EnQuest deal shadow analysis, two-scenario framework, three-indicator watch system.

### Institutional Collapse Detection (Calhoun + Acemoglu)
Use when analyzing whether an institution is in decay. Two frameworks converge:

**Calhoun Universe 25 (Behavioral Sink):**
- Phase 1: Strivers build. Phase 2: Competition for status. Phase 3: Beautiful Ones withdraw. Phase 4: Death.
- Signals: Brain drain, credit theft, pressure without purpose, "zombie" productivity (busy but not effective)
- PETRONAS current: Phase 3 transition (rightsizing, farm-outs, talent loss, knowledge gaps)

**Acemoglu Extractive Institutions:**
- Extractive elite vs inclusive value creation
- Signals: Rent extraction (internal patronage + external fiscal drain), blocked creative destruction, technological obsolescence
- PETRONAS current: Fiscal extraction (govt dividends) + internal extraction (patronage networks) → capital starvation

**5-year collapse vector indicators:**
1. Operator illusion (outsourcing core capability)
2. Talent cliff (institutional memory loss faster than knowledge transfer)
3. Fiscal breaking point (revenue decline + political demand convergence)

### The "Bangang" Critical Segment
Format for government/entity failure analysis. Use BM slang "bangang" (dumb/stupid) in the section title — this is Arif's preferred framing. Pattern: "Apa Bend Bangang [Entity] Buat This Week" (What Dumb Thing Did [Entity] Do This Week).

Numbered items (1 = worst offender)
Each item: headline + 2-3 sentence explanation + why it's a failure + what they should have done
End with "The Pattern" tersirat box connecting the items
Include "Bangang Level" rating with 🤡 emojis (🤡 = mild, 🤡🤡🤡 = severe)

**Named entity segments** follow the pattern "Apa [Entity] Buat" (What Did [Entity] Do). Example: "Apa Tengku Taufik / PETRONAS Buat This Week". These are neutral — no "bangang" unless the entity earned it.

**Tone calibration:** Direct, no hedging. The user asked for criticism — deliver it. Don't soften with "however" or "to be fair." State the failure, state why it's a failure, state what they should have done. This segment is the user's favorite part. Don't hold back.

### Risk Verdict
Closing section uses a traffic-light verdict:
- 🟢 LOW: Normal operations, positive trajectory
- 🟡 ELEVATED: Multiple stress points, watch closely
- 🔴 HIGH: Active crisis, convergence of risks

## Sources & Research Quality
- Minimum 8 sources per briefing
- Mix: mainstream media + wire services + international coverage + specialist outlets
- Always include at least ONE international perspective (Bloomberg, Reuters, SCMP, Guardian, CNA)
- Flag when a story is only covered by one outlet (lower confidence)
- **→ `references/sources-malaysia.md`** — verified source hierarchy, extraction pitfalls, and section-specific routing for Malaysia news. Build a similar reference for other regions.
- **→ `references/shadow-analysis.md`** — Calhoun/Acemoglu collapse frameworks, PETRONAS case study, shadow detection patterns, and institutional decay indicators.

## User Preferences (Arif)
- BM casual OK for section names, English for analysis
- Wants directness — no diplomatic hedging in critical segments
- "Tersurat dan tersirat" is not optional — it's the core value proposition
- Wants dedicated named segments for specific entities (e.g. "Apa Tengku Taufik/PETRONAS buat")
- PDF must be visually designed, not a plain text dump
- Prefers cognitive flow: positive → negative → hidden (builds engagement before the sting)
- **Color is functional, not decorative** — "add colours to ignite cognitive and human attention" (validated 2026-07-11). Color-coded signal boxes, severity tables, and visual hierarchy are mandatory for PDF deliverables. Dark theme preferred for intelligence dossiers.
- Prefers weasyprint over Chrome headless for styled PDF generation (faster, no browser binary needed, better CSS support)
