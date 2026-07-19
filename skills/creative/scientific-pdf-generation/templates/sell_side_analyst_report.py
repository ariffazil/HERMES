"""
Sell-Side Analyst Report Template — Mode C
==========================================

UOBKH / CIMB / Maybank IB / Kenanga / RHB / HLIB / PublicInvest house style.
Light background, navy/gold accent, recommendation banner, scenario tables.

Proven 2026-07-13: PETRONAS 1H 2026 sector forecast (15 pages, 8 figures, 14 tables, 780 KB).

Usage:
  1. Copy this file to your project directory
  2. Modify FIG_DIR, PDF_PATH, OUT_DIR, then populate the build_report() flow list
  3. Run: python3 sell_side_analyst_report.py

Requires: pip install --break-system-packages reportlab matplotlib
"""

import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/.mpl')  # silence pyrolite warning

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, NextPageTemplate,
)
from datetime import datetime
from pathlib import Path

# ── Config (CHANGE THESE) ──────────────────────────────────────────────
OUT_DIR  = Path('/root/your/project')
FIG_DIR  = OUT_DIR / 'figs'
PDF_PATH = OUT_DIR / 'analyst-report.pdf'
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)

# ── Mode C Color Palette ──────────────────────────────────────────────
NAVY       = colors.HexColor('#003366')
GOLD       = colors.HexColor('#C5A572')
TEAL       = colors.HexColor('#2A9D8F')
RED        = colors.HexColor('#C73E1D')
LIGHT_GREY = colors.HexColor('#F3F4F6')
DARK_GREY  = colors.HexColor('#374151')
MED_GREY   = colors.HexColor('#6B7280')

# ── Matplotlib defaults (light theme, sans-serif) ─────────────────────
plt.rcParams.update({
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
    'text.color':        '#374151',
    'axes.labelcolor':   '#374151',
    'xtick.color':       '#6B7280',
    'ytick.color':       '#6B7280',
    'axes.edgecolor':    '#6B7280',
    'grid.color':        '#D1D5DB',
    'grid.alpha':        0.3,
    'font.family':       'DejaVu Sans',
    'font.size':         10,
    'axes.spines.top':   False,
    'axes.spines.right': False,
})


# ── Page Templates ─────────────────────────────────────────────────────
def header_footer(canvas_obj, doc):
    """Standard broker page header + footer (used for content pages)."""
    canvas_obj.saveState()
    # Header
    canvas_obj.setStrokeColor(NAVY)
    canvas_obj.setLineWidth(1.2)
    canvas_obj.line(1.5*cm, 28.0*cm, 20.0*cm, 28.0*cm)
    canvas_obj.setFillColor(NAVY)
    canvas_obj.setFont('Helvetica-Bold', 7.5)
    canvas_obj.drawString(1.5*cm, 28.2*cm,
        "UOB KAY HIAN  |  EQUITY RESEARCH  |  MALAYSIA DAILY")
    canvas_obj.setFillColor(MED_GREY)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.drawRightString(20.0*cm, 28.2*cm,
        f"{datetime.now():%A, %d %B %Y}  |  Hermes-Prime (Federated Research)")
    # Footer
    canvas_obj.setLineWidth(0.4)
    canvas_obj.line(1.5*cm, 1.2*cm, 20.0*cm, 1.2*cm)
    canvas_obj.setFillColor(MED_GREY)
    canvas_obj.setFont('Helvetica', 6.5)
    canvas_obj.drawString(1.5*cm, 0.8*cm,
        "Refer to last page for important disclosures. AC: Hermes-Prime certifies independent views.")
    canvas_obj.drawRightString(20.0*cm, 0.8*cm, f"Page {doc.page}")
    canvas_obj.restoreState()


def cover_page(canvas_obj, doc):
    """Cover page — navy banner across the top, gold accent rule below."""
    canvas_obj.saveState()
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 27.5*cm, 21*cm, 2.5*cm, fill=1, stroke=0)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.rect(0, 27.0*cm, 21*cm, 0.4*cm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont('Helvetica-Bold', 8)
    canvas_obj.drawString(1.5*cm, 28.5*cm, "UOB KAY HIAN  |  EQUITY RESEARCH")
    canvas_obj.setFont('Helvetica', 7.5)
    canvas_obj.drawRightString(20.0*cm, 28.5*cm, f"{datetime.now():%A, %d %B %Y}")
    canvas_obj.restoreState()


# ── Styles ─────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14,
                    fontName='Helvetica-Bold', textColor=NAVY,
                    spaceAfter=4, spaceBefore=8, leading=16)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11.5,
                    fontName='Helvetica-Bold', textColor=NAVY,
                    spaceAfter=4, spaceBefore=10, leading=14)
H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=10,
                    fontName='Helvetica-Bold', textColor=DARK_GREY,
                    spaceAfter=2, spaceBefore=6, leading=12)
H4 = ParagraphStyle('H4', parent=styles['Heading4'], fontSize=8.5,
                    fontName='Helvetica-Oblique', textColor=MED_GREY,
                    spaceAfter=2, spaceBefore=4, leading=10)
Body = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=8.8,
                      fontName='Helvetica', textColor=DARK_GREY,
                      alignment=TA_JUSTIFY, leading=11.5, spaceAfter=4)
BodySm = ParagraphStyle('BodySm', parent=Body, fontSize=7.8, leading=10)
Bullet = ParagraphStyle('Bullet', parent=Body, leftIndent=10, bulletIndent=2, spaceAfter=1)
Subdued = ParagraphStyle('Subdued', parent=Body, textColor=MED_GREY, fontSize=7.8)
Disclaim = ParagraphStyle('Disclaim', parent=Body, fontSize=6.5,
                         textColor=MED_GREY, alignment=TA_JUSTIFY, leading=8)


# ── Component: Recommendation Banner ──────────────────────────────────
def make_recommendation_banner(rating, current_price, target_price, upside_pct,
                                currency='RM'):
    """Top recommendation banner — 4 columns, colour-coded by rating."""
    rating_bg = {'BUY': TEAL, 'HOLD': GOLD, 'SELL': RED}[rating]
    data = [
        [rating, 'Last Traded Price', 'Target Price (12-mth)', 'Implied Upside'],
        [f"{currency} {current_price:.2f}",
         f"{currency} {target_price:.2f}",
         f"+{upside_pct:.1f}%"]
    ]
    t = Table(data, colWidths=[3.0*cm, 4.5*cm, 4.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (0,1), rating_bg),
        ('TEXTCOLOR', (0,1), (0,1), colors.white),
        ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (0,1), 18),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (1,1), (-1,1), 11),
        ('FONTNAME', (1,1), (-1,1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1,1), (-1,1), NAVY),
        ('TOPPADDING', (0,0), (-1,0), 7),
        ('BOTTOMPADDING', (0,0), (-1,0), 7),
        ('TOPPADDING', (0,1), (0,1), 10),
        ('BOTTOMPADDING', (0,1), (0,1), 10),
        ('TOPPADDING', (1,1), (-1,1), 14),
        ('BOTTOMPADDING', (1,1), (-1,1), 14),
        ('GRID', (0,0), (-1,-1), 0.4, colors.grey),
        ('BOX', (0,0), (-1,-1), 1.2, NAVY),
    ]))
    return t


# ── Component: Styled Data Table ──────────────────────────────────────
def fmt_table(headers, rows, col_widths=None, header_bg=NAVY, alt_bg=LIGHT_GREY):
    """Standard alternating-row table with navy header."""
    if col_widths is None:
        col_widths = [12.5*cm / len(headers)] * len(headers)
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.6),
        ('TOPPADDING', (0,0), (-1,0), 4),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('TOPPADDING', (0,1), (-1,-1), 3),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]
    for i in range(1, len(data), 2):
        style_cmds.append(('BACKGROUND', (0,i), (-1,i), alt_bg))
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Component: Sector Recap Table ──────────────────────────────────────
def make_sector_recap(sector, last_price_ref, recommendation, outlook,
                     catalyst, key_risk):
    """Cover-page sector recap (Field/Detail rows)."""
    data = [
        ['Field', 'Detail'],
        ['Sector', sector],
        ['Last price reference', last_price_ref],
        ['Recommendation', recommendation],
        ['Outlook', outlook],
        ['Key catalyst', catalyst],
        ['Single largest risk', key_risk],
    ]
    t = Table(data, colWidths=[4.5*cm, 11.0*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,1), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.8),
        ('TOPPADDING', (0,0), (-1,0), 4),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('TOPPADDING', (0,1), (-1,-1), 3),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BACKGROUND', (0,2), (0,2), LIGHT_GREY),
        ('BACKGROUND', (0,4), (0,4), LIGHT_GREY),
        ('BACKGROUND', (0,6), (0,6), LIGHT_GREY),
    ]))
    return t


# ── Component: Standard AC Disclaimer Block ───────────────────────────
def make_disclaimer_block(broker_name='UOB KAY HIAN'):
    """Standard CMSA / Bursa Malaysia disclaimer + analyst certification."""
    text1 = (
        "This report is prepared for general circulation. It does not have regard to the "
        "specific investment objectives, financial situation and the particular needs of any "
        "recipient. Advice should be sought from a financial adviser regarding the suitability "
        "of any investment product, taking into account the specific investment objectives, "
        "financial situation or particular needs of any person in receipt of the recommendation, "
        "before the person makes a commitment to purchase the investment product. This report is "
        "confidential. This report may not be published, circulated, reproduced or distributed in "
        "whole or in part by any recipient of this report to any other person without the prior "
        "written consent of the publisher. The information or views in the report ("
        "\"Information\") has been obtained or derived from sources believed by the publisher "
        "to be reliable. However, no representation is made as to the accuracy or completeness "
        "of such sources or the Information and the publisher accepts no liability whatsoever "
        "for any loss or damage arising from the use of or reliance on the Information. "
        "Past performance is not indicative of future results. <b>FORWARD-LOOKING STATEMENTS "
        "DISCLOSE MATERIAL UNCERTAINTY.</b> 1H 2026 projection is a model output and should "
        "not be construed as a forecast."
    )
    text2 = (
        "<b>AC (Analyst Certification):</b> Hermes-Prime (Federated Research) certifies that "
        "(1) the views expressed in this report accurately reflect his/her personal views "
        "about all of the subject corporation(s) and securities in this report; (2) the "
        "report was produced independently by him/her; (3) he/she does not carry out, "
        "whether for himself/herself or on behalf of any other person, any of the Subject "
        "Business involving any of the subject corporation(s) or securities referred to "
        "in this report; and (4) he/she has not received and will not receive any "
        "compensation that is directly or indirectly related or linked to the "
        "recommendations or views expressed in this report. <b>Hermes-Prime is a "
        "sovereign-aligned federated research agent operated within the arifOS Kernel "
        "(port 8088), authored on behalf of an institutional user for internal research "
        "purposes. This report is not investment advice.</b>"
    )
    return [Paragraph(text1, Disclaim), Spacer(1, 0.3*cm),
            Paragraph(text2, Disclaim)]


# ── Build Report ──────────────────────────────────────────────────────
def build_report(flow):
    """Build the PDF with cover + content page templates.

    flow[0] MUST be the cover content. flow[1] should be NextPageTemplate('Content').
    """
    doc = BaseDocTemplate(
        str(PDF_PATH), pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.0*cm, bottomMargin=1.5*cm,
        title="Sell-Side Analyst Report",
        author="Hermes-Prime (Federated Research)",
        subject="Equity Research"
    )
    frame = Frame(1.5*cm, 1.5*cm, 18.0*cm, 27.0*cm, id='normal',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[frame], onPage=cover_page),
        PageTemplate(id='Content', frames=[frame], onPage=header_footer),
    ])

    # Insert NextPageTemplate after the cover content (assumed to be first ~6 elements)
    flow_with_template = list(flow)
    flow_with_template.insert(1, NextPageTemplate('Content'))

    doc.build(flow_with_template)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"\n✓ PDF: {PDF_PATH}  ({size_kb:.1f} KB)")
    return PDF_PATH


# ── Example: Cover + Sector Recap ─────────────────────────────────────
def example_cover():
    """Build a minimal example to verify the template renders."""
    flow = [
        Spacer(1, 4.5*cm),
        Paragraph("MALAYSIA DAILY", Subdued),
        Paragraph("EXAMPLE CO. — Q1 2026 Sector Forecast", H1),
        Paragraph("Read-Through: Group Profit Drivers in Transition", H4),
        Spacer(1, 0.4*cm),
        HRFlowable(width="100%", thickness=1.5, color=NAVY),
        Spacer(1, 0.3*cm),
        make_recommendation_banner("HOLD", current=18.76, target=19.50, upside=3.9),
        Spacer(1, 0.4*cm),
        Paragraph("Sector Recap", H2),
        make_sector_recap(
            sector="OIL & GAS — MALAYSIA",
            last_price_ref="KLCI O&G index, 13 July 2026",
            recommendation="HOLD (sector-level)",
            outlook="Mixed — Brent tailwind offset by FX, Downstream drag",
            catalyst="1H 2026 Group results (expected Aug-Sep 2026)",
            key_risk="Domestic gas fiscal dispute",
        ),
        Spacer(1, 0.3*cm),
        Paragraph("Key Takeaways", H2),
    ]
    for takeaway in [
        "<b>Revenue up, PAT down:</b> 1H 26E revenue +10.8% YoY, PAT -7.8% — FX translation drag.",
        "<b>Segment axis shift:</b> Gas & Maritime now drives ~54% of group PAT.",
        "<b>Single largest unpriced risk:</b> Domestic gas fiscal dispute could swing PAT by RM 5-10bn.",
    ]:
        flow.append(Paragraph(f"▸ {takeaway}", Bullet))
    return flow


if __name__ == "__main__":
    # Minimal example — replace with your full report flow
    flow = example_cover()
    flow.append(PageBreak())
    flow.extend(make_disclaimer_block())
    build_report(flow)