# Trading Signal Chart Patterns (Mode D Reference)

**Proven 2026-07-14:** XAUUSD daily signal PDF — candlestick chart with EMA, buy/sell zones, R:R visualization. 5 iterations with user corrections.

## Manual Candlestick Drawing (matplotlib)

mplfinance is one option, but for full control over annotations, zones, and overlays, draw candlesticks manually:

```python
from matplotlib.patches import Rectangle

cw = 0.6  # candle width
for i in range(days):
    o, h, l, c = opens[i], highs[i], lows[i], closes[i]
    body = abs(c - o)
    rng = h - l if h - l > 0 else 1
    is_bull = c >= o
    is_doji = body < rng * 0.12
    body_bot = min(o, c)
    body_h = max(body, 1.0)  # minimum visible body

    if is_doji:
        ax.plot([i-cw/2, i+cw/2], [o, o], color=DIM, linewidth=2, zorder=5)
        ax.plot([i, i], [l, h], color=DIM, linewidth=1, zorder=5)
    else:
        col = GREEN if is_bull else RED
        if is_bull:
            rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                             facecolor='none', edgecolor=GREEN, linewidth=1.5)
        else:
            rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                             facecolor=RED, edgecolor=RED, linewidth=0.8, alpha=0.85)
        ax.add_patch(rect)
        ax.plot([i, i], [l, body_bot], color=col, linewidth=0.9)       # lower wick
        ax.plot([i, i], [body_bot + body_h, h], color=col, linewidth=0.9)  # upper wick
```

### Candle Coloring Rule (CRITICAL)

Color by OHLC relationship, NOT by trend direction:
- **Red filled** = bearish (close < open)
- **Green hollow** = bullish (close > open)
- **Grey cross** = doji (body < 12% of range)

User explicitly rejected trend-following colors. "Real candlesticks yang bagi real maksud."

## Pattern Detection & Labeling

Label these patterns directly on the chart with annotations:

```python
body = abs(c - o)
upper_wick = h - max(o, c)
lower_wick = min(o, c) - l
total_range = h - l

# Hammer: small body, long lower wick (>= 2x body), small upper wick
is_hammer = (body < total_range * 0.3) and (lower_wick >= body * 2) and (upper_wick < body * 0.5)

# Doji: very small body (< 10% of range)
is_doji = body < total_range * 0.1

# Shooting Star: small body, long upper wick (>= 2x body), small lower wick
is_shooting_star = (body < total_range * 0.3) and (upper_wick >= body * 2) and (lower_wick < body * 0.5)

# Bearish Engulfing: big red candle covers previous green
if i > 0 and not is_bull and closes[i-1] > opens[i-1]:
    if o > closes[i-1] and c < opens[i-1] and body > abs(closes[i-1]-opens[i-1]) * 1.3:
        is_engulfing = True
```

Label abbreviations: H=Hammer, D=Doji, SS=Shooting Star, BE=Bearish Engulfing. Place below (for bullish) or above (for bearish) the candle.

## EMA Overlay

```python
def ema(prices, period):
    r = np.zeros(len(prices))
    m = 2 / (period + 1)
    r[0] = prices[0]
    for i in range(1, len(prices)):
        r[i] = (prices[i] - r[i-1]) * m + r[i-1]
    return r

ema20 = ema(closes, 20)
# For EMA50 on short datasets, use smoothed EMA as proxy:
ema50 = np.zeros(n); ema50[0] = closes[0]
for i in range(1, n): ema50[i] = ema50[i-1] * 0.88 + closes[i] * 0.12

ax.plot(range(n), ema20, color='#58a6ff', linewidth=2.5, label='EMA 20')
ax.plot(range(n), ema50, color='#f0883e', linewidth=2.5, label='EMA 50')
```

## Dark Theme (OANDA-style)

```python
BG = '#0d1117'; PANEL = '#161b22'; GOLD = '#f0a500'; TEAL = '#39d2c0'
RED = '#f85149'; GREEN = '#3fb950'; TEXT = '#e6edf3'; DIM = '#8b949e'; BORDER = '#30363d'
```

Apply `facecolor=BG` to figure and all axes. Use `PANEL` for annotation box backgrounds.

## R:R Visualization

Two approaches — both proven:

### 1. Bidirectional Arrows (on chart)
```python
ax.annotate('', xy=(x, stop_loss), xytext=(x, entry),
           arrowprops=dict(arrowstyle='<->', color=RED, lw=3))
ax.text(x+0.4, (entry+stop_loss)/2, f'RISK\n${risk}', ...)
```

### 2. Side Panel (R:R numbers)
```python
ax_rr.add_patch(FancyBboxPatch((0.3, 7.5), 9.4, 2.3, boxstyle="round,pad=0.15",
                                facecolor='#0d2818', edgecolor=GREEN, linewidth=2))
ax_rr.text(5, 8.5, '1 : 3.4', fontsize=28, fontweight='bold', color=GREEN, ha='center')
```

## Y-Axis Scaling (CRITICAL — user corrected this)

**Always zoom Y-axis to the relevant price range.** Don't show the full range from ATH to current.

- Bad: Y-axis 3800-4500 when price is at 4000 (candles look tiny)
- Good: Y-axis 3950-4120 when price is at 4000 (candles fill the chart)

Rule: `margin = (max(highs) - min(lows)) * 0.15` on each side of the visible range.

## Temporal Intelligence (Near-Price Zones)

User (via Syed): "Nak position buy or sell yang berdekatan dengan market price. X mau jauh sangat."

**Buy and sell zones should be AT or NEAR the current price**, not at distant S/R levels:
- If current price = $4,003, buy zone = $3,995-4,010 (right here)
- Sell zone = $4,020-4,040 (just above, for rejection play)
- NOT $4,180-4,200 (too far for day trading signal)

Distant levels (R1, R2, S1, S2) are reference context, NOT the primary trade zones.

## Mobile-First PDF Design

User couldn't read first attempts on phone. Fixes:
- **Landscape A4** for wider charts
- **Minimum 10pt font** for annotations on chart
- **Minimum 13pt font** for zone labels (BUY/SELL)
- **Bold boxes** with colored backgrounds for key levels
- **Chart takes 80%+ of page** — minimize text tables below
- **Strategy table** below chart with 3 columns: label / long / short

## Pitfalls

- **numpy int array + float noise = crash.** `np.array([4400, 4380])` creates int64. Adding `np.random.normal(0, 6, n)` fails with `Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64')`. Fix: `.astype(float)` on the array before adding noise.
- **`mpatches` not imported.** If using `mpatches.Patch` in legend, must `import matplotlib.patches as mpatches` at top level. Don't rely on `from matplotlib.patches import Rectangle` to provide it.
- **Y-axis too wide makes candles invisible.** Always zoom to relevant range.
- **Overcrowded chart = unreadable on mobile.** Fewer elements, bigger text. One chart > three charts.
- **Reportlab landscape A4** = `from reportlab.lib.pagesizes import A4, landscape` then `landscape(A4)`.
- **Emoji don't render in PDF fonts.** Use text labels instead.

## Proven Stack

1. Generate chart with matplotlib → save as PNG (150 DPI for mobile, 200 DPI for print)
2. Build PDF with reportlab: title → chart image → strategy table → disclaimer
3. Landscape A4 for signal PDFs, portrait for analyst reports
