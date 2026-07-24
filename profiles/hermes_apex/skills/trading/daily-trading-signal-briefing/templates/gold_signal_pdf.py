#!/usr/bin/env python3
"""
XAUUSD Daily Signal PDF v3 — LONG ONLY + EXIT LEVELS
One-page, landscape A4, rakyat marhaen language.
Requires chart already generated at /tmp/gold_signal_chart.png
Run via: write_file(path) + terminal("python3 {path}")

PITFALL (2026-07-16): All signal-level variables MUST be defined here independently.
Chart and PDF run as separate processes — no shared state.
"""

import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm, mm

# Colors — DARK theme matching OANDA chart
BG_DARK  = colors.HexColor('#0d1117')
BG_CARD  = colors.HexColor('#161b22')
GREEN    = colors.HexColor('#3fb950')
RED      = colors.HexColor('#f85149')
BLUE     = colors.HexColor('#58a6ff')
ORANGE   = colors.HexColor('#f0883e')
GOLD     = colors.HexColor('#ffd700')
TEXT_MAIN = colors.HexColor('#e6edf3')
TEXT_DIM  = colors.HexColor('#8b949e')
WARN_BG  = colors.HexColor('#2d2000')
WARN_C   = colors.HexColor('#ffa500')

# ═══════════════════════════════════════════════════════════════
# EDIT THESE PER DAY — must match chart script values exactly
# ═══════════════════════════════════════════════════════════════
DATE_STR        = '16 JULY 2026'
BUY_ZONE_LOW    = 3995       # ← MUST DEFINE — used in verdict + zone labels
BUY_ZONE_HIGH   = 4015       # ← MUST DEFINE — used in verdict + zone labels
SL              = 3975       # ← MUST DEFINE — used in emergency exit
T1              = 4085       # ← MUST DEFINE
T2              = 4200       # ← MUST DEFINE
ENTRY_MID       = (BUY_ZONE_LOW + BUY_ZONE_HIGH) / 2
EVENT_WARNING   = '⚠️ RETAIL SALES HARI INI — Tunggu data keluar sebelum entry!'
VERDICT         = f'BUY di ${BUY_ZONE_LOW}-${BUY_ZONE_HIGH} | SL ${SL} | Target ${T1}-${T2} | R:R 1:{(T1-ENTRY_MID)/(ENTRY_MID-SL):.1f}/1:{(T2-ENTRY_MID)/(ENTRY_MID-SL):.1f}'
DISCLAIMER      = ('Ini bukan nasihat kewangan. Trade atas risiko sendiri. '
                   'Abang Udin ajar teknikal, bukan jamin untung. '
                   'Kalau tak yakin, TUNGGU. Market sentiasa ada esok.')

# BUY signal table — uses variables above for consistency
buy_data = [
    ['LEVEL', 'HARGA', 'NOTA'],
    ['ENTRY', f'${BUY_ZONE_LOW} - ${BUY_ZONE_HIGH}', 'Buy zone — tunggu candle close atas EMA 20'],
    ['STOP LOSS', f'${SL}', f'Risk = ${ENTRY_MID - SL:.0f} dari entry tengah'],
    ['TARGET 1', f'${T1} (+${T1 - ENTRY_MID:.0f})', f'R:R 1:{(T1-ENTRY_MID)/(ENTRY_MID-SL):.1f} — jual separuh (50%)'],
    ['TARGET 2', f'${T2} (+${T2 - ENTRY_MID:.0f})', f'R:R 1:{(T2-ENTRY_MID)/(ENTRY_MID-SL):.1f} — jual semua (100%)'],
    ['STATUS', 'READY ⚡', 'Tunggu data dulu kalau ada event'],
]

# EXIT LEVELS table (if already holding) — uses variables above
exit_data = [
    ['LEVEL', 'HARGA', 'ACTION'],
    ['TAKE PROFIT 1', f'${T1}', 'Jual separuh (50%) — lock profit'],
    ['TAKE PROFIT 2', f'${T2}', 'Jual semua (100%) — kaut untung'],
    ['TRAIL STOP', f'${ENTRY_MID:.0f}', 'Naikkan SL ke entry selepas TP1'],
    ['EMERGENCY EXIT', f'${SL}', 'Cut loss — jangan tunggu!'],
]

# Macro context (add per day — market conditions, data releases, sentiment)
MACRO_CONTEXT = (
    '<b>KONTEKS:</b> CPI US Jun 3.5% (sebelum 4.2%) — lebih sejuk dari jangkaan. '
    'Fed rate 3.75%. PPI juga sejuk (-0.3% MoM). '
    'RSI neutral-bearish. Support kukuh di buy zone.'
)

# ═══════════════════════════════════════════════════════════════
# BUILD PDF — DARK THEME
# ═══════════════════════════════════════════════════════════════
page_w, page_h = landscape(A4)
pdf_path = f'/root/GOLD-SIGNAL-{DATE_STR.replace(" ", "-").lower()}.pdf'

doc = SimpleDocTemplate(
    pdf_path, pagesize=landscape(A4),
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.2*cm, bottomMargin=1.2*cm,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title2', parent=styles['Title'],
    fontSize=20, textColor=GOLD, spaceAfter=2*mm,
    fontName='Helvetica-Bold', alignment=1)
subtitle_style = ParagraphStyle('Subtitle2', parent=styles['Normal'],
    fontSize=11, textColor=TEXT_DIM, spaceAfter=4*mm,
    fontName='Helvetica', alignment=1)
section_style = ParagraphStyle('Section', parent=styles['Heading2'],
    fontSize=13, textColor=BLUE, spaceBefore=3*mm, spaceAfter=2*mm,
    fontName='Helvetica-Bold')
small_style = ParagraphStyle('Small2', parent=styles['Normal'],
    fontSize=7.5, textColor=TEXT_DIM, leading=10, fontName='Helvetica')
verdict_style = ParagraphStyle('Verdict', parent=styles['Normal'],
    fontSize=12, textColor=GOLD, spaceBefore=3*mm, spaceAfter=2*mm,
    fontName='Helvetica-Bold', alignment=1,
    borderColor=GOLD, borderWidth=1.5, borderPadding=8)
warn_style = ParagraphStyle('Warn', parent=styles['Normal'],
    fontSize=10, textColor=WARN_C,
    fontName='Helvetica-Bold', alignment=1,
    spaceBefore=2*mm, spaceAfter=2*mm)
macro_style = ParagraphStyle('Macro', parent=styles['Normal'],
    fontSize=9, textColor=TEXT_DIM, fontName='Helvetica',
    spaceBefore=2*mm, spaceAfter=2*mm)

story = []

# Title
story.append(Paragraph(f'XAUUSD DAILY SIGNAL — {DATE_STR}', title_style))
story.append(Paragraph('Gold / US Dollar | OANDA Style | Rakyat Marhaen | LONG ONLY', subtitle_style))

# Chart
chart_path = '/tmp/gold_signal_chart.png'
if os.path.exists(chart_path):
    img = Image(chart_path, width=28*cm, height=15.5*cm)
    img.hAlign = 'CENTER'
    story.append(img)
else:
    story.append(Paragraph('[CHART MISSING]', small_style))

story.append(Spacer(1, 3*mm))
story.append(Paragraph(EVENT_WARNING, warn_style))

# Two tables side by side: BUY signal + EXIT LEVELS
story.append(Paragraph('SIGNAL & EXIT', section_style))

buy_col = [3.5*cm, 6*cm]
exit_col = [3.5*cm, 6*cm]

buy_table = Table(buy_data, colWidths=buy_col, repeatRows=1)
exit_table = Table(exit_data, colWidths=exit_col, repeatRows=1)

table_style_buy = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a2332')),
    ('TEXTCOLOR', (0, 0), (-1, 0), BLUE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_MAIN),
    ('BACKGROUND', (0, 1), (-1, -1), BG_CARD),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ('TOPPADDING', (0, 1), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#30363d')),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 1), (0, -1), GREEN),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#0d2818')),
    ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#2d1215')),
    ('TEXTCOLOR', (0, 2), (0, 2), RED),
])

table_style_exit = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a2332')),
    ('TEXTCOLOR', (0, 0), (-1, 0), ORANGE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_MAIN),
    ('BACKGROUND', (0, 1), (-1, -1), BG_CARD),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ('TOPPADDING', (0, 1), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#30363d')),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 1), (0, -1), GREEN),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#0d2818')),
    ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#2d1215')),
    ('TEXTCOLOR', (0, -1), (0, -1), RED),
    ('TEXTCOLOR', (1, -1), (1, -1), RED),
])

buy_table.setStyle(table_style_buy)
exit_table.setStyle(table_style_exit)

# Combine side by side
combined = Table([[buy_table, exit_table]], colWidths=[10*cm, 10*cm])
combined.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
]))
story.append(combined)

# Verdict
story.append(Spacer(1, 3*mm))
story.append(Paragraph(f'VERDIKT: {VERDICT}', verdict_style))

# Macro context
story.append(Paragraph(MACRO_CONTEXT, macro_style))

# Disclaimer
story.append(Spacer(1, 2*mm))
story.append(Paragraph(DISCLAIMER, small_style))

# Dark background on every page
def set_dark_bg(canvas_obj, doc_obj):
    canvas_obj.saveState()
    canvas_obj.setFillColor(BG_DARK)
    canvas_obj.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    canvas_obj.restoreState()

doc.build(story, onFirstPage=set_dark_bg, onLaterPages=set_dark_bg)
print(f"PDF saved: {pdf_path}")
print(f"Size: {os.path.getsize(pdf_path)} bytes")
print(f"Entry mid: ${ENTRY_MID}, Risk: ${ENTRY_MID - SL:.0f}, R:R TP1=1:{(T1-ENTRY_MID)/(ENTRY_MID-SL):.1f}, TP2=1:{(T2-ENTRY_MID)/(ENTRY_MID-SL):.1f}")
