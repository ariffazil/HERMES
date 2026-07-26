# Mode B — Marketing Pitch Deck Pattern

When to use: personal pitch decks, product one-pagers, AI agent proposals, trading tool introductions, lifestyle-brand documents. Audience is a single person or small group — not an institution, not a conference.

Distinct from the standard Mode B intelligence dossier (BaseDocTemplate with headers/footers). This pattern uses **direct canvas construction** — each page is a standalone composition with no running header/footer. More flexible for mixed layouts (cards, diagrams, comparison panels).

## Orientation

- **Landscape A4** for pitch decks (wider canvas = better for side-by-side layouts)
- Portrait A4 for single-column briefings

## Construction Pattern (direct canvas, NOT Platypus)

```python
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

W, H = landscape(A4)
c = canvas.Canvas(OUT, pagesize=landscape(A4))

def bg():
    c.setFillColor(HexColor('#0d1117'))
    c.rect(0, 0, W, H, fill=1, stroke=0)

def gold_line(y, x1=60, x2=None):
    if x2 is None: x2 = W - 60
    c.setStrokeColor(HexColor('#f0a500'))
    c.setLineWidth(1.5)
    c.line(x1, y, x2, y)

def panel(x, y, w, h, radius=6):
    c.setFillColor(HexColor('#161b22'))
    c.setStrokeColor(HexColor('#30363d'))
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

def text(x, y, txt, size=12, color=HexColor('#e6edf3'),
         font='Helvetica', align='left'):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == 'center':   c.drawCentredString(x, y, txt)
    elif align == 'right':  c.drawRightString(x, y, txt)
    else:                   c.drawString(x, y, txt)

# Each page: bg() → content → c.showPage()
bg()
# ... draw content ...
c.showPage()
c.save()
```

## Card Layout Pattern

Used for lists of features, blindspots, agents, etc. Each card = panel + icon + title + description.

```python
y = H - 120  # start from top
for i, (title, desc, consequence) in enumerate(items):
    panel(50, y - 95, W - 100, 90, radius=4)

    # Number circle (gold filled, dark text)
    cx, cy = 85, y - 50
    c.setFillColor(GOLD)
    c.circle(cx, cy, 14, fill=1, stroke=0)
    c.setFillColor(BG)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(cx, cy - 5, str(i + 1))

    # Title (amber) + description (text) + consequence (red)
    text(115, y - 30, title, size=15, color=AMBER, font='Helvetica-Bold')
    text(115, y - 50, desc, size=10, color=TEXT)
    text(115, y - 70, consequence, size=10, color=RED)

    y -= 100  # card spacing
```

## Flow Diagram Pattern

Two-row zigzag flow: top row L→R, bottom row R→L. Color-coded boxes by function.

```python
box_w, box_h = 110, 65
gap = 18

# Color map per function
colors_map = {
    'SCOUT': AMBER, 'PATTERN': GOLD, 'RISK': RED,
    'YOU': GREEN, 'JOURNAL': AMBER, 'WATCHDOG': RED,
    'REPORT': GOLD, 'RESULT': GREEN,
}

# Draw box
c.setFillColor(PANEL)
c.setStrokeColor(col)
c.setLineWidth(1.5)
c.roundRect(x, y, box_w, box_h, 6, fill=1, stroke=1)

# Arrow between boxes
ax = x + box_w + 2
ay = y + box_h / 2
c.setStrokeColor(DIM)
c.setLineWidth(1.2)
c.line(ax, ay, ax + gap - 4, ay)
c.line(ax + gap - 6, ay + 4, ax + gap - 2, ay)  # arrowhead top
c.line(ax + gap - 6, ay - 4, ax + gap - 2, ay)  # arrowhead bottom

# Vertical connector between rows
c.line(x_mid, row1_y - 2, x_mid, row2_y + box_h + 6)
```

## Before/After Comparison Pattern

Two side-by-side panels with color-coded headers.

```python
bw = (W - 150) / 2  # half width each
bh = 200

# BEFORE panel (red accent)
panel(bx, by, bw, bh)
text(bx + bw/2, by + bh - 25, 'SEBELUM', size=18, color=RED,
     font='Helvetica-Bold', align='center')
c.setStrokeColor(RED)
c.setLineWidth(2)
c.line(bx + 20, by + bh - 38, bx + bw - 20, by + bh - 38)

# AFTER panel (green accent)
panel(ax2, by, bw, bh)
text(ax2 + bw/2, by + bh - 25, 'SELEPAS', size=18, color=GREEN,
     font='Helvetica-Bold', align='center')
c.setStrokeColor(GREEN)
c.setLineWidth(2)
c.line(ax2 + 20, by + bh - 38, ax2 + bw - 20, by + bh - 38)

# Arrow between
text(bx + bw + 15, by + bh/2, '>>>', size=24, color=GOLD, font='Helvetica-Bold')
```

## Page Structure for Pitch Deck

Standard 6-page pitch deck spine:

1. **Cover** — large title (gold), subtitle (amber), tagline (dim), gold accent lines framing title, prepared-for line at bottom
2. **Problem** — numbered card list (blindspots, pain points), each with title + description + consequence in red
3. **Solution** — numbered card list (agents, features), each with icon box + title + description + green tagline
4. **How it works** — flow diagram (color-coded boxes + arrows), key principle callout box at bottom
5. **Lifestyle upgrade** — before/after comparison panels, key benefits checklist below
6. **Closing** — validation message, value proposition, CTA box, final tagline

## Typography Notes

- **No emojis** — use text symbols: `[S]`, `[+]`, `[x]`, `[=]`, `[~]`, `>>>`, `>`
- **BM-English mix** works well for Malaysian audience — keep casual, Penang style
- Body: 10-11pt Helvetica. Titles: 24-28pt Helvetica-Bold. Section headers: 15-18pt.
- Page numbers: 9pt dim, centered at bottom

## Visual Verification

After generating, convert to PNGs and inspect:

```bash
pdftoppm -png -r 150 output.pdf /tmp/page_preview
# Then use vision_analyze on each page image
```

This catches layout issues (overlapping text, misaligned cards, clipped content) that text-based checks miss.

## Proven

- 2026-07-14: Abang Sado × AI pitch deck (6 pages, landscape A4, dark/gold theme, card layouts, flow diagram, before/after panels). 12KB output. All 6 pages visually verified clean.
