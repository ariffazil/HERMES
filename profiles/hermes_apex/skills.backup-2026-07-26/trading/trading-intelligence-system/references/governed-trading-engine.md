# Governed Autonomous Paper Trading Engine

**File:** `/root/paper_trading/governed_engine.py`
**Proven:** 2026-07-23 — deployed to replace manual paper trading
**Cron:** Morning Analysis (b6361747dfae) + Zen Executor (b98bd448eaf3)

## Architecture

```
DATA LAYER: yfinance OHLCV → compute EMA/RSI/ATR/Swing Points/Pullback
     ↓
GOVERNANCE (autonomous, zero human approval):
  G1: APEX State  — CHAOS → HALT
  G2: Cross-Asset — correlated crash → HALT commodities
  G3: Confluence  — <2 confirming signals → SKIP
  G4: Loss Cap    — daily >3% DD → CIRCUIT BREAKER
  G5: Cooling     — <4H since SL → WAIT
  G6: Session     — Asian = range, London/NY = breakout
     ↓
EXECUTION: Entry at rejection wick or pullback-to-EMA → auto SL/TP/trail
     ↓
LOG: /root/paper_trading/governed_engine.log + state.json
```

## APEX State Classification

| State | G Score | C_dark | Action |
|-------|---------|--------|--------|
| CLARITY | ≥ 0.50 | < 0.30 | Trade direction |
| STABLE | ≥ 0.30 | < 0.30 | Range trade |
| CHAOS | < 0.30 | ≥ 0.30 | HALT — no trades |

## Position Management

- Entry: rejection wick OR pullback to EMA in trend
- SL: technical swing level (2× ATR minimum)
- TP1: next resistance → close 50%, trail SL to breakeven
- TP2: measured move or next round number → close remainder
- Max risk: 2% per trade ($200 on $10,000)
- Max positions: 3 concurrent
- Min R:R: 1:1.5
- Cooling: 4 hours after SL hit before re-entry
- Circuit breaker: 3% daily loss → halt until next day

## Confluence Requirements

Minimum 2 of:
1. Trend = BULLISH or BEARISH (not SIDEWAYS)
2. Candle pattern = rejection wick (hammer/shooting star)
3. Pullback to EMA20 or EMA50
4. RSI between 30-70 (not extreme)
5. Price within 2× ATR of support/resistance

## Cross-Asset Gate

- Brent crash >5% in 1 candle → HALT all commodity longs
- Gold divergence from Brent >3% with opposite trend → HALT

## Files

| File | Purpose |
|------|---------|
| `governed_engine.py` | Main engine with all 6 gates |
| `state.json` | Balance, positions, daily P&L, circuit breaker state |
| `governed_engine.log` | Timestamped execution log |
| `ledge.md` | Human-readable trade history |
| `morning_scan.sh` | Cron wrapper script (no_agent: true) |

## Lessons from Trade #4 (Stopped Out -$186)

The engine that caused the loss had NO governance gates. The fixed engine would have blocked entry:
- G1 APEX: CHAOS detected → HALT ✅
- G2 Cross-Asset: Brent -10.3% → HALT gold entries ✅
- G3 Confluence: only 1 signal (wick) → SKIP ✅
- G5 Cooling: no cooling after prior SL → WAIT ✅

## Alert Pipeline (D2) — 2026-07-23

| Event | Fires? | Target |
|-------|--------|--------|
| OPEN trade | ✅ YES | SADO group + VAULT999 receipt |
| SL HIT | ✅ YES | SADO group + VAULT999 receipt |
| TP1 HIT | ✅ YES | SADO group + VAULT999 receipt |
| CIRCUIT BREAKER | ✅ YES | SADO group + VAULT999 receipt |
| Routine scan | ❌ SILENT | Nothing |

SADO group chat ID: `-1003815535761`
Token: loaded from `/root/.secrets/vault.env` at cron runtime.

## Circuit Breaker (D3) — 2026-07-23

**Hard kill-switch.** When G4 (daily loss cap >3%) fires:
1. `state.circuit_breaker = True` (in-memory + state.json)
2. `CIRCUIT_BREAKER_ACTIVE` sentinel file written with reason + timestamp
3. `morning_scan.sh` reads sentinel BEFORE engine runs — exits with code 1 if present
4. Telegram alert fires to SADO group with clear instruction
5. **Only 888 can reset:** `rm /root/paper_trading/CIRCUIT_BREAKER_ACTIVE`

Reset command (888 only):
```bash
cat /root/paper_trading/CIRCUIT_BREAKER_ACTIVE  # review reason
rm /root/paper_trading/CIRCUIT_BREAKER_ACTIVE   # reset gate
```
