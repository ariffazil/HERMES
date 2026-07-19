# Proven Data Gathering Pipeline (2026-07-14 Pilot)

## What Works

### Price Data
1. **Twelve Data** (twelvedata.com/markets) — has OHLC in snippet, no API key needed for basic search result
   - Search: `web_search("XAUUSD price [DATE]")` → Twelve Data result shows Open/High/Low/Close/%Change
   - Example: "Jul 13, 2026 | 4.1114K | 4.1130K | 3.9866K | 3.9992K | -2.7313%"
   - Parse the K suffix: 4.1114K = $4,111.4

2. **TradingEconomics** — good for spot verification but often behind paywall
3. **RoboForex** — snippet shows bid/ask (e.g., "3999.43 USD and 3999.5 USD")
4. **Vantage Markets** — headline often includes current price (e.g., "Gold Falls to $4050 Before CPI")

### Technical Analysis
1. **DailyForex** — best structured analysis with concrete S/R levels and trading signals
   - URL pattern: `dailyforex.com/forex-technical-analysis/YYYY/MM/xauusd-analysis-DD-month-YYYY/`
   - Contains: support/resistance points, bullish/bearish scenarios, entry/SL/target, RSI commentary
   - `web_extract()` works well on these pages

2. **Intellectia.ai** — good macro context + range (e.g., "consolidating between $3,900 and $4,300")

3. **YouTube video descriptions** — often list this week's events (CPI, PPI, FOMC dates)
   - Example: "Tuesday 14 July CPI, warsh testify | Wednesday 15 July PPI | Thursday 16 July retail sales"

### Events Calendar
1. **YouTube analysis descriptions** — surprisingly reliable for event dates
2. **Web search** `"gold economic events this week [month] [year]"` 
3. **TradingEconomics calendar** — but often paywalled

## Execution Pattern

```
# 1. Three parallel searches
web_search("XAUUSD gold price today [DATE]")
web_search("gold news today [MONTH] [YEAR] economic events")  
web_search("XAUUSD technical analysis support resistance [MONTH] [YEAR]")

# 2. Extract the best TA page
web_extract(["https://dailyforex.com/..."])

# 3. Parse: current price, S/R levels, RSI, events
# 4. Set signal levels from real S/R (not formulaic)
# 5. Generate chart + PDF via write_file() + terminal()
```

## Pitfalls Found During Pilot

- **execute_code sandbox** does NOT have matplotlib/reportlab even after `pip install` in terminal. Must use `write_file()` to create script + `terminal("python3 script.py")` to run.
- **Twelve Data K suffix** — 4.1114K means $4,111.4, not $4,111,400. Parse carefully.
- **Multiple sources disagree** on exact price. Use the most recent + cross-verify.
- **DailyForex pages repeat content 3x** in web_extract (ad injection). The first block is the real content.
- **Market hours matter** — XAUUSD trades Sun 6pm - Fri 5pm ET. Outside this, price is last close.
- **YouTube descriptions** are gold mines for event calendars but never for price targets.
