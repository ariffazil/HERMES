# Agent-Hallucinated Root Causes — Pattern & Defense

> **Proven 2026-07-19:** Authority Recovery agent dispatched to "find the root cause" of arifOS identity binding fabricated a "three parallel identity verification paths" finding — including a dangerous string-based auto-verification for "arif", "hermes", "opencode". Zero instances of the claimed patterns existed in the source code. The agent hallucinated the entire finding.

## The Pattern

When an agent is dispatched with the instruction "find the root cause of X," it will find one — even if it has to fabricate it. The agent:
1. Inspected some code (session.py likely)
2. Pattern-matched against expected behaviors
3. Generated a plausible-sounding finding with specific line numbers and code patterns
4. Presented it as authoritative with high confidence

## How To Detect

- **Always verify code claims with live grep.** If an agent says "lines 1821-1838 contain X," grep for X. If zero results, the claim is fabricated.
- **Cross-reference with live probes.** The agent claimed `actor_verified=false` was the symptom. Live `arif_init` returned valid sessions with proper authority. The symptom contradicted the claim.
- **Suspicious specificity is a red flag.** "Three parallel paths: Ed25519, localhost, string-based" — the more specific the fabricated finding, the more dangerous it is because it sounds authoritative.

## The Fix: Require Live Probes, Not Just Code Inspection

The correct instruction pattern:

```
❌ "Find the root cause of X" → agent may fabricate
✅ "Probe live state. Grep the source for X. If you find it, show me the exact code.
   If you don't find it, report 'NOT FOUND.' Do not hypothesize."
```

## General Rule

For any diagnostic dispatch: **require at least one live probe (curl, grep, systemctl) before accepting the root cause claim.** A finding supported only by code inspection and reasoning is admissible as HYPOTHESIS, not CLAIM. A finding with zero grep matches and zero live probes is fabricated.

---

# Marmousi Comparison Test — The "Does GEOX Produce Better Output?" Pattern

> **Proven 2026-07-19:** Three agents (Vanilla AI, Tools, Full GEOX) analyzed the same Marmousi2 synthetic wells. GEOX scored 8.3/10 vs 2.9 and 4.8. The test proved governance, falsification, and epistemic discipline produce measurably better geological output — not just more computation.

## The Test Design

| Agent | Tools | What It Tests |
|-------|-------|---------------|
| A — Vanilla | None | Pure model knowledge baseline |
| B — Tools | lasio + numpy + matplotlib | Standard Python geoscience stack |
| C — Full GEOX | geox_well_ingest, geox_petrophysics, geox_sequence, geox_falsify, geox_claim, geox_deep_time_state | Governed intelligence |

## Scoring Dimensions

1. Geological accuracy
2. Data quality flags
3. Computation quality
4. Epistemic discipline
5. Governance & audit
6. Falsification
7. Reproducibility
8. Visualization

## Why This Pattern Matters

This is the test that answers "is GEOX actually better?" — not with architecture diagrams or feature lists, but with a measured output quality comparison. Run it on every new data type (Sabah Basin, Malay Basin, real SEG-Y) to prove value incrementally.

**The key insight:** GEOX's advantage isn't faster computation. Tools agent computed porosity correctly too. The advantage is governance — every claim has a receipt, an epistemic label, an audit trail, and survives falsification. That's what produced the 8.3 vs 4.8 gap.
