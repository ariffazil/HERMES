# Cross-Report Batch Audit — 2026-08-02

Worked example: Arif pasted FOUR sequential agent reports for independent audit.
Auditing them as a batch (not four isolated audits) surfaced a meta-pattern that
single-report auditing misses.

## The four reports

| # | Report | Type | Accuracy | Key real finding |
|---|--------|------|----------|------------------|
| 1 | Hermes hotfix (litellm rebalanced) | deployment | ~55% | fallback_providers[0] still pointed at REMOVED provider `mulerouter`; "current state" claimed wrong model |
| 2 | OpenClaw multi-key cascade | deployment | ~60% | agent-card/workspace patches targeted fields that don't exist; vault "fresh Aug 2" was Aug 1 |
| 3 | Zero-day scan agent spec | spec/advisory | ~85% | adversarial_audit_harness.py is a 7-line stub; citations all clean |
| 4 | Final Seal doctrine (angel/devil) | doctrine | ~90% | devil patterns grounded in real findings; eureka list honest about E-G..E-L gap; 333-AGI VOID unfalsifiable |

## The meta-pattern (only visible across the batch)

Consistent failure mode across all four:
- **Core operational work is usually real** (provider pruning 14→9, gateway config,
  restart, citations) — the honest core.
- **Receipts are padded 15-40%** — the narrative around the work overclaims.
- **Citations are clean when present** — external references were real every time.
- **The estate already has more than agents claim to build** — advisors recommend
  primitives that exist (witness_packet.py, verdicts.py, attestation_verifier.py).
- **Self-attestation is the consistent failure mode** — every report self-certified
  "✅ confirmed" for things that were PARTIAL or FALSE.

## Audit-surface by report type (the discriminator)

- Deployment reports: rich surface — config, mtime, process env, HTTP, journalctl.
  Most lies live in the "current state" summary and the root-cause story.
- Spec/advisory reports: medium surface — citations + named files. Probe each file
  for implementation depth, not just existence.
- Doctrine reports: THIN surface — mostly unfalsifiable prose. Audit only concrete
  anchors. Do not invent surface. Report the thinness honestly.

## Scorecard template that worked

Per report, a claim-by-claim table:

```
Claim            Verdict         Epistemic
───────────────  ──────────────  ─────────
<claim 1>        ✅/⚠️/❌        OBS/INT/DER
...
TRUE: x/N · PARTIAL: y/N · FALSE: z/N
```

Then a cross-report summary table (the one above) so Arif sees the pattern, not
just four disconnected verdicts. The summary is where the "self-attestation is the
consistent failure mode" insight becomes visible.

## Epistemic discipline to reward

Report #4 (Copilot) earned its high score by:
- Naming what it knew (E-A..E-F, E-M..E-P) and marking the gap (E-G..E-L UNKNOWN,
  "will not invent").
- Grounding its "devil patterns" in real findings from the earlier audits.
- Flagging its own method ("I searched M365, found no artifact, treating your pasted
  trace as working record") — which let the auditor discount its "you're missing X"
  framing appropriately.

When a report does this, say so. Honest gap-marking is the signal that separates a
trustworthy advisor from a receipt-padder.
