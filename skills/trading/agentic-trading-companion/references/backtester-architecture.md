# XAUUSD Backtester Architecture

Proven 2026-07-16. Complete walk-forward backtester at `/root/trading/backtest/engine.py`.

## Design Decisions

1. **Pure Python, no numpy** — EMA, swing detection, S/R clustering all in stdlib. Keeps it deployable anywhere.
2. **Walk-forward, no look-ahead** — All signals use data up to and including current bar only.
3. **S/R zones cached** — Recomputed every 20 bars (configurable) to avoid O(n²) swing detection.
4. **Position management in-loop** — Partial TP at 1R, trailing stop after 1R trigger, SL moved to breakeven.

## Regime Detection

```
UPTREND:   EMA20 > EMA50 > EMA200  → Buy dips to support/EMA
DOWNTREND: EMA20 < EMA50 < EMA200  → Sell rallies to resistance/EMA
SIDEWAYS:  EMAs tangled            → Buy support, sell resistance
```

## Entry Signal Logic

1. Compute S/R zones from recent swing highs/lows (lookback=60 bars, swing_lb=8)
2. Cluster nearby levels within 0.5% tolerance
3. Price touches zone (within 0.15%) → check confirmation candle
4. Confirmation: bullish/bearish close OR near EMA20 in trending regime
5. Enforce minimum 2R RR — if nearest S/R doesn't give 2R, use 2x SL distance as TP

## Position Sizing

```
lots = (equity * risk_pct) / (sl_distance * contract_size)
contract_size = 100 for XAUUSD (1 lot = 100 oz)
risk_pct = 0.01 (1% per trade)
max 3 concurrent positions
```

## Exit Management

| Exit | Trigger | Action |
|------|---------|--------|
| SL | Price hits initial stop | Full close |
| TP | Price hits target | Full close |
| Partial TP | 1R favorable excursion | Close 50%, move SL to BE+1 |
| Trailing SL | After 1R, trail at 0.3% step | Moves with price |

## Metrics Computed

- Win rate, avg RR, total return, max drawdown (absolute + %)
- Sharpe ratio (annualized, using 24-bar daily returns)
- Profit factor (gross profit / gross loss)
- Breakdown by regime and by exit reason
- Best/worst trade, avg bars held

## Common Pitfalls

- **Variable naming**: When destructuring OHLCV, use `price = bar["close"]` consistently. Don't mix `close` and `price` — causes NameError. (Bug hit 2026-07-16, two occurrences in entry signal logic.)
- **EMA warmup**: Need 200+ bars warmup before trading (EMA200 needs 200 bars to stabilize). Set warmup=210 minimum.
- **S/R clustering tolerance**: Too tight = too many zones (noise). Too loose = merged zones (missed entries). 0.5% works for gold's typical range.
- **Minimum 2R enforcement**: If nearest S/R only gives 1.5R, override to 2x SL distance. Don't let bad RR trades through.

## CLI Usage

```bash
python /root/trading/backtest/engine.py \
  --data /root/trading/data/xauusd_1h.json \
  --output /root/trading/backtest/results/h1_results.json \
  --equity 10000 \
  --risk 0.01 \
  --max-pos 3 \
  --warmup 210
```
