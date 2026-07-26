# News Feed & YouTube Bias Diagnosis

> **Purpose:** When user asks "why does Google/YouTube suggest this?" — diagnose algorithmic bias and source contrasting signals to break filter bubbles.

---

## When to Use

- User shares a news article or YouTube video and asks "why am I seeing this?"
- User asks "what's the bias?" or "what signal am I missing?"
- User wants to diversify their information diet

## Diagnosis Method

### Step 1: Classify the content type

| Type | Description | Example |
|---|---|---|
| **Institutional PR** | Company/government-initiated announcement | PETRONAS media release |
| **Corporate narrative** | Management framing of results | "Disciplined cost management" |
| **Reassurance** | Government "all is well" messaging | "Bekalan stabil hingga Disember" |
| **Techno-alarm** | AI/tech will destroy jobs | "200 experts warn on AI impact" |
| **Product marketing** | Disguised as tutorial/guide | Tailscale "beginner guide" with sponsor |
| **Genuine journalism** | Independent investigation, sources cited | Reuters, IEEFA analysis |

### Step 2: Identify the feed signal

What triggered the algorithm?

| Signal | What Google/YouTube thinks | Reality |
|---|---|---|
| Recent searches for [company] | "User interested in company news" | Serves company PR, not critical analysis |
| Technical work detected | "User is a developer" | Serves beginner tutorials, not advanced |
| Location = Malaysia | "User wants local news" | Serves government-aligned media |
| Engagement with AI content | "User is AI builder" | Serves AI hype, not substance |

### Step 3: Source 3 contrasting signals

For each piece of content the user shares, find 3 contrasting perspectives:

1. **Critical/skeptical take** — What's the opposite narrative?
2. **Global/regional perspective** — What do sources outside the user's bubble say?
3. **Data-driven counter** — What do the numbers say vs the narrative?

### Step 4: Recommend source diversification

Suggest 3-5 sources the user should add to their regular rotation:
- Independent research institutes (IEEFA, Stratfor, Chatham House)
- International wire services (Reuters, Bloomberg) — not beholden to local access
- Academic/industry analysis (IEA, Wood Mackenzie, Rystad)
- Worker/community forums (Reddit, industry-specific)
- Opposition/alternative media

## Proven Examples

### 2026-07-13: Arif's Google News feed

**3 articles served:** Gentari solar at KLIA2 (PR), government guarantees petroleum supply (reassurance), PETRONAS-Shizuoka LNG deal (growth).

**Bias:** All 3 were PETRONAS-initiated or government-initiated. Google served the company's own narrative.

**3 contrasting signals found:**
1. LNG supply glut (IEEFA, IEA) — structural headwind to PETRONAS growth story
2. Malaysia fuel subsidy crisis (Reuters, Stratfor) — RM 38bn/year fiscal burden, larger than PETRONAS dividend
3. PETRONAS reputation risk (Berkshire Media) — negative sentiment 48.8M reach vs PETRONAS 26.2M

### 2026-07-13: Arif's YouTube suggestion

**Video:** "Tailscale, Clearly Explained (Beginner's Guide)" by David Ondrej

**Bias:** YouTube detected "developer + VPS + AI agents" from session activity. Served Level 1 content for a Level 5 user. Product marketing disguised as tutorial (Hostinger sponsor).

**Diagnosis:** The tool itself (Tailscale) is legitimate. The content framing (beginner guide) doesn't match the user's level. The algorithm optimizes for engagement, not relevance.

## Pitfalls

- **Don't dismiss all algorithmic suggestions.** Sometimes the algorithm is right. Evaluate content on merit, not source.
- **Don't assume malice.** Algorithm bias is structural, not intentional. The algorithm serves what gets engagement.
- **Don't over-correct.** Adding too many contrasting sources creates noise. Recommend 3-5 high-signal sources, not 20.
