# Public Figure Social Media Scan

Proven pattern for scanning a public figure's X (Twitter) and Threads presence, then synthesizing into a structured reflection. Born from Ray Dalio scan (2026-07-12).

## When to Use

- "Scan [person]'s X and Threads"
- "What's [person] saying lately"
- "Full reflection on [person]'s recent output"
- "Research [public figure]'s current thinking"

## Workflow

### Phase 1: Parallel Discovery (3 batches)

```
# Batch 1: Platform presence
web_search("[person] latest posts X Twitter 2025 2026")
web_search("[person] Threads threads.com recent 2025 2026")

# Batch 2: Thematic depth
web_search("[person] [key topic 1] 2025 2026")
web_search("[person] [key topic 2] interview")

# Batch 3: Media coverage
web_search("[person] [recent claim/viral post]")
web_search("[person] book/article/project 2025 2026")
```

### Phase 2: Extract Profiles + Key Posts

```
# Profiles (expect partial data — see pitfalls)
web_extract(["https://x.com/[handle]", "https://www.threads.com/@[handle]"])

# Specific post URLs (from search results)
web_extract(["https://x.com/[handle]/status/[id]", ...])

# Richest articles (Fortune, HBR, Bloomberg extract well)
web_extract(["https://fortune.com/[article]", ...])
```

### Phase 3: Targeted Deep Dive

If initial extraction is thin, search for specific post IDs or article titles, then extract those URLs directly.

### Phase 4: Synthesize

Structure output as:

1. **Identity** — who they are, current state, motivation
2. **X/Twitter** — the big themes, with post dates, view counts, key quotes
3. **Threads** — the different voice (if applicable), engagement contrast
4. **The Pattern** — what connects all their output into one unified message
5. **So What** — how this maps to the user's context (arifOS, work, etc.)
6. **Honest Assessment** — what they get right AND what they don't address

## Platform-Specific Extraction Limits

| Platform | What You Get | What You Don't |
|----------|-------------|----------------|
| **X profile** (`x.com/handle`) | Bio, pinned post, 2-3 visible posts | Login wall cuts off most content |
| **X specific post** (`x.com/handle/status/ID`) | Full post text, date, view count, article preview | Replies, engagement breakdown |
| **Threads profile** (`threads.com/@handle`) | Bio, 5-6 recent posts | "Log in to see more" cuts off |
| **Threads specific post** | Full post text, engagement counts | Sometimes returns empty (JS-heavy) |
| **Fortune/Bloomberg/HBR** | Full article text, clean extraction | Paywalled Bloomberg sometimes blocks |
| **Yahoo Finance** | Article text but heavy nav noise | Messy extraction, needs filtering |
| **YouTube** | Transcript (if youtube-content skill loaded) | No transcript without skill |

## Pitfalls

- **X profile pages are login-gated.** `web_extract` on `x.com/handle` returns only bio + pinned/visible posts (3-4 max). Always search for specific post URLs to get actual content. The `xurl` CLI can read posts by ID if authenticated.
- **Threads profiles show ~5-6 posts then gate.** Don't rely on profile page alone. Search for specific post URLs.
- **Threads post URLs sometimes extract empty.** JS-heavy rendering. Fall back to what the profile page showed, or use `browser_navigate` + `browser_snapshot`.
- **Don't use xurl CLI for read-only scans unless auth is confirmed.** `xurl auth status` must show valid OAuth2. If not, web_search + web_extract is sufficient for public figure scanning.
- **Publication articles are the richest source.** Fortune, HBR, Bloomberg articles extract cleanly and contain the substance. Social posts are the headlines; articles are the thesis.
- **View counts on X posts signal impact.** 80M views vs 200K views tells you what resonated. Include in synthesis.
- **Engagement contrast between platforms reveals audience.** Dalio: 80M views on X (macro alarm), 73 likes on Threads (governance philosophy). The platform audience shapes the message.

## Output Quality Signals

- Lead with the person's **current state** (prophet mode? defensive? promoting?)
- Use **tables** for platform comparison and theme mapping
- Tag evidence class: OBS (verified post/date/number), INT (pattern interpretation), SPEC (your read on motivation)
- End with **"So What"** mapped to the user's context — this is where the value is
