# Frontend API-to-DOM Audit Pattern

> For federation dashboards served as static SPAs with backend API layers.
> Proven on Gold Dashboard 2026-07-17.

## The Pattern

When auditing a federation dashboard (Gold, Brent Crude, Natural Gas):
1. **Confirm the transport layer** — `curl` the Caddyfile, identify the `root` directory and API proxy
2. **Probe API directly** — `curl` all API endpoints (`/health`, `/api/ticker`, `/api/macro`, `/api/calendar`, `/api/signal_v2`)
3. **Check browser rendering** — load the page, compare what's in the DOM vs what the API returns
4. **Identify binding gaps** — if API returns data but DOM shows "—" or "Loading...", the JS isn't consuming the API response

## Gold Dashboard Architecture (2026-07-17)
```
/var/www/html/gold/index.html   — 72KB SPA (static HTML+JS+CSS)
localhost:3456                  — Gold API (Node.js, 12 endpoints)
Caddy: handle /wealth/gold/*    → root * /var/www/html/gold
Caddy: @wealth_gold_api         → reverse_proxy localhost:3456
```

## API Endpoints (Gold)
| Endpoint | Returns | Status (2026-07-17) |
|----------|---------|---------------------|
| `/health` | uptime, endpoints, cache_size | ✅ |
| `/api/ticker` | price, change, RSI, EMAs, S/R levels | ✅ |
| `/api/macro` | DXY, VIX, US10Y, silver, GSR | ✅ |
| `/api/calendar` | economic events array | ✅ |
| `/api/gold/signal_v2` | direction, R:R, confluence, verdict | ✅ |
| `/api/gold/history` | historical prices | ✅ |

## Common Failure Modes

1. **API returns data, DOM shows "—"** — JS fetch succeeds but the rendering pipeline doesn't bind the response to the DOM elements. Likely a missing `.then()` or DOM selector mismatch.

2. **Calendar stuck on "Loading events..."** — same pattern: `fetch('/api/calendar')` succeeds but the DOM update never fires.

3. **Price discrepancy between header and body** — header uses one data source (possibly cached/stale), body sections use another. Check if different API endpoints or different update intervals.

4. **Oil API down** — systemd unit `oil-api` or equivalent not running. `systemctl start oil-api` or equivalent.

## Diagnostic Commands
```bash
# Is the page serving?
curl -sI https://arif-fazil.com/wealth/gold/ | head -5

# Is the API alive?
curl -s http://localhost:3456/health | python3 -m json.tool

# What does the API actually return?
curl -s http://localhost:3456/api/macro | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d,indent=2))"

# Compare API price vs what's in the HTML
curl -s http://localhost:3456/api/ticker | python3 -c "import json,sys; print(json.load(sys.stdin)['price'])"
```

## Fix Approach

For frontend binding gaps, the fix is in the `index.html` JavaScript:
1. Open the HTML and find the macro indicators section
2. Trace the `fetch('/api/macro')` call
3. Verify the response is being processed correctly (check JSON structure matches DOM selectors)
4. If the fetch call exists but DOM update doesn't, it's a rendering pipeline gap
5. Re-deploy with `scripts/deploy-site.sh gold` or equivalent
