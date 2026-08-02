---
name: wealth-commodity-dashboard
description: "Manage the three WEALTH commodity dashboards — Gold, Brent Crude (Oil), Natural Gas — at arif-fazil.com/{gold,oil,gas}"
version: 1.0.0
tags: [wealth, dashboard, gold, oil, gas, commodity, live-data, caddy, temporal-intelligence]
---

# WEALTH Commodity Dashboards

Three live commodity dashboards serving **temporal State-of-Truth (SOT)** — every number on screen is pulled from a live API, never hardcoded.

| Dashboard | URL | API port | Symbol | Status (2026-08-03) |
|---|---|---|---|---|---|
| Gold | `arif-fazil.com/gold/` | `:3456` | XAUUSD | ✅ LIVE — 1,753-line TradingView dashboard with `fetch_gold.py` API |
| Brent Crude (Oil) | `arif-fazil.com/oil/` | `:3457` | XBRENT | 🔴 STALE — 121-line stub with **hardcoded $84.32** (actual: ~$90.12). Not using live API. |
| Natural Gas | `arif-fazil.com/gas/` | `:3458` | XNATGAS | ⚫ MISSING — `fetch_gas.py` (1,294 lines) exists but **no HTML dashboard**. wealth.arif-fazil.com/gas/ returns empty shell. |

**API scripts exist for all three** at `/root/arif-fazil.com/sites/arif-fazil.com/dist/{gold,gas}/api/`:
- `fetch_gold.py` (1,269 lines) — GC=F, XAUUSD=X fallback, full tech indicators + signals
- `fetch_gas.py` (1,294 lines) — NG=F, NATGAS=X fallback, full tech indicators + signals
- **`fetch_oil.py` does NOT exist** — Oil dashboard has no live data pipeline

## Architecture

**Dual surfacing (PROVEN 2026-08-03):** Commodity pages exist in TWO surfaces:
1. **React SPA:** `/world/oil`, `/world/gas`, `/world/gold` — CommodityPage component, fetches from `/{slug}/api/ticker`
2. **Static standalone:** `/oil/`, `/gas/`, `/gold/` — standalone HTML served from `/var/www/html/{oil,gas,gold}/`

Legacy redirect: `/oil/` → `/world/oil` etc. The static pages are NOT React — they're standalone with their own JS/API calls.

```
Browser → Caddy → Static HTML (/var/www/html/{gold,oil,gas}/index.html)
                    ↓ JS fetch()
                  Caddy proxy /wealth/{gold,oil,gas}/api/* → localhost:34{56,57,58}
                    ↓
                  Commodity API (signal_v2, ticker, apex, macro, levels, calendar)
```

Caddy config (in main `arif-fazil.com` block):
```caddyfile
@wealth_gold_api path /wealth/gold/api/*
handle @wealth_gold_api {
    uri strip_prefix /wealth/gold
    reverse_proxy localhost:3456
}
handle /wealth/gold/* { ... }
redir /gold /gold/ 308       # ← CRITICAL: bare path redirect
handle /gold/* { ... }
```

Same pattern for `/oil` and `/gas`.

## Iron Rules

### 1. NEVER hardcode data in HTML
Every price, S/R level, regime, score, and analysis text MUST come from the live API via JavaScript. Hardcoded values = **stale lies that cost Syed money**.

Bad (old):
```html
<span id="pulsePrice">$4,063.40</span>           ← JUL 16 — BASI
<span class="signal-score bullish">Bullish</span> ← LIE — regime is BEARISH
```

Good (now):
```html
<span id="pulsePrice">—</span>                    ← placeholder, JS fills
<span class="signal-score" id="tfTrendScore">—</span>
```

### 2. Boot sequence: DATA BEFORE CHART
TradingView chart is heavy. `refreshTicker()` and `refreshMacro()` MUST fire FIRST (await), then `renderChart()` async (fire-and-forget). The pulse bar populates in <1 second while the chart loads in background.

```javascript
// ✅ CORRECT
await Promise.all([refreshTicker(), refreshMacro()]);
renderChart('4H');  // no await — background
refreshApex(); refreshSignals(); refreshTechnicalForge(); refreshCalendar();
```

```javascript
// ❌ WRONG (old way — chart blocked data for 5+ seconds)
await renderChart('4H');
await Promise.all([refreshTicker(), ...]);
```

### 3. EVERY number needs a timeframe label
- S/R levels: append `1H` label
- Driver text: append `TF: 1H levels, 4H regime`
- Regime: show in bias pill (`BEARISH · 📉 DOWNTREND`)
- Timestamp: show `● LIVE` marker with MYT time

### 4. Technical Forge must be dynamic
All four cards (TREND, MOMENTUM, STRUCTURE, VOLUME) must populate from `refreshTechnicalForge()` which fetches ticker + signal_v2 + apex data. Generate analysis text from live numbers, not pre-written prose.

### 5. Gold is the template for oil/gas
All three dashboards share identical structure — only the API endpoint and commodity labels differ. When fixing one, copy the template and sed-replace:

```bash
cp /var/www/html/gold/index.html /var/www/html/oil/index.html
sed -i \
  -e 's|/wealth/gold/api|/wealth/oil/api|g' \
  -e "s|ASSET: 'gold'|ASSET: 'oil'|g" \
  -e 's|XAUUSD|Brent Crude|g' \
  -e 's|yfinance:GC=F|yfinance:BZ=F|g' \
  /var/www/html/oil/index.html
```

## Key Files

| File | Purpose |
|---|---|
| `/var/www/html/gold/index.html` | Gold dashboard (canonical template) |
| `/var/www/html/oil/index.html` | Oil dashboard (copy from gold) |
| `/var/www/html/gas/index.html` | Gas dashboard (copy from gold) |
| `/etc/caddy/Caddyfile` | Caddy routes for all three |
| `/root/trading/` | Gold signal engine source |

## Dashboard Sections (all live via JS)

| Section | Data source | Refresh |
|---|---|---|
| **Pulse bar** (price, S/R, regime, RSI) | `apiFetch('/ticker')` | 2 min |
| **Macro ticker** (DXY, US10Y, VIX, Silver, GSR) | `apiFetch('/macro')` | 5 min |
| **Market Pulse** (APEX clarity, risk, trend energy) | `apiFetch('/apex')` | 5 min |
| **Technical Forge** (Trend, Momentum, Structure, Volume) | ticker + signal_v2 + apex | 5 min |
| **Synthesis & Decision Gate** | `apiFetch('/signal_v2')` | 5 min |
| **Calendar events** | `apiFetch('/calendar')` | 5 min |
| **Chart** (TradingView) | Lightweight Charts library | on timeframe change |

## Caddy Trailing-Slash Fix (PROVEN 2026-07-18)

`handle /gold/*` does NOT match `/gold` (no trailing slash). Bare path falls through to SPA catch-all → serves homepage instead of dashboard.

**Fix:** Add explicit redirect BEFORE each handle block:
```caddyfile
redir /gold /gold/ 308
handle /gold/* { ... }
redir /oil /oil/ 308
handle /oil/* { ... }
redir /gas /gas/ 308
handle /gas/* { ... }
```

## Verification

```bash
# All redirects working
curl -s -o /dev/null -w "%{http_code} → %{redirect_url}\n" https://arif-fazil.com/gold
# Should return: 308 → https://arif-fazil.com/gold/

# All pages returning live data (not homepage HTML)
curl -s https://arif-fazil.com/gold/ | grep -c "pulsePrice\|● LIVE"
curl -s https://arif-fazil.com/oil/ | grep -c "pulsePrice\|● LIVE"
curl -s https://arif-fazil.com/gas/ | grep -c "pulsePrice\|● LIVE"

# APIs healthy
curl -s localhost:3456/health | jq .status
curl -s localhost:3457/health | jq .status
curl -s localhost:3458/health | jq .status
```

## Pitfalls

- **Iron Rule #1 IS being violated (2026-08-03).** The Oil dashboard (`/var/www/html/oil/index.html` or `dist/wealth/oil.html`) has hardcoded $84.32 for Brent, $80.15 for WTI, $3.42 for NatGas — while current market is ~$90.12 Brent. The Rule says "NEVER hardcode data in HTML" but this stub was shipped with hardcoded values and no API fetch. **Fix:** create `fetch_oil.py` (clone from `fetch_gas.py`, change ticker to BZ=F), build oil.html from gold template, wire to live API. Until fixed, the oil page is a "stale lie" per Iron Rule #1.
- **Gas has an API but no HTML page.** `fetch_gas.py` (1,294 lines) is complete with yfinance ticker (NG=F), EMA/RSI/ATR, signal generation, support/resistance, macro context. But there is no `/var/www/html/gas/index.html` dashboard. The wealth.arif-fazil.com/gas/ route shows an empty stub. **Fix:** clone gold.html → gas.html, sed-replace API paths + labels + ticker.
- **Oil has no fetch script at all.** Unlike gold and gas which have `fetch_*.py` scripts, oil has neither a live API pipeline nor a proper HTML dashboard. It's the most broken of the three.
- **SPA CommodityPage must fetch the SHORT API path**
- **Hardcoded defaults rot FAST.** Within 48 hours, the market moves and the site lies. Always replace hardcoded values with `—` loading indicators.
- **Copy-paste between commodities must change ALL references.** yfinance ticker, API path, asset name, chart title, currency labels. Test with curl after sed.
- **The `patch` tool refuses `/etc/caddy/Caddyfile`** — use `sudo sed` via terminal for Caddy edits, then `caddy validate` + `systemctl reload caddy`.
- **Browser snapshots taken too early show `—` everywhere.** Wait 5+ seconds for JS to finish before verifying. The pulse bar populates first (~1s), Technical Forge second (~3s), chart last (~5s).
- **If site shows stale data despite live API,** check: (1) Caddy proxy working? (2) Does the backend have the SHORT endpoint alias (not just full path)? (3) Browser console JS errors?
- **The synthesis/verdict text is generated by refreshSignals()** — it reads judge_reason from signal_v2 API. If verdict shows old text, refreshSignals may not have run yet or the API call failed.
