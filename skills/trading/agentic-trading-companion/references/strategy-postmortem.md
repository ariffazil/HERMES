# Strategy Post-Mortem (2026-07-16)

## What Failed (v1 backtest on real gold data)
- **786 trades, 43% win rate, PF 0.77, -62.5% return, 64.8% max DD**
- Root cause 1: P&L multiplier 100 instead of 1000 → lots 10× too large
- Root cause 2: Traded SIDEWAYS regime (441 trades, 40.8% win, -$4,452)
- Root cause 3: SL too tight (1× ATR) → noise stopped out 448 times

## What Worked (v2 optimized)
- **294 trades, 45.9% win rate, PF 1.19, +23.5% return, 16.8% max DD**
- Fix 1: Correct P&L multiplier (1000)
- Fix 2: Skip SIDEWAYS entirely
- Fix 3: Widen SL to 2× ATR
- Fix 4: 2× ATR trailing stop (profit engine)

## The 7 Configurations Tested

| # | Config | Trades | Win% | PF | Return | Max DD | Sharpe |
|---|--------|--------|------|-----|--------|--------|--------|
| 1 | Baseline (no filter) | 292 | 44.9 | 1.14 | 165.6% | 14.9% | 0.74 |
| 2 | **Trail 2x ATR** | **294** | **45.9** | **1.19** | **234.7%** | **16.8%** | **0.98** |
| 3 | RSI 45/55 | 136 | 45.6 | 1.10 | 65.1% | 15.4% | 0.58 |
| 4 | Zone strong (2+) | 142 | 46.5 | 1.06 | 30.8% | 11.0% | 0.36 |
| 5 | Zone very strong (3+) | 109 | 47.7 | 1.02 | 8.9% | 13.7% | 0.13 |
| 6 | 2% risk ❌ | 292 | 44.9 | 0.84 | -359% | 51.3% | -1.13 |
| 7 | SL 1.5x ATR | 331 | 46.2 | 1.02 | 35.9% | 27.6% | 0.13 |

## Key Insights
1. **Trailing stop = profit engine.** 65 TP hits ($11,273) + trailing exits catch big moves.
2. **2% risk kills.** Even profitable strategy → -359% with double risk.
3. **Wider SL > tighter SL.** 2× ATR SL: PF 1.19. 1.5× ATR SL: PF 1.02.
4. **RSI filter kills trade count.** 136 vs 292 trades, lower absolute return.
5. **Zone strength doesn't help enough.** Fewer trades, not enough PF improvement.
6. **Win rate ~45% is normal for trend-following.** Don't optimize for win rate — optimize for avg win/loss ratio.

## Regime Breakdown
- UPTREND: 185 trades, 44.9% win, +$1,567 (best absolute)
- DOWNTREND: 109 trades, 47.7% win, +$780
- SIDEWAYS: 0 trades (skipped) → saved $4,452 in losses

## The Fundamental Truth
The directional calls are RIGHT (trailing stop profitable). The issue was always entry timing and stop placement. Fix the execution layer, not the signal layer.
