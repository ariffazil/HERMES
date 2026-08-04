---
name: trading-signal-chart
description: "Generate trading signal charts and PDFs — candlestick OHLC with EMA overlays, buy/sell zones, stop loss, targets. **PASSIVE NODE — STRICTLY READ-ONLY. NO broker API, NO MT5 bridge, NO execute_trade.**"
version: 2.1.0
author: Hermes Agent (consolidated from daily-trading-signal-briefing, trading-analysis-xauusd)
tags: [trading, chart, candlestick, gold, xauusd, signal, pdf, matplotlib, passive]
organ: WEALTH (:18082)
f1-boundary: "STRICTLY READ-ONLY — chart generation + analysis output + cron dispatch only. Zero broker/MT5 code allowed."
zen-organs: [W EXECUTION (chart only), ΔR (price data), ∇F (signal meaning)]
triggers:
  - "trading signal"
  - "gold signal"
  - "xauusd chart"
  - "candlestick chart"
  - "daily signal"
  - "buy sell signal"
  - "trading plan chart"
---

# Trading Signal Chart — PASSIVE NODE

**F1 BOUNDARY: STRICTLY READ-ONLY.** This skill generates charts, analysis, and text. It NEVER calls broker APIs, MT5 bridge, or `execute_trade`. If you need trade execution, use `agentic-trading-companion` (ACTIVE NODE).

**ABSORBED:** daily-trading-signal-briefing · trading-analysis-xauusd

---

## Delivery Preference — VISUAL FIRST (Arif/Syed)

**MANDATORY ORDER:**
1. **CHART** — Generate and deliver image FIRST
2. **Summary** — 3-5 bullet points MAX (or none if chart is self-explanatory)
3. **Text analysis** — ONLY if explicitly requested

**User feedback (Jul 2026):** "Aku malas nak baca" — Arif prefers images over long text. When asked for trading analysis, the DEFAULT deliverable is a chart. Text is supplementary, not primary.

**User feedback (Aug 2026 — "live gold today + upcoming week + full agentic intelligence insights, minimize text focus on visual deliver for human cognitive understanding"):** Reinforces the above with two new rules:
1. **PDF = single visual artifact.** Build the chart + analysis panel + disclaimer in ONE matplotlib figure, then wrap the same figure with `matplotlib.backends.backend_pdf.PdfPages`. Do NOT build a separate reportlab doc for "visual-first" requests — the user wants to open ONE PDF and see the whole picture without scrolling. Chart area + right-side LEGEND PANEL (per Side Panel rule below) + small footer line = the whole PDF.
2. **Chat-side text ≤ 8 markdown lines.** No repeated values that are already on the chart. No narrative summary. Default = `MEDIA:` link to PDF + `MEDIA:` link to PNG + ≤ 8-line bullet recap (price, range, bull/bear trigger, key zones, sentiment tag, disclaimer).

**Pattern:**
- User asks: "Bagi prediction untuk gold" → Deliver chart with S/R levels + 3-line summary
- User asks: "Baca analysis" → NOW provide detailed text
- User asks: "PDF live gold today + week trend" → ONE-PDF approach (matplotlib + PdfPages) + chat-side bullet recap only
- Never lead with long markdown tables when a chart can convey the same info

**Chart = king. Text = servant. PDF = the unit of delivery for visual-first requests.**

---

## Audience

Rakyat marhaen — common people, not brokers. Simple language. BUY HERE, SELL HERE, SL HERE. No Fibonacci, no Elliott Wave jargon. Delivered to Syed/Abang Sado via Telegram and SADO group.

## Core Trading Methodology (from Abang Udin, Jul 2026)

### Analysis Framework

1. **Identify Key Levels** — Resistance zones (previous highs, round numbers), Support zones (previous lows, consolidation floors)
2. **Read Price Action** — Candlestick patterns at key levels, trend direction, volume confirmation
3. **Confirmation-Based Entries** — NEVER call entry without confirmation candle. Wait for rejection candle at key level.
4. **Risk Management** — Always calculate R:R. Tight SL ($20-30 on gold). Partial close strategy.

### The 8 Core Principles

1. **TEMPORAL** — Buy/sell zones MUST be close to current market price. Not $200 away.
2. **OANDA STYLE** — Zoom IN, big candles, tight Y-axis, labels on side not blocking candles.
3. **REAL CANDLESTICKS** — Red filled = bearish, Green hollow = bullish. No trend-coloring.
4. **EMA 20 + 50** — Blue fast, orange slow. Dynamic S/R.
5. **ONE CHART, ONE WORLD** — Everything on one chart. Chart = king.
6. **R:R VISUAL** — Show risk/reward arrows on chart. R:R big and bold. < 1:2 = NO TRADE.
7. **CONFIRMATION** — Wait for candle close above EMA 20 on 1H. Don't catch falling knives.
8. **EVENT DAYS** — CPI, NFP, FOMC = wait. Hot = no trade. Cold = confirm.

### Half-Close Workflow

When position is in decent profit:
1. Close 50% → lock profit
2. Move SL to breakeven on remaining → free ride
3. Trail SL to recent swing high/low
4. Let remainder ride to TP1/TP2

### Exit Strategy

> **One Rule:** Exit when the reason you entered is no longer valid.

- TP hit → take it, don't chase
- Candle rejection at resistance → exit or partial
- Structure break → exit
- Trade doesn't move in 24-48hrs → reassess

### News Event Framework

| Event | MYT Time | Avg Gold Move |
|---|---|---|
| CPI | 20:30 monthly | $40-80 |
| NFP | 20:30 1st Friday | $50-100 |
| FOMC | 02:00, 8x/year | $30-80 + $50-100 press |

**15-Minute Rule:** T-15 close positions. T-0 watch. T+15 confirm direction. T+30 enter if clear.

### Multi-Position Management

- Calculate average entry across all positions
- Single SL for all positions
- Single TP at major support/resistance
- R:R from average entry to TP

---

## Design Principles

### Mobile-First. ALWAYS.

**Rules:**
- ONE chart per page. Font minimum: 10pt labels, 13pt key levels, 15pt current price.
- Box labels (BUY ZONE, STOP LOSS) must be 13-14pt bold filled background.
- Figure size: 11×7 inches minimum. DPI 150.

**What WORKED:** Single candlestick chart 11×7, dark BG, big labels. Strategy table BELOW chart in PDF (reportlab Table), not matplotlib subplot. R:R as simple box in corner.

### Candlestick Colors

- RED filled body = bearish (close < open) — ALWAYS
- GREEN hollow body = bullish (close > open) — ALWAYS
- Do NOT color by trend direction
- Doji = grey thin cross. Mark: H=Hammer, D=Doji, SS=Shooting Star, BE=Bearish Engulfing

### EMA Overlays

- EMA 20 = blue (#58a6ff), linewidth 2.2
- EMA 50 = orange (#f0883e), linewidth 2.2
- Both on every timeframe
- Mark Golden Cross / Death Cross when they occur

### Dark Theme Colors

```
Background:  #0d1117   Gold accent: #f0a500
Panel:       #161b22   Green (bull): #3fb950
Red (bear):  #f85149   Blue (EMA20): #58a6ff
Orange(50):  #f0883e   Teal (S/R):   #39d2c0
Text:        #e6edf3   Dim:          #8b949e
```

### Chart Elements (every chart)

| Element | Style |
|---|---|
| BUY zone | Green shaded band + 14pt label box |
| SELL zone | Red shaded band + 14pt label box |
| STOP LOSS | Red dashed line + 13pt annotation |
| TARGET 1 | Green dotted line + 13pt annotation |
| TARGET 2 | Teal dotted line + 13pt annotation |
| R:R box | Top-right corner, dark panel, 22pt number |
| Current price | Gold circle + 15pt label |
| EMA 20/50 | Blue/Orange lines, 2.2pt |
| Risk/Reward arrows | Bidirectional, red=down green=up |

### PDF Structure — One Page, Chart + Table

```
┌─────────────────────────────────────┐
│  GOLD DAILY SIGNAL title            │
│─────────────────────────────────────│
│  [CANDLESTICK CHART — 19cm wide]    │
│─────────────────────────────────────│
│  Strategy Table: ENTRY/SL/TP1/TP2/R:R│
│  VERDICT line                       │
│  Disclaimer                         │
└─────────────────────────────────────┘
```

Landscape A4 for wider charts.

### Multi-Timeframe — When Requested

Use SEPARATE charts stacked vertically, NOT one dense chart:
- Daily (trend) — largest
- 4H (intermediate) — medium
- 1H (entry) — smallest

### Confirmation Signals

Always include: "Wait for candle close above EMA 20 on 1H before entry" or "Wait for RSI to turn up from oversold."

### Zoomed Chart Mode

Default: 72 candles (3 days of H1). Zoomed: 36 candles (1.5 days). User says "zoom in" → use 36.

### S/R Level Detection — Pivot-Based Within Visible Range

Don't use rolling window extremes on full 60-day data. Use pivot-based detection within charted window. Max 2-3 per side. Focus on levels NEAR current price.

### RSI Panel — Below Main Chart (TINY)

`height_ratios=[9, 1]` — RSI gets only 10% vertical space. Not `[3, 1]`.

### Signal Zone Visualization

Entry/SL/TP bands on chart. Risk zone (red shading), Reward zone (green shading).

### Side Panel for Portfolio Review Labels

When doing portfolio review with multiple assets: chart area = candles ONLY. ALL labels, levels, R:R, analysis go in a RIGHT-SIDE LEGEND PANEL (28% of figure width). Never overlay text on candles.

---

## Signal Format (2 signals every morning)

### BUY SIGNAL (Long entry)
```
ENTRY:     $X - $Y
STOP LOSS: $Z
TARGET 1:  $T1 (+$N)
TARGET 2:  $T2 (+$N)
R:R:       1:X.X / 1:Y.Y
STATUS:    READY / WAIT / NO TRADE
```

### EXIT LEVELS (Sell if already holding)
```
TAKE PROFIT 1:   $TP1 — Jual separuh (50%)
TAKE PROFIT 2:   $TP2 — Jual semua (100%)
TRAIL STOP:      $X — Naikkan SL ke entry
EMERGENCY EXIT:  $EX — Cut loss
```

---

## Data Sources

| Source | Latency | Best for |
|---|---|---|
| Gold API `:3456` | Real-time | Primary feed (chart) |
| yfinance GC=F | ~15 min | Fallback |
| web_search | Variable | Quick check |

### Gold API Integration

```bash
# Quick chart pipeline
curl -s 'http://localhost:3456/api/gold/history?period=3d' | python3 flatten.py
# Render chart
python3 chart_script.py  # reads /tmp/gold_flat.json → /tmp/gold_chart.png
# Ticker (price, RSI, EMAs)
curl -sf localhost:3456/api/gold/ticker
```

---

## Chart Generation Pipeline

### Preferred: chart_pro.py

```bash
cd /root/trading && python3 scripts/chart_pro.py --signal LONG --entry 4003 --sl 3970 --tp 4066 --json
```

Output: `/tmp/xauusd_chart.png` (300KB, 180 DPI, landscape)
JSON metadata: price, bias, confidence, rsi, ema20/50/200, support[], resistance[]

### End-to-End Workflow

**Step 1: Gather Data** (3 parallel searches)
```python
web_search("XAUUSD gold price today [DATE]")
web_search("gold news today [MONTH] [YEAR] economic events")
web_search("XAUUSD technical analysis support resistance [MONTH] [YEAR]")
```

**Step 2: Set Signal Levels** — Use extracted S/R as zone boundaries. Buy zone = nearest strong support ±$10.

**Step 3: Generate Chart** — `write_file()` + `terminal()` (not execute_code — matplotlib not in sandbox).

**Step 4a: Generate ONE-PDF (visual-first requests)** — Build the figure with candles + EMAs + zones + right-side LEGEND PANEL carrying all text (sentiment tag, range, bull/bear triggers, action). Wrap the SAME figure with `matplotlib.backends.backend_pdf.PdfPages` — see `templates/gold_live_weekly_pdf.py`. ONE render call, no reportlab table.

**Step 4b: Generate PDF (daily-signal cron format with strategy table)** — reportlab Table below chart, `write_file()` + `terminal()`. Use only when user asks for a paper trading plan / printable signal sheet, not for visual-first "what's gold doing today" requests.

**Step 5: Deliver** — chat-side ≤ 8 lines of markdown bullets. PDF + PNG as `MEDIA:` links. NEVER repeat values that are already on the chart.

### Voice Note Generation (SADO 8am)

After text + chart, generate BM voice note:
```bash
edge-tts --voice ms-MY-OsmanNeural --rate "+5%" \
  --file /tmp/syed_voice.txt --write-media /tmp/syed_voice.mp3
```
~90 seconds. Spell out numbers in BM. Lead with story, then levels, then verdict, then action.

---

## Pitfalls (CUMULATIVE)

- **`$` in matplotlib text = LaTeX crash.** Replace `$` with `USD` in ALL text. `plt.rcParams['text.usetex'] = False` alone not enough.
- **numpy int64 in JSON output.** Use custom encoder: `np.integer`→int, `np.floating`→float, `np.ndarray`→list.
- **Plotly+kaleido too slow for cron** (60s+). Use matplotlib (3-5s).
- **Variable passage between chart and PDF scripts.** PDF must independently define ALL signal-level variables (BUY_ZONE_LOW, SL, T1, T2, ENTRY_MID). No shared state.
- **DPI too high on mobile.** Use 150, not 200.
- **Engine session gate at 8am MYT.** Gold engine blocks Asian session. Fall back to web-search pipeline.
- **S/R level clusters.** If levels within $5, treat as one. Supplement with web-search data.
- **Chart zone shading matters.** Profit zone (green) + risk zone (red) makes setup instantly visible.
- **Bias pill in header.** BULLISH/BEARISH/NEUTRAL + confidence %.
- **Cron venv path.** Use `/root/venv/bin/python3`, not bare `python3`, for cron scripts.
- **Gold API missing trading module.** Fall back to ticker-only mode + web search.
- **R:R consistency.** Use ONE entry midpoint for ALL calculations. Chart entry_mid = PDF entry_mid.
- **DO NOT use execute_code() for matplotlib/reportlab.** Use write_file() + terminal().
- **S/R from full 60d data with rolling(20) produces useless levels.** Detect within charted window.
- **`MEDIA:/path` delivery is NOT guaranteed visible to user.** Verify with `ls -lh` that file exists and has size > 0. If user says "hang x bagi" after MEDIA: delivery, assume the Telegram gateway didn't render it — regenerate or resend. Pitfall (2026-07-31): chart generated at 148K but user repeatedly said not received. Always confirm output file exists and has content before declaring "delivered."
- **Percentage, not pips, in chart labels.** Label S/R and price levels in price format ($4,050), not pip distance. Let `agentic-trading-companion` handle the % communication.
- **Pyrolite style sheet emits non-fatal `legend.bbox_to_anchor` warning** on user-level matplotlibrc. Ignore — chart/PDF still render correctly. Pitfall (2026-08-04).
- **For visual-first PDF requests, skip reportlab.** Single `matplotlib.backends.backend_pdf.PdfPages.savefig(fig, bbox_inches='tight')` is enough. Building a second reportlab doc duplicates effort and breaks the "one artifact, one picture" preference. Pitfall (2026-08-04).
- **Chat-side text must be sparse for visual-first requests.** ≤ 8 markdown lines. NEVER repeat price/RSI/levels that are already labelled on the chart. The PDF is the unit; chat is just a delivery notice. Pitfall (2026-08-04).

---

## Human-Readable Label Mapping (MANDATORY for user-facing text)

| Internal | Human Label |
|---|---|
| G score | Clarity |
| C_dark | Risk |
| dS/dt | Trend Energy |
| APEX Φ | Agreement |
| CLARITY state | Clear Trend |
| STABLE state | Ranging |
| CHAOS state | Choppy |
| SEAL | Strong Signal |
| PROCEED | Good to Go |
| SABAR | Wait |
| HOLD | Hold Off |

---

## References

- `references/multi-timeframe-structure.md`
- `references/indicator-calculations.md`
- `references/canvas-pdf-wrapping.md`
- `references/gold-api-internal-data-shape.md`
- `references/cron-chart-alert-delivery.md`
- `references/tradingview-lightweight-charts-webapp.md`
- `references/gold-dashboard-architecture.md`
- `references/gold-api-extension-pattern.md`
- `references/proven-data-pipeline.md`
- `references/red-news-impact.md`
- `references/chart-fallback-yfinance.md`
- `references/exit-strategy-framework.md`
- `references/paper-trading-workflow.md`
- `references/session-2026-07-14-xauusd.md`
- `references/visual-first-pdf-recap.md` — chat-side ≤8-line recap template (2026-08-04)
- `templates/gold_signal_chart.py`
- `templates/xauusd_signal_pdf.py`
- `templates/gold_mtf_chart.py`
- `templates/gold_live_weekly_pdf.py` — one-PDF visual-first template using `PdfPages` (2026-08-04)
