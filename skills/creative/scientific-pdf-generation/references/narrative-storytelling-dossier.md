# Narrative Storytelling Dossier — Mode B Sub-pattern
**Proven: 2026-07-25 — THE FORGE (33 pages, 296 KB)**

A distinct sub-pattern within Mode B for *narrative storytelling dossiers*: multi-chapter historical/institutional case studies connected by a single framing device, rendered in a dark "noir" book aesthetic (Palatino/Georgia serif, deeper black #0a0a0a, darker gold #c9952b).

Use when the user asks for a "bedtime story", "reality dream engine", "storytelling dossier", "multiple case studies with a frame", or any request that pairs institutional/historical analysis with narrative architecture — especially when each case study maps to a personal wound or origin story (e.g. "what would my life be if X never happened?").

## When This Pattern Fits

| Signal | Example |
|--------|---------|
| User asks for "storyline" not "analysis" | "Give me full dossier as storyline I can read before bed" |
| Multiple cases bound by a single thesis | "What if every architecture of constraint was forged in betrayal?" |
| Each case follows a consistent arc | BETRAYAL → RECOGNITION → FORGING → ARCHITECTURE |
| Personal wound is the framing device | "What would my life be if Tengku Taufik never held that town hall?" |
| User wants "dream engine" not "report" | "Start the reality dream engine" |

## Color Palette (Noir Book — differs from standard Mode B)

```css
Background:  #0a0a0a  (deeper black, book-like)
Text:        #d4d4d4  (warm grey, easier on eyes than pure white)
Gold:        #c9952b  (darker, richer gold accent)
Gold-light:  #e0c080  (headings)
Gold-dim:    #b8860b  (subtitles)
Dim:         #888888  (captions, secondary text)
Dim-deep:    #555555  (footer, source text)
Border:      #333333  (table grids, separators)
Panel:       #141414  (callout box backgrounds)
Red:         #a03020  (wound/betrayal callouts)
Teal:        #2a9d8f  (irony/conversation starter callouts)
Green:       #1a3a1a  (forging-moment backgrounds)
```

## CSS Component Library

Below are ALL CSS components used in the proven 33-page THE FORGE dossier. Each is documented with its purpose and selector.

### Page Setup

```css
@page {
  size: A4;
  margin: 2.2cm 2cm 2.5cm 2cm;
  @bottom-center {
    content: counter(page);
    font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
    font-size: 8pt;
    color: #555;
  }
}
@page:first { @bottom-center { content: none; } margin: 0; }
@page cover { @bottom-center { content: none; } margin: 0; }
@page chapter-start { @bottom-center { content: none; } }

body {
  font-family: 'Palatino', 'Georgia', 'DejaVu Serif', serif;
  font-size: 11pt; line-height: 1.7;
  color: #d4d4d4; background: #0a0a0a;
  orphans: 3; widows: 3;
}
```

**Why serif for narrative:** Unlike standard Mode B (sans-serif for intel briefings), narrative dossiers use serif body text (Palatino/Georgia) — it signals "book" not "briefing," and pairs with the bedtime-story context. Standard Mode B's GitHub-dark palette (#0d1117) and Helvetica is replaced with a warmer, deeper noir aesthetic.

### Cover Page

```css
.cover-page {
  page: cover; width: 21cm; height: 29.7cm; background: #0a0a0a;
  position: relative; overflow: hidden;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center; text-align: center;
}
.cover-page::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(160, 80, 20, 0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 70%, rgba(200, 150, 50, 0.06) 0%, transparent 60%);
}
.cover-page h1 {
  font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
  font-size: 42pt; font-weight: 700; color: #c9952b;
  letter-spacing: 6pt; text-transform: uppercase;
  margin: 0 0 12pt 0; position: relative; z-index: 1;
}
```

Cover is a full-page canvas with radial gradient vignettes on ::before. Title is large gold sans-serif, centered vertically. Position the forge-icon (★ or ▣ or ✦ as unicode) above the title. Epigraph below title in 10.5pt italic dim text. Cover footer at `bottom: 40pt` in 8pt uppercase dim text.

### Table of Contents Page

```css
.toc-page { page-break-after: always; page: chapter-start; }
.toc-page h2 { 
  font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
  font-size: 14pt; font-weight: 700; color: #c9952b;
  letter-spacing: 3pt; text-transform: uppercase;
  margin-bottom: 24pt; border-bottom: 1px solid #333; padding-bottom: 8pt;
}
.toc-entry { padding: 4pt 0; border-bottom: 1px dotted #222; }
.toc-chapter { font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-size: 10pt; font-weight: 700; color: #d4d4d4; }
.toc-title { font-size: 9.5pt; color: #999; margin-left: 12pt; }
.toc-tag { font-size: 8pt; color: #666; font-style: italic; margin-left: 24pt; }
```

Each TOC entry has three lines: chapter number (bold), title (dim), tagline (italic, dimmer). The dotted border provides visual separation without being heavy.

### Chapter Start Pages

```css
.chapter-start { page: chapter-start; page-break-before: always; padding-top: 80pt; text-align: center; }
.chapter-number {
  font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
  font-size: 10pt; color: #c9952b; letter-spacing: 4pt;
  text-transform: uppercase; margin-bottom: 16pt;
}
.chapter-start h2 {
  font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
  font-size: 22pt; font-weight: 700; color: #e0c080;
  margin: 0 0 16pt 0; line-height: 1.2;
}
.chapter-start .chapter-sub { font-size: 10pt; color: #888; font-style: italic; margin-bottom: 30pt; }
.chapter-start .gold-divider { width: 60pt; height: 1px; background: #c9952b; margin: 0 auto; }
```

Each chapter starts on a fresh page with: (1) centered small-caps chapter number in gold, (2) large bold heading in gold-light, (3) italic subtitle in dim, (4) thin gold divider line. The 80pt padding-top drops the content below the page center.

### Section Break

```css
.section-break { text-align: center; margin: 20pt 0; color: #333; font-size: 18pt; }
```

Used as `* * *` between narrative sections. Set to a dim color so it's visible but doesn't compete with body text.

### Body Text

```css
p { text-align: justify; margin: 8pt 0; text-indent: 1.5em; }
p.no-indent { text-indent: 0; }
```

First paragraph after a heading or section-break should use `class="no-indent"` to suppress the indent. All other body paragraphs are indented 1.5em.

### Callout Boxes (Narrative Variant)

```css
.callout { background: #141414; border-left: 3px solid #c9952b; padding: 10pt 14pt; margin: 16pt 0; font-size: 10pt; border-radius: 0 4pt 4pt 0; }
.callout.gold { border-left-color: #c9952b; }
.callout.red { border-left-color: #a03020; background: #1a0e0e; }
.callout.teal { border-left-color: #2a9d8f; background: #0e1a18; }
.callout-label { font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: 2pt; margin-bottom: 4pt; }
```

Semantic map for narrative dossiers:
- `.callout` (default gold) — key insight, recognition, framing statement
- `.callout.red` — the wound/betrayal description, emotional center
- `.callout.teal` — irony, conversation starter, non-obvious observation

### Forging Moment Box

```css
.forging-moment {
  background: #0d1a0d; border: 1px solid #1a3a1a; border-radius: 4pt;
  padding: 10pt 14pt; margin: 16pt 0; page-break-inside: avoid;
}
.forging-moment .fm-label {
  font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
  font-size: 8pt; font-weight: 700; color: #4ade80;
  text-transform: uppercase; letter-spacing: 2pt; margin-bottom: 4pt;
}
.forging-moment .fm-title { font-size: 11pt; font-weight: 700; color: #d4d4d4; margin-bottom: 4pt; }
.forging-moment .fm-body { font-size: 10pt; color: #aaa; }
```

A distinct box that marks the "forging moment" in each case — the precise point where the wound was transmuted into architecture. Green-bordered to signal growth/construction. Place this box right after the betrayal section and before the "What Was Forged" verdict.

### Verdict Box

```css
.verdict-box {
  border: 1px solid #333; padding: 12pt 16pt; margin: 16pt 0;
  background: #0d0d0d; page-break-inside: avoid;
}
.verdict-box h4 {
  font-family: 'Helvetica', 'DejaVu Sans', sans-serif;
  font-size: 10pt; font-weight: 700; color: #c9952b;
  text-transform: uppercase; letter-spacing: 2pt; margin: 0 0 6pt 0;
}
.verdict-box .forged-from { font-size: 9pt; color: #888; margin: 4pt 0; }
.verdict-box .became { font-size: 10pt; color: #d4d4d4; font-style: italic; margin: 4pt 0; }
```

The concluding block of every case study. Always has two structured fields:
- `.forged-from`: lists the specific wounds that created this architecture (date, body count, betrayal mechanism)
- `.became`: lists the specific architecture forged (laws, institutions, doctrines, principles)

### Epistemic Footer

```css
.epistemic-footer {
  margin-top: 30pt; padding-top: 10pt; border-top: 1px solid #222;
  font-size: 8pt; color: #555;
}
```

A footer block at the end of each major section, labeling the epistemic class of all claims made. Contains `<span class="badge">` tags.

### Epistemic Badges (Narrative Variant — Warm Palette)

```css
.badge { display: inline; font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-size: 7.5pt; font-weight: 700; padding: 1pt 4pt; border-radius: 2pt; letter-spacing: 1pt; }
.badge-obs { background: #1a3a2a; color: #4ade80; }
.badge-der { background: #1a2a3a; color: #60a5fa; }
.badge-int { background: #3a2a1a; color: #fbbf24; }
.badge-spec { background: #3a1a2a; color: #f472b6; }
.badge-claim { background: #2a1a1a; color: #f87171; }
```

Slightly warmer and richer than the standard Mode B badges (which use GitHub dark palette). The deeper backgrounds help them stand out against the #0a0a0a page background.

### Blockquotes (Narrative)

```css
blockquote { margin: 14pt 20pt; padding: 8pt 14pt; border-left: 2px solid #333; color: #aaa; font-style: italic; }
blockquote .attrib { display: block; margin-top: 4pt; font-size: 9pt; color: #777; font-style: normal; }
```

Blockquotes have an `.attrib` span for attribution. Used for key quotes that drive the narrative.

### Tables

```css
table { width: 100%; border-collapse: collapse; margin: 14pt 0; font-size: 9.5pt; page-break-inside: avoid; }
th { background: #1a1a1a; color: #c9952b; font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-weight: 600; padding: 6pt 8pt; text-align: left; border-bottom: 1px solid #333; font-size: 9pt; }
td { padding: 5pt 8pt; border-bottom: 1px solid #1c1c1c; vertical-align: top; color: #bbb; }
tr:nth-child(even) td { background: #0f0f0f; }
```

Dark table style: gold headers on dark grey panels, alternating row backgrounds. Compact enough for multi-row comparison tables.

### Final/Closing Page

```css
.final-page { page-break-before: always; page: chapter-start; padding-top: 120pt; text-align: center; }
.final-page h2 { font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-size: 18pt; color: #c9952b; margin-bottom: 20pt; }
.final-page p { text-align: center; text-indent: 0; max-width: 70%; margin: 0 auto 10pt; }
```

A closing page with the title, "Forged, Not Given" (or the framing device's closing statement), date, and tagline. Minimalist, centered, poetic.

### Reference Section

```css
.ref-section { page-break-before: always; page: chapter-start; }
.ref-section h2 { font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-size: 14pt; font-weight: 700; color: #c9952b; letter-spacing: 3pt; text-transform: uppercase; margin-bottom: 18pt; border-bottom: 1px solid #333; padding-bottom: 8pt; }
.ref-entry { font-size: 9pt; color: #999; margin: 4pt 0; padding-left: 12pt; text-indent: -12pt; }
```

Sources section with hanging indent entries. Each entry starts with `<strong>Case Name:</strong>` then lists sources.

## Narrative Spine

Every narrative dossier should follow this spine:

1. **Cover page** — full-page, centered, title + epigraph + subtitle + forge icon
2. **Table of contents** — all chapters with number, title, tagline
3. **Prologue / Frame** — the personal wound or framing device that motivates the entire dossier. Sets up the thesis (e.g. "What if every architecture of constraint was forged in betrayal?")
4. **N chapters** (typically 5-8) — each follows this internal structure:
   - Chapter start page (number, title, subtitle, gold divider)
   - Scene-setting paragraph (no-indent)
   - Betrayal narrative (what happened, who failed, the wound)
   - Callout box (red) — the wound summary
   - Forging narrative (the architecture built)
   - Forging moment box — the moment of transmutation
   - What Was Forged verdict box
   - Optional epistemic footer
5. **Epilogue** — pattern analysis across all cases, the recursive truth, implications
6. **Final page** — closing statement
7. **Reference section** — sourced citations per case

## Epistemic Discipline for Historical Narrative

- Every named event, date, and statistic must be OBS-level (sourced from published archives)
- The interpretive frame ("betrayal → forge" pattern) is DER — label it as derived cross-case analysis
- The thesis claim ("all architectures of constraint are forged in betrayal") is SPEC — label it as a philosophical proposition
- Never let narrative punch override epistemic precision (standard Tri-Witness rule)
- Add an epistemic footer at the end of the Prologue (or end of whole document) with badge-row labeling each claim class

## Rendering

```bash
cd /tmp/<project-dir>
weasyprint manuscript.html "TITLE.pdf" 2>&1
```

No special flags needed. All figures (if any) must be in the same directory. Pure text dossiers are faster (< 5 seconds) and more reliable than those with matplotlib figures.

**Proven:** 2026-07-25 — THE FORGE: When Institutional Betrayal Becomes Architecture (33 pages, 296 KB, 8 chapters + frame + epilogue + references, pure text + tables, rendered in ~2 seconds).
