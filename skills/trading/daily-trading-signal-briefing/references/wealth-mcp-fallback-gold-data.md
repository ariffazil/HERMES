# WEALTH MCP Gold Data Fallback (Proven 2026-07-27)

## Context

The WEALTH organ on port 18082 has a `capital_market` tool that can serve live gold data (XAUUSD price, commodities, FX). However, the MCP bridge can be unreachable even when the underlying organ health-check passes. This doc documents the fallback chain.

## Fallback Order

### 1. WEALTH capital_market (primary — try first)

```bash
# Step A: Init session (WEALTH requires session_id post-2026-07-18)
curl -X POST http://localhost:8088/mcp -d '{
  "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"arif_init","arguments":{
    "actor_id":"Hermes","intent":"gold market data query",
    "requested_authority":"OBSERVE_ONLY"
  }}
}' | jq .

# Step B: Query commodity (XAUUSD) and FX (USD/MYR)
# Use the session_token from arif_init response
{"name":"capital_market","arguments":{
  "mode":"commodity","commodity":"xauusd",
  "session_id":"SEAL-xxxx", "session_token":"sct_v1.ey..."
}}
{"name":"capital_market","arguments":{
  "mode":"fx","base":"USD","targets":"MYR",
  "session_id":"SEAL-xxxx", "session_token":"sct_v1.ey..."
}}
```

**Failure modes:**
- `SESSION_REQUIRED` error → do arif_init first, retry
- `MCP server 'wealth' is unreachable after 6 consecutive failures` → MCP bridge down. Use web fallback.

### 2. Gold-API (port 3456) — Preferred internal fallback

If gold-api is running, it's faster and more reliable than web search:

```bash
curl -sf localhost:3456/api/gold/ticker      # Price, RSI, EMAs, signal
curl -sf localhost:3456/api/gold/macro        # DXY, VIX, US10Y
curl -sf localhost:3456/api/gold/calendar     # Economic events
curl -sf localhost:3456/api/gold/apex         # Full market intelligence
```

See `references/gold-data-apis.md` for complete API docs and Caddy routing details.

**Failure mode:** If gold-api returns 500 with `"No module named 'trading'"`, the `/root/trading/` module is missing. Use ticker-only endpoints (/api/gold/ticker) and web search for narrative.

### 3. Web fallback (when BOTH WEALTH MCP AND gold-api fail)

Proven chain from 2026-07-27:

| Data needed | Source | Method | Reliability |
|---|---|---|---|
| **Live price** | AlanChand (alanchand.com/en/gold-price/usd_xau) | smart_fetch | ✅ Good — shows current/open/high/low |
| **Spot + narrative** | TradingEconomics (tradingeconomics.com/commodity/gold) | smart_fetch | ✅ Good — narrative context + spot price |
| **Technical (RSI, S/R, EMAs)** | Clearank (clearank.com/forex/xau-usd/) | smart_fetch | ✅ Best — full technical breakdown |
| **USD/MYR** | Exchange Rates UK (exchangerates.org.uk) | smart_fetch | ✅ Live rate ± intraday range |
| **YouTube analysis** | youtube.com | smart_fetch | ⚠️ Medium — good for event calendars |

**Execution pattern:**

```python
# Three parallel fetches
results = {
  "price": smart_fetch("https://alanchand.com/en/gold-price/usd_xau"),
  "tech": smart_fetch("https://clearank.com/forex/xau-usd/"),
  "fx": smart_fetch("https://www.exchangerates.org.uk/Dollars-to-Malaysian-Ringgit-currency-conversion-page.html"),
  "narrative": smart_fetch("https://tradingeconomics.com/commodity/gold"),
}
```

Web search fallback for fast confirmation:
```
web_search("XAUUSD gold price today 27 July 2026")
web_search("XAUUSD technical analysis support resistance July 2026")
web_search("USD MYR exchange rate today July 2026")
```

## Data extracted from each source (proven 2026-07-27)

### AlanChand
- Current XAUUSD price, daily change (USD and %), yesterday close
- 24h min/max, 7-day range, 30-day range, 365-day range

### TradingEconomics
- Narrative context (geopolitical events, Fed policy, macro drivers)
- Forecast: quarterly and 12-month targets
- ATH (All Time High) — was $5,608 in Jan 2026

### Clearank
- RSI(14), MACD, SMA50, SMA200 — exact numbers
- EMA20 — dynamic support level
- Day open/high/low, prev close
- Key insight: "price above 20-day EMA = bullish short-term, below 50-day SMA = resistance"

### Exchange Rates UK
- Live USD/MYR, daily change %, intraday range
- 7-day and 30-day trend
- Month high/low

## Producing the Signal from Fallback Data

From the web data, compute these metrics:

| Metric | Formula / Source |
|---|---|
| **Current price** | AlanChand or TradingEconomics spot |
| **Bias (short-term)** | Price > 20-day EMA → Bullish; RSI 50-70 → Bullish; both → strong Bullish |
| **Bias (medium-term)** | Price < 50-day SMA → capped, resistance at SMA50 |
| **S1** | 20-day EMA (from Clearank) |
| **S2** | Round number below (e.g., $4,000 psychological) |
| **R1** | 50-day SMA (from Clearank) |
| **R2** | 30-day high (from AlanChand) |
| **R:R** | (R1 - price) : (price - S1) if bullish; (price - S1) : (R1 - price) if bearish |
| **Confluence** | Count confirming indicators (RSI bullish + above EMA + R:R > 1:2 + no event risk) |
| **Risk level** | Low if R:R > 1:3 and RSI not overbought/oversold; High if RSI > 70 or < 30 |
| **Confidence** | Estimate: 70%+ if confluence ≥ 3, 50-70% if confluence = 2, < 50% if confluence < 2 |

## Populating the Gold Page

The page at https://arif-fazil.com/gold/ has these data slots that need filling:

- `#pulsePrice` — current price
- `#pulseDelta` / `#pulsePct` — daily change
- `#biasPill` — bias label (BULLISH/BEARISH/NEUTRAL)
- `#biasConfluence` — confluence level
- `#riskBars` — risk indicator (1-5 bars)
- `#maVerdict` — SEAL/SABAR/HOLD badge
- `#predRead` — narrative one-liner
- `#pulseDriver` — what's driving price
- `.level-chip.S1 .val` etc. — S1/S2/R1/R2 values
- `#mainChart` — lightweight-charts candlestick chart data

The page is a static HTML+JS app; it pulls data from an API at runtime via JavaScript. To populate it, either:
1. Update the WEALTH capital_market backend to serve live data
2. Or build a cron that pushes data into the page's API endpoint

## Why This Happens

The WEALTH MCP bridge can fail even when:
- `systemctl is-active wealth-organ` → `active`
- `curl -sf http://localhost:18082/health` → healthy JSON response

This is a known MCP bridge transient failure. The organ itself is healthy but the MCP transport layer temporarily drops. The web fallback works in < 2 seconds and produces the same quality data.
