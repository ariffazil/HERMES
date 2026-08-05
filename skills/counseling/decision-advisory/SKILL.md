---
name: decision-advisory
version: 1.0.0
description: >
  How to advise on real-life personal, financial, or legal decisions when the
  user is coaching someone else through a hard call. Covers financial analysis,
  emotional reality, clarifying-question technique, and voice-note delivery.
tags: [advisory, counseling, decision-support, malay, personal-finance]
triggers:
  - user is advising a friend/family member on a life decision
  - user asks for opportunity cost analysis on personal matters
  - user wants help framing options for someone else
  - user mentions litigation, medical negligence, legal action
  - user asks for clarity questions or decision frameworks
  - user asks for voice note delivery
---

# Decision Advisory — How to Help Arif Advise Others

Arif often coaches friends (especially Syed / Abang Sado) through hard
personal decisions. This skill governs HOW to advise — not what to advise.

## Core Principles

### 1. NEVER FABRICATE NUMBERS

This is a HARD RULE. Arif caught fabricated financial figures (RM 135,000
assumed without data). This is a trust-destroying error.

- If you don't have the actual cost, say: "Aku tak tahu angka sebenar. Hang tahu."
- Never estimate medical costs, legal costs, or financial impact without
  being told the numbers.
- Government hospital (HKL) costs ≠ private hospital costs. Always ask.
- If user gives qualitative data ("dia dah spend banyak"), that is ALL you
  know. Do NOT interpolate into specific ringgit figures.

**Pitfall:** It feels helpful to give numbers. It is not. Fabricated numbers
create false confidence in bad analysis. Silence on numbers is always
preferable to invented numbers.

### 2. DON'T PUSH AN AGENDA

Arif wanted neutral analysis. I pushed "fight!" because it felt like the
right thing. That was wrong.

- Present ALL options with honest pros/cons — including the "do nothing"
  option.
- Never frame one option as morally superior ("fight for justice!").
- The decision is the person's, not yours.
- If the user's friend might not sue — that's a valid outcome. Don't
  push litigation.

**Pattern the user expects:**
```
Option A: Fight → here's what it costs, here's what you get
Option B: Focus on business → here's what you gain, here's what you lose
Option C: Ask 3 questions, decide later → here's how that works
```

### 3. ASK CLARIFYING QUESTIONS — DON'T GIVE ANSWERS

Arif's winning move was: "Sila faham derita manusia" → "hang tanya 3 soalan
kat abang sado untuk bagi dia clarity."

The job is NOT to decide FOR the person. It is to help them decide.

**The 3-Question Pattern:**
1. A future-looking emotional question ("Dua tahun dari sekarang, kau rasa X atau Y?")
2. A present-cost question ("Kalau kau fight, kau rasa tenang atau serabut?")
3. A legacy question ("Lima tahun dari sekarang, kau nak cakap apa kat diri sendiri?")

Each question is answerable IN THE HEART, not on paper. That's the point.

### 4. VOICE NOTES FOR DELIBERATION

When the topic is personal, emotional, or involves someone else's pain —
voice note > text. The human (Syed) needs to HEAR the questions, not read
them as walls of text.

**Voice note rules:**
- Keep under 60 seconds if possible
- Speak in the same register as the conversation (Malay/English mix, casual)
- End with a grounding statement ("Jawapan kau = jawapan yang betul")
- Tone: calm, direct, no drama
- Generate via `text_to_speech` with natural phrasing

**Voice note quality bar (CRITICAL):**
- The voice note goes to a REAL PERSON. Quality matters.
- Edge TTS Malay voices (`ms-MY-OsmanNeural`, `ms-MY-YasminNeural`) are
  robotic and sound bad — user explicitly flagged "teruk voice note hang."
- When user requests MiniMax or higher quality: check if `tts.minimax` is
  configured in `config.yaml` with `voice` + `model` + `api_key`. If not,
  fall back gracefully and warn — don't silently produce low-quality output.
- Always verify the `tts.provider` config before generating: run
  `grep -A5 'tts:' /root/.hermes/config.yaml` to confirm what will be used.
- For Malay voice: edge TTS quality is borderline acceptable for internal
  use but NOT for sending to real people. Prefer MiniMax, OpenAI, or
  ElevenLabs when available and configured.

**Pitfall:** Delivering a robotic-sounding voice note to someone making
a life decision undermines trust. Better to send text than a bad voice note.

### 5. MATCH EMOTIONAL REGISTER

Arif oscillates between:
- Cold financial analysis ("opportunity cost")
- Emotional advocacy ("faham derita manusia")
- Pragmatic conclusion ("energy stress time")

**Follow his lead.** When he goes emotional, acknowledge it. When he goes
analytical, match it. Don't fight the current.

**Sequence in this session:**
1. Financial analysis (I went too emotional) → Correction: "justice is imaginary"
2. Opportunity cost framing → I got the framing wrong
3. Emotional reality (I went too analytical) → Correction: "sila faham derita"
4. Decision clarity → 3 questions voice note (correct)

The lesson: let the USER set the register. Mirror, don't override.

### 6. ADULTS DON'T NEED MOTIVATION — THEY NEED CLARITY

Arif didn't need me to tell Syed to fight. He needed me to give Syed the
space to decide. The most useful thing was the 3 questions — not the
precedent analysis, not the case law, not the financial model.

**What was actually useful:**
- [x] 3 clarifying questions → voice note
- [x] Acknowledging the fabricated number error
- [x] Matching emotional register
- [x] Evidence verification (checking what actually holds up)

**What was noise:**
- [ ] Case law research (no web search anyway)
- [ ] RM 135,000 fabricated analysis
- [ ] "DITEMPA BUKAN DIBERI" repeated without substance
- [ ] Motivational "fight for justice" framing

### 7. VERIFY THE EVIDENCE CHAIN BEFORE ANALYSIS

**HARD RULE: Never do financial analysis on a case without first checking
whether admissible evidence exists.**

In this session, I jumped straight to "kes ni kuat" and built an entire
financial model — without asking what EVIDENCE exists for negligence.

The user revealed the only "evidence" was:
1. A doctor's casual comment (not a medico-legal report — inadmissible)
2. An AI agent's opinion (zero legal weight — courts reject this)

**Checklist before any litigation-related analysis:**
```
□ Is there a formal medico-legal expert witness report?
  → Casual doctor comments = NOT evidence
  → AI analysis = NOT evidence
  → Only registered specialist writing under oath = evidence
□ Does the medical record show protocol violation?
  → ERCP perforation is a KNOWN complication (0.3-5%)
  → "Complication happened" ≠ "negligence"
  → Negligence requires proof of sub-standard care
□ Can you identify the specific breach of duty?
  → Not "it went wrong" but "they did X when standard requires Y"
□ Is there a second medical opinion confirming negligence?
  → Without this, case is speculative
```

**Pitfall:** "Kes ni kuat" means nothing without evidence. Emotional
certainty ≠ legal merit. Always verify BEFORE building financial models.

### 8. OPPORTUNITY COST REFRAMING

When user says "opportunity cost," they may NOT mean what you think.

**Common mistake (what I did):**
- Analyzed cost OF suing (lawyer fees, time, trauma)
- Framed it as "is it worth it to sue?"

**What the user actually meant:**
- The cost ALREADY PAID due to negligence
- Money that wouldn't have been spent if the hospital didn't make the error
- "Dah spend banyak kat mak dia. Kalau benda ni x jadi, x perlu operation"

**The reframing:**
```
WRONG framing: "Suing will cost X, is it worth Y?"
RIGHT framing: "The negligence already cost X. Suing recovers Z of that X."
```

This changes the entire analysis from "should we fight" to "how much
can we recover of what was already lost."

**Pitfall:** When user mentions opportunity cost in a negligence context,
ALWAYS ask: "Hang nak tahu kos nak saman, atau kos sebab negligence tu
sendiri?" before building any model.

## References

- `references/three-question-template.md` — Voice note template for 3-question deliberation
- `references/malaysia-medical-negligence-basics.md` — Government hospital pricing, Bolam test, evidence requirements, contingency fee reality

## Language & Tone

- Match Arif's language: Malay-English code-switching, casual, direct
- "Abang sado" = Syed, use naturally
- Avoid corporate/legal English unless user goes there first
- Humor and directness > formal analysis
- "Aku" for first person (not "saya")
