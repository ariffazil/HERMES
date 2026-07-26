# Social Intelligence From Group Chat — "Who Should I Meet"

When a user sends a group chat export and asks "who should I meet at this event" or "who's worth talking to," the analysis shifts from behavioral profiling to **strategic people identification**. This is social intelligence extraction — mapping the group's key players, connectors, and high-value contacts for the user's specific context.

## When This Applies
- User has a group chat export for an upcoming event (reunion, conference, meetup)
- User asks "who should I meet," "who's interesting," "who should I talk to"
- User is ambivalent about attending and needs a reason (specific people to connect with)
- User shares emotional vulnerability + chat + then asks for strategic input

## Extraction Pipeline

### Step 1: Identify Organizers & Key Roles
Search for named roles and committee positions:
```
AJK | committee | pres | president | bendahari | treasurer |
ketua | admin | urusetia | coordinator | logistik
```
These people are **social hubs** — they know everyone, they're busy, but a brief acknowledgment goes a long way.

### Step 2: Map Professional Backgrounds
Search for career/industry signals:
```
Dr | doctor | engineer | pensyarah | lecturer | lawyer |
accountant | CEO | founder | business | startup | professor |
PhD | usahawan | creative | media | artist
```
Also look for **room/silo groupings** (common in reunion chats — career talk panels, industry breakout rooms). These reveal who shares the user's professional language.

### Step 3: Identify Connectors & Energy Carriers
Look for people who:
- Added multiple members to the group
- Tag others by name frequently
- Share nostalgic content (old photos, memories)
- Use humor that gets reactions
- Post motivational/energizing content
- Are mentioned by others ("korang kena jumpa dia")

These are **social batteries** — they make a room feel alive. Connecting with them reduces the user's social load because they carry conversations.

### Step 4: Find Emotional Anchors
Search for people who:
- Share specific memories involving the user's era/class/homeroom
- Use nostalgic language ("zaman dulu2", "masa orientasi", "kenangan")
- Are mentioned in the context of shared experiences
- Express genuine excitement about reconnecting

These are **low-effort connection points** — shared history means no small talk needed.

### Step 5: Identify Strategic Value Matches
Cross-reference the user's background with group members:
- **Same industry** → professional shorthand, no explaining needed
- **Complementary industry** → interesting cross-pollination
- **Different world entirely** → fresh perspective, ego-free conversation
- **Celebrity/notable presence** → skip unless genuine connection exists

### Step 6: Build the Recommendation
Structure output as:

**🎯 Meet These People** — 3-5 people with specific reasons
**⚠️ Skip the Pressure** — celebrity hype, overtaxed organizers
**🛡️ Home Base** — which sub-group/room/silo the user belongs to as a starting point

For each recommended person:
- Name + role/occupation (from chat)
- WHY they're worth meeting (specific to the user's context)
- What to talk about (lowest-effort entry point)

## Pitfalls

### P1: Don't recommend everyone
The user asked WHO to meet, not a full attendee list. Pick 3-5 max. Quality over quantity. Each recommendation needs a specific reason tied to the user's context.

### P2: Don't recommend celebrities for ego
If there's a notable/celebrity presence in the group, don't recommend them unless there's a genuine connection angle. "Everyone wants a selfie" is not a reason.

### P3: Match recommendations to user's energy state
If the user is emotionally drained (expressed vulnerability, scars, ambivalence), recommend **low-effort connections** — people who share history, people who carry conversations, people in the user's industry. Don't recommend networking-heavy targets that require performative energy.

### P4: The "home base" concept
Always identify which sub-group/room/silo the user naturally belongs to. This is their safe starting point — walk in, find your people, breathe. The rest can happen organically.

### P5: Connectors > Contacts
A person who knows everyone and introduces freely is more valuable than a person with an impressive title but no social warmth. Prioritize social batteries over professional stars.

### P6: Don't dump raw data
The user wants insight, not a spreadsheet. Don't list every AJK member with phone numbers. Curate. Explain WHY each person matters for THIS user.

### P7: Respect the ambivalence → strategic shift
When a user goes from "I don't want to go" to "who should I meet," they've made the decision to attend. Don't revisit the ambivalence. Shift fully into strategic mode. The emotional work is done — now help them maximize the experience.

## Output Format

```markdown
**🎯 Meet These People:**

**1. [Name]** — [Role]. [One sentence about who they are from the chat]. [One sentence about why they matter for this user]. [Lowest-effort conversation starter].

**2. [Name]** — ...

**⚠️ Skip the Pressure:**
- **[Name]** — [why to skip]

**🛡️ Your Home Base:**
[Which sub-group the user belongs to. Where to start. What to do first.]
```

Keep it tight. 3-5 recommendations. Each with a specific reason. The user is about to walk into a room — give them a map, not a thesis.
