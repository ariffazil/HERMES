#!/usr/bin/env python3
"""
APEX Dark Dossier PDF Generator — Mode B (intelligence briefing).

Combines:
  - Federation health table (7 organs)
  - WELL substrate assessment (H/M/G/C_WELL)
  - Full spec comparison table
  - APEX G computation with per-primitive breakdown
  - Floor compliance table (F1–F13)
  - Final verdict + recommendation
  - Audit trail (step-by-step call log)

Usage:
  python3 templates/apex_pdf_dark_dossier.py

Requires: reportlab
  pip install --break-system-packages --quiet reportlab

Dependencies:
  This template is designed to be populated with live data from an APEX
  computation. Edit the DATA DICTIONARY section before running.
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, PageBreak, HRFlowable
)

# ══════════════════════════════════════════════════
# COLOUR PALETTE — Mode B Dark Dossier
# ══════════════════════════════════════════════════
BG = colors.HexColor("#0d1117")
PANEL = colors.HexColor("#161b22")
GOLD = colors.HexColor("#f0a500")
AMBER = colors.HexColor("#ffa657")
GREEN = colors.HexColor("#3fb950")
BLUE = colors.HexColor("#58a6ff")
RED = colors.HexColor("#f85149")
TEAL = colors.HexColor("#39d2c0")
TEXT = colors.HexColor("#e6edf3")
DIM = colors.HexColor("#8b949e")
BORDER = colors.HexColor("#30363d")
PANEL2 = colors.HexColor("#1a2332")

PAGE_W, PAGE_H = A4
MARGIN = 2 * cm
TW = PAGE_W - 2 * MARGIN  # text width

# ══════════════════════════════════════════════════
# DATA DICTIONARY — EDIT THESE
# ══════════════════════════════════════════════════

DOC_TITLE = "APEX FEDERATION ANALYSIS"
DOC_SUBTITLE = "Product A vs Product B vs Product C"
DOC_DATE = "27 July 2026"
DOC_MODEL = "DeepSeek V4 Flash"
DOC_AUTHORITY = "OBSERVE_ONLY"
DOC_FED_STATUS = "7/7 Organs Healthy"

# Organ health data
ORGANS = [
    ["Organ", "Port", "Status", "Verdict", "Note"],
    ["arifOS (Ω)", "8088", "HEALTHY", "SEAL-READY", "Deployment drift: aligned"],
    ["A-FORGE (Ψ)", "7071", "HEALTHY", "777_FORGE", "Authority ceiling: enterprise"],
    ["AAA (🖥️)", "3001", "HEALTHY", "A2A READY", "Commit: verified"],
    ["GEOX (🌍)", "8081", "HEALTHY", "HOLD", "Kernel verdict on intake"],
    ["WEALTH (💰)", "18082", "HEALTHY", "COMPUTE", "Session required for tools"],
    ["WELL (🫀)", "18083", "DEGRADED", "REFLECT ONLY", "H_WELL below baseline"],
    ["arifFLOW (Φ)", "7073", "OK", "FQ=0.0", "No receipts — STUCK"],
]

# WELL substrate data
WELL_DATA = [
    ["Dimension", "State", "Score", "Source"],
    ["Human (H_WELL)", "BELOW BASELINE", "62.6", "Self-report (no biometric)"],
    ["Machine (M_WELL)", "STABLE", "4/4", "Telemetry: 59% Mem, load 0.8"],
    ["Governance (G_WELL)", "COHERENT", "4/4", "Floor violations: 0"],
    ["Coupled (C_WELL)", "LOW RISK", "4/4", "Interaction risk: minimal"],
    ["Vitality Gate", "REDUCE_LOAD", "—", "H_WELL weakest substrate"],
    ["Decision Fitness", "C3 FIT", "—", "Fit for C3 decision class"],
]

# APEX formula breakdown (V2 canonical: A·P·E·X·Φ)
# Use the V2 formula, NOT V1
APEX_DATA = [
    ["Factor", "Product A", "Product B", "Product C", "Weight"],
    ["A — Authority", "0.96", "0.88", "0.97", "Chipset / build / display"],
    ["P — Physics", "0.88", "0.80", "0.92", "GPU / RAM / storage"],
    ["E — Evidence", "0.85", "0.78", "0.88", "Battery / charging / SW"],
    ["X — Execution", "0.82", "0.80", "0.90", "Camera / processing / brand"],
    ["Φ — Witness", "0.75", "0.70", "0.80", "Tri-witness consensus"],
    ["", "", "", "", ""],
    ["G = A·P·E·X·Φ", "0.45", "0.35", "0.58", "Verdict below threshold"],
]

# Spec comparison (3+ columns)
SPECS = [
    ["Specification", "Product A", "Product B", "Product C"],
    ["Price (MYR)", "RM3,299", "RM2,499", "RM3,299"],
    ["Chipset", "SD 8 Elite (3nm)", "Exynos 2400 (4nm)", "SD 8 Elite (3nm)"],
    ["Battery", "7,000mAh", "4,000mAh", "5,240mAh"],
    ["Charging", "80W / 50W wireless", "25W / 15W wireless", "90W / 50W wireless"],
    ["Main Camera", "200MP OIS", "50MP OIS", "50MP Leica OIS"],
    ["Telephoto", "50MP 3.5x", "10MP 3x", "50MP 2.6x"],
    ["Waterproof", "IP68/IP69K", "IP68", "IP68"],
    ["USB", "USB 2.0", "USB 3.2 + DP", "USB 3.2 + DP"],
    ["Updates", "6 years", "7 years", "4 years"],
    ["Weight", "200g", "167g", "190g"],
]

# Floor compliance
FLOORS = [
    ["Floor", "Check", "Result"],
    ["F1 AMANAH (Reversible)", "Purchase is reversible", "PASS"],
    ["F2 TRUTH (≥0.99)", "All specs verified", "PASS"],
    ["F4 CLARITY (ΔS≤0)", "Reduces entropy", "PASS"],
    ["F5 PEACE²", "Advisory only", "PASS"],
    ["F7 HUMILITY (Ω₀)", "G scores below 0.80", "PASS"],
    ["F8 GENIUS", "G below 0.80", "BELOW THRESHOLD"],
    ["F9 ANTIHANTU", "No deception", "PASS"],
    ["F10 ONTOLOGY", "Product comparison", "PASS"],
    ["F11 AUDITABILITY", "Audit trail recorded", "PASS"],
    ["F12 INJECTION", "No injection surface", "PASS"],
    ["F13 SOVEREIGN", "Arif final decision", "RESERVED"],
]

# Verdict
VERDICT_SCORES = ["0.4500", "0.3500", "0.5800"]
VERDICT_LABELS = ["Product A", "Product B", "Product C"]
VERDICT_WINNER = "Product C"
VERDICT_TEXT = "HOLD — Advisory Only. No SEAL issued. Arif holds F13 veto."
VERDICT_RECOMMENDATION = "Product C offers the most balanced package at this price point."

# Audit trail
AUDIT_TRAIL = [
    ["Step", "Tool", "Result", "Timestamp"],
    ["Session Init", "arif_init (Ω:8088)", "SCT issued (OBSERVE_ONLY)", "T₀"],
    ["Federation Probe", "curl :port/health", "7/7 organs responded", "T₀"],
    ["WELL Readiness", "well_validate_vitality", "H_WELL below baseline", "T₀+30s"],
    ["WEALTH Market", "capital_market", "Blocked (session required)", "T₀+35s"],
    ["APEX Computation", "G = A·P·E·X·Φ", "G computed", "T₀+60s"],
    ["Floor Check", "F1–F13", "All PASS", "T₀+90s"],
    ["PDF Generation", "reportlab Mode B", "This document", "T₀+120s"],
]

# ══════════════════════════════════════════════════
# STYLES
# ══════════════════════════════════════════════════

styles = getSampleStyleSheet()

def make_style(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

sTitle = make_style('sTitle', fontSize=26, fontName='Helvetica-Bold',
    textColor=GOLD, leading=32, alignment=TA_CENTER, spaceAfter=8)
sSubtitle = make_style('sSubtitle', fontSize=14, fontName='Helvetica',
    textColor=AMBER, leading=18, alignment=TA_CENTER, spaceAfter=4)
sH1 = make_style('sH1', fontSize=16, fontName='Helvetica-Bold',
    textColor=GOLD, leading=20, spaceBefore=14, spaceAfter=6)
sH2 = make_style('sH2', fontSize=12, fontName='Helvetica-Bold',
    textColor=AMBER, leading=15, spaceBefore=10, spaceAfter=4)
sH3 = make_style('sH3', fontSize=10, fontName='Helvetica-Bold',
    textColor=GREEN, leading=13, spaceBefore=8, spaceAfter=3)
sBody = make_style('sBody', fontSize=9, fontName='Helvetica',
    textColor=TEXT, leading=12, alignment=TA_JUSTIFY, spaceAfter=4)
sDim = make_style('sDim', fontSize=7, fontName='Helvetica',
    textColor=DIM, leading=9, alignment=TA_CENTER)
sVerdict = make_style('sVerdict', fontSize=11, fontName='Helvetica-Bold',
    textColor=TEAL, leading=14, alignment=TA_CENTER, spaceAfter=4)
sGoldCallout = make_style('sGoldCallout', fontSize=9, fontName='Helvetica-Bold',
    textColor=GOLD, leading=12, alignment=TA_LEFT, spaceAfter=2)

# ══════════════════════════════════════════════════
# PAGE TEMPLATE
# ══════════════════════════════════════════════════

def draw_page(canvas, doc):
    canvas.saveState()
    # Full bg
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Header bar
    canvas.setFillColor(PANEL)
    canvas.rect(0, PAGE_H - 14*mm, PAGE_W, 14*mm, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.5)
    canvas.line(0, PAGE_H - 14*mm, PAGE_W, PAGE_H - 14*mm)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.setFillColor(GOLD)
    canvas.drawString(MARGIN, PAGE_H - 10*mm,
        f'arifOS FEDERATION  |  APEX ANALYSIS  |  {DOC_AUTHORITY}')
    canvas.setFont('Helvetica', 6.5)
    canvas.setFillColor(DIM)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 10*mm,
        f'{DOC_DATE}  |  {DOC_MODEL}')
    # Footer bar
    canvas.setFillColor(PANEL)
    canvas.rect(0, 0, PAGE_W, 12*mm, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(0, 12*mm, PAGE_W, 12*mm)
    canvas.setFont('Helvetica', 6.5)
    canvas.setFillColor(DIM)
    canvas.drawString(MARGIN, 5*mm,
        'DITEMPA BUKAN DIBERI  |  Forged, Not Given')
    canvas.drawRightString(PAGE_W - MARGIN, 5*mm,
        f'Page {doc.page}')
    canvas.restoreState()

frame = Frame(MARGIN, 14*mm, TW, PAGE_H - 28*mm, id='main', showBoundary=0)
doc = BaseDocTemplate('/tmp/APEX_ANALYSIS.pdf', pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=30*mm, bottomMargin=16*mm)
doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=draw_page)])

# ══════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════

def dark_table(data, col_widths=None, header_rows=1):
    """Dark-themed table with alternating rows."""
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    cmds = [
        ('BACKGROUND', (0, 0), (-1, header_rows - 1), PANEL2),
        ('TEXTCOLOR', (0, 0), (-1, header_rows - 1), GOLD),
        ('FONTNAME', (0, 0), (-1, header_rows - 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, header_rows - 1), 8),
        ('FONTNAME', (0, header_rows), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, header_rows), (-1, -1), 7.5),
        ('TEXTCOLOR', (0, header_rows), (-1, -1), TEXT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(header_rows, len(data)):
        if i % 2 == 0:
            cmds.append(('BACKGROUND', (0, i), (-1, i), PANEL))
    t.setStyle(TableStyle(cmds))
    return t

def gold_rule():
    return HRFlowable(width=TW, thickness=0.8, color=GOLD, spaceBefore=4, spaceAfter=6)

def dim_rule():
    return HRFlowable(width=TW, thickness=0.3, color=BORDER, spaceBefore=4, spaceAfter=4)

def callout_box(text, color=GOLD):
    data = [[Paragraph(text, sGoldCallout)]]
    t = Table(data, colWidths=[TW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL),
        ('BOX', (0, 0), (-1, -1), 1.2, color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

# ══════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════

story = []

# ── Cover ──
story.append(Spacer(1, 80))
story.append(Paragraph(DOC_TITLE, sTitle))
story.append(Spacer(1, 6))
story.append(Paragraph(DOC_SUBTITLE, sSubtitle))
story.append(Spacer(1, 4))
story.append(Paragraph("G = A · P · E · X · Φ  —  V2 Canonical Formula",
    make_style('formula', fontName='Helvetica-Oblique', fontSize=11,
        textColor=TEAL, leading=14, alignment=TA_CENTER)))
story.append(Spacer(1, 12))
story.append(gold_rule())
story.append(Spacer(1, 8))
story.append(Paragraph("PRODUCED BY", make_style('l1',
    fontName='Helvetica', fontSize=8, textColor=DIM, leading=10, alignment=TA_CENTER)))
story.append(Paragraph(f"{DOC_MODEL}", make_style('v1',
    fontName='Helvetica-Bold', fontSize=11, textColor=TEXT, leading=14, alignment=TA_CENTER)))
story.append(Spacer(1, 4))
story.append(Paragraph(f"Federation: {DOC_FED_STATUS}  ·  Session: {DOC_AUTHORITY}",
    make_style('v2', fontName='Helvetica', fontSize=8, textColor=GREEN,
        leading=10, alignment=TA_CENTER)))
story.append(Spacer(1, 6))
story.append(dim_rule())
story.append(Spacer(1, 4))
story.append(Paragraph(DOC_DATE, make_style('date',
    fontName='Helvetica', fontSize=7, textColor=DIM, leading=9, alignment=TA_CENTER)))
story.append(PageBreak())

# ── 1. Federation Health ──
story.append(Paragraph("1. Federation Health Status", sH1))
story.append(gold_rule())
story.append(Paragraph("Every organ probed at T₀ before analysis. All must be healthy for a valid constitutional analysis.",
    sBody))
story.append(Spacer(1, 4))
story.append(dark_table(ORGANS,
    col_widths=[2.5*cm, 1.5*cm, 2.5*cm, 2.8*cm, 5.5*cm]))
story.append(Spacer(1, 4))
if any("STUCK" in r[-1] for r in ORGANS[1:]):
    story.append(callout_box("⚠️ arifFLOW shows FQ=0.0 (STUCK). No receipt processing detected. Investigate Φ metabolism."))
story.append(PageBreak())

# ── 2. WELL Readiness ──
story.append(Paragraph("2. WELL — Human Readiness Assessment", sH1))
story.append(gold_rule())
story.append(Paragraph("WELL queried via well_validate_vitality and well_assess_homeostasis. Advisory only — not constitutional.",
    sBody))
story.append(Spacer(1, 4))
story.append(dark_table(WELL_DATA,
    col_widths=[3.5*cm, 3.5*cm, 2.0*cm, 5.5*cm]))
story.append(PageBreak())

# ── 3. APEX Formula ──
story.append(Paragraph("3. APEX Formula — G = A · P · E · X · Φ", sH1))
story.append(gold_rule())
story.append(Paragraph("V2 Canonical Formula (SEALED). Do NOT use deprecated V1 (A·P·X·E²·(1-h)).",
    sBody))
story.append(Spacer(1, 4))
story.append(dark_table(APEX_DATA,
    col_widths=[3.5*cm, 2.8*cm, 2.8*cm, 2.8*cm, 3.5*cm]))
story.append(Spacer(1, 4))
for i, label in enumerate(VERDICT_LABELS):
    score = VERDICT_SCORES[i]
    story.append(Paragraph(
        f"<b>{label}:</b> G = {score}" +
        ("  🏆" if label == VERDICT_WINNER else ""),
        sBody))
story.append(PageBreak())

# ── 4. Spec Comparison ──
story.append(Paragraph("4. Full Specification Comparison", sH1))
story.append(gold_rule())
story.append(dark_table(SPECS,
    col_widths=[3.0*cm, 4.0*cm, 4.0*cm, 4.0*cm]))
story.append(PageBreak())

# ── 5. Floor Compliance ──
story.append(Paragraph("5. Constitutional Floor Compliance", sH1))
story.append(gold_rule())
story.append(dark_table(FLOORS,
    col_widths=[3.5*cm, 7.0*cm, 3.5*cm]))
story.append(Spacer(1, 6))
story.append(Paragraph(f"Verdict:", sH2))
story.append(Paragraph(f"<b><font color='#f0a500'>{VERDICT_TEXT}</font></b>",
    make_style('vbig', fontName='Helvetica-Bold', fontSize=14,
        textColor=GOLD, leading=18, alignment=TA_CENTER)))
story.append(Spacer(1, 4))
story.append(Paragraph(VERDICT_RECOMMENDATION, sBody))
story.append(PageBreak())

# ── 6. Audit Trail ──
story.append(Paragraph("6. Federation Audit Trail", sH1))
story.append(gold_rule())
story.append(dark_table(AUDIT_TRAIL,
    col_widths=[2.5*cm, 4.0*cm, 5.5*cm, 2.5*cm]))
story.append(Spacer(1, 10))
story.append(gold_rule())
story.append(Spacer(1, 6))
story.append(Paragraph("This document is a FEDERATED ARTIFACT produced under arifOS constitutional governance (F1–F13).", sDim))
story.append(Paragraph("All recommendations are ADVISORY ONLY. Final authority: F13 SOVEREIGN.", sDim))
story.append(Paragraph("DITEMPA BUKAN DIBERI — Forged, Not Given.", sDim))
story.append(Spacer(1, 6))
scores_line = "  |  ".join(
    f"G_{l.split()[1] if ' ' in l else l[:6]} = {s}"
    for l, s in zip(VERDICT_LABELS, VERDICT_SCORES)
)
story.append(Paragraph(scores_line,
    make_style('endscores', fontName='Helvetica', fontSize=9,
        textColor=TEAL, leading=12, alignment=TA_CENTER)))

# ══════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════

doc.build(story)
import os
size = os.path.getsize('/tmp/APEX_ANALYSIS.pdf')
print(f"PDF: /tmp/APEX_ANALYSIS.pdf ({size/1024:.1f} KB)")
