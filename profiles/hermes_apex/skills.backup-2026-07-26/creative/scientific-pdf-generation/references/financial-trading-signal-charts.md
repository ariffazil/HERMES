# Financial Trading Signal Charts — Mode D Specification

**Proven 2026-07-14:** XAUUSD daily trading signal PDF — candlestick chart with EMA, buy/sell zones, R:R panel, dark theme. Multiple iterations with Arif + Syed (Abang Sado) feedback.

## When to Use

Trading signal PDFs, daily market briefings, technical analysis charts, forex/commodity signal sheets. Mode D = dark theme, candlestick-first, mobile-readable.

## Critical User Preferences (Learned the Hard Way)

1. **ZOOM IN to relevant price range.** NEVER show the full history if it makes candles small. User said: "jangan la zoom out sangat. Boleh x ikut context." Show last 15-20 candles in a tight Y-axis range around current price. The chart should look like OANDA zoomed in.

2. **Candles must be BIG.** The chart is the hero. Candles should fill 80%+ of the chart area. If the Y-axis range is too wide, candles look like thin lines — unacceptable.

3. **No wasted whitespace.** "Too many empty space" — user complaint. Fill the chart area. No dead zones. If price is trending down, don't show empty space above the trend.

4. **Real candlestick coloring.** Red filled = bearish (close < open). Green hollow = bullish (close > open). NOT colored by trend direction. User said: "candlestick yang bagi real maksud."

5. **Mark candlestick patterns.** H=Hammer, D=Doji, SS=Shooting Star, BE=Bearish Engulfing. Label them ON the chart where they appear.

6. **EMA 20 + EMA 50 overlays.** Always include. User said: "Include ema 20 50 as well."

7. **Buy/Sell zones CLOSE to current price.** "Syed nak position buy or sell yang berdekatan dengan market price. X mau jauh sangat. Temporal intelligence." Zones should be within $30-50 of current price, not $200 away.

8. **Strategy table below chart.** Not inline boxes that block candles. Long vs Short side-by-side with entry, SL, T1, T2, R:R.

9. **Dark theme.** OANDA-style. BG=#0d1117, text=#e6edf3, gold=#f0a500 accent.

10. **Mobile-first.** Text must be readable on phone. Labels on Y-axis (right side), not inline boxes overlapping candles.

## Color Palette (Mode D — Trading Signal)

```python
BG        = '#0d1117'  # background (GitHub dark)
PANEL     = '#161b22'  # slightly lighter panels
GOLD      = '#f0a500'  # accent, current price marker
TEAL      = '#39d2c0'  # support levels, T2 targets
RED       = '#f85149'  # bearish candles, sell zone, stop loss
GREEN     = '#3fb950'  # bullish candles, buy zone, long targets
TEXT      = '#e6edf3'  # body text (near-white)
DIM       = '#8b949e'  # captions, dates, secondary text
BORDER    = '#30363d'  # grid lines, table borders
C_RED     = '#f85149'  # candle red (same as RED)
C_GREEN   = '#3fb950'  # candle green (same as GREEN)
C_DARKRED = '#ff5252'  # stop loss lines
C_ORANGE  = '#f0883e'  # EMA 50, short targets
C_BLUE    = '#58a6ff'  # EMA 20
```

## Candlestick Rendering (matplotlib — manual)

Do NOT use mplfinance. Draw candlesticks manually with Rectangle patches for full control.

```python
cw = 0.65  # candle width
for i in range(n):
    o, h, l, c = opens[i], highs[i], lows[i], closes[i]
    body = abs(c - o)
    rng = h - l if h - l > 0 else 1
    is_bull = c >= o
    body_bot = min(o, c)
    body_h = max(body, 0.8)
    
    if is_bull:
        # HOLLOW green — no fill
        rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                         facecolor='none', edgecolor=GREEN, linewidth=1.5)
    else:
        # FILLED red
        rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                         facecolor=RED, edgecolor=RED, linewidth=0.8, alpha=0.85)
    ax.add_patch(rect)
    # Wicks
    ax.plot([i, i], [l, body_bot], color=col, linewidth=0.9)
    ax.plot([i, i], [body_bot + body_h, h], color=col, linewidth=0.9)
```

### Doji Detection
```python
is_doji = body < rng * 0.1
# Draw as cross: thin horizontal line + vertical wick
ax.plot([i-cw/2, i+cw/2], [o, o], color=DIM, linewidth=1.5)
ax.plot([i, i], [l, h], color=DIM, linewidth=0.8)
```

### Hammer Detection
```python
lower_wick = min(o, c) - l
upper_wick = h - max(o, c)
is_hammer = (body < rng * 0.3) and (lower_wick >= body * 2) and (upper_wick < body * 0.5)
```

### Bearish Engulfing Detection
```python
if i > 0 and not is_bull and closes[i-1] > opens[i-1]:
    if o > closes[i-1] and c < opens[i-1] and body > abs(closes[i-1]-opens[i-1]) * 1.3:
        # Bearish engulfing
        ax.annotate('BE', xy=(i, h+15), fontsize=5.5, ...)
```

## EMA Calculation

```python
def ema(prices, period):
    result = np.zeros(len(prices))
    multiplier = 2 / (period + 1)
    result[0] = prices[0]
    for i in range(1, len(prices)):
        result[i] = (prices[i] - result[i-1]) * multiplier + result[i-1]
    return result

ema20 = ema(closes, 20)
# For EMA50 proxy on short datasets:
ema50 = np.zeros(n); ema50[0] = closes[0]
for i in range(1, n): ema50[i] = ema50[i-1] * 0.92 + closes[i] * 0.08
```

## Chart Layout — Zoomed OANDA Style

```python
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
fig.subplots_adjust(left=0.08, right=0.85, top=0.93, bottom=0.08)
# Right margin (0.85) leaves space for level labels on Y-axis

# Y-axis: TIGHT to relevant range
ax.set_ylim(3970, 4080)  # only $110 range for $4,000 price

# Level labels on right side (not inline boxes)
ax.text(n+0.3, price, f' BUY ${price}', fontsize=10, fontweight='bold',
       color=GREEN, va='center',
       bbox=dict(boxstyle='round,pad=0.2', facecolor=PANEL, edgecolor=GREEN, linewidth=1))
```

## Key Pitfalls

- **NEVER show full history that makes candles small.** User wants to see candle BODIES clearly. If that means showing only 15 days, show 15 days.
- **NEVER put large inline boxes on the chart.** They block candles. Use Y-axis labels (right side) or small top-left annotations.
- **NEVER use mplfinance for these charts.** It doesn't give enough control over annotations, zones, and styling. Manual Rectangle patches are the way.
- **NEVER use `astype(float)` after `np.roll` on int array.** Causes casting error. Always: `opens = np.roll(closes, 1).astype(float)`.
- **NEVER use walrus operator `:=` in matplotlib kwargs.** Causes SyntaxError. Assign separately.
- **Import `matplotlib.patches as mpatches` explicitly.** It's needed for legend Patch handles but not auto-imported.
- **PDF orientation:** Landscape A4 for trading signal PDFs. Chart fills most of the page. Strategy table below.
- **User reads on MOBILE.** Keep text large. Keep labels readable. No tiny fonts.

## Strategy Table Pattern (below chart)

```python
strat = [
    ['LONG $3,995-4,010', 'SL $3,975', 'T1 $4,045 (+$42)', 'T2 $4,080 (+$77)', 'R:R 1:3.4', 'PREFERRED'],
    ['SHORT $4,020-4,040', 'SL $4,060', 'T1 $3,980 (+$30)', 'T2 $3,950 (+$60)', 'R:R 1:2.0', 'SECONDARY'],
]
# Green bg for long row, red bg for short row
# Gold border, dark theme
```

## R:R Visual on Chart

```python
# Vertical double-headed arrow from entry to SL (risk) and entry to T1 (reward)
ax.annotate('', xy=(x_pos, stop_loss), xytext=(x_pos, entry),
           arrowprops=dict(arrowstyle='<->', color='#ff5252', lw=3))
ax.text(x_pos+0.5, mid, f'RISK\n${risk}', fontsize=11, fontweight='bold', color='#ff5252', ...)

ax.annotate('', xy=(x_pos, target), xytext=(x_pos, entry),
           arrowprops=dict(arrowstyle='<->', color=GREEN, lw=3))
ax.text(x_pos+0.5, mid, f'REWARD\n+${reward}', fontsize=11, fontweight='bold', color=GREEN, ...)
```

## Data Sources for Gold Price

| Source | Latency | Cost | Best for |
|---|---|---|---|
| MT5 Python (`MetaTrader5` package) | Real-time | Free | Execution platform data |
| GoldAPI.io | Real-time | Free 300/mo | Backup feed |
| TradingEconomics | ~15min | Free web | Quick reference |
| OANDA API | Real-time | Paid | Professional |

## PDF Generation

```python
from reportlab.lib.pagesizes import landscape, A4
# Landscape for trading signal PDFs
doc = SimpleDocTemplate(out, pagesize=landscape(A4),
    topMargin=0.3*cm, bottomMargin=0.3*cm, leftMargin=0.3*cm, rightMargin=0.3*cm)

# Chart fills most of page
story.append(Image(chart_path, width=29*cm, height=16*cm))
# Strategy table below
story.append(Table(strat_data, colWidths=[4.5*cm, 3*cm, 4.5*cm, 4.5*cm, 3*cm, 3.5*cm]))
```
