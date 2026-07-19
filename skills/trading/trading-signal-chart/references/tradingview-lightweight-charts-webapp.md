# TradingView Lightweight-Charts Web App Pattern

When building a live trading chart web app (not PDF), use TradingView's open-source lightweight-charts library. This produces TradingView-quality interactive charts in the browser.

## When to Use

- User asks for "live chart", "web chart", "trading terminal", "chart app"
- Need real-time auto-refreshing chart (not static PDF)
- Deploy at a URL for mobile/desktop access
- Interactive (zoom, pan, crosshair, timeframe switch)

## Stack

- **Frontend:** TradingView lightweight-charts v4 (CDN: `https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js`)
- **Backend:** Node.js API server serving OHLCV data in TradingView format
- **Data source:** yfinance (Python) via `child_process.execFile` from Node.js
- **Deploy:** Static HTML + API proxy via Caddy

## Live Deployment (Proven 2026-07-14)

- **API server:** `/var/www/html/arif/wealth/gold/api/server.js` (Node.js, port 3456)
- **Data fetcher:** `/var/www/html/arif/wealth/gold/api/fetch_gold.py` (Python, yfinance)
- **Systemd:** `gold-api.service` — enabled, auto-restart
- **Frontend:** `/var/www/html/arif/wealth/gold/index.html` (static)
- **URL:** https://arif-fazil.com/wealth/gold

## Data Format (TradingView)

```javascript
// OHLCV data must use Unix timestamps in SECONDS (not milliseconds)
const candlestickData = [
  { time: 1689312000, open: 4000.5, high: 4015.2, low: 3995.0, close: 4010.3, volume: 1234 },
  // ...
];
```

## API Endpoints (All Implemented)

| Endpoint | Returns | Cache |
|---|---|---|
| `GET /api/gold/history?interval=1h&period=30d` | OHLCV array `{time, open, high, low, close, volume}` | 5 min (keyed by interval_period) |
| `GET /api/gold/ticker` | Current price, 24h change, high/low, volume | 5 min |
| `GET /api/gold/signals` | Latest 50 signals from `/root/trading/journal/signals.jsonl` | 5 min |
| `GET /api/gold/macro` | DXY, US10Y, USD/MYR, XAU/MYR | 5 min |
| `GET /api/gold/levels` | S/R levels, pivot, EMAs, swing highs/lows | 5 min |
| `GET /health` | Server status | none |

## Node.js Server Pattern

```javascript
// Key architecture: Node.js HTTP server → Python subprocess → yfinance
const { execFile } = require('child_process');
const PYTHON = '/root/venv/bin/python3';  // venv, not system python
const FETCH_SCRIPT = path.join(__dirname, 'fetch_gold.py');

function runPython(command, args) {
  return new Promise((resolve, reject) => {
    execFile(PYTHON, [FETCH_SCRIPT, command].concat(args), {
      timeout: 30000,
      maxBuffer: 10 * 1024 * 1024,
      env: { ...process.env, PYTHONUNBUFFERED: '1' }
    }, (err, stdout, stderr) => {
      if (err) return reject(new Error(stderr || err.message));
      resolve(JSON.parse(stdout.trim()));
    });
  });
}
```

**Why `execFile` not `execSync`:** Non-blocking, proper error handling, timeout support.

## Python Fetcher Pattern

```python
# fetch_gold.py — called by Node.js via child_process
# Usage: python3 fetch_gold.py history 1h 30d
#        python3 fetch_gold.py ticker
#        python3 fetch_gold.py macro
#        python3 fetch_gold.py levels 3mo

import sys, json, yfinance as yf

GOLD_TICKER = "GC=F"

def get_history(interval="1h", period="30d"):
    ticker = yf.Ticker(GOLD_TICKER)
    df = ticker.history(interval=interval, period=period)
    candles = []
    for idx, row in df.iterrows():
        candles.append({
            "time": int(idx.timestamp()),  # Unix SECONDS
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"])
        })
    candles.sort(key=lambda x: x["time"])
    return candles

# Results are JSON-serialized to stdout, read by Node.js
print(json.dumps(result))
```

## CORS Configuration

```javascript
const ALLOWED_ORIGINS = [
  'https://arif-fazil.com',
  'https://www.arif-fazil.com',
  'http://localhost:3000',
  'http://localhost:8080',
];

function getCorsHeaders(origin) {
  const headers = {
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
  if (origin && ALLOWED_ORIGINS.includes(origin))
    headers['Access-Control-Allow-Origin'] = origin;
  else if (!origin)
    headers['Access-Control-Allow-Origin'] = '*';  // curl/direct
  return headers;
}
```

Handle OPTIONS preflight with 204 response. Set `Cache-Control: public, max-age=60` on all responses.

## Macro Data: XAU/MYR Computation

Yahoo Finance `XAUMYR=X` ticker is unreliable. Compute XAU/MYR from:
```python
gold_price = float(yf.Ticker("GC=F").fast_info.last_price)
usd_myr = float(yf.Ticker("MYR=X").fast_info.last_price)
xau_myr = round(gold_price * usd_myr, 2)
```

## Frontend Features

1. **Candlestick series** — green up, red down
2. **EMA overlays** — LineSeries for EMA 20 (cyan) and EMA 50 (orange)
3. **S/R level lines** — Horizontal line series, green dashed (support), red dashed (resistance)
4. **Signal overlay** — Entry/SL/TP as horizontal lines with price markers
5. **Volume histogram** — Below candlesticks, subtle colors
6. **Timeframe selector** — H1, H4, D1 buttons that reload data
7. **Info panel** — Current price, RSI, signal status (HTML overlay)
8. **Auto-refresh** — setInterval every 60 seconds
9. **Crosshair** — Built-in with lightweight-charts

## EMA Calculation (Client-Side)

```javascript
function calcEMA(data, period) {
  const k = 2 / (period + 1);
  const ema = [];
  let prev = data[0].close;
  for (let i = 0; i < data.length; i++) {
    const val = data[i].close * k + prev * (1 - k);
    ema.push({ time: data[i].time, value: val });
    prev = val;
  }
  return ema;
}
```

## Dark Theme Config

```javascript
const chart = LightweightCharts.createChart(container, {
  layout: {
    background: { type: 'solid', color: '#0d1117' },
    textColor: '#e6edf3',
  },
  grid: {
    vertLines: { color: '#1e2530' },
    horzLines: { color: '#1e2530' },
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal,
  },
  rightPriceScale: {
    borderColor: '#30363d',
  },
  timeScale: {
    borderColor: '#30363d',
    timeVisible: true,
    secondsVisible: false,
  },
});
```

## Caddy Proxy Config

```caddyfile
# In arif-fazil.com block:
handle /wealth/gold/* {
    @api path /wealth/gold/api/*
    handle @api {
        uri strip_prefix /wealth/gold
        reverse_proxy localhost:3456
    }
    handle {
        try_files /wealth/gold/{path} /wealth/gold/index.html
        root * /var/www/html/arif
        file_server
    }
}
```

## Systemd Service

```ini
[Unit]
Description=Gold Data API Server (XAUUSD live data)
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/node /var/www/html/arif/wealth/gold/api/server.js
WorkingDirectory=/var/www/html/arif/wealth/gold/api
Restart=always
RestartSec=5
Environment=NODE_ENV=production
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
SyslogIdentifier=gold-api

[Install]
WantedBy=multi-user.target
```

## Pitfalls

- **OHLCV time must be in SECONDS, not milliseconds.** Lightweight-charts v4 expects seconds. If you pass milliseconds, chart renders empty with no error.
- **yfinance is Python, not Node.js.** Use `child_process.execFile(PYTHON, [script, ...args], ...)` to fetch data from Node.js backend. Prefer `execFile` over `execSync` — it handles errors cleanly and doesn't block the event loop. Cache the output to avoid hammering Yahoo.
- **Use venv Python for yfinance.** On this system, yfinance is installed in `/root/venv/bin/python3`, not system Python. Always use the full venv path.
- **XAU/MYR Yahoo ticker is broken.** `XAUMYR=X` returns errors from Yahoo Finance. Compute it instead: `gold_price (GC=F) × USD/MYR (MYR=X)`. Proven 2026-07-14.
- **CORS headers required.** API must set `Access-Control-Allow-Origin` for the frontend domain. Handle OPTIONS preflight with 204 response.
- **Don't use mplfinance for web charts.** mplfinance is matplotlib-based (static images). Lightweight-charts is interactive JavaScript. Different tools for different outputs.
- **5-minute cache is critical.** yfinance rate-limits aggressively. Cache OHLCV data for 5 min minimum. Key history cache by `interval_period` (e.g., `1h_30d`).
- **Mobile viewport.** Set `<meta name="viewport" content="width=device-width, initial-scale=1.0">` and make chart container `width: 100vw; height: 70vh`.
- **NEVER rewrite Python/JS files via terminal heredoc.** If the file content contains any string that matches the heredoc delimiter (e.g., `PYEOF`, `EOF`), the heredoc terminates early, silently truncating or deleting the file. This destroyed both server.js and fetch_gold.py during the 2026-07-14 build. Always use `write_file` tool for creating/rewriting code files — it's atomic and safe. Use terminal heredocs ONLY for simple config files where content won't collide with the delimiter. Proven 2026-07-14.
- **Signals JSONL reading.** Read `/root/trading/journal/signals.jsonl` with `fs.readFileSync`, split on newline, `JSON.parse` each line, take last 50. Cache for 5 min. Handle missing file gracefully (return empty array).
