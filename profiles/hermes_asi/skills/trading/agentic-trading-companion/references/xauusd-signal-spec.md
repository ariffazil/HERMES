# XAUUSD Signal Engine Spec

## Trading Parameters (Abang Sado Udin)

| Parameter | Value |
|---|---|
| Instrument | XAUUSD (Gold vs USD) |
| Timeframe | H1 primary, H4/D1 for context |
| Style | EMA 20/50 + H1 S/R + candle confirmation + RSI divergence |
| Risk per trade | 1% |
| RR minimum | 1:2 (1:3 ideal) |
| Max trades/day | 2 |
| Max daily loss | 2% |
| Sessions | London + NY only (Asian = blocked) |
| News filter | Skip NFP, CPI, FOMC, FOMC Minutes |
| Confluence | ≥2 indicators required (single = F3 breach) |

## Data Source

```python
import yfinance as yf
# Primary: Gold futures
df = yf.Ticker("GC=F").history(period="60d", interval="1h")
# Fallback: Spot gold
df = yf.Ticker("XAUUSD=X").history(period="60d", interval="1h")
```

## Indicators

### EMA 20/50
```python
df['ema_fast'] = df['Close'].ewm(span=20, adjust=False).mean()
df['ema_slow'] = df['Close'].ewm(span=50, adjust=False).mean()
df['ema_cross'] = 0  # 1=bullish, -1=bearish
df.loc[df['ema_fast'] > df['ema_slow'], 'ema_cross'] = 1
df['ema_cross_signal'] = df['ema_cross'].diff()  # ±2 = fresh crossover
```

### RSI(14)
```python
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['rsi'] = 100 - (100 / (1 + rs))
```

### RSI Divergence
- Bullish: price lower low + RSI higher low
- Bearish: price higher high + RSI lower high
- Lookback: 20 periods

### Support/Resistance (Pivot-based)
```python
window = 20
highs = df['High'].rolling(window=window, center=True).max()
lows = df['Low'].rolling(window=window, center=True).min()
resistance = sorted(highs.dropna().unique(), reverse=True)[:3]
support = sorted(lows.dropna().unique())[:3]
```

### Candlestick Patterns
- Hammer: lower_wick > 2×body, upper_wick < body, close > open
- Shooting Star: upper_wick > 2×body, lower_wick < body, close < open
- Bullish Engulfing: close > open, prev_close < prev_open, close > prev_open
- Bearish Engulfing: close < open, prev_close > prev_open, close < prev_open
- Doji: body < 10% of total range

## Session Filter (MYT/UTC)

| Session | UTC | MYT |
|---|---|---|
| London | 07:00-16:00 | 3:00pm-12:00am |
| New York | 12:00-21:00 | 8:00pm-5:00am |
| Asian | 00:00-07:00 | 8:00am-3:00pm (BLOCKED) |

## Confluence Rules

```
Bull signals: EMA_BULLISH, EMA_CROSS_BULL, NEAR_SUPPORT, CANDLE_BULLISH, RSI_BULL_DIV, RSI_OVERSOLD
Bear signals: EMA_BEARISH, EMA_CROSS_BEAR, NEAR_RESISTANCE, CANDLE_BEARISH, RSI_BEAR_DIV, RSI_OVERBOUGHT

Min confluence = 2
```

## SL/TP Calculation

```python
atr = df['High'].tail(14).sub(df['Low'].tail(14)).mean()
if signal_type == 'LONG':
    sl = entry - atr * 1.5
    tp = entry + (entry - sl) * rr_min
elif signal_type == 'SHORT':
    sl = entry + atr * 1.5
    tp = entry - (sl - entry) * rr_min
```

## Briefing Format (Telegram)

```
GOLD SIGNAL — 14 Jul 2026, 8:00 AM MYT
SESSION: LONDON
PRICE: $4,085

SIGNAL: SHORT
Confidence: 75%
Confluence: 3/4 — EMA_BEARISH, RSI_BEAR_DIV, RSI_OVERBOUGHT

Entry: $4,085
Stop Loss: $4,110
Take Profit: $4,034
R:R = 1:2.0

Reasoning:
  • EMA20 (4044) < EMA50 (4056)
  • RSI bearish divergence
  • RSI 84.9 — overbought

MACRO:
  DXY: 100.7 (-0.57%)
  US 10Y: 4.573%

Support: $3,955, $3,965, $3,973
Resistance: $4,783, $4,780, $4,775

---
AI companion signal. Kau decide, kau execute.
```

## APEX 5 — Questions Before Any Trade Advice

Before giving trading advice to a human, ask these 5 questions:

1. **Berapa lot size?** — Risk exposure
2. **Masuk sebab apa?** — Valid setup vs impulse
3. **Ada trade lain tak?** — Total exposure
4. **Kalau hilang duit ni, ok ke?** — Financial safety
5. **Dah plan exit ke belum?** — Discipline level

> Tanpa 5 ni, AI cuma teka. Dengan 5 ni, AI boleh nasihat.

## Blindspot Checklist

| Blindspot | Danger | Fix |
|---|---|---|
| Confirmation bias | Hold losing trade | Check D1/W1 bigger picture |
| H1 support trust | Can't see break | Hard stop loss |
| Comfort with loss | Skip risk mgmt | Max daily loss limit |
| Single instrument | All-in | Focus ok, limit capital |
| No journal | Repeat mistakes | Log every trade |
| Support worship | Bigger crash | Stronger S = bigger SL |
| No macro view | News kills setup | Check calendar
