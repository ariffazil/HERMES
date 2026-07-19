# XAUUSD Indicator Calculations — Reference

All calculations match `/root/trading/scripts/gold_engine.py` logic.

## EMA (Exponential Moving Average)

```python
# Pandas built-in (preferred over manual loop)
df['ema20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['ema50'] = df['Close'].ewm(span=50, adjust=False).mean()

# Manual (for numpy-only contexts)
def ema(prices, period):
    r = np.zeros(len(prices))
    m = 2 / (period + 1)
    r[0] = prices[0]
    for i in range(1, len(prices)):
        r[i] = (prices[i] - r[i-1]) * m + r[i-1]
    return r
```

**EMA Cross Signal:**
- `ema20 > ema50` → BULLISH
- `ema20 < ema50` → BEARISH
- Crossover = direction change (use `.diff()` on the binary signal)

## RSI (Relative Strength Index)

```python
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['rsi'] = 100 - (100 / (1 + rs))
```

**Thresholds:**
- RSI > 70 = Overbought (avoid LONG, consider SHORT)
- RSI < 30 = Oversold (avoid SHORT, consider LONG)
- RSI 30-70 = Neutral zone

## Support/Resistance — Pivot-Based

```python
def find_sr_levels(df, window=12):
    """Detect S/R from local pivots. Use CHART window, not full dataset."""
    candidates = []
    for i in range(window, len(df) - window):
        if df['High'].iloc[i] == df['High'].iloc[i-window:i+window+1].max():
            candidates.append(('R', df['High'].iloc[i]))
        if df['Low'].iloc[i] == df['Low'].iloc[i-window:i+window+1].min():
            candidates.append(('S', df['Low'].iloc[i]))

    def cluster(levels, threshold=5.0):
        if not levels: return []
        levels = sorted(levels)
        clusters = [[levels[0]]]
        for v in levels[1:]:
            if v - clusters[-1][-1] < threshold:
                clusters[-1].append(v)
            else:
                clusters.append([v])
        return [round(np.mean(c), 2) for c in clusters]

    return (cluster([v for t,v in candidates if t=='R']),
            cluster([v for t,v in candidates if t=='S']))
```

**Key:** Run on charted window (48h), NOT full60d data. Otherwise S/R levels
are outside visible range and chart looks empty.

## Candlestick Pattern Detection

```python
# For each candle i (starting from 1):
body = abs(c - o)
upper_wick = h - max(o, c)
lower_wick = min(o, c) - l
total_range = h - l

# Hammer (bullish reversal)
if lower_wick > 2 * body and upper_wick < body and c > o: → 'H'

# Shooting Star (bearish reversal)
if upper_wick > 2 * body and lower_wick < body and c < o: → 'SS'

# Bearish Engulfing
if c < o and prev_c > prev_o and c < prev_o and o > prev_c: → 'BE'

# Bullish Engulfing
if c > o and prev_c < prev_o and c > prev_o and o < prev_c: → 'BEn'

# Doji (indecision)
if body < total_range * 0.1: → 'D'
```

## Signal Generation Logic

Require ≥2 confluence factors (F3 WITNESS rule):

1. EMA crossover direction (bullish/bearish)
2. RSI not overbought (< 70 for LONG) or oversold (> 30 for SHORT)
3. Proximity to S/R level (nearest support for LONG, nearest resistance for SHORT)

```python
if ema_bullish and rsi < 70:
    # LONG: entry at current price, SL below nearest support
    entry = current_price
    sl = nearest_support - (range * 0.15)
    tp1 = entry + (range * 0.5)
    tp2 = entry + (range * 1.0)
    tp3 = entry + (range * 1.5)
elif not ema_bullish and rsi > 30:
    # SHORT: entry at current price, SL above nearest resistance
    entry = current_price
    sl = nearest_resistance + (range * 0.15)
    tp1 = entry - (range * 0.5)
    tp2 = entry - (range * 1.0)
    tp3 = entry - (range * 1.5)
```

## Data Source

```python
import yfinance as yf
df = yf.Ticker("GC=F").history(period="60d", interval="1h")
# Fallback: yf.Ticker("XAUUSD=X")
```

GC=F = Gold futures (Yahoo Finance). 1h interval, 60d period gives ~1200 candles.
