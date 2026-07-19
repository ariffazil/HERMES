# Briefing Template — HTML Structure

The HTML template for executive intelligence briefings uses these cognitive-aligned design elements:

## Design Principles
- **Dark cover page** (#0f0c29 gradient) — "classified" feel, sets tone
- **Scoreboard at top** — key metrics in grid, instant context
- **Color-coded cards** — each section gets a distinct left-border color
  - Politics: `#302b63` (indigo)
  - Bangang/Critical: `#dc3545` (red)
  - PETRONAS/Corporate: `#00a651` (green)
  - Viral/Social: `#ff6b35` (orange)
  - Tersirat/Subtext: `#6f42c1` (purple)
  - Positive: `#28a745` (green)
  - Warning: `#ffc107` (amber)
- **Verdict badges** — inline colored labels (red/green/purple/orange)
- **Tersirat boxes** — purple gradient background, distinct from regular cards
- **Quote blocks** — dark background, white text, for key statements
- **Section headers** — gradient backgrounds with emoji + tag

## Cognitive Flow
1. **Cover** → Sets tone, date range, classification
2. **TOC** → Orient the reader
3. **Scoreboard** → Key numbers at a glance
4. **Positive/Neutral** → Politics, economics (builds context)
5. **Critical** → "Bangang" segment (the sting)
6. **Entity Deep Dive** → PETRONAS, specific company
7. **Social/Viral** → Lighter content, engagement hook
8. **Tersirat** → The real value — hidden patterns
9. **Verdict** → One-line synthesis, scorecard

This flow mirrors how humans process information: context → facts → criticism → hidden meaning → takeaway.

## CSS Patterns
```css
/* Card with colored left border */
.card { background: #f8f7ff; border-left: 4px solid #302b63; padding: 14px 16px; margin-bottom: 14px; border-radius: 0 6px 6px 0; }
.card.bangang { border-left-color: #dc3545; background: #fff5f5; }
.card.petronas { border-left-color: #00a651; background: #f0fff5; }
.card.tersirat { border-left-color: #6f42c1; background: #f8f0ff; }

/* Verdict badges */
.verdict { margin-top: 8px; font-size: 10pt; font-weight: 600; padding: 4px 10px; border-radius: 4px; display: inline-block; }
.verdict.red { background: #fee; color: #dc3545; }
.verdict.green { background: #efe; color: #28a745; }
.verdict.purple { background: #f0e6ff; color: #6f42c1; }

/* Tersirat box */
.tersirat-box { background: linear-gradient(135deg, #f8f0ff, #f0e6ff); border: 1px solid #d0c0f0; border-radius: 8px; padding: 16px; margin: 16px 0; }

/* Scoreboard grid */
.scoreboard { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
.score-item { background: #f8f7ff; border-radius: 8px; padding: 14px; text-align: center; border: 1px solid #e8e6f0; }
.score-item .value { font-size: 20pt; font-weight: 800; color: #302b63; }

/* Quote box */
.quote-box { background: #24243e; color: #e8e6f0; padding: 16px 20px; border-radius: 8px; margin: 16px 0; font-style: italic; }

/* Avoid page breaks inside cards */
.card, .tersirat-box, .quote-box, .scoreboard { break-inside: avoid; }
```

## A4 Page Setup
```css
@page { size: A4; margin: 15mm; }
```
This rule is CRITICAL — without it, Chrome/Playwright defaults to US Letter and may produce unexpected page breaks.
