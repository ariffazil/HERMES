# Eureka Genesis + HITV Protocol — Forging Session (2026-07-29)

## Origin

This session forged two canonical conceptual frameworks simultaneously:

1. **Eureka 1-4 + Meta-Eureka** — The origin story: GPTs as fossil record, prompt-leaking as feature, governed mode as trojan horse, category error as validation. The conversation itself proved the architecture.

2. **HITV v0.1 (Human-in-the-Veto)** — The design solution to the BANGANG HITL problem. Full protocol: consent compression, 4 decision classes, approval grammar, sovereign-in-training modes.

## Three-Pulse Metabolism

The federation runs on three agents with three distinct pulses:

| Agent | Role | Pulse | Verify cycle |
|-------|------|-------|-------------|
| **HERMES** | Sovereign relay — conversation | Conversation rhythm | Read Arif's reply; detect correction |
| **OPENCRAWL** (Surface Guardian) | Registry drift detection, surface consistency | Every health probe (60s) | Registry == live MCP tools/list? |
| **OPECODE** | Forge execution under lease | Every cooling cycle + F4 check | execute_count vs verify_count |

**Heart:** arifFLOW daemon (:7073) computes FQ = Σ(Execute.cost) / Σ(Verify.cost). FQ < 0.5 = STUCK → all agents HOLD.

**Live gap discovered:** The architecture is conceptually complete but metabolically fractured:
- SurfaceGuard detects drift but doesn't push receipts to arifFLOW
- HERMES doesn't emit FlowReceipts per turn
- OPECODE's CoolingGate operates independently of arifFLOW's FQ
- No NATS channel `arifflow.fq.verdict` for federation-wide HOLD propagation

## HITV Core Doctrine

> **Human is not a processor. Human is veto, intent, and legitimacy source.**

### Decision Classes

| Class | Name | Verdict | Human need |
|-------|------|---------|------------|
| 0 | Observe only | SEAL auto | None — low risk, read-only |
| 1 | Reversible action | PARTIAL/SEAL | None — undo path exists |
| 2 | Consequential action | HOLD → SEAL | Brief approval (consent-compressed) |
| 3 | Irreversible/sovereign | 888_HOLD | Explicit Arif sanction |

### Consent Compression Format

Every approval payload MUST be:

```
INTENT: What the system wants to do
SCOPE: Bounds of the action
RISK: What could go wrong
UNDO: Can it be reversed?
EVIDENCE: On what basis?
ASK: SEAL / MODIFY / REJECT
```

### Sovereign-in-Training Modes

- **Light Mode (Passenger-safe):** "Safe mode on. I'll only do reversible actions unless you approve."
- **Governed Mode (Operator):** "This action affects money/data/reputation. Approval required."
- **Sovereign Mode (ARIF-level):** Full F1-F13, AAA loop, A-FORGE, evidence taxonomy, authority chain.

## Naming Correction (2026-07-29)

- ~~OpenClaw~~ → **OpenCrawl** (Surface Guardian, immune system). Not a mechanic. Observes, classifies, routes, verifies health consistency. Never forges, never converses.
- The three agents: **HERMES** (relay) · **OPENCRAWL** (surface) · **OPECODE** (forge)

## Key Formulations

- "A prompt is wish with syntax. A kernel is a promise with physics."
- "He expected a fish. You handed him a submarine."
- "F13 is not a bottleneck. F13 is the legitimacy valve."
- "Bad HITL asks humans to think like machines. Good HITL lets machines process, but forces humans to remain morally present."
- "GPTs taught us that intelligence without flow is noise. arifOS proved that flow IS the intelligence — not the model, not the prompt, not the output."
