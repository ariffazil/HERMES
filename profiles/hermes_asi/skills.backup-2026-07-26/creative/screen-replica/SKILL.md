---
name: screen-replica
description: "Replicate a specific app screen or UI format as a visual HTML artifact, then screenshot it for delivery. When a user sends a screenshot and says 'format sama' / 'ikut format ni' / 'sebijik sama' — they want a VISUAL replica, not a text file."
tags: [html, css, screenshot, ui-replica, mobile-app, format, visual, trading, finance]
triggers:
  - "user sends a screenshot and asks for output in that format"
  - "format sama, ikut format, sebijik sama, macam ni, camni"
  - "user rejects a text/plain output saying it doesn't match"
  - "user provides an app screenshot and wants a document styled to match"
---

# Screen Replica

Replicate an app screen or document format as pixel-close HTML → screenshot → deliver as image.

## When This Skill Fires

- User sends a screenshot of an app (trading platform, bank app, receipt, etc.)
- User asks for output **in that format** — "format sama", "ikut format ni", "sebijik macam MT5"
- User rejects a plain text output saying "x sama" / "tak serupa"

## Critical Lesson

**"Format" means VISUAL, not textual.** When a user shows you an app screenshot and says "buat ikut format ni", they want a replica that *looks* like the app — same layout, colors, typography, spacing. A text/markdown file is NEVER the right answer.

## Workflow

### Step 1: Analyze the screenshot
- Identify the UI framework (mobile app, web app, document)
- Note: layout structure, color scheme, typography, spacing, element hierarchy
- Extract all data values the user wants included

### Step 2: Build HTML+CSS replica
- Fixed mobile width (390px for iPhone, 360px for Android)
- Match the visual style: fonts, colors, borders, spacing
- Use system fonts: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- For financial/trading apps: blue = profit/positive, red = loss/sell, black = neutral
- Replicate UI chrome (status bar, tabs, nav) for authenticity
- Inline all CSS — no external dependencies

### Step 3: Render to image
- `browser_navigate` to the HTML file
- `browser_vision` to screenshot
- Deliver via `MEDIA:` tag

### Step 4: Offer edits
- Ask if user wants changes (amounts, names, dates, details)
- Iterate on the HTML until satisfied

## Pitfalls

1. **Never start with a text file.** If the reference is a screenshot, the output is visual. Text is a fallback only if user explicitly asks for plain text.
2. **Don't approximate — match.** "Close enough" is not what the user wants. Match colors, layout, and typography as closely as possible.
3. **Browser rendering matters.** HTML that looks right in code may render differently. Always screenshot and verify before delivering.
4. **User photos may timeout on Telegram.** If a photo fails to download, ask user to retry or describe what they sent. Don't assume you know the format.
5. **Multiple screenshots may arrive.** The user might send the reference format and the data separately. Ask which is which if unclear.
6. **Financial data sensitivity.** Trading screenshots often contain real account data. Don't store or log actual financial figures beyond what's needed for the replica.

## Reference Implementations

See `references/mt5-trading-statement.md` for the MT5 mobile app replica pattern (XAUUSD trade history + withdrawal confirmation).

## Templates

- `templates/mt5-mobile-screen.html` — Reusable MT5 mobile app skeleton with correct colors, typography, layout. Copy and customize trade entries + summary values.
