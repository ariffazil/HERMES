# Portfolio Optimization Forge Results — 2026-07-06

## Test Setup

5 Bursa assets: PETRONAS, TENAGA, MAYBANK, CIMB, PBBANK
Expected returns: μ = [0.12, 0.08, 0.10, 0.06, 0.14]
Covariance matrix: Σ (5×5, positive definite)

## Agent A: Markowitz vs Equal-Weight ❌ KILL

| γ (risk aversion) | Sharpe | Δ vs Baseline |
|---|---|---|
| Baseline (equal weight) | 0.9285 | — |
| γ=0.5 (aggressive) | 0.7431 | -20.0% |
| γ=1.0 (moderate) | 0.8071 | -13.1% |
| γ=5.0 (very conservative) | 0.9316 | +0.3% |

**Why:** Equal-weight is near-optimal for correlated Bursa assets. Markowitz concentrates into 2-3 names, increasing variance faster than return.

## Agent B: Kelly vs Fixed 1% Risk ✅ FORGE (conditional)

| Asset | Kelly f* | Monte Carlo Kelly | Monte Carlo Baseline | Winner |
|---|---|---|---|---|
| MAYBANK (60% win) | 33% | 673x | 52x | Kelly 13x |
| PETRONAS (55% win) | 27% | 274x | 67x | Kelly 4x |
| CIMB (40% win) | 12% | 8x | 29x | Baseline 3.6x |
| PBBANK (52% win) | 28% | 1983x | 238x | Kelly 8x |

**Why:** Kelly wins huge when edge is real, loses hard when edge is weak. That's the point — it sizes to edge quality.

**Condition:** Only forge if WEALTH can estimate win rate from historical trade data.

## Agent C: Robust/Chance-Constrained ❌ KILL

| Method | CVaR(95%) | Δ vs Baseline |
|---|---|---|
| Baseline (equal weight) | 0.1307 | — |
| Robust γ=0.05 | 0.3393 | +159.6% WORSE |
| Chance-constrained 3% | 0.1290 | -1.3% better |

**Why:** Robust optimization concentrates 100% into PBBANK, destroying diversification. Chance-constrained barely moves the needle.

## The Zen

> The best optimization is knowing when NOT to optimize.
> Equal-weight is the Zen of portfolios — no false precision, no overfitting.
> Kelly is the one exception: when edge is real, sizing matters.

## Implementation

Kelly was forged into `wealth_stock_analysis(mode="kelly")`:
- Half-Kelly default (kelly_fraction=0.5)
- APEX W organ mapping (Execution — work done by optimal sizing)
- C_dark detection for bad inputs (low win rate, terrible risk/reward, insufficient data)
- Closed-form solution via scipy — no solver needed
