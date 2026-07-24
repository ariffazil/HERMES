#!/usr/bin/env python3
"""
Geological Intelligence Dossier — Template
============================================
Domain-specific intelligence report with reportlab + matplotlib.
Proven: 2026-07-07, PTTEP Block K Deepwater Sabah dossier (10 pages, 5 figures, 829 KB).

Structure:
  1. Title page (info table, classification, quote)
  2. Executive Summary
  3. Regional geological setting + map figure
  4. Stratigraphy + column figure
  5. Activity timeline + timeline figure
  6. Strategy analysis + diagram figure
  7. Play types / resource potential + chart figure
  8. Implications / recommendations (callout boxes)
  9. Quick reference table
  10. Questions to ask in the room
  11. References (hanging indent)
  12. Epistemic band table
  13. Provenance disclaimer

Key patterns:
  - DejaVu fonts MUST be registered via pdfmetrics (see pitfalls in SKILL.md)
  - TableStyle TEXTCOLOR needs one command per row (see pitfalls)
  - Figures: matplotlib with white theme, muted colors, serif fonts
  - Callout boxes: ParagraphStyle with backColor + borderPadding
  - Info tables: key-value layout for metadata

Modify: replace title, content, figures, references. Keep structure.
"""

# ── Font Registration (REQUIRED — see SKILL.md pitfalls) ──────────────
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-BoldItalic', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf'))
pdfmetrics.registerFontFamily('DejaVuSerif',
    normal='DejaVuSerif', bold='DejaVuSerif-Bold',
    italic='DejaVuSerif-Italic', boldItalic='DejaVuSerif-BoldItalic')

# ── Imports ───────────────────────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate,
    Paragraph, Spacer, Image, PageBreak, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# ── Config ────────────────────────────────────────────────────────────
OUT_DIR = Path("/tmp/dossier_output")
OUT_DIR.mkdir(exist_ok=True)
PDF_PATH = OUT_DIR / "dossier.pdf"

# ── Colors ────────────────────────────────────────────────────────────
BLACK = HexColor("#1a1a1a")
DARK_GRAY = HexColor("#333333")
MED_GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#999999")
RULE_GRAY = HexColor("#cccccc")
ACCENT = HexColor("#1a5276")

# ── Layout ────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 2.5*cm, 2.5*cm, 3.0*cm, 2.5*cm
TEXT_W = PAGE_W - ML - MR

# ── Fonts (registered above — NO SPACES in names) ────────────────────
SERIF = "DejaVuSerif"
SERIF_B = "DejaVuSerif-Bold"
SERIF_I = "DejaVuSerif-Italic"
SANS_B = "Helvetica-Bold"

# ── Matplotlib white theme ───────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "text.color": "#1a1a1a",
    "axes.labelcolor": "#1a1a1a",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.edgecolor": "#666666",
    "grid.color": "#cccccc",
    "grid.alpha": 0.5,
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Liberation Serif"],
    "font.size": 10,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


# ── Header/Footer ────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(ML, PAGE_H - MT + 0.8*cm, PAGE_W - MR, PAGE_H - MT + 0.8*cm)
    canvas.setFont(SERIF_I, 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawString(ML, PAGE_H - MT + 1.0*cm, "Document Title — Year")
    canvas.drawRightString(PAGE_W - MR, PAGE_H - MT + 1.0*cm, "CONFIDENTIAL")
    canvas.line(ML, MB - 0.5*cm, PAGE_W - MR, MB - 0.5*cm)
    canvas.setFont(SERIF, 8)
    canvas.drawCentredString(PAGE_W/2, MB - 1.0*cm, f"— {doc.page} —")
    canvas.restoreState()


def title_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(SERIF_I, 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(PAGE_W/2, MB - 1.0*cm, "Footer text")
    canvas.restoreState()


def build_pdf():
    doc = BaseDocTemplate(str(PDF_PATH), pagesize=A4,
                          leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)
    content_frame = Frame(ML, MB, PAGE_W - ML - MR, PAGE_H - MT - MB, id="content")
    title_frame = Frame(ML, MB, PAGE_W - ML - MR, PAGE_H - MT - MB, id="title")
    doc.addPageTemplates([
        PageTemplate(id="TitlePage", frames=[title_frame], onPage=title_footer),
        PageTemplate(id="ContentPage", frames=[content_frame], onPage=header_footer),
    ])

    # Styles
    S = {}
    S["title"] = ParagraphStyle("Title", fontName=SANS_B, fontSize=24, leading=30,
                                 textColor=BLACK, alignment=TA_CENTER, spaceAfter=4*mm)
    S["subtitle"] = ParagraphStyle("Subtitle", fontName=SERIF_I, fontSize=13, leading=17,
                                    textColor=DARK_GRAY, alignment=TA_CENTER, spaceAfter=6*mm)
    S["section"] = ParagraphStyle("Section", fontName=SANS_B, fontSize=13, leading=17,
                                   textColor=ACCENT, spaceBefore=10*mm, spaceAfter=4*mm)
    S["body"] = ParagraphStyle("Body", fontName=SERIF, fontSize=10, leading=14,
                                textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=3*mm)
    S["caption"] = ParagraphStyle("Caption", fontName=SERIF_I, fontSize=9, leading=12,
                                   textColor=MED_GRAY, spaceBefore=2*mm, spaceAfter=5*mm)
    S["ref"] = ParagraphStyle("Ref", fontName=SERIF, fontSize=9, leading=12,
                               textColor=DARK_GRAY, leftIndent=1*cm, firstLineIndent=-1*cm,
                               spaceAfter=1.5*mm)
    S["callout"] = ParagraphStyle("Callout", fontName=SERIF, fontSize=9, leading=13,
                                   textColor=DARK_GRAY, alignment=TA_JUSTIFY,
                                   leftIndent=0.5*cm, rightIndent=0.5*cm, spaceAfter=3*mm,
                                   backColor=HexColor("#f0f4f8"), borderPadding=6)

    story = []

    # ── TITLE PAGE ────────────────────────────────────────────────────
    story.append(Spacer(1, 3.0*cm))
    story.append(Paragraph("Title Here", S["title"]))
    story.append(Paragraph("Subtitle", S["subtitle"]))
    story.append(Spacer(1, 1.5*cm))

    # Info table (key-value metadata)
    info_data = [
        ['Prepared for', 'Recipient — Role, Organization'],
        ['Subject', 'Subject description'],
        ['Date', 'July 2026'],
        ['Classification', 'Confidential — For Discussion Only'],
    ]
    info_table = Table(info_data, colWidths=[3.5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), SANS_B, 9),
        ('FONT', (1, 0), (1, -1), SERIF, 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('TEXTCOLOR', (0, 0), (0, -1), ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, RULE_GRAY),
    ]))
    story.append(info_table)
    story.append(NextPageTemplate("ContentPage"))
    story.append(PageBreak())

    # ── SECTIONS ──────────────────────────────────────────────────────
    story.append(Paragraph("1. Section Title", S["section"]))
    story.append(Paragraph("Body text here.", S["body"]))

    # ── FIGURE EXAMPLE ────────────────────────────────────────────────
    # fig = Image(str(OUT_DIR / "fig.png"), width=15.5*cm, height=10*cm)
    # story.append(fig)
    # story.append(Paragraph("<b>Figure 1.</b> Caption. <i>[OBS — source.]</i>", S["caption"]))

    # ── CALLOUT BOX ───────────────────────────────────────────────────
    story.append(Paragraph(
        "<b>Key Takeaway:</b> Important insight here.", S["callout"]))

    # ── REFERENCES ────────────────────────────────────────────────────
    story.append(Paragraph("References", S["section"]))
    story.append(Paragraph(
        "Author, A. (2026). Title. <i>Journal</i>, volume, pages.", S["ref"]))

    # ── EPISTEMIC BAND ────────────────────────────────────────────────
    ep_data = [
        ['Band', 'Meaning'],
        ['OBS', 'Observed (direct measurement)'],
        ['DER', 'Derived (computed)'],
        ['INT', 'Interpreted (reasoning)'],
        ['SPEC', 'Speculated (conceptual)'],
    ]
    ep_table = Table(ep_data, colWidths=[2*cm, 13.5*cm])
    ep_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), SANS_B, 8),
        ('FONT', (0, 1), (-1, -1), SERIF, 8),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#e8e8e8")),
        ('TEXTCOLOR', (0, 0), (-1, 0), BLACK),
        ('GRID', (0, 0), (-1, -1), 0.5, RULE_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(ep_table)

    doc.build(story)
    print(f"PDF: {PDF_PATH} ({PDF_PATH.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    build_pdf()
