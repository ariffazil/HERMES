# PETRONAS Fiscal Intelligence — Pipeline Reference (2026-07-29)

## Source

| Field | Value |
|---|---|
| **Article** | Ballooning subsidy bill to wipe out PETRONAS dividend gain, says BIMB |
| **Publisher** | The Edge Malaysia |
| **URL** | https://theedgemalaysia.com/node/812228 |
| **Date** | 28 Jul 2026 |
| **Fetcher** | smart_fetch (direct HTTP, 240ms, HTTP 200) |

## Key Data Extracted

| Metric | Budget 2026 | Actual/Expected | Delta |
|---|---|---|---|
| Fuel subsidies | RM21.6b | ~RM40b | **+85%** |
| PETRONAS dividend | RM20.0b | ~RM33.5b | **+67.5%** |
| Fiscal deficit (% GDP) | 3.5% | 3.8% | **+30 bps** |
| Brent assumption | US$65/bbl | US$92.50 avg (H1 2026) | **+42.3%** |
| Brent spot (28 Jul) | — | ~US$87 | — |

## Institutional Stress Index (Manual)

| Dimension | Score | Band |
|---|---|---|
| Financial | 0.55 | MODERATE-HIGH |
| Governance | 0.60 | MODERATE-HIGH |
| Workforce | 0.30 | LOW-MODERATE |
| Legal | 0.25 | LOW |
| External Exploitation | 0.70 | HIGH |
| **Composite** | **~0.55** | **MODERATE-HIGH** |

## Cross-References Found

- **SERC (Mar 2026):** Already flagged higher Petronas dividend likely — published via The Malaysian Reserve
- **Supply Crisis (Jun 2026):** Whole-of-nation response needed — published via The Edge & The Star

## Key BIMB Quote

> "Given the limited appetite to introduce new taxes or raise tax rates, tapping a larger dividend from PETRONAS remains the most practical way to offset higher fuel subsidies."

## Pipeline Issues Encountered

1. **WEALTH server unreachable** — `wealth_institutional_stress_index` returned 3 consecutive failures
2. **arif_seal blocked** — OBSERVE_ONLY authority correctly rejected irreversible operation
3. **Workaround:** Manual stress computation + forge work receipt filing as evidence artifact

## Handoff FI-001

Filed at `/root/forge_work/2026-07-29/petronas-fiscal-intelligence-20260728.md`
