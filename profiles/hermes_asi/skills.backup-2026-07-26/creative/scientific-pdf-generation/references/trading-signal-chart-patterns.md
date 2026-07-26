# Trading Signal Chart — Mode D Reference

**Proven 2026-07-14:** XAUUSD daily signal chart — iterative refinement over 8+ attempts. User corrections drove every design decision.

## The User's Vision (Abang Udin + Arif)

The chart must look like **OANDA mobile app** — dark theme, candlesticks fill the screen, zoomed into current price action. One chart must explain the entire trading plan: where to buy, where to sell, where to stop, where to take profit.

## Critical Design Rules (ALL learned from user corrections)

### 1. ZOOM IN — not out
- **WRONG:** Showing $4,800 → $4,000 range (800 points) — candles become tiny
- **RIGHT:** Show $3,970 → $4,080 range (110 points) — candles fill the chart
- **User quote:** "Jangan la zoom out sangat. Boleh x ikut context"
- **Rule:** Y-axis range = current price ± $50-80 for day trading signals

### 2. NO EMPTY SPACE
- **WRONG:** 50 candles with price dropping diagonally — top-right is dead black
- **RIGHT:** 15-20 recent candles filling the entire chart area
- **User quote:** "Too many empty space"
- **Rule:** Number of candles should fill horizontal space tightly

### 3. BUY/SELL ZONES = RIGHT AT CURRENT PRICE
- **WRONG:** Sell zone at $4,200 when price is $4,003 ($200 away)
- **RIGHT:** Buy $3,995-4,010, Sell $4,020-4,040 (within $40 of current)
- **User quote:** "Syed nak position buy or sell yang berdekatan dengan market price"
- **Rule:** Entry zones must be within 1-2% of current price for day trading

### 4. REAL CANDLESTICKS — color follows OHLC, not trend
- **WRONG:** All red candles in a downtrend (trend-following color)
- **RIGHT:** Red = close < open (filled), Green = close > open (hollow), regardless of trend
- **User quote:** "Aku nak candlestick yang bagi real maksud"
- **Special patterns to mark:**
  - **H** = Hammer (small body, long lower wick ≥ 2x body) — reversal signal
  - **D** = Doji (body < 10% of range) — indecision
  - **SS** = Shooting Star (small body, long upper wick) — top warning
  - **BE** = Bearish Engulfing (big red covers previous green) — trend change

### 5. EMA 20 + EMA 50 on chart
- EMA 20 = blue (#58a6ff), faster
- EMA 50 = orange (#f0883e), slower
- Death cross (EMA20 < EMA50) = bearish confirmation
- Golden cross = bullish confirmation

### 6. ONE CHART explains everything
- **WRONG:** Separate tables for strategy, separate R:R panel, multiple charts
- **RIGHT:** Buy zone, sell zone, stop loss, targets, R:R — all visual ON the chart
- **User quote:** "Satu chart can explain the whole world"
- Strategy table goes BELOW the chart, not on it

### 7. Scale = CANTIK (beautiful)
- Candles must be BIG relative to chart area
- Labels on Y-axis (right side), not inline boxes blocking candles
- R:R box — small, top corner, out of the way
- **User quote:** "Scale of the chart x cantik"

### 8. Landscape PDF for trading charts
- A4 landscape gives wider chart, better proportions
- Chart image fills 90%+ of the page
- Strategy strip below — minimal text

## Dark Theme Color Palette (OANDA Style)

```python
BG        = '#0d1117'  # Main background (near-black)
PANEL     = '#161b22'  # Slightly lighter panels
GOLD      = '#f0a500'  # Headlines, current price marker
TEAL      = '#39d2c0'  # Support levels, T2 targets
RED       = '#f85149'  # Bearish candles, sell zones, stop losses
GREEN     = '#3fb950'  # Bullish candles, buy zones, targets
TEXT      = '#e6edf3'  # Body text (near-white)
DIM       = '#8b949e'  # Captions, dates, secondary text
BORDER    = '#30363d'  # Grid lines, spines
C_RED     = '#f85149'  # Candle red (bearish)
C_GREEN   = '#3fb950'  # Candle green (bullish)
EMA_BLUE  = '#58a6ff'  # EMA 20
EMA_ORANGE= '#f0883e'  # EMA 50
SL_RED    = '#ff5252'  # Stop loss lines
```

## Candlestick Drawing Pattern

```python
cw = 0.6  # candle width
for i in range(n):
    o, h, l, c = opens[i], highs[i], lows[i], closes[i]
    body = abs(c - o)
    rng = h - l if h - l > 0 else 1
    is_bull = c >= o  # REAL meaning — not trend-following
    body_bot = min(o, c)
    body_h = max(body, 1.0)
    
    if body < rng * 0.1:  # Doji
        ax.plot([i-cw/2, i+cw/2], [o, o], color=DIM, linewidth=2)
        ax.plot([i, i], [l, h], color=DIM, linewidth=1)
    else:
        col = GREEN if is_bull else RED
        if is_bull:
            rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                            facecolor='none', edgecolor=GREEN, linewidth=1.5)
        else:
            rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                            facecolor=RED, edgecolor=RED, linewidth=0.8, alpha=0.85)
        ax.add_patch(rect)
        ax.plot([i, i], [l, body_bot], color=col, linewidth=0.9)
        ax.plot([i, i], [body_bot + body_h, h], color=col, linewidth=0.9)
```

## Level Drawing Pattern

```python
# Buy zone — shaded band
ax.axhspan(entry_lo, entry_hi, alpha=0.25, color=GREEN, zorder=0)
ax.axhline(y=entry_lo, color=GREEN, linewidth=3, alpha=0.9)
ax.axhline(y=entry_hi, color=GREEN, linewidth=3, alpha=0.9)

# Labels on RIGHT side (Y-axis), not inline
ax.text(n+0.3, price, f' BUY ${entry_lo}-${entry_hi}', fontsize=10, 
        fontweight='bold', color=GREEN, va='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d2818', edgecolor=GREEN, linewidth=1.5))

# Stop loss — dashed
ax.axhline(y=sl, color='#ff5252', linestyle='-.', linewidth=2.5, alpha=0.9)

# Targets — dotted
ax.axhline(y=t1, color=GREEN, linestyle=':', linewidth=2, alpha=0.6)
```

## R:R Visual Pattern

```python
# Risk arrow (down from entry to SL)
ax.annotate('', xy=(x, sl), xytext=(x, entry_mid),
           arrowprops=dict(arrowstyle='<->', color='#ff5252', lw=3))
ax.text(x+0.4, (entry_mid+sl)/2, f'RISK\n${int(entry_mid-sl)}', fontsize=11,
       fontweight='bold', color='#ff5252', va='center',
       bbox=dict(boxstyle='round,pad=0.2', facecolor='#3d1010', edgecolor='#ff5252'))

# Reward arrow (up from entry to T1)
ax.annotate('', xy=(x, t1), xytext=(x, entry_mid),
           arrowprops=dict(arrowstyle='<->', color=GREEN, lw=3))
ax.text(x+0.4, (entry_mid+t1)/2, f'REWARD\n+${int(t1-entry_mid)}', fontsize=11,
       fontweight='bold', color=GREEN, va='center',
       bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d2818', edgecolor=GREEN))
```

## PDF Layout Pattern (Landscape)

```python
from reportlab.lib.pagesizes import landscape, A4

doc = SimpleDocTemplate(out, pagesize=landscape(A4),
    topMargin=0.3*cm, bottomMargin=0.3*cm, leftMargin=0.3*cm, rightMargin=0.3*cm)

# Chart fills the page
story.append(Image(chart_path, width=29*cm, height=16*cm))

# Strategy strip below
strat = [
    ['LONG $3,995-4,010', 'SL $3,975', 'T1 $4,045 (+$42)', 'T2 $4,080 (+$77)', 'R:R 1:3.4', 'PREFERRED'],
    ['SHORT $4,020-4,040', 'SL $4,060', 'T1 $3,980 (+$30)', 'T2 $3,950 (+$60)', 'R:R 1:2.0', 'SECONDARY'],
]
```

## Iteration Log (What Failed and Why)

| Attempt | Problem | User Feedback | Fix |
|---|---|---|---|
| v1 | Line chart, no candlesticks | "Aku nak candlestick" | Switch to OHLC candlesticks |
| v2 | Green/red by trend direction | "Candlestick yang bagi real maksud" | Color by OHLC (close vs open) |
| v3 | No EMA, no patterns | "Include ema 20 50 as well" | Add EMA 20/50 + pattern labels |
| v4 | Too cluttered, small text | "Aku x nampak apa" | Simplify, bigger text |
| v5 | Buy zone $4,200 (far from $4,003) | "Nak position berdekatan market price" | Move zones to $3,995-4,010 |
| v6 | Y-axis $3,900-4,450 (too wide) | "Scale x cantik" | Zoom to $3,970-4,080 |
| v7 | $4,800-4,000 range, empty space | "Too many empty space" | 60 candles, tighter range |
| v8 | Still showing full $4,800 range | "Jangan zoom out sangat" | 15 days, $3,970-4,080, BIG candles |
| FINAL | Zoomed in, big candles, clean | "Ok" ✅ | 15 candles, tight range, labels on Y-axis |

## Multi-Timeframe Note

User (Abang Udin) wants multi-timeframe eventually (Daily + 4H + 1H), but the FIRST priority is getting one timeframe right with proper zoom and scale. Multi-timeframe is a future enhancement — don't overcomplicate the first deliverable.
