# Gold Trading Session Volatility & News Impact

## Source
Analysis of 11,461 hourly XAUUSD candles from yfinance GC=F (Jul 2024 - Jul 2026).
Real data, not synthetic. Referenced by `trading-intelligence-system` skill.

## Volatility by Session (MYT = UTC+8)

| Session | MYT Hours | Avg Range | >1% Moves | Rank |
|---------|-----------|-----------|-----------|------|
| **LONDON** | 15:00-19:00 | **0.576%** | 306 | 🔴 #1 MOST VOLATILE |
| US NEWS | 20:00-22:00 | 0.376% | 84 | 🟡 #3 |
| ASIAN | 07:00-14:00 | 0.370% | 193 | 🟢 #4 |
| LATE US/OVERNIGHT | 23:00-04:00 | 0.385% | 224 | ⚪ #2 |

**Key finding: London session moves gold 54% more than US news window.**

### Why London is king for gold:
- LBMA (London Bullion Market Association) sets the gold price
- Bank-bank besar buka position waktu London open
- US data (CPI, NFP at 8:30 AM ET = 8:30-9:30 PM MYT) often "price in" during London
- London-NY overlap (20:00-00:00 MYT) = secondary peak

### Top 5 Biggest Single-Candle Moves (2yr data):
| Date | MYT | Move% | Direction | Probable Trigger |
|------|-----|-------|-----------|-----------------|
| 29 Jan 2026 | 18:00 | 7.66% | DOWN | FOMC decision |
| 23 Mar 2026 | 15:00 | 4.48% | UP | Flash crash recovery |
| 30 Jan 2026 | 12:00 | 3.94% | DOWN | Post-FOMC follow-through |
| 12 Feb 2026 | 19:00 | 3.85% | DOWN | CPI / data release |
| 29 Jan 2026 | 05:00 | 3.81% | DOWN | Overnight crisis continuation |

**Pattern: FOMC and CPI days produce the biggest moves, but they START in London session.**

## News Impact Hierarchy (Forex Factory color codes)

### 🔴 RED (High Impact) — AVOID TRADING
| Event | MYT | Avg Gold Move | Duration |
|-------|-----|---------------|----------|
| FOMC Rate Decision | 02:00 | ±3-7% | 4-24 hours |
| US CPI | 20:30 | ±1-4% | 2-8 hours |
| Non-Farm Payrolls (NFP) | 20:30 | ±1-3% | 1-4 hours |
| Fed Chair Press Conf | 02:30 | ±2-5% | 2-12 hours |

**Rule: Close all positions 30min before red news. Re-enter 30min after.**

### 🟡 YELLOW (Medium Impact) — TRADE WITH CAUTION
| Event | MYT | Avg Gold Move |
|-------|-----|---------------|
| Fed Speech (various) | Various | ±0.5-1% |
| ISM PMI | 22:00 | ±0.3-0.8% |
| Retail Sales | 20:30 | ±0.3-0.8% |
| PPI | 20:30 | ±0.2-0.5% |

### 🟢 GREEN (Low Impact) — IGNORE
- Housing data, consumer sentiment, minor surveys
- ±0.1-0.3% — noise, not signal

## Practical Rules for Syed

1. **Best trading hours**: 15:00-19:00 MYT (London session)
2. **Dangerous hours**: 20:30 MYT on red news days (CPI, NFP)
3. **Dead hours**: 07:00-14:00 MYT (Asian session, low vol)
4. **Red news day** = reduce position size or sit out entirely
5. **30-minute rule**: Wait 30min after red news before entering
6. **London open trap**: First 30min (15:00-15:30) often fake — wait for direction

## Correlation: News Surprise → Gold Direction

**General rule (not always):**
- CPI lower than forecast → USD weak → Gold UP
- CPI higher than forecast → USD strong → Gold DOWN
- NFP weaker than forecast → USD weak → Gold UP
- NFP stronger than forecast → USD strong → Gold DOWN
- Fed dovish (rate cut signal) → Gold UP
- Fed hawkish (rate hike signal) → Gold DOWN

**But**: Market often "prices in" the expectation BEFORE the release. The reaction can be opposite to the "obvious" direction if the surprise was already anticipated. This is why waiting 30min is safer than trading the spike.
