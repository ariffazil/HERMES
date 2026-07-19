# Group Chat Event Read — Quick Context Extraction

When user sends a WhatsApp group chat export (not a 1-on-1 conversation), the analysis goals shift from behavioral profiling to **situational awareness**. The user is often a participant in the group, emotionally connected to the content, and processing their own feelings about an upcoming or recent event.

## When This Applies
- User sends a group chat export (reunion, wedding planning, family event, team outing)
- User shares emotional context alongside the chat ("I kinda feel not going", "why am I nervous")
- The chat has a clear EVENT with date, attendance, logistics

## Quick-Read Pipeline (before full text-forensics)

### Step 1: Structural Triage
1. **Read the FIRST 20 lines** → identify group name, creator, formation date, initial purpose
2. **Read the LAST 30 lines** → current state, most recent messages, event status
3. **Count total lines** → gauge conversation span

### Step 2: Event Detection
Search for these keywords to identify the core event:
```
reunion | gathering | meetup | majlis | jemput | hadir | event | 
hari ni | malam ni | tarikh | lokasi | restoran | hotel | 
bayaran | tiket | RSVP | confirm | attendance
```

### Step 3: Attendance Signal Extraction
Search for refusal/acceptance patterns:
```
tak datang | tak dapat | tak hadir | tak pi | tak join | 
sorry | maaf | tak boleh | can't make | confirm | onz | 
jom | akan datang | will be there
```

### Step 4: Emotional Context Mapping
When the user shares feelings alongside the chat:
- **Don't analyze the user** — reflect what the chat reveals
- **Name the event and its significance** (e.g., "20-year school reunion")
- **Show the attendance reality** (who's going, who's not, common reasons)
- **Connect to the user's stated emotion** without over-interpreting
- **Don't push attendance** — respect ambivalence while offering perspective

### Step 5: Grounded Response
Lead with: what is this event + what does the chat show about it.
Then: acknowledge the user's emotional state with specifics from the chat.
End with: one honest question or observation. Not a motivational speech.

## Pitfalls

### P1: Don't treat group chats like 1-on-1 forensics
Group chats are about the EVENT and GROUP DYNAMICS, not one person's behavioral profile. Focus on the collective context.

### P2: The user is IN the chat
Unlike analyzing someone else's conversation, the user is a participant. They can see everything you see. Your job is to SYNTHESIZE and REFLECT, not to reveal hidden data.

### P3: Read start AND end, not just start
The beginning gives context (group formation, initial purpose). The end gives CURRENT STATE (event happening now, recent attendance, last-minute changes). Both are essential.

### P4: Don't over-interpret emotional vulnerability
When a user says "I kinda feel not going" alongside a reunion chat, the connection is obvious. Don't pathologize it. Don't turn it into a therapy session. Acknowledge, reflect, offer one grounded observation.

### P5: Media omitted still tells a story
Group chats are heavy on `<Media omitted>`. The TEXT around media messages (comments, reactions, "wah cantik!", "jom tengok") reveals what was shared. Use surrounding context to infer content type.

### P6: Anonymous numbers are normal
WhatsApp exports show phone numbers, not names, for contacts not saved. Don't flag this as unusual. Focus on named contacts and the user's own messages.
