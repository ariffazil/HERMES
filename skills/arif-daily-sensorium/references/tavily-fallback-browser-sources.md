# Tavily Fallback & Browser Sources (2026-07-17 proven)

## When Tavily Fails

Both `web_search` and `web_extract` use Tavily under the hood. When Tavily returns **432** (credits exhausted), both tools become useless. Do NOT retry — go straight to browser.

## Proven Browser Sources for Sensorium

### World News
| Source | URL | CAPTCHA? | Notes |
|--------|-----|----------|-------|
| **Al Jazeera** | `aljazeera.com` | No | Best world news. Iran, UK, AI, Ukraine coverage. Fast. |
| Reuters | `reuters.com/world/` | **DataDome** | Blocked. Don't attempt. |
| AP News | `apnews.com/world` | Timeout | Unreliable. Skip. |
| Bloomberg | `bloomberg.com` | **Bot detection** | Blocked. Don't attempt. |

### Malaysia News
| Source | URL | Notes |
|--------|-----|-------|
| **NST Nation** | `nst.com.my/news/nation` | Politics, crime. Rich detail. |
| **NST Economy** | `nst.com.my/business/economy` | GDP, inflation, ringgit, research houses. |
| **NST Corporate** | `nst.com.my/business/corporate` | Bursa, banks, corporate deals. |
| The Star | `thestar.com.my/news/nation` | Timeout occasionally. |

### Market Data
| Data | Source | URL | Format |
|------|--------|-----|--------|
| **Gold (XAU/USD)** | Kitco | `kitco.com/charts/gold` | Bid/Ask, % change, NY time |
| **WTI Crude** | TradingView | `tradingview.com/symbols/USOIL/` | Price, % change, day range |
| **Brent Crude** | TradingView | `tradingview.com/symbols/UKOIL/` | Price, % change, day range. Also has news headlines. |
| **USD/MYR** | XE.com | `xe.com/currencyconverter/convert/?From=USD&To=MYR` | Mid-market rate, UTC timestamp |
| Investing.com | — | Empty page. Skip. |
| Oilprice.com | — | Timeout. Skip. |

## Parallel Navigation Strategy

Browser navigation is sequential (one page at a time). Prioritize:

1. **Al Jazeera** (world + Iran + AI) — snapshot, scroll down once
2. **NST Nation** (Malaysia politics/crime) — snapshot
3. **NST Economy** (GDP, inflation, forecasts) — snapshot
4. **Kitco** (gold) — snapshot
5. **TradingView USOIL** (WTI) — snapshot
6. **TradingView UKOIL** (Brent) — snapshot
7. **XE.com** (USD/MYR) — snapshot

7 navigations × ~5s each = ~35s for all market + news data. Faster than serial Tavily retries.

## Integration With Sensorium Workflow

Replace Workflow §2 ("Build Candidate Event Set") when Tavily fails:

```
§2a. Navigate to Al Jazeera → snapshot → extract world headlines
§2b. Navigate to NST Nation → snapshot → extract Malaysia headlines  
§2c. Navigate to NST Economy → snapshot → extract economic data
§2d. Navigate to Kitco → snapshot → extract gold price
§2e. Navigate to TradingView USOIL → snapshot → extract WTI
§2f. Navigate to TradingView UKOIL → snapshot → extract Brent
§2g. Navigate to XE.com → snapshot → extract USD/MYR
```
