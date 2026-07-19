# APEX × WEALTH Optimization Upgrades (2026-07-06)

Session: Testing whether APEX Pillar IV (Mathematical Optimization Foundation) improves WEALTH tools. Three upgrades forged in-place to `internal/monolith.py`.

## Upgrades Applied

### 1. Robust EVOI (`wealth_evoi_compute`)

**What:** Added `robust: bool = False` parameter. When True, computes EVOI under uncertainty ranges (prior ± 0.10, posterior ± 0.15) across 50×50 grid. Returns worst-case EVOI, CVaR(5%), and robust_regret.

**Key fields added to envelope:**
- `robust_analysis.expected_evoi_musd` — mean across samples
- `robust_analysis.worst_case_evoi_musd` — minimum across samples
- `robust_analysis.cvar_5pct_musd` — conditional value at risk
- `robust_analysis.robust_regret_musd` — gap between expected and worst-case
- `robust_verdict` — ROBUST_SEAL / ROBUST_SABAR / ROBUST_VOID

**Backward compatible:** `robust=False` (default) produces identical output.

### 2. Nash Multi-Factor Stock Scoring (`wealth_stock_analysis`, mode="nash_multi_factor")

**What:** New mode that computes Nash bargaining product across factors. Compares Nash (no trade-offs) vs additive (linear trade-offs). Flags divergence >5%.

**Key fields:**
- `nash_score` — geometric mean: exp(Σ w_i · ln(f_i))
- `additive_score` — arithmetic mean: Σ w_i · f_i
- `trade_off_detected` — True if Nash and additive diverge >5%
- `method` — "Nash bargaining product (Nash 1950) — APEX Pillar IV"

### 3. Scar Accumulation (`wealth_survival_engine`, `scar_history` param)

**What:** Added `scar_history: list[dict] | None = None` parameter. Tracks loss events, builds forbidden zones, escalates boundary verdict when scar pressure > 0.3.

**Key fields:**
- `scar_pressure` — fraction of periods with losses
- `constraint_count` — number of >5% loss events
- `forbidden_zones` — list of flagged allocations

## Solver Environment

- **Pyomo 6.10.1** installed, IPOPT available
- **GLPK** (`glpsol`) and **CBC** installed via apt
- Agents need packages pre-installed — they can't handle apt permission prompts

## Findings

- Equal-weight portfolios are near-optimal for correlated assets (Markowitz concentrates risk)
- Kelly criterion wins huge when edge is real (13x on 60% win rate), loses when edge is weak
- Robust optimization with L1 penalty destroys diversification — counterproductive without strong views
- Nash product prevents zero-collapse: any factor at zero = total collapse (feasibility, not optimality)
- Scar accumulation is cutting-plane optimization: feasible region shrinks monotonically as scars accumulate
