# Red/Blue Team Position Analysis

Proven 2026-07-21 — multi-asset portfolio review for Syed (Brent, Gold, NatGas).

## When to Use

When reviewing active positions or proposed trades. Run BEFORE delivering analysis to Syed. Every trade gets attacked AND defended before a verdict is reached. This is not optional — the system says "agent sayang Syed lebih dari Syed sayang diri sendiri." The Red Team is how it proves it.

## Pattern

```
For each position:
  ┌─────────────────┐
  │ 1. Live probe   │ ← curl ticker + signal_v2 + apex APIs
  └────────┬────────┘
           │
     ┌─────┴─────┐
     │           │
  ┌──┴──┐   ┌───┴──┐
  │ RED │   │ BLUE │
  │ TEAM│   │ TEAM │
  └──┬──┘   └──┬───┘
     │          │
     └────┬─────┘
          │
   ┌──────┴──────┐
   │  ⚖️ VERDICT │ ← trail SL / hold / close / SABAR
   └─────────────┘
```

## Red Team — Attack Checklist

For each position, ask:

1. **Technical exhaustion** — RSI >70 (overbought) or <30 (oversold)? Is it at resistance/support?
2. **At a ceiling/floor** — Is price literally scraping an S/R level from the ticker API?
3. **Engine disagrees** — What does `signal_v2` confidence say? If <0.5, why is position open?
4. **Reversal drawdown** — If price reverses 2%, what happens to P&L? Is the psychological hit acceptable?
5. **Macro headwind** — DXY/US10Y/VIX direction? Any calendar event risk?

Format: Numbered list with 🚨 for critical, ⚠️ for warning.

## Blue Team — Defend Checklist

For each position, ask:

1. **EMA alignment** — EMA20 > EMA50 > EMA200 all pointing same direction? = trend intact.
2. **R:R math** — Risk dollars vs reward dollars. Even at low win rate, does math work?
3. **SL cushion** — How far is current price from SL? Wide enough to survive noise?
4. **Fundamental bid** — Is there structural demand? Geopolitical premium? Supply constraint?
5. **Entry quality** — Was this a pullback buy in trend? Breakout? How sound was the original thesis?

Format: Numbered list with ✅ for strong points.

## Verdict Output

Map to one of:

| Verdict | Action |
|---------|--------|
| **TRAIL** | Move SL tighter → lock profit, let run |
| **HOLD** | No change, thesis intact |
| **CLOSE** | Exit now, take profit or cut loss |
| **SABAR** | Wait, no entry (for watchlist items) |

Always include concrete numbers: new SL price, locked profit amount, distance to TP.

## Multi-Asset Portfolio Format

When reviewing multiple assets simultaneously:

```
┌─────────────────────────────────────────────────────┐
│ PORTFOLIO DASHBOARD — [date] [time] MYT             │
├──────────┬──────────┬──────────┬────────────────────┤
│ Position │ Entry    │ P&L      │ Key Metrics        │
├──────────┼──────────┼──────────┼────────────────────┤
│ ❶ Brent  │ $88.44   │ +$269    │ RSI 82.6, EMA ↑   │
│ ❷ Gold   │ (none)   │ —        │ RSI 51.7, SABAR   │
│ ❸ NatGas │ (none)   │ —        │ RSI 43.9, WATCH   │
└──────────┴──────────┴──────────┴────────────────────┘
```

## Live Data Sources

```bash
# Gold ticker
curl -s http://localhost:3456/api/ticker | python3 -m json.tool

# Brent ticker
curl -s http://localhost:3457/api/ticker | python3 -m json.tool

# NatGas ticker
curl -s http://localhost:3458/api/ticker | python3 -m json.tool

# Macro
curl -s http://localhost:3456/api/macro | python3 -m json.tool
```

All APIs return: `symbol, price, change, changePct, rsi, rsiState, signal, confidence, ema20/50/200, emaTrend, support[], resistance[], pivot, timestamp`.

## Chart Delivery Rules (CRITICAL)

See `syedos` skill for the **CHART LABEL PITFALL** — labels and annotations MUST NOT block candlestick bodies. All data goes in a right-side legend panel. Pattern proven after user rejection ("Weii hang tutup price dengan label. Buat balik.").

## Pitfalls

- **Don't skip the Red Team** — even when P&L is green. A position in profit can still be a bad hold.
- **RSI overbought in a trend is not an automatic close** — trend can stay overbought. Factor it, don't panic.
- **"SABAR is a position"** — silence is a signal. Don't force a trade when engine confidence is low.
- **Chart labels must not block candles** — separate delivery rule (see above).
