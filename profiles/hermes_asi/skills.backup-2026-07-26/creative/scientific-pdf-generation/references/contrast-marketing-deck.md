# Contrast-Table Marketing Deck Pattern

Use when: competitive comparison PDFs, "X vs Y" arguments, tech security briefings, evidence-heavy persuasion documents. Audience is a single person or small group — typically to counter enthusiasm for a competitor or explain why one approach beats another.

Distinct from the standard Mode B marketing deck (card layouts, flow diagrams, before/after). This pattern uses **Platypus flowables** (not direct canvas) because it's data-heavy — tables, stats, card callouts, quote blocks. Dark background via `BaseDocTemplate.handle_pageBegin`.

## When This Pattern Fits

- "Why X beats Y" arguments (kernel > sandbox, DeepSeek > Gemini)
- Security/tech briefings with exploit evidence (CVE tables, vendor response tables)
- Any PDF that needs to PROVE a point with data, not just pitch with emotion
- Audience needs to see the evidence chain, not just the conclusion

## Color Palette (Indigo/Cyan variant)

```
Background:  #0a0a0f (near-black)
Cards:       #131320 (card surface)
Accent:      #6366f1 (indigo — primary)
Accent2:     #06b6d4 (cyan — quotes, key callouts)
Red:         #ef4444 (negative/failure/before)
Amber:       #f59e0b (warnings)
Green:       #10b981 (positive/after)
Purple:     #a855f7 (tertiary accent)
Gray:        #64748b (dim labels)
Lgray:      #94a3b8 (body text dim)
Border:     #1e293b (table grid lines)
White:      #ffffff (body text primary)
```

## Stat Pair Pattern

Two big numbers side by side — punchy, memorable.

```python
def stat_pair(num1, label1, num2, label2):
    t = Table([
        [Paragraph(num1, big_stat), Paragraph(num2, big_stat)],
        [Paragraph(label1, stat_label), Paragraph(label2, stat_label)],
    ], colWidths=[85*mm, 85*mm])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,1), (-1,1), 2),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
    ]))
    return t

# Styles
big_stat = ParagraphStyle('Stat', fontSize=28, leading=34, textColor=WHITE,
    fontName='Helvetica-Bold', alignment=TA_CENTER)
stat_label = ParagraphStyle('SL', fontSize=9, leading=12, textColor=GRAY,
    alignment=TA_CENTER)
```

Used in: "7 Escapes / 4 Failure modes" and "7 Escapes / 13 Constitutional floors".

## Contrast Table Pattern

Two-column comparison — red header for "wrong way", green header for "right way".

```python
contrast_data = [
    [Paragraph("<b>Sandbox / Sudo</b>", body_white),
     Paragraph("<b>Kernel (arifOS)</b>", body_white)],
    ["Trust boundary — satu garisan", "Constitutional chain — setiap pautan diverifikasi"],
    # ... more rows ...
]
t_contrast = Table(contrast_data, colWidths=[82*mm, 88*mm])
t_contrast.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), RED),
    ('BACKGROUND', (1,0), (1,0), GREEN),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('BACKGROUND', (0,1), (0,-1), HexColor("#1f1315")),   # dark red tint
    ('BACKGROUND', (1,1), (1,-1), HexColor("#0f1a14")),   # dark green tint
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER),
]))
```

## Evidence Table Pattern

For exploit/CVE data — target column in red, status column color-coded by vendor response.

```python
exploit_data = [
    [Paragraph("<b>Target</b>", body_white), ...],
    ["Cursor", ".claude hook config → unsandboxed execution", "CVE-2026-48124 · Patched"],
    # ...
]
t_exp = Table(exploit_data, colWidths=[36*mm, 80*mm, 54*mm])
t_exp.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ACCENT),     # header row colored
    ('BACKGROUND', (0,1), (-1,-1), CARD),        # body rows card bg
    ('TEXTCOLOR', (0,1), (0,-1), RED),           # target column red
    ('TEXTCOLOR', (2,1), (2,-1), GREEN),          # status column green
    # Override specific rows if needed:
    ('TEXTCOLOR', (2,6), (2,7), AMBER),           # Google downgrade = amber
    # ...
]))
```

## Failure Mode Card Pattern

Block card with accent LINEBELOW — title in white, body in gray, example in small text.

```python
def card(title_text, body_text, accent_color, width=170*mm):
    t = Table([[Paragraph(title_text, card_title), Paragraph(body_text, card_body)]],
              colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,0), 3, accent_color),
    ]))
    return t
```

## Numbered Row Pattern

For 4-item lists where each item has a number, bold title, description, and example.

```python
fm_data = [
    [Paragraph("<b>1</b>", body_white), 
     Paragraph("<b>Denylist sandboxes</b> can't keep pace with the OS", body),
     Paragraph("Antigravity macOS Seatbelt bypass", small)],
    # ... rows 2-4 ...
]
t_fm = Table(fm_data, colWidths=[8*mm, 100*mm, 58*mm])
t_fm.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), CARD),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER),
    ('TEXTCOLOR', (0,0), (0,-1), ACCENT),    # numbers in accent color
]))
```

## Quote Block Pattern

Center-aligned italic quote in cyan — used for key insight or external citation.

```python
quote = ParagraphStyle('Quote', fontSize=13, leading=20, textColor=ACCENT2,
    fontName='Helvetica-Oblique', alignment=TA_CENTER, spaceBefore=8, spaceAfter=8)

story.append(Paragraph(
    "<b>\"The agent stays inside the box and follows every rule. "
    "It just writes a file that a trusted tool outside the box later runs...\"</b>",
    quote))
```

## Pro-Tip: `HexColor` collisions with matplotlib

When using both reportlab and matplotlib in the same script, define TWO color namespaces:

```python
# For reportlab Paragraphs/Tables only:
DARK = HexColor("#0a0a0f")
# For matplotlib only (plain strings):
DARK_S = "#0a0a0f"
```

Never pass a reportlab `HexColor` object to matplotlib's `color=` param — it crashes with `ValueError: Color(...) is not a valid value for color`.

## Page Structure (Contrast Deck)

Standard spine for a "Why X beats Y" contrast deck:

1. **Cover** — BIG title (1-3 words), subtitle with key stats, thin accent rule, tagline, attribution
2. **The Problem** — narrative intro, stat pair, numbered failure modes, key insight card
3. **The Evidence** — exploit table with color-coded vendor responses, warning card
4. **Why Sudo/Sandbox Fail** — numbered list (4 structural reasons), quote from external source
5. **The Answer** — contrast table (side-by-side), constitutional floors list, key principle
6. **Closing** — restated title, narrative wrap, stat pair callback, closing tagline

## Verified

- 2026-07-22: "Why Kernel Beats Sandbox" — 7 pages, dark/indigo-cyan, Pillar Security sandbox escape evidence. Stat pairs, contrast table, exploit evidence table, failure mode cards, quote blocks. 13.8KB. Audience: Ezriq (single person, competitive persuasion).
