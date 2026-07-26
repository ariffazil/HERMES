# Multi-Timeframe Analysis (H4 vs H1)

Arif: "Abang sado selalu sebut H4 H1, aku x faham sangat, macam mana nak guna"

## Core Principle

```
H4 cakap ARAH mana  →  H1 cakap BILA masuk
```

H4 dulu, H1 kemudian. Jangan terbalik.

## Timeframe Meaning

| Timeframe | Candle duration | Role | Use |
|---|---|---|---|
| **H4** | 4 hours | BIG TREND | Determine direction (UP/DOWN/SIDEWAYS) |
| **H1** | 1 hour | ENTRY TIMING | Find exact entry point |
| **M15** | 15 minutes | Micro-timing | Fine-tune entry (optional, can be noisy) |
| **Daily** | 24 hours | Macro context | Overall trend backdrop |

## The Golden Rule

```
If H4 = DOWN  → only look for SELL entries on H1
If H4 = UP    → only look for BUY entries on H1
If H4 = SIDEWAYS → wait, or range trade S1→R1
```

Kalau H4 kata DOWN tapi H1 tengah naik — **SABAR**. Tunggu H1 ikut direction H4.

## Visual Example

```
H4:  ╲╲╲╲╲╲╲╲╲╲╲╲╲╲   ← "Trend turun, aku cari SELL je"
         ↘️
H1:      ╱╱╱╱╱╱╱        ← "Tapi H1 tengah naik... SABAR"
                ↘️
H1:              ╲╲╲╲╲   ← "Ha! H1 dah ikut H4. Baru ENTRY SELL"
```

## Why Not One Timeframe?

| Single timeframe | Problem |
|---|---|
| H1 only | Noise. Whipsaw. Signal palsu. |
| H4 only | Terlalu lambat. Half the move dah lepas bila signal keluar. |
| **H4 + H1** | H4 bagi trend besar, H1 bagi timing tepat. |

## Gold Engine Regime Detection

The trading engine uses EMA20/50/200 alignment for regime (H4 function) + 1H S/R levels for entry zones. Both must align before signal fires. If not → **SABAR** verdict.

Current state (Jul 18, 2026): DOWNTREND 95%, price $4,023 pullback above EMAs → engine says SABAR because H1 hasn't aligned with H4 downtrend yet.

## Pattern Recognition

Common patterns visible through multi-timeframe:

- **Bearish flag:** Sharp drop on H4, sideways/slight-up consolidation on H1 → continuation down
- **Bullish flag:** Sharp rise on H4, slight-down consolidation on H1 → continuation up
- **Double bottom/top:** Reversal patterns visible on both timeframes for confirmation
- **Pennant:** Triangle consolidation → breakout in trend direction

## Pitfall

- **Don't counter-trade the higher timeframe.** H4 down + H1 bullish engulfing ≠ BUY. Wait for H1 to confirm H4 direction, not fight it.
- **Weekend gap risk.** Monday open can gap significantly from Friday close, especially after major news events over the weekend.
