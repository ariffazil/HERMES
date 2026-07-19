# Gold Dashboard Architecture Reference

> Maintained 2026-07-18. Ground truth for the gold web dashboard.

## Live URLs

| URL | Status | Notes |
|---|---|---|
| `https://arif-fazil.com/gold/` | Primary | Redirects `/gold` → `/gold/` |
| `https://arif-fazil.com/wealth/gold/` | Legacy | Same dashboard, different path |
| `https://wealth.arif-fazil.com/gold/` | Organ subdomain | Same dashboard |

## Data Flow

```
gold-api (Python, :3456)
  ├── /api/ticker        → price, EMA20/50/200, RSI, S/R levels (1H)
  ├── /api/signal_v2     → signal, regime, confluence, verdict
  ├── /api/apex          → G, C_dark, clarity, risk, trend, condition
  ├── /api/macro         → DXY, US10Y, VIX, silver, GSR
  ├── /api/calendar      → ForexFactory high-impact events
  ├── /api/levels        → S/R 1H + Daily
  └── /api/history       → OHLCV for chart
         ↓
Caddy: /wealth/gold/api/* → strip_prefix /wealth/gold → localhost:3456
         ↓
Browser JS: CONFIG.API_BASE = origin + '/wealth/gold/api'
  fetch('/ticker') → pulse bar
  fetch('/signal_v2') → synthesis verdict
  fetch('/apex') → market intelligence
  fetch('/macro') → macro ticker
  fetch('/calendar') → events
  fetch('/history?days=30&interval=1h') → TradingView chart
```

## Key Files

| File | Purpose |
|---|---|
| `/var/www/html/gold/index.html` | Single-file dashboard (HTML+CSS+JS, no build) |
| `/etc/caddy/Caddyfile` | Gold routes: `handle /wealth/gold/*` (line ~186) + `handle /gold/*` (line ~267) |
| `/root/trading/` | gold-api backend, signals, regime, backtest |
| `gold-api.service` | systemd unit for :3456 |

## Caddy Routing Notes

```
# Wealth terminal — serves /wealth/gold/*, /wealth/oil/*, /wealth/gas/*
handle /wealth/* {
    root * /var/www/html
    try_files {path} {path}index.html /wealth/index.html
    file_server
}

# Gold API proxy
@wealth_gold_api path /wealth/gold/api/*
handle @wealth_gold_api {
    uri strip_prefix /wealth/gold
    reverse_proxy localhost:3456
}

# Gold static files
handle /wealth/gold/* {
    uri strip_prefix /wealth/gold
    root * /var/www/html/gold
    try_files {path} /index.html
    file_server
}

# Direct route — CRITICAL: redirect BEFORE handle block
redir /gold /gold/ 308
handle /gold/* {
    root * /var/www/html/gold
    try_files {path} /index.html
    file_server
}
```

**Trailing slash bug:** `handle /gold/*` matches `/gold/xxx` but NOT `/gold`. The bare `/gold` path falls through to the SPA catch-all which serves the main `arif-fazil.com` homepage. Fix: `redir /gold /gold/ 308` before the handle block.

## Boot Sequence (fixed 2026-07-18)

```javascript
// BEFORE (broken): chart blocked live data
await renderChart('4H');  // heavy TradingView init
await Promise.all([refreshTicker(), ...]);  // data delayed

// AFTER (fixed): data first, chart non-blocking
await Promise.all([refreshTicker(), refreshMacro()]);  // data in <500ms
renderChart('4H');  // chart in background
refreshApex();
refreshSignals();
refreshCalendar();
```

## Visual Chart Analysis Requirement

Arif: "Weiii trading agent kena pandai tengok chart laaa, wajib."

The trading agent MUST be able to visually analyze charts (candlestick patterns, S/R levels, trendlines) from screenshots. Current model (deepseek-v4-pro) lacks native vision. Workaround options:

1. **Auxiliary vision config** — `hermes config set auxiliary.vision.provider xiaomi-mimo` + `hermes config set auxiliary.vision.model mimo-v2.5` — requires MiMo API quota (currently exhausted)
2. **Anthropic Claude direct API** — has native vision, requires credit balance (currently exhausted)
3. **OCR fallback** — tesseract extracts text from chart screenshots, works for price levels but not candle patterns
4. **Switch main model** to vision-capable (claude-sonnet-4, gpt-4o, gemini-flash)

Until vision is restored, use: OCR + live API data + user description to reconstruct chart context.
