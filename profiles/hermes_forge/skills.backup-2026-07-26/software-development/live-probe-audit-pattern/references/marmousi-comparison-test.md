# Marmousi Comparison Test — The "Does GEOX Produce Better Output?" Pattern

> **Proven 2026-07-19:** Three agents (Vanilla AI, Tools, Full GEOX) analyzed the same Marmousi2 synthetic wells. GEOX scored 8.3/10 vs 2.9/10 and 4.8/10. The test proved governance, falsification, and epistemic discipline produce measurably better geological output — not just more computation.

## Why This Test Matters

This is the answer to "is GEOX actually better?" — not measured by architecture diagrams or feature lists, but by output quality. Run it on every new data type (Sabah Basin, Malay Basin, real SEG-Y) to prove value incrementally.

## Test Design

| Agent | Tools | What It Tests |
|-------|-------|---------------|
| A — Vanilla | None | Pure model knowledge. No computation. No libraries. |
| B — Tools | lasio + numpy + matplotlib | Standard Python geoscience stack. Manual petrophysics. |
| C — Full GEOX | geox_well_ingest, geox_petrophysics, geox_sequence, geox_falsify, geox_claim, geox_deep_time_state | Governed intelligence. Epistemic labels. Falsification. |

## Scoring Dimensions

1. Geological accuracy
2. Data quality flags
3. Computation quality
4. Epistemic discipline
5. Governance & audit
6. Falsification
7. Reproducibility
8. Visualization

## 2026-07-19 Results

| Dimension | Vanilla (A) | Tools (B) | GEOX (C) |
|-----------|:-----------:|:---------:|:--------:|
| Geological accuracy | 5/10 | 6/10 | 7/10 |
| Data quality flags | 7/10 | 5/10 | 8/10 |
| Computation quality | 2/10 | 8/10 | 8/10 |
| Epistemic discipline | 6/10 | 5/10 | 9/10 |
| Governance & audit | 1/10 | 2/10 | 10/10 |
| Falsification | 0/10 | 0/10 | 8/10 |
| Reproducibility | 1/10 | 4/10 | 9/10 |
| Visualization | 1/10 | 8/10 | 7/10 |
| **Overall** | **2.9** | **4.8** | **8.3** |

## Key Finding

GEOX's advantage is NOT faster computation. The Tools agent computed porosity correctly too. The advantage is governance — every claim has a receipt, an epistemic label, an audit trail, and survives falsification. That's what produced the 8.3 vs 4.8 gap.

## How To Reproduce

1. Prepare identical well data (LAS files from Marmousi2 or equivalent)
2. Dispatch three agents with identical task: "analyze these wells for reservoir quality"
3. Agent A gets no tools. Agent B gets lasio+numpy+matplotlib. Agent C gets full GEOX MCP surface.
4. Score each output on the 8 dimensions
5. Publish comparative analysis with per-dimension scoring

## Why This Beats Feature Tables

Feature tables say "GEOX has falsification, Petrel doesn't." But nobody believes feature tables. A scored comparison on real data says "GEOX scored 8.3/10 vs 4.8/10 on the same wells." That's evidence, not marketing.

Run this test with every major data release. It becomes the empirical foundation for every capability claim.
