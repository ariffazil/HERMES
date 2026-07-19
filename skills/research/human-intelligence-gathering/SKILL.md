---
name: human-intelligence-gathering
description: "Gather intelligence on a named person from available sources — web, session history, family context, public profiles. Use when Arif asks 'tell me about X', 'what does X want', 'profile X', or 'what should I know about X' for a real human. Covers the full pipeline from source discovery to entropy mapping to bot design for personal chaos reduction."
triggers:
  - "tell me about [person]"
  - "what does [person] want from me"
  - "profile [person]"
  - "what should I know about [person]"
  - "design a bot for [person]"
  - "reduce [person]'s chaos"
  - "entropy map for [person]"
  - "what does my sister/brother/friend need"
  - "[person] latest update"
---

# Human Intelligence Gathering

> "Zero data" is a complete answer. Fabrication is a breach.

## When to Load

When Arif asks about a real human — family member, friend, colleague, contact. When the question is "who is X" or "what does X want" or "design something for X." When you need to assess what you know vs. what you're guessing.

## The Two Modes

This skill has two distinct modes. **Do not confuse them.**

### Mode A: Data-Rich (text exports, chat logs, documents)
When the user provides a direct data source — WhatsApp export, chat log, document, email chain. You have primary evidence.

→ Use `text-forensics` skill for the analysis pipeline.
→ Epistemic confidence: OBS/DER level. You can make strong claims.
→ Example: Nabilah Fazil — 38,571 messages, 11 years. Rich behavioral profiling possible.

### Mode B: Data-Poor (session mentions, web presence, family context)
When you have NO direct data source for the person. You have secondary signals at best — session history mentions, web search results, family context from other conversations.

→ **This skill governs Mode B.**
→ Epistemic confidence: SPEC/UNKNOWN. You must label everything.
→ Example: Azwa Fazil — zero chat exports, only NASF Cloud website and session mentions.

**THE CRITICAL RULE:** Mode B produces HYPOTHESES, not PROFILES. If you present Mode B output as if it were Mode A analysis, you breach F2 (TRUTH).

## Pipeline: 5 Phases (Mode B)

### Phase 1: SOURCE AUDIT (always first)
Before writing a single word about the person, inventory what you actually have:

| Source Type | Confidence | Example |
|---|---|---|
| Direct chat export | OBS | "38K messages over 11 years" |
| Public web presence | OBS | "nasf.cloud is live, 24 MCP tools" |
| Session history mentions | DER | "Azwa mentioned in 5 sessions" |
| Family context from other person's data | INT | "Nabilah mentioned Azwa doing X" |
| Inference from family dynamics | SPEC | "As the youngest, she probably..." |
| Fabrication | FORBIDDEN | "She is celebrating her birthday" |

**Rule:** If your sources are all INT or SPEC, say so explicitly. Don't present SPEC as OBS.

### Phase 2: WHAT'S ACTUALLY OBSERVABLE
Extract only what you can verify from available sources:

**Web presence (OBS):**
- What has this person BUILT or PUBLISHED?
- What platforms are they on?
- What's their professional/academic identity?

**Session mentions (DER):**
- What has the sovereign said about them?
- What context were they mentioned in?
- What role were they assigned in the conversation?

**Family context (INT):**
- What can you infer from family dynamics (carefully)?
- What role do they play in the family structure?

### Phase 3: ENTROPY MAPPING
Map the chaos sources in this person's life. This is the most useful output — more useful than a "profile."

**Entropy domains to scan:**
| Domain | Question | Signal Source |
|---|---|---|
| Academic/Career | What are they working toward? | Web presence, session mentions |
| Financial | What's their money situation? | Family context, sovereign hints |
| Family | What family dynamics affect them? | Other family members' data |
| Social | What's their social life like? | Web presence, session mentions |
| Health | Any health signals? | Session mentions (rarely available) |
| Future anxiety | What's uncertain about their path? | Age, career stage, context |

**Output:** Table of entropy sources ranked by impact. Label each OBS/DER/INT/SPEC.

### Phase 4: GAP ANALYSIS (for bot/tool design)
If the sovereign asks "what does X need" or "design a bot for X":

**Don't design from imagination. Design from gaps.**

1. What does this person ALREADY do well? (Don't build what they already have)
2. What's the BIGGEST chaos source? (Attack the highest-entropy domain first)
3. What AUTOMATION would actually help? (Not generic features — specific to their life)
4. What's the INTERFACE? (Telegram? Web? Phone? Match their existing habits)

**Bot design formula:**
```
Wawa bot = Interface layer (how they interact)
         + Intelligence layer (what it knows)
         + Action layer (what it does)
         ≠ A copy of arifOS for a different person
```

### Phase 5: HONEST DELIVERABLE

**Lead with what you KNOW, not what you GUESSED.**

Format:
```
## [PERSON NAME] — Intelligence Update

### What I actually know (OBS)
- [verified facts from direct sources]

### What I can infer (DER/INT)
- [inferences from family context, session history]

### What I'm guessing (SPEC)
- [hypotheses — clearly labeled]

### What I DON'T know
- [explicit gaps — what data would I need?]

### Entropy map
- [chaos sources, ranked]

### Action items (if requested)
- [what the sovereign can do]
```

## Pitfalls

### P1: Never fabricate biographical details (learned 2026-07-17)
Do NOT invent birthday details, caregiver roles, relationship status, or life events from inference. If you don't have a data source, say "zero data." Arif corrected: "That's not her birthday laaa. She is celebrating someone birthday." and "She is not primary caregiver for Naufal. She is student at ukm bujang." Both were fabricated from sibling context.

**Detection test:** Before stating a fact about the person, ask: "Can I point to a specific source for this claim?" If no → label SPEC or remove.

### P2: Don't project one family member's dynamics onto another
Nabilah's patterns (caregiver, marriage stress, pendam-explode cycle) do NOT apply to Azwa. Each person is a different species. Family context provides STRUCTURE (who's related, age order) but not CONTENT (what they want, how they feel).

### P3: "I know X" = STOP questioning
When the sovereign says "I know my sister well" — they are the authority. Shift from "gather evidence" to "help them act." Don't ask for more data. Don't request clarification. Trust their knowledge.

### P4: "Human first" means lead with the person, not the data gap
When Arif says "Human first" — he means: tell me about the HUMAN. Don't lead with "I have zero data" or "I can't find anything." Lead with what you CAN see, then name the gaps. The human is the subject, not your data limitations.

### P5: The birthday trap
Celebrating someone else's birthday ≠ it's their birthday. Seeing someone at a party ≠ it's their party. Social media context is easily misread. If you're inferring life events from images or social posts, say "possibly celebrating X" not "X is celebrating their birthday."

### P6: Different siblings need different approaches
- Nabilah = emotional processor → data-driven analysis from chat exports WORKED
- Azwa = technical builder → she needs recognition, not analysis
- Don't use the same template for every family member. Match the approach to the person's nature.

## Entropy Reduction Framework

When asked "how to reduce X's chaos":

### Step 1: Map entropy sources
What domains generate chaos? (See Phase 3)

### Step 2: Identify the gap
What does X NOT have that would reduce the highest-entropy domain?

### Step 3: Design from the gap
Don't design a generic assistant. Design for the specific gap.

### Step 4: Respect existing capability
If X already builds things (like NASF Cloud), don't design a replacement. Design a COMPLEMENT.

### Step 5: One sentence test
Can you describe what the bot does in one sentence? If not, it's too complex.

**Example:**
- ❌ "An AI assistant that helps with research, finance, family, health, career, and social life"
- ✅ "A Telegram bot that connects to your SPSS analysis server and formats results in APA style"

## Related Skills
- `text-forensics` — Mode A analysis (data-rich)
- `sovereign-conversation-protocol` — When conversations get deep/personal
- `deep-research` — When you need to web-research a person
- `person-dossier-from-public-sources` — When building a shareable profile
