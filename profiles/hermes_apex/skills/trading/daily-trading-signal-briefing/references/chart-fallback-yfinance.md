# Chart Generation Fallback When /root/trading Is Missing

**Proven:** 2026-07-20 cron run. gold-api signal_v2/apex fail with "No module named 'trading'", and `/root/trading/scripts/chart_pro.py` doesn't exist.

## Fallback Chain

```
gold-api signal_v2 → FAIL (no trading module)
gold-api ticker    → OK (self-contained, uses yfinance directly)
       ↓
yfinance GC=F      → OK (20-candle OHLC via venv python)
       ↓
template chart     → OK (/root/HERMES/skills/trading/daily-trading-signal-briefing/templates/gold_signal_chart.py)
```

## Step-by-Step

### 1. Fetch OHLC from yfinance

```bash
/root/venv/bin/python3 -c "
import yfinance as yf, json
gold = yf.Ticker('GC=F')
hist = gold.history(period='1mo')
dates = [i.strftime('%d %b') for i in hist.index]
ohlc = [[round(r['Open'],1), round(r['High'],1), round(r['Low'],1), round(r['Close'],1)] for _, r in hist.iterrows()]
print(json.dumps({'dates': dates[-18:], 'ohlc': ohlc[-18:]}))
"
```

**Note:** `GC=F` is gold futures (COMEX). Prices may differ $2-5 from XAUUSD spot. For chart visuals this is acceptable — the signal levels come from the ticker's spot price.

### 2. Adapt the Template

Copy the template from `templates/gold_signal_chart.py` and replace:
- `dates_labels` — last 18 entries from yfinance output
- `ohlc` — last 18 OHLC tuples
- `CURRENT_PRICE`, `BUY_ZONE_LOW/HIGH`, `ENTRY_MID`, `SL_BUY`, `TARGET1_BUY`, `TARGET2_BUY` — from signal construction
- `EVENT_WARNING` — from calendar data
- `CHART_TITLE` — include date + verdict

### 3. Run with venv python

```bash
/root/venv/bin/python3 /tmp/build_gold_signal.py
```

Output goes to `/tmp/gold_signal_chart.png` (~170KB at 150 DPI).

### 4. Deliver

Include chart as MEDIA:/tmp/gold_signal_chart.png in the message.

## RSI Note

The chart calculates RSI from the 18-candle OHLC data (futures). The ticker's RSI may differ (uses spot data, longer history). The ticker RSI is authoritative for signal decisions; the chart RSI is visual context only.

## Template Location

```
/root/HERMES/skills/trading/daily-trading-signal-briefing/templates/gold_signal_chart.py
```

The template handles: candlesticks, EMA 20/50, buy/sell zones, SL/T1/T2 lines, R:R box, RSI subplot, event warning, current price marker. 18 candles, 14×8 inches, dark OANDA theme.
