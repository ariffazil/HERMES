# PR Media Contradiction Mapping

> **Technique:** Systematic comparison of official/media narrative vs. verified facts
> **Origin:** SEARAH JV media audit, 2026-07-22
> **Analyst:** Hermes Agent for Arif Fazil

## When to Use

When an institution launches a major announcement and you need to detect whether media coverage reflects independent journalism or coordinated PR amplification. The technique reveals what the institution wants hidden by reading what media systematically omits.

## The Technique: Omission Pattern Grid

### Step 1: Identify the core facts

Build the ground truth from primary sources — Companies House filings, court records, PSC registers, treaty databases. These are your OBS (observed) facts. No PR release qualifies as a primary source for this purpose.

### Step 2: Collect media coverage across outlets

Gather coverage from:
- Official press releases (the institution's own words)
- Mainstream national media (both pro-government and independent)
- Business/financial press
- International wire services (Reuters, Bloomberg)
- Social media explainer accounts (Threads, TikTok, Instagram)
- Industry analyst reports (Wood Mackenzie, Rystad, etc.)

### Step 3: Build the omission grid

Create a matrix. Each row is a verifiable fact. Each column is a media source. Mark which facts each source includes and which it omits.

| Fact | Official PR | National Media A | National Media B | Business Press | International Wire | Social Media Explainer |
|---|---|---|---|---|---|---|
| UK incorporation | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| English law jurisdiction | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| $2 share capital | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| PETROS dispute | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Federal Court cases | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Board asymmetry (2 IT in London, 2 MY in KL) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| $20B capex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 300k-500k boe/d production | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 19 assets | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Reading the grid:** When multiple outlets independently omit the SAME sensitive facts while including the SAME positive facts, you are looking at coordinated messaging — not independent journalism.

### Step 4: Read what IS said against what IS true

For each outlet that discusses the sensitive topic, compare their framing against verified facts:

| What They Say | What's True | Technique Used |
|---|---|---|
| "PETRONAS kekal milik penuh Malaysia" | Parent entity yes. 5 MY assets now in UK company, 50% Eni-owned, English law. | **Parent-asset conflation** — talk about parent, avoid talking about assets |
| "hanya aset huluan" | Core producing gas fields feeding Bintulu LNG — backbone of MY gas export | **Minimizing language** — "only" for things that are actually strategically critical |
| "tidak mengubah pemilikan terhadap aset-aset lain" | Deflects to what WASN'T transferred, avoids what WAS | **Straw-man framing** — answer a different question than the one asked |
| "tidak tepat" / "misconception" | Sets up a straw man ("PETRONAS dijual") then knocks it down — while the real question (UK structure, jurisdiction, PETROS) goes unaddressed | **Crisis-response PR posture** — make the critic look confused, not the institution look questionable |

### Step 5: Identify the source

When an outlet's language mirrors the official press release almost verbatim, the article is PR amplification, not reporting:

| Official PR | Outlet |
|---|---|
| "strengthen portfolio value, support sustainable energy development" | "strengthening regional energy security, accelerating sustainable energy development" |
| "unlock the full value of an integrated portfolio" | "unlock growth opportunities across both countries" |

### Step 6: Check for sponsorship

For social media explainers, check:
- Bio: does the account advertise "Collaboration/Sponsorship"?
- Content style: 15-slide carousel = significant production effort ≠ casual explanation
- Imagery: official PR photography or independent images?
- Framing: "people are confused, let us clarify" = PR crisis posture
- Positioning: "pendemokrasian ilmu" (democratizing knowledge) while running paid PR = disguise

### Step 7: Find the pattern

**Coordinated PR campaign indicators:**
1. Same omissions across geographically and editorially separate outlets
2. Near-identical language to official press release
3. Defensive framing ("clarifying misconceptions") launched simultaneously
4. Social media accounts with sponsorship flags running institution-friendly explainers
5. The sensitive facts that are absent from Malaysian domestic media appear in international analyst reports (Wood Mackenzie, Reuters — which aren't dependent on Malaysian government access)

**The iron rule:** If multiple outlets from different publishers ALL omit the same sensitive facts, it's not coincidence. It's a press office that knows exactly what questions to avoid.

## Case Study: SEARAH JV Media Audit (2026-07-22)

### Ground Truth (from Companies House, court records, UNCTAD)

1. SEARAH LIMITED registered in UK (Co. No. 17027115), ENI House, London
2. Governed by UK Companies Act 2006 — English law, London arbitration
3. Share capital: USD 2 (nominal SPV)
4. 5 Malaysian assets transferred: SK316, Kasawari, 2008 PSC, Angsi Besar, NC3
5. PETROS (Sarawak state oil company) disputes ownership of SK316 and Kasawari
6. Two Federal Court cases active: PETRONAS vs Sarawak, Sarawak vs Federation
7. Board: 2 Italian directors (London-based), 2 Malaysian (KL-based)
8. Data leak trial ongoing: ex-PETRONAS manager leaked Q1 2024 data to PETROS CEO/CFO
9. $20B committed capex, $6B JP Morgan credit facility
10. Production: 300k boe/d → 500k target

### Media Sources Audited

| Source | Type | Omissions | Language Pattern | Verdict |
|---|---|---|---|---|
| PETRONAS press release (Jun 8) | Official | All structural facts omitted | Baseline — "strengthen portfolio value" | PR |
| Eni press release (Jun 8) | Official | All structural facts omitted | Baseline — "satellite model" | PR |
| BusinessToday (Jun 8) | Malaysian business | All omitted, near-verbatim PR language | PR reworded | PR amplification |
| The Malaysian Reserve (Jul 17) | Malaysian business | UK incorporation, English law, PETROS, court cases, board, data leak all omitted | Neutral business reporting, but only surface facts | Selective reporting |
| ATMA Studio Threads (Jul 21) | Social media explainer | UK incorporation, English law, PETROS, court cases, board, data leak, sponsorship flag in bio | Defensive PR framing: "tidak tepat," "hanya," "tidak mengubah" — official PR photo used | Paid PR disguised as education |
| Reuters (Jun 8) | International wire | Some structural facts included (UK structure implied), PETROS disputed context absent | "JV to manage 19 gas assets," "satellite model" | Analytical reporting |
| Wood Mackenzie (Jun 2026) | Industry analyst | Structural facts discussed, "reshape Southeast Asia's upstream sector" | Independent analysis | Independent |

### Key Findings

1. **Every Malaysian-facing source omits UK incorporation, English law jurisdiction, PETROS dispute, and Federal Court cases.** International sources don't.
2. **ATMA Studio openly advertises paid sponsorships** yet positions SEARAH content as "pendemokrasian ilmu." The 15-slide carousel uses official PR photography and mirrors PETRONAS talking points while systematically omitting structural concerns.
3. **BusinessToday's article is indistinguishable from the PETRONAS press release** — light paraphrasing, same framing, same omissions.
4. **The coordinated omission pattern spans 4 Malaysian outlets** (PETRONAS PR, BusinessToday, Malaysian Reserve, ATMA Studio) — all omit the same structural facts while emphasizing the same positive ones. This is a press office strategy, not independent editorial judgment.

### The "Trojan Horse" Signal

When an institution simultaneously:
- Distributes a press release with strategic omissions
- Has business media outlets reprint it near-verbatim
- Has social media explainer accounts (with disclosed sponsorship flags) run defensive "clarification" content
- All sources omit the same politically sensitive facts (PETROS, Federal Court, UK jurisdiction)

...you are not looking at a media ecosystem. You are looking at a coordinated communications operation.

## Integration with Institutional Body Language

This technique maps to:
- **Channel D: Information Posture** — reading what the institution suppresses vs. what it amplifies
- **Channel G: Boundary Behaviour** — how it treats the public's right to know
- **The Signal Hierarchy** — official language (tier 6) contradicts irreversible commitments (tier 1: UK incorporation, English law, asset transfer)
- **Institutional dissonance:** "We are still fully Malaysian" while assets move to UK jurisdiction

## Pitfalls

1. **Assuming coordination without evidence of contact.** Omission patterns can emerge from shared press releases and journalist training, not necessarily direct coordination. The technique identifies the PATTERN; attribution of intent requires additional evidence.
2. **Single-outlet reading.** One outlet omitting a fact is not a pattern. Four outlets independently omitting the same fact — that's a pattern.
3. **Confusing international vs domestic reporting norms.** International wire services have larger research teams and less government-access dependency. Their inclusion of sensitive facts may reflect capability, not independence.
4. **Over-reading sponsorship flags.** An account that takes sponsorships doesn't mean every post is sponsored. But when the content mirrors official PR and uses official photography, the sponsorship flag becomes significant.
