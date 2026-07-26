# Two-Proportion Z-Test Without scipy

Used in arifOS audit/fatigue modules to compare rates between groups
(e.g., nighttime vs daytime approval rates) without pulling in scipy.

## Abramowitz & Stegun 7.1.26 — Standard Normal CDF

High-precision approximation sufficient for p-value computation.
Maximum absolute error < 7.5e-8.

```python
import math

def _normal_cdf(x: float) -> float:
    """Abramowitz & Stegun 7.1.26 standard normal CDF approximation."""
    if x < 0:
        return 1 - _normal_cdf(-x)
    b = [0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429]
    t = 1 / (1 + 0.2316419 * x)
    poly = t * (b[0] + t * (b[1] + t * (b[2] + t * (b[3] + t * b[4]))))
    return 1 - 0.3989422804014327 * math.exp(-0.5 * x * x) * poly
    # 0.3989422804014327 = 1/√(2π)
```

## Two-Proportion Z-Test

Two-tailed p-value comparing proportions p1 and p2 from samples of size n1 and n2.
Returns None when either group has < 5 samples (normal approximation unreliable).

```python
def _two_proportion_z(n1: int, p1: float, n2: int, p2: float) -> float | None:
    if n1 < 5 or n2 < 5:
        return None
    pp = (n1 * p1 + n2 * p2) / (n1 + n2)
    if not (0 < pp < 1):
        return None
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    return 2 * (1 - _normal_cdf(abs(p1 - p2) / se))
```

## Usage in ReviewConsistencyScorer

```python
for outcome in ("approved", "rejected", "amended"):
    dt_rate = daytime.get(outcome, 0) / dt_total
    nt_rate = night.get(outcome, 0) / nt_total
    p_val = _two_proportion_z(dt_total, dt_rate, nt_total, nt_rate)
    if p_val is not None and p_val < 0.05:
        # Flag as significant drift
```

## Minimum Sample Thresholds

- Use ≥10 daytime samples and ≥5 nighttime samples before running the test.
- Below threshold: return `{"flagged": False, "reason": "insufficient_data"}`.
