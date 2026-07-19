# arifOS Three-Layer A2A Model — Transport → Governance → Intelligence

> **Doctrinal insight from conversation 2026-07-13:** Arif asked about A2A protocol, pasted Google's A2A vs Agentic Intelligence comparison table, and I explained how arifOS adds a constitutional layer that standard A2A doesn't have.

## The Standard A2A Model (2 layers)

```
A2A = plumbing (transport)
Agentic Intelligence = brain (reasoning)
```

This is the industry-standard view. A2A carries tasks between agents. Agentic intelligence makes those tasks meaningful. An inventory agent tells an ordering agent "stock is low → order more," and the ordering agent just... does it.

## The arifOS Model (3 layers)

```
┌─────────────────────────────────┐
│   TRANSPORT  — A2A / JSON-RPC   │  AAA port 3001
│   Carries tasks between agents   │
├─────────────────────────────────┤
│   GOVERNANCE — F1-F13 / 888     │  arifOS port 8088
│   Constitutional floor check     │
│   "Are you allowed to do this?"  │
├─────────────────────────────────┤
│   INTELLIGENCE — Domain Agents   │  GEOX / WEALTH / WELL / A-FORGE
│   Domain reasoning + execution   │
└─────────────────────────────────┘
```

## What Changes

| | Standard A2A | arifOS |
|---|---|---|
| **Agent A → Agent B** | "Do X" → Agent B does X | "Do X" → Kernel checks F1-F13 → SEAL/HOLD → Agent B does X |
| **Authority model** | Peer-to-peer (capability) | Constitutional (authority gated through kernel) |
| **Reversibility check** | None | F1: every mutation reversible or backed up |
| **Evidence discipline** | None | F2: OBS/DER/INT/SPEC before action |
| **Blast radius** | None | 888_JUDGE checks blast_radius before SEAL |
| **Sovereign veto** | None | F13: Arif holds final veto |

## Why This Matters

**META-MESA passed 8/8** not because our agents are smarter, but because we govern the *connection between them*. Standard A2A gives pipes. We gave the pipes a constitution.

The common mistake in the industry: people build smart agents with zero governance, bolt on A2A, and call it a multi-agent system. arifOS inserts a sovereign gate between communication and action.

## How to Explain It

When someone asks "don't you just use A2A?":

> "A2A is the transport layer — it carries the message. We add a governance layer on top. Before an A2A task reaches the target agent, arifOS kernel checks F1 (reversible?), F2 (evidence base?), F5 (stakeholder impact?), F13 (sovereign boundary?). The target agent only acts if the kernel issues a SEAL. That's how META-MESA passed — not because we connect agents, but because we govern the connection."

## Where This Lives in the Stack

```
A2A Agent Card → arifOS kernel validates floor compliance → SEAL issued → 
target agent receives task via A2A → executes → returns artifacts → 
VAULT999 seals outcome
```

The agent card itself carries constitutional metadata (class, bound_to, power_band, f1_boundary, rollback_plan) — an arifOS extension beyond the base A2A spec. See `references/a2a-agent-card-normalization.md` for how to expose these fields.

## See Also

- `references/a2a-protocol-overview.md` — technical A2A spec, SDKs, RPC reference
- `a2a-agent-card-registration` skill — operational card wiring in AAA gateway
- `governed-agent-anatomy` skill — constitutional primitives (Identity, Kernel, Actuator chain)
