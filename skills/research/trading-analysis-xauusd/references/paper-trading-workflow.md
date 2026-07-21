# Paper Trading Cron Architecture

Proven 2026-07-20. Arif assigned $10K virtual paper trading for 1 month.

## Architecture: Brain → Hands

Two-cron chain, unified under one ledger:

| Cron | Schedule | Deliver | Role |
|------|----------|---------|------|
| `b6361747dfae` 🧠 Morning Analysis | 8am M-F | `local` | Portfolio review + market scan + setup ranking |
| `b98bd448eaf3` 🔥 Zen Executor | Every 3h | `origin` (SADO) | Reads morning context. Executes. Silent unless trade. |

Chain: Morning Analysis output → `context_from` → Zen Executor.

## Ledger: `/root/paper_trading/ledger.md`

Single source of truth. Format: Account Summary, Live Prices, Trade Log, Open Positions, Signal Watchlist. Update on EVERY trade with timestamp + rationale.

## Paused/Removed Noise

| Cron | Was | Action |
|------|-----|--------|
| `adbe4006fba5` | Hourly price alert → SADO | PAUSED |
| `8037961a7422` | 15-min position monitor → SADO | PAUSED |
| `7f1468e5e66a` | Daily gold signal 9am | REMOVED — absorbed |
| `2258f1b3fa0e` | Gold signal briefing 8am | REMOVED — absorbed |

## Zen Law

IF NO TRADE → output "." (single period). Nothing else.
IF TRADE → format: `🔥 [ACTION] [INSTRUMENT] @ $PRICE | P&L: +/-$XXX | Balance: $XXX`

## Key Lesson: Proactivity Over Paralysis

Arif's explicit correction (2026-07-20): "Hang pandai2 LA fikir. Hang agentic intelligence kan."

Agent was waiting for "perfect rejection wick" at $4,000 before entering. Arif called it out as passive/robotic. Consolidation at key level IS confirmation. Default = evaluate and act. Only defer when genuinely ambiguous.

## Ledger Format (Full Template)

File: `/root/paper_trading/ledger.md`. Must include these sections:

- **Account Summary table** — Balance, Equity, Open P&L, Closed P&L, Trade count
- **Live Prices** — Current snapshot at entry time
- **Trade Log table** — Every trade: #, Date, Type (MARKET/LIMIT/STOP), Instrument, Direction, Entry, Exit, Risk ($), P&L ($), R:R, Notes (rationale)
- **Open Positions** — Per position: Entry, SL, TP1/TP2, Risk amount, R:R, Rationale
- **Capital Allocation** — Total, Risk Reserved, Available, Positions count
- **Analysis** — Current reads per instrument, signal watchlist

Update on EVERY trade (entry, close, adjust). Last line: timestamp.

## Decision Framework

### When to ENTER
- Price tests key support/resistance with consolidation (consolidation IS confirmation)
- Macro context aligns with technical setup
- R:R ≥ 1:1.5 achievable
- Capital free (≤2 positions open, one slot remaining)

### When to EXIT
- SL hit → close immediately, log P&L
- TP1 hit → close half, move SL to breakeven
- TP2 hit → close remainder
- Structure breaks → exit regardless of P&L

### When to STAY OUT
- News event imminent → wait
- No clear level within reach
- R:R below 1:1.5
- 3 positions already open

## Price Sources (Priority Order)

1. Arif's dashboard (arif-fazil.com/gold/) — XAUUSD, MYR rates, macro context
2. hound smart_search — oil, gas, secondary confirm
3. WEALTH organ capital_market — requires authenticated arifOS session; fallback to web

## Noisy Crons to Silence on Setup

| Job ID | Name | Action |
|--------|------|--------|
| `adbe4006fba5` | Hourly price alert | PAUSE |
| `8037961a7422` | 15-min position monitor | PAUSE |
| `7f1468e5e66a` | Daily gold signal 9am | REMOVE — absorbed into unified morning analysis |
| `2258f1b3fa0e` | Gold signal briefing 8am | REMOVE — absorbed into unified morning analysis |
