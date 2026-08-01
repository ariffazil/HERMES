# Independent WCAG Contrast Verification

When a design-token spec (or any artifact) claims specific contrast ratios, **recompute them independently** before ratifying. Self-reported ratios can be wrong even when the overall math discipline is sound.

## Proven case (2026-08-01)

A PRIMER-1 design-token spec claimed 13 contrast ratios. Independent verification found 12/13 exact matches and 1 error:
- **teal-900 `#064E3B` on paper `#FAF7F0`**: claimed 4.76:1 "AA caption-only", actual **9.08:1 AAA**
- The error was over-restriction (not a safety failure) but would have caused CI to enforce a "caption-only" restriction the math didn't require

## Verification script

```python
import json

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexstr):
    h = hexstr.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

def contrast(fg, bg):
    l1, l2 = lum(fg), lum(bg)
    return (max(l1,l2) + 0.05) / (min(l1,l2) + 0.05)

def verdict(r, body=False):
    if body:
        return "AAA" if r >= 7 else ("AA" if r >= 4.5 else "FAIL")
    return "AAA" if r >= 7 else ("AA" if r >= 4.5 else ("AA-large" if r >= 3 else "FAIL"))

# Usage: verify every claimed ratio in a spec
claims = [
    # (label, fg_hex, bg_hex, claimed_ratio, is_body_text)
    ("ink on paper",      "#1A1A1A", "#FAF7F0", 16.27, True),
    ("yellow-900 paper",  "#5C4500", "#FAF7F0",  8.51, True),
    # ... add all claimed pairs
]

for label, fg, bg, claimed, body in claims:
    actual = contrast(fg, bg)
    delta = actual - claimed
    status = "MATCH" if abs(delta) < 0.15 else "DISCREPANCY"
    print(f"{label:<30} claimed={claimed:.2f} actual={actual:.2f} Δ={delta:+.2f} {status} → {verdict(actual, body)}")
```

## What to check

1. **Every claimed ratio** — recompute from hex values, don't trust the number
2. **WCAG verdict correctness** — a ratio can be right but the verdict label wrong (e.g. 9.08:1 labeled "AA" when it's AAA)
3. **Scope restrictions** — if a token is labeled "caption-only" but the ratio exceeds AAA threshold, the restriction is over-constrained
4. **Catastrophe pairs** — verify that fill-only tokens (500-series on paper) really do fail as text
5. **Trap tokens** — verify that "almost passes" tokens (700-series) really do fail at the claimed level

## WCAG thresholds (quick reference)

| Level | Normal text | Large text (≥18pt/14pt bold) |
|-------|------------|------------------------------|
| AA    | ≥ 4.5:1    | ≥ 3:1                        |
| AAA   | ≥ 7:1      | ≥ 4.5:1                      |
