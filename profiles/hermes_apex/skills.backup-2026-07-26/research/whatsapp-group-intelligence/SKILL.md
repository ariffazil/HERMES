---
name: whatsapp-group-intelligence
description: Analyze exported WhatsApp group chats to extract key people, power structures, event details, and social dynamics. Use when the user shares a .zip or .txt WhatsApp chat export and needs to understand who's who, who to meet, or whether to attend an event. Combines structural analysis (roles, activity, mentions) with emotional intelligence (identity gaps, institutional pressure, social anxiety).
triggers:
  - "whatsapp chat export"
  - "group chat analysis"
  - "who should I meet"
  - "reunion attendee analysis"
  - "event decision support"
---

# WhatsApp Group Intelligence

Analyze exported WhatsApp group chats to extract actionable social intelligence.

## When to Use

- User shares a WhatsApp chat export (.zip or .txt)
- User asks "who should I meet" at an event
- User is deciding whether to attend a gathering
- User needs a reply drafted for a specific person in the group

## Step-by-Step Protocol

### 1. Extract & Structure

- Unzip if needed. Typical exports: `.txt` chat log + `.vcf` contacts
- Identify group name, creation date, creator
- Count total messages, date range, active participants

### 2. Map the Power Structure

Extract from the chat:
- **Admins/Creators** — who created the group, who has admin
- **AJK/Committee** — formal roles (president, treasurer, logistics, etc.)
- **Connectors** — people who add others, tag people, bridge subgroups
- **Anchors** — most active, highest message count, keep the group alive
- **Lurkers** — added but rarely/never spoke

### 3. Profile Key Individuals

For each named person, extract:
- **Name** (from WhatsApp display name or mentions)
- **Phone** (if visible)
- **Role** in group (admin, AJK, connector, anchor)
- **Profession/industry** (if mentioned in chat)
- **Personality signals** — humor style, leadership energy, warmth
- **Notable quotes** — anything that reveals character

### 4. Match to User's World

Cross-reference identified people against the user's:
- **Industry** (e.g., petroleum engineering, AI, geoscience)
- **Background** (e.g., same university, same hometown)
- **Interests** (e.g., tech, business, creative)
- **Emotional needs** (e.g., needs warmth, needs professional peers, needs someone who remembers the old days)

Produce a ranked list: who to meet first, who to avoid, who's the safe entry point.

### 5. Event Context

From the chat, extract:
- Event date, venue, time
- Attendance numbers (paid/confirmed vs total group)
- Dress code, program flow, special activities
- Last-minute updates or changes

### 6. Emotional Intelligence Layer

Read between the lines:
- **Identity gap** — is the user carrying weight (institutional, personal) that the group doesn't know about?
- **Social anxiety signals** — "I kinda feel not going" = needs permission, not persuasion
- **Institutional pressure** — MSS, rightsizing, career uncertainty = walking into "so kerja mana?" is a minefield
- **Introvert protection** — user may need a safe entry point, not a full social agenda

### 7. Reply Drafting

When asked "what to reply to X":
- Match tone to the person's energy in the chat (casual, warm, formal)
- Keep it short — no over-explaining, no excuses
- Preserve the relationship bridge for future
- Suggest 2-3 options: warm, minimal, and one with light humor

## Output Format

```
## Group Summary
- Group name, date range, message count
- Total participants, active vs lurkers

## Power Structure
- Creator, admins, AJK roles
- Top 5 anchors by activity

## People to Meet (ranked for user)
1. **Name** — role, why they matter for THIS user
2. ...

## People to Skip
- Name — reason

## Event Details
- Date, venue, program

## Emotional Read
- What the user is really feeling
- What they need to hear (honest, not motivational)
- Safe entry strategy
```

## Pitfalls

- **Don't assume professions** from phone numbers. Only label what the chat explicitly states.
- **Don't over-analyze lurkers.** They might just be private, not disinterested.
- **Don't push attendance.** If the user decides not to go, respect it. The analysis still has value for future events.
- **Privacy awareness.** Phone numbers and names are sensitive. Don't store them beyond the session context.
- **Don't web-search participants.** The chat export is the source. External lookup crosses a privacy line.
- **BM/English mix.** Malaysian WhatsApp chats are typically BM-English code-switched. Parse both.
