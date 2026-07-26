---
name: visual-format-replication
description: "Pixel-perfect visual replicas from screenshots — match exact colors, fonts, spacing, layout."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [visual, replication, screenshot, html, clone, format, match, pixel-perfect, interface]
    related_skills: [sketch, claude-design, popular-web-designs, document-intelligence]
---

# Visual Format Replication

When a user shows a screenshot and says "format sama", "sebijik sama", "same format", "ikut format" — they want a **pixel-perfect visual replica**, NOT a text file or approximation.

## When to use this

- User sends a screenshot of an app/document and wants something that looks identical
- User corrects text output saying "x sama" (not the same) — they mean visually
- User says "ikut format" (follow the format) with a reference image
- User says "sebijik sama" (exactly the same) about an interface

## When NOT to use this

- User wants a new design direction → use `sketch`
- User wants a polished one-off artifact → use `claude-design`
- User wants a document (PDF, spreadsheet) → use `document-intelligence` or `nano-pdf`
- User wants a diagram → use `excalidraw` or `architecture-diagram`

## Core method

```
analyze source → extract exact specs → build HTML → verify visually → deliver image
```

### 1. Analyze the source screenshot FIRST

Use `vision_analyze` on the source image to extract:
- **Exact hex colors** for every element (text, backgrounds, accents, borders)
- **Font sizes** and weights (regular 400, semibold 600, bold 700)
- **Spacing** (padding, margins, row heights)
- **Layout structure** (flex direction, alignment, borders between rows)
- **Element positioning** (headers, tabs, content, footers)

**Do NOT guess colors.** Extract them from the image. Guessing leads to 3+ correction rounds.

### 2. Build HTML matching exactly

- Use the exact hex codes from step 1
- Match font sizes, weights, and families precisely
- Replicate spacing and padding exactly
- Keep the same layout structure (flex, grid, positioning)
- Use system fonts that match the source (e.g., `-apple-system` for iOS apps)
- Single self-contained HTML file with inline `<style>`

### 3. Verify visually

Open in browser and use `browser_vision` to confirm match:
```
browser_navigate(url="file:///path/to/replica.html")
browser_vision(question="Does this match the source? Check colors, fonts, spacing.")
```

### 4. Deliver as image

- Screenshot the HTML via `browser_vision`
- Send via `MEDIA:/path/to/screenshot.png`
- Do NOT send HTML files or text files — users want the visual result

### 5. Iterate on feedback

If user says colors/format don't match:
- Re-analyze the source with `vision_analyze` — be more specific in your question
- Common mistakes:
  - Using iOS blue (#007AFF) when app uses a different blue (#2962FF)
  - Using iOS red (#FF3B30) when app uses material red (#E53935)
  - Wrong font weights (400 vs 600)
  - Missing subtle borders or background colors
  - Adding extra sections the user didn't ask for

## Reference palettes

### MetaTrader 5 (MT5) mobile
| Element | Hex |
|---------|-----|
| Buy / positive | #2962FF |
| Sell / negative | #E53935 |
| Text primary | #212121 |
| Text secondary | #757575 |
| Borders / separators | #F5F5F5 |
| Background | #FFFFFF |
| Active tab bg | #F5F5F5 |
| Inactive tab text | #757575 |
| Bottom nav inactive | #9E9E9E |
| Bottom nav active | #2962FF |
| Bottom nav active bg | #E3F2FD |

### iOS default
| Element | Hex |
|---------|-----|
| System blue | #007AFF |
| System red | #FF3B30 |
| System green | #34C759 |
| Label | #000000 |
| Secondary label | #8E8E93 |
| Separator | #C6C6C8 |
| Grouped background | #F2F2F7 |

## Anti-patterns

- **Sending text files** when user wants visual output
- **Approximating colors** instead of extracting exact hex codes
- **Skipping vision_analyze** on the source — guessing causes frustration
- **Sending HTML source** — screenshot it and send the image
- **Adding extras** the user didn't show — keep to exactly what they asked
- **Using wrong color palette** — always verify which app/system the source is from

## Tool sequence

```
vision_analyze(source_screenshot, "extract exact hex colors, fonts, spacing, layout")
  → write_file(/root/replica.html)
  → browser_navigate(file:///root/replica.html)
  → browser_vision("does this match the source screenshot exactly?")
  → MEDIA:/path/to/screenshot.png
```
