# COOLING_RECEIPT — Integrity as Metabolism

> **Ratified:** EUREKA 2026-07-13 (F13)
> **Spec:** `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`
> **P0 status:** ✅ COMPLETE — cooling.receipt registered in seal_chain.js classifyEventType(), validateCooling() with 4 invariants, all tests passing

## What It Is

The COOLING_RECEIPT is a seal_v3 envelope that records what the agent learned from an action — whether the system is converging on correct behavior or diverging into repeated failure.

## The 4 Invariants

| Invariant | Rule | Rationale |
|-----------|------|-----------|
| INV-C1 | action_class must be OBSERVE | COOLING-MUST-NOT-SELF-DEPLOY — reflection, not mutation |
| INV-C2 | caller must not contain "forge" | Execution plane cannot cool itself |
| INV-C3 | supersedes.type must be COLD_LINK | Chains to immutable original seal |
| INV-C4 | governance path explicit | Governed observation, not free-form note |

## Convergence

3× consecutive DIVERGING → F13 escalation. Same trajectory logic as J-collapse detection.

## Connection to AI Equation

AI = Capability × Grounding × Authority × Continuity × Accountability × **Metabolism**

Without cooling, system cannot learn from failure — only accumulates logs. COOLING_RECEIPT converts failure into architecture.

## Reference

- EUREKA seal: `/root/A-FORGE/forge_work/2026-07-13/EUREKA-SESSION-SEAL.md`
- Cooling spec: `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`
- validateCooling(): `/root/AAA/a2a-server/seal_chain.js`
