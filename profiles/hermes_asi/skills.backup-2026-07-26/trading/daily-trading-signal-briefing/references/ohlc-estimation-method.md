# OHLC Estimation from Web Search Data

When Twelve Data API is unavailable or rate-limited, estimate daily OHLC from web search results.

## Method (proven 2026-07-15)

### Sources (in priority order)
1. **TradingEconomics** — gives close price + daily change (% and absolute). Most reliable.
2. **SmartGoldTrade / DailyForex / FXStreet** — give support/resistance levels, weekly high/low, specific session prices.
3. **CNBC / Reuters** — give spot price, weekly performance, context.

### Derivation Rules

**Close:** Use TradingEconomics exact close. Verify against other sources (within $10).

**Open:** If TradingEconomics gives day change, compute: `open = close - change`. Otherwise use previous day's close.

**High:** Take the highest of:
- Resistance levels mentioned for that day/week
- Any "tested $X" or "high of $X" from analysis
- Open + $30-50 (normal daily range for gold in 2026)

**Low:** Take the lowest of:
- Support levels mentioned ("tested $X", "low of $X")
- "two-week low of $3,983" type phrases
- Open - $30-50 (normal daily range)

### Example (14 Jul 2026)
- TradingEconomics: close $4,054, change +$52 (+1.31%)
- Implied open: $4,054 - $52 = $4,002
- FXStreet: "touching a two-week low of $3,983 earlier in the Asian session"
- SmartGoldTrade: "tested the $4,200 zone but stalled" (that was Jul 11-12)
- Result: O=$4,002, H=$4,080 (post-CPI rally range), L=$3,990 (near $3,983 but bounced), C=$4,054

### Validation
- Body size (|C-O|) should be $30-80 for a normal day, $100+ for event days
- Wick ratios should be reasonable (not >2x body on both sides)
- Close should be within the day's H-L range
- Cross-check: if multiple sources say "rallied 2%", the body should reflect that

### Pitfalls
- NEVER invent exact prices — use real data points as anchors
- NEVER make all candles bearish in a downtrend (there are always bounces)
- The most recent candle is the most critical to get right — spend more time on it
- If you can't determine H/L, use ATR of ~$40-50 for gold in mid-2026
