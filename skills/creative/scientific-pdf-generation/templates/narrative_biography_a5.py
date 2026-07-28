#!/usr/bin/env python3
"""
Mode E: A5 Narrative Biography Booklet (reportlab)
===================================================
Forge a Walter Isaacson-style biography PDF in A5 booklet format.
Cream background, Times-Roman serif body, gold accents, chapter structure.

HOW TO USE:
  1. Copy this file and rename for your subject
  2. Replace all placeholder text marked with SUBJECT:
  3. Replace chapter titles, body text, and quotes
  4. Run: python3 your_script.py
  5. Output: /root/SUBJECT_BIOGRAPHY.pdf

REQUIREMENTS:
  pip install reportlab

COLOR PALETTE:
  Cream BG:  #f5f0e8
  Gold:      #c9a227
  Navy:      #16213e
  Dark:      #1a1a2e
  Grey:      #444444
  Dim grey:  #888888
"""

from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)

# ── CONFIG ──────────────────────────────────────────────────────
SUBJECT = "Full Name Here"
OUTPUT = f"/root/{SUBJECT.upper().replace(' ', '_')}_BIOGRAPHY.pdf"
TITLE = "THE BOOK TITLE HERE"
SUBTITLE = "The Making of [Subject]"

# ── COLORS ──────────────────────────────────────────────────────
GOLD   = HexColor("#c9a227")
NAVY   = HexColor("#16213e")
DARK   = HexColor("#1a1a2e")
CREAM  = HexColor("#f5f0e8")
GREY   = HexColor("#444444")
DIM    = HexColor("#888888")

# ── FONTS ───────────────────────────────────────────────────────
# Built-in: Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic
# For DejaVu Serif or Liberation Serif, register TTF:
#   from reportlab.pdfbase import pdfmetrics
#   from reportlab.pdfbase.ttfonts import TTFont
#   pdfmetrics.registerFont(TTFont("LibSerif", "/usr/share/fonts/.../LiberationSerif-Regular.ttf"))

SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"
SERIF_BI = "Times-BoldItalic"

# ── STYLES ──────────────────────────────────────────────────────
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'BookTitle', fontName=SERIF_B, fontSize=26, leading=32,
    textColor=GOLD, alignment=TA_CENTER, spaceAfter=4*mm,
)
subtitle_style = ParagraphStyle(
    'BookSub', fontName=SERIF_I, fontSize=14, leading=18,
    textColor=GOLD, alignment=TA_CENTER, spaceAfter=4*mm,
)
desc_style = ParagraphStyle(
    'Desc', fontName=SERIF_I, fontSize=11, leading=15,
    textColor=DIM, alignment=TA_CENTER, spaceAfter=10*mm,
)
chap_num_style = ParagraphStyle(
    'ChapterNum', fontName=SERIF_B, fontSize=11, leading=14,
    textColor=GOLD, alignment=TA_CENTER, spaceBefore=2*mm, spaceAfter=1*mm,
)
section_style = ParagraphStyle(
    'SectionHead', fontName=SERIF_B, fontSize=18, leading=24,
    textColor=GOLD, spaceBefore=8*mm, spaceAfter=4*mm,
)
body_style = ParagraphStyle(
    'Body', fontName=SERIF, fontSize=11, leading=15,
    textColor=DARK, alignment=TA_JUSTIFY, spaceBefore=1*mm, spaceAfter=2*mm,
)
quote_style = ParagraphStyle(
    'Quote', fontName=SERIF_I, fontSize=11, leading=15,
    textColor=GREY, alignment=TA_CENTER,
    leftIndent=12*mm, rightIndent=12*mm, spaceBefore=3*mm, spaceAfter=3*mm,
)
pull_style = ParagraphStyle(
    'Pull', fontName=SERIF_I, fontSize=13, leading=17,
    textColor=NAVY, alignment=TA_CENTER,
    leftIndent=8*mm, rightIndent=8*mm, spaceBefore=3*mm, spaceAfter=3*mm,
)
epilogue_style = ParagraphStyle(
    'Epilogue', fontName=SERIF_I, fontSize=10, leading=14,
    textColor=DIM, alignment=TA_CENTER, spaceBefore=10*mm,
)
footer_style = ParagraphStyle(
    'Footer', fontName=SERIF_I, fontSize=8, leading=10,
    textColor=DIM, alignment=TA_CENTER,
)

def hr():
    return HRFlowable(width="60%", thickness=0.5, color=GOLD,
                       spaceBefore=3*mm, spaceAfter=3*mm)

# ── BUILD ───────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A5,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=20*mm,
    )
    story = []

    # ── TITLE PAGE ──
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph(TITLE, title_style))
    story.append(Paragraph(SUBTITLE, subtitle_style))
    story.append(Spacer(1, 5*mm))
    story.append(hr())
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "One-line description of the book's scope here.",
        desc_style
    ))
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph(
        "\"A defining quotation from the subject here.\"",
        quote_style
    ))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("— Subject Name", ParagraphStyle(
        'Attribution', parent=desc_style, fontSize=10, textColor=DIM
    )))
    story.append(PageBreak())

    # ── CHAPTER 1 ──
    story.append(Paragraph("CHAPTER ONE", chap_num_style))
    story.append(Paragraph("Chapter Title Here", section_style))
    story.append(hr())

    story.append(Paragraph(
        "Body text paragraph one. Replace with the narrative biography content. "
        "Keep paragraphs tight — 3-5 sentences each. Use multiple paragraphs "
        "for a single chapter. End each chapter with a strong thematic close.",
        body_style
    ))
    story.append(Paragraph(
        "Second paragraph continuing the narrative thread. The writing should "
        "be scene-driven and causal — connect events through thematic threads, "
        "not just chronology.",
        body_style
    ))

    # Optional pull quote
    story.append(Paragraph(
        "\"A memorable quote from the subject or a contemporary source, "
        "set apart for emphasis.\"",
        pull_style
    ))

    story.append(Paragraph(
        "Continue the chapter after the pull quote. This pattern — "
        "body → pull quote → body — creates rhythm.",
        body_style
    ))

    # ── CHAPTER 2 (add more chapters following same pattern) ──
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("CHAPTER TWO", chap_num_style))
    story.append(Paragraph("Second Chapter Title", section_style))
    story.append(hr())

    story.append(Paragraph(
        "Chapter 2 body text. Repeat the pattern: chapter number, title, "
        "gold rule, body paragraphs, optional quotes.",
        body_style
    ))

    # ── ADD MORE CHAPTERS: copy the CHAPTER pattern above ──

    # ── EPILOGUE ──
    story.append(Spacer(1, 8*mm))
    story.append(hr())
    story.append(Paragraph("EPILOGUE", chap_num_style))
    story.append(Paragraph("The Long Game", section_style))
    story.append(hr())

    story.append(Paragraph(
        "Closing thoughts here. Tie the early arc to the subject's later "
        "achievements. End with a resonant thematic sentence.",
        body_style
    ))

    # ── FINAL ATTRIBUTION ──
    story.append(Spacer(1, 10*mm))
    story.append(hr())
    story.append(Paragraph(
        "Born [DATE], [PLACE] · [KEY HONOURS]",
        footer_style
    ))
    story.append(Paragraph(
        "Sources: [List key sources at end, no inline footnotes]",
        ParagraphStyle('Sources', parent=footer_style, fontSize=7, textColor=DIM)
    ))

    doc.build(story)
    print(f"PDF generated: {OUTPUT}")

if __name__ == "__main__":
    build()
