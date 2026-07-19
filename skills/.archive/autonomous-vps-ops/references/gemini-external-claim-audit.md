# External AI Claim Audit Pattern

When external AI (Gemini, ChatGPT, etc.) produces architectural assessments, validate against F2 (Truth) before accepting.

## The Inflation Pattern

External models tend to inflate achievements. Common patterns:

| Claim Type | Red Flag | Reality Check |
|---|---|---|
| "Enterprise-grade" | Applied to single-VPS setup | Enterprise = multi-region, multi-tenant, 99.99% SLA |
| "Aerospace-grade" | Applied to cron + shell scripts | Aerospace = formal verification, DO-178C, redundant hardware |
| "Production-level SRE" | Applied to basic monitoring | SRE = error budgets, SLOs, toil tracking, on-call rotations |
| "Revolutionary" | Applied to incremental improvement | If it's a known pattern, it's not revolutionary |

## Audit Checklist

For each external claim, score:

1. **Grounding (OBS/DER/INT/SPEC)** — Is this an observation or speculation?
2. **Scale match** — Does the claimed grade match the actual scope?
3. **Missing context** — What would make this claim true? (e.g., "aerospace-grade IF it had formal verification")
4. **Useful kernel** — What 60% is accurate and worth keeping?

## Example: Gemini Assessment (2026-07-12)

**Gemini claimed:** "Production-level SRE / aerospace-grade autonomous control loop"
**Actual:** Single-VPS systemd timer + shell scripts + state machine
**Score:** 60% accurate (immune system analogy, hierarchy encoding, normalized elite for individual context), 40% inflated (no multi-region, no chaos engineering, no SLOs)
**Useful kernel:** The biological immune system analogy (smoketest=pain receptor, state machine=reflex arc, rollback=immune response) is genuinely good framing.

## Response Template

```
Gemini's assessment is X% accurate, Y% inflation.

Accurate:
- [specific claims that match reality]

Overstated (F2 violation):
- [specific claims that don't match scale]

Useful kernel:
- [analogies or framings worth keeping]
```
