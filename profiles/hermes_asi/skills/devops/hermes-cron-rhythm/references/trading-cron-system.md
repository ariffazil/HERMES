# Trading Cron System — Delivery & Script Reference

## Delivery Targets

| Target | Telegram ID | Use |
|--------|-------------|-----|
| Arif DM | `telegram:267378578` | Personal briefs, daily news |
| AAA Group | `telegram:-1003753855708` | Machine alerts, system health |
| SADO Group | `telegram:-1003815535761` | ALL trading signals, price alerts, position monitors, weekly reports |
| Syed DM | `telegram:1042200555` | Personal trading alerts |

**Rule:** ALL trading signals go to SADO group. Zero trading noise in AAA or DM.

## Scripts

All at `/root/trading/scripts/`. Config at `/root/trading/config/trading_spec.json`.

### price_alert.py

```bash
cd /root/trading && python3 scripts/price_alert.py --check
```

- Fetches XAUUSD via yfinance (GC=F with XAUUSD=X fallback)
- Calculates EMA20/50, RSI14, S/R pivots, candlestick patterns
- 4 alert conditions: near S/R (0.3%), EMA cross, RSI 30/70 cross, candle pattern
- **Empty stdout** = no conditions met → cron delivers nothing (silent)
- **Non-empty stdout** = Telegram-ready alert text
- Session-aware: exits silently outside London/NY hours
- Tested: detects RSI overbought/oversold, near support/resistance

### chart_pro.py

```bash
cd /root/trading && python3 scripts/chart_pro.py --json 2>/dev/null
```

- Generates professional dark-theme candlestick chart (PNG, 180 DPI)
- Output: `/tmp/xauusd_chart.png`
- Used by agent-driven alerts — agent sends chart image first, then text explanation

### weekly_report.py

```bash
cd /root/trading && python3 scripts/weekly_report.py --telegram
```

- Reads journal from `/root/trading/journal/trade_log.json`
- Calculates: win rate, avg RR, profit factor, max drawdown, setup breakdown
- `--telegram` flag = compact format for delivery
- `--save` flag = write to dated file

## Cron Wrapper Pattern

When `no_agent: true`, the `script` field expects a FILE PATH in `~/.hermes/scripts/`. Shell commands don't work.

**Wrong:** `script: "cd /root/trading && python3 scripts/price_alert.py --check"`
**Right:** Create `/root/.hermes/scripts/price-alert.sh`:

```bash
#!/bin/bash
# XAUUSD Price Alert — wrapper for cron
cd /root/trading && python3 scripts/price_alert.py --check 2>/dev/null
```

Then: `script: "price-alert.sh"`

## Agent-Driven Alert Pattern (XAUUSD Price Alert)

For alerts that need LLM context (explanation, chart interpretation), convert from `no_agent` script to agent-driven:

1. Remove the old `no_agent` job (can't switch `no_agent` via update)
2. Create new job WITHOUT `no_agent` and WITHOUT `script`
3. Set `skills: ["daily-trading-signal-briefing"]` for trading context
4. Prompt instructs agent to: run price_alert.py, check if output is empty (stay silent if so), generate chart, deliver chart + human-language explanation

**Key difference:** `no_agent` delivers script stdout verbatim. Agent-driven lets the LLM add meaning, context, and chart interpretation in human language.

## Known Cron Jobs (trading) — Updated 2026-07-16

| Job ID | Name | Schedule | Delivery | Type |
|--------|------|----------|----------|------|
| adbe4006fba5 | XAUUSD Price Alert | every hour Mon-Fri | SADO | agent-driven LLM+chart |
| 2258f1b3fa0e | Gold Signal Briefing | 08:00 Mon-Fri | SADO | LLM + chart |
| 7f1468e5e66a | XAUUSD Daily Gold Signal | 09:00 Mon-Fri | AAA | LLM |
| 8037961a7422 | Trading Position Monitor | every 15min 07:00-23:00 Mon-Fri | SADO | agent-driven (red news aware) |
| 7269e5cfee2e | Weekly Trading Report | Fri 20:00 | AAA | LLM |

All deliver to SADO group (`telegram:-1003815535761`) except XAUUSD Daily (AAA group).

## Gold API Endpoints (replaces direct yfinance calls)

```bash
curl -sf localhost:3456/api/gold/apex       # market intelligence
curl -sf localhost:3456/api/gold/signal_v2   # engine_v2 signal + sizing
curl -sf localhost:3456/api/gold/calendar    # ForexFactory USD events
curl -sf localhost:3456/api/gold/ticker      # quick price/RSI/EMA
curl -sf localhost:3456/api/gold/macro       # DXY, US10Y, VIX, GSR
```

## Red News Awareness (Position Monitor)

The position monitor checks `/api/gold/calendar` for approaching high-impact USD events:
- **T-15 min:** Critical alert — "🚨 [event] DALAM 15 MINIT — TUTUP POSITION"
- **T-2 hrs:** Warning — "⚠️ [event] dalam X minit — Jangan buka position baru"
- **T-6 hrs:** Notice — "📅 [event] dalam Xj Xm — Hati-hati"

Full red news rules: `references/red-news-impact.md`
