---
name: mt5-ai-trading-agent
description: "Build AI-powered trading agents that connect MetaTrader 5 to Hermes intelligence — technical analysis, signal generation, risk management, voice delivery. Covers XAUUSD, forex, commodities."
version: 1.0.0
tags: [trading, metatrader5, mt5, xauusd, forex, gold, ai-agent, technical-analysis, risk-management]
metadata:
  hermes:
    tags: [trading, metatrader5, mt5, xauusd, forex, gold, ai-agent, technical-analysis, risk-management]
    related_skills: [tts-edge-fallback, deep-research, music-intelligence]
triggers:
  - trade
  - trading
  - mt5
  - metatrader
  - xauusd
  - gold trading
  - forex bot
  - trading bot
  - trading signal
  - buat duit
---

# MT5 AI Trading Agent

Build AI-powered trading agents that combine MetaTrader 5 execution with Hermes intelligence — technical analysis, macro awareness, risk management, and voice-delivered signals.

## Architecture

```
MT5 Terminal (Windows/VPS)
    ↕ MetaTrader5 Python package
Python Signal Engine (technical analysis)
    ↕ API call
Hermes AI Agent (macro, sentiment, news, reasoning)
    ↕ Decision + risk calc
Telegram Bot (signals, voice notes, confirm flow)
    ↕ User confirmation
MT5 Execute Trade
```

## Broker Setup (Prerequisite — Do This First)

**MT5 app on its own is an empty shell.** When you first download MT5 mobile/desktop, it connects to `MetaQuotes Ltd.` — this is NOT a real broker. It says right on the screen: "Not a broker, no real trading accounts." You cannot trade with this.

### Step-by-step for Malaysian traders

1. **Open a real trading account** with a broker (see [broker comparison](references/malaysia-broker-setup.md))
2. **Get from broker:** Account number, password, server name
3. **In MT5:** Settings → New Account → enter broker credentials
4. **Verify:** Broker Information should show your broker's name, NOT "MetaQuotes Ltd."

### Recommended brokers for micro-lot XAUUSD (Malaysia)

| Broker | Server Name | Spread XAUUSD | Min Lot | Regulation |
|---|---|---|---|---|
| **Exness** | Exness-Real | 15-20 sen | 0.01 | FSA, FSCA |
| **IC Markets** | ICMarkets-Live | 10-15 sen | 0.01 | ASIC, CySEC |
| **XM** | XMGlobal-Real | 20-25 sen | 0.01 | CySEC, ASIC |
| **Pepperstone** | Pepperstone-Live | 12-18 sen | 0.01 | ASIC, FCA |

Full comparison + funding methods in `references/malaysia-broker-setup.md`.

### Wine path for Linux VPS

Since arifOS runs on Linux (`af-forge`), MT5 Python requires Wine:

```bash
# Install Wine (Ubuntu/Debian)
sudo apt install wine wine32 wine64

# Download MT5 terminal inside Wine
wine mt5setup.exe

# Install MetaTrader5 Python via Wine's Python
wine pip install MetaTrader5
```

Alternative: MQL5 EA inside MT5 triggered by webhook from gold-api — zero Wine dependency, but less flexible than Python.

## MT5 Connection

### Authentication (no API key needed)

MT5 uses **broker credentials**, not API keys:

| Field | Source |
|---|---|
| Account Number | Broker (Exness, XM, ICMarkets, Pepperstone) |
| Password | Broker (set at account creation) |
| Server | Broker (e.g., "Exness-Real", "XMGlobal-Live") |

### Python Connection

```python
import MetaTrader5 as mt5

# Initialize
mt5.initialize()

# Login
mt5.login(
    login=12345678,           # account number
    password="your_password",  # broker password
    server="Broker-Live"       # server name
)

# Get live price
tick = mt5.symbol_info_tick("XAUUSD")
print(f"Bid: {tick.bid}, Ask: {tick.ask}")

# Get candles
rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 100)

# Place order
order = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "XAUUSD",
    "volume": 0.01,
    "type": mt5.ORDER_TYPE_BUY,
    "price": tick.ask,
    "sl": tick.ask - 20,
    "tp": tick.ask + 40,
    "magic": 202607,
    "comment": "Hermes AI Signal",
}
result = mt5.order_send(order)
```

### Key Constraints

- **MetaTrader5 Python package = Windows only** (no Linux/Mac native). Use Wine or Windows VPS.
- **MT5 mobile** has no Python API — desktop terminal required for automation.
- **MQL5 Algo Trading** (inside MT5) is separate from Python — EAs run in MQL5, Python runs externally.
- **Investor password** = read-only (monitoring). **Main password** = trade execution.

## Technical Analysis Engine

Multi-indicator composite scoring for signal generation:

| Indicator | Calculation | Signal |
|---|---|---|
| SMA(10, 20) | Simple moving averages | Trend direction |
| EMA(9) | Exponential MA | Fast trend |
| RSI(14) | Relative Strength Index | >70 overbought, <30 oversold |
| MACD(12,26,9) | Moving Average Convergence Divergence | Histogram > 0 = bullish |
| Bollinger(20,2σ) | Bollinger Bands | Price outside bands = extreme |
| ATR(14) | Average True Range | Volatility for SL/TP sizing |
| Pivot Points | (H+L+C)/3 | S/R levels |

### Composite Scoring

```python
score = 0
# Each indicator contributes +1 (bullish), -1 (bearish), or 0 (neutral)
# Sum across all indicators
# score >= 2 → STRONG BUY
# score >= 0.5 → BUY
# score <= -2 → STRONG SELL
# score <= -0.5 → SELL
# else → NEUTRAL (wait)
```

**Key principle:** Multiple weak signals converging > one strong signal in isolation.

## Risk Management (Non-Negotiable)

| Parameter | Rule | Default |
|---|---|---|
| Risk per trade | Max 2% of account | 2% |
| Stop Loss | 1.5× ATR | Always set |
| Take Profit | 3.0× ATR (2:1 R:R minimum) | Always set |
| Lot size | `risk_amount / SL_distance` | Auto-calculated |
| Max positions | 3 concurrent | Per account |

### Lot Size Formula (XAUUSD)

```python
# XAUUSD: 1 lot = 100 oz, 1 point movement = $1 per 0.01 lot
risk_amount = account_balance * risk_pct  # e.g., $1000 * 2% = $20
sl_distance = atr * 1.5                   # e.g., $28.71 * 1.5 = $43.06
lot_size = risk_amount / sl_distance       # $20 / $43.06 = 0.46 lots
lot_size = max(0.01, min(lot_size, 10.0)) # clamp
```

## Signal Delivery — Voice-First Default

**Default delivery mode is VOICE, not text.** Most trading contacts prefer voice notes — they're at the gym, driving, or between clients. Text is supplementary.

### Serving Style (Critical)

When serving trading contacts (VIP or otherwise):
- **Don't ask unnecessary questions.** If you have enough info to serve, serve. "Nak buat macam mana?" when the answer is obvious = annoying.
- **Respect their identity.** A personal trainer / business owner who trades = they're busy. Be efficient, not chatty.
- **No group pings.** Trading signals go to DM only. Never ping in group chat.
- **Profile first, serve second.** Build a complete profile (name, occupation, preferred voice, trading pairs, risk tolerance) BEFORE sending anything. One setup conversation, then silent service.

### Telegram Text Signal

```
🔴 SELL XAUUSD @ $4,118
SL: $4,161 | TP: $4,032
Lot: 0.46 | Risk: $20 (2%)
R:R: 1:2.0

Confidence: MEDIUM
Reasons: RSI overbought, above BB upper, MACD bearish

Reply: ✅ EXECUTE or ❌ SKIP
```

### Voice Note (BM — Nusantara Mode)

When delivering trading signals as voice:

1. Write for speech — no markdown, no symbols
2. Spell numbers naturally: "$4,120" → "empat ribu seratus dua puluh dolar"
3. Use conversational BM with trading jargon in English
4. Structure: Yang bagus → Yang tak bagus → Trade plan → Kesimpulan
5. Use edge-tts `ms-MY-OsmanNeural` with `--rate="-5%"` for dense content
6. Max 4 minutes per note

```bash
edge-tts --voice ms-MY-OsmanNeural --file /tmp/signal.txt --write-media /tmp/signal.mp3 --rate="-5%"
```

### Confirm Flow (Semi-Auto)

```
Agent → Signal + Voice to Telegram
User  → ✅ or ❌
Agent → Execute on MT5 or Skip
Agent → Confirm execution receipt
```

## Macro Context Integration

AI agent adds value beyond technical analysis by incorporating:

- **Fed policy / interest rate** expectations
- **US economic data** (NFP, CPI, unemployment)
- **Geopolitical tensions** (Middle East, trade wars)
- **USD strength** (DXY index)
- **Commodity correlations** (oil, silver)
- **Central bank gold buying** trends

Research via `web_search` or `arif_observe(mode="search")` before each signal.

## XAUUSD Specifics

| Parameter | Value |
|---|---|
| Current range (Jul 2026) | $4,029–$4,205 |
| ATH | $5,595 (Jan 29, 2026) |
| Typical daily range | $30–80 |
| Best sessions | London (3pm–12am MYT), NY overlap |
| Spread (typical) | 15–30 cents |
| Swap (long) | -$3 to -$5/lot/night |
| Swap (short) | +$1 to +$3/lot/night |

## Pitfalls

- **MT5 default server is MetaQuotes demo, NOT a real broker** — fresh MT5 install connects to "MetaQuotes Ltd." which says "Not a broker, no real trading accounts." If Broker Information shows this, you need to open a real broker account first. The MT5 app is an empty shell until you log into a broker.
- **MetaTrader5 Python = Windows only** — no native Linux/Mac. Use Windows VPS or Wine on Linux (see Broker Setup §Wine path).
- **MT5 mobile has no API** — desktop terminal required for Python automation.
- **Gold is news-sensitive** — one Fed statement can move it 30-40 pips. Always set SL.
- **Spread blowup during news** — high-impact events widen spread significantly. Avoid trading 5 min before/after.
- **Swap fees accumulate** — holding long gold positions overnight costs $3-5/lot. Factor into swing trades.
- **RSI divergence on gold** — RSI can stay overbought/oversold longer than expected on XAUUSD due to strong trends. Don't counter-trade RSI alone.
- **BPM double-time in price action** — gold's volatility can trigger false breakouts. Use multi-timeframe confirmation.
- **Demo first** — always test on demo account for 3+ months before going live.
- **Not financial advice** — always include disclaimer. AI signals are educational, not guaranteed.
- **Visual chart analysis is WAJIB** — Arif (2026-07-18): "Weiii trading agent kena pandai tengok chart laaa, wajib. Pi cari cara nak ignite visual intelligence!!" Use MiniMax vision via `mmx vision describe` as primary. OCR fallback only if mmx quota exhausted. See §Vision Chart Analysis.

## Gold/Oil/Gas Site Dashboards — Cognitive Clarity

**Canonical URLs:**
- Gold: `https://arif-fazil.com/gold/`
- Brent Crude: `https://arif-fazil.com/oil/`
- Natural Gas: `https://arif-fazil.com/gas/`

(Also reachable via `/wealth/{gold,oil,gas}/` and organ subdomains.)

Three single-file HTML dashboards backed by gold-api (:3456), oil-api (:3457), gas-api (:3458). All three share identical architecture. Gold is the canonical template; oil & gas are derived via sed substitution (4 differing lines: API_BASE, asset name, yfinance symbol, labels). Dark theme, TradingView Lightweight Charts, mobile-responsive.

### Live Data Rule (NON-NEGOTIABLE)

Every number on the site comes from the live gold API. **No hardcoded numbers.** Stale data = Syed makes wrong trades = real money lost. Arif: "kalau abang sado tengok chart salah, lepas tu buat tarde rugi sapa nak tanggung?"

- HTML defaults: use `—` (em dash), never stale prices
- Timestamp: use "Loading live data..." not old dates
- Boot sequence: **refreshTicker + refreshMacro FIRST, chart second** (no await on heavy renderChart)

Full architecture, API endpoints, Caddy routing, and pitfalls: `references/gold-site-architecture.md`.

## Vision Chart Analysis — WAJIB

**Arif (2026-07-18):** "Weiii trading agent kena pandai tengok chart laaa, wajib. Pi cari cara nak ignite visual intelligence!!"

The trading agent MUST be able to analyze chart screenshots sent via Telegram. Current working solution:

### Primary: MiniMax Vision via mmx-cli

```bash
# Requires: npm install -g mmx-cli + MiniMax Token Plan subscription
source /root/.secrets/vault.env
mmx auth login --api-key "$MINIMAX_API_KEY" --non-interactive
mmx vision describe --file /path/to/chart.jpg --non-interactive
```

Returns structured analysis: price, timeframe, pattern, S/R levels, volume, position markers. Works on MT5 mobile screenshots, TradingView charts, any trading platform.

### Fallback chain when vision fails:
1. **OCR (tesseract)** — extracts price numbers, labels, timestamps from screenshots
2. **Gold API live data** — cross-references OCR numbers with actual live market
3. **User description** — ask "describe the chart" if both fail

### Key pattern: Vision + API cross-reference
Always cross-check vision analysis against live gold API data. Vision tells you what the chart LOOKS like; the API tells you what the market IS doing right now. If they disagree, the API wins.

## Multi-Timeframe Analysis (H4 + H1)

The standard approach for Syed/Abang Sado — widely used among traders.

### The Rule
```
H4 determines DIRECTION → H1 determines TIMING
```

**Never trade against the higher timeframe.** If H4 says DOWNTREND, you only look for SELL entries on H1. Buy signals on H1 during H4 downtrend = traps.

### Live example (2026-07-18)
```
H4: EMA20 ($4,007) < EMA50 ($4,014) → BEARISH / DOWNTREND
H1: Price ($4,023) > both EMAs → PULLBACK within downtrend

Analysis: H4 says DOWN — look for sell entries only.
H1 pullback hasn't aligned yet → SABAR (wait).
When H1 turns down to follow H4 → entry signal.
```

### Three alignment states
| H4 | H1 | Action |
|---|---|---|
| UP | UP | BUY entry |
| UP | DOWN | SABAR — wait for H1 to align |
| DOWN | DOWN | SELL entry |
| DOWN | UP | SABAR — wait for H1 to turn |
| SIDEWAYS | either | Range trade or stay out |

Full reference: `references/multi-timeframe-h4-h1.md`.

For generating visual trading signal PDFs with candlestick charts, use the `scientific-pdf-generation` skill (Mode D). Key specs:

- **Chart type:** Manual candlestick drawing with matplotlib (not mplfinance — need full annotation control)
- **Color rule:** Red filled = bearish (close < open), Green hollow = bullish (close > open). NOT trend-following colors.
- **EMA overlay:** EMA 20 (blue #58a6ff) + EMA 50 (orange #f0883e) always
- **Dark theme:** BG #0d1117, OANDA-style
- **Layout:** Landscape A4, chart = 80% of page, strategy table below
- **Mobile-first:** 10pt+ annotations, 13pt+ zone labels, bold colored boxes
- **Temporal zones:** Buy/sell zones AT current price, not distant S/R
- **Pattern labels:** H=Hammer, D=Doji, SS=Shooting Star, BE=Bearish Engulfing

Full reference: `scientific-pdf-generation/references/trading-signal-charts.md`

## References

- `references/xauusd-agent-demo.py` — full working Python demo with technical analysis engine, signal generation, and risk management calculator
- `references/mt5-python-setup.md` — step-by-step MT5 + Python setup guide
- `references/malaysia-broker-setup.md` — broker comparison + funding for Malaysian MT5 traders
- `references/multi-timeframe-h4-h1.md` — H4/H1 multi-timeframe analysis explained for traders
- `references/gold-site-architecture.md` — arif-fazil.com/gold live dashboard architecture, API endpoints, Caddy routing

## Phased Deployment (Constitutional Path)

This skill covers **Phase 3-4** (auto/semi-auto execution). For earlier phases:

| Phase | Mode | Skill | What happens |
|---|---|---|---|
| 1 | Companion | `syedos` | AI generates signal, human executes on MT5 manually |
| 2 | Demo | `syedos` + this skill | AI executes on demo account via MT5 Python |
| 3 | Supervised | This skill | AI executes live, human approves each trade |
| 4 | Semi-auto | This skill | AI auto-exutes with risk limits, human monitors weekly |

**Phase 1 gold engine (already live):**
- Location: `/root/trading/scripts/gold_engine.py`
- Config: `/root/trading/config/trading_spec.json`
- Journal: `/root/trading/journal/signals.jsonl`
- Cron: `2258f1b3fa0e` — 8am MYT daily
- Uses Yahoo Finance (free, no API key), yfinance + pandas + ta
- EMA 20/50, RSI divergence, S/R, candle patterns, session filter, ≥2 confluence rule

**To advance to Phase 2:** Connect MT5 Python on Windows VPS, use this skill's MT5 connection code, point signals from gold_engine.py to mt5.order_send().
