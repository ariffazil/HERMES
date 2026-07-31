---
name: agentic-trading-companion
description: "Build an AI trading companion system — signal engine, price alerts, journal tracking, chart generation, and web terminal. **ACTIVE NODE — carries MT5 bridge, governance pipeline, APEX integration. Every trade execution requires 888 approval.**"
version: 2.0.0
author: Hermes Agent (consolidated from trading-intelligence-system)
tags: [trading, xauusd, gold, agentic, signals, journal, active, governance]
organ: WEALTH (:18082)
f1-boundary: "IRREVERSIBLE ACTION GATE — only skill with MT5 access. Trade execution REQUIRES 888_SOVEREIGN approval. No auto-fire."
zen-organs: [W EXECUTION, ΔG GOVERNANCE, Ω WITNESS, ∂M/∂t MEMORY, ∇F MEANING]
aaa-contract: "A2A_TRADING_CONTRACT — registered at /root/AAA/agents/agentic-trading-companion/agent-card.json"
triggers:
  - "trading agent"
  - "trading companion"
  - "build trading system"
  - "gold signal"
  - "XAUUSD signal"
  - "agentic trading"
  - "backtest"
  - "position sizing"
  - "risk management"
  - "execute trade"
---

# Agentic Trading Companion — ACTIVE NODE

**F1 BOUNDARY: IRREVERSIBLE ACTION GATE.** This is the ONLY skill with MT5 bridge access. Every trade execution MUST carry 888_SOVEREIGN approval before firing to broker. No auto-fire, no autonomous execution without human key.

**ABSORBED:** trading-intelligence-system (APEX predictor, backtester, governed engine, federation wiring)

---

## Constitutional Anchors

- **F13 SOVEREIGN**: Every trade requires human approval. Signal delivered → "Approve?" → "Ok/Skip/SL tighter" → fire.
- **F10 ONTOLOGY**: Agent proposes, human decides. AI never executes autonomously.
- **F1 AMANAH**: Reversibility first. Human in control at all times.
- **F3 WITNESS**: ≥2 confluence indicators required. Single-indicator = breach.
- **F7 HUMILITY**: Confidence capped at 0.90.

---

## Arif's Core Philosophy (verbatim)

> "There is only 3 pattern for chart. Upwards, downward, sideways. The rule is simple, buy low sell high. Risk/reward."

Three patterns, zone-based entries, controlled risk. The system embodies this.

---

## Communication Mandate — PERCENTAGE FIRST (Jul 2026)

**Arif/Syed prefer percentage, not pips.** When communicating trading results, signals, or P&L:

| ❌ WRONG | ✅ RIGHT |
|----------|----------|
| "+7.1 pips" | "+0.018%" |
| "Risk 20 pips" | "Risk 0.49%" |
| "SL 50 pips away" | "SL 1.23% away" |
| "TP 100 pips" | "TP 2.47%, R:R 1:2" |

**Formula:** `(Current − Entry) ÷ Entry × 100 = %`

**Why percentage:**
- Cross-asset comparison (XAUUSD % = EURUSD % = BTCUSD %)
- No broker decimal confusion (Syed's broker has non-standard pip counting)
- No mental conversion overhead — 1% is 1% everywhere
- Direct risk sizing: "2% risk" means the same thing regardless of pair

**Exception:** Institutional traders/brokers still use pip as lingua franca. But Arif and Syed get percentage by default.

**User feedback (Jul 2026):** "Weh apasal x pakai percentage ja?? Pip ni menyusahkan laaa" — Arif. Default all human-facing output to %. Pip format only when explicitly requested or when talking to broker/institutional context.

---

## Human Cognitive Defense — Abang Sado Trading Psychology (Jul 2026)

**Root diagnosis:** Pip is a broker-designed abstraction that creates emotional distance from real money. "Rugi 100 pips" sounds like a game. "Rugi RM2,400" is real pain — and pain is information the brain needs.

### Sleep Gate (G7 — MANDATORY)

Syed has documented brain fog when sleep-deprived (ISFJ, Chaos & Pain Hypnos sleep aid). Trading while sleep-impaired = guaranteed loss.

| Sleep Hours | Trading Allowed? | Rationale |
|-------------|:----------------:|-----------|
| 7+ hours | ✅ Full access | Cognitive capacity online |
| 5-6 hours | ⚠️ Demo only | Impaired judgment |
| < 5 hours | ❌ MT5 LOCKED | Brain fog — "bila dia kata x ingat, dia memang x ingat" |

### Pre-Entry Checklist (G8)

Before ANY trade, Syed MUST answer:

```
□ Aku tidur cukup malam tadi? (Ya / Tak)
  → Kalau Tak: TUTUP MT5. Balik tidur.

□ Stop loss berapa RM aku sanggup rugi?
  → RM_______

□ Take profit berapa RM aku target?
  → RM_______

□ R:R ratio > 1:2? (Ya / Tak)
  → Kalau Tak: JANGAN ENTRY.

□ Aku tengah stress/marah/sedih? (Ya / Tak)
  → Kalau Ya: JANGAN ENTRY.
```

One checklist = one gate. Must pass ALL. Fail one = close app.

### Translation Layer — RM/%, Not Pips

Syed keeps trading in pips on MT5 (that's what his broker shows). Don't force him to change. Instead, translate:

```
═══════════════════════════════════════
  CAPITAL: RM________
  RISK PER TRADE: ____%  (max 2%)
  MAX LOSS: RM________
═══════════════════════════════════════

ENTRY: $________
STOP LOSS: $________
RISK IN $: $________

POSITION = MAX LOSS RM ÷ RISK IN $
═══════════════════════════════════════
```

He fills in RM values. Position size auto-calculated. No pip math required.

### Breathing Reset Protocol (G9 — Cognitive Off-Ramp)

When Syed is anxious (floating P/L, post-SL, or impulse-entry risk), deploy breathing techniques. Full reference at `references/abang-sado-breathing-techniques.md`.

Quick reference:
- **Box Breathing** (4-4-4-4) → floating P/L anxiety
- **Physiological Sigh** (double inhale + long exhale) → post-SL tilt risk
- **Pre-Entry Breath Check** (10s inhale + exhale) → last gate before BUY/SELL
- **4-7-8 Breathing** → sleep prep (with Hypnos)

**Golden rule:** "Nafas adalah steering wheel untuk emosi." Breathe first, then act.

### Broker Audit (One-Time)

Syed's broker has non-standard pip decimal places. One session to audit:
1. Open 0.01 lot trade
2. Watch floating P/L live
3. Calculate: movement $X → profit RM Y
4. Derive actual pip value
5. Save in reference table

Do this ONCE. Never ask "what broker decimal standard?" again.

---

## Quick Commands

```bash
cd /root
python -m trading.main alert              # Live signal (real yfinance data)
python -m trading.main scan --json        # Signal as JSON
python -m trading.main status             # Risk state

# Backtest
python /root/trading/backtest/engine_v2.py \
  --data /root/trading/data/xauusd_1h.json \
  --equity 10000 --risk 0.01

# Governed engine (paper trading)
python3 /root/paper_trading/governed_engine.py scan
```

---

## Architecture (6 Components)

```
┌─────────────────────────────────────────────────┐
│ 1. SIGNAL ENGINE   — EMA/RSI/S/R/Candle/Regime  │
│ 2. PRICE ALERT     — Monitor + notify            │
│ 3. JOURNAL         — Track + stats + VAULT999    │
│ 4. CHART PDF       — Visual signal delivery      │
│ 5. WEB TERMINAL    — Live TradingView-style      │
│ 6. GOVERNED ENGINE — Autonomous paper trading    │
└─────────────────────────────────────────────────┘
     ↓ signals governed via ↓
  arifOS F1-F13 constitutional gate
  WELL readiness check
  VAULT999 seal on every trade
```

### Component 1: Signal Engine

Python at `/root/trading/signals/engine_v2.py`:
1. Fetches OHLCV (yfinance GC=F gold futures)
2. Detects regime (UPTREND/DOWNTREND/SIDEWAYS via EMA20/50/200 alignment)
3. Calculates EMA, RSI, S/R pivots, candle patterns
4. Checks confluence (≥2 indicators mandatory)
5. Session filter (London/NY only)
6. News calendar check (skip NFP/CPI/FOMC windows)
7. Outputs: direction, entry zone, SL, TP, RR, confidence

**Signal Logic:**
1. Regime: EMA20/50/200 alignment → UPTREND / DOWNTREND / SIDEWAYS
2. **Skip SIDEWAYS** — biggest edge. Don't trade chop zones (40.8% WR, net negative)
3. Zones: Swing point clustering → support/resistance (strength = test count)
4. Proximity: Price within 1.5× ATR of zone
5. Confirmation: Bullish/bearish candle or rejection wick
6. Sizing: 1% risk per trade, quarter-Kelly
7. Stops: SL = 2× ATR from zone (not 1× — too tight)
8. Trailing: After 1R profit, trail with 2× ATR stop
9. Judge: F1-F13 constitutional floor via arifOS

```json
{
  "signal": "LONG/SHORT/NO_SIGNAL",
  "confidence": 0.75,
  "entry": 4082.40,
  "sl": 4107.81,
  "tp": 4031.58,
  "rr_ratio": 2.0,
  "confluence_count": 3,
  "regime": "DOWNTREND"
}
```

### Component 2: Price Alert Monitor

Script checks every 30 min during sessions:
- Price near S/R levels (within 0.3%)
- Fresh EMA crossover
- RSI crossed 30 or 70
- Candlestick pattern formed

**Critical:** Empty output = NOTHING = SILENT. Watchdog pattern.

### Component 3: Journal Engine

Tracks every signal and outcome. JSON at `journal/trade_log.json`.
- `--sync` — import signals from engine
- `--log --signal_id <id> --outcome win --pnl <amount>` — log outcome
- `--stats` — win rate, avg RR, profit factor, max drawdown
- `--report` — weekly markdown report

**NEEDS:** VAULT999 seal integration (CRITICAL GAP — see below).

### Component 4: Chart PDF

See `trading-signal-chart` skill (PASSIVE NODE). This component delegates chart generation to the passive node.

### Component 5: Web Terminal

TradingView lightweight-charts at `https://arif-fazil.com/gold/`.
Three dashboards: Gold (:3456), Brent Oil (:3457), Natural Gas (:3458).

**Dashboard Rules (NON-NEGOTIABLE):**
1. STALE DATA = HARAM. Every number from live API. Defaults `—` or `Loading...`.
2. Boot: TICKER FIRST, CHART SECOND. `await Promise.all([refreshTicker(), refreshMacro()])`.
3. Timeframe labels mandatory on every data point.
4. Timestamp = ● LIVE with green dot.
5. SABAR > fake BUY. Show HOLD when confluence 0%.

### Component 6: Governed Autonomous Paper Trading Engine

**File:** `/root/paper_trading/governed_engine.py` — autonomous with 6 constitutional gates:

| Gate | Rule | Blocks |
|------|------|--------|
| G1: APEX State | CHAOS → HALT | No trades in chaos |
| G2: Cross-Asset | Brent crash >5% → HALT commodities | Contagion protection |
| G3: Confluence | <2 signals → SKIP | Single-trigger entries |
| G4: Loss Cap | Daily >3% DD → CIRCUIT BREAKER | Blowout prevention |
| G5: Cooling | <4H since last SL → WAIT | Revenge trading block |
| G6: Session | Asian = range only | Timezone discipline |

---

## APEX Market State Integration

The APEX primitives map to market state:

- **A (Authority)** = EMA alignment strength (cleanly EMA20>50>200 or reverse)
- **P (Physics)** = Price action strength (momentum consistency, body-to-wick)
- **E (Evidence)** = Signal clarity / SNR (net directional move vs total)
- **X (Execution)** = Trend stability (ATR consistency)
- **Φ (Witness)** = Multi-timeframe confirmation (1H/4H/1D geometric mean)

| State | Formula | Action |
|---|---|---|
| CLARITY | G ≥ 0.50 AND C_dark < 0.30 | Trade direction |
| STABLE | G ≥ 0.30 AND C_dark < 0.30 | Range trade |
| CHAOS | G < 0.30 OR C_dark ≥ 0.30 | DON'T TRADE |

**Current bottleneck (Jul 2026):** E=0.246 (poor SNR during consolidation). G collapses to 0.01. System correctly says HOLD.

---

## Optimized Strategy (backtested on 2yr real gold data)

```yaml
Config: 1% risk, 2× ATR SL, 2× ATR trailing stop, RR ≥ 1:2
Skip SIDEWAYS regime entirely
294 trades | 45.9% win rate | PF 1.19 | Sharpe 0.98
$10k → $12,347 (23.5% over 2yr, ~11.7% annualized)
Max drawdown: 16.8%
UPTREND: +$1,567 | DOWNTREND: +$780 | SIDEWAYS: skipped
```

---

## Risk Rules

| Rule | Value | Why |
|------|-------|-----|
| Risk/trade | 1% | 2% destroys account (-359% in backtest) |
| Daily loss | 3% | Circuit breaker |
| Max DD | 10% | Capital preservation |
| Min RR | 1:2 | Winners ≥ 2× losers |
| SL | 2× ATR | 1× ATR too tight (noise stops you out) |
| Trail | 2× ATR | Lets winners run |
| Max positions | 2-3 | Concentration control |
| SIDEWAYS | SKIP | 40.8% WR, net negative |
| Syed max lot | 0.10 | Cap in config |

---

## Federation Integration

### Asset APIs (all Express.js, live on VPS)

| Asset | Port | Symbol | Public Path |
|---|---|---|---|
| Gold (XAUUSD) | :3456 | GC=F | `/wealth/gold/api/*` |
| Brent Crude | :3457 | BZ=F | `/wealth/oil/api/*` |
| Natural Gas | :3458 | NG=F | `/wealth/gas/api/*` |

### API Endpoints (identical across all 3)

| Endpoint | What it does |
|---|---|
| `/api/ticker` | Price, RSI, EMA20/50/200, S/R 1H |
| `/api/signal_v2` | Full signal: regime + confluence + entry/SL/TP |
| `/api/apex` | G score, C_dark, clarity/risk/trend |
| `/api/macro` | DXY, US10Y, VIX, GSR |
| `/api/calendar` | ForexFactory high-impact USD events |
| `/api/levels` | S/R 1H + Daily pivot levels |
| `/api/history` | OHLCV for TradingView chart |

### Caddy Routing

```
/wealth/{gold,oil,gas}/api/* → strip_prefix /wealth/{gold,oil,gas} → localhost:{3456,3457,3458}
/gold → /gold/ 308 redirect
```

### ⚠️ CRITICAL GAPS (identified 2026-07-18)

| Gap | Impact |
|---|---|
| **Gold engine has NO GIT REPO** | `/root/trading/` is loose scripts. VPS dies = all lost |
| **arif_judge NOT wired to signals** | Signals computed but not F1-F13 governed |
| **VAULT999 NOT recording trades** | No immutable audit trail |
| **No API auth** | Endpoints open. No monetization possible |
| **Oil & gas backtests not done** | Only gold has 2yr backtest |

---

## Sovereign Approval Gate (F13) — CRITICAL

**STRUCTURAL GAP (post-mortem 2026-07-23):** Morning Analysis recommends setups, Zen Executor auto-executes them — with NO human approval between them.

- Syed-approved trades: 100% WR (1/1)
- Auto-executed trades: 33% WR (1/3)
- Net: -$145.40 (auto losses: -$576.40, Syed profit: +$431.00)

**THE FIX — inject human gate:**

```
Morning Analysis → signal setup
    ↓
Hermes sends to Arif/Syed: "Signal: XAUUSD BUY $zone. Approve?"
    ↓
Arif/Syed: "Ok" / "Skip" / "SL tighter"
    ↓
IF APPROVED → Zen Executor watches for trigger
IF SKIPPED → ignored
```

**Without this gate, paper bot trades like headless robot.** Human approval IS the edge — not the technical signal. This is F13 SOVEREIGN in action at the trading layer.

---

## Cron Schedule

| Job | Schedule | Delivery |
|---|---|---|
| Gold Signal Briefing | 8am MYT Mon-Fri | SADO group |
| Price alert | 8:30am MYT daily | SADO group |
| XAUUSD Daily Signal | 9am MYT Mon-Fri | origin |
| Weekly report | Friday 8pm MYT | SADO group |

---

## Modules

- `signals/regime.py` — 3-pattern regime detection
- `signals/engine_v2.py` — signal generation (buy low sell high, trend-only)
- `signals/apex_predictor.py` — APEX G/C_dark/dS market state
- `signals/scanner.py` — EMA, RSI, MACD, ATR, S/R, candle patterns
- `signals/data_feed.py` — yfinance data (GC=F)
- `risk/position_sizer.py` — Kelly + fixed-risk
- `risk/manager.py` — drawdown protection, daily loss limits
- `governance/gate.py` — arifOS F1-F13 constitutional gate
- `backtest/engine_v2.py` — backtester (corrected P&L, trend-only)

---

## Pitfalls (CRITICAL)

### Gold P&L Multiplier = 1000, NOT 100

XAUUSD futures: `pnl = (exit - entry) * lots * 1000`. Using 100 → lots 10× too large → blowup. This bug caused -62% in initial backtest.

### RSI Filters Too Strict in Trends

In trends, RSI avg=58 (uptrend) / 44 (downtrend). Only 1.9-2.6% of bars cross 35/65 thresholds. Don't use RSI as entry gate in trending markets.

### yfinance Data Limits

GC=F = futures, not spot (may differ from MT5 by $2-5). Hourly max ~2yr. Daily 25+yr available.

### Backtest Gotchas

- Warmup 210 bars minimum (EMA200 needs 200 + buffer)
- Verify P&L math manually on 2-3 trades before trusting results
- `max(0.01, lots)` may exceed 1% risk on wide stops — use `max(0.001, lots)` for backtest

### $ in matplotlib = Math Mode Crash

`plt.rcParams['text.usetex'] = False` AND replace `$` with `USD` in ALL text strings.

### XAUUSD Pip Convention — GET THIS RIGHT

XAUUSD pip calculation varies by broker decimal places. **Always state the convention used.**

| Convention | 1 Pip Equals | Example: 4045.44 → 4047.00 |
|------------|:------------:|:---------------------------:|
| **2 decimals (most MT5)** | $0.01 | **156 pips** |
| **3 decimals (some brokers)** | $0.001 | **1560 pips** |
| **Points (price units)** | $1.00 | **1.56 points** |

**Pip value per lot:**
- 1 standard lot (100 oz) = **$1.00 per pip** (2-decimal convention)
- So 156 pips × 1 lot = $156 P&L

**Rule:**
1. When analyzing Syed's trades, **use 2-decimal convention** (MT5 standard): 1 pip = $0.01
2. Price difference × 100 = pips (e.g., 1.56 × 100 = 156 pips)
3. NEVER mix "points" and "pips" in the same message without clarifying
4. If unsure, just state raw price movement: "Entry 4045.44, current 4047.00 = +$1.56/oz profit" — unambiguous

**Pitfall (2026-07-31):** Gave inconsistent pip math to Syed — said "1.56 points = 15.6 pips" then corrected to "1.56 pips". Both wrong under standard convention. Syed called it out: "Hang Kira pips pon x betul canna hang analisa." Rule: **If you can't do the math in your head, just state the price move and let him calculate.** Wrong math destroys trading credibility instantly.

### SABAR Discipline

SABAR is a FEATURE, not a bug. Never suggest lowering confluence thresholds to "fix" lack of signals. Arif: "SABAR JA LA... Thats why abang sado tu sado."

---

## Human-Language Translation: `translateJudge()`

Constitutional floor language is internal. Public dashboards must convert:

```
BEFORE: "F1: No stop loss — irreversible risk; F2: No confluence factors..."
AFTER:  "Market belum jelas. Tunggu trend + isyarat aligned sebelum masuk."
```

Strips F-floor refs. Replaces jargon (insufficient reward → potensi untung tak berbaloi). Conversational BM.

---

## Related Skills

- `trading-signal-chart` — PASSIVE NODE (chart generation, NO broker access)
- `syedos` — Abang Sado trading companion (voice mode, XAUUSD signals)
- `mt5-ai-trading-agent` — MetaTrader 5 bridge (future sync needed)
- `daily-trading-signal-briefing` — absorbed into trading-signal-chart

---

## References

- `references/xauusd-signal-spec.md`
- `references/backtester-architecture.md`
- `references/gold-dashboard-architecture.md`
- `references/trading-web-terminal.md`
- `references/strategy-postmortem.md`
- `references/backtest-methodology.md`
- `references/gold-session-volatility.md`
- `references/plain-language-translator.md`
- `references/trade-review-chart.md`
- `references/governed-trading-engine.md`
- `references/red-blue-team-analysis.md`
- `references/cognitive-trading-psychology.md`
