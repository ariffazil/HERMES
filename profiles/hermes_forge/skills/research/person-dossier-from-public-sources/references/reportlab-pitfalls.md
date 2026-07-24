# Reportlab HTML Parser Pitfalls

These bit a real PDF build in July 2026. The pattern: reportlab's mini-HTML parser is **partial** — it implements only a small subset. Below are the failure modes encountered and the fix for each.

---

## Pitfall 1: `<span style='...'>` raises `findSpanStyle not implemented`

**Symptom:**
```
ValueError: findSpanStyle not implemented in this parser
```

**Cause:** reportlab's parser does not implement `findSpanStyle`. `<span style='color:#888'>` and similar inline-styled tags blow up at paragraph build time.

**Fix:** use `<font color='...'>` for color, and `<font size='...'>...</font>` for size. Reportlab supports both.

```python
# WRONG
Paragraph("<span style='color:#888;font-size:8.5pt'>label</span>", style)

# RIGHT
Paragraph("<font color='#888'><font size='8'>label</font></font>", style)
```

**Compound styles** (color + size + bold): nest `<font>` tags. Reportlab will close them in order. Don't try to combine.

---

## Pitfall 2: keyError on `papers[i]["coauthors"]` after building a list with mixed dicts

**Symptom:** the loop body references a key that exists on some dicts but not all, because the dict literal was copied and a field was dropped on paste/merge.

**Fix:** when building a list of dicts that all share the same shape, **add the field to every dict explicitly** before the loop. If you find one missing, fix the source, don't paper over with `.get(..., "")` (silent fallbacks hide schema drift).

---

## Pitfall 3: avoid `<para>...</para>` wrappers inside `Paragraph`

**Symptom:** parser tries to nest paragraph tags. Always pass a string of inline tags, not a paragraph wrapper.

**Fix:** `Paragraph("text <b>bold</b> text", style)`. The `<para>` wrapper is added by reportlab itself.

---

## Pitfall 4: page decorations fail silently on first call

**Symptom:** header band doesn't show on page 1, only on later pages.

**Fix:** pass the same decoration function to BOTH `onFirstPage` and `onLaterPages` in `doc.build(..., onFirstPage=fn, onLaterPages=fn)`. Reportlab distinguishes first vs later; if you only pass `onLaterPages`, page 1 has no header.

```python
doc.build(story, onFirstPage=page_decorations, onLaterPages=page_decorations)
```

---

## Pitfall 5: Y coordinate system in `canv` is **bottom-up**, not top-down

When drawing on the page directly (not via flowables), the y-coordinate origin is at the bottom-left. To draw a band at the **top** of the page, the y-coordinate must be close to `A4[1] - band_height`, not a small number.

```python
# A4 = (595, 842) in points
canv.rect(0, A4[1] - 1.4 * cm, A4[0], 1.4 * cm, fill=1, stroke=0)  # TOP band
canv.drawString(2 * cm, A4[1] - 0.9 * cm, "text")  # text inside the band
```

For text, use `canv.drawString(x, y, "text")` where y is the **baseline** of the text. For 14pt text inside a band that starts at `A4[1] - 1.4 cm`, baseline around `A4[1] - 0.9 cm` works.

---

## Pitfall 6: `Paragraph` does not auto-escape `&` in user content

**Symptom:** if your content has "AT&T" or "Tom & Jerry", parser chokes.

**Fix:** use `&amp;` in source strings, or wrap with `xml.sax.saxutils.escape()`.

---

## Pitfall 7: Tables with `colWidths` that exceed page width

**Symptom:** table gets clipped or wraps weirdly.

**Fix:** sum `colWidths` first; if > `A4[0] - 2*leftMargin - 2*rightMargin`, scale down proportionally.

---

## Verification recipe

After `doc.build(...)`, run a quick check:

```python
import subprocess
r = subprocess.run(['pdftotext', '-layout', 'output.pdf', '-'],
                   capture_output=True, text=True)
print('PAGES:', r.stdout.count('\x0c') + 1)
# spot-check label counts
for label in ['OBS', 'DER', 'INT', 'SPEC']:
    print(f'{label}:', r.stdout.count(label))
```

If `pdftotext` is not installed (`apt install poppler-utils`), the subprocess will fail. Fall back to `pypdf` or `PyPDF2` for page count.
