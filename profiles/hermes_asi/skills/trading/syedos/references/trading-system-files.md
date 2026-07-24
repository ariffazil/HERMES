# Trading System Files — Complete Inventory

> Created: 2026-07-14. Phase 1 companion mode.

## Directory Structure

```
/root/trading/
├── config/
│   └── trading_spec.json          # Master config (risk, sessions, confluence rules)
├── scripts/
│   ├── gold_engine.py             # Signal generation engine
│   ├── price_alert.py             # Real-time price monitoring
│   ├── journal_engine.py          # Trade tracking + statistics
│   ├── weekly_report.py           # Weekly Telegram report generator
│   └── xauusd_chart_pdf.py        # Candlestick chart PDF generator
├── journal/
│   ├── signals.jsonl              # Raw signal log (auto-appended)
│   └── trade_log.json             # Trade outcomes (manual entry)
├── signals/                       # Legacy signal modules
├── strategies/                    # Legacy strategy files
│   └── xauusd_rsi_basic.py
├── GOVERNANCE/                    # Governance docs
├── config/
│   └── oanda.env                  # OANDA credentials (Phase 2+)
└── lib/                           # Python venv (packages installed here)
```

## Script Details

### gold_engine.py
**Purpose:** Core signal generation with confluence validation.
**Data source:** Yahoo Finance (GC=F futures, yfinance package)
**Indicators:** EMA 20/50, RSI 14, RSI divergence, candlestick patterns (hammer, shooting star, engulfing, doji), S/R from pivot highs/lows
**Macro:** DXY index, US 10Y Treasury yields
**Filters:** Session (London/NY only), news window (NFP/CPI/FOMC), ≥2 confluence required
**Output:** JSON signal object or Telegram-formatted briefing

### price_alert.py
**Purpose:** Silent watchdog — alerts only when something notable happens.
**Checks:** Price near S/R (within 0.3%), EMA crossover, RSI extreme (<30 or >70), candlestick pattern formed
**Behavior:** Empty stdout = nothing to report. Non-empty = deliver to Telegram.
**Session-aware:** Silently exits outside London/NY hours.

### journal_engine.py
**Purpose:** Track trade outcomes and calculate performance metrics.
**Commands:**
- `--sync` — Import signals from signals.jsonl into trade_log.json
- `--log --signal_id <id> --outcome <win|loss|breakeven> --pnl <amount>` — Log outcome
- `--stats` — Full statistics (win rate, profit factor, avg RR, max drawdown, setup breakdown, hourly analysis)
- `--report [--period weekly|monthly|all]` — Markdown report with recommendations
- `--list [--open]` — List all or pending trades

### weekly_report.py
**Purpose:** Generate Telegram-ready weekly performance summary.
**Command:** `python3 weekly_report.py --telegram`
**Output:** Compact format with total trades, wins, losses, win rate, avg RR, best/worst trade, recommendations.

### xauusd_chart_pdf.py
**Purpose:** Professional candlestick chart PDF for daily briefings.
**Command:** `python3 xauusd_chart_pdf.py [--output path]`
**Specs:** Dark theme (#0d1117), H1 candles, EMA 20/50 overlay, S/R lines, RSI panel, pattern markers, signal zones. Landscape A4.

## Config Parameters (trading_spec.json)

| Key | Value | Notes |
|---|---|---|
| instrument | XAUUSD | Phase 1: single instrument |
| ema_fast / ema_slow | 20 / 50 | Standard crossover |
| rsi_period | 14 | Standard RSI |
| min_confluence | 2 | F3 WITNESS: single indicator = breach |
| max_risk_pct | 1.0 | Per trade |
| min_rr_ratio | 2.0 | Minimum R:R |
| sessions | london, ny | Asian blocked |
| skip_events | NFP, CPI, FOMC, FOMC_MINUTES | 30min before, 60min after |
| briefing_time | 08:00 MYT | Daily signal delivery |

## Dependencies

Installed in `/root/trading/lib/` venv:
- yfinance — market data
- pandas — data processing
- numpy — calculations
- ta — technical analysis (backup)
- reportlab — PDF generation
- matplotlib — chart generation

## Cron Job IDs (for reference)

| ID | Name | Schedule |
|---|---|---|
| 2258f1b3fa0e | Gold Signal Briefing | 0 8 * * 1-5 |
| 3050000c14b6 | Price Alert | */30 8-20 * * 1-5 |
| 7269e5cfee2e | Weekly Report | 0 20 * * 5 |
