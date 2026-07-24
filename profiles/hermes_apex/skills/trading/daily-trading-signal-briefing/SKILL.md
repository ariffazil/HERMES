---
name: daily-trading-signal-briefing
description: "Daily XAUUSD gold trading signal for rakyat marhaen. One-page PDF, dark OANDA-style chart, zoomed candlesticks, buy/sell zones near current price, EMA 20/50, R:R visual, simple language. Not broker jargon."
triggers:
  - "gold signal"
  - "trading signal"
  - "XAUUSD signal"
  - "daily gold"
  - "emas signal"
tags: [trading, xauusd, gold, signal, daily, pdf]
---

# Daily XAUUSD Trading Signal Briefing

## Audience
Rakyat marhaen — common people, not brokers. Simple language. BUY HERE, SELL HERE, SL HERE. No Fibonacci, no Elliott Wave jargon.

## Teacher
Abang Udin (@rico_ricaldo_33) — pure technical trader, OANDA platform, XAUUSD only.

## Operating Mode (sovereign 2026-07-14)

**LONG ONLY.** Short is not in the playbook. R:R on short near oversold support = terrible. Short only becomes relevant if price breaks major support with confirmation.

**Two signals every morning:**
1. **BUY SIGNAL** — where to enter long, SL, targets, R:R
2. **EXIT LEVELS** — where to take profit / sell if already holding gold

**Jiwa belum kuat = NORMAL.** This is preparation. Watch first. Learn the zones. Paper trade mentally. When jiwa ready, the signal will be there. No pressure. Market sentiasa ada esok.

## Core Principles (from Abang Udin, 14 Jul 2026)

1. **TEMPORAL** — Buy/sell zones MUST be close to current market price. If price is $4,003, buy zone = $3,995-4,010. Not $200 away.
2. **OANDA CHART STYLE** — Zoom IN, big candles, tight Y-axis (only relevant range), no wasted space. Labels on Y-axis, not blocking candles.
3. **REAL CANDLESTICKS** — Red filled = bearish (close < open), Green hollow = bullish (close > open). Hammer at support = reversal. Doji = indecision. Shooting star = warning. Bearish engulfing = trend change.
4. **EMA 20 + 50** — Blue = EMA 20 (fast), Orange = EMA 50 (slow). Dynamic support/resistance. Death cross = bearish, Golden cross = bullish.
5. **ONE CHART, ONE WORLD** — Everything on one chart. Buy zone, sell zone, SL, targets, R:R. No cluttered tables dominating. Chart = king.
6. **R:R VISUAL** — Show risk arrow (red) and reward arrow (green) on chart. R:R number big and bold. If R:R < 1:2, say NO TRADE.
7. **CONFIRMATION** — Wait for candle close above EMA 20 on 1H before entering. Don't catch falling knives.
8. **EVENT DAYS** — CPI, NFP, FOMC, Fed speak = wait for data. Hot = no trade. Cold = confirm. Don't force it.

## Chart Generation (Pro — Preferred)

**Preferred renderer:** `/root/trading/scripts/chart_pro.py` — matplotlib-based, 180 DPI, dark theme, mobile-ready. Replaces older chart approaches.

```bash
cd /root/trading && python3 scripts/chart_pro.py --signal SHORT --entry 4055 --sl 4076 --tp 4027 --json
```

Output: `/tmp/xauusd_chart.png` (300KB, 180 DPI, landscape)
JSON metadata: price, bias, confidence, rsi, ema20/50/200, support[], resistance[], signal, entry, sl, tp

Features: candlesticks, EMA 20/50/200, S/R levels (max 2-3 clean), signal overlay with zone shading, RSI panel, bias pill, confidence %, bottom synthesis banner.

### Chart Pro Pitfalls

- **`$` in matplotlib text = LaTeX math mode crash.** Dollar signs in any text passed to `ax.text()`, `fig.text()`, `ax.set_title()` trigger `ParseException: Expected end of text, found '$'`. Fix: replace `$` with `USD` in all matplotlib text strings, OR set `plt.rcParams['text.usetex'] = False` + `plt.rcParams['mathtext.default'] = 'regular'` before any plot calls. The chart_pro.py already handles this.
- **numpy int64/float64 in JSON output (proven 2026-07-16).** When chart_pro.py returns metadata via `--json`, numpy types (`int64`, `float64`) crash `json.dumps()` with `TypeError: Object of type int64 is not JSON serializable`. Fix: use a custom JSON encoder that converts `np.integer` → `int`, `np.floating` → `float`, `np.ndarray` → `list`. Already patched in chart_pro.py (2026-07-16). General rule: ANY script that returns JSON from numpy/pandas data MUST use a custom encoder — never assume `json.dumps()` handles numpy types.
- **Plotly + kaleido = too slow for server-side.** Plotly with kaleido export takes 60+ seconds for a single chart. matplotlib generates the same chart in 3-5 seconds. Use matplotlib for cron jobs and server-side generation. Plotly only for interactive web dashboards.
- **`execute_code()` sandbox lacks matplotlib.** The hermes_tools sandbox uses a different venv. Use `write_file()` + `terminal()` for chart generation. chart_pro.py runs via terminal.
- **Venv path for cron-triggered scripts (proven 2026-07-16).** When running `python3` in cron context, the shell wrapper may try to source arifOS auto-venv functions (`_arifos_auto_venv`, `_arifos_auto_env`) which fail with `command not found`. Always use `/root/venv/bin/python3` explicitly for cron-triggered chart/engine scripts, not bare `python3`.

### Older Chart Approaches (Fallback)

If chart_pro.py fails, fall back to the template at `templates/gold_signal_chart.py` (also matplotlib, same dark theme, slightly different layout).

When `/root/trading/` is entirely missing, use the yfinance OHLC fallback chain documented in `references/chart-fallback-yfinance.md` (proven 2026-07-20).

### Chart Specification
- **Theme**: Dark (#0d1117 background) — both chart AND PDF must use dark theme
- **Size**: 14×8 inches, 150 DPI
- **Y-axis**: Zoomed to relevant range only (current price ± $50-80)
- **Candles**: 15-20 daily candles, big (width 0.55)
- **EMA**: EMA 20 (blue #58a6ff, 2.5pt), EMA 50 (orange #f0883e, 2.5pt). Compute from extended data (50+ candles) not just visible 18.
- **Buy zone**: Green band + green border lines (3pt). LONG ONLY — no sell zone.
- **SL**: Red dashed (-. , 2.5pt)
- **Targets**: Green/orange dotted (: , 2pt)
- **R:R**: Box top-left, big number. Calculate from ENTRY_MID (midpoint of buy zone), NOT current price.
- **RSI**: Calculate from OHLC data (numpy), not hardcoded values
- **Current price**: Gold marker + label
- **Labels**: On Y-axis side, not inline blocking candles

### PDF Output
- Landscape A4
- Chart = main content (29cm × 16cm)
- Strategy table below: BUY SIGNAL (entry, SL, targets, R:R) + EXIT LEVELS (TP1, TP2, trail stop, emergency exit)
- Event warning if CPI/NFP/FOMC/Fed speak today
- One-line verdict
- Disclaimer
- Save to `/root/GOLD-SIGNAL-{DATE}.pdf`

## Signal Format

### BUY SIGNAL (Long entry)
| | LEVEL |
|---|---|
| ENTRY | $X - $Y |
| STOP LOSS | $Z |
| TARGET 1 | $T1 (+$N) |
| TARGET 2 | $T2 (+$N) |
| R:R | 1:X.X / 1:Y.Y |
| STATUS | READY / WAIT FOR DATA / NO TRADE |

### EXIT LEVELS (Sell if already holding)
| | LEVEL | ACTION |
|---|---|---|
| TAKE PROFIT 1 | $TP1 | Jual separuh (50%) |
| TAKE PROFIT 2 | $TP2 | Jual semua (100%) |
| TRAIL STOP | $X | Naikkan SL ke entry |
| EMERGENCY EXIT | $EX | Cut loss — jangan tunggu |

## Signal Logic (LONG ONLY)
1. Fetch latest XAUUSD OHLC data
2. Calculate EMA 20, EMA 50
3. Identify current price
4. **BUY SIGNAL:** buy zone = nearest strong support ± $10
5. SL = below buy zone by $15-25 (tight)
6. Targets = next 2 resistance levels
7. Calculate R:R — if < 1:2, say NO TRADE
8. **EXIT LEVELS:** TP1 = nearest resistance (jual 50%), TP2 = next resistance (jual semua)
9. Trail stop = move SL to entry after TP1 hit
10. Check calendar events (CPI, NFP, FOMC)
11. Generate chart + PDF
12. HARAM: never generate SHORT signal as primary. Only mention short if price breaks major support.

## End-to-End Workflow (proven 2026-07-14 pilot)

### Step 1: Gather Data (3 parallel web searches)
```
web_search("XAUUSD gold price today [DATE]")
web_search("gold news today [MONTH] [YEAR] economic events")
web_search("XAUUSD technical analysis support resistance [MONTH] [YEAR]")
```
Then `web_extract()` the best technical analysis page (DailyForex, Vantage, FXStreet) for concrete levels.

**Key data to extract:**
- Current/open/high/low/close price
- Support levels (S1, S2, S3)
- Resistance levels (R1, R2, R3)
- RSI reading
- EMA position (price above/below)
- Calendar events (CPI, NFP, FOMC, Fed speak)

### Step 2: Set Signal Levels
Use extracted support/resistance as zone boundaries — NOT formulaic offsets.
Buy zone = nearest strong support cluster (±$10).
Sell zone = nearest strong resistance cluster (±$15).
SL = below/above the zone by $15-25 (tight, not wide).
Targets = next resistance (for buys) or next support (for sells).

### Step 3: Generate Chart
Write chart Python to `/tmp/build_gold_signal.py`, run via `terminal()`.
**IMPORTANT:** Use `write_file()` + `terminal()`, NOT `execute_code()`.
Matplotlib/reportlab are installed in the system Python but execute_code runs in a sandbox that may not have them.

### Step 4: Generate PDF
Write PDF Python to `/tmp/build_gold_pdf.py`, run via `terminal()`.
Uses `reportlab` — same pattern: `write_file()` + `terminal()`.
**CRITICAL:** Copy ALL signal-level variables (`BUY_ZONE_LOW`, `BUY_ZONE_HIGH`, `SL`, `T1`, `T2`, `ENTRY_MID`) into the PDF script header. The PDF runs in a separate process — it does NOT inherit variables from the chart script. Use f-strings in the data tables so values update automatically when variables change.

### Step 5: Deliver
Send chart as photo + PDF as document to the user.
Include strategy table in message text for quick reading.

## Support Files

- `references/gold-api-extension-pattern.md` — how to add new endpoints to gold-api (THE way to add trading features)
- `references/red-news-impact.md` — CPI/NFP/FOMC impact on gold: move sizes, 15-minute rule, Syed briefing text
- `references/gold-data-apis.md` — API endpoints and pricing data sources
- `references/proven-data-pipeline.md` — proven web-scraping pipeline (no API key needed), pitfalls, source quality ranking
- `references/ohlc-estimation-method.md` — how to estimate daily OHLC from web search when Twelve Data is unavailable (proven 2026-07-15)
- `templates/gold_signal_chart.py` — OANDA dark candlestick chart (matplotlib, proven 2026-07-14)
- `templates/gold_signal_pdf.py` — one-page PDF with strategy table (reportlab, proven 2026-07-14)
## Live Web Chart (Alternative to PDF)

For interactive live charts, deploy TradingView lightweight-charts web app:
- **URL:** https://arif-fazil.com/wealth/gold
- **Backend:** Node.js API on port 3456, systemd service `gold-api`
- **Frontend:** `/var/www/html/gold/index.html`
- **Features:** H1/H4/D1 candlestick, EMA 20/50, S/R levels, signal overlay, auto-refresh 60s
- **Pattern:** `trading-signal-chart` skill → `references/tradingview-lightweight-charts-webapp.md`

Use web chart for live monitoring. Use PDF for daily briefings and signal delivery.

### Gold Dashboard Architecture & Troubleshooting
See: `references/gold-dashboard-architecture.md` — full architecture, Caddy routing, trailing-slash bug (fixed 2026-07-17), stale data investigation, zone computation logic, API endpoints, troubleshooting commands, and how to extend gold-api.

## Gold API Integration (2026-07-16)

The gold-api (port 3456) now has endpoints that replace direct yfinance calls:

```bash
# APEX market intelligence (G/C_dark/dS/state/verdict)
curl -sf localhost:3456/api/gold/apex

# Full signal from engine_v2 + position sizing
curl -sf localhost:3456/api/gold/signal_v2

# ForexFactory economic calendar (high-impact USD events)
curl -sf localhost:3456/api/gold/calendar

# Quick ticker (price, change, RSI, EMAs)
curl -sf localhost:3456/api/gold/ticker
```

**When extending gold-api (adding new endpoints):**
1. Add Python command to `/var/www/html/gold/api/fetch_gold.py` (function `cmd_XXX`)
2. Add to CLI choices and handlers dict in `fetch_gold.py`
3. Add endpoint to `/var/www/html/gold/api/server.js` handlers object
4. Add short alias (without `/gold/` prefix) for Caddy strip_prefix compatibility
5. Restart: `systemctl restart gold-api`
6. Test: `curl -sf localhost:3456/api/XXX`

**CRITICAL USER RULE:** Arif forbids creating new servers/repos. Always extend the existing gold-api. Never create a new MCP server, new port, or new service for trading features.

**Command dependencies:** Not all endpoints need the `/root/trading` module. `ticker`, `history`, `signals`, `levels`, `macro`, `calendar` are self-contained. `signal_v2` and `apex` require the `trading` package. If those endpoints return HTTP 500, see `references/gold-api-command-dependencies.md` for the degraded-mode fallback.

**Human-readable labels:** All user-facing text (gold site, Telegram messages to Syed) must use plain language. NO jargon like G, C_dark, dS, APEX, Φ. Use: Clarity, Risk, Trend Energy, Condition, Structure, Strength, Signal, Stability, Agreement, Momentum, Volume. State names: Clear Trend / Ranging / Choppy. Verdicts: Strong Signal / Good to Go / Wait / Hold Off.

## Pitfalls

- **ENGINE SESSION GATE (proven 2026-07-15):** The gold engine `--briefing` has a session filter that blocks output during Asian session (00:00-07:00 UTC). The 8am MYT cron (00:00 UTC) ALWAYS hits this gate. When the engine returns only "SESSION: ASIAN/BLOCKED — Outside trading hours" with no signal data, fall back to the web-search data pipeline (Step 1-2). Do NOT deliver just the session-blocked message — the user needs actual signal levels. The engine computes the signal internally but `format_briefing()` returns early when `session_ok=False`. To bypass for testing, edit `gold_engine.py` line 343-346 to remove the early return, or run during London/NY hours.
- **R:R CONSISTENCY:** Use ONE entry price for ALL R:R calculations (chart + PDF + message). The chart calculates from `entry_mid = (BUY_ZONE_LOW + BUY_ZONE_HIGH) / 2`. The PDF must use the SAME entry midpoint, not a different hardcoded value. If chart says 1:1.6 / 1:2.5, PDF must say the same. Derive PDF values from the chart's entry_mid: `risk = entry_mid - SL`, `reward1 = T1 - entry_mid`, `reward2 = T2 - entry_mid`.
- **VARIABLE PASSAGE (proven 2026-07-16):** Chart and PDF are written as SEPARATE Python scripts (`/tmp/build_gold_signal.py` and `/tmp/build_gold_pdf.py`). They run in separate processes — no shared state. The PDF script MUST independently define ALL signal-level variables: `BUY_ZONE_LOW`, `BUY_ZONE_HIGH`, `SL`, `T1`, `T2`, `ENTRY_MID`. Common mistake: defining `ENTRY_MID`, `SL`, `T1`, `T2` in the PDF script but forgetting `BUY_ZONE_LOW`/`BUY_ZONE_HIGH` (used in the verdict line and zone labels). Fix: copy the full signal-level variable block from the chart script into the PDF script header.
- **S/R LEVEL QUALITY CHECK (proven 2026-07-16):** chart_pro.py's S/R algorithm can return clustered levels (e.g., $4,044, $4,043, $4,042) that are essentially the same price. Always sanity-check the `support[]` and `resistance[]` arrays in the JSON output. If levels are within $5 of each other, treat them as ONE level and supplement with web-search S/R data from Step 1. The engine's S/R detection works best on volatile days with clear swing highs/lows — on quiet/consolidation days, the algorithm clusters.
- NEVER show zones far from current price (temporal intelligence)
- NEVER use green/red based on trend direction — use OHLC actual
- NEVER zoom out to show 3-month range when action is at $4,000
- NEVER put labels inline blocking candles — use Y-axis side
- NEVER use broker jargon — rakyat marhaen language
- NEVER use `execute_code()` for matplotlib/reportlab — use `write_file()` + `terminal()` (packages are in system Python, not in sandbox)
- ALWAYS check if market is open before saying "live price"
- ALWAYS verify day of week before saying "market closed"
- ALWAYS include event warnings (CPI, NFP, FOMC) on chart AND in message
- ALWAYS verify Twelve Data / source prices against TradingEconomics spot before publishing
- When RSI < 35, label "near oversold" — supports buy bias
- When price is below both EMA 20 and 50, note "bearish trend" but check for reversal signals (doji, hammer)
- **CRON VENV PATH (proven 2026-07-16):** All cron-triggered Python scripts MUST use `/root/venv/bin/python3`, not bare `python3`. The shell wrapper in cron context tries to source arifOS auto-venv functions that don't exist, causing `command not found`. Affects: `price_alert.py`, `gold_engine.py`, `chart_pro.py`, any script run via `terminal()` in cron jobs.
- If event day (CPI/FOMC/NFP), add prominent "WAIT FOR DATA" warning — don't suppress the signal, but gate it
- **TradingConfig missing contract_multiplier (proven 2026-07-16):** `position_sizer.py` calls `cfg.contract_multiplier` but `TradingConfig` didn't have this field. Fix: added `contract_multiplier: float = 1.0` to `/root/trading/core/config.py`. If other config attributes fail with `AttributeError`, add them to the dataclass.
- **GOLD-API MISSING TRADING MODULE (proven 2026-07-20):** `cmd_signal_v2` and `cmd_apex` in `fetch_gold.py` import from `trading.*` (lines 420-424, 515-521). If `/root/trading/` doesn't exist on the server, these endpoints return HTTP 500 with `"No module named 'trading'"`. The `cmd_ticker` function is SELF-CONTAINED (only uses yfinance + numpy/pandas directly) and works regardless. **Degraded-mode fallback for cron jobs:** When `curl -sf localhost:3456/api/gold/signal_v2` returns exit code 22 (HTTP error), check `systemctl status gold-api --no-pager -l` for the error. If it's "No module named 'trading'", fall back to ticker-only mode: use `curl -sf localhost:3456/api/gold/ticker` for price/RSI/EMAs/S/R levels, supplement with web search (hound mcp_smart_search + mcp_smart_fetch) for narrative context and concrete levels from FXEmpire/FXStreet. The ticker's built-in `signal` field and S/R arrays are sufficient for the decision gate. Chart/PDF generation still works if `/root/trading` has chart_pro.py — but check existence first with `test -f /root/trading/scripts/chart_pro.py`.

## Gold Signal Engine (Phase 1 Companion — Live)

A Python-based signal engine is live at `/root/trading/scripts/gold_engine.py`. It can replace or supplement the web-search-based signal generation above.

**Use the engine when:** you need fast, consistent, automated signals with proper indicator calculation AND it's during London/NY hours (15:00-05:00 MYT).
**Use the web-search method when:** you need narrative context, news sentiment, the engine data source fails, OR the engine returns session-blocked (which happens at 8am MYT cron — see Pitfalls).

```bash
cd /root/trading && python3 scripts/gold_engine.py --briefing
```

**Engine workflow for cron jobs (8am MYT):** Try engine first. If output is ≤3 lines and contains "ASIAN/BLOCKED", discard it and fall back to the web-search pipeline (Step 1-2 above). Never deliver just the session-blocked message.

Engine features: EMA 20/50, RSI + divergence, candle patterns, S/R levels, DXY/yields macro, session filter (London/NY only), ≥2 confluence rule, journal logging.

Cron job `2258f1b3fa0e` delivers daily at 8am MYT to SADO group.

**Confluence rule (F3 WITNESS):** Single-indicator signal = rejected. Minimum 2 of: EMA crossover, S/R proximity, candle pattern, RSI divergence.

## Voice Note Generation (SADO 8am Daily Briefing — proven 2026-07-18)

Cron job `2258f1b3fa0e` adds a **voice note (BM OsmanNeural, ~90 seconds)** alongside the text + chart briefing for the SADO group. This audio channel reinforces the same signal in three formats (text + chart + voice) — proven pattern from `tts-edge-fallback` and `syedos` skills.

**Voice generation step** (added after Step 5 in the cron prompt):

1. After text message is formatted, populate `/tmp/syed_voice.txt` from the same data:
   - Opening: "Abang Sado, ni update gold [hari ni/pagi ni]. Harga sekarang [spell out] dolar."
   - Cerita: 2-3 sentence summary of what happened
   - Levels: support + resistance, spelled out
   - Trend: EMA200 direction + position relative to current price
   - RSI: number + state (cold/neutral/hot)
   - Verdict: SEAL/SABAR/HOLD/VOID + 1-line sebab
   - Aturan: one specific action
   - Close: "Trade selamat, abang."

2. Numbers — spelled out as BM words. Examples:
   - $4,023 → "empat ribu dua puluh tiga dolar"
   - $67 → "enam puluh tujuh dolar"
   - $4,019.73 → round to "empat ribu dua puluh" for spoken
   - 63.6 → "enam puluh tiga perpuluhan enam"

3. Generate MP3:
   ```bash
   cat > /tmp/syed_voice.txt << 'EOF'
   [populated script]
   EOF
   edge-tts --voice ms-MY-OsmanNeural --rate "+5%" \
     --file /tmp/syed_voice.txt --write-media /tmp/syed_voice.mp3
   ```

4. Deliver: text first → chart → voice note (voice goes last in Telegram). All three to SADO group.

**Voice-only skip rule:** If verdict is SABAR AND state is "Choppy", voice is optional (text suffices — "jangan trade" is the only message). Otherwise, voice is MANDATORY.

**Full template + verdict→action mapping + edge-tts gotchas:** see `references/voice-briefing-format.md` in `syedos` skill.

## Red News Impact Rules (proven 2026-07-16)

Three monster events move gold $50-150 in minutes:

| Event | MYT Time | Avg Gold Move | Direction Rule |
|---|---|---|---|
| CPI | 20:30 monthly | $40-80 (1-2%) | CPI low → Gold up. CPI high → Gold down |
| NFP | 20:30 first Friday | $50-100 (1.2-2.5%) | Jobs few → Gold up. Jobs many → Gold down |
| FOMC | 02:00, 8x/year | $30-80 + $50-100 press | Dovish → Gold up. Hawkish → Gold down |

### The 15-Minute Rule (CRITICAL)
- **T-15 min:** CLOSE all positions, DON'T open new ones
- **T-0:** News released — JUST WATCH
- **T+15 min:** Check direction confirmed
- **T+30 min:** THEN enter trade if trend clear

**Why?** Spread blows out 100-200 pips. Stop hunt. Slippage. First move is always wrong.

### For Syed (BM casual)
"Abang Sado, setiap kali ada red news — CPI, NFP, FOMC — tutup semua position 15 minit sebelum. Tunggu 30 minit lepas news. Baru masuk balik. Lot kurangkan 50%. Spread masa red news boleh makan semua profit micro-lot kau."

Full reference: `references/red-news-impact.md`

## Human-Readable Label Mapping (MANDATORY for user-facing text)

Arif explicitly forbids APEX theory jargon in gold site and Telegram messages to Syed.

| Internal Term | Human Label |
|---|---|
| G score | Clarity |
| C_dark | Risk |
| dS/dt | Trend Energy |
| A | Structure |
| P | Strength |
| E | Signal |
| X | Stability |
| Φ (Phi) | Agreement |
| CLARITY state | Clear Trend |
| STABLE state | Ranging |
| CHAOS state | Choppy |
| BUY direction | Trending Up |
| SELL direction | Trending Down |
| FLAT | No Direction |
| SEAL verdict | Strong Signal |
| PROCEED | Good to Go |
| SABAR | Wait |
| HOLD | Hold Off |

NEVER use G, C_dark, dS, APEX, Φ in user-facing text. Always use the human label.
