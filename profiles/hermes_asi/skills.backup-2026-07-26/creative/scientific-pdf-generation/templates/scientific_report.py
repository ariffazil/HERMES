#!/usr/bin/env python3
"""
Scientific Report PDF — Minimal Scaffold
=========================================
Copy this file and modify for your document.
Replace: title, sections, figures, references.

Requirements: reportlab (pip install reportlab)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate,
    Paragraph, Spacer, Image, PageBreak, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────
OUT_DIR = Path("/root/your/output/dir")  # CHANGE THIS
PDF_PATH = OUT_DIR / "your-report.pdf"   # CHANGE THIS

# ── Colors ─────────────────────────────────────────────────────────────
BLACK = HexColor("#1a1a1a")
DARK_GRAY = HexColor("#333333")
MED_GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#999999")
RULE_GRAY = HexColor("#cccccc")
ACCENT = HexColor("#2c5f8a")

# ── Layout ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 2.5*cm, 2.5*cm, 3.0*cm, 2.5*cm
TEXT_W = PAGE_W - ML - MR
COL_GAP = 0.5 * cm
COL_W = (TEXT_W - COL_GAP) / 2

# ── Fonts ──────────────────────────────────────────────────────────────
SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"
SANS_B = "Helvetica-Bold"


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(ML, PAGE_H - MT + 0.8*cm, PAGE_W - MR, PAGE_H - MT + 0.8*cm)
    canvas.setFont(SERIF_I, 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawString(ML, PAGE_H - MT + 1.0*cm, "Your Document Title — Year")
    canvas.line(ML, MB - 0.5*cm, PAGE_W - MR, MB - 0.5*cm)
    canvas.setFont(SERIF, 8)
    canvas.drawCentredString(PAGE_W/2, MB - 1.0*cm, f"— {doc.page} —")
    canvas.restoreState()


def title_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(SERIF_I, 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(PAGE_W/2, MB - 1.0*cm, "Your Footer Text")
    canvas.restoreState()


def build():
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
    S["title"] = ParagraphStyle("Title", fontName=SERIF_B, fontSize=22, leading=28,
                                 textColor=BLACK, alignment=TA_CENTER, spaceAfter=6*mm)
    S["subtitle"] = ParagraphStyle("Subtitle", fontName=SERIF_I, fontSize=14, leading=18,
                                    textColor=DARK_GRAY, alignment=TA_CENTER, spaceAfter=8*mm)
    S["section"] = ParagraphStyle("Section", fontName=SANS_B, fontSize=13, leading=17,
                                   textColor=BLACK, spaceBefore=10*mm, spaceAfter=4*mm)
    S["body"] = ParagraphStyle("Body", fontName=SERIF, fontSize=10, leading=14,
                                textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=3*mm)
    S["caption"] = ParagraphStyle("Caption", fontName=SERIF, fontSize=9, leading=12,
                                   textColor=DARK_GRAY, spaceBefore=2*mm, spaceAfter=5*mm)
    S["ref"] = ParagraphStyle("Ref", fontName=SERIF, fontSize=9, leading=12,
                               textColor=DARK_GRAY, leftIndent=1*cm, firstLineIndent=-1*cm,
                               spaceAfter=1.5*mm)

    story = []

    # ── Title Page ─────────────────────────────────────────────────────
    story.append(Spacer(1, 3.5*cm))
    story.append(Paragraph("Your Title Here", S["title"]))
    story.append(Paragraph("Your Subtitle", S["subtitle"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Author / Organization", S["body"]))
    story.append(Paragraph("Date", S["body"]))
    story.append(NextPageTemplate("ContentPage"))
    story.append(PageBreak())

    # ── Abstract ───────────────────────────────────────────────────────
    abstract_style = ParagraphStyle("Abstract", fontName=SERIF, fontSize=9.5, leading=13.5,
                                     textColor=DARK_GRAY, alignment=TA_JUSTIFY,
                                     leftIndent=2*cm, rightIndent=2*cm, spaceAfter=3*mm)
    story.append(Paragraph("ABSTRACT", ParagraphStyle("AbsLabel", fontName=SANS_B, fontSize=10,
                                                        alignment=TA_CENTER, spaceAfter=3*mm)))
    story.append(Paragraph("Your abstract text here.", abstract_style))
    story.append(Spacer(1, 5*mm))

    # ── Sections ───────────────────────────────────────────────────────
    story.append(Paragraph("1. Introduction", S["section"]))
    story.append(Paragraph("Body text here. Use TA_JUSTIFY for clean paragraphs.", S["body"]))

    # ── Figure example ─────────────────────────────────────────────────
    # fig = Image(str(OUT_DIR / "fig1.png"), width=15.5*cm, height=10*cm)
    # story.append(fig)
    # story.append(Paragraph("<b>Figure 1.</b> Caption with <i>epistemic label</i>.", S["caption"]))

    # ── References ─────────────────────────────────────────────────────
    story.append(Paragraph("References", S["section"]))
    story.append(Paragraph(
        "Author, A. (2026). Title. <i>Journal</i>, volume, pages.", S["ref"]))

    doc.build(story)
    print(f"✅ PDF: {PDF_PATH} ({PDF_PATH.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    build()
