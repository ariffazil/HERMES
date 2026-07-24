# News Feed Bias Detection Pattern

> Proven: 2026-07-13. Arif's Google News + YouTube feed analysis.

## When to Use

When the user shares news links and asks "what's the bias?", "why is my feed showing this?", "what signal am I missing?", or "suggest contrasting sources." Also when the user shares multiple news stories that all seem to align with one narrative direction.

## The Pattern

### Step 1: Classify Each Story by Narrative Type

| Type | Description | Who benefits |
|---|---|---|
| **Institutional** | Government says X, company does Y, experts warn Z | The institution being covered |
| **Corporate PR** | Company announcement framed as news | The company |
| **Techno-alarm** | "Experts warn about X" with AI/tech signatories | The tech companies (often signatories themselves) |
| **Reassurance** | "Government guarantees supply/stability" | The government managing panic |
| **Bottom-up** | Worker forums, opposition media, market data | Rarely served by algorithm |

### Step 2: Map the Bias Pattern

Look for the common thread across all stories. If all stories are top-down institutional narratives, the feed is optimised for establishment framing. If all are tech-hype, the feed is optimised for builder/entrepreneur framing.

Common bias patterns:
- **All institutional** → user sees official version only, misses dissent
- **All tech-hype** → user sees opportunity only, misses displacement
- **All doom/fear** → user sees risk only, misses execution
- **All Malaysian domestic** → user misses global context

### Step 3: Find Contrasting Signals

For each story, search for the **opposite framing**:

| If feed shows... | Search for... |
|---|---|
| "AI impact is coming" | "AI layoffs already happening" + specific company names |
| "Company is growing" | "Company considered selling" + "Company losses" + opposition criticism |
| "Government guarantees supply" | "Subsidy cost explosion" + "Fiscal pressure" + market data |
| "Expert warns about X" | "Worker displaced by X" + "Company using X as cover for cuts" |

### Step 4: Source Contrasting Links

Pull from sources the algorithm WON'T serve:
- **Worker forums:** Reddit r/Layoffs, Glassdoor, Blind
- **Opposition media:** Malaysiakini, FMT commentary, opposition MPs
- **Market data:** FRED, BNM, CME futures, TradingEconomics
- **Academic/contrarian:** HBR, Yale Insights, Oxford INET, NBER
- **International:** Reuters, Bloomberg, FT (for non-domestic perspective)

### Step 5: Present the Meta-Pattern

Show the user:
1. What their feed serves them (the narrative)
2. What the contrasting signal says (the counter-narrative)
3. The gap between them (where the real insight lives)
4. How to debias (specific sources to actively pull)

## Example (2026-07-13)

**User's feed:** Nobel laureates on AI (The Star), Gentari solar at KLIA2 (The Edge), Government guarantees petroleum supply (Astro Awani)

**Bias:** All three are top-down institutional narratives. No bottom-up dissent, no market data, no opposition voice.

**Contrasting signals found:**
1. AI layoffs already happening — HBR: "Companies Are Laying Off Workers Because of AI's Potential—Not Its Performance" + NYT: 150+ companies, 115,000 cuts in 2026
2. Gentari might be sold — Bloomberg Oct 2024: PETRONAS considered $300-500m minority stake sale
3. Fuel subsidy exploding — RM 1.99/L subsidised vs RM 3.72/L market = RM 52m/day gap

**Meta-pattern:** Feed optimised for institutional narrative. Contrasting signals require active search from worker forums, market data, and academic sources.

## YouTube Algorithm Bias (proven 2026-07-13)

YouTube's recommendation algorithm detects user behavior patterns and serves content that matches **activity signals**, not **expertise level**. This creates a specific bias: beginner content for advanced users.

**Detection pattern:**
- User does technical work (Python, VPS, server management) → YouTube detects "developer/infra" signal
- YouTube serves beginner tutorials for tools the user already uses at advanced level
- Sidebar recommendations cluster around the same audience segment (AI builder, developer, infrastructure)

**Why this happens:** YouTube optimizes for engagement probability, not expertise match. A Tailscale beginner guide gets served to someone running 6 MCP servers because the algorithm sees "servers + networking" signals but can't distinguish Level 1 from Level 5.

**Contrasting signal:** Search for advanced/architecture-level content explicitly (e.g., "Tailscale ACLs for multi-agent orchestration" not "Tailscale clearly explained"). Or use alternative platforms (Hacker News, architecture blogs, conference talks) where content is curated by expertise level.

**Proven 2026-07-13:** Arif's YouTube suggested "Tailscale, Clearly Explained (Beginner's Guide)" by David Ondrej (401K subs) while running a 6-organ agentic federation on a single VPS. The video was Level 1 content for a Level 5 user.

## Pitfalls

- **Don't assume malice.** Algorithm bias is structural, not intentional. The feed serves what gets engagement.
- **Don't dismiss the institutional narrative entirely.** It's often factually correct. The bias is in framing and omission, not fabrication.
- **The contrasting signal is often LESS polished** than the institutional narrative. Reddit posts, opposition media, and market data don't have PR teams. That's the point.
- **Present both sides, then let the user decide.** Don't replace one bias with another.
