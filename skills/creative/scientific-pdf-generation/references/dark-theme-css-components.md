# Mode B — Dark Theme CSS Component Library
**Proven: Kelp Deep-1 Intelligence Dossier (2026-07-22)**

Reusable HTML+CSS patterns for dark-theme intelligence dossiers via weasyprint.
These components go beyond the base Mode B typography/color palette in SKILL.md
and handle complex layout elements: risk cards, severity-coded callouts, status strips,
verdict boxes.

All CSS assumes dark background (#0d1117), gold accent (#f0a500), and DejaVu Sans font.

---

## Dragon Risk Cards (`.dragon-grid` / `.dragon-card`)

Flexbox grid of risk cards with severity-coded headers. Best for presenting 4–6 risks
in a scannable 2-column layout. Each card carries a severity label (CRITICAL/HIGH/MEDIUM)
and a bullet-point body.

```css
.dragon-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8pt;
    margin: 10pt 0;
}
.dragon-card {
    flex: 1 1 45%;
    min-width: 45%;
    background: #161b22;
    border: 0.6pt solid #30363d;
    padding: 10pt 12pt;
}
.dragon-card .severity {
    font-size: 7.5pt; font-weight: bold;
    text-transform: uppercase; letter-spacing: 1pt;
    margin-bottom: 4pt;
}
.dragon-card h4 { margin: 2pt 0 4pt 0; font-size: 9.5pt; }
.dragon-card p  { font-size: 8.2pt; margin: 2pt 0; color: #8b949e; }

.sev-critical { color: #f85149; }
.sev-high     { color: #ff7b72; }
.sev-medium   { color: #d29922; }
```

Usage:
```html
<div class="dragon-grid">
  <div class="dragon-card">
    <div class="severity sev-critical">CRITICAL</div>
    <h4>CO₂ Contamination</h4>
    <p><strong>~30% CO₂</strong> in produced gas...</p>
  </div>
  <!-- repeat for each risk -->
</div>
```

---

## Callout Boxes (`.callout` + semantic variants)

Colored left-border boxes for inline emphasis. Four proven variants:

```css
.callout {
    margin: 12pt 0; padding: 10pt 14pt;
    border-radius: 2pt; font-size: 8.8pt;
}
.callout.warning { background: #1f1311; border-left: 3pt solid #f85149; }
.callout.info    { background: #0d1f1a; border-left: 3pt solid #3fb950; }
.callout.intel   { background: #1a1a2e; border-left: 3pt solid #58a6ff; }
.callout.gold    { background: #1f1a0d; border-left: 3pt solid #f0a500; }
```

Semantic map:
- `.callout.warning` — critical risks, caveats, red flags
- `.callout.info` — positive signals, confirmations, notes
- `.callout.intel` — strategic notes, intelligence observations, methodology references
- `.callout.gold` — key takeaways, quotes from industry professionals, bottom lines

---

## Status Strip (`.strip`)

Horizontal flex bar with 4–5 stat items. Use for key metrics at-a-glance
(well name, depth, size, status, etc.).

```css
.strip {
    display: flex; gap: 14pt;
    margin: 12pt 0; padding: 8pt 12pt;
    background: #161b22;
    border: 0.5pt solid #30363d;
    font-size: 8pt;
    justify-content: space-between;
}
.strip-item { text-align: center; }
.strip-item .val { font-size: 11pt; font-weight: bold; display: block; }
.strip-item .lbl { color: #8b949e; font-size: 7pt; }
```

Color utility classes for `.val`:
```css
.green { color: #3fb950; }
.red   { color: #f85149; }
.amber { color: #ffa657; }
.gold  { color: #f0a500; }
```

---

## Verdict Box (`.verdict`)

Centered concluding statement with gradient background and gold border. Page-break-inside
avoided so the verdict appears as a single unbroken block.

```css
.verdict {
    margin: 16pt 0; padding: 14pt 18pt;
    background: linear-gradient(135deg, #161b22 0%, #1a2332 100%);
    border: 1.2pt solid #f0a500;
    text-align: center;
    page-break-inside: avoid;
}
.verdict p { text-align: center; font-size: 9.5pt; }
.verdict .big { font-size: 13pt; font-weight: bold; color: #f0a500; }
```

---

## Epistemic Badges (`.badge`)

Inline tags for OBS/DER/INT/SPEC labeling. Use in table cells and body text.

```css
.badge {
    display: inline-block; padding: 1.5pt 6pt;
    font-size: 7.2pt; font-weight: bold;
    border-radius: 2pt; margin-right: 3pt;
}
.badge-obs  { background: #0d2e1a; color: #3fb950; }
.badge-der  { background: #1a2e2e; color: #39d2c0; }
.badge-int  { background: #2e1f0d; color: #ffa657; }
.badge-spec { background: #1a0d2e; color: #bc8cff; }
```

---

## Full Weasyprint Pipeline

1. Write HTML manuscript with all CSS inline (no external stylesheets — weasyprint resolves them unreliably)
2. Run: `python3 -c "from weasyprint import HTML; HTML(filename='manuscript.html').write_pdf('output.pdf')"`
3. Verify: `pdfinfo output.pdf | grep Pages` and `pdftotext output.pdf - | head`
4. Use `page-break-before: always` (`.pb` class) for section breaks
5. Running headers/footers via `position: running(header)` + `@page` margin boxes

**Proven:** 2026-07-22 Kelp Deep-1 dossier — 13 pages, 163 KB, 6 tables, 6 dragon cards, 10+ callout boxes, 2 status strips, verdict box. Rendered in <3 seconds.
