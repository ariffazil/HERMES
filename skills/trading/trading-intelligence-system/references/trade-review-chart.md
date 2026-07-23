# Trade Review Chart Pattern (Dark Theme)

Proven: 2026-07-21 — Brent crude position review for Abang Sado Syed.

## When to Use

When a trader (Syed, Arif) wants to review an active position visually — showing entry, SL, TP levels, and current price on a candlestick chart.

## Stack

- `yfinance` for data (e.g., `BZ=F` for Brent, `GC=F` for gold)
- `matplotlib` with dark theme (Mode B colors from scientific-pdf-generation)
- Manual candlestick rendering (no mplfinance dependency)

## Color Palette

```python
BG      = "#0d1117"
PANEL   = "#161b22"
GOLD    = "#f0a500"
GREEN   = "#3fb950"
RED     = "#f85149"
TEAL    = "#39d2c0"
TEXT    = "#e6edf3"
DIM     = "#8b949e"
BORDER  = "#30363d"
```

## Chart Structure

1. **Main chart** — 1H candles, last 5 days (~120 bars)
2. **EMA 50 overlay** — dim grey, 1.2pt line, alpha 0.6
3. **Horizontal level lines** — ENTRY (gold), SL (red), TP1 (green), TP2 (optional)
4. **Current price dot** — TEAL filled circle, 14pt marker, black edge
5. **P&L badge** — top-left, green box with `+$X.XX (+Y.Y%)`
6. **Info box** — top-right, monospace font, listing RSI, trend, R:R, cushion, distance to TP
7. **Highlight zone** — semi-transparent gold band around entry

## X-axis

- Show date/time labels for ~8 evenly spaced ticks
- Format: `%m/%d %H:%M`
- Offset last 4 bars right to accommodate annotation arrow

## Y-axis

- Range: `min(df['Low'].min(), SL-2)` to `max(df['High'].max(), TP1+1)` plus 8% padding
- Price labels on left

## Legend

- Custom patches: green (P&L), gold (entry), red (SL), green (TP1), teal (current)
- Position: lower left
- Facecolor: PANEL, edgecolor: BORDER

## Pitfalls

- Import `pandas` explicitly — yfinance returns DataFrames but doesn't auto-import pd
- yfinance deprecation warnings are cosmetic, ignore
- Use `matplotlib.use('Agg')` for headless rendering
- Set `MPLCONFIGDIR=/tmp/.mpl` to silence pyrolite warnings
- Figure size: 14×8 inches, DPI 150
- Save as PNG, not PDF — Telegram renders PNG inline
