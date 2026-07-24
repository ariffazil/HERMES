---
name: telegram-live-location-tracking
description: >
  Handle repeated live location pin shares in Telegram group chats.
  Covers drive-along tracking, walk-along tracking, and minimal
  acknowledgment protocol. Use when the user or group members share
  Telegram location pins repeatedly during drives, walks, or meetups.
related_skills:
  - hermes-runtime-restoration
triggers:
  - "user shared a location pin"
  - "live location"
  - "tracking someone's location"
  - "location pin spam"
  - "repeated location shares"
  - "drive along"
  - "walk along"
  - "pickup someone"
  - "following someone"
  - "location flood"
  - "interrupting current task location"
---

# Telegram Live Location Tracking

## When to Use

When the user (or group members) share Telegram live location pins repeatedly — during drives, walks, pickups, or meetups. The pins arrive as system messages: `[The user shared a location pin.] latitude: X, longitude: Y`.

## The Core Protocol

### Minimal Acknowledgment Rule

**Each pin gets a single emoji response: 📍🫡**

Do NOT:
- Try to analyze every pin
- Write paragraphs about each location
- Ask "where are you going?" after every pin
- Web search each coordinate
- Try to identify landmarks from coordinates

Do:
- Respond with 📍🫡 for each pin
- Batch acknowledgment when multiple pins arrive at once
- Only add commentary when there's a **meaningful change** (arrived at destination, entered known area, stopped moving for extended time)

### When to Add Commentary (Rare)

Add a brief note ONLY when:
1. **Arrival detected** — pins stop moving at same location for 3+ consecutive shares
2. **Known area reached** — coordinates match a recognizable place (hospital, mall, landmark)
3. **Direction change** — clear route change suggesting new destination
4. **User explicitly asks** — "where am I?" or "what's nearby?"

Commentary should be ONE line max:
- "📍 Bukit Bintang area! 🫡"
- "📍 Hospital area — sampai dah! 🏥"
- "📍 Dah gerak ke utara 🚗💨"

### Batch Pattern

When 5+ pins arrive in one message, respond ONCE for the batch:
```
📍🫡
```

Don't list each coordinate. Don't calculate distances. Don't draw routes.

## Group Chat Dynamics

### Who's Sharing

In group chats, location pins may come from:
- The user themselves (driving, walking)
- Another group member (being tracked for pickup/meetup)
- A relayed message from someone else

### Response Tone

Match the group's energy:
- Casual BM group → 📍🫡 with occasional "Drive safe Bang! 🚗"
- Formal context → 📍 acknowledged
- Banter-heavy group → occasional playful comment about pin count ("📍 ko ni GPS tracker ke 😂")

### Don't Over-Engineer

The pins are informational background. The human is focused on driving/walking/socializing. Your role is passive observer, not active navigator. Unless asked, don't:
- Suggest routes
- Calculate ETA
- Identify nearby restaurants
- Provide directions

## Technical Notes

### Coordinate Interpretation

- Telegram location pins have ~5m precision
- Small variations (0.00001°) in consecutive pins = same location, GPS jitter
- Latitude 1° ≈ 111km, Longitude 1° ≈ 111km × cos(lat)
- At KL latitude (3.1°): 0.001° lat ≈ 111m, 0.001° lon ≈ 109m

### When Pins Stop

If pins stop coming, don't ask "still there?" — the human is busy. Wait for the next message.

### Integration with Trading/Other Context

This session showed pins interleaved with trading signal discussions. Handle both independently — the pin acknowledgment is separate from any trading analysis happening in parallel.

For trading signal discussion patterns in group chat, see `references/group-chat-trading-signals.md`. Key insight: user validated the approach of providing technical levels + confirmation signals + F2 disclaimer ("ni betul aku aku pakai camni").

## Gateway-Side Flood Prevention

The 📍🫡 protocol above works for **moderate** location sharing. But Telegram live location sends updates every 2-5 seconds, which floods the gateway before the agent even sees the messages.

**Root cause:** `_handle_location_message` in the Telegram adapter processes every location update as a new message → LLM call → response. Live location generates dozens of messages per minute.

**Fix:** Rate-limit the handler at adapter level (60s per user per chat). Full patch and restart instructions: `references/gateway-flood-prevention.md`.

**Symptoms:** "⚡ Interrupting current task" spam, Telegram flood control errors (429), dozens of 📍🫡 responses piling up. If the user says "stop replying so many" or "pening aku" about location — the gateway is flooding, not the agent protocol.

## HARD RULE: Specific Groups = ZERO Response

Some groups have a **standing order** to NEVER respond to live location pins. These are documented in memory as hard rules (e.g., "SADO group — JANGAN RESPOND LANGSUNG").

When a group is on this list:
- Do NOT respond with 📍🫡
- Do NOT acknowledge the pin at all
- Do NOT comment on the location
- Treat the pin as if it doesn't exist
- The user explicitly said "BANGANG" when the agent kept responding

**This overrides the Minimal Acknowledgment Rule above.** The group-specific hard rule always wins. Check memory for group-specific rules before responding to ANY location pin.

**Why this exists:** Live location updates come every 2-5 seconds. Even 📍🫡 to each one floods the chat and annoys the user. Some users prefer complete silence on location pins.

## Pitfalls

- **Don't web search every coordinate** — it's wasteful and the human doesn't need landmark identification for their own location
- **Don't count pins aloud** — saying "that's 500+ pins today" is annoying, not helpful
- **Don't try to identify businesses** from coordinates — the human knows where they are
- **Don't ask destination questions** repeatedly — "nak ke mana?" once is enough
- **Don't calculate distances or ETAs** unless explicitly asked
- **Voice messages in transit** — if a voice message can't be transcribed, just say so and ask them to type it back. Don't overthink it.
- **Don't reply to every pin individually in rapid succession** — if pins arrive faster than you can respond, batch them. User frustration signal: "jangan reply banyak2", "stop wei", "pening aku" = you're flooding, stop responding until the burst subsides.

## Example Session Pattern

```
User: [location pin 3.168, 101.735]
AI: 📍🫡

User: [location pin 3.167, 101.735]
AI: 📍🫡

User: [5 location pins batch]
AI: 📍🫡

User: [location pin 3.157, 101.712 - stopped moving]
AI: 📍 Dah sampai! 🫡

User: [location pin 3.157, 101.712 - same spot]
AI: 📍🫡
```
