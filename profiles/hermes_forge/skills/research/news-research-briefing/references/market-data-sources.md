# Market Data Sources — Extraction Patterns & Pitfalls

Validated Jul 2026. Browser-based extraction patterns for when Tavily is down.

## CNBC — Commodities & Equities

### URL Patterns (validated)

| Instrument | URL | Notes |
|---|---|---|
| Gold (XAU/USD) | `https://www.cnbc.com/quotes/XAU=` | Spot price. Works reliably. |
| WTI Crude (front month) | `https://www.cnbc.com/quotes/%40CL.1` | Use `%40CL.1`, NOT `CL=F` (404s) |
| Brent Crude (front month) | `https://www.cnbc.com/quotes/%40LCO.1` | Use `%40LCO.1`, NOT `BZ=F` |
| S&P 500 | `https://www.cnbc.com/quotes/.SPX` | |
| Dow Jones | `https://www.cnbc.com/quotes/.DJI` | |
| Nasdaq | `https://www.cnbc.com/quotes/.IXIC` | |

### Extraction via Browser

CNBC pages load with a sidebar, navigation, and ads. For clean price data:

```javascript
// Get main content area (price data lives here)
document.querySelector('main').innerText.substring(0, 3000)
```

Key data points to extract:
- **Last price** — appears after "Last | [time]"
- **Change** — +/- value and percentage
- **Key Stats** — Open, Day High, Day Low, Prev Close
- **Volume** — if available

### Pitfalls

- CNBC's `/quotes/CL=F` returns 404. Use `/quotes/%40CL.1` for WTI.
- Some data carries 15-minute delay. Note the timestamp from the page ("Last | 6:15 PM EDT").
- The "LATEST ON [INSTRUMENT]" section shows news links, not current price — don't confuse them.
- CNBC world markets page (`/world-markets/`) may show stale articles (weeks old). Don't rely on it for current market state.

## XE.com — Forex Rates

### URL Pattern

```
https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MYR
```

Replace `USD` and `MYR` with desired currency pair.

### Extraction

The page shows:
- Mid-market rate at specific UTC time
- Conversion table (1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000 units)

Key data: `1.00 USD = 4.09613284 MYR` with timestamp `Mid-market rate at 15:02 UTC`

### Pitfalls

- XE shows mid-market rate — not the rate you'd get from a bank or money transfer.
- Rate timestamp is important — note the UTC time.
- XE doesn't have commodity quotes. Use CNBC for gold/oil.

## Google Finance

### What Works

- Stock quotes: `https://www.google.com/finance/quote/AAPL:NASDAQ`
- Index quotes: `https://www.google.com/finance/quote/.DJI:INDEXDJX`

### What Doesn't Work

- **Commodity lookups** — `XAU-USD`, `GC=F`, `CL=F` all return "Page Not Found"
- **Forex** — some pairs work, others don't. Unreliable for commodities.

Use CNBC for commodities, XE for forex.

## Alternative Sources (when CNBC fails)

| Source | URL | Coverage |
|---|---|---|
| MarketWatch | `marketwatch.com/investing/future/gold` | Gold, oil, indices |
| Investing.com | `investing.com/commodities/` | Full commodities |
| TradingView | `tradingview.com/symbols/XAUUSD/` | Charts + price |
| Bloomberg | `bloomberg.com/quote/XAUUSD:CUR` | May be paywalled |

## Browser Fallback Chain (complete)

```
1. web_search (Tavily) — fastest, broadest
   ↓ 402 (quota) or 432 (backend down)
2. web_extract on known URLs — may fail on paywalls
   ↓ paywall or timeout
3. browser_navigate → browser_snapshot — always works, slower
   ↓ need cleaner data
4. browser_console extraction — surgical, fastest browser method
```

**Tavily 432 = backend-wide outage.** Do NOT retry web_search or web_extract — both will fail. Switch immediately to browser.

## Data Format Rule

Every market price MUST carry all five fields:

```
| Instrument | Value | Change | Source | Timestamp |
```

Example:
```
| WTI Crude (Aug'26) | $82.47 | +4.46% | CNBC | Jul 17, 6:15 PM EDT |
```

Never combine prices from different dates or sessions into one apparent current range without explaining the time difference.
