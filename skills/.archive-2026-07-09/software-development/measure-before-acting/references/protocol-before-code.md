# Protocol Before Code (FORGED 2026-07-20)

## Pattern

When building a multi-layer architecture change, lock the protocol in documentation FIRST,
making it a constitutional requirement. Then write the traffic code to satisfy that protocol.

## Trigger (from Arif)

> "Defining these routes in AGENTS.md is the correct epistemic sequence. 
> You lock the protocol in the documentation first, making it a constitutional 
> requirement, and then you write the traffic code to satisfy that protocol.
> ΔS < 0."

## The Session

During the Tri-Layer Cognition routing session (2026-07-20), Arif identified three
traffic gaps (L1→L2 evidence_sha, L1→L2 reversion_event, L2→L3 auto-indexing).
Instead of jumping to implementation, he directed:

1. First: document the routing protocol in AGENTS.md as a constitutional requirement
2. Then: implement one route at a time, testing each independently

Result: Protocol locked in `arifOS/AGENTS.md` under "Tri-Layer Cognition — Routing Protocol"
with layer mapping, schema bridge, three route contracts, and an implementation checklist.
Route 3 (L2→L3 memory sync) was then implemented in 35 lines.

## The Check

Before writing code for any architectural change spanning multiple components:

1. Document the protocol in AGENTS.md or equivalent canonical doc
2. Define contracts (function signatures, field schemas, data flow)
3. Define implementation checklist with checkbox items
4. Implement one route at a time, committing independently
5. Each commit references the protocol section it satisfies

## Why

- **ΔS < 0:** Protocol documents REDUCE entropy — they answer "what should happen" before code fights over "what does happen"
- **F2 TRUTH:** Protocol-as-doc is the epistemic floor. Code can drift; the protocol statement is the source of truth
- **F4 CLARITY:** Separating protocol from implementation prevents conflating "this is what we need" with "this is how I built it"
- **F11 AUDIT:** Protocol docs create an audit trail of architectural intent independent of implementation

## Anti-Pattern

```
Code first → "what does this do?" → reverse-engineer behavior → document later (never)
```

## Correct Pattern

```
Protocol doc → route contracts → implementation checklist → one route → commit → verify → next route
```
