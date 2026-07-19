---
name: dark-explanatory-diagrams
description: "Dark-themed HTML+SVG visual guides for non-tech subjects — anatomy, biology, timelines, recovery journeys, process flows, laws/rules, and educational explanations. Sibling to architecture-diagram; same dark grid aesthetic but extended for explanatory/educational content."
version: 1.0.0
author: arifOS
license: MIT
metadata:
  hermes:
    tags: [diagrams, SVG, HTML, education, visualization, anatomy, timelines, biology, recovery, processes]
    related: [architecture-diagram, excalidraw, manim-video]
---

# Dark Explanatory Diagrams — Skill

## When to Use

Trigger when the user asks to **"lukis"** / **"gambar"** / **"draw"** / **"visualize"** / **"explain visually"** a concept that is:

- **Anatomical / biological** — body parts, surgical procedures, anatomical comparisons (e.g. ACL pre/post-surgery)
- **Temporal / processual** — recovery timelines, project phases, decision journeys, evolution steps
- **Conceptual / educational** — laws, principles, do/don't, classification systems
- **Comparative** — before/after, healthy/damaged, option A vs option B
- **Mathematical / scientific** — formulas, derivations, scientific phenomena (NOT animations)

Output: **single dark-themed HTML file with inline SVG** — no external libs, no rendering engine, opens in any browser, sent to user via `MEDIA:/absolute/path`.

## When NOT to Use

| Subject | Use instead |
|---|---|
| Software/cloud/infra architecture | `architecture-diagram` (has dedicated tech component types) |
| Hand-drawn whiteboard sketches | `excalidraw` |
| Math/algorithm animations (3Blue1Brown-style) | `manim-video` |
| Quick inline diagrams in chat | Direct SVG in markdown (no skill needed) |
| PowerPoint-style slides | `powerpoint` |
| Heavy reports / PDF docs | `scientific-pdf-generation` or `nano-pdf` |

## Design System

### Background & Surface
- Page bg: `#020617` (slate-950)
- Grid pattern: 40px squares, stroke `#1e293b` width 0.5
- Card surface: `#0f172a` (slate-900), border `#1e293b` radius 8px, padding 20px
- Header bar: pulsing dot (10px circle, glow, 2s pulse anim) + 18px bold title
- Subtitle: 10px slate-400, margin-bottom 24px

### Typography
- Font: **JetBrains Mono** (Google Fonts)
- H1 (page): 18px bold
- H2 (section): 14px bold
- H3 (card): 12px slate-300
- Body: 11-12px slate-300
- Caption: 8-9px slate-400
- Annotation: 7-8px (use sparingly)

### Color Palette (semantic, NOT by element type)

| Meaning | Color (hex) | Typical use |
|---|---|---|
| Healthy / normal / proceed / anatomy baseline | `#22d3ee` (cyan-400) | Intact bones, healthy state, "BUAT" |
| Replacement / graft / success / proceed | `#34d399` (emerald-400) | New tissue, healthy growth, OK actions |
| Damaged / rupture / danger / warning | `#fb7185` (rose-400) | Rupture, infected, "JANGAN", red flags |
| Caution / transition / hardware / mid-recovery | `#fbbf24` (amber-400) | Surgical screws, phase 2, warning states |
| Highlight / signature / key milestone | `#a78bfa` (violet-400) | Final return phase, signature quote |
| Neutral / context / secondary | `#94a3b8` (slate-400) | Background anatomy, contextual labels |

Card fills use `rgba(R,G,B,0.15-0.4)` + 1.5px stroke in full hex color. Arrow markers in SVG use the same hex as the path.

## 4 Canonical Patterns

### Pattern 1: Side-by-Side Anatomy (Before/After)

For: surgical procedures, comparative anatomy, healthy/damaged states.

Structure:
- Two-column SVG with vertical divider at midpoint (dashed slate)
- Mid-divider label: arrow text showing the transformation (e.g. "RUPTURE → GRAFT")
- Each side: labeled parts using the semantic palette
  - Bones/tissues = cyan
  - Healthy ligaments/organs = emerald
  - Damaged parts = rose (with rupture symbol: `M x y L x y` cross + circle)
  - Hardware (screws, implants) = amber circles
  - Harvest site = rose dashed box with arrow to destination
- Color-coded legend row below SVG using 12px swatches

ViewBox: minimum 800x480. For one anatomy, 400x480 works.

### Pattern 2: Timeline with Phases

For: recovery journeys, project phases, multi-step processes, evolution.

Structure:
- SVG viewBox 800x360
- Main horizontal timeline at y≈80 (stroke #1e293b width 2)
- Milestone circles: 5-7px radius, color-coded by phase (red → amber → emerald → cyan → violet)
- Labels: timestamp (e.g. "W0", "W6") 9-12px above/below
- Sub-labels (e.g. "HARI 1", "FONDASI") 8-9px below timestamps
- Phase zone rectangles below timeline (y 135-185): rgba fill + 1px stroke + 9px bold title + 8px sub-detail (2 lines max)
- Detail bullet rows below zones (y 215-280): 5 items per phase in 8-9px
- Optional: secondary metric curve at y≈320 (e.g. risk timeline)
- "You are here" marker: dashed vertical line + small badge with arrow

### Pattern 3: Multi-Card Grid (Do/Don't, Laws, Options)

For: action lists, do/don't comparisons, principle collections, classifications.

Structure:
- 2-column grid (`grid-template-columns: 1fr 1fr`) for do/don't
- 3-5 column grid for laws/principles
- Each card: 1px border `#1e293b`, radius 6px, padding 12px, centered content
- 24px bold number/icon at top
- 10px bold title below
- 9px description (2-3 lines max)
- Color dot in card-header indicates category

### Pattern 4: Signature Quote Card

For: 1-sentence takeaway, core message, principle distillation.

Structure:
- Card with gradient background (e.g. `linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)`)
- Centered text 14-16px bold, color violet-300 (`#c4b5fd`)
- Use sparingly — once per document max

## File Structure

Single HTML file:
1. `<head>`: meta + JetBrains Mono link + inline `<style>`
2. `<body>`:
   - Header (pulse dot + h1)
   - Subtitle
   - N `.card` sections (each with `.card-header` + content)
   - Footer (sources + disclaimer)

## Output Conventions

1. **Save path**: `/root/<topic>-guide.html` or `~/<filename>.html` for ad-hoc; use project dir if user specifies.
2. **Deliver**: Tell user path via `MEDIA:/root/<file>.html` (Telegram renders HTML link).
3. **Verify**: Run `ls -la <path> && wc -l <path>` after writing to confirm file exists.
4. **Pure inline**: No external CSS, no JS libs (except Google Fonts), no React/Vue/Tailwind.
5. **BM-friendly**: Title and labels can mix English + BM as user prefers; default to user's last-used language.

## Pitfalls

- **viewBox too small** → text gets clipped. Min 800x400 for anatomy, 800x300 for timeline, 800x200 for single-section diagrams.
- **Text inside pattern fills** → invisible. Always set `fill="#hex"` explicitly on every `<text>`.
- **Telegram `MEDIA:` prefix** → file MUST be absolute path. `/root/file.html` not `./file.html`.
- **SVG arrow markers** → define once in `<defs>`, reference via `marker-end="url(#arrow-id)"`.
- **Color contrast on dark bg** → emerald/cyan/violet/rose all readable. Avoid yellow/amber text on slate bg (low contrast); use as fill/stroke not body text.
- **Multiple sections** → wrap each in `.card` div. Don't dump all content as one giant raw SVG.
- **Long pages (>500 lines)** → consider breaking into 2-3 HTML files if user needs portability.
- **Path label collisions** → when 2+ labels compete for same x-coordinate, offset vertically (one at y=A, one at y=A+12).
- **Animated pulse** → use CSS `@keyframes` (no JS), 2s loop, opacity 1→0.4→1.

## Reference Examples

- `/root/aminol-acl-guide.html` — full working example: anatomy (Pattern 1) + 9-month timeline (Pattern 2) + do/don't cards (Pattern 3) + 5 laws grid (Pattern 3) + signature quote (Pattern 4). 445 lines, single file.

## Companion Skills

- `architecture-diagram` — software/cloud/infra diagrams (tech component types: Frontend/Backend/Database/AWS/Security)
- `excalidraw` — hand-drawn whiteboard sketches (JSON format)
- `manim-video` — math/algorithm animations (MP4 output)

## Bundled Support Files

- `templates/explanatory-guide-skeleton.html` — copy-and-modify starter with all 4 patterns wired up (anatomy SVG, timeline SVG, do/don't cards, signature quote). Replace `{{TEMPLATE}}` placeholders and ship.