# Backtest Methodology

## Test Protocol
1. Always use REAL data (yfinance GC=F), never synthetic
2. Run on multiple timeframes: 1h (primary), 4h (confirmation), 1d (trend)
3. Minimum 100 trades for statistical significance
4. Compare at least 3 configurations before selecting best

## What We Tested (2026-07-16)

### v1 (BROKEN): Multi-factor engine + wrong P&L
- 786 trades, 43% win rate, PF 0.77, **-62.5% return**
- Root cause: P&L multiplier = 100 (should be 1000) → lots 10× too large
- Also: traded SIDEWAYS (441 trades, 40.8% win, -$4,452)

### v2 (FIXED): Corrected P&L + trend-only
- Tested 7 configurations on 11,461 real hourly candles
- Best: 2× ATR trail → 294 trades, 45.9% win, PF 1.19, +23.5%

### Config Comparison

| Config | Trades | Win% | PF | Return | Max DD | Sharpe |
|--------|--------|------|-----|--------|--------|--------|
| Baseline (no filter) | 292 | 44.9% | 1.14 | 165.6% | 14.9% | 0.74 |
| **Trail 2x ATR** | **294** | **45.9%** | **1.19** | **234.7%** | **16.8%** | **0.98** |
| RSI 45/55 | 136 | 45.6% | 1.10 | 65.1% | 15.4% | 0.58 |
| Zone strong (2+) | 142 | 46.5% | 1.06 | 30.8% | 11.0% | 0.36 |
| Zone very strong (3+) | 109 | 47.7% | 1.02 | 8.9% | 13.7% | 0.13 |
| 2% risk ❌ | 292 | 44.9% | 0.84 | -359% | 51.3% | -1.13 |
| SL 1.5x ATR | 331 | 46.2% | 1.02 | 35.9% | 27.6% | 0.13 |

### Key Findings
1. **Trailing stop is the profit engine**: 65 TP hits = $11,273. Trail catches big moves.
2. **2% risk is account suicide**: Even with profitable strategy, leverage kills.
3. **Wider SL (2× ATR) beats 1.5×**: Fewer noise stops, better PF.
4. **RSI filter kills trade count**: 136 vs 292 trades, lower total return.
5. **Strong zones alone don't help**: Fewer trades, not enough PF improvement to compensate.

## Running a Backtest
```bash
python /root/trading/backtest/engine_v2.py \
  --data /root/trading/data/xauusd_1h.json \
  --output /root/trading/backtest/results/$(date +%Y%m%d).json \
  --equity 10000 \
  --risk 0.01
```

## Verification Checklist
- [ ] P&L multiplier = 1000 (not 100)
- [ ] Lot sizing: `risk / (sl_distance * 1000)`
- [ ] Minimum lot: `max(0.001, ...)` for backtest
- [ ] Warmup ≥ 210 bars
- [ ] Real data, not synthetic
- [ ] Manual P&L spot-check on 2-3 trades
