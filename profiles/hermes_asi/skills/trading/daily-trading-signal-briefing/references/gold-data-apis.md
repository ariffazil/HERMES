# Gold Data APIs — Live Endpoints (Updated 2026-07-16)

## Primary: Gold-API (port 3456) — USE THIS FIRST

The gold-api Node.js server on port 3456 is the canonical data source. It has 5-min cache and calls yfinance internally. Direct yfinance calls time out on this VPS — always use gold-api.

```bash
# APEX market intelligence
curl -sf localhost:3456/api/gold/apex
# Returns: G, C_dark, dS, state, direction, verdict, APEX primitives, volume, momentum

# Full signal (engine_v2 + position sizing + governance gate)
curl -sf localhost:3456/api/gold/signal_v2
# Returns: signal (direction/entry/SL/TP/RR/lot/verdict), regime, zones, confluence

# Quick ticker
curl -sf localhost:3456/api/gold/ticker
# Returns: price, change, changePct, RSI, EMA20/50/200, signal, confidence

# Macro context
curl -sf localhost:3456/api/gold/macro
# Returns: DXY, VIX, US10Y, silver, gold_silver_ratio

# Economic calendar (ForexFactory JSON)
curl -sf localhost:3456/api/gold/calendar
# Returns: events[] with date/time/impact/event/actual/forecast/previous, next_event

# OHLCV history
curl -sf "localhost:3456/api/gold/history?interval=1h&period=30d"
# Returns: candles[], ema20[], ema50[], ema200[], rsi[]
```

**Short aliases (for Caddy strip_prefix compatibility):**
- `/api/apex` → `/api/gold/apex`
- `/api/signal_v2` → `/api/gold/signal_v2`
- `/api/ticker` → `/api/gold/ticker`
- `/api/macro` → `/api/gold/macro`
- `/api/calendar` → `/api/gold/calendar`

**Via Caddy (public):** `https://arif-fazil.com/wealth/gold/api/apex` etc.

**PITFALL (proven 2026-07-16):** Caddy strips `/wealth/gold` from the path. So `/wealth/gold/api/macro` → `/api/macro` on the backend. If the Node.js server only has `/api/gold/macro` but NOT `/api/macro`, Caddy returns 404. Always add BOTH full path AND short alias in server.js.

## ForexFactory Calendar JSON API

```
https://nfs.faireconomy.media/ff_calendar_thisweek.json
```

Returns array of events with: `title`, `country`, `date` (ISO 8601 with TZ offset), `impact` (High/Medium/Low), `forecast`, `previous`, `actual`.

Filter: `country === "USD"` and `impact in ("High", "Medium")` for gold-relevant events.

**PITFALL:** HTML scraping of ForexFactory breaks due to merged cells. The JSON API is reliable.

## yfinance (Fallback — slow on this VPS)

```python
import yfinance as yf
ticker = yf.Ticker("GC=F")
df = ticker.history(period="30d", interval="1h")
```

**PITFALL:** yfinance download calls timeout after 60s on this VPS. Use gold-api instead. yfinance is only used INTERNALLY by gold-api's Python backend.

## Other APIs (reference only)

| API | Endpoint | Notes |
|---|---|---|
| GoldAPI.io | `https://www.goldapi.io/api/XAU/USD` | 300 req/month free, real-time |
| API Ninjas | `https://api.api-ninjas.com/v1/goldprice` | Free tier, 15-min delay |
| Twelve Data | OHLCV time-series | Free 800/day, $29/mo pro |
| MetaTrader 5 | `mt5.symbol_info_tick("XAUUSD")` | Zero cost, real-time, needs MT5 running |
