---
name: trading-intelligence-system
description: arifOS Trading Intelligence System — agentic signal engine + risk management + governance pipeline for XAUUSD. SCANNER → SIGNAL → RISK → JUDGE → EXECUTE → TRACK → ALERT.
trigger: When user asks about gold trading, XAUUSD signals, trading system, position sizing, backtesting, or risk management.
---

# Trading Intelligence System

## What It Is
An agentic trading system at `/root/trading/` that generates governed trading signals for XAUUSD. Every signal passes through arifOS constitutional floors (F1-F13) before becoming actionable.

## Arif's Core Philosophy (verbatim)
> "There is only 3 pattern for chart. Upwards, downward, sideways. The rule is simple, buy low sell high. Risk/reward."

No complex indicators. No overfitting. Three patterns, zone-based entries, controlled risk. The system embodies this — not the other way around.

## Quick Commands
```bash
cd /root
python -m trading.main alert              # Live signal (real yfinance data)
python -m trading.main scan --json        # Signal as JSON
python -m trading.main status             # Risk state

# Backtest on real data
python /root/trading/backtest/engine_v2.py \
  --data /root/trading/data/xauusd_1h.json \
  --output /root/trading/backtest/results/latest.json \
  --equity 10000 --risk 0.01

# Direct v2 engine
python -c "
from trading.signals.data_feed import fetch_xauusd_yfinance
from trading.signals.engine_v2 import generate_signal_v2
candles = fetch_xauusd_yfinance(period='1mo', interval='1h')
signal = generate_signal_v2(candles)
print(signal.to_alert_text())
"
```

## Modules
- `signals/regime.py` — 3-pattern regime detection (UPTREND/DOWNTREND/SIDEWAYS)
- `signals/engine_v2.py` — signal generation (buy low sell high, trend-only)
- `signals/apex_predictor.py` — APEX G/C_dark/dS market state (CLARITY/CHAOS/STABLE)
- `signals/scanner.py` — EMA, RSI, MACD, ATR, S/R, candle patterns
- `signals/data_feed.py` — yfinance data (GC=F gold futures)
- `risk/position_sizer.py` — Kelly + fixed-risk
- `risk/manager.py` — drawdown protection, daily loss limits
- `governance/gate.py` — arifOS F1-F13 constitutional gate
- `backtest/engine_v2.py` — backtester (corrected P&L, trend-only)
- `ARCHITECTURE.md` — full federation integration doc (GEOX→arifOS→WEALTH→A-FORGE→WELL→AAA→VAULT999)
- `README.md` — system overview

## APEX Integration (market predictor)
The APEX primitives map to market state:
- **A (Authority)** = EMA alignment strength (how cleanly EMA20>50>200 or reverse)
- **P (Physics)** = Price action strength (momentum consistency, body-to-wick, trend persistence)
- **E (Evidence)** = Signal clarity / SNR (net directional move vs total movement)
- **X (Execution)** = Trend stability (ATR consistency — low CV = stable)
- **Φ (Witness)** = Multi-timeframe confirmation (1H/4/1D geometric mean)

**State classification:**
- `G ≥ 0.50 AND C_dark < 0.30` → **CLARITY** (trade the direction)
- `G ≥ 0.30 AND C_dark < 0.30` → **STABLE** (range trade)
- `G < 0.30 OR C_dark ≥ 0.30` → **CHAOS** (don't trade)

**Verdict mapping:**
- G ≥ 0.80 → SEAL (high conviction)
- G ≥ 0.50 → PROCEED
- G ≥ 0.30 → SABAR
- else → HOLD

**Bottleneck in current gold market (Jul 2026): E=0.246** — poor SNR because price is consolidating. G collapses to 0.01. System correctly says HOLD.

## Federation Integration (2026-07-16 — WIRED, updated 2026-07-18)

Trading tools run as three independent Express.js APIs backed by yfinance data. Three cognitive clarity dashboards live at `https://arif-fazil.com/{gold,oil,gas}/` — all consuming their respective API backends through Caddy reverse proxy.

### Asset APIs (all Express.js, live on VPS)

| Asset | Port | yfinance Symbol | Public Path | Dashboard |
|---|---|---|---|---|
| **Gold** (XAUUSD) | :3456 | GC=F | `/wealth/gold/api/*` | `arif-fazil.com/gold/` |
| **Brent Crude** | :3457 | BZ=F | `/wealth/oil/api/*` | `arif-fazil.com/oil/` |
| **Natural Gas** | :3458 | NG=F | `/wealth/gas/api/*` | `arif-fazil.com/gas/` |

All three APIs share identical endpoint structure (`/api/ticker`, `/api/signal_v2`, `/api/apex`, `/api/macro`, `/api/levels`, `/api/calendar`, `/api/history`).

**Bridge module:** `/root/arifOS/arifosmcp/runtime/trading_bridge.py`
**Observatory:** `("trading", "TRADING :3456", "127.0.0.1", 3456)` in observatory routes

### Public Web Endpoints (Caddy-proxied)

Caddy strips `/wealth/{gold,oil,gas}` prefix and proxies to respective port:
```
https://arif-fazil.com/wealth/gold/api/ticker  →  localhost:3456/api/ticker
https://arif-fazil.com/wealth/oil/api/ticker   →  localhost:3457/api/ticker
https://arif-fazil.com/wealth/gas/api/ticker   →  localhost:3458/api/ticker
```

| Tool | Internal endpoint | Public web path | What it does |
|---|---|---|---|
| `trade_signal` | `/api/{asset}/signal_v2` | `/wealth/{asset}/api/signal_v2` | Full signal: regime + confluence + entry/SL/TP + verdict |
| `apex_evaluate` | `/api/{asset}/apex` | `/wealth/{asset}/api/apex` | G score, C_dark, clarity/risk/trend/condition |
| `trade_scan` | `/api/{asset}/ticker` | `/wealth/{asset}/api/ticker` | Price, RSI, EMA20/50/200, emaTrend, S/R levels (1H) |
| `trade_calendar` | `/api/{asset}/calendar` | `/wealth/{asset}/api/calendar` | ForexFactory high-impact USD events |
| `trade_macro` | `/api/{asset}/macro` | `/wealth/{asset}/api/macro` | DXY, US10Y, VIX, silver, GSR |
| `trade_levels` | `/api/{asset}/levels` | `/wealth/{asset}/api/levels` | S/R 1H + Daily pivot levels |
| `trade_history` | `/api/{asset}/history` | `/wealth/{asset}/api/history` | OHLCV for TradingView chart |

### Live Dashboard Architecture

- **Files:** `/var/www/html/{gold,oil,gas}/index.html` (single-file HTML, no build step)
- **Template:** Gold is canonical; oil & gas derived via sed substitution (4 lines: API_BASE, asset name, yfinance symbol, labels)
- **Caddy redirects:** `/gold`, `/oil`, `/gas` → `/gold/`, `/oil/`, `/gas/` (Caddy `handle /gold/*` doesn't match `/gold` without slash)

### Dashboard Rules (NON-NEGOTIABLE — Arif: "kalau abang sado tengok chart salah, rugi sapa nak tanggung?")

1. **STALE DATA = HARAM.** Every number from live API. HTML defaults use `—` or `Loading...`. Never hardcoded prices/dates.
2. **Boot sequence: TICKER FIRST, CHART SECOND.** `refreshTicker()` + `refreshMacro()` with `await Promise.all()` before heavy `renderChart()` loads async.
3. **Timeframe labels mandatory.** `1H` label on S/R levels, `TF: 1H levels, 4H regime` in driver text.
4. **Timestamp = ● LIVE.** Green dot + current MYT time, never a stale date.
5. **Technical Forge = API-driven.** Trend/Momentum/Structure/Volume cards populated by `refreshTechnicalForge()` from ticker + signal_v2 + apex.
6. **SABAR > fake BUY.** Confluence 0% + DOWNTREND → show SABAR/HOLD. Not a fake signal. This is the competitive moat.

### Plain-Language Translation Layer

Constitutional floor language (F1, F2, F7) is internal. The dashboard's synthesis uses `translateJudge()` to convert to human-readable BM:

```
BEFORE: "F1: No stop loss — irreversible risk; F2: No confluence factors..."
AFTER:  "Market belum jelas. Tunggu trend + isyarat aligned sebelum masuk."
```

Strips F-floor refs, replaces jargon (insufficient reward → potensi untung tak berbaloi), produces conversational BM for non-traders. See `references/plain-language-translator.md`.

### ⚠️ CRITICAL GAPS (2026-07-18 audit)

| Gap | Impact |
|---|---|
| **Gold engine has NO GIT REPO** | `/root/trading/` is scripts on VPS. If VPS dies, all signal code lost. Must create `github.com/ariffazil/trading-intel` |
| **arif_judge NOT wired to signals** | Signals computed but not constitutionally governed. No F1-F13 enforcement pipeline |
| **VAULT999 NOT recording trades** | No immutable audit trail. Can't prove signal history to clients/regulators |
| **No API auth / paywall** | Endpoints are open. No API keys, no rate limiting. Can't monetize |
| **Oil & gas backtests not done** | Only gold has 2yr backtest. Oil/gas are live but unverified |

**Still NOT wired:**
- MT5 execution (needs 888_HOLD — real money)
- WELL readiness check before signal delivery
- Governed Signal API product packaging (docs, OpenAPI spec, client SDK)

## Reference Files
- `references/backtest-methodology.md` — backtest setup, corrected multiplier, pitfall log
- `references/gold-session-volatility.md` — 2yr volatility analysis by MYT hour, news impact hierarchy, Syed trading rules
- `references/plain-language-translator.md` — `translateJudge()` pattern for converting arifOS F-floor language to human-readable BM on public dashboards

## Cron Integration
The existing `XAUUSD Price Alert` cron job (adbe4006fba5) sends price updates. The new system replaces it with: scan → APEX state → regime → signal → risk → judge → alert. When wiring, use `python -m trading.main alert` as the cron command.

## Optimized Strategy (backtested on 2yr real gold data)
```
Config: 1% risk, 2× ATR SL, 2× ATR trailing stop, RR ≥ 1:2
Skip SIDEWAYS regime entirely
294 trades | 45.9% win rate | PF 1.19 | Sharpe 0.98
$10k → $12,347 (23.5% over 2yr, ~11.7% annualized)
Max drawdown: 16.8%
UPTREND: +$1,567 | DOWNTREND: +$780 | SIDEWAYS: skipped
```

## Signal Logic
1. **Regime**: EMA20/50/200 alignment → UPTREND / DOWNTREND / SIDEWAYS
2. **Skip SIDEWAYS** — biggest edge. Don't trade chop zones.
3. **Zones**: Swing point clustering → support/resistance (strength = test count)
4. **Proximity**: Price within 1.5× ATR of zone
5. **Confirmation**: Bullish/bearish candle or rejection wick
6. **Sizing**: 1% risk per trade, quarter-Kelly
7. **Stops**: SL = 2× ATR from zone (not 1× — too tight)
8. **Trailing**: After 1R profit, trail with 2× ATR stop
9. **Judge**: F1-F13 constitutional floor via arifOS

## Risk Rules
| Rule | Value | Why |
|------|-------|-----|
| Risk/trade | 1% | 2% destroys account (-359% in backtest) |
| Daily loss | 3% | Circuit breaker |
| Max DD | 10% | Capital preservation |
| Min RR | 1:2 | Winners must be ≥ 2× losers |
| SL | 2× ATR | 1× ATR too tight (noise stops you out) |
| Trail | 2× ATR | Lets winners run (biggest profit source) |
| Max positions | 2-3 | Concentration risk control |
| SIDEWAYS | SKIP | 40.8% win rate, net negative |

## Pitfalls (CRITICAL — read before modifying)

### Gold P&L Multiplier
**XAUUSD futures: multiplier = 1000, NOT 100.**
- 1 standard lot = 100 troy oz
- $1 price move = $100 per lot
- Point-based: `pnl = (exit - entry) * lots * 1000`
- Lot sizing: `lots = risk_amount / (sl_distance * 1000)`
- Using 100 instead of 1000 makes lot sizes 10× too large → account blowup
- This bug caused -62% return in initial backtest. Fixed version: +23.5%.

### RSI Filters Are Too Strict in Trends
- In UPTREND, RSI avg = 58. Only 1.9% of bars have RSI < 35
- In DOWNTREND, RSI avg = 44. Only 2.6% of bars have RSI > 65
- Using RSI 35/65 as entry filter → almost zero trades
- **Fix**: Don't use RSI as entry gate in trending markets. Price-at-zone + confirmation is sufficient.

### yfinance Data Limits
- `GC=F` = gold futures, not spot. Prices may differ from MT5 by $2-5
- Hourly data: max ~2 years (yfinance/Yahoo API hard limit)
- Daily data: 25+ years available (period='max')
- 4h data: resampled from 1h by fetch script
- Data files: `/root/trading/data/xauusd_{1h,4h,1d}.json`
- Re-fetch: `python /root/trading/data/fetch_xauusd.py`

### Backtest Gotchas
- Warmup 210 bars minimum (EMA200 needs 200 bars + buffer)
- Don't trust first backtest run — always verify P&L math manually
- `max(0.01, lots)` minimum lot may exceed 1% risk on wide stops — use `max(0.001, lots)` for backtest
- Profit factor and Sharpe are more reliable than total return for strategy comparison
- Always backtest on REAL data, not synthetic (agent-generated sample data skews results)

### Syed Constraints
- Max lot: 0.10 (cap in config)
- Balance estimate: ~$500
- Confuses long/short directions — keep alerts unambiguous
- Voice alerts: ms-MY-OsmanNeural
- Prefers simple BM explanations
