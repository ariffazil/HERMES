---
name: geox-comparative-testing
description: "Three-agent comparison methodology for proving GEOX governance value — GEOX vs Vanilla AI vs External Tools on identical geological data. Used when the question is 'does GEOX actually make AI produce better geological output?'"
tags: [geox, testing, comparison, governance, falsification, marmousi, petrophysics]
triggers:
  - "does GEOX actually work"
  - "prove GEOX value"
  - "compare GEOX to vanilla"
  - "benchmark GEOX"
  - "test GEOX against"
  - "3-agent test"
  - "Marmousi"
  - "does governance add value"
---

# GEOX Comparative Testing — 3-Agent Methodology

> Proven: 2026-07-19 — Marmousi2 synthetic wells.
> **Governance-weighted** (architectural): GEOX 8.3/10 · Vanilla 2.9/10 · Tools 4.8/10
> **Geological-accuracy-weighted** (honest rescore, Hermes audit 2026-07-19): GEOX 6.3/10 · Vanilla 2.2/10 · Tools 4.3/10
> The 8.3 score weights governance, falsification, and reproducibility heavily — valid for architecture/investor audiences. The 6.3 score weights geological accuracy and practical usefulness — valid for geoscientist audiences. Use the score that matches your audience. Never present 8.3 as "geologically superior" — it's "governance superior" with comparable computation.

## The Question

"Does GEOX governance actually make AI produce better geological output?"

Not "does GEOX have more features?" Not "is the protocol working?" The question is: given identical data, does GEOX produce objectively better, more honest, more auditable geological analysis than unaided AI?

## The 3-Agent Design

| Agent | Name | Tools | What it tests |
|-------|------|-------|---------------|
| **A** | Vanilla | None — pure model knowledge | Baseline: how good is raw AI geological reasoning? |
| **B** | Tools | lasio + numpy + matplotlib | Can standard Python geoscience tools match GEOX? |
| **C** | GEOX | Full stack: geox_well_ingest, geox_petrophysics, geox_sequence, geox_falsify, geox_claim, geox_deep_time_state | Does governed intelligence beat ungoverned intelligence? |

## Test Data Requirements

Minimum: 2-3 wells with DT, GR, RHOB curves. Synthetic (Marmousi2) works for initial validation. Real data (Sabah Basin, Malay Basin) for production comparison.

## Scoring Dimensions (10-point scale)

| Dimension | What it measures |
|-----------|-----------------|
| Geological accuracy | Correctness of reservoir quality, zone identification, porosity ranges |
| Data quality flags | Detection of bad data (GR=0, missing logs, negative densities) |
| Computation quality | Correct petrophysics (Vsh, φe, Sw), proper cutoffs, zone targeting |
| Epistemic discipline | Explicit OBS/DER/INT/SPEC labeling, confidence capping at 0.90 |
| Governance & audit | VAULT999 receipts, claim engine entries, audit trail completeness |
| Falsification | Kill matrix application, honest INCONCLUSIVE vs PROVEN distinction |
| Reproducibility | Same inputs → same outputs, full provenance chain |
| Visualization | Well panels, crossplots, interpretable output |

## The Falsification Test (GEOX-only)

GEOX runs the 7-filter kill matrix on a geological claim. The claim format: "These wells contain viable reservoir-quality sands." The filters:

1. Physical plausibility
2. Stratigraphic consistency
3. Burial/compaction consistency
4. Pore pressure consistency
5. Cross-well coherence
6. Deep-time context fit
7. Alternative hypothesis survival

**Critical:** The result is often INCONCLUSIVE, not PROVEN. GEOX's honesty about uncertainty IS the advantage. Vanilla and Tools agents assert their conclusions. GEOX admits when it cannot determine something (e.g., "fluid phase: SPEC — cannot determine without RT").

## Expected Results

GEOX should win on governance, epistemic discipline, falsification, and reproducibility — even when computation quality is identical to the Tools agent. The gap widens with real (non-synthetic) data because ambiguity and contradictions are where governance adds the most value.

## Anti-Patterns

- **Don't compare feature counts.** More tools ≠ better output. Measure output quality.
- **Don't use GEOX-only data.** All three agents get the same LAS/SEG-Y files.
- **Don't score GEOX on computation alone.** The Tools agent computes porosity correctly too. GEOX's advantage is the governance layer around the computation.
- **Don't cherry-pick wells.** Use all available wells. Honest comparison includes failures.
- **Don't claim "falsification advantage" when all filters return NOT_TESTED.** The Marmousi test: 2/7 PASS (no contradictory evidence found), 5/7 NOT_TESTED. The engine ran. It didn't add geological insight. Be honest about this.
- **Don't claim WEALTH bridge is operational unless proven.** As of 2026-07-19, `geox_to_wealth_bridge` returns "Unknown tool" via kernel routing. The bridge infrastructure exists in code but the deployed bridge is broken. Don't claim "cross-organ bridge ready" without live verification.
- **AI-vs-AI is a low bar.** This test compares AI agents against each other. The real question — "does GEOX produce better output than a human geoscientist using Petrel?" — is not answered here. The bar for that claim is much higher and requires human review.

## Reference

See `references/marmousi-2026-07-19.md` for the full 3-agent comparison report with per-well scoring, falsification audit, and the 8.3/10 vs 2.9/10 vs 4.8/10 breakdown.
