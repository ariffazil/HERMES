---
name: text-forensics
description: "Analyze large exported chat/text files to extract behavioral profiles, life timelines, emotional signatures, and relationship dynamics. Use when user sends a WhatsApp/Telegram/iMessage export, large chat log, or any longitudinal personal text corpus and wants to understand WHO the person is, WHAT patterns exist, and WHAT the data reveals."
triggers:
  - user sends a large chat export file
  - analyze this chat for patterns
  - what does this conversation tell you
  - profile this person from chat data
  - review my chat with someone
  - large text file with date-stamped messages from multiple senders
  - who should I meet at this event
  - who's interesting in this group
  - identify key people from this chat
---

# Text Forensics — Longitudinal Chat/Text Behavioral Analysis

## When to Load
- User sends a WhatsApp/Telegram/iMessage chat export
- User asks for behavioral profiling from conversation data
- Any large text corpus with timestamped multi-sender messages

## Pipeline: 5 Phases

### Phase 1: STRUCTURAL PARSE (always first)
Parse the chat file into structured messages. Do NOT read line-by-line manually — use code.

**WhatsApp regex pattern:**
```python
re.match(r"(\d+/\d+/\d+),\s+(\d+:\d+\s+[AP]M)\s+-\s+([^:]+):\s+(.*)", line)
```

**Key metrics to extract immediately:**
- Total messages, per-sender counts
- Date range (first → last message)
- Messages per year (temporal density)
- Active vs silent periods

**Execution pattern:** Use `execute_code` with `write_file` to create a parse script, then `terminal` to run it. Batch reads are unreliable for 30K+ line files — always write script to disk first.

### Phase 2: KEYWORD FREQUENCY ANALYSIS
Extract topic clusters by frequency. Group keywords into semantic categories:
- **People:** names of family, friends, partners
- **Life events:** marriage, divorce, birth, death, career changes
- **Emotions:** love, fear, anger, sadness, gratitude
- **Practical:** money, housing, work, health, legal

Output: topic frequency table + sample messages per topic.

### Phase 3: CHRONOLOGICAL LIFE TIMELINE
Extract dated messages matching life-event keywords. Output as timeline:
```
[date] event description (message excerpt)
```

**Critical: extract BOTH sides of conversations around key events.** Context from the other party reveals relationship dynamics.

### Phase 4: BEHAVIORAL PATTERN RECOGNITION
Look for these patterns across the full timeline:

1. **Repetition patterns** — Does the person repeat the same phrase/behavior? (e.g., chronic "sorry", recurring "takut")
2. **Pendam-explode cycle** — Bottling → bottling → eruption → burn bridge → cool down → reconnect
3. **Role assignment** — Is this person the invisible caretaker? The crisis manager? The emotional dumping ground?
4. **Dependency signals** — Who does this person lean on? What happens when that person is unavailable?
5. **Agency markers** — When does this person make independent decisions vs. seek approval?
6. **Language shifts** — Code-switching (BM↔English), formality changes, emoji density — all signal emotional state
7. **Silence patterns** — What topics get one-word answers? What gets long paragraphs? What gets ignored?

### Phase 5: STRUCTURED DELIVERABLE
Output shape (adapt to context):

**Tier 1: Fakta Keras** — Dates, names, events, timeline. OBS-level.
**Tier 2: Yang Tersembunyi** — Things the person said but the reader likely missed. DER-level.
**Tier 3: Pattern Recognition** — Behavioral loops, recurring dynamics. INT-level.
**Tier 4: Luka (Trauma Layers)** — Ordered by depth. Be specific — cite messages.
**Tier 5: Kekuatan** — What the person does well. Honest, not flattery.
**Tier 6: Nasihat/Wisdom** — Raw, direct, grounded in the data. Not generic self-help.

## Group Chat Variant
For group chats (reunion planning, family events, team outings), see `references/group-chat-event-read.md` for a lighter quick-read pipeline focused on event context and attendance signals rather than deep behavioral profiling.

## Reunion Chat Variant
For reunion-specific dynamics (nostalgia floods, identity confusion, "aib" photo bonding, attendance ambivalence), see `references/reunion-chat-variant.md`. Covers low-signal presence mode when the user shares images/location without narration during emotional processing.

## Social Intelligence Variant ("Who Should I Meet")
When the user sends a group chat and asks who to meet at the event — or shifts from ambivalence to strategic planning — see `references/social-intelligence-from-chat.md`. Covers: key role extraction, professional background mapping, connector/energy-carrier identification, emotional anchor finding, and curated 3-5 person recommendation output with "home base" starting point.

## Pitfalls

### P1: Don't sanitize the analysis
The user sent you 38K messages because they want REAL insight. Don't soften trauma findings. Don't euphemize. Don't say "challenging circumstances" when you mean "financial abuse pattern." The RASA rule applies — speak like a person, not a risk assessment.

### P2: Don't confuse volume for importance
A person who sends 500 "sorry" messages reveals more than someone who sends 5000 normal messages. Frequency of specific emotional words > total message count.

### P3: Both sides matter
Analyzing only one sender's messages gives a distorted picture. Always parse BOTH sides. The response pattern (or non-response) reveals as much as the message itself.

### P4: Code-switching is signal
BM-English mixing patterns reveal emotional state, audience, and comfort level. Formal BM = distance. Casual BM + English = trust. Pure English = professional context or emotional walls.

### P5: The deliverable is the insight, not the data
Don't dump raw message counts and call it analysis. The user wants to UNDERSTAND someone. Lead with the insight, support with the data.

### P6: Handle "edited" and "deleted" messages
WhatsApp marks edited messages with `<This message was edited>` and deleted with `This message was deleted`. These are signal — edited messages often represent second thoughts or face-saving. Deleted messages around sensitive topics are especially noteworthy.

### P7: Media omitted is not nothing
`<Media omitted>` means the user didn't include the media. But the CONTEXT around media messages often reveals what was sent. Don't ignore these lines — the surrounding text is still data.

### P8: Don't apply chat-forensics to someone you have NO data on (learned 2026-07-17)
This skill works on EXISTING chat exports. Do NOT apply the same profiling approach to a family member or person you don't have direct data for. Failure mode: Arif asked about Azwa (sister, UKM student). Agent had no chat export for Azwa — but inferred birthday details, caregiver roles, and family dynamics from Nabilah's chat data and session mentions. All wrong. The Nabilah analysis was accepted because it was DATA-DRIVEN (38K messages). The Azwa analysis was rejected because it was INFERENCE-DRIVEN (zero messages).
**Rule:** If you don't have a chat export or direct data source for a person, say "zero data" and stop. Don't extrapolate from sibling context, family patterns, or session mentions. The sovereign knows their family better than you do.

### P9: Forwarded messages are someone else's voice
Long blocks of text that are clearly forwarded (political posts, religious content, news articles) reveal what the person CONSUMES and VALUES, even if they didn't write it. Note the topics.

## Python Parse Template

Write this to `/tmp/chat_parse.py` and run via `terminal`:

```python
import re
from collections import Counter

FILE_PATH = "/path/to/chat.txt"  # Update

with open(FILE_PATH, "r", errors="replace") as f:
    lines = f.readlines()

messages = []
current_msg = None
for line in lines:
    line = line.strip()
    match = re.match(r"(\d+/\d+/\d+),\s+(\d+:\d+\s+[AP]M)\s+-\s+([^:]+):\s+(.*)", line)
    if match:
        if current_msg:
            messages.append(current_msg)
        current_msg = {"date": match.group(1), "time": match.group(2),
                       "sender": match.group(3).strip(), "text": match.group(4).strip()}
    elif current_msg and line:
        current_msg["text"] += " " + line
if current_msg:
    messages.append(current_msg)

print(f"Total parsed: {len(messages)}")
sender_counts = Counter(m["sender"] for m in messages)
for s, c in sender_counts.most_common():
    print(f"  {s}: {c}")

dates = [m["date"] for m in messages]
print(f"Range: {dates[0]} to {dates[-1]}")

year_counts = Counter()
for d in dates:
    parts = d.split("/")
    if len(parts) == 3:
        y = parts[2]
        if len(y) == 2: y = "20" + y
        year_counts[y] += 1
for y in sorted(year_counts.keys()):
    print(f"  {y}: {year_counts[y]}")
```

## Keyword Extraction Template

```python
# After parsing, run keyword analysis
keywords = {
    "category_name": ["keyword1", "keyword2"],
}

for msg in target_sender_msgs:
    for kw, cat in keywords.items():
        if kw.lower() in msg["text"].lower():
            topic_counts.setdefault(cat, 0)
            topic_counts[cat] += 1
```

## Deliverable Formatting

- Use BM casual for emotional content, English for structural/analytical
- Use numbered tiers (Fakta → Pattern → Trauma → Kekuatan → Nasihat)
- Cite specific dates and message excerpts as evidence
- Be raw in nasihat — the user wants real wisdom, not platitudes
- If the user asks for nasihat FOR the person being analyzed, write it as if speaking to them directly
- Tag epistemic levels: what's OBS (direct quote), what's DER (inferred from patterns), what's INT (interpreted), what's SPEC (speculation)
