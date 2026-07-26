# Gold Site Dashboard — Live Architecture

> Canonical URL: `https://arif-fazil.com/gold/`
> Deploy path: `/var/www/html/gold/index.html`
> Last updated: 2026-07-18 (live data enforcement)

## Architecture

```
Browser (arif-fazil.com/gold)
    ↕ JS fetch (CONFIG.API_BASE = /wealth/gold/api)
Caddy reverse proxy
    ↕ strip /wealth/gold → localhost:3456
Gold API (:3456 — Flask/Python)
    ↕ yfinance → pandas → ta
Yahoo Finance (free tier)
```

## Live Data Rule — NON-NEGOTIABLE

**Every number on the site MUST come from the live API.** Hardcoded/stale data is HARAM because traders (Syed/@rico_ricaldo_33) make real money decisions based on what they see.

### Hardcoded defaults rule:
- HTML defaults: use `—` (em dash), never stale price numbers
- Timestamp: use "Loading live data..." not old dates
- All elements must have JS IDs so `refresh*()` functions can populate them

### Boot sequence: TRUTH BEFORE BEAUTY

```javascript
// ✅ CORRECT: Live data first, chart second
document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([refreshTicker(), refreshMacro()]); // LIVE DATA FIRST
  renderChart('4H');                                     // chart in background
  refreshApex(); refreshSignals(); refreshTechnicalForge(); refreshCalendar();
});

// ❌ WRONG: Chart first blocks live data for 3-8 seconds
await renderChart('4H');
await Promise.all([refreshTicker(), ...]);
```

### Sections that must be live

| Section | Function | API endpoint | Elements updated |
|---|---|---|---|
| **Pulse bar** | `refreshTicker()` | `/ticker` | price, delta, S1/S2/R1/R2, bias pill, RSI, timestamp |
| **Market Pulse** | `refreshApex()` | `/apex` | clarity, risk, trend energy, condition, structure/strength/signal % |
| **Macro ticker** | `refreshMacro()` | `/macro` | DXY, US10Y, VIX, Silver, GSR |
| **Technical Forge** | `refreshTechnicalForge()` | ticker + signal_v2 + apex | trend/momentum/structure/volume scores + analysis text |
| **Synthesis** | `refreshSignals()` | `/signal_v2` | verdict, direction, confluence %, RR ratio, judge reason |
| **Calendar** | `refreshCalendar()` | `/calendar` | high-impact USD events |
| **Chart** | `renderChart(tf)` | `/history` | TradingView candlestick chart |

### Refresh intervals
- Ticker: every 120s (2 min)
- Full refresh: every 300s (5 min)
- Chart: on timeframe change

## Caddy Routing

```
arif-fazil.com/gold   → 308 redirect → /gold/
arif-fazil.com/gold/* → /var/www/html/gold (static)
arif-fazil.com/wealth/gold/api/* → strip /wealth/gold → localhost:3456 (reverse proxy)
```

**Gotcha:** `handle /gold/*` in Caddy does NOT match `/gold` (no trailing slash). Need explicit `redir /gold /gold/ 308` before the handle block.

## Gold API Endpoints

| Endpoint | Returns | Key fields |
|---|---|---|
| `/api/ticker` | Live quote | price, change, rsi, ema20/50/200, emaTrend, support[], resistance[] |
| `/api/gold/ticker` | Same as above | gold-specific alias |
| `/api/apex` | APEX scores | G, C_dark, clarity, risk, trend_energy, condition, structure% |
| `/api/signal_v2` | Trading signal | direction, verdict, confluence_score, rr_ratio, judge_reason |
| `/api/levels` | S/R zones | support_1h[], resistance_1h[], support_daily[], resistance_daily[], pivot |
| `/api/macro` | Macro indicators | DXY, US10Y, VIX, SILVER, GSR |
| `/api/calendar` | Economic events | high-impact USD events this week |
| `/api/history` | OHLCV candles | interval + period params |

## Pitfalls

1. **Stale HTML defaults** — the most dangerous bug. "$4,063" from Jul 16 was shown to traders for 2 days while live API said "$4,023". Fix: `—` placeholders + data-first boot.

2. **Caddy /gold without trailing slash** — falls through to SPA catch-all, serves homepage instead of gold dashboard. Fix: `redir /gold /gold/ 308`.

3. **TradingView chart blocks DOMContentLoaded** — heavyweight library takes 3-8s to init, blocking live data display. Fix: fire ticker first, chart second (no await on chart).

4. **CORS should be fine** — same origin (arif-fazil.com → Caddy proxy → localhost). But test with `curl -sI` to confirm `access-control-allow-origin: *`.
