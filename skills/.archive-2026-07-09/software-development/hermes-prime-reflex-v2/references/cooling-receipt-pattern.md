# Cooling Receipt Pattern (2026-07-13)

## What It Is
COOLING_RECEIPT is VAULT999 seal_v3 — a metabolic seal type that closes the learning loop after execution. Records drift between plan and reality, proposes improvement, routes back through governance.

## Constitutional Invariants
- **INV-C1**: action_class must be OBSERVE (COOLING-MUST-NOT-SELF-DEPLOY)
- **INV-C2**: caller must not contain "forge"
- **INV-C3**: supersedes.type must be COLD_LINK
- **INV-C4**: governance path must be explicit

## Governance Routing
| Authority | Behavior |
|-----------|----------|
| AUTO | Auto-apply if within existing capability |
| OBSERVE_ONLY | Store for human review |
| 888_HOLD | Route to arif_judge |
| F13_SOVEREIGN | Route to arif_judge with F13 escalation |

## When to Use
Post-execution drift, post-verification anomaly, human correction, scheduled reflection, session close.

## Reference
`/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md` (387 lines)
