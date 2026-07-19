# Gold API (`:3456`) — Federation-Internal Data Shape

Internal quick-reference for hitting the federation-internal gold API at `localhost:3456/api/gold/*` (the `gold-api` Node.js service feeding the `/wealth/gold/` dashboard). **Different shape than yfinance** — different alignment code.

## Endpoints (live, confirmed 2026-07-18)

| Endpoint | Shape | Used for |
|---|---|---|
| `GET /api/gold/history?interval=1h&period=5d` | `{"candles": [...], "ema20": [...], "ema50": [...], "ema200": [...], "rsi": [...]}` | Render chart |
| `GET /api/gold/ticker` | `{symbol, price, change, changePct, rsi, rsiState, ema20, ema50, ema200, emaTrend, support[], resistance[], pivot}` | Header + S/R |
| `GET /api/gold/levels` | `{support_1h[], resistance_1h[], support_daily[], resistance_daily[], pivot}` | Levels |
| `GET /api/gold/signal_v2` | `{signal: {direction, strength, confidence, verdict, judge_reason, ...}, regime: {regime, confidence, price, ema_*, rsi}, zones: {buy_zone, sell_zone}}` | Verdict + regime badge |
| `GET /api/gold/apex` | `{apex: {A, P, E, X, Phi}, G, C_dark, dS, state, direction, momentum, ...}` | Internal APEX score (omit for retail briefings) |
| `GET /health` | `{status: "ok"}` | Liveness probe |

## Critical Data-Shape Differences (the gotcha)

**Candles are flat OHLCV dicts. EMAs and RSI are LIST-OF-DICTS keyed by unix timestamp.**

```json
// /api/gold/history candles[i]:
{
  "time": 1783915200,
  "open": 4068.1,
  "high": 4068.1,
  "low": 4057.8,
  "close": 4066.3,
  "volume": 0
}

// /api/gold/history ema20[i]:
{"time": 1783915200, "value": 4066.3}
```

**You CANNOT zip them by index** — they may have different lengths (RSI starts after 14 periods; EMA200 may be NaN early). You MUST align by timestamp.

## Working alignment snippet (proven 2026-07-18)

```python
import urllib.request, json

def fetch(endpoint):
    with urllib.request.urlopen(f"http://localhost:3456{endpoint}") as r:
        return json.loads(r.read())

hist = fetch("/api/gold/history?interval=1h&period=5d")
candles = hist['candles']  # [{time, open, high, low, close, volume}]

def align(series):
    """Align [{time, value}] series to candle indices by timestamp."""
    out = [None] * len(candles)
    candle_times = {c['time']: i for i, c in enumerate(candles)}
    for pt in series:
        if pt['time'] in candle_times:
            out[candle_times[pt['time']]] = pt['value']
    return out

ema20  = align(hist.get('ema20',  []))
ema50  = align(hist.get('ema50',  []))
ema200 = align(hist.get('ema200', []))
rsi    = align(hist.get('rsi',    []))

# Plot: skip None entries — matplotlib draws line through gaps with gaps
ax.plot(xs, ema20, color='#3b82f6', linewidth=1.0, label='EMA 20')
# Bar (RSI) — set bar height = 0 for None days to avoid gaps
rsi_color = ['#22c55e' if (v is not None and v < 30)
             else '#ef4444' if (v is not None and v > 70)
             else '#3b82f6' if v is not None else '#0d0d1a'
             for v in rsi]
```

**Symptom if you forget align-by-time:**
```
TypeError: unhashable type: 'dict'
# or matplotlib crashes trying to plot dict values.
```

## Chart recipe (matches WEALTH gold site visual identity)

| Element | Style |
|---|---|
| Background | `#07070d` (matrix dark) / `#0d0d1a` (panels) |
| Bull candle | `#22c55e` filled body |
| Bear candle | `#ef4444` filled body |
| EMA 20 | `#3b82f6` 1.0pt |
| EMA 50 | `#f59e0b` 1.2pt |
| EMA 200 | `#c9a84c` 1.5pt (slow = gold) |
| Support zone | `#22c55e` dashed + shaded band α=0.08 |
| Resistance zone | `#ef4444` dashed + shaded band α=0.08 |
| Current price | `#c9a84c` solid 1.0pt |
| RSI bars | colored by zone (green<30, red>70, blue neutral) |
| Y-margin | `(price_max - price_min) * 0.08` |
| DPI | 120 for one-shot, 150 for daily cron |

## Caddy HTTPS Gotcha (browser tool failure, proven workaround)

`https://gold.arif-fazil.com/` resolves fine in real browsers. But when verifying
the dashboard locally via the `browser_navigate` tool, it fails:

```
Navigation failed: net::ERR_SSL_PROTOCOL_ERROR
# on http://localhost/gold/  AND  http://127.0.0.1/gold/
```

Caddy's localhost vhost forces HTTPS upgrade for everything. `browser_navigate`
respects this and refuses to load the HTTP version.

**Don't fight it.** Render server-side from the JSON API instead — `:3456/api/gold/*`
returns JSON that matplotlib consumes directly:

```python
# Skip the browser entirely. Fetch → plot → save → MEDIA: send.
import urllib.request, json
import matplotlib.pyplot as plt
# ... render code as above ...
plt.savefig('/tmp/xauusd_latest.png', dpi=120, facecolor='#07070d')
```

This is faster (one HTTP call to JSON vs. full Chromium boot), produces zero Caddy noise,
and the chart looks identical to the web one.

## Voice note for retail traders (matches tts-edge-fallback §Trading/Analysis)

When briefing someone like Syed (retail XAUUSD trader) who's not a TA expert:

1. **Don't quote S/R levels in numbers — say "support"/"resistance" in English, keep BM for surrounding prose.** BM traders expect jargon to stay English; rewriting "support" → "sokongan" sounds forced.
2. **Spell out big numbers in BM:** `$4,023` → "empat ribu dua puluh tiga dolar". Single thousands is OK (`"empat ribu"`).
3. **Lead with the drop/recovery story** (what happened), then the level (where to act), then the verdict (what to do).
4. **End with action:** "SABAR — tunggu break $4019 atau $4026" beats "monitor the levels".
5. **Cap at ~90 seconds** of audio per brief. Keep it conversational, not lecture.
6. **Generate via `edge-tts` (ms-MY-OsmanNeural, --rate="+5%")**, deliver as `MEDIA:/path/to/voice.mp3`. Saves to `/root/forge_work/<YYYY-MM-DD>/`.

See `tts-edge-fallback` skill for full voice config and Penang-voice limitations.

## When to use this API vs. yfinance/MT5

| Source | When |
|---|---|
| **gold-api `:3456`** | Federation internal — briefing, cron charts, dashboard rendering. **Default for Arif-facing briefings.** |
| yfinance (`GC=F`) | Backup or external demo. Latency 15min. |
| MT5 Python | Real-time execution. Required for live trading, not for charts. |

The `:3456` API is the WEALTH federation's gold substrate — feeds `/wealth/gold/` site
the daily briefing cron (`adbe4006fba5`), and the position monitor. **Don't bypass it.**
