#!/usr/bin/env python3
"""
Starter template: 14-page reportlab PDF with cover + body + references + appendices.
Proven 2026-07-03 (Kinabalu Two-Oceanics, 1.4 MB, 14 pages).

Edit the SECTION FUNCTIONS for your own topic. Keep the header/footer + table styles.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
                                Table, TableStyle)
import os

# === Edit these for your topic ===
OUT = "/root/your_artifact.pdf"
COVER_IMG = "/root/your_block.png"
TITLE = "Your Artifact Title"
SUBTITLE = "Your subtitle / claim"
KEYWORDS = "keyword1, keyword2, keyword3"
CLAIM_ID = "your_claim_id_hex"

# === Colors (earth-tone palette) ===
BRAND = HexColor('#7a2e1a')
DEEP = HexColor('#1a3a6a')
WARM = HexColor('#8b6a3a')
SEAL = HexColor('#2c5f8a')
GOLD = HexColor('#a07a4f')
LIGHT = HexColor('#fbfaf6')
GRAY = HexColor('#444')

# === Styles ===
styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=20, leading=24,
                    textColor=BRAND, spaceAfter=12, fontName='Helvetica-Bold')
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, leading=18,
                    textColor=DEEP, spaceAfter=8, spaceBefore=14, fontName='Helvetica-Bold')
H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11.5, leading=14,
                    textColor=GOLD, spaceAfter=4, spaceBefore=8, fontName='Helvetica-Bold')
BODY = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5, fontName='Helvetica')
SMALL = ParagraphStyle('Small', parent=BODY, fontSize=8, leading=10, textColor=GRAY)
ABSTRACT = ParagraphStyle('Abstract', parent=BODY, fontSize=10, leading=14,
                          alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8,
                          spaceAfter=8, textColor=black, fontName='Helvetica-Oblique')
QUOTE = ParagraphStyle('Quote', parent=BODY, fontSize=11, leading=15,
                       alignment=TA_CENTER, textColor=BRAND, fontName='Helvetica-Oblique',
                       leftIndent=20, rightIndent=20, spaceAfter=10)
KERN = ParagraphStyle('Kern', parent=BODY, fontSize=10, leading=13, textColor=BRAND,
                      alignment=TA_CENTER, fontName='Helvetica-Bold',
                      leftIndent=10, rightIndent=10)
CAP = ParagraphStyle('Cap', parent=BODY, fontSize=8, leading=10, alignment=TA_CENTER,
                     textColor=GRAY, spaceAfter=8, fontName='Helvetica-Oblique')

def P(t, style=BODY):
    return Paragraph(t, style)

def tbl(data, colWidths=None):
    t = Table(data, colWidths=colWidths, repeatRows=1)
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.4, HexColor('#888')),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,0), BRAND),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ]
    t.setStyle(TableStyle(style))
    return t

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Oblique', 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 28.7*cm, f"{TITLE}  ·  arifOS Federation · F13 SOVEREIGN")
    canvas.drawRightString(19*cm, 28.7*cm, "DOI: arifos/2026.07.03-your-slug-v1")
    canvas.drawString(2*cm, 1.2*cm, "DITEMPA BUKAN DIBERI  ·  GEOX-LC sealed  ·  GEOX audit 2026-07-03")
    canvas.drawRightString(19*cm, 1.2*cm, f"Page {doc.page}")
    canvas.setStrokeColor(BRAND); canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.5*cm, 19*cm, 1.5*cm)
    canvas.restoreState()

# === Build document ===
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=1.5*cm, bottomMargin=1.8*cm,
                        title=TITLE, author='arifOS Federation · GEOX Earth Intelligence',
                        subject=SUBTITLE)
flow = []

# 1. Cover
flow.append(Spacer(1, 1*cm))
flow.append(P(TITLE, H1))
flow.append(P(SUBTITLE, ABSTRACT))
img = Image(COVER_IMG, width=17*cm, height=16.3*cm)
flow.append(img)
flow.append(P(f"Figure 1 (cover). Cross-section A–A′ (Panel B) with 3D block (Panel B′) and timeline (Panel C).", CAP))
flow.append(Spacer(1, 0.4*cm))
flow.append(P(f"<b>Keywords:</b> {KEYWORDS}", BODY))
flow.append(P("&#8220;Your kernel one-liner here.&#8221;", QUOTE))
flow.append(PageBreak())

# 2-13. Body sections
# (add your H2 + P + tbl blocks here, ending with PageBreak before references)

# 14. References
flow.append(P("REFERENCES", H2))
for ref in [
    "Author, A. (Year). Title. *Journal* Vol(Issue), Pages.",
    # ... add 10-20 more
]:
    flow.append(P(f"• {ref}", SMALL))
flow.append(PageBreak())

# Appendix
flow.append(P("APPENDIX A — GEOX LIVE AUDIT TRAIL", H2))
flow.append(P("All claims in this artifact were independently probed through the GEOX MCP server.", BODY))
# (add your audit table here)

flow.append(Spacer(1, 0.4*cm))
flow.append(P(f"<b>Sealed under arifOS Federation · GEOX-LC · F13 SOVEREIGN authority</b><br/>DITEMPA BUKAN DIBERI  ·  2026-07-03  ·  claim {CLAIM_ID}", KERN))

# === Build ===
doc.build(flow, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Saved {OUT}")
print(f"Size: {os.path.getsize(OUT)/1024:.1f} KB")
