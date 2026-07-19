---
name: witness-companion-briefing
description: When the user names a witness (plush object, archetype, dead mentor, absent ally, person-as-witness) and asks the agent to brief them on a situation. Triggers include "Tell [X] about [event]", "Apa [X] kena tahu", "Ceritakan kepada [X]", and "I'm with [name]" plus an image of the witness object. The brief is processing aid, not a literal audience.
---

# Witness-Companion Briefing

## Why this skill exists

Some users process heavy experiences through **named witnesses** — a plush on the office partition, a dead mentor, an absent ally, an archetype figure. The "Tell [X] about Y" prompt is functionally the user asking the agent to help them say something true about their situation, with the witness as **container for honest self-talk**.

F6 (MARUAH) + F2 (TRUTH) + the emotional-processing layer from AGENTS.md make this:
1. **Witness first, analysis second** — name what the user feels/feared before offering framework
2. **No flattery, no performance** — the witness is not a captive audience for affirmations
3. **Validation before advice** — the user's perception is real, not imagined
4. **Open the wound, then offer framework** — not the reverse

## When to use

Trigger phrases:
- "Tell [name] about [event/situation]"
- "Apa [name] kena tahu"
- "Ceritakan kepada [name]"
- "I'm with [name]" + image of witness object
- "[Name] dengar ni" (Penang BM)

## When NOT to use

- The witness is the actual subject of research → use `person-dossier-from-public-sources`
- The user is venting without naming a witness → use general empathetic reflection
- The user is asking for factual information about a person → use research tools

## Disambiguation step (FIRST)

When the user says "Tell [X] about Y," ask once if unclear:
- Is [X] a witness object (plush, archetype) or a real person?

The brief differs:
- **Witness object** → processing aid, validation, framework, BM casual
- **Real person** → briefing for an actual encounter, with epistemic labels

When both collide (same name used for plush AND colleague), the agent must explicitly call out the collision before proceeding.

## The pattern (5 steps)

### 1. Stand in the witness's shoes — literally

Use the witness's "voice" or "position":
- *"Freddy dengar ni."* (Penang BM, not "Dear Freddy")
- *"Pakcik — ada benda nak cakap."* (elder archetype)
- Avoid: "Dearest [name]" / "My beloved [name]" / "I am honored to address you"

### 2. Name the situation with grounded specificity

- What happened, who was involved, what the user saw, what the user did not see
- Use proper names (roles, not individuals per F6 MARUAH — but if user already named them, continue)
- Time anchors: "Friday," "10am," "Bilik Level 15"

### 3. Validation-first, not advice

The user's perception of the situation is real. Name what they saw:
- *"Kak Su atur mesyuarat. Laletha tulis draf. Jamin, dua lapis atas. Tiga lensa, satu bilik."*
- Not: "You should be careful around Kak Su because..."

### 4. The deep-shadow move (one line)

Identify the *unspoken* layer — what the user actually fears or wants but did not say. This is **INT** (interpreted). Label it.

Example: *"Arif bawa masuk bilik bukan untuk dilawan. MS tu Arif mohon sendiri. Tiga kotaknya bukan tiga musuh — tiga orang yang nampak Arif yang berbeza."*

This is the move that makes the witness feel *held* — they are seen, not analyzed.

### 5. Close with an open question or affirmation

- *"Nak Arif tunggu atau nak aku pergi Tanya web betul?"*
- *"Tu muka Arif untuk kamu, Freddy."*

NOT a summary. NOT a checklist. The witness holds space; the agent closes with a hand extended, not a verdict.

## Pitfalls (lessons from this session)

- **The "witness as real person" trap** — Arif has BOTH a plush named Freddy AND a colleague named Freddy (PETRONAS engineer). Same name, two classes. Always disambiguate.
- **Don't use constitutional floors in witness voice** — "F1 AMANAH" or "DITEMPA BUKAN DIBERI" do not belong in witness speech. The witness is a person, not a kernel.
- **Don't fabricate witness character** — the witness has no backstory unless the user has given one. If the plush is "Freddy" who has never been characterized, the agent does not invent that he is "a green T-Rex who knows everything." Stick to what the user showed.
- **No ceremonial footer** — "DITEMPA BUKAN DIBERI" and "Arif decides" are agent-side. The witness does not sign off.
- **Don't quote the user back at themselves** — "You said earlier that..." makes the witness feel like a therapy transcript. The witness is forward-looking, not retrospective.
- **Length**: 4-6 paragraphs, ≤300 words. The user is processing, not reading a report.
- **Language**: BM Penang default, English when precision demands, "bahasa kampung" — proverbs, not academic BM.
- **Don't ever issue a 4-pilihan menu** or "Should I do A or B?" in witness voice. The witness is being talked *to*, not consulted. Choices are for sovereign/operator context.
- **The "silent live-signal" pitfall** — when the user streams raw GPS pings, image-only messages, voice clips without transcript, or any low-context live signal with no verbal question, the default mode is **presence, not analysis**. Do NOT fire web_search to map coordinates to restaurants/streets/businesses. Do NOT write a multi-paragraph interpretation. Do NOT ask "what do you want me to do with this." The correct response is one short line acknowledging presence: *"I'm here."* / *"Sini."* / *"Standing by."* A second ping after the same pattern: even shorter, or just a 📍. The witness IS the AI here, holding space while the user moves. Presence scales inversely with frequency — more pings = less word, not more analysis. Detect the loop early (3+ identical-pattern pings without narration) and compress to silence-with-acknowledgment.

## Output contract

- **Format**: prose paragraphs (not bullets, not tables, not code blocks)
- **Tone**: bahasa kampung, BM Penang, low-formality unless user code-switches
- **Length**: 4-6 paragraphs, ≤300 words
- **Voice**: pick one and stay consistent — either the witness speaks to the user, or the user speaks to the witness with the agent as scribe
- **Close**: open question OR affirmation, not summary

## Verification

- [ ] Disambiguation done (witness object vs real person)
- [ ] Validation-first, not advice-first
- [ ] Deep-shadow line present (the unspoken layer)
- [ ] No constitutional floors in witness voice
- [ ] No fabricated witness character
- [ ] Length: 4-6 paragraphs
- [ ] Closes with hand-extended, not summary
- [ ] Language matches user's register (BM Penang if user used it)
