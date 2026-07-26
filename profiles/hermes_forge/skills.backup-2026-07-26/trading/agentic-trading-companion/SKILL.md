---
name: agentic-trading-companion
description: "Build an AI trading companion system — signal engine, price alerts, journal tracking, chart generation, and web terminal. NOT auto-execution. Phase 1: AI proposes, human decides. Proven: 2026-07-14 XAUUSD gold trading system for Abang Sado Udin."
triggers:
  - "trading agent"
  - "trading companion"
  - "build trading system"
  - "gold signal"
  - "XAUUSD signal"
  - "trading journal"
  - "trading chart"
  - "agentic trading"
  - "AI trading"
  - "backtester"
  - "backtest"
  - "trading backtest"
tags:
  - trading
  - xauusd
  - gold
  - agentic
  - signals
  - journal
---

# Agentic Trading Companion

## When to Use

When building an AI-assisted trading system for a human trader. NOT for building an autonomous trading bot (Phase 2+). This is Phase 1: AI proposes signals, human decides and executes.

## Constitutional Anchors

- **F10 ONTOLOGY**: Agent proposes, human decides. AI never executes trades.
- **F1 AMANAH**: Reversibility first. Human in control at all times.
- **F7 HUMILITY**: AI hasn't proven itself. No autonomous access.
- **F3 WITNESS**: ≥2 confluence indicators required. Single-indicator signal = breach.

## Architecture (5 Components)

```
┌─────────────────────────────────────────────┐
│  1. SIGNAL ENGINE  — EMA/RSI/S/R/Candle     │
│  2. PRICE ALERT    — Monitor + notify        │
│  3. JOURNAL        — Track + stats + report  │
│  4. CHART PDF      — Visual signal delivery  │
│  5. WEB TERMINAL   — Live TradingView-style  │
└─────────────────────────────────────────────┘
     ↓ signals delivered via ↓
  Telegram cron (daily briefing + alerts)
  Web app (live chart + data)
  PDF (morning briefing chart)
```

## Component 1: Signal Engine

Core Python script that:
1. Fetches OHLCV data (yfinance or broker API)
2. Calculates EMA 20/50, RSI(14), S/R pivots, candlestick patterns
3. Checks confluence (≥2 indicators required)
4. Validates session filter (London/NY only for gold)
5. Checks news calendar (skip NFP/CPI/FOMC windows)
6. Outputs signal with entry/SL/TP/RR/confidence

**Output format:**
```json
{
  "signal": "LONG/SHORT/NO_SIGNAL",
  "confidence": 0.75,
  "entry": 4082.40,
  "sl": 4107.81,
  "tp": 4031.58,
  "rr_ratio": 2.0,
  "confluence_count": 3,
  "confluence_signals": ["EMA_BEARISH", "RSI_BEAR_DIV", "RSI_OVERBOUGHT"],
  "reasons": ["EMA20 < EMA50", "RSI bearish divergence", "RSI 83.6 overbought"]
}
```

**Key rules:**
- Confidence cap at 0.90 (F7 HUMILITY)
- Single-indicator = reject (F3 WITNESS)
- "No signal" is a valid and important output
- Session filter: Asian session = low volume, false signals → blocked

→ See `references/xauusd-signal-spec.md` for full trading spec

## Component 2: Price Alert Monitor

Script that checks every 30 min during trading sessions:
- Price near S/R levels (within 0.3%)
- Fresh EMA crossover
- RSI crossed 30 or 70
- Candlestick pattern formed

**Critical:** Empty output = nothing notable = SILENT. Only deliver non-empty alerts. This is the watchdog pattern.

**Cron setup (no_agent: true):**
The `script` field is a FILE PATH in `~/.hermes/scripts/`, NOT a shell command. Create a wrapper:

```bash
# ~/.hermes/scripts/price-alert.sh
#!/bin/bash
cd /root/trading && python3 scripts/price_alert.py --check 2>/dev/null
```

Then set `script: "price-alert.sh"` in the cron job. Schedule: `30 8 * * *` (8:30am daily).

**Delivery:** SADO group (`telegram:-1003753855708`). For Syed DM, his Telegram chat ID is needed — check gateway logs or ask Arif.

## Component 3: Journal Engine

Tracks every signal and outcome:
- `--sync` — import signals from engine output
- `--log --signal_id <id> --outcome win --pnl <amount>` — log outcome
- `--stats` — win rate, avg RR, profit factor, max drawdown
- `--report` — weekly markdown report

**Storage:** JSON at `journal/trade_log.json`

**Weekly report format (Telegram-ready):**
- Total trades, wins, losses, win rate
- Average RR, profit factor
- Best/worst setup type
- Best/worst trading hour
- Recommendations based on data

## Component 4: Chart PDF (Mode D)

Dark-theme OANDA-style candlestick chart:
- H1/H4 timeframe candlesticks
- EMA 20 (cyan) + EMA 50 (orange) overlays
- S/R levels as dashed horizontal lines
- RSI panel below main chart
- Signal overlay (entry/SL/TP lines)
- Landscape A4, mobile-readable

→ See `references/trading-chart-pdf.md` for rendering spec

## Component 5: Web Terminal

TradingView lightweight-charts based web app:
- Live candlestick chart with auto-refresh
- EMA/RSI computed client-side
- S/R level lines + signal overlay
- Dark theme, gold accents, mobile-first
- API backend (Node.js + yfinance Python bridge)
- Deploy behind Caddy reverse proxy

→ See `references/trading-web-terminal.md` for deployment spec

## Cron Schedule (Proven 2026-07-15)

| Job | Schedule | Delivery |
|---|---|---|
| Gold Signal Briefing | 8am MYT Mon-Fri | SADO group |
| Price alert | 8:30am MYT daily | SADO group |
| XAUUSD Daily Gold Signal | 9am MYT Mon-Fri | origin |
| IG Story Gym Quote | 1pm MYT daily | origin |
| Weekly report | Friday 8pm MYT | SADO group |

For Syed personal DM delivery, his Telegram chat ID is needed. All scripts at `/root/trading/scripts/`.

## Chart Generator: chart_pro.py (Proven 2026-07-16)

Professional-grade chart generator at `/root/trading/scripts/chart_pro.py`. Uses matplotlib (NOT Plotly — kaleido too slow for cron).

**Features:**
- Dark theme (#0d1117) matching WEALTH dashboard
- EMA 20 (cyan) + 50 (orange) + 200 (purple dotted) — toggleable
- S/R levels: max 2-3 clean labels, not cluttered
- Signal overlay: entry (gold) / SL (red dashed) / TP (green dashed) + zone shading
- RSI panel with overbought/oversold shading
- Bias pill (BULLISH/BEARISH/NEUTRAL) + confidence %
- Bottom banner: synthesis verdict + "Kau decide, kau execute. F13 Active"
- 180 DPI, mobile-readable, Telegram-ready PNG

**Usage:**
```bash
python3 chart_pro.py --signal SHORT --entry 4055 --sl 4076 --tp 4027
python3 chart_pro.py --json    # Output metadata
python3 chart_pro.py --force   # Auto-detect signal
```

## WEALTH Gold Dashboard (Existing — Maintained 2026-07-18)

Live at `https://arif-fazil.com/gold/` (primary) and `https://arif-fazil.com/wealth/gold/` (legacy). Cognitive clarity dashboard: live price pulse, 1H S/R levels with timeframe label, regime display (📉 DOWNTREND), APEX market state, signal synthesis verdict, TradingView chart. **Use this existing version — don't rebuild.**

### Architecture (end-to-end)
```
gold-api :3456 (Python, yfinance → GC=F)
    ↓ internal REST
Caddy reverse proxy: /wealth/gold/api/* → strip_prefix /wealth/gold → localhost:3456
    ↓ public HTTPS
Browser JS: CONFIG.API_BASE = origin + '/wealth/gold/api'
    ↓ fetch('/ticker'), fetch('/signal_v2'), fetch('/apex'), fetch('/macro'), fetch('/calendar')
Gold Dashboard (/var/www/html/gold/index.html)
```

### API Endpoints (all through Caddy proxy)
| Endpoint | Full path | Returns |
|---|---|---|
| `/ticker` | `/wealth/gold/api/ticker` | Price, change%, EMA20/50/200, emaTrend, RSI, S/R pivot levels (1H) |
| `/signal_v2` | `/wealth/gold/api/signal_v2` | Full signal: direction, entry, SL, TP, RR, confluence, regime, verdict |
| `/apex` | `/wealth/gold/api/apex` | G score, C_dark, clarity/risk/trend/condition |
| `/macro` | `/wealth/gold/api/macro` | DXY, US10Y, VIX, silver, gold/silver ratio |
| `/calendar` | `/wealth/gold/api/calendar` | ForexFactory high-impact USD events |
| `/levels` | `/wealth/gold/api/levels` | Support/resistance 1H + Daily |
| `/history` | `/wealth/gold/api/history?days=30&interval=1h` | OHLCV for TradingView chart |

### Critical Rules — TRUTH AND REALITY Standard (2026-07-18)

Arif's mandate: *"Kalau hang sama ja macam scammer telegram"* — scammers give signals without timeframes or context. The gold dashboard must show LIVE data with clear timeframe labels. Hardcoded fallback values that go stale make us no better than Telegram scammers.

**1. NO hardcoded price/SR/regime values in HTML.** All defaults must be `—` or `Loading...`, replaced by live API fetch. The site previously had `$4,063.40` and `S1 $4,020` hardcoded from Jul 16 — visible as defaults before JS loaded. FIXED 2026-07-18.

**2. Boot sequence: LIVE DATA FIRST, chart second.** Original boot had `await renderChart('4H')` blocking data fetch. Heavy TradingView init delayed live data by seconds. Fix: `await Promise.all([refreshTicker(), refreshMacro()])` FIRST, then `renderChart('4H')` non-blocking. Data visible in <500ms.

**3. Timeframe labels mandatory.** S/R levels show `1H` label. Driver shows `TF: 1H levels, 4H regime`. Timestamp shows `● LIVE` with green dot. No anonymous numbers — every data point has provenance.

**4. Caddy routing: trailing slash fix.** `handle /gold/*` doesn't match `/gold` (no trailing slash). Bare path fell through to SPA catch-all → served homepage instead of gold dashboard. Fix: `redir /gold /gold/ 308` before the handle block. Same for `/oil` and `/gas`.

**5. Regime display in pulse bar.** Bias pill now shows `Bearish · 📉 DOWNTREND` (not just `Bearish`). Regime from `emaTrend` field in ticker API (EMA20/50/200 alignment).

### Files
- Backend: `gold-api.service` (systemd), Python on port 3456, `/root/trading/`
- Frontend: `/var/www/html/gold/index.html` (single-file, no build step)
- Caddy: `/etc/caddy/Caddyfile` — gold routes at `handle /wealth/gold/*` + `handle /gold/*`
- Caddy reload: `sudo systemctl reload caddy` (888_HOLD — affects all HTTPS)

## SADO Alert with Chart Screenshot

`/root/trading/scripts/sado_alert.py` — checks S/R proximity, generates chart + message. Used by cron job to post alerts with chart images to SADO group.

## User Preferences (Proven 2026-07-16)

- **"Guna ni ja kalau dah elok"** — If an existing solution works (e.g., WEALTH dashboard), USE IT. Don't rebuild. User explicitly rejected rebuilding when a polished version already existed.
- **Stay focused on task.** Don't comment on people's activities, locations, or social context. User corrected: "Stop stalking abang sado location. Focus kerja hang."
- **Don't over-engineer charts.** User wants scannable, mobile-first, clean. Less S/R labels > more. One good chart > three mediocre ones.
- **NEVER respond to live location pins.** Hard rule. User said "BANGANG" when agent kept responding to Telegram live location updates in SADO group. Live location pins are GPS updates from someone sharing their location — they trigger every few seconds. Responding floods the group. IGNORE completely. This is not a preference — it's a hard behavioral rule. Memory entry: "SADO group: NEVER reply to live location pins."
- **Voice notes for trader communication.** When the user says "bagi voice note" or "explain kat dia" — generate a Malay voice note using edge-tts (ms-MY-OsmanNeural) and send as audio. Useful for explaining trade setups to traders who prefer listening over reading. Pattern: draft text → edge-tts → .ogg → deliver.
- **Chart zoom mode.** When user says "zoom in" — use `df.tail(36)` instead of `df.tail(72)`. Fewer candles = bigger, clearer. Tradeoff: less context but better detail. Use zoomed for signal confirmation, full for trend analysis.
- **Long vs Short confusion.** When a trader says "long target 3975" but price is at4045 — that's SHORT, not LONG. Explain clearly: Long = buy first, sell higher. Short = sell first, buy lower. TP below current price = SHORT. Don't assume the trader knows the terminology. Explain in simple BM with examples. Use voice note if they prefer listening.

## Component 6: Backtester

Walk-forward backtester at `/root/trading/backtest/engine_v2.py`. Pure Python, no dependencies. Replaced v1 (`engine.py`) after post-mortem (2026-07-16).

**Architecture:** 3-regime detection (uptrend/downtrend/sideways via EMA alignment), S/R zone clustering from swing highs/lows, entry on zone touch + confirmation candle, trailing stop management. **SIDEWAYS regime is SKIPPED** — biggest edge from backtesting.

**Key rules:** 1% risk per trade, max 2-3 positions, minimum 2R RR enforced, 210-bar warmup, 2× ATR SL, 2× ATR trailing stop.

**Proven optimized config (2yr real gold data, 2026-07-16):**
- 294 trades | 45.9% win rate | PF 1.19 | Sharpe 0.98
- $10k → $12,347 (23.5% over 2yr) | Max DD 16.8%
- Trailing stop is the profit engine: 65 TP hits = $11,273
- 2% risk DESTROYS the account (-359%)

→ See `references/backtester-architecture.md` for full architecture
→ See `trading-intelligence-system` skill for full backtest methodology and config comparison table

**P&L CRITICAL (proven 2026-07-16):** XAUUSD futures multiplier = **1000**, NOT 100. Using 100 → lots 10× too large → account blowup. `pnl = (exit - entry) * lots * 1000`. `lots = risk / (sl_distance * 1000)`. This bug caused initial backtest to show -62.5% loss on a strategy that's actually profitable.

## Pitfalls

- **Don't rush to live trading.** Build → backtest → paper trade (2-4 weeks) → review → then live. Track record = credibility.
- **"No signal" is a signal.** Don't force trades. Days without valid setups are normal.
- **Session filter matters.** Asian session gold = choppy, false breakouts. London/NY only.
- **≥2 confluence mandatory.** Single-indicator signals are F3 WITNESS breaches. Don't shortcut.
- **News windows = no trade.** NFP, CPI, FOMC can invalidate any technical setup in seconds.
- **Chart PDF: zoom in.** User rejected charts showing too much range. Show relevant price action only.
- **Chart PDF: big labels.** Mobile-first. Minimum 10pt body, 13pt key levels, 15pt current price.
- **Price alerts: silent when nothing.** Don't spam with "no alerts" messages.
- **Journal: log outcomes honestly.** Unlogged trades = invisible losses = false win rate.
- **Don't auto-execute in Phase 1.** AI proposes, human decides. Build trust first.
- **Backtester: variable naming pitfall.** When destructuring OHLCV bars, pick ONE name for close price (`price` or `close`) and use it consistently. Mixing causes `NameError`. Hit 2026-07-16 — two occurrences in `check_entry_signal()`.
- **Don't put shell commands in cron `script` field.** For `no_agent: true` jobs, `script` is a FILE PATH in `~/.hermes/scripts/`. Create a wrapper `.sh` script instead.
- **MATPLOTLIB DOLLAR SIGN PITFALL (Critical):** `$` in matplotlib text triggers LaTeX math mode and crashes with `ParseException`. Fix: (1) `plt.rcParams.update({'text.usetex': False, 'mathtext.default': 'regular'})` AND (2) replace `$` with `USD` in ALL text passed to `fig.text()`, `ax.text()`, `ax.set_title()`, `ax.annotate()`. The rcParams fix alone is NOT enough — dollar signs in annotation text still break. Always replace `$` → `USD` in matplotlib text strings. Proven 2026-07-16 — sado_alert.py crashed on `fig.text(..., "Near SUPPORT $4065.2")` until both fixes applied.
- **Plotly+kaleido too slow for cron.** Takes 60s+ to render. Use matplotlib instead (3-5s). Proven 2026-07-16.
- **whisper CLI broken (numba/llvmlite).** OpenAI whisper fails with `ImportError: Numba requires at least version 0.47.0 of llvmlite`. Use `faster-whisper` instead: `pip install faster-whisper`, then `from faster_whisper import WhisperModel`. Proven 2026-07-16 for Malay audio transcription.
- **S/R levels: less is more.** User rejected charts with 6+ S/R levels. Max 2-3 per side, labeled cleanly. Clutter kills readability on mobile.
- **XAUUSD P&L multiplier = 1000 (CRITICAL).** Gold futures: 1 lot = 100 oz, $1 move = $100/lot. Multiplier for point-based calc is **1000**, not 100. Using 100 makes lot sizes 10× too large → account blowup. Proven 2026-07-16: initial backtest showed -62.5%, corrected version +23.5%. Always verify P&L math manually on 2-3 trades before trusting backtest results.
- **RSI as entry filter is too strict in trends.** In uptrend, RSI avg=58, only 1.9% of bars below 35. In downtrend, RSI avg=44, only 2.6% above 65. Using RSI 35/65 as entry gate → near-zero trades. Fix: don't use RSI to gate entries in trending markets. Price-at-zone + confirmation candle is sufficient.
- **Always backtest on REAL data.** Synthetic/sample data gives misleading results. yfinance GC=F: hourly max ~2yr, daily 25+yr. Proven 2026-07-16.
- **2% risk per trade is account suicide.** Even with a profitable strategy (PF 1.19), 2% risk caused -359% return and 51% max DD in backtest. Stick to 1%. Kelly fraction 0.25 max.
- **STALE DATA = HARAM (2026-07-18).** Arif: "Kalau hang sama ja macam scammer telegram." Hardcoded HTML fallback values (price, S/R levels, regime) become stale and mislead users. Every visible data point on the gold dashboard must come from the live API. Defaults must be `—` or `Loading...`, never stale numbers. Boot sequence must prioritize live data over heavy chart rendering. Every number must have a timeframe label. Stale data = no different from Telegram scammers who post signals without timeframes or evidence.

## Proven Stack

- **Data:** yfinance (GC=F for gold futures, XAUUSD=X fallback)
- **Indicators:** pandas + numpy (EMA, RSI, S/R pivots, candlestick patterns)
- **Backtester:** Pure Python (no deps) at `/root/trading/backtest/engine.py`
- **Chart PDF:** reportlab + matplotlib (Mode D dark theme)
- **Web charts:** TradingView lightweight-charts v4 (CDN)
- **API:** Python (FastAPI/Flask) on port 3456, proxied by Caddy
- **Deployment:** Caddy reverse proxy + systemd service
- **Delivery:** Telegram (cron + direct)

## Human-Language Translation: `translateJudge()` (2026-07-18)

arifOS constitutional floors (F1–F13) produce verdicts in governance language:
> *"F1: No stop loss — irreversible risk; F2: No confluence factors — no evidence basis; F7: Confidence capped at 0.90..."*

**This is NOT human-readable.** Makcik kedai runcit opens the site, sees "F1: No stop loss", closes tab. Arif: *"Ayat2 tu manusia rakyat biasa boleh faham ka?"*

### The Pattern

```javascript
function translateJudge(reason) {
  if (!reason) return 'Tunggu isyarat lebih jelas sebelum masuk.';
  let txt = reason
    .replace(/F1:[^;]*;?/g, '')
    .replace(/F2:[^;]*;?/g, '')
    .replace(/F7:[^;]*;?/g, '')
    .replace(/F\d+:[^;]*;?/g, '')
    .replace(/RR ratio [\d.]+ < 1\.5[^;]*;?/g, '')
    .replace(/Confluence score [\d.]* too low;?/g, '')
    .replace(/Signal strength NONE[^;]*;?/g, '')
    .replace(/No clear direction[^;]*;?/g, '')
    .replace(/\s+/g, ' ').trim();
  
  if (!txt || txt.length < 10) {
    if (reason.includes('SABAR')) return 'Market belum jelas. Tunggu trend + isyarat aligned sebelum masuk.';
    if (reason.includes('HOLD')) return 'Ada risiko yang perlu diselesaikan dulu. Jangan masuk lagi.';
    return 'Semak syarat entry sebelum buat keputusan.';
  }
  
  txt = txt
    .replace(/insufficient reward/g, 'potensi untung tak berbaloi')
    .replace(/irreversible risk/g, 'risiko tak boleh undur')
    .replace(/no evidence basis/g, 'tiada bukti cukup')
    .replace(/no confluence factors/g, 'isyarat tak sehala')
    .replace(/Confidence capped/g, 'keyakinan terhad')
    .replace(/not enough confluence/g, 'isyarat bercampur');
  
  return txt;
}
```

**Result — before vs after:**

| Sebelum (F-floor) | Selepas (Rakyat) |
|---|---|
| *"F1: No stop loss — irreversible risk; F2: No confluence factors..."* | **"Market belum jelas. Tunggu trend + isyarat aligned sebelum masuk."** |
| *"Apex G-Score: 0.02 — weak — do not enter"* | **"Kualiti isyarat: LEMAH — jangan masuk"** |

**Where to apply:** Every human-facing surface in the federation that displays signal verdicts — gold/oil/gas dashboards, Telegram signals, trading PDFs. Strip F-floor references, translate remaining technical terms to BM, use conversational tone.

### Language Rules for Rakyat Surface

1. **NO F-floor references** (F1, F2, F7, etc.) — internal governance language only
2. **NO Apex G-Score** — say "Kualiti isyarat: BAIK/SEDERHANA/LEMAH"
3. **BM labels for metrics:** "Nisbah Untung/Risiko" not "RR Ratio", "Isyarat sehala" not "Confluence", "Trend" not "Regime"
4. **Conversational, not clinical.** "Market belum jelas. Tunggu dulu." beats "Signal strength NONE — not enough confluence."

## Commodity Dashboard Replication Pattern (2026-07-18)

Gold, oil, and gas dashboards share identical HTML/JS structure — only the API endpoint and commodity name differ. When updating all three:

```bash
# 1. Fix gold first (single source of truth)
# 2. Copy to oil and gas
cp /var/www/html/gold/index.html /var/www/html/oil/index.html
cp /var/www/html/gold/index.html /var/www/html/gas/index.html

# 3. Sed-swap commodity-specific strings for oil
sed -i \
  -e 's|Gold — Cognitive|Brent Crude (Oil) — Cognitive|g' \
  -e 's|/wealth/gold/api|/wealth/oil/api|g' \
  -e "s|ASSET: 'gold'|ASSET: 'oil'|g" \
  -e 's|XAUUSD|Brent Crude|g' -e 's|XAU/USD|BRENT/USD|g' \
  -e 's|Gold price pulse|Brent Crude price pulse|g' \
  -e 's|XAU/MYR|BRENT/MYR|g' \
  -e 's|yfinance:GC=F|yfinance:BZ=F|g' \
  /var/www/html/oil/index.html

# 4. Sed-swap for gas
sed -i \
  -e 's|Gold — Cognitive|Natural Gas — Cognitive|g' \
  -e 's|/wealth/gold/api|/wealth/gas/api|g' \
  -e "s|ASSET: 'gold'|ASSET: 'gas'|g" \
  -e 's|XAUUSD|Natural Gas|g' -e 's|XAU/USD|NATGAS/USD|g' \
  -e 's|Gold price pulse|Natural Gas price pulse|g' \
  -e 's|XAU/MYR|NATGAS/MYR|g' \
  -e 's|yfinance:GC=F|yfinance:NG=F|g' \
  /var/www/html/gas/index.html
```

**API ports:** gold :3456, oil :3457, gas :3458. All have identical endpoint structures. Caddy proxies `/wealth/{gold,oil,gas}/api/*` → `localhost:{3456,3457,3458}`.

**Caddy trailing-slash fix:** `handle /gold/*` doesn't match `/gold` (no trailing slash). Bare paths fall through to SPA catch-all → serve wrong page. Fix: `redir /gold /gold/ 308` before handle block. Same for oil and gas.

## SABAR Discipline — Constitutional Mandate (2026-07-18)

Arif, when told the engine could lower confluence thresholds to produce more signals: **"SABAR JA LA... Thats why abang sado tu sado."**

**Meaning:** The engine's strictness is a FEATURE, not a bug. When the engine says SABAR with 0% confluence, it's protecting the trader from bad entries. Abang Sado is SADO precisely because he waits — he doesn't force trades.

| Approach | Result |
|---|---|
| Lower thresholds to 1 confluence | More signals, lower quality, scammers do this |
| Keep ≥2 confluence mandatory | Fewer signals, higher quality, Sado does this |

**Never suggest lowering signal thresholds to "fix" the lack of signals.** No signal is a valid and important output. The dashboard showing "SABAR — 0% confluence" is HONEST. A dashboard forcing "BUY" every day is what scammers do. Arif: *"Kalau hang sama ja macam scammer telegram."*

## APEX Market Prediction (v3 addition — 2026-07-16)

New module at `signals/apex_predictor.py` applies APEX theory to market state classification:
- G = A · P · E · X · Φ (Authority, Physics, Evidence, Execution, Witness)
- C_dark = A · (1-P) · (1-X) (shadow score)
- States: CLARITY (G≥0.50, trade), STABLE (G≥0.30, range trade), CHAOS (G<0.30, don't trade)
- Volume analysis integrated: rising/falling volume + price confirmation
- Multi-timeframe witness: 1H/4H/1D geometric mean

Full details in `trading-intelligence-system` skill. The APEX predictor adds a governance layer on top of the existing signal engine — signals only fire when market state is CLARITY, not CHAOS.

## Related Skills

- `daily-trading-signal-briefing` — existing skill for daily gold signal format
- `trading-signal-chart` — candlestick chart rendering templates
- `scientific-pdf-generation` — Mode D trading signal PDF spec
- `trading-intelligence-system` — APEX predictor, backtest methodology, federation integration
