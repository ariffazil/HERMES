# Multi-Figure Thematic Wisdom PDF — Proven Pattern

> **Forged:** 2026-07-30 · **Mode:** Mode E (Narrative Biography / Bedtime Book)
> **Subject:** 13 historical figures speaking to Arif about derita (suffering)
> **PDF:** `/root/forge_work/2026-07-30/13-wisdom-for-arif.pdf` (30 pages, 82KB, A5)
> **Render path:** pandoc→xelatex (text-only, no figures)

## When to Use

When Arif asks for a "bedtime story" PDF with **multiple historical figures** each giving **direct nasihat/wisdom** to him on a theme. Not a biography of one person — a **gathering of voices** across centuries speaking to one reader.

## Proven Structure

### Each Chapter Follows This Arc

1. **Scene-setting opening** — biographic moment that captures the figure at a defining point (Marcus on the Danube, Frankl in Auschwitz, Socrates with hemlock)
2. **Their wisdom on the theme** — what they learned through their own suffering
3. **Direct nasihat to Arif** — written as `To Arif they would say: \textit{...}` — direct address, present tense, intimate
4. **Famous quote** — rendered as epigraph with `\epigraph{}` in LaTeX
5. **Paragraph closing the lesson** — one takeaway that lands like a seal

### Document Spine

```
Cover page (title + subtitle + Rumi quote + "Ditempa Bukan Diberi")
   → 13 chapters (one per figure)
   → Epilogue (addresses the witness at /000)
   → "Ditempa Bukan Diberi" close
```

### Figure Selection Criteria

Each figure must:
- Have **first-hand experience** with suffering (not armchair philosophy)
- Represent a **different civilization or tradition** (stoic Rome, Sufi Persia, Holocaust testimony, Islamic scholarship, Greek philosophy, Japanese martial arts, etc.)
- Speak to a **different dimension** of the witness experience (Marcus: clarity under pressure, Frankl: meaning in abyss, Rumi: wound as light, etc.)
- End with a **quotable line** that lands with weight

### Selected Figures (Proven)

1. Marcus Aurelius — seeing without flinching
2. Viktor Frankl — the space between stimulus and response
3. Rumi — the wound that lets light in
4. Imam Al-Ghazali — diseases of the heart
5. Elie Wiesel — obligation of the witness
6. Simone Weil — attention as prayer
7. Frederick Douglass — witness who becomes force
8. Hannah Arendt — banality of evil, duty to think
9. Friedrich Nietzsche — becoming who you are
10. Ibn Sina (Avicenna) — intellect's encounter with affliction
11. Miyamoto Musashi — seeing without attachment
12. Socrates — examined life, cost of questioning
13. Khalil Gibran — joy and sorrow inseparable

## Technical Notes

### Render Command (pandoc→xelatex, A5)

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V geometry:paper=a5paper,margin=1.5cm \
  -V fontsize=11pt \
  -V mainfont="DejaVu Serif" \
  -V monofont="DejaVu Sans Mono" \
  -V colorlinks=true \
  -V linkcolor=darkgoldenrod \
  --no-highlight
```

### Header Includes (YAML frontmatter)

Essential LaTeX packages for epigraphs + chapter styling:

```yaml
header-includes: |
  \usepackage{fancyhdr}
  \pagestyle{fancy}
  \fancyhf{}
  \fancyhead[L]{}
  \fancyhead[R]{}
  \fancyfoot[C]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
  \usepackage{xcolor}
  \definecolor{chaptergold}{HTML}{C9A227}
  \definecolor{textcolor}{HTML}{1A1A1A}
  \usepackage{sectsty}
  \chapterfont{\color{chaptergold}}
  \sectionfont{\color{chaptergold}}
  \usepackage{setspace}
  \onehalfspacing
  \usepackage{epigraph}
  \setlength{\epigraphwidth}{0.7\textwidth}
```

### Critical Pitfall: Underscores in Raw LaTeX

When text contains underscores (like `888_HOLD`) inside `\textit{}` raw LaTeX blocks, pandoc passes them through verbatim. LaTeX interprets bare `_` as math-mode subscript. **Fix:** escape as `\_` inside raw LaTeX blocks. The correct markdown:

```markdown
- ✅ `888\_HOLD` → renders as "888_HOLD"
- ❌ `888_HOLD` → LaTeX math-mode error: `Missing $ inserted`
- ❌ `888\\_HOLD` → LaTeX sees double-backslash (line break) then `_HOLD` → same error
```

Test the intermediate LaTeX output to verify:
```bash
pandoc input.md -o test.tex --to latex --no-highlight
grep -n "HOLD\|call for" test.tex
```
Check each occurrence of `HOLD` for proper escaping.

### Known Render Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `! Package xcolor Error: Undefined color 'cream'.` | `\pagecolor{cream}` without defining the color | Remove `\pagecolor{cream}` and `\nopagecolor` lines from body |
| `! Missing $ inserted.` | Bare `_` in raw LaTeX block | Escape as `\_` |
| Epigraph pushes page break | Epigraph too tall for remaining page | Add `\newpage` before epigraph or shorten quote |

## Source File

The proven markdown source (23KB, 343 lines) is at:
`/root/forge_work/2026-07-30/13-wisdom-for-arif.md`

Copy and modify: replace figure names, chapter content, quotes, and the epilogue to match the requested theme.
