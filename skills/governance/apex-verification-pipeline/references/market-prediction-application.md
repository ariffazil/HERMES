# APEX Market Prediction Application

## Mapping APEX Primitives to Market State

The canonical APEX formula `G = A·P·E·X·Φ` maps to market prediction:

| Primitive | Market Meaning | Computation |
|-----------|---------------|-------------|
| **A** (Authority) | EMA alignment strength | Pair spread normalized to [0,1] |
| **P** (Physics) | Price action strength | Momentum consistency × 0.4 + body ratio × 0.3 + persistence × 0.3 |
| **E** (Evidence) | Signal clarity / SNR | `net_move / total_move * 2.5`, capped at 1.0 |
| **X** (Execution) | Trend stability | `1 - CV(ATR)` over 10 bars |
| **Φ** (Witness) | Multi-TF confirmation | geometric mean of (daily, 4H, 1H) directional scores |

**E is usually the bottleneck** in consolidating markets — price chops randomly, SNR collapses, G drops below threshold.

## State Classification
```
CLARITY:  G ≥ 0.50 AND C_dark < 0.30  → trade the direction
STABLE:   G ≥ 0.30 AND C_dark < 0.30  → range trade
CHAOS:    G < 0.30 OR C_dark ≥ 0.30   → don't trade
```

## Verdict
```
G ≥ 0.80 + C_dark < 0.30 + dS ≤ 0  → SEAL (high conviction)
G ≥ 0.50 + C_dark < 0.30            → PROCEED
G ≥ 0.30 + C_dark < 0.30            → SABAR (wait)
else                                 → HOLD
```

## Volume Integration
- Rising volume + price direction = confirmation
- Rising volume + against position = reversal warning
- Falling volume = no conviction (don't trust the move)

## Real Example (XAUUSD 16 Jul 2026)
```
A=0.429  P=0.540  E=0.246  X=0.955  Φ=0.273
G=0.0148  C_dark=0.0088  →  CHAOS  →  HOLD
```
E bottleneck: price consolidating 4019-4050, falling volume, poor SNR. Triggers for CLARITY: volume spike + break below 4019 or above 4050.

## Implementation
```python
from trading.signals.apex_predictor import evaluate_market
apex = evaluate_market(candles_1h=..., candles_4h=..., candles_1d=..., ema_20=..., ...)
# apex.state, apex.verdict, apex.direction, apex.G, apex.C_dark
```
