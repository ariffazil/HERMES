# weasyprint PDF Template — Scientific Geological Manuscripts

Proven path 2026-07-03 (Kinabalu Two-Oceanics, 15 pages, 1.5 MB).
Use this when `reportlab` is not available (PEP 668 blocks install on this VPS).

## Stack

- **weasyprint v68.1** (`/usr/local/bin/weasyprint`) — system binary, NOT in GEOX venv
- **pandoc** (`/usr/bin/pandoc`) — Markdown → HTML if you want to author in MD
- **matplotlib** (`/root/GEOX/.venv/bin/python3`) — for figures
- **HTML + CSS** — write manuscript as a single HTML file, embed `<img src="figN.png">`

## The command

```bash
# 1. Place HTML at /tmp/<project>/manuscript.html
# 2. Place figures at /tmp/<project>/fig*.png (same directory)
# 3. base_url resolves relative image paths:
weasyprint /tmp/<project>/manuscript.html /root/<project>.pdf
```

Or programmatically (works inside GEOX venv):
```python
from weasyprint import HTML
HTML(filename='/tmp/.../manuscript.html',
     base_url='/tmp/<project>/').write_pdf('/root/output.pdf')
```

## CSS — minimal scientific template

```css
@page { size: A4; margin: 2cm 1.8cm;
  @top-center { content: "TITLE • GEOX-LC-001 • Arif (F13)"; font-size: 9pt; color: #555; }
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 9pt; color: #555; }
  @bottom-right { content: "DITEMPA BUKAN DIBERI"; font-size: 8pt; color: #888; font-style: italic; }
}
body { font-family: 'Times New Roman', Georgia, serif; font-size: 11pt; line-height: 1.55; color: #111; }
h1 { font-size: 22pt; color: #1e3a5f; border-bottom: 3px solid #c44545; padding-bottom: 8px; }
h2 { font-size: 15pt; color: #1e3a5f; border-bottom: 1px solid #aaa; padding-bottom: 4px;
     margin-top: 22pt; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #2c5985; margin-top: 14pt; page-break-after: avoid; }
.abstract { background: #fff8e1; border-left: 4px solid #c44545; padding: 12pt 16pt;
            margin: 12pt 0; font-size: 10.5pt; }
.abstract-title { font-weight: bold; color: #1e3a5f; margin-bottom: 4pt; }
.figure { text-align: center; margin: 14pt 0; page-break-inside: avoid; }
.figure img { max-width: 100%; height: auto; border: 1px solid #ccc; }
.figure-caption { font-size: 9.5pt; color: #333; margin-top: 6pt; font-style: italic; line-height: 1.4; }
table { border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 10pt; page-break-inside: avoid; }
th { background: #1e3a5f; color: white; padding: 6pt 8pt; text-align: left; border: 1px solid #444; }
td { padding: 5pt 8pt; border: 1px solid #aaa; vertical-align: top; }
tr:nth-child(even) { background: #f5f5f0; }
.key-finding { background: #d4edda; border-left: 3px solid #28a745; padding: 6pt 10pt; margin: 6pt 0; font-size: 10.5pt; }
.warning { background: #f8d7da; border-left: 3px solid #c44545; padding: 6pt 10pt; margin: 6pt 0; font-size: 10.5pt; }
.note { background: #d1ecf1; border-left: 3px solid #17a2b8; padding: 6pt 10pt; margin: 6pt 0; font-size: 10pt; }
.receipts { font-family: 'Courier New', monospace; font-size: 8.5pt; background: #f4f4f4;
            border: 1px solid #ddd; padding: 8pt 12pt; margin: 10pt 0; word-break: break-all; }
code { font-family: 'Courier New', monospace; font-size: 9.5pt; background: #f4f4f4; padding: 1pt 4pt; }
.page-break { page-break-after: always; }
.caption-section { page-break-before: always; }
```

## 15-page structure (proven Kinabalu Two-Oceanics)

| Page | Section | Content |
|---|---|---|
| 1 | Cover | Title, subtitle, author, claim ID, abstract (yellow box), keywords |
| 2 | §1 Core Eureka | Contrast score table |
| 3 | §2 Regional Context | Figure 1 regional map + plate boundaries |
| 4 | §3 Cross-Section | Figure 2 block diagram + Geophysical discriminator (red box) |
| 5-6 | §4 Rock-Physics | Figure 3 bar charts + detailed table + Vp/Vs interpretation |
| 7 | §5 Three-Step Evolution | Figure 4 timeline + Falsified callout |
| 8 | §6 Jurassic Carbonate Décollement | Mechanism + KT-7 Franke RC |
| 9 | §7 Biostratigraphic Tie | 12-row NN-zone table |
| 10-11 | §8 Falsification Framework | GEOX-LC-001 4-hypothesis table + killer tests + acquisition sequence |
| 12 | §9 Model Contrast | Figure 5 model comparison matrix |
| 13-14 | §10-11 Receipts & Conclusions | SHA256 + GEOX claim + arifOS judgment + 6 conclusions |
| 15 | §12 References + Footer | 14 citations + DITEMPA BUKAN DIBERI |

## weasyprint gotchas

- **`box-shadow` ignored** — harmless warning, don't try to fix
- **Wide-aspect images** (e.g. 3971×964 cross-section) NEED `max-width: 100%` in CSS or they overflow
- **Header overlap on tables** — use `<table>` with explicit `<th>` background, NOT matplotlib's `ax.table()` (that one overlaps on PDF render)
- **`page-break-before: always`** on each `<h2>` keeps figures+text paired cleanly
- **HTML img src** must be relative path AND same directory as HTML OR base_url must resolve
- **Empty/missing images** render as broken icons — verify with `ls /tmp/<project>/*.png` before weasyprint

## Verification

```bash
pdfinfo /root/output.pdf | grep -E "Pages|File size"   # should show 10-20 pages, 1-2 MB
sha256sum /root/output.pdf                              # for the receipt
pdftotext /root/output.pdf - | head -40                  # confirm text content
pdftoppm -png -r 100 -f 5 -l 5 /root/output.pdf /tmp/p5  # render page 5 for visual audit
```

## Why this beats reportlab on this box

- `reportlab` pip install: blocked by PEP 668 ("--break-system-packages" needed, risky)
- System `reportlab` not present
- `weasyprint` already installed system-wide, v68.1
- HTML/CSS authoring is faster than reportlab's ParagraphStyle + TableStyle
- Visual debug = open HTML in browser, fix CSS, regenerate PDF (faster than reportlab rebuild)
- LibreOffice `lowriter --convert-to pdf` is an alternative if pandoc/weasyprint fail