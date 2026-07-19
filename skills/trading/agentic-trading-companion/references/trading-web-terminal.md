# Trading Web Terminal — TradingView-level Chart App

## Stack

- **Frontend:** Single HTML file, TradingView lightweight-charts v4 (CDN)
- **Backend:** Node.js http server (port 3456) + Python yfinance bridge
- **Deployment:** Caddy reverse proxy + systemd service
- **Data:** yfinance GC=F (gold futures), 5-min cache

## Frontend Spec

```
CDN: https://unpkg.com/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js
```

**Features:**
- Candlestick chart (green up, red down)
- EMA 20 (cyan) + EMA 50 (orange) — computed client-side
- Volume histogram below (subtle)
- S/R level lines (green dashed support, red dashed resistance)
- Signal overlay (entry=gold, SL=red dashed, TP=green dashed)
- RSI(14) panel below main chart
- Timeframe selector (H1/H4/D1)
- Info panel overlay (price, change, RSI, EMA status, signal)
- Auto-refresh 60 seconds
- Loading skeleton with shimmer

**Client-side EMA:**
```javascript
function calcEMA(data, period) {
  const k = 2 / (period + 1);
  const ema = [];
  let prev = data[0].close;
  for (let i = 0; i < data.length; i++) {
    const val = data[i].close * k + prev * (1 - k);
    ema.push({ time: data[i].time, value: Math.round(val * 100) / 100 });
    prev = val;
  }
  return ema;
}
```

**Client-side RSI:**
```javascript
function calcRSI(data, period = 14) {
  if (data.length < period + 1) return null;
  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const diff = data[i].close - data[i - 1].close;
    if (diff > 0) gains += diff; else losses -= diff;
  }
  let avgGain = gains / period;
  let avgLoss = losses / period;
  for (let i = period + 1; i < data.length; i++) {
    const diff = data[i].close - data[i - 1].close;
    avgGain = (avgGain * (period - 1) + (diff > 0 ? diff : 0)) / period;
    avgLoss = (avgLoss * (period - 1) + (diff < 0 ? -diff : 0)) / period;
  }
  if (avgLoss === 0) return 100;
  return Math.round((100 - 100 / (1 + avgGain / avgLoss)) * 10) / 10;
}
```

## API Endpoints

| Endpoint | Response |
|---|---|
| `GET /api/gold/history?interval=1h&period=7d` | `[{time, open, high, low, close, volume}]` (Unix seconds) |
| `GET /api/gold/ticker` | `{price, change, changePercent, high24h, low24h, volume24h}` |
| `GET /api/gold/signals` | Array of signal objects from journal |
| `GET /api/gold/macro` | `{dxy, us10y, usd_myr, xau_myr}` |
| `GET /api/gold/levels` | `{support: [...], resistance: [...]}` |

**TradingView format:** `time` is Unix SECONDS (not milliseconds).

## Caddy Config (add to arif-fazil.com block)

```
@wealth_gold_api path /wealth/gold/api/*
handle @wealth_gold_api {
    uri strip_prefix /wealth/gold
    reverse_proxy localhost:3456
}

handle /wealth/gold/* {
    uri strip_prefix /wealth/gold
    root * /var/www/html/arif/wealth/gold
    file_server
    try_files {path} /index.html
}
```

## Systemd Service

```ini
[Unit]
Description=Gold Data API Server (XAUUSD live data)
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/html/arif/wealth/gold/api
ExecStart=/usr/bin/node /var/www/html/arif/wealth/gold/api/server.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

## Data Fetching (Python bridge)

Node.js calls Python for yfinance data:
```python
# fetch_gold.py
import yfinance as yf
import json, sys

interval = sys.argv[1] if len(sys.argv) > 1 else "1h"
period = sys.argv[2] if len(sys.argv) > 2 else "7d"

ticker = yf.Ticker("GC=F")
df = ticker.history(period=period, interval=interval)

candles = []
for idx, row in df.iterrows():
    candles.append({
        "time": int(idx.timestamp()),
        "open": round(row["Open"], 2),
        "high": round(row["High"], 2),
        "low": round(row["Low"], 2),
        "close": round(row["Close"], 2),
        "volume": int(row.get("Volume", 0))
    })

print(json.dumps(candles))
```

## Color Palette

```
BG:        #0d1117
Panel:     #161b22
Gold:      #f0a500
Green:     #3fb950
Red:       #f85149
Cyan:      #58a6ff
Orange:    #ffa657
Text:      #e6edf3
Dim:       #8b949e
Border:    #30363d
```

## Pitfalls

- **yfinance cache:** Cache data for 5 min. Don't hammer Yahoo on every request.
- **TradingView time format:** SECONDS, not milliseconds. Common mistake.
- **CORS:** Set `Access-Control-Allow-Origin` to your domain only.
- **File permissions:** Chown to www-data after creating files in /var/www/html/.
- **Caddy backup:** Always backup Caddyfile before editing: `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak.$(date +%Y%m%d)`
