# Canvas-Based PDF Wrapping (reportlab)

## When to Use

For single-page trading signal PDFs where you need precise control over
layout, accent lines, and text positioning. Preferred over SimpleDocTemplate
for one-page chart PDFs.

## Pattern

```python
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def create_signal_pdf(chart_png_path, pdf_path, now_myt):
    """Wrap a matplotlib-rendered chart PNG into a premium PDF."""
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    w, h = landscape(A4)

    # 1. Dark background fill
    c.setFillColor(HexColor('#0d1117'))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # 2. Gold accent line at top
    c.setStrokeColor(HexColor('#f0a500'))
    c.setLineWidth(2)
    c.line(20, h - 15, w - 20, h - 15)

    # 3. Chart image (fills ~85% of page)
    c.drawImage(chart_png_path, 20, 25, width=w-40, height=h-55,
                preserveAspectRatio=True, anchor='c')

    # 4. Footer text
    c.setFillColor(HexColor('#8b949e'))
    c.setFont('Courier', 7)
    c.drawString(20, 10,
                 f'Generated: {now_myt}  |  Abang Sado Udin  |  XAUUSD H1')

    # 5. Gold accent line at bottom
    c.setStrokeColor(HexColor('#b07800'))
    c.setLineWidth(1)
    c.line(20, 20, w - 20, 20)

    c.save()
```

## Key Points

- `landscape(A4)` = 842×595 points (wide format for charts)
- `preserveAspectRatio=True, anchor='c'` centers the chart without distortion
- Gold accent lines at top (2pt) and bottom (1pt, dimmer) frame the chart
- Footer text at y=10, gold line at y=20, chart bottom at y=25
- HexColor requires hex WITH `#` prefix
- DPI 150 for the PNG source is optimal (150 DPI × A4 landscape ≈ 2500×1750px)

## Pitfalls

- **Don't use SimpleDocTemplate for single-page chart PDFs** — it adds margins,
  headers, and flowable logic you don't need. Canvas is simpler and gives
  pixel-level control.
- **Don't draw text at y < 10** — it clips off the page bottom.
- **Gold line thickness**: 2pt top (bold), 1pt bottom (subtle). Same thickness
  looks flat.
