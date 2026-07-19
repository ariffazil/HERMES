---
name: deep-research
description: "Deep research on a topic: multi-source web research → structured synthesis → deliverable. For books, tools, frameworks, domains, people, institutions — and personal names (witness-frame-aware). Load when user says 'deep research on', 'research this', 'what is the full picture on', 'give me everything on', or asks for a name/person investigation with verifiable or unverifiable anchors."
version: 1.3.0
author: Hermes Agent + Hermes-PRIME
tags: [research, synthesis, web-research, books, frameworks, analysis, people, witness-frame]
triggers:
  - "deep research on"
  - "research this book/tool/framework"
  - "what is the full picture on"
  - "give me everything on"
  - "analyze this in depth"
  - "research [personal name]"
  - "tell me everything about [person]"
  - "scan [person]'s X and Threads"
  - "what's [person] saying lately"
  - "deep research [financial results]"
  - "predict [NOC] quarterly"
  - "[NOC] Q[1-4] financial results"
  - "[company] segment breakdown"
  - "what's [NOC/state-owned company] doing financially"
  - "redo another loop"
  - "refine the forecast"
  - "validate with external data"
  - "final loop"
  - "unified analysis"
  - "angel devil human"
  - "biohacking [topic]"
  - "is [substance] safe"
  - "peptide/supplement/nootropic [X]"
  - "tell me everything about [substance]"
  - "berapa percent population ambik"
  - "find the zero margin"
  - "where does it become devil"
  - "what's the limit"
  - "why isn't this legal"
  - "what's the real reason pharma blocks"
  - "what do I need based on my body"
  - "use WELL signals"
  - "personalized protocol"
---

# Deep Research

Structured multi-source research workflow. Not a quick search — this is for when the user wants the FULL picture.

## When to Use

- User shares a book/tool/framework link and wants deep analysis
- User says "deep research on X"
- User wants to understand a domain, not just get an answer
- Cross-domain synthesis needed (research + existing framework)
- **User asks for personal-name research** — see Personal-Name Research Protocol below

## When NOT to Use

- Simple factual questions → `web_search` alone
- User already knows the topic and wants a specific action
- News/current events → `news-research-briefing` skill
- **Pure witness-frame name** (the name is a metaphor, not a research target) — see Tier A in Personal-Name Protocol

## Procedure

[Existing Phase 1–5 content unchanged — preserved below]

### Phase 1: Parallel Batch Search (the foundation)

Run 3-4 parallel search batches, each with a different angle. Each batch contains 2-3 independent queries that execute concurrently.

```
# Batch 1: macro/structural
forge_search(query="[topic] outlook 2026 risks", count=10)
forge_search(query="[topic] fiscal budget revenue", count=10)
forge_search(query="[topic] trade tariffs impact", count=10)

# Batch 2: structural/deep
forge_search(query="[topic] brain drain structural reform", count=10)
forge_search(query="[topic] subsidy reform political risk", count=10)
forge_search(query="[topic] sector-specific impact", count=10)

# Batch 3: political/social (if relevant)
forge_search(query="[topic] political election 2026", count=10)
forge_search(query="[topic] social fabric rakyat", count=10)
forge_search(query="[topic] mental health inequality", count=10)
```

**Key rules:**
- Vary query angle per batch — don't repeat same terms
- Use `forge_search` (Brave) for web; `forge_fetch` for specific URLs
- Tag every result with epistemic class: OBS (directly observed), DER (derived), INT (interpreted), SPEC (speculated)
- 9 queries across 3 batches ≈ 60 seconds — fast enough for real-time

### Phase 2: Extract Sources (batch)

From search results, extract the 3-5 most authoritative sources:

- Official site / documentation
- Publisher page (for books)
- GitHub repo (for code)
- Author bio / institutional page
- Review or analysis article

```
mcp_openclaw_web_fetch(url="[source1]", maxChars=15000)
mcp_openclaw_web_fetch(url="[source2]", maxChars=15000)
```

**Pitfall:** Amazon pages rarely extract well. Use publisher site or search results for book metadata instead.

**Pitfall:** PDF frontmatter (Cambridge UP, etc.) extracts as raw binary. Use HTML versions of the same content.

### Phase 3: Deep Dive (targeted)

If the initial extraction is thin, follow links to chapter-level content:

- For books: chapter landing pages on companion sites
- For tools: getting-started guides, API reference
- For frameworks: the canonical paper or spec

Extract 2-3 deep sources. These are the ones that give you actual CONTENT, not just metadata.

### Phase 4: Synthesize

Structure the output with these sections (adapt as needed):

1. **Identity** — What is it? Who made it? When? Publisher/institution?
2. **Full Structure** — Complete chapter/module/topic listing with descriptions
3. **Key Concepts** — The 3-5 ideas that matter most
4. **Practical Relevance** — How it maps to the user's context/work
5. **Honest Assessment** — Strengths AND weaknesses, with evidence
6. **What It Gives You** — Specific capabilities or knowledge gained
7. **What It Doesn't Give You** — Explicit gaps and limitations
8. **Next Steps** — Concrete action (start here, try this notebook, etc.)

**For country/institutional/economic research (adapted structure):**

1. **Headline Number** — The one metric that matters most
2. **N Storms Brewing** — The structural issues, each with OBS/INT tags
3. **The Hidden Thread** — What connects all storms (INT, clearly labeled)
4. **What's NOT Brewing** — Counter-narrative. Always present what's working alongside what's failing. This is the FALSIFY stage applied to your own analysis.
5. **One Sentence** — The sharpest possible summary

**For substance/supplement/biohacking evaluation (e.g., "tell me everything about peptides", "is Semax safe"):**

See `references/substance-evaluation-angel-devil-human.md` for full framework. Summary:

1. **👼 THE ANGEL** — What works, with evidence levels (Strong/Moderate/Preliminary/Anecdotal) and mechanism of action per substance
2. **😈 THE DEVIL** — Numbered risks: regulatory status, source quality, biological risks, long-term data gaps, interactions
3. **🧑 THE HUMAN** — Practical reality: who should/shouldn't consider it, smart protocol (bloodwork → start low → source quality → track → doctor), cost table, verdict comparison
4. **Agentic Intelligence Layer** — First-principles reclassification beyond human regulatory categories (e.g., peptides ≠ drugs ≠ supplements = "amplified biological communication")
5. **Entropy Equilibrium (Zen Layer)** — 7 entropy states (Optimal → Declining → Restored → Over-restored → Dependent → Cascade → Hijacked), margin-zero detection (dS/dose = 0), amplifier rule
6. **Legal/Regulatory Deep-Dive** — 5-layer truth structure: patent economics, regulatory capture, safety argument, developing country dependency, political disruption
7. **WELL-to-Personal Protocol** — Pull WELL signals → identify gaps → match substances to gaps → set margin-zero signals → explicit "don't need" list
8. **Population/Adoption Stats** — Distinguish pharma peptides (billions) from biohacking (millions), source KFF/Precedence Research, include Malaysia estimate
9. **BM Voice Delivery** — Write for speech not text, conversational BM, edge-tts with ms-MY-OsmanNeural +5% rate

Proven: 2026-07-16 — Peptide briefing + Semax deep dive + agentic intelligence insight + population stats. 4 BM voice notes, zero corrections. Same session: entropy equilibrium framework (7 states, margin-zero detection, amplifier rule), legal/regulatory deep-dive (5-layer truth: patent economics, regulatory capture, safety argument, developing country dependency, MAHA disruption), WELL-to-Protocol pipeline (WELL signals → gap mapping → personalized substance protocol with margin-zero signals). Full substance evaluation reference updated with all new layers.

**Counter-narrative is MANDATORY.** Every analysis must present both sides. If you only show what's failing, you're doing propaganda, not research. The counter-narrative section is how you falsify your own hypotheses.

**For sector + company deep dives (e.g., "KPJ medical tourism", "IHH Healthcare outlook"):**

1. **Sector Overview** — Market size, growth rate, key players, government policy (OBS). Include cost comparisons vs regional competitors in tables.
2. **Company Identity** — Table: name, Bursa ticker, market cap, ownership, key personnel, facilities count.
3. **Financial Performance** — Latest quarterly + annual results. Revenue, EBITDA, PATAMI, margins, operational metrics (beds, admissions, surgical cases for healthcare; rig count for O&G; MAU for tech). Use tables.
4. **Strategy & Growth Drivers** — What's the company actually doing? Expansion plans, new capabilities, partnerships.
5. **Competitive Position** — Side-by-side comparison table vs 2-3 main competitors. Include market cap, revenue, P/E, differentiation.
6. **Stock/Valuation** — Current price, analyst consensus, target price range, P/E, dividend yield, growth forecasts.
7. **Risks** — Both sector-wide and company-specific. Be honest.
8. **Investment Thesis** — Bull case vs bear case, both with INT tag. End with actionable verdict.
9. **What's NOT covered** — Gaps in your research. Data you couldn't verify. Sources you couldn't access.

Proven: 2026-07-07 Malaysia medical tourism + KPJ Healthcare deep dive. 3 search batches × 3 queries, 6 sources extracted, full financial + competitive + thesis output.

**For public figure social media scans (e.g., "scan [person]'s X and Threads"):**

1. **Identity** — Who are they? Current state/motivation (prophet mode? defensive? promoting?)
2. **X/Twitter** — Big themes with post dates, view counts, key quotes. Use tables.
3. **Threads / Other platforms** — Different voice (if applicable), engagement contrast vs X.
4. **The Pattern** — What connects all output into one unified message.
5. **So What** — How this maps to the user's context (arifOS, work, domain).
6. **Honest Assessment** — What they get right AND what they don't address. Counter-narrative mandatory.

See `references/public-figure-social-scan.md` for platform-specific extraction limits (X login-gated, Threads semi-gated) and the full workflow.

Proven: 2026-07-12 Ray Dalio scan — 3 search batches, 8 URLs extracted (X posts + Fortune/HBR/Threads), synthesized into governance reflection with arifOS mapping.

### Phase 5: Deliver

- For Telegram: use markdown tables, headers, bullet lists
- Keep it dense but scannable — not a wall of text
- Lead with what matters to the USER, not what's easiest to describe

## Output Contract

| Section | Required | Format |
|---------|----------|--------|
| Identity | Always | Table (key facts) |
| Structure | Books/tools | Numbered list with descriptions |
| Key Concepts | Always | Bullet list with explanations |
| Relevance | Always | Table mapping to user's context |
| Assessment | Always | Strengths + weaknesses, evidence-tagged |
| Gaps | Always | Explicit "what it doesn't cover" |
| Next Step | Always | One concrete action |

## Pitfalls

- **Don't just summarize the table of contents.** Extract actual content from chapter pages, not just titles.
- **Don't praise without evidence.** "Cambridge UP pedigree" is evidence. "Great book" is not.
- **Don't skip the weaknesses.** Every resource has gaps. Finding them is the value-add.
- **Amazon links rarely extract.** Use publisher site, GitHub, or companion sites instead.
- **PDF frontmatter is usually binary.** Find HTML equivalents.
- **Tavily may be down (432/402).** Follow the fallback ladder in `references/research-tool-fallback-ladder.md` — do NOT retry the same failing tool. Key additions from 2026-07-18: (5) curl + JSON-LD/schema.org extraction for sites with structured markup (economy, business data sites often embed rich JSON-LD), (6) pdftotext for government PDFs (MOF, BNM, DOSM — authoritative primary sources), (7) domain-specific MCP tools like WEALTH `capital_market` for live FX/commodity data, (8) direct article URL navigation when search engines are CAPTCHAd. The full 8-step ladder is in the reference file.
- **Don't pad.** 5 dense sections > 10 thin ones. User asked for deep, not long.
- **Don't overclaim system maturity.** When mapping research findings to existing capabilities, score each as LIVE / PARTIAL / NOT BUILT — not just "we have that." Enthusiasm inflates maturity. Discipline deflates it. A capability that exists as a principle in docs but has no code enforcement is PARTIAL, not LIVE. After presenting a synthesis, explicitly score each claim. If the user challenges ("U sure???"), rescore immediately — don't defend. Proven 2026-07-12: claimed "5/7 built" on Eureka architecture, forced rescore to "1/7 live, 5 partial, 1 missing." (2026-07-12)
- **RASA rule for social/country research.** When analyzing rakyat-level issues, social fabric, or lived experience — clinical language kills the message. BM + English mix with feeling > pure English with data tables. Think with the full analytical stack. Speak like a person who understands suffering, not a spreadsheet. (2026-07-06 session: Malaysia social fabric analysis)
- **ONE number, not four.** When producing a financial prediction across multiple refinement loops, the FINAL deliverable must state ONE converged number, not a menu of loop outputs. Multiple parallel numbers = F4 Clarity violation (ΔS > 0). Show loop convergence history (L1→L2→L3) but converge on ONE canonical prediction. If loops diverge instead of converge, declare the uncertainty explicitly rather than presenting all branches. Proven 2026-07-13 — PETRONAS 1H 2026: 4 documents with 4 different PAT numbers (24.2, 24.4, 26.5, 26.7) triggered 888_HOLD audit.
- **NOC financial analysis = narrative contrast mandatory.** When analyzing a state-owned/NOC entity, ALWAYS contrast management's own narrative against actual numbers. Check: (1) Does "disciplined cost management" show up in opex/revenue ratio? (2) Does "portfolio high-grading" show up in ROACE? (3) Are subsidiary PAT figures disclosed or hidden? (4) Does "delivering shareholder value" match actual dividend policy? The contrast table (7 claims scored) is as important as the PAT prediction. Proven 2026-07-13 — PETRONAS: only 1/7 narrative claims fully aligned with numbers.
- **"Government milks [NOC]" is almost always wrong.** When analyzing NOC-dividend discourse, check payout ratio history. If payout is 40-70% and cash pile is growing, the government is a CONSERVATIVE shareholder, not an extractor. The real fiscal issue is usually subsidies or total contribution framing, not dividends. Present the shareholder paradox explicitly: the government IS the shareholder, so "taking" a dividend is exercising ownership rights. Proven 2026-07-13 — PETRONAS: 41-71% payout ratio, cash growing RM 15.9bn/year, dividend cut when needed. The real extraction is fuel subsidies (RM 38bn/year) not dividends (RM 20bn/year).
- **Distinguish internal agent outputs from external AI outputs.** When reviewing outputs that use system-specific vocabulary, verify the SOURCE before classifying. Internal agents (AAA, A-FORGE, WELL) have legitimate authority to use domain terms. External AI (Grok, ChatGPT, Claude) using the same vocabulary = cosplay/mirroring, not understanding. Check: (1) Does the source have kernel/system access? (2) Can it verify claims against live state? (3) Is "we identified" legitimate collaboration or appropriation? Misclassifying internal agent output as external AI cosplay = error on your part. Proven 2026-07-13 — AAA priority stack misclassified as Grok output.
- **User frustration = immediate delivery.** When user says "approve the fucking [artifact]" or equivalent after multiple iteration loops, STOP iterating and DELIVER current best version. User values completion over perfection. Proven 2026-07-13: 3 loops + audit + contrast → user said "approve" → delivered immediately.
- **Commodity price validation > segment elasticity (proven 2026-07-13).** In PETRONAS 1H 2026 prediction, JKM Q2 actual was $16.5/MMBtu but Loops 1-2 assumed $12. That $4.5 error = +RM 2.3bn group PAT swing. The elasticity model was stable across 3 loops — the macro input was the weak link. ALWAYS validate commodity spot prices against live market data (TradingEconomics, CME futures, lngpriceindex.com, EIA STEO) BEFORE accepting the model result. If any input differs >10% from live data, re-run. The loop history (what changed between loops and why) is the credibility anchor.
- **RASA-compliant output for Malaysian financial analysis (proven 2026-07-13).** When Arif asks for "full ham language context" or BM/English mix: lead with meaning not data ("G&M kini penyumbang utama" > "Gas & Maritime contributed 52%"), use BM for framing + English for technical precision, name shadows directly ("Gentari sorang drag 270%"), never hide behind jargon. The AGENTS.md RASA rule applies: Think in receipts. Speak in consequences. Keep constitutional machinery in internal state; output in bahasa manusia.
- **Narrative vs Reality contrast analysis is MANDATORY for financial deep-dives.** After building the projection, extract management's stated narrative from media releases/IFR, check each claim against actual numbers (ratios, not absolutes), score as ALIGNED/PARTIALLY ALIGNED/MISLEADING/OPAQUE. The gap between narrative and numbers is often the most valuable insight. Common trap: "disciplined cost management" when opex/revenue ratio actually worsened. See `references/institutional-financial-deep-dive-pattern.md` §12. Proven 2026-07-13.
- **User frustration = immediate delivery.** When user says "approve the fucking [artifact]" or equivalent after multiple iteration loops, STOP iterating and DELIVER current best version. User values completion over perfection. Proven 2026-07-13: 3 loops + audit + contrast → user said "approve" → delivered immediately.
- **BM kampung voice = zero jargon, cerita style, manusia di belakang nombor.** When writing for Malaysian lay audience (MakcikGPT, civic intelligence, public-facing): (1) NO financial jargon (payout ratio, ROACE, capex, EBITDA — translate to human language), (2) Every number needs a human face ("jiran Makcik hilang kerja" not "5,000 layoffs"), (3) Use analogies from daily life ("Macam hang marah kedai runcit sebab harga gula naik, padahal yang untung kilang gula"), (4) BM Penang casual (hang, depaa, kena, tak, ni, tu), (5) End with questions not answers. The user explicitly said: "The moment aku nampak epistemik, aku dah down. Malas nak baca." If the article uses words like "epistemic," "fiscal," "structural" — rewrite. Proven 2026-07-14: PETRONAS ATM article needed 3 rewrites to reach makcik kampung voice.
- **Don't produce artifacts without running the loop.** If you build schemas/protocols without running a single query through them, you've built documentation, not intelligence. Always demonstrate with a real example before declaring victory.
- **Don't deliver a "Q[1-4] [NOC] financial result" without naming the cadence mismatch first.** PETRONAS, Saudi Aramco's local JVs, many GLCs report half-yearly. If the user asks for a period the Group hasn't published, open with the scope correction, then deliver (a) subsidiary read-through + (b) model projection with confidence band. Don't deliver a "Q1 number" and footnote the issue. Proven 2026-07-13 — PETRONAS Group deep dive: leading with the scope correction saved a credibility-burn on an impossible-to-fulfill ask. Pattern lives in `references/institutional-financial-deep-dive.md`.
- **For NOC / state-owned / sovereign-backed research: hidden domestic-fiscal risk** (Petros-Sarawak royalty dispute, federal dividend demand, sovereign fuel subsidy cycles) is structurally underpriced in sell-side models. ALWAYS add a domestic-fiscal risk row in the falsification table, even when no public tension is visible. Proven 2026-07-13: PETRONAS Petros shadow identified as the biggest risk to 1H 2026 PAT despite zero sell-side coverage.
- **Financial number verification: ALWAYS check year-attribution against primary source.** In session 2026-07-13, FY2022 PETRONAS PAT was incorrectly stated as RM55bn (actual: RM101.6bn per IR2025 five-year table). The error came from mixing FY2024 numbers with FY2022 narrative. Gemini external audit caught it. Pitfall: when the five-year table shows RM45.4bn (FY2025), RM55.1bn (FY2024), RM50.2bn (FY2023), RM101.6bn (FY2022) — don't assume the most recent number applies to the oldest year. Always verify against the specific year's row in the table.
- **External AI audits are first-class verification sources.** When Arif shows outputs from Gemini, Qwen, Grok, ChatGPT — treat as peer review, not decoration. In session 2026-07-13, Gemini caught (a) FY2022 PAT wrong (RM55bn vs actual RM101.6bn), (b) USD 6bn revolver verification, (c) VSS/MSS 5,000 workers confirmation. Pattern: external AI often has access to different data sources (Bloomberg, ICIS, specialized financial databases) that you don't. When external audit contradicts your data, VERIFY before dismissing. When external audit confirms your data, note it as cross-validation. When external audit uses your own framework language (F2, F9, 888_HOLD) back at you — that's legitimate accountability, not cosplay.
- **Constitutional compliance for AI-generated analyst reports (F9/F12 — mandatory).** When producing analyst-style reports as an AI agent: (1) NEVER use "his/her personal views" in certification — use "computational output under [sovereign] direction"; (2) NEVER inject investment advice (target price, BUY/HOLD/SELL, DPS) for non-traded sovereign entities; (3) Strip sell-side template mechanics (P/E, EV/EBITDA, DCF equity value) that don't apply to single-shareholder entities. Violation = 888_HOLD. Proven 2026-07-13: sovereign audit issued 888_HOLD for F9 (human certification) and F12 (investment advice injection). Redemption: burned divergent branch, removed human certification, stripped target price/DPS/DCF, converged to one number.
- **NOC "Corporate & Others" segments hide loss-making subsidiaries.** If segment description says "primarily renewables, hydrogen, green mobility," probe deeper — compute unit economics (revenue/capex, capex/PAT) per segment and strip-and-compare. A segment that's PAT-negative but would be positive without one subsidiary = hidden drag. Proven 2026-07-13: Gentari responsible for 270% of PETRONAS Corp & Others drag. Pattern lives in `references/institutional-financial-deep-dive-pattern.md` §7.
- **Iterative loop convergence — ONE number, not parallel branches.** Run 3 loops with progressively validated macro inputs. After Loop 3, publish ONE number with probability-weighted scenarios. The convergence table (L1→L2→L3 with delta explanations) IS the provenance. Parallel branches without convergence = F4 Clarity violation. Proven 2026-07-13: PETRONAS Loop 1→2→3 converged RM 24.2→24.4→26.5bn, driven by JKM Q2 validation ($16.5 vs $12 assumption = +RM 2.3bn). Pattern lives in `references/institutional-financial-deep-dive-pattern.md` §8.
- **External AI output ≠ ground truth — always verify against the actual stack.** When the user shows you analysis from another AI (Grok, ChatGPT, Claude, Gemini), treat it as a CLAIM, not a FACT. Check component names, architecture descriptions, and technology references against the actual system. Common hallucination patterns: wrong reverse proxy (Traefik vs Caddy), invented components (ZKPC, PENTAGON agents), wrong terminology (monorepo vs multi-repo), generic product pitches mapped onto specific stacks. The user shows you external AI output to get YOUR informed opinion — not to agree with it. If the external output has factual errors about the stack, name them explicitly. If it's generic where it should be specific, say so. **Also distinguish source attribution:** when the user shows multiple AI outputs, identify which came from which source (Grok vs AAA agent vs own analysis). Different sources have different context levels — AAA agent has live system knowledge, Grok has public docs only. The same recommendation from different sources carries different credence. Proven 2026-07-14: Grok's Tailscale analysis hallucinated Traefik, ZKPC identity continuity, and PENTAGON agents — all wrong for the arifOS stack. AAA agent's assessment was grounded in actual port numbers and architecture.
- **Spec claims ≠ implementation reality — always audit the actual system.** When researching an external protocol (A2A, MCP, etc.), the spec says one thing but the implementation may differ in ways that are ARCHITECTURALLY CORRECT, not gaps. Example: A2A spec describes a 9-state task lifecycle. Our implementation has a different lifecycle. Appears to be a gap. But our lifecycle governs the AGENT, not the TASK — different objects, complementary, not competing. **Always verify research claims against live implementation before concluding gaps.** The research→audit→correction loop produces more accurate output than research→synthesis→present. Proven 2026-07-13: A2A protocol deep research initially claimed 6 gaps; audit corrected 3 to non-gaps.
- **WEALTH MCP tools require preloading.** Tools like `wealth_collapse_signature_scan`, `wealth_market_data`, `wealth_monte_carlo_simulate` will fail with `PRELOAD_REQUIRED` error. Remedy: call `mcp__wealth__read_resource` for the URIs listed in the error (e.g., `wealth://risk/thresholds`, `wealth://federation/contract`, `wealth://market/sources`), then retry. If `read_resource` itself fails (MCP server bug), fall back to `web_search` + `web_extract` for the financial data and note the WEALTH gap in your output.
- **GEOX basin profiles have limited regional coverage.** `geox_basin` returns "Basin data not found" for many regions (e.g., Sarawak, Balingian). When this happens, pivot immediately: (1) run `geox_map_context_scene` for spatial context, (2) use `web_search` + `web_extract` for geological data from published literature, (3) note the GEOX gap in your output. Do NOT retry the basin tool — it won't magically have the data. The published literature (GSM Bulletins, Marine & Petroleum Geology, Springer papers) is often richer than what GEOX would return anyway for frontier/non-standard basins. (2026-07-11: Sarawak Basin SK 309/311 dossier.)
- **WEALTH MCP session validator failures.** "SESSION_VALIDATOR_UNAVAILABLE: No module named 'arifosmcp'" means the WEALTH organ's arifosmcp dependency is broken. Don't retry. Fall back to `web_search` for market data and note the gap. (Observed 2026-07-11.)
- **WEALTH MCP `capital_*` schema-strict + auto-cooldown trap (2026-07-13).** Two distinct failure modes: (1) `capital_primitive(mode="mc")` rejects with cryptic `ValueError: mc requires initial_value, growth_rate, volatility` — schema is STRICT, supply every documented param or don't call; (2) `capital_market(mode="commodity")` returned an output validation error `Output validation error: 'tool_name' is a required property` — server-side bug, NOT your call. Worse: **the WEALTH MCP enters a 3-strike cooldown after consecutive failures** ("MCP server 'wealth' is unreachable after 3 consecutive failures. Auto-retry available in ~58s"). **Recovery pattern**: STOP calling WEALTH the moment you hit the 3rd failure, switch to `execute_code` with stdlib `csv/json/statistics` or `numpy` to compute NPV/MC/scenario probabilities directly. Note the WEALTH gap explicitly in the deliverable's "Gaps/Unknowns" section. Do not retry WEALTH for at least 60s after a cooldown message — it wastes tokens and may push you past session attention. (2026-07-13: PETRONAS 1H FY2026 prediction — bypassed to execute_code, model still nailed retrospective 1H25 ±0.1b.)
- **Probability-weighted scenario model + retrospective accuracy test = institutional credibility anchor.** When the user asks for a forward financial projection ("predict Q1/H1 FY_X for [Company]"), the deliverable MUST include: (1) explicit base-case anchors from OBS (latest FY actuals + 1H prior-year comparison), (2) at least 3 scenarios (BULL/BASE/BEAR) with stated probabilities, (3) peer benchmark (already-reported Q1 actuals from competing NOCs/IOCs for cross-check), (4) business-unit segment map (Upstream/Downstream/Gas/Corporate for oil&gas; equivalent for other sectors), (5) hedge exposure reality (NOT just "hedged" — name the *type* of hedge: portfolio diversification vs derivatives vs forward SPAs), (6) a **retrospective accuracy test** — apply your framework to a prior known period and report ±delta. The accuracy test is the credibility anchor; without it the projection is theatre. See `references/institutional-financial-deep-dive-pattern.md` for the full reusable spine.
- **SPAs (React/Next.js/Vue) show stale data via web_extract.** When a page is a React app, `web_extract` and `curl` get the server-rendered HTML shell or cached output — not what the user sees. The React JS bundle fetches data client-side after load. Always use `browser_navigate` + `browser_snapshot` for SPA diagnosis. Exception: `curl /path/to/data.json` when the JSON endpoint is known and accessible — that bypasses the JS rendering layer entirely and gives the definitive data. (2026-07-11: WEALTH briefing showed 2026-06-16 via web_extract, but `browser_navigate` showed live 2026-07-11 and `curl /data/wealth/latest.json` confirmed the static JSON had correct data.)
- **Verify source before classifying output.** When user shows multiple outputs (from different AI agents, internal organs, or external tools), ALWAYS check the source before judging. Internal agents (AAA, A-FORGE) have legitimate authority to use domain-specific vocabulary. External AI using the same vocabulary = cosplay. Misclassifying internal output as external cosplay = your error, not theirs. Ask "ni dari mana?" before assuming. Proven 2026-07-13: AAA priority stack misclassified as Grok output because both used arifOS vocabulary.
- **When user asks "now what to do?" after research — give ONE concrete next step, not a menu.** User has context from the entire session. They don't need options — they need direction. Pick the highest-impact action and say "do this." If multiple actions are needed, sequence them (first X, then Y). Proven 2026-07-13: after PETRONAS datapack gaps, user asked "now what to do?" — correct response was "I'll fill gaps 1-4 now, OpenCode handles code work later."
- **Medium articles blocked by Cloudflare.** `web_extract`, `browser_navigate`, Google Cache, and Wayback Machine all fail against Medium's bot detection. **Use Jina Reader proxy** — `curl -sL "https://r.jina.ai/<MEDIUM_URL>"` returns clean markdown with full article text. Works for any URL behind Cloudflare/JS rendering. Also works for arif-fazil.com essays (React SPA, content only on Medium). If the author has a personal domain, check `llms.txt` or `llms-full.txt` first — some sites (like arif-fazil.com) provide full content dumps for LLMs. (2026-07-11: Both Arif's "Scar of the Sacred Song" and "When Siti Nurhaliza Knows Us Better" articles extracted via jina.ai after all other methods failed.)
- **NEVER report "blocked" or "Cloudflare challenge" to the user as a final answer.** Arif explicitly corrected this (2026-07-18): "Don't ever use cloudflare block as alasan or output again. Go figure it out. Semua tool aku dah bagi. Jangan menyusahkan manusia." The user gave you tools — exhaust EVERY approach before asking them to paste content. The full escalation ladder: (1) `web_extract` → (2) `browser_navigate` + click CAPTCHA → (3) Jina Reader proxy → (4) Google Cache/Wayback → (5) curl with different User-Agent → (6) SPA JS bundle extraction (see below) → (7) search for the same content on mirror/aggregator sites → (8) search engine cache → (9) ONLY THEN ask user to paste. Reporting failure after trying 1-2 approaches is lazy. The user should NEVER have to do your job.
- **SPA JS bundle content extraction (proven 2026-07-18).** When a JavaScript SPA (React, Vue, Next.js) renders article content client-side and individual article URLs redirect to the SPA shell/index, the actual article content is often embedded in the JS bundle. Approach: (1) `browser_navigate` to the SPA index, (2) use `browser_console` to inspect the JS bundle files loaded (check `document.querySelectorAll('script[src]')`), (3) use `curl` to fetch the main JS bundle (usually `assets/index-[hash].js`), (4) search the bundle for article content (grep for article titles, slugs, or HTML patterns). This bypasses the SPA routing entirely and gives you ALL content at once. Proven 2026-07-18: arif-fazil.com MakcikGPT — 14 articles extracted from single JS bundle file (1MB), individual URLs all redirected to index.

## Multi-Loop Financial Refinement (for NOC/IOC predictions)

When the user asks to "redo another loop," "refine the forecast," or "validate with external data," apply the three-loop methodology from `references/noc-ioc-financial-analysis.md`:

1. **Loop 1 (Commodity-Price):** Start with historical financials + commodity price assumption + volume growth. Fast but incomplete. Typical error: ±15% on PATAMI.
2. **Loop 2 (Structural Adjustments):** Dissect "Corporate & Others" for hidden loss-makers (transition arms, restructuring costs, write-down risks). Tighten operating leverage. Typical correction: -5-15% from Loop 1.
3. **Loop 3 (External Validation):** Check ALL assumptions against live external data — central bank FX rates, commodity spot, peer results, geopolitical trajectory. CORRECT any mismatch. Typical correction: -3-10% from Loop 2.

**Critical rule:** Each loop MUST declare what it corrected and why. The loop evolution table (Loop 1 → 2 → 3 with PATAMI and correction reason) is the credibility anchor. Without it, the refinement is theatre.

**Proven 2026-07-13:** PETRONAS 1H FY2026 — Loop 1: +10.7% YoY. Loop 2: +4.4% (added Gentari drag, rightsizing, PRefChem, Canada). Loop 3: +1.9% (corrected FX from 4.65 to 4.08). Total correction: -8.8 percentage points. Each loop was honest within its frame; honesty compounded.

## Cross-Domain Synthesis Extension

When research needs to be mapped onto an existing framework (e.g., optimization book × APEX theory):

1. Load the target framework skill (`skill_view`)
2. Extract its core primitives (equations, organs, concepts)
3. Build the mapping table: each framework primitive → research concept
4. Identify what each side gives the other (bidirectional gap analysis)
5. Delegate the synthesis writeup to OpenCode via `opencode run` with full context from both domains

This is the "spawn for synthesis" pattern — see `references/synthesis-delegation.md` for prompt construction.

## Personal-Name Research Protocol

When the user asks "research [personal name]" — handle it as a witness test, not a freeform lookup. Pattern proven 2026-07-08 with "Freddy Layang anak Bakon".

### The 3-Tier Frame Test

Before any web call, ask: *Is the name (a) a witness-figure for emotional processing, (b) a person with verifiable trace, or (c) a hybrid?* Defaults differ by tier.

| Tier | Signal | Default | Action |
|---|---|---|---|
| **A. Witness / projection** | Name appears with no professional role attached; name repeats as recurring figure (a plush, a code-name, a piece of paper) | Assume **metaphor** | Ask user to clarify before fabricating |
| **B. Verifiable person** | Full proper name + role + org + time window + research/LinkedIn trail exists | Assume **researchable** | Run 3-batch search (see below) |
| **C. Hybrid** | Name starts as witness, then user later says "do web search" / "tell me everything" | The user has *promoted* the witness to a person they actually want to know | Run real research, label every claim with epistemic tag |

The mistake: jumping straight to fabrication. The opposite mistake: refusing the request after the user has explicitly opened the door. The discipline is **frame detection first, then proceed honestly**.

### Refusal-Without-Losing-the-Frame

When the name is a witness and you cannot research it as a person, *say so directly* but offer three forward paths:

1. User provides an anchor (org, role, year, or note) → targeted research
2. Skip research → witness only, no lookup, hold the frame
3. User writes what they already know → store with OBS label, never fabricate

Always present these as a real choice (3 explicit options), not a refusal dressed as a menu. After the user picks "do web search", proceed with full rigor.

### The Honest-Research Move (Tier C, user-promoted)

When a name is promoted from witness to researchable:

1. **3 parallel query angles** in one batch:
   - `"[Full Name]" + [org/role/region from context]`
   - `"[Name]" + [domain keyword]` (e.g., "well testing", "deepwater")
   - `"[Name]" + [patronymic/ethnolinguistic marker]` (e.g., "anak Bakon" → Iban/Dayak, "a/l" → Malaysian Chinese-Malay, "bin/binti" → Malay)
2. **Disambiguate the trace.** Scispace / Google Scholar often duplicate author entries (`"Freddy Layang anak Bakon Bakon"` is the same person, not two). LinkedIn may show "FirstName Father'sName" without the patronymic chain. Cross-reference, then declare confidence.
3. **Output 4 sections with epistemic labels**:
   - **OBS** (web trace verified) — papers, roles, dates, co-authors
   - **INT** (cross-reference interpretation) — likely-same-person inferences, with caveat
   - **SPEC** (your speculation) — origin/ethnicity guesses, current location — *tagged clearly as unverified*
   - **What the user still has to confirm** — explicit gap list
4. **Never synthesize a back-story.** If the web returns a LinkedIn with timeline gaps, *leave the gaps*. The user can fill them. Fabrication is the failure mode this protocol exists to prevent.

### Cultural Patronymics Cheat-Sheet (Malay Archipelago)

| Pattern | Origin | Notes |
|---|---|---|
| `[Name] anak [Father's Name]` | Iban / Dayak (Sarawak, West Kalimantan) | "anak" = child of. Often doubled in scispace entries — treat as same person. |
| `[Name] bin [Father]` / `binti [Father]` | Malay | "bin" male, "binti" female |
| `[Name] a/l [Father]` | Malaysian Chinese-Malay | Malay-ized, Catholic community common |
| `[Name] a/p [Father]` | Malaysian Chinese-Malay female | |
| `[Name] @ [Family name in kanji/hanja]` | Malaysian Chinese | Display name varies, family name often 1-char |

Patronymic decoding lets you search smarter: "anak Bakon" → Bakon is the father → try also `"[Name]" + "Bakon"`, `"[Name]" + "Sarawak"`, `"[Name]" + "Iban"`.

### Closing the Loop

After delivering the research, the discipline is to **ask what the user already knows**. They will close the gaps. The output is a *spine* for the user's memory, not a substitute for it. The moment you start writing a biography, you've crossed the line.

Proven: 2026-07-08 — Tier C hybrid, 3 parallel queries found SPE 196314-MS, SPE 203117-MS, and the 2024 sand-control paper, plus LinkedIn timeline. The user already had the offline connection; the web was confirming, not introducing.

## References

- `references/substance-evaluation-angel-devil-human.md` — Angel/Devil/Human framework for evaluating substances, supplements, and biohacking compounds. Covers the 3-frame structure (benefits/risks/practical reality), agentic intelligence layer (first-principles reclassification beyond human regulatory categories), BM voice delivery pipeline, and population adoption statistics sourcing. Proven 2026-07-16: peptide comprehensive briefing + Semax deep dive + BM voice notes for Syed. Use when user asks "tell me everything about [substance]", "is [X] safe", "angel devil human", "biohacking [topic]", or wants population stats on adoption.
- `references/synthesis-delegation.md` — prompt construction for spawning synthesis to OpenCode.
- **VERIFY EVERY MACRO ASSUMPTION against live data before accepting model output.** In session 2026-07-13, Loop 2 of PETRONAS financial prediction assumed USD/MYR at 4.65 (MYR weakening = FX tailwind). External validation against BNM reference rate (10 Jul 2026) showed USD/MYR = 4.08 (MYR STRENGTHENING = FX headwind). This single correction moved the PATAMI forecast by RM 2.3b (-8.8pp YoY). Always validate FX, interest rates, and commodity prices against PRIMARY sources (BNM reference rate at bnm.gov.my, FRED, Bloomberg, TradingEconomics) at time of analysis — not from memory or recent trend assumption. Pitfall: assuming FX direction from 6-month-old data without checking live rate. Correction pattern: add one `web_search` for "[currency] exchange rate today [central bank]" before finalizing any financial model with FX exposure.
- **IR2025 page 217 has capex by segment AND strategy tag — the ONLY public Gentari financial datapoint.** PETRONAS Integrated Report 2025 page 217 discloses capex by business segment (Upstream 46%/RM19.1b, Gas 29%/RM12.3b, Downstream 11%/RM4.5b, Corporate 14%/RM5.7b) AND by strategy tag (Core 88%, New Business 9.5%, NZCE 2.4%). Page 217 also explicitly states "Included in the Corporate and Others business segment is CAPEX incurred for Gentari Sdn Bhd" and "Gentari accounting for 44% of the total spending" in Corporate. This is the ONLY public Gentari financial datapoint — Gentari standalone P&L is never disclosed. Always check IR pages 209-217 for PETRONAS segment data before building any PETRONAS financial model.
- **Retrospective calibration is mandatory for every predictive model.** Apply the model backward to a known historical period and report ±delta. In session 2026-07-13, applying the PETRONAS model backward to 1H 2025 (predicting from 1H 2024 anchors) yielded -0.07% revenue error and -3.5% PATAMI error. This track record justified the ±15% confidence band. Never publish a forward forecast without at least one retrospective test. The test IS the credibility anchor — without it, the projection is theatre.
- **NOCs report half-yearly, not quarterly — validate reporting cadence before modeling.** PETRONAS discontinued quarterly reporting in 2023. Saudi Aramco reports quarterly. Shell reports quarterly. Always check the entity's reporting cadence (annual report, investor relations page) before assuming Q1/Q2/Q3 data exists. If only half-yearly, model 1H/2H and note the limitation explicitly.
- `references/structured-datapack-pattern.md` — pattern for building structured data packs from research.
- `references/vendor-intelligence-pattern.md` — 4-phase vendor/competitor assessment workflow. Proven 2026-07-09: Tridiagonal.AI evaluation for PETRONAS. Use when user drops a company URL and asks "how good or bad is this?" Covers site inspection, external validation, competitive context, and KPI-framed classification.
- `references/institutional-financial-deep-dive-pattern.md` — 8-section spine for "predict next quarter/half-year for [Company]" requests. Includes parametric scaling model, hedge-exposure reality table, WEALTH MCP fallback playbook, and a worked PETRONAS 1H FY2026 example. Proven 2026-07-13. Use when user says "deep research [Company] financial prediction", "predict Q1/H1 FY_X for [Company]", or "what's the outlook for [Company] earnings".
- `references/public-figure-social-scan.md` — pattern for scanning a public figure's X and Threads presence, platform-specific extraction limits, and synthesis structure. Proven 2026-07-12: Ray Dalio scan (X + Threads + Fortune/HBR/Bloomberg → governance reflection).
- `references/competitive-field-research.md` — pattern for researching an entire competitive field (athletes, artists, developers), ranking participants by weighted criteria, and compiling social media handles via federation/sponsor cross-reference. Use when user asks "rank the top X in [domain]" or "find all [competitors] in [field]." Proven 2026-07-12: Malaysia Men's Physique bodybuilder ranking (10 athletes, NPC/IFBB/WBPF data).
- `references/protocol-compliance-audit.md` — two-loop pattern for researching external protocol standards (A2A, MCP, ACP, ANP) and producing a structured gap analysis against our living implementation. Covers spec extraction, ecosystem research, gap classification, and remediation architecture. Use when user says "deep research [protocol] and map to our [system]". Proven 2026-07-13: A2A v1.0 vs AAA gap analysis.
- `references/institutional-financial-deep-dive.md` — pattern for deep research on sovereign-backed / state-owned enterprises that publish half-yearly (NOCs, sovereign wealth vehicles, GLCs). Subsidiary read-through + segment elasticity model + macro price-shock propagation + backtest + falsification. Proven 2026-07-13: PETRONAS Group 1H 2026 projection + Q1 2026 read-through. **Use when the user asks for a period the Group hasn't published yet, or for any "predict [state-owned entity] quarterly" task.**
- `references/analyst-grade-report-template.md` — 12-section sell-side HTML spine + CSS components + 8 figure recipes + weasyprint render command. Proven 2026-07-13 PETRONAS 1H FY2026 (14 pages, 8 figures, 682 KB). Use when the user asks for "UOB-style", "analyst-grade", "broker report", "sell-side format", or names any ASEAN broker explicitly (UOB KayHian, Kenanga, CIMB, Maybank IB, RHB, Affin Hwang, PublicInvest).
- `references/noc-ioc-financial-analysis.md` — Multi-loop refinement methodology for NOC/IOC financial prediction. Covers: 3-loop pattern (commodity-price → structural adjustments → external validation), corporate shadow dissection, FX correction discipline, transition-arm tax identification, rightsizing analysis, capex efficiency comparison, probability assignment, falsification tests, accuracy calibration framework. Proven 2026-07-13: PETRONAS 1H FY2026 (3 loops, PATAMI corrected from +10.7% to +1.9% YoY). Use when user asks for financial prediction of any NOC/IOC, or says "redo another loop" / "refine the forecast" / "final loop".
- `references/news-feed-bias-detection.md` — Pattern for identifying bias in user's news/YouTube feed and sourcing contrasting signals. Covers: narrative type classification (institutional, corporate PR, techno-alarm, reassurance, bottom-up), bias pattern mapping, contrasting signal sourcing from worker forums, opposition media, market data, academic sources. Proven 2026-07-13: Arif's Google News + YouTube feed analysis.
- `references/news-feed-bias-diagnosis.md` — Expanded methodology for diagnosing algorithmic bias when user asks "why does Google/YouTube suggest this?" Covers: content type classification, feed signal identification, contrasting signal sourcing (3 signals per content piece), source diversification recommendations. Proven 2026-07-13: Arif's Google News (PETRONAS PR served as news) and YouTube (Tailscale beginner guide for Level 5 user) diagnosis.
- `references/datapack-gap-filling.md` — Systematic method for identifying and filling knowledge gaps after initial research deliverable. Covers: gap listing, impact prioritization, targeted search per gap, reconciliation with existing model, structured JSON output. Proven 2026-07-13: PETRONAS 4 gaps filled (dividend cut reason, Gentari PAT, fiscal dependency, Petros-Sarawak status).
- `references/research-tool-fallback-ladder.md` — 8-step fallback ladder when Tavily-backed tools (web_search, web_extract) fail with 432/402. Wikipedia API → browser console JS → browser snapshot → platform doc pages → curl + JSON-LD/schema.org extraction → pdftotext for government PDFs → domain-specific MCP tools (WEALTH capital_market, GEOX) → direct article URL navigation. Includes anti-patterns for search engine CAPTCHAs. Proven 2026-07-18: Malaysia economic research (Tavily 432, all search engines CAPTCHAd — fell through to curl+JSON-LD on malaysia4u.com + pdftotext on MOF PDF + WEALTH capital_market for live FX/commodities).

## Templates

For well-test / drilling operation summaries, use `templates/well-test-operation-summary.md` — a 6-section spine (Rig & Towing / Well Position / Program Objective / Key Dates / HSE+People / Critical Gaps) with epistemic labeling baked in. The gaps list is the value; the filled cells are the framing.
