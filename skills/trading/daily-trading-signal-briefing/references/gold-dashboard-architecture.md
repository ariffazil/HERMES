# Gold Dashboard Architecture & Common Issues

> Live at `https://arif-fazil.com/gold/` | `https://arif-fazil.com/wealth/gold/`
> 2026-07-17 — built from session debug session

## Architecture

```
Browser → arif-fazil.com/gold/
           │
           ▼
         Caddy (reverse proxy)
           │
           ├── /gold/*  → /var/www/html/gold/index.html  (static)
           ├── /wealth/gold/ → /var/www/html/gold/        (same HTML)
           └── /wealth/gold/api/* → strip_prefix → localhost:3456  (gold-api)
```

**Frontend:** `/var/www/html/gold/index.html` — 74KB single-page HTML/JS
**Backend:** gold-api systemd service on port 3456 (Node.js + Python bridge)
**Chart:** TradingView Lightweight Charts (loaded from unpkg CDN)
**Refresh:** 60s auto-refresh via `setInterval(refreshAll, CONFIG.REFRESH_INTERVAL)`

## Key API Endpoints (gold-api :3456)

| Endpoint | Used by dashboard? | What it returns |
|---|---|---|
| `/api/ticker` | YES — `refreshTicker()` | Price, change%, RSI, EMA20/50/200, support[], resistance[], pivot, emaTrend |
| `/api/gold/signal_v2` | Indirectly | Full signal with regime, entry/SL/TP, zones, confluence |
| `/api/gold/apex` | No (for agents) | G/C_dark/dS market state |
| `/api/gold/levels` | No | 1H + Daily S/R levels |
| `/api/gold/macro` | YES — macro ticker bar | DXY, US10Y, VIX, Silver, Gold/Silver ratio |
| `/api/gold/calendar` | YES — economic events | ForexFactory high-impact events |

## Caddy Routing (from /etc/caddy/Caddyfile)

```
# Gold chart app API — reverses to gold-api
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

# Direct route — MUST include redirect for bare /gold
redir /gold /gold/ 308
handle /gold/* {
    root * /var/www/html/gold
    try_files {path} /index.html
    file_server
}
```

## Critical: Trailing Slash Bug (FIXED 2026-07-17)

**Problem:** Caddy's `handle /gold/*` matches `/gold/xxx` but NOT bare `/gold` (no trailing slash). Request fell through to SPA catch-all → served arif-fazil.com homepage instead of gold dashboard.

**Symptoms:**
- `arif-fazil.com/gold` → 10KB (wrong — homepage HTML)
- `arif-fazil.com/gold/` → 75KB (correct — gold dashboard)
- `arif-fazil.com/wealth/gold/` → 75KB (correct)

**Fix:** Added `redir /gold /gold/ 308` before the handle block.
```bash
sudo sed -i '/# Gold dashboard.*direct route/a\\tredir /gold /gold/ 308' /etc/caddy/Caddyfile
sudo caddy fmt /etc/caddy/Caddyfile --overwrite
sudo systemctl reload caddy
```

Same pattern applies to `/oil` and `/gas` routes.

## Stale Data Issue (INVESTIGATED 2026-07-17)

**Symptom:** Dashboard shows price from 2 days ago (2026-07-16), not live data.

**Root cause:** HTML has hardcoded fallback values (lines 1285-1288, 1306):
```html
<span class="level-chip support">S1 <span class="val">$4,020</span></span>
<span class="val" id="pulseTimestamp">2026-07-16 08:42 MYT</span>
```

JS fetches from `CONFIG.API_BASE = window.location.origin + '/wealth/gold/api'` → calls `/wealth/gold/api/ticker` → Caddy strips prefix → `localhost:3456/api/ticker`.

**API works from server-side:** `curl localhost:3456/api/ticker` returns live data ($4,023 on Jul 18).

**Possible causes for browser stall:**
- CORS headers on gold-api responses (check `Access-Control-Allow-Origin`)
- JS error in browser console halting refreshAll()
- CSP blocking the API fetch
- Cloudflare caching the HTML page (bypass: add `Cache-Control: no-cache` header)

## How Buy/Sell Zones Are Computed

1. **Source:** 1H chart, 20-candle window for pivot detection
2. **Support** = recent swing lows (price reversed up from here)
3. **Resistance** = recent swing highs (price reversed down from here)
4. **Strength** = number of times price touched/reversed at a level

**Regime determines zone assignment:**
- UPTREND → Buy Zone = nearest support below price, Sell Zone = nearest resistance above
- DOWNTREND → Sell Zone = nearest resistance above (sell the rally), Buy Zone = nearest support below (deep value)
- SIDEWAYS → Buy Zone = nearest support, Sell Zone = nearest resistance

**Engine code:** `/root/trading/signals/regime.py` — `find_zones()` + `generate_signal_v2()`

## Adding New Endpoints to gold-api

1. Add Python CLI command to `/var/www/html/gold/api/fetch_gold.py` (function `cmd_XXX`)
2. Add to CLI choices and handlers dict in `fetch_gold.py`
3. Add endpoint to `/var/www/html/gold/api/server.js` handlers object
4. Add short alias (without `/gold/` prefix) for Caddy strip_prefix compatibility
5. Restart: `systemctl restart gold-api`
6. Test: `curl -sf localhost:3456/api/XXX`

**Arif's rule:** "Extend gold-api, NEVER new servers." No new ports, no new services.

## Troubleshooting Quick Reference

```bash
# Check gold-api health
curl -s localhost:3456/health | python3 -m json.tool

# Check Caddy route
curl -s -o /dev/null -w "%{http_code} %{size_download}" https://arif-fazil.com/gold/
curl -s -o /dev/null -w "%{http_code} %{size_download}" https://arif-fazil.com/wealth/gold/api/ticker

# Check website is serving gold HTML (75KB+), not homepage (10KB)
curl -s https://arif-fazil.com/gold/ | wc -c

# Restart gold-api
systemctl restart gold-api

# Reload Caddy after routing changes
sudo systemctl reload caddy

# View gold-api logs
journalctl -u gold-api --since "5 min ago" --no-pager
```
