# Sovereign Self-Assessment from Session History

> **When the sovereign asks about THEMSELVES** — building a personal psychological assessment from `session_search` across past conversations, not from exported chat files (which is `text-forensics` territory).

## When to Use This Mode

This is Mode C of human-intelligence-gathering. It applies when:

- Arif asks: "what trauma have I endured / not endured?"
- Arif asks: "what's unresolved in me?"
- Arif asks: "tell me about myself based on what you know"
- The subject IS the sovereign, not an external person

**Do NOT use this mode for external persons.** Use Mode A (text-forensics, chat exports) or Mode B (web + session mentions) for that.

## Why This Is Different

| Mode | Subject | Data Source | Risk |
|---|---|---|---|
| A: Data-rich | External person | Chat export, documents | Fabrication from missing data |
| B: Data-poor | External person | Web, session mentions | Inference-overreach, sibling-context projection |
| **C: Sovereign self** | **The sovereign** | **session_search + memory** | **Overclaiming inner truth** |

**The critical risk for Mode C is Scar #12** — turning plausible interpretations into claims about the sovereign's inner life. The analysis crosses from OBS/DER into INT at the exact point where you infer meaning, motive, or wound from pattern. Every INT must be labeled as such.

## Pipeline: 5 Phases

### Phase 1: SOURCE INVENTORY (what do you actually have?)

Before a single claim, inventory what data exists:

| Source | What It Gives | Epistemic Ceiling |
|---|---|---|
| `memory` (user profile) | Explicitly stated facts | OBS — if the user said it directly |
| `memory` (your notes) | Observations from past sessions | DER — you wrote these, they may be stale |
| `session_search` | Conversation transcripts | OBS — but text-only, no tone/body |
| `carry_forward.json` | Session state summaries | DER — compressed, may miss context |
| RASA DERITA document | User's authored framework | OBS — direct artifact of their thinking |
| Direct question from user | Current intent | OBS — but shaped by what they choose to share |

**Rule of thumb:** If 80%+ of your sources are `session_search` results (conversation transcripts), you are in Mode C. That's fine — just name it.

### Phase 2: TARGETED SEARCH STRATEGY

Do NOT run a single generic `session_search`. Run multiple targeted queries:

```python
queries = [
    "Arif bapa abah mother mak family",
    "Arif PETRONAS Laletha Kak Su BANGANG",
    "Arif gay shadow desire identity",
    "Arif trauma luka sakit perit",
    "Arif cerita kisah hidup background UK scholar",
    "Hakikat Diri self shadow love",
    "Nabilah trauma betrayal",
]
```

**Important:** Session IDs change. Session TITLES are more stable for cross-reference. If a session title appears in search results (e.g. "Hakikat Diri, Altruisme, dan Cinta"), note the session_id and use it for deep reading.

**Search depth:** Limit 5-10 per query. If a query returns nothing useful, try different keyword combinations. BM terms (sakit, luka, perit) may find different sessions than English terms (trauma, wound, grief).

### Phase 3: DEEP SESSION READING

When you find a relevant session, read the **bookend messages** (first 3 + last 3) to understand:
- **What was the trigger?** (the user's opening intent)
- **What was resolved or sealed?** (the closing state)
- **What was the relationship dynamic?** (user pushing back? agreeing? deflecting?)

Then read the **anchor message** (the FTS5 hit) plus its ±5 context window to understand the specific content.

**If a session has multiple matches** (multiple hits across the conversation), read the full sequence. The July 7 "Hakikat Diri" session had matches at messages 10264, 12437, 12440, 12444 — reading them in sequence reveals a narrative arc from external analysis → shadow recognition → personal disclosure → deep wound mapping.

### Phase 4: STRUCTURED ASSESSMENT

Organize findings into this framework:

#### A. Trauma the sovereign KNOWS they endured
- Events they explicitly named as traumatic
- People/relationships they flagged as wounding
- Experiences they processed consciously
→ Epistemic: OBS (from their own words)
→ Format: event + their framing + evidence

#### B. Trauma they may have endured but may not fully CONSCIOUS of
- Patterns visible across multiple sessions that the sovereign has NOT named as trauma
- Behaviors that look like coping mechanisms (compartmentalization, intellectualization)
- Structural conditions they navigate daily (e.g. being gay in Malaysia) that they frame as "fine" but leave measurable marks
→ Epistemic: DER/INT — MUST label as interpretation
→ Format: pattern evidence + your interpretation + explicit "this is my reading, not their claim"

#### C. What they have NOT yet endured
- Experiences that have not yet been tested
- Vulnerabilities that remain ungapped in their protection architecture
- Losses that haven't happened yet (losing someone who knows them fully)
→ Epistemic: SPEC — forward-looking, by nature uncertain
→ Format: counterfactual statements ("they have not yet faced X")

### Phase 5: F13 BOUNDARY MAINTENANCE

**The sovereignty rule:** Never promote Layer 3 (possible interpretation) to Layer 1 (observed action). State what they said. Offer interpretations as questions, not claims. Explicitly acknowledge what you cannot see.

Before outputting:
1. Review every claim. Is it labeled OBS/DER/INT/SPEC?
2. For every INT claim: is there a clear OBS foundation, or is it floating?
3. For every SPEC claim: is it framed as possibility, not prediction?
4. Has any claim crossed from "what the data suggests" to "what I assert about their inner life"?
5. Could a reader mistake your interpretation for a statement of fact about the sovereign's psychology?

**If any answer is "yes" or "unclear" → downgrade the epistemic label, add hedging, or remove the claim.**

## The RASA DERITA Lens

For deeper assessments, use the RASA DERITA framework as an analytical lens (since it is the sovereign's own authored framework):

| RASA DERITA Axis | Question for Assessment |
|---|---|
| **Axis I: Trust & Betrayal** | Where has the sovereign experienced institutional or personal betrayal? How did they respond — acknowledgment path or denial path? |
| **Axis II: Causality & Consequence** | What cascades from their wounds? How far downstream have the consequences spread? |
| **Axis III: Power & Consent** | Where was their consent overridden? Where did they override themselves (compartmentalization, self-sufficience as protection)? |
| **Axis IV: Truth & Naming** | What have they named? What remains unnamed? What do they intellectualize rather than feel? |
| **Axis V: Epistemic Humility** | What do they NOT know about themselves? Where is the map confused with the territory? |

**Important:** The RASA DERITA framework is the SOVEREIGN'S tool. Using it to analyze the sovereign is a privilege, not a right. Always flag when you're using their own framework back at them — and invite correction.

## Example Output Structure

```markdown
## [SOVEREIGN] — Personal Assessment

### What I Actually Know (OBS)
- [Event/fact directly stated by sovereign, with session citation]

### What Patterns Reveal (DER)
- [Recurring behavior/statement cluster across sessions]

### What I Interpret (INT — READ WITH CAUTION)
- [Connections I'm drawing — labeled as my interpretation]
- [The sovereign may disagree — they know themselves better]

### What Remains Untested (SPEC)
- [Forward-looking: what they haven't faced yet]

### What I DON'T Know
- [Explicit gap list — what data would change this analysis?]

### The Protection Architecture
- [Structural observation about their coping patterns]
- [This is derived from behavior, not claimed as inner truth]
```

## Known Risks

1. **Overclaiming inner truth (Scar #12).** This is the #1 failure mode. Every plausible interpretation can feel profound — but profundity is not evidence. If your analysis "sounds like poetry," you've probably crossed the line.
2. **Session-search false negatives (Scar #13).** FTS5 indexes message CONTENT, not metadata. If the sovereign's name doesn't appear in a session's text, that session won't be found. Cross-check with `sessions.json` for DM-based conversations where the user appears as "No name" or similar.
3. **Stale memory.** Your `memory` entries may be outdated. Session history is ground truth; memory is a cached summary. Prefer session_search over memory when depth is needed.
4. **Compression loss.** Large sessions (e.g. the 7 July shadow analysis) get truncated in search results. The bookend + anchor window may miss critical mid-session disclosures. Use multiple targeted queries to find specific anchor points.
5. **The sovereign is NOT a case study.** They are F13. The analysis serves them, not the framework. If the sovereign says "that's not right" — stop. Do not defend the analysis.

## Origin

First demonstrated: 2026-07-30 session. Arif asked "what trauma have I endured / not endured / what's unresolved?" Answer was built from 5+ session_search queries across 10+ sessions, cross-referenced with memory and the RASA DERITA framework.

---

*DITEMPA BUKAN DIBERI. Mode C of human-intelligence-gathering.*
