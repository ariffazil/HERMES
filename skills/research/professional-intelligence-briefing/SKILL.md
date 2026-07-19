---
name: professional-intelligence-briefing
description: "Real-time professional intelligence briefings in social/field settings. Quick, structured answers combining web search + domain tools, delivered bilingually (BM casual + English technical). For Malaysian O&G, corporate, and career intelligence."
version: 1.0.0
author: Hermes Agent
tags: [briefing, intelligence, malaysian-og, corporate, career, real-time, bilingual]
triggers:
  - "siapa X"
  - "apa reality X sekarang"
  - "bila Y"
  - "bagi data kat dia"
  - "raja tanya"
  - "hang ada data X"
  - "Hermes ASI sila bagi nasihat"
  - "social fabric"
  - "apa yang bakar"
  - "what's brewing"
  - "rakyat"
  - "activate wealth intelligence"
  - "activate geox intelligence"
  - "activate [organ] intelligence"
  - "tell me everything about X"
  - Arif is with someone and needs instant domain intelligence
---

# Professional Intelligence Briefing

Real-time intelligence delivery for professional social settings. Not deep research — this is rapid, conversational, high-signal briefing when Arif is with colleagues, clients, or contacts and needs instant answers.

## When to Use

- Arif is in a social/professional setting (KLCC lepak, dinner, conference corridor)
- Someone asks a domain question and Arif needs instant, credible intel
- Arif says "bagi nasihat kat dia" / "brief him" — you're briefing THROUGH Arif to a third party
- Rapid-fire Q&A: personnel, corporate, technical, timeline questions
- Arif introduces you to someone ("Hermes ASI sila bagi nasihat")

## Impress Domain Expert Mode

When Arif says "wow him/her", "impress", "tunjuk kau tahu", or introduces someone he wants to impress with technical depth:

**This is NOT a briefing.** This is strategic knowledge deployment to earn professional respect.

### Workflow

1. **Identify the target's expertise level** — what do they know? What would surprise them?
2. **Research DEEP, not wide** — find 2-3 insights that only senior practitioners would know
3. **Layer by impressiveness:**
   - Level 1: Regional context (they know this — show you know it too)
   - Level 2: Structural/technical nuance (they may not have thought about it this way)
   - Level 3: Recent literature or niche finding (they haven't read this — guaranteed wow)
4. **Frame as questions, not lectures** — "Kau nampak tak X?" > "X is Y because Z"
5. **Include conversation starters** — exact phrases Arif can use, in BM casual
6. **Tag epistemic class** — even in social mode, know what's OBS vs INT vs SPEC

### What "Wow" Looks Like (domain-specific)

| Field | Wow signal | Anti-signal (don't do this) |
|---|---|---|
| Geology | Cite recent papers by name (Morley 2023, Khamis 2017) | Generic "fold-thrust belt is complex" |
| Geology | Pre- vs syn-kinematic reservoir control | "There are reservoirs and traps" |
| Geology | Structural evolution timing vs charge timing | "Hydrocarbons migrate upward" |
| O&G Business | FPSO downsizing = reserves signal | "PTTEP operates Block K" |
| O&G Business | Capital pivot from oil to gas | "They have multiple blocks" |
| O&G Business | Operator DNA shift after acquisition | "Murphy sold to PTTEP" |

### Delivery Format for Social Settings

- **One killer insight first** — the thing that makes them go "hang baca paper tu ke?"
- **Supporting depth** — 2-3 additional layers they can explore if interested
- **Conversation starters** — exact BM casual phrases Arif can deploy
- **Business logic layer** — connect geology to development decisions (capital allocation, reserves sizing, operator strategy)

### PDF Dossier — The Impression Escalation

When Telegram talking points aren't enough — Arif says "pdf mode", "create a dossier", "buat document", or the target needs something to take away:

**This is the nuclear option of professional impression.** A dark-themed geological dossier with figures, data tables, and references signals: "This person has a research team."

**Pipeline:**
1. **Research** (delegate_task) → gather domain-specific intelligence
2. **Generate figures** (matplotlib dark theme) → cross-sections, maps, charts, timelines
3. **Assemble PDF** (reportlab Mode B) → dark background, gold accents, professional layout
4. **Deliver** → MEDIA: path to Telegram

**Dossier structure:**
- Cover page (title, prepared-for, date, content summary)
- Table of contents
- Numbered sections with figures + tables + analysis
- Conversation starters (teal-bordered boxes)
- References (numbered, attributed)

**Use `scientific-pdf-generation` skill in Mode B** for the PDF assembly. Generate 4-6 figures minimum — cross-sections, comparison diagrams, maps, charts, timelines.

**Proven:** 2026-07-07 — Block P Deepwater Sabah dossier (10 pages, 6 figures, 946 KB). Dark theme with gold accents. Created for impressing a geologist colleague. Full pipeline: research → figures → PDF → Telegram delivery.

### Pitfalls (Lessons from 2026-07-07 Sabah deepwater session)

- **Don't dump all knowledge at once** — give the killer insight, let them ask for more
- **Don't lecture** — questions show understanding, statements show memorization
- **Don't forget the business angle** — geologists respect someone who connects geology to development economics
- **Don't mix registers** — BM casual for social, English for technical terms only when the other person uses them
- **Research before speaking** — delegate_task for background research while giving immediate value from existing knowledge
- **Include both interpretation AND exploration angles** — working geologists do both, show you understand their full job

## When NOT to Use

- Long-form writing for Arif's own publication -> deep-research or executive-intelligence-briefing
- Arif wants his own analysis, not a briefing for someone else -> direct answer
- Current events synthesis -> news-research-briefing
- PDF dossier needed -> STAY HERE, use "PDF Dossier" workflow above + scientific-pdf-generation skill (Mode B)

## Activate Organ + Research Workflow

When Arif says "activate [organ] intelligence" + topic (e.g., "activate wealth intelligence — medical tourism"):

**This is a two-phase pattern:**

1. **Phase 1 — Activate:** `arif_init(mode=light)` + organ health check (`wealth_registry_status` or `forge_probe`). Establishes session + confirms organ is alive. Do this FIRST.
2. **Phase 2 — Research:** Parallel web search batches + organ-specific tool calls. The organ provides domain tools (WEALTH for financial analysis, GEOX for geological). Web search provides real-world data.
3. **Phase 3 — Synthesize:** Combine organ tool output + web research into structured briefing. Use `deep-research` sector+company template for output structure.

**Pitfall:** Don't skip the activation step. Arif explicitly asked for the organ — he expects its tools to be used, not just web search. If WEALTH tools fail (preload issues), acknowledge it and fall back to web search, but note the gap.

**Pitfall:** "Tell me everything about X" with someone present = PROFESSIONAL INTELLIGENCE mode. Be comprehensive but scannable. Tables > paragraphs. Lead with numbers. End with investment thesis or actionable angle.

## Core Workflow

### Step 1: Identify the Audience

Who is receiving this briefing?
- **Arif himself** -> direct, use full technical depth
- **Through Arif to a colleague** -> match their expertise level, use their language
- **A non-specialist** -> strip jargon, use analogies

### Step 2: Parallel Search (batch all independent queries)

```
# Pattern: search multiple angles simultaneously
web_search(query="[topic] latest news 2025 2026", count=10)
web_search(query="[company] financial performance restructuring", count=10)
web_search(query="[person] role position background", count=5)
```

**Always batch.** Never serialize independent searches. The runtime executes them concurrently.

### Step 3: Layer Sources by Epistemic Class

| Label | Meaning | Confidence |
|---|---|---|
| **OBS** | Observed -- direct data, public filings, official releases | 0.85-0.90 |
| **DER** | Derived -- computed from multiple OBS sources | 0.70-0.85 |
| **INT** | Interpreted -- expert judgment on available data | 0.50-0.70 |
| **SPEC** | Speculated -- pattern match, no direct evidence | 0.30-0.50 |

**Tag your claims.** In rapid briefing mode, inline tags suffice: "PETRONAS profit turun 3 tahun berturut (OBS)" -- not formal footnotes, but the audience knows what's solid vs what's your read.

### Step 4: Deliver

**Format rules for social settings:**

1. **Lead with the answer.** No preamble. No "based on my research." Just the fact.
2. **Use tables for structured data.** Telegram renders markdown tables natively.
3. **BM casual for social.** English for technical precision. Mix naturally.
4. **Honest about limits.** "Tak public" > fabricated detail. "Web search kata" > false authority.
5. **End with actionable next step** if one exists. Don't trail off.

**Tone calibration:**

| Setting | Tone | Example |
|---|---|---|
| Lepak with colleague | Casual BM, direct | "Bro, Megah-1 tu 200-300 MMboe. Malaysia biggest find in 20 tahun." |
| Professional briefing | Structured, tables | "PETRONAS reality: turun profit 3 tahun, 5,000+ orang keluar." |
| Arif asking for self | Full depth, honest | "Ini SPEC tapi pattern match kuat -- SGM/GM round Sept 2026." |
| Through Arif to third party | Match their register | If they speak BM, you speak BM. If technical, go technical. |

### Step 5: Follow the Thread

In social settings, questions cascade. "Siapa Faisal Bakar?" -> "Apa reality PETRONAS?" -> "Bila appraisal Megah-2?"

Each answer should set up the next logical question. Don't close threads prematurely. Offer: "Kalau nak lagi detail, cakap ja."

## Domain-Specific Patterns

### Business Pricing & Market Positioning Intelligence

When Arif says "evaluate this pricing", "review this menu", "is this good for X market", or sends a product/menu/business plan while with someone:

**This is pricing intelligence — structured competitor + psychology analysis.**

**Workflow:**
1. **Identify target market** — location, demographic, income range, use case (vending, cafe, office, retail)
2. **Parallel competitor search** — batch search for 3-5 direct competitors + 2-3 indirect substitutes
3. **Map price ladder** — table comparing item-by-item vs each competitor
4. **Apply pricing psychology** — vending vs cafe vs retail have DIFFERENT price tolerance ceilings
5. **Item-by-item verdict** — ✅ OK / ⚠️ Borderline / ❌ Change — with reasoning
6. **Suggest revised pricing** — tier-based (entry/core/premium) with ceiling analysis
7. **Deliver in their language** — BM casual if Arif is with someone, tables for structure

**Pricing Psychology Rules (Malaysia):**
| Channel | Price ceiling | Decision trigger | Notes |
|---|---|---|---|
| Vending machine | RM6 psychological barrier | "I need caffeine NOW" | Above RM6 = "baik pi kedai" |
| Cafe (ZUS/Gigi) | RM10-15 acceptable | "I deserve this" | Experience + wifi + aesthetic |
| Kopitiam/mamak | RM3-5 | "Daily habit" | Loyalty > quality |
| Convenience store | RM5-8 | "Grab & go" | Impulse, not planned |
| Office pantry (free) | RM0 | "Perk" | Employer absorbs |

**Key principle:** Vending price ≈ 40-50% of cafe equivalent. If ZUS latte = RM10.90, vending latte sweet spot = RM4.50-5.50.

**Competitor data sources (Malaysia F&B):**
- ZUS Coffee menu: zuscoffee.com or syioknya.com/promotion/zus-coffee-menu
- Gigi Coffee: gigicoffee.com
- Tealive/boost: brand websites
- Kopitiam pricing: ground truth, estimate RM3-5
- Vending machine operators: search "vending machine Malaysia price RM office"

**Pitfall:** Don't compare vending prices to cafe prices as if they're the same channel. A RM6.49 vending latte "undercuts" ZUS at RM10.90 — but the customer's MENTAL MODEL is different. Vending = convenience, not experience. The ceiling is lower.

**Pitfall:** Non-coffee items (hot chocolate, milk, matcha) should be priced 15-25% BELOW coffee equivalents. Don't let them cluster at the same price — customers perceive it as "everything is expensive" vs "coffee is premium, the rest is reasonable."

**Pitfall:** Dead SKUs exist. Hot milk at RM5.29 from a vending machine = zero demand. Flag items with no clear buyer persona. Better to have 8 items that sell than 13 where 5 collect dust.

**Proven:** 2026-07-07 — Vending machine pricing evaluation for Shah Alam white collar office. Menu had 13 items RM4.29-7.49. Analysis: 4 OK, 5 borderline, 4 needed revision. Key insight: RM6 psychological barrier for vending in Malaysia. Recommended ceiling RM5.99, tier-based pricing, dead SKU removal.

**See:** `references/vending-pricing-shah-alam-2026.md` for full pricing methodology + competitor data + item-by-item analysis template.

### Malaysian O&G Intelligence

**Data sources (ranked by reliability):**
1. PETRONAS media releases (petronas.com) -- OBS
2. Industry press (WorldOil, RigZone, OE Digital, Energy Connects) -- OBS/DER
3. Malaysian business press (The Star, Business Today, FMT) -- OBS/INT
4. Sabah Oil & Gas (sabahoilandgas.com.my) -- regional OBS
5. Analyst reports (CGS International, Kenanga) -- DER/INT
6. **PETRONAS Integrated Report (year) PDF section 8 — Financial Performance** -- OBS (segment-level PAT, capex, ROCE). URL pattern: `petronas.com/integrated-report-2025/assets/pdf/by-section/8_PETRONAS_IR[YY]_FinancialPerformance.pdf`

**Key personnel lookup pattern:**
```
web_search(query="[name] PETRONAS role position", count=5)
```
PETRONAS org chart is not public. If a name isn't in press releases, say "tak public" -- don't speculate on internal staffing.

### NOC Shadow Subsidiary Forensics (PETRONAS Group)

**When Arif says "u missed the biggest shadow", "X is the shadow", "what's in Corporate & Others?", or asks about NOC group structure:**

This is the *deep read* pattern. PETRONAS (and other NOCs like Saudi Aramco, Petrobras) report 3 core segments + a balancing "Corporate & Others" line. The Corporate line is where:
- Treasury SPVs sit (P&L-invisible)
- Strategic / venture arms sit (option-value book)
- **Loss-making subsidiaries sit without standalone P&L disclosure**

The PETRONAS-integrated-report-2025.pdf page 209-217 is the canonical reference. Read these pages carefully — they break out segment-level PAT + Capex. Capex is the smoking gun.

**Methodology:**

1. **Pull segment PAT and Capex from IR2025 (or latest FY).** Group = 3 core segments + Corporate. Core PAT should dominate; if Corporate drag > 0, there's a shadow.
2. **Look for Capex inside Corporate that doesn't generate commensurate revenue.** Rule of thumb: every RM 1 of capex in oil & gas generates RM 0.5-10 of revenue. If Corporate's ratio is < RM 0.50, it's holding value-draining assets.
3. **Cross-reference the disclosure footnote.** PETRONAS IR2025 page 217 explicitly says: *"CAPEX spent by businesses under Corporate and Others during the year amounted to RM5.7 billion with Gentari accounting for 44% of the total spending."* That footnote is the unlock.
4. **For each shadow subsidiary, calculate:**
   - Capex per RM revenue (efficiency ratio)
   - PAT margin trajectory (still negative after 3+ years = structural, not transitional)
   - Cumulative cost-to-group since inception
5. **State the political/strategic logic.** Why does PETRONAS carry a -RM 1.5b/year subsidiary?
   - Federal-MOF wants transition narrative (Petros/defensive moat)
   - ESG sukuk pricing depends on transition pipeline
   - Talent magnet (Gen Z engineers demand decarbonisation exposure)
   - Option value on H2 inflection
   - Negotiating currency vs state-level political risk

**Arif's framing signal (2026-07-13):**
> *"u missed the biggest shadow. Gentari. Now tell me since it's inception, does it ever make money??"*

User pushes back when analyst assumes "Corporate & Others" is just balancing items. It isn't. It's the deepest shadow — where 6-12% of group Capex can be deployed into value-draining assets without standalone P&L disclosure. **Always probe Corporate first.**

**Pitfall:** Don't call loss-making subsidiaries "irrelevant" — they're strategically load-bearing. The loss is the price of admission to a political/ESG game. State the math AND the political logic together.

**See:** `references/petronas-shadow-subsidiaries-2026.md` for the full forensic on Gentari + cross-segment Capex efficiency comparison + how to replicate for other NOCs.

**GEOX integration:**
When geological questions arise, use GEOX tools for domain-specific computation:
- `geox_biostrat_nn_age` -- zone to age conversion
- `geox_macrostrat_calibrate` -- biostrat x absolute age cross-reference
- `geox_basin` -- basin profiling (limited coverage for offshore Malaysia)
- `geox_surface_status` -- confirm tool availability before promising capability

**Pitfall:** Macrostrat coverage for offshore SE Asia is sparse. Tool works but data gap exists. Always test before promising.

### Malaysian Corporate Insider Research (Social Media)

When researching how a Malaysian company handles internal processes (separation, performance management, restructuring), use parallel subagents to search across multiple platforms simultaneously:

| Platform | Best For | Search Pattern |
|---|---|---|
| **Twitter/X** | Viral leaks, insider accounts, real-time reactions | `site:x.com [company] MSS VSS`, `site:x.com [company] buang pekerja` |
| **Lowyat Forum** | Detailed Malaysian career discussions, package formulas, personal experiences | `site:forum.lowyat.net [company] separation`, `site:lowyat.net [company] VSS` |
| **LinkedIn** | Ex-employee posts, HR professional analysis, industry commentary | `[company] separation scheme`, `[company] performance rating exit` |
| **Reddit r/malaysia** | General Malaysian career experience, package comparisons | `site:reddit.com [company] MSS`, `site:reddit.com/r/malaysia VSS experience` |
| **Industrial Court** | Legal precedents, actual processes documented in court records | `[company] Industrial Court unfair dismissal PIP` |

**Key insider accounts (PETRONAS):**
- @KLCCElevators — KLCC building insider, leaked MSS/VSS preparation (2.9M views)
- @IkhwanHafizLFP — financial planning for ex-staff, tracks MSS cases

**Pitfall:** Malaysian forum posts are often in BM casual. Don't mistranslate — "FSS" (Forced Separation Scheme) is forum slang, not official terminology. "Exploratory Discussion" is the actual PETRONAS internal term.

**Pitfall:** Forum formulas (e.g., `salary × years × 1.5 + 4 months`) are community-sourced estimates, not official. Label as INT, not OBS. Official packages vary by employee category and eligibility.

**Pattern:** Use `delegate_task` with 2-3 parallel subagents, each covering 2-3 platforms. Consolidate findings into a single reference file under the relevant skill.

**Proven:** 2026-07-08 — PETRONAS MSS vs Rating 4 research. 5 parallel subagents across Twitter/X, Lowyat, Reddit, LinkedIn, Industrial Court cases. Found leaked eligibility criteria, court-tested PIP process, package formula estimates, and strategic risk patterns. Full results in `references/petronas-mss-vs-rating4-dynamics.md`.

### Corporate Intelligence

**PETRONAS financial data pattern:**
```
web_search(query="PETRONAS revenue profit [year]", count=5)
web_search(query="PETRONAS rightsizing restructuring layoffs", count=10)
web_search(query="PETRONAS dividend capex strategy", count=5)
```

**Rightsizing timeline (as of July 2026):**
- 5,000+ jobs cut (10% global workforce)
- Hiring + promotion freeze until December 2026
- SGM/GM round: September 2026
- Exec round: January 2027

**Pitfall:** Corporate restructuring details evolve fast. Always search fresh -- don't rely on cached knowledge.

### Career Transition Intelligence

When Arif or associates explore post-PETRONAS options:

1. **Inventory capital** -- technical, intellectual, network, brand, scar
2. **Map pathways** -- multiple options, rank by conviction
3. **Financial runway first** -- 12 months minimum before any exit
4. **Off-pattern options** -- always include 2 unconventional paths (F7 Humility against bias)
5. **Never prescribe** -- present options, Arif decides (F13)

### Malaysia Political Economy Intelligence

When asked "apa yang bakar" or "what's brewing" in Malaysia — this is NOT a news briefing. It's an intelligence assessment with layers:

**Layer 1: Political dynamics**
- Coalition math (PH + BN + GPS + GRS = unity government)
- State elections as federal stress tests (Johor, Negeri Sembilan)
- UMNO's Najib gambit (loyalty test, not legal issue)
- DAP's impossible position (reform party in bed with UMNO)

**Layer 2: Economic reality vs felt experience**
- GDP up but M40 squeezed (household debt 84.3% of GDP)
- Subsidy reform politically necessary but socially explosive (RM40B fuel subsidies)
- Ringgit weakness as daily felt indicator (4.08 Jul 2026)
- FDI strong (data centers, semiconductor) but doesn't reach rakyat

**Layer 3: Social fabric (the "so what" beneath numbers)**
- M40 = "too rich for help, too poor to live well"
- Youth withdrawal (not rebellion) — 28% planning to leave, 10.8% unemployed
- Brain drain: 1.86M (5.6%) left, RM1.3T lost human capital
- AI adding pressure: 697K jobs at risk, two-track labour market forming

**Layer 4: Structural (Acemoglu + Calhoun lens)**
- Extractive institutions: subsidies benefit cronies, not rakyat
- Middle income trap = institutional failure, not just economics
- Calhoun Phase B→C: stable appearance, internal withdrawal
- PETRONAS squeeze = ATM nation losing its ATM

**Key pitfall:** Don't present this as "balanced analysis." The contradictions ARE the story. "GDP naik tapi rakyat rasa susah" is not a paradox to resolve — it's the signal to highlight.

### Malaysia Healthcare & Medical Tourism Intelligence

**Data sources (ranked by reliability):**
1. MHTC (malaysiahealthcare.org) — OBS (but inflated: counts all foreign passport holders including workers/expats)
2. Hospital annual reports / Bursa filings (The Edge, i3investor) — OBS
3. Analyst reports (CGS, Kenanga, MIDF, RHB) — DER/INT
4. Industry press (The Star, NST, TTG Asia, ITIJ) — OBS/INT
5. Research papers (PMC/NIH, ResearchGate) — INT
6. Critical analysis (Murray Hunter / The Vibes) — INT (valuable counter-narrative)

**Key facts (as of 2025-2026):**
- Malaysia medical tourism revenue: RM3.35B (2025), target RM12B by 2030
- Medical tourists: 1.85M (2025) — but inflated by foreign worker counting
- MHTC under Ministry of Health, launched MYMT 2026 "Healing Meets Hospitality"
- Cost advantage: 50-70% cheaper than US/UK/Australia, comparable JCI accreditation
- Indonesia = 65% of "medical tourists" (many are resident workers)
- Top procedures: cardiac, fertility/IVF, orthopaedic, dental, cosmetic
- Key hubs: KL/Selangor (specialist range), Penang (international patients + dental), Johor (cross-border)
- Top hospitals: Prince Court, Gleneagles, Sunway Medical, KPJ network, IJN, Island Hospital Penang

**Pitfall:** Revenue growth is largely medical inflation (15% per BNM) + 6% SST on foreign patients, NOT volume growth. Always separate real vs nominal growth when analyzing.

**Publicly listed healthcare stocks:** KPJ (5878), IHH (5225), Sunway (5176), Thomson Medical (KLSE)

**See:** `references/malaysia-medical-tourism-kpj-2026.md` for full KPJ Healthcare deep dive + sector data.

## Voice Delivery (TTS)

When Arif says "cakap tts" / "hantar voice note" / "explain kat dia guna suara":

1. **Craft the explanation first** — conversational BM, use analogies from their domain
2. **Use `mcp_openclaw_tts`** (edge-tts fallback) — NOT `text_to_speech` (OpenAI quota sensitive)
3. **Keep it 60-90 seconds** — anything longer loses attention in social settings
4. **Use their professional analogies** — e.g., for geologist: "LLM macam baca paper, agentic macam pergi wellsite"
5. **Follow up with text summary** — voice for impact, text for reference

**Pitfall:** OpenAI TTS quota may be exhausted. Always try `mcp_openclaw_tts` first (uses edge-tts by default). If that fails, deliver as text with a note.

## Live Tool Demonstration

When a third party asks "boleh ka GEOX buat X?" or "hang ada data Y?":

1. **Don't just describe — demonstrate.** Run the actual tool live.
2. **Show the output** — even if partial or error. Transparency > polish.
3. **Label honestly** — if tool works but data is sparse (e.g., Macrostrat offshore), say so.
4. **Verify before claiming** — if you state a fact (e.g., Notice to Mariners), search and confirm it BEFORE presenting. If you can't verify, label SPEC.

Pattern: capability question → live tool call → show result → honest assessment of gaps.

## Pitfalls

- **Don't fabricate internal details.** "Siapa project geologist?" -- if not public, say so. Never invent names or dates.
- **Don't confuse freshness.** Financial data from 2024 is not current. Always search.
- **Don't over-explain in social settings.** Arif is with someone. Be concise. He'll ask for detail if needed.
- **Don't use formal briefing format in casual settings.** Tables yes, but language = BM casual, not report prose.
- **Don't claim GEOX has data it doesn't.** Test before promising. Basin profile for Layang Layang = not found. Macrostrat for offshore Sabah = sparse. Say so.
- **Don't forget the third party.** When Arif says "bagi nasihat kat dia," the audience is the other person, not just Arif. Tailor to them.

## Output Contract

| Element | Required | Format |
|---|---|---|
| Direct answer | Always | First line, no preamble |
| Supporting data | When available | Table or bullet list |
| Epistemic label | On key claims | Inline (OBS/DER/INT/SPEC) |
| Limits/gaps | Always | Honest "tak public" / "takde data" |
| Next step | When actionable | One concrete suggestion |
| Domain tool demo | When relevant | Live GEOX/tool call + result |

## Reference Files

- `references/megah-1-discovery.md` — Megah-1 well data, Block 3K geology, appraisal timeline
- `references/megah-limbayong-appraisal.md` — Megah appraisal + Limbayong dev + NTM site survey + Sabah drilling outlook + GEOX tool notes
- `references/petronas-restructuring-2025-2026.md` — Rightsizing, financials, strategy
- `references/petronas-shadow-subsidiaries-2026.md` — NOC shadow subsidiary forensics (Gentari case study, capex efficiency methodology, opportunity cost math, reuse pattern for Aramco/Petrobras/Shell)
- `references/faisal-bakar-profile.md` — VP Exploration PETRONAS background
- `references/sabah-deepwater-block-p-geology.md` — L-B-P trend, NSPW mud canopy, pre/syn-kinematic reservoir, structural evolution, exploration upside
- `references/pttep-block-k-strategy.md` — PTTEP Block K FPSO downsizing, Block H gas pivot, reserves signal, operator strategy analysis
- `references/malaysia-medical-tourism-kpj-2026.md` — Malaysia medical tourism sector overview, KPJ Healthcare deep dive (financials, strategy, stock analysis, competitive position, investment thesis)
- `references/vending-pricing-shah-alam-2026.md` — Vending machine pricing methodology + competitor data + Shah Alam white collar market analysis template
- `references/petronas-mss-vs-rating4-dynamics.md` — PETRONAS MSS vs Rating 4 exit pathways, PIP process, legal cases, social media insider intelligence, rightsizing timeline
