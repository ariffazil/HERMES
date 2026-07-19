---
name: trading-signal-chart
description: >-
  Generate trading signal charts and PDFs — candlestick OHLC with EMA overlays,
  buy/sell zones, stop loss, targets, R:R visualization. Dark theme (OANDA-style).
  Mobile-first: one chart, big text, legible on phone. Multi-timeframe when needed.
  For daily gold/trading signal briefings, cron-based or on-demand.
triggers:
  - "trading signal"
  - "gold signal"
  - "xauusd chart"
  - "candlestick chart"
  - "trading pdf"
  - "daily signal"
  - "buy sell signal"
  - "trading plan chart"
  - "risk reward chart"
tags:
  - trading
  - chart
  - candlestick
  - gold
  - xauusd
  - signal
  - pdf
  - matplotlib
---

# Trading Signal Chart Generation

## When to Use

When generating trading signal charts, daily trading briefings, buy/sell signal PDFs,
or any candlestick-based technical analysis visualization for human consumption.

**Key audience:** Traders reading on mobile phones. Text must be BIG. Chart must be CLEAN.
One glance = full understanding.

## Spatial Intelligence Protocol (2026-07-16)

When analyzing or describing a chart, follow this order:

1. **Spatial Layout** — Describe the visual structure first: where are candles relative to EMAs, S/R zones, and current price? What's the "shape" of the chart?
2. **Candle Formations** — Identify patterns: doji (indecision), engulfing (reversal), pinbar (rejection), consolidation (small bodies near support/resistance).
3. **Trend Structure** — HH/HL (bullish) or LH/LL (bearish)? Where is price relative to EMA stack?
4. **Zone Interactions** — Is price bouncing off support? Rejecting at resistance? Breaking with conviction?
5. **Meaning Resolution** — Translate visual into context: "consolidation near support with rising RSI = high-probability bounce" or "repeated rejection at resistance with weakening volume = distribution."
6. **Calibrated Confidence** — Assign confidence with evidence: structure clear (high), mixed signals (medium), reversal risk (lower).

**Output format:** Spatial layout → meaning → confidence → "Kau decide" + F13 reminder.

## Design Principles (LESSONS LEARNED — HARD WAY)

### 1. MOBILE-FIRST. ALWAYS.

User said "Fail. Aku x nampak apa" (I can't see anything) FOUR times before we got it right.

**Rules:**
- ONE chart per page. Never stack 3 charts unless text is 14pt+.
- Font minimum: 10pt for labels, 13pt for key levels, 15pt for current price.
- Box labels (BUY ZONE, STOP LOSS, TARGET) must be 13-14pt bold with filled background.
- Figure size: 11×7 inches minimum for single chart. DPI 150 (not 200 — file too big).
- PDF image width: 19cm (near full page). Leave only minimal margins.

**What FAILED (do NOT repeat):**
- Multi-panel charts (3 timeframes + R:R + RSI + signals) in one figure — too dense, unreadable
- 8pt text on chart labels — invisible on phone
- Complex gridspec layouts with 6+ subplots — rendering issues, clipping
- Strategy tables as separate charts — user can't connect chart to table

**What WORKED:**
- Single candlestick chart, 11×7, dark BG, big labels
- Strategy table BELOW chart in PDF (reportlab Table), not as matplotlib subplot
- R:R as a simple box in the corner of the chart, not a separate panel

### 2. REAL CANDLESTICKS — Not Trend-Following Colors

User explicitly corrected: "Aku nak candlestick yang bagi real maksud" (I want candlesticks with real meaning).

**Rules:**
- RED filled body = bearish (close < open) — ALWAYS
- GREEN hollow body = bullish (close > open) — ALWAYS
- Do NOT color based on trend direction (e.g., all red in downtrend)
- Doji = grey thin cross (indecision)
- Mark patterns: H=Hammer, D=Doji, SS=Shooting Star, BE=Bearish Engulfing

**Candlestick drawing code (proven):**
```python
cw = 0.6
for i in range(n):
    o, h, l, c = opens[i], highs[i], lows[i], closes[i]
    body = abs(c - o)
    rng = h - l if h - l > 0 else 1
    is_bull = c >= o
    is_doji = body < rng * 0.1
    body_bot = min(o, c)
    body_h = max(body, 1.5)
    
    if is_doji:
        ax.plot([i-cw/2, i+cw/2], [o, o], color=DIM, linewidth=2, zorder=5)
        ax.plot([i, i], [l, h], color=DIM, linewidth=1, zorder=5)
    else:
        col = GREEN if is_bull else RED
        if is_bull:
            rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                            facecolor='none', edgecolor=GREEN, linewidth=1.5)
        else:
            rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                            facecolor=RED, edgecolor=RED, linewidth=0.8, alpha=0.85)
        ax.add_patch(rect)
        ax.plot([i, i], [l, body_bot], color=col, linewidth=0.9)
        ax.plot([i, i], [body_bot + body_h, h], color=col, linewidth=0.9)
```

### 3. EMA OVERLAYS — Always Include

User (via Syed's feedback): "Include ema 20 50 as well"

**Rules:**
- EMA 20 = blue (#58a6ff), linewidth 2.2
- EMA 50 = orange (#f0883e), linewidth 2.2
- Both on every timeframe
- Mark Golden Cross / Death Cross when they occur

**EMA calculation:**
```python
def ema(prices, period):
    r = np.zeros(len(prices))
    m = 2 / (period + 1)
    r[0] = prices[0]
    for i in range(1, len(prices)):
        r[i] = (prices[i] - r[i-1]) * m + r[i-1]
    return r
```

**Pitfall:** For short datasets (<50 candles), EMA50 won't have enough data.
Use a smoothed proxy: `e50[i] = e50[i-1]*0.88 + closes[i]*0.12`

### 4. DARK THEME — OANDA Style

User showed OANDA mobile app screenshot as reference. Dark = professional for trading.

**Colors (OANDA-inspired):**
```
Background:  #0d1117
Panel:       #161b22
Gold accent: #f0a500
Green:       #3fb950 (bullish, buy zone, targets)
Red:         #f85149 (bearish, sell zone, stop loss)
Blue:        #58a6ff (EMA 20)
Orange:      #f0883e (EMA 50)
Teal:        #39d2c0 (support levels)
Text:        #e6edf3
Dim:         #8b949e
Border:      #30363d
```

### 5. TEMPORAL INTELLIGENCE — Zones AT Current Price

Syed's feedback: "Nak position buy or sell yang berdekatan dengan market price. X mau jauh sangat."

**Buy and sell zones must be AT or NEAR the current price**, not at distant S/R levels:
- If current price = $4,003 → buy zone = $3,995-4,010 (right here)
- Sell zone = $4,020-4,040 (just above, rejection play)
- NOT $4,180-4,200 (too far for day trading signal)

Distant levels (R1, R2, S1, S2) are reference context on the chart (subtle dashed lines), NOT the primary trade zones. The primary zones should be actionable NOW.

### 6. Y-AXIS SCALE — Zoomed to Relevant Range

User said "Scale of the chart x cantik" when Y-axis showed 3800-4500 but price was at 4000.

**Always zoom Y-axis to the relevant price range:**
- Bad: 3800-4500 when price is at 4000 (candles look tiny)
- Good: 3950-4120 when price is at 4000 (candles fill the chart)
- Rule: `margin = (max(highs) - min(lows)) * 0.15` on each side

### 7. CHART ELEMENTS — What Must Be On Every Chart

| Element | Style | Size |
|---|---|---|
| BUY zone | Green shaded band + label box | 14pt bold |
| SELL zone | Red shaded band + label box | 14pt bold |
| STOP LOSS | Red dashed line + annotation box | 13pt bold |
| TARGET 1 | Green dotted line + annotation box | 13pt bold |
| TARGET 2 | Teal dotted line + annotation box | 13pt bold |
| R:R box | Top-right corner, dark panel | 22pt number |
| Current price | Gold circle + label box | 15pt bold |
| EMA 20 | Blue line | 2.2pt |
| EMA 50 | Orange line | 2.2pt |
| RISK/REWARD arrows | Bidirectional, red=down, green=up | 3pt |
| Legend | Upper left, small | 10pt |

### 8. PDF STRUCTURE — One Page, Chart + Table

**Proven layout (mobile-friendly). Use landscape A4 for wider charts:**

```python
from reportlab.lib.pagesizes import A4, landscape
doc = SimpleDocTemplate(out, pagesize=landscape(A4), ...)  # wider chart
```

```
┌─────────────────────────────────────┐
│  GOLD DAILY SIGNAL (title, gold)    │
│  Date | Agent Intelligence          │
│─────────────────────────────────────│
│                                     │
│  [CANDLESTICK CHART — 19cm wide]    │
│  [with EMA, zones, SL, targets]     │
│                                     │
│─────────────────────────────────────│
│  ┌─────────┬──────────┬──────────┐  │
│  │         │ LONG     │ SHORT    │  │
│  │ ENTRY   │ $4,000   │ $4,180   │  │
│  │ SL      │ $3,970   │ $4,240   │  │
│  │ T1      │ $4,150   │ $4,080   │  │
│  │ T2      │ $4,200   │ $4,000   │  │
│  │ R:R     │ 1:3.7    │ 1:2.2    │  │
│  └─────────┴──────────┴──────────┘  │
│─────────────────────────────────────│
│  VERDICT: LONG $4,003 | SL $3,970   │
│  Not financial advice.              │
└─────────────────────────────────────┘
```

### 9. MULTI-TIMEFRAME — When Requested

User (via Syed): "Multi time frame. Candlestick pattern structure. Confirmation."

When multi-TF is needed, use SEPARATE charts stacked vertically, NOT one dense chart:
- Daily (trend) — largest
- 4H (intermediate) — medium
- 1H (entry) — smallest

**Pitfall:** Don't cram all 3 into one matplotlib figure with gridspec.
Each timeframe needs enough vertical space for candlesticks to be readable.
Better: generate 3 separate PNGs, stack in PDF with reportlab.

### 10. CONFIRMATION SIGNALS

Syed's feedback: "Confirmation. Ni komen abang sado Syed."

Always include a confirmation section:
- "Wait for candle close above EMA 20 on 1H before entry"
- "Wait for RSI to turn up from oversold"
- "Wait for volume confirmation on breakout"

## Data Sources for Gold Price

| Source | Latency | Cost | Best for |
|---|---|---|---|
| MT5 Python (`MetaTrader5` pkg) | Real-time | Free | Primary feed + execution |
| GoldAPI.io | Real-time | 300 req/month free | Backup feed |
| TradingEconomics | ~15 min | Free tier | Macro context |
| web_search "XAUUSD price today" | Variable | Free | Quick check |

## Pitfalls (CUMULATIVE — all proven failures)

- **numpy dtype casting:** `np.roll(int_array, 1)` returns int64. Adding float noise crashes.
  Fix: `.astype(float)` before arithmetic. Proven 2026-07-14.
- **matplotlib mpatches:** Must import `import matplotlib.patches as mpatches` BEFORE using
  `mpatches.Patch()` in legend. Import at top of file, not inline. Proven 2026-07-14.
- **Walrus operator in function args:** `facecolor=NAVY:=GOLD_C` is invalid syntax.
  Use `facecolor=GOLD_C` (assign separately if needed). Proven 2026-07-14.
- **DPI too high on mobile:** 200 DPI = 3MB+ PDF. Use 150 DPI for mobile-first charts.
- **Matplotlib `$` in text = LaTeX math mode crash.** Any `$` in text passed to `ax.text()`,
  `fig.text()`, `ax.set_title()`, or `ax.annotate()` triggers matplotlib's math parser.
  Symptom: `ValueError: Expected end of text, found '$'`. Fix: (1) `plt.rcParams.update({'text.usetex': False, 'mathtext.default': 'regular'})`
  at top of file. (2) Replace `$` with `USD` in ALL text strings that go to matplotlib
  labels — S/R labels, price annotations, alert text. (3) For the alert bottom text:
  `alert_text = alert_text.replace("$", "USD")`. This applies to EVERY matplotlib text
  function, not just `fig.text()`. Proven 2026-07-16: `sado_alert.py` — 5 iterations
  before identifying `$` in S/R labels and alert text as the root cause.
- **Emoji in PDF:** Emoji characters silently dropped by reportlab/pandoc.
  Use text equivalents or colored boxes instead.
- **Chart too complex:** 6+ subplots + annotations + multiple timeframes = user can't read.
  Simplify ruthlessly. One chart > three charts.
- **Dark BG + dark text:** Ensure all text is light-colored (#e6edf3) on dark backgrounds.
  Default matplotlib text color is black — invisible on #0d1117.
- **Portrait PDF for wide charts:** If the chart is wider than tall (single timeframe, zoomed),
  use `landscape(A4)` for the PDF. Portrait squeezes a wide chart into a narrow column.
  Proven 2026-07-14.
- **Reportlab HexColor requires `#` prefix:** `HexColor('#0d1117')` works, `HexColor('0d1117')` crashes
  with cryptic color parse error. Always include the `#`. Proven 2026-07-14.
- **Signal text clipping left:** When placing ENTRY/SL/TP text at x=-2 on candlestick chart,
  set `ax.set_xlim(-4, n+8)` to give enough left margin. Otherwise text is invisible.
  Proven 2026-07-14.

### 11. S/R LEVEL DETECTION — Pivot-Based Within Visible Range

Don't use rolling window extremes on full 60-day data — that produces S/R levels
far outside the visible chart range. Use pivot-based detection on the charted window.

```python
def find_sr_levels(df_chart, window=12):
    """Detect S/R from local pivots within the visible range."""
    candidates = []
    for i in range(window, len(df_chart) - window):
        if df_chart['High'].iloc[i] == df_chart['High'].iloc[i-window:i+window+1].max():
            candidates.append(('R', df_chart['High'].iloc[i]))
        if df_chart['Low'].iloc[i] == df_chart['Low'].iloc[i-window:i+window+1].min():
            candidates.append(('S', df_chart['Low'].iloc[i]))

    def cluster(levels, threshold=5.0):
        if not levels: return []
        levels = sorted(levels)
        clusters = [[levels[0]]]
        for v in levels[1:]:
            if v - clusters[-1][-1] < threshold:
                clusters[-1].append(v)
            else:
                clusters.append([v])
        return [round(np.mean(c), 2) for c in clusters]

    res = cluster([v for t, v in candidates if t == 'R'])
    sup = cluster([v for t, v in candidates if t == 'S'])
    return res, sup
```

**Pitfall:** S/R from full 60d data with `rolling(20)` produces levels like 3,955
and 4,783 when visible range is 4,050-4,100. Chart looks empty. Always detect
within the charted window.

### 12. SIGNAL DETECTION — EMA + RSI Confluence

Use EMA crossover direction + RSI filter + S/R proximity:

```python
ema_bull = ema20[-1] > ema50[-1]
rsi = calc_rsi(df, 14)

if ema_bull and rsi < 70:
    nearest_support = min(support_levels, key=lambda x: abs(x - price))
    signal = {'dir': 'LONG', 'entry': price, 'sl': nearest_support - margin, ...}
elif not ema_bull and rsi > 30:
    nearest_res = min(resistance_levels, key=lambda x: abs(x - price))
    signal = {'dir': 'SHORT', 'entry': price, 'sl': nearest_res + margin, ...}
```

**F3 WITNESS:** Single-indicator signal = breach. Require ≥2 confluence factors.

### 13. SIGNAL ZONE VISUALIZATION — Entry/SL/TP Bands

```python
ax.axhline(y=entry, color=GOLD, ls='-', lw=2.0, zorder=5)
ax.text(-2, entry, f"ENTRY {entry:,.2f}", fontsize=8.5, color=GOLD,
        va='center', ha='right', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.25', fc=BG, ec=GOLD, alpha=0.9))
ax.axhspan(sl, entry, alpha=0.08, color=RED, zorder=0)    # Risk zone
ax.axhspan(entry, tp3, alpha=0.04, color=GREEN, zorder=0) # Reward zone
```

**Pitfall:** Text at x=-2 needs `ax.set_xlim(-4, n+8)` or it clips off the left.

### 14. RSI PANEL — Below Main Chart (SMALL)

**User explicitly said: "RSI tu x payah besar sangat. Focus price signal."**

RSI panel must be TINY. The main chart is the star. RSI is supporting context only.

**Ratio:** Use `height_ratios=[9, 1]` — RSI gets only 10% of vertical space. NOT `[3, 1]` or `[5, 1.5]`.

```python
gs = GridSpec(2, 1, figure=fig, height_ratios=[9, 1], hspace=0.03)
ax_rsi = fig.add_subplot(gs[1], sharex=ax)
ax_rsi.plot(x, rsi_vals, color=GOLD, linewidth=1)  # thin line
ax_rsi.axhline(y=70, color=RED, ls='--', lw=0.3, alpha=0.3)
ax_rsi.axhline(y=30, color=GREEN, ls='--', lw=0.3, alpha=0.3)
ax_rsi.set_ylim(20, 80)
ax_rsi.set_ylabel('RSI', fontsize=7)  # tiny label
ax_rsi.text(len(x)-0.5, rsi, f'{rsi:.0f}', color=GOLD, fontsize=8, fontweight='bold', va='center')
```

**Rules:**
- RSI label: 7-8pt (not 10pt+)
- Line width: 1 (not 1.5+)
- Grid: minimal (alpha=0.1)
- No fill_between for zones — just thin dashed lines at 30/70
- RSI value label: small gold box, 8pt

- **Plotly+kaleido too slow for cron.** Takes 60s+ to render a single chart. Use matplotlib instead (3-5s). kaleido dependency also heavier to install. Proven 2026-07-16.
- **S/R levels: less is more.** User rejected charts with 6+ S/R levels. Max 2-3 per side, labeled cleanly. Clutter kills readability on mobile. Focus on levels NEAR current price. Proven 2026-07-16.
- **chart_pro.py is the current standard.** `/root/trading/scripts/chart_pro.py` — matplotlib-based, 180 DPI, dark theme, EMA 20/50/200, bias pill, zone shading, RSI panel, bottom verdict banner. Use this for all Telegram chart delivery. Replaces older xauusd_chart_pdf.py for signal charts. Proven 2026-07-16.
- **WEALTH Gold Dashboard exists.** Live at arif-fazil.com/wealth/gold with superior quality (technical focus, world context, decision gate). Don't rebuild — use existing. API at /wealth/gold/api/gold/*. Proven 2026-07-14.
- **Chart zone shading matters.** User feedback: profit zone (green) + risk zone (red) shading makes trade setup instantly visible. Always include for signal charts. Proven 2026-07-16.
- **Bias pill in header.** BULLISH/BEARISH/NEUTRAL badge + confidence % in chart header gives instant context. Add to all signal charts. Proven 2026-07-16.

## Zoomed Chart Mode

When user says "zoom in" — reduce candle count for bigger, clearer candles.

**Default:** 72 candles (3 days of H1). Good for overview.
**Zoomed:** 36 candles (1.5 days of H1). Good for detail.

```python
# Zoomed view
recent = df.tail(36).copy().reset_index()  # 36 candles instead of 72
```

**Effect:** Candles are 2x bigger, easier to read formations, S/R interactions more visible.

**Tradeoff:** Less context (can't see older trends). Use zoomed for signal confirmation, full for trend analysis.

## Voice Note Delivery for Trading Explanations

When explaining trading concepts to non-technical users (e.g., long vs short confusion, daily chart briefings to retail traders like Abang Sado Syed):

1. **Write the text first** — clear, simple BM-English mix
2. **Generate voice with edge-tts** — `ms-MY-OsmanNeural` for Nusantara voice
3. **Deliver BOTH** — text for reading, voice for listening

```bash
# Write explanation
cat << 'EOF' > /tmp/explain.txt
Abang Sado, ni Hermes. [explanation in simple BM]
EOF

# Generate voice
edge-tts --voice ms-MY-OsmanNeural --text "$(cat /tmp/explain.txt)" --write-media /tmp/explain.ogg
```

**Rules (proven 2026-07-18 with Abang Sado):**
- Keep it under **90 seconds** of speech (~220 words). Retail traders listen on the move.
- Use simple language — no jargon translations to BM
- **Spell out big numbers in BM**: `$4,023` → "empat ribu dua puluh tiga dolar" — single-thousands OK
- **Keep TA terms in English**: `support`, `resistance`, `break`, `EMA200`, `RSI` — BM translators sound forced and retail traders already know the English terms
- **Lead with the story** (what happened — drop/recovery), then the level (where to act), then the verdict (what to do)
- **End with action**: "SABAR — tunggu break $4019 atau $4026" beats "monitor the levels"
- End with clear action item

Full briefing checklist for retail-trader voice notes: `references/gold-api-internal-data-shape.md` §Voice note for retail traders. Voice config + Penang-voice limitations: see `tts-edge-fallback` skill.

## Live Implementation

**Working script:** `/root/trading/scripts/xauusd_chart_pdf.py`
- Fetches XAUUSD via yfinance (GC=F), calculates EMA 20/50, RSI 14, S/R
- Renders dark-theme H1 candlestick chart with overlays
- Outputs landscape A4 PDF with reportlab
- Usage: `python3 xauusd_chart_pdf.py [--output path.pdf]`
- Used by daily briefing cron (job `2258f1b3fa0e`)

## References

- `references/multi-timeframe-structure.md` — Daily/4H/1H layout patterns
- `references/canvas-pdf-wrapping.md` — reportlab canvas-based PDF wrapping (proven)
- `references/indicator-calculations.md` — EMA, RSI, S/R, candlestick patterns, signal logic (matches gold_engine.py)
- `references/tradingview-lightweight-charts-webapp.md` — Live interactive chart web app pattern (TradingView lightweight-charts + Node.js API + Caddy deploy)
- `references/gold-api-internal-data-shape.md` — gold-api `:3456` federation endpoint shape, align-by-timestamp for EMA/RSI, Caddy HTTPS-upgrade gotcha, voice-briefing checklist (proven 2026-07-18)
- `references/cron-chart-alert-delivery.md` — pattern for automated chart alerts via cron (silent watchdog, chart+message delivery, matplotlib `$` fix)
- `templates/gold_signal_chart.py` — Proven single-chart template (dark theme, EMA, zones)
- `templates/xauusd_signal_pdf.py` — Complete XAUUSD H1 chart+PDF pipeline (fetch→indicators→S/R→signal→render→PDF)

## Web-Based Live Charts (TradingView Lightweight-Charts)

For interactive, auto-refreshing live charts (not static PDF), use TradingView lightweight-charts library.
Full pattern: `references/tradingview-lightweight-charts-webapp.md`

**Proven deployment:** https://arif-fazil.com/wealth/gold (Node.js API on port 3456, systemd `gold-api.service`, deployed 2026-07-14)

Key differences from PDF charts:
| | PDF (matplotlib/reportlab) | Web (lightweight-charts) |
|---|---|---|
| Output | Static image/PDF | Interactive browser chart |
| Refresh | Manual (new PDF) | Auto (60s interval) |
| Interactivity | None | Zoom, pan, crosshair |
| Deploy | File/attachment | URL (e.g., /wealth/gold) |
| Best for | Daily briefings, signals | Live monitoring, dashboards |

## Related Skills

- `scientific-pdf-generation` — parent skill for PDF rendering (reportlab/weasyprint)
- `news-research-briefing` — research methodology for gathering market data
- `capital-market` (WEALTH MCP) — live FX/commodity data
- `syedos` — Abang Sado trading companion (APEX 5, blindspots, full system)
