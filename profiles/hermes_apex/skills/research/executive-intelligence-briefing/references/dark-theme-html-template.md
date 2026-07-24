# Dark-Themed Intelligence Dossier — HTML/CSS Template

Proven: 2026-07-11, Malaysia Civic Intelligence Briefing (14 pages, 61KB, weasyprint).

## Quick Start

1. Copy the HTML pattern below
2. Replace content sections with your briefing data
3. Convert: `weasyprint input.html output.pdf`
4. Verify: `pdfinfo output.pdf | grep Pages`

## Color Palette (GitHub Dark)

```
Background:  #0d1117
Panel:       #161b22 (header/footer/sidebars)
Gold accent: #f0a500 (H1 headings, accent lines)
Amber:       #ffa657 (H2 subheadings)
Green:       #3fb950 (positive signals, H3)
Blue:        #58a6ff (info, H4, links)
Red:         #f85149 (warnings, critical)
Teal:        #39d2c0 (quotes, conversation starters)
Text:        #e6edf3 (body — near-white, NOT pure white)
Dim:         #8b949e (captions, footer)
Border:      #30363d (table grid lines)
```

## CSS Components

### Page Setup
```css
@page {
  size: A4;
  margin: 2cm 2.2cm;
  @top-left { content: "Document Title — Date"; font-size: 7pt; color: #8b949e; }
  @top-right { content: "Organization"; font-size: 7pt; color: #f0a500; font-weight: bold; }
  @bottom-center { content: "Page " counter(page); font-size: 7pt; color: #8b949e; }
}
body { background: #0d1117; color: #e6edf3; font-family: 'Helvetica', sans-serif; font-size: 10pt; line-height: 1.55; }
```

### Signal Boxes (left-border accent)
```css
.signal-box { background: #161b22; border-left: 4px solid #f0a500; padding: 12px 16px; margin: 14px 0; border-radius: 0 6px 6px 0; }
.signal-box.red { border-left-color: #f85149; }
.signal-box.green { border-left-color: #3fb950; }
.signal-box.blue { border-left-color: #58a6ff; }
.signal-box.amber { border-left-color: #ffa657; }
```
Usage: `<div class="signal-box red"><strong>LABEL:</strong> Warning text</div>`

### Key Insight Box (green-bordered)
```css
.key-insight { background: #0d1f0d; border: 1px solid #3fb950; padding: 16px 20px; margin: 16px 0; border-radius: 6px; }
.key-insight .label { color: #3fb950; font-size: 8pt; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
```

### Warning Box (red-bordered)
```css
.warning-box { background: #1f0d0d; border: 1px solid #f85149; padding: 16px 20px; margin: 16px 0; border-radius: 6px; }
.warning-box .label { color: #f85149; font-size: 8pt; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
```

### Executive Callout (gold-bordered)
```css
.exec-callout { background: #1a1f28; border: 2px solid #f0a500; padding: 20px 24px; margin: 20px 0; border-radius: 8px; }
.exec-callout .headline { font-size: 14pt; color: #f0a500; font-weight: bold; }
```

### Tables (alternating rows)
```css
table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 9pt; }
th { background: #1a2332; color: #f0a500; padding: 8px 10px; border-bottom: 2px solid #f0a500; }
td { padding: 7px 10px; border-bottom: 1px solid #21262d; }
tr:nth-child(even) td { background: #161b22; }
tr:nth-child(odd) td { background: #0d1117; }
```

### Color-Coded Readings (inline)
```css
.reading-critical { color: #f85149; font-weight: bold; }
.reading-warning { color: #ffa657; font-weight: bold; }
.reading-good { color: #3fb950; font-weight: bold; }
.reading-info { color: #58a6ff; font-weight: bold; }
```
Usage: `<td class="reading-critical">COLLAPSING</td>`

### Epistemic Tags
```css
.tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 8pt; font-weight: bold; }
.tag-obs { background: #0d2818; color: #3fb950; }
.tag-der { background: #1a1a0d; color: #ffa657; }
.tag-int { background: #1a0d1a; color: #bc8cff; }
.tag-spec { background: #1a0d0d; color: #f85149; }
```

### Summary Strips (key-value)
```css
.summary-strip { background: #161b22; padding: 14px 18px; margin: 16px 0; border-radius: 6px; border: 1px solid #30363d; }
.summary-strip .item { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #21262d; }
```

### Blockquotes
```css
blockquote { background: #161b22; border-left: 3px solid #ffa657; padding: 12px 16px; font-style: italic; color: #ffa657; }
```

## Document Structure

1. **Cover page** — centered title (gold), subtitle (amber), divider line, tagline, metadata
2. **Table of contents** — summary-strip with section → title mapping
3. **Numbered sections** — H1 (gold) → H2 (amber) → H3 (green) → H4 (blue)
4. **Signal boxes** — key findings, warnings, positives
5. **Tables** — color-coded readings, comparison data
6. **Footer note** — centered, dim, border-top separator

## Pitfalls

- **Unicode emojis do NOT render** in PDF fonts. Replace 🔥 with "CRITICAL", ⚠️ with "WARNING", etc.
- **weasyprint ignores `box-shadow`** — don't use it for visual effects.
- **`vh` units** sometimes rejected by weasyprint — use `px` instead.
- **Keep HTML self-contained** — all CSS inline in `<style>` tag, no external files.
- **Font fallback** — use `'Helvetica', 'DejaVu Sans', sans-serif` chain.
