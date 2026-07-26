# Isaacson-Style Biography Pattern — HTML→weasyprint

> **Proven:** 2026-07-21 — Tengku Muhammad Taufik biography (19 pages, 94KB). Built twice in one session, second version integrated OpenCode shadow dossier intelligence.
> **Stack:** HTML + CSS → weasyprint. No matplotlib, no reportlab. Pure text.

## When to Use

When the user asks for a "Walter Isaacson-style biography" or "full biography" of a corporate/institutional figure — deep narrative, psychological depth, shadow mapping, the person behind the title.

NOT for: quick profiles, intelligence dossiers (use Mode B reportlab), or sell-side analyst reports (use Mode C).

## Design Philosophy

Isaacson's biographical style emphasizes:
- Narrative arc over chronology — start with the name, end with the coda
- Psychological depth over hagiography — map the scars, not just the achievements
- Tension between stated beliefs and revealed actions
- Historical forces that shape individual choices
- Epigraphs that frame the subject's own words against institutional reality

## HTML+CSS Template

**Typography:**
- Body: Georgia / DejaVu Serif, 10.5pt, 1.6 line-height, justified
- Headings: Helvetica / DejaVu Sans, navy (#1b3a5c)
- Epigraphs: italic, centered, 11.5pt
- Footnotes: 8pt, grey (#888)

**Page layout:**
- A4, 2.4cm sides, 2.6cm bottom
- Running page numbers: "— N —" (Georgia, 9pt)
- First page: no page number
- Cover page with `page-break-after: always`
- TOC after cover with `page-break-after: always`

**Key CSS patterns:**

```css
@page { margin: 2.4cm 2.0cm 2.6cm 2.0cm;
  @bottom-center { content: "— " counter(page) " —"; font-family: 'Georgia', serif; font-size: 9pt; color: #777; } }
@page:first { @bottom-center { content: none; } }
body { font-family: 'Georgia', 'DejaVu Serif', serif; font-size: 10.5pt; line-height: 1.6; color: #1a1a1a; text-align: justify; orphans: 3; widows: 3; }
h2 { font-family: 'Helvetica', 'DejaVu Sans', sans-serif; font-size: 14pt; font-weight: 700; color: #1b3a5c; border-bottom: 1px solid #ccc; page-break-after: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; page-break-inside: avoid; }
th { background: #1b3a5c; color: white; font-family: 'Helvetica', sans-serif; padding: 4pt 7pt; font-size: 8.5pt; }
td { padding: 4pt 7pt; border-bottom: 0.5pt solid #d9d9d9; }
tr:nth-child(even) td { background: #f7f9fb; }
```

**Special elements:**

- `.cover-page` — centered, 90pt top padding, page-break-after
- `.cover-epigraph` — italic, 11pt, centered, 36pt margins
- `blockquote` — 14pt left margin, 3pt grey left border, italic
- `.free-speech` — blue left border, light blue background, for reconstructed speech
- `.sig-box` — gold border, cream background, for signature findings
- `.toc` — simple two-column table, 10pt
- `.ornament` — centered `— § —` divider
- `.verse` / `.verse-attrib` — centered poetry format for final quotes

## Build Pipeline

```python
import subprocess, os

OUT_DIR = '/tmp/bio'
os.makedirs(OUT_DIR, exist_ok=True)

html_path = f'{OUT_DIR}/biography.html'
with open(html_path, 'w') as f:
    f.write(FULL_HTML_STRING)

pdf_path = f'{OUT_DIR}/Biography.pdf'
result = subprocess.run(['weasyprint', html_path, pdf_path],
    capture_output=True, text=True, timeout=60)

# Verify
info = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
```

## Standard Spine (20 chapters)

1. The Name — name etymology, birth year, institutional context
2. The Scholar — education, what the discipline choice reveals
3. The Apprenticeship — mentors, formative roles
4. The Ascension — predecessor contrast table
5. The Kingdom at Peak — the golden years
6. The Impossible Geometry — multi-pressure structural analysis
7. The Identity Paradox — structural contradictions in the role
8. The Beautiful One — Universe 25 mapping, comfort-as-reform
9. The Closed Door — the pivotal private moment
10. The Two Voices — speech signature analysis (human vs corporate)
11. The [Key] Interview — analysis of the most revealing public appearance
12. The Things They Cannot Say — unspeakable truths
13. The Scars — personal/professional wounds
14. The DNA They Inherited — institutional founding history
15. The Universe 25 Mapping — the institutional cycle table
16. The Orphan's Paradox — "the individual who cares more..."
17. The Discourse Geometry — axes present vs absent
18. The ATLAS333 / Paradox Map — cognitive geometry framework mapping
19. What They Would Say If They Could — reconstructed free speech
20. The Geometry of a Life — final synthesis
21. Coda: The Name, Revisited — the two irreconcilable readings

Not every chapter is needed for every subject. Adapt the spine to the person.

## Pitfalls

- **Pure text only.** No matplotlib figures. The weasyprint pipeline handles text + CSS tables cleanly. If you need charts, switch to Mode C or Mode B reportlab.
- **Nested quotes crash Python.** Use raw strings `r"""..."""` for HTML with complex quotes. Alternatively, use double-quoted Python strings with escaped inner quotes: `"<font color=\"#xxx\">\"text\"</font>"`.
- **Test with pdftotext.** After render, run `pdftotext output.pdf - | head -20` to verify the title page renders. Check page count with `pdfinfo`.
- **Emoji don't render in weasyprint.** Replace all emoji with text equivalents before rendering.
- **TOC must be on its own page.** Use `page-break-after: always` on the TOC div.
