# Memory Lifecycle: 5 Generations (Eureka 2026-07-12)

## The 5 Generations

| Gen | Name | Pattern | arifOS Status |
|-----|------|---------|---------------|
| 1 | Transcript | Store conversation → retrieve similar text | Legacy |
| 2 | Semantic | Chunk → embed → vector search | Current (Qdrant/pgvector) |
| 3 | Governed | + provenance + truth class + expiry + authority | Current (memory_store.py) |
| 3.5 | Outcome-attributed | + record whether memory improved decision | **NEXT BUILD** |
| 4 | Predictive | Pattern → current-state match → forecast → modify routing | Planned |
| 5 | Counterfactual | Did this memory actually improve the decision? | Speculative |

## The Key Principle

> Truth does not automatically grant authority.

A true memory (OBS class, high confidence) may have NO authority to affect action.
A memory with authority to change routing may be wrong (INT class, medium confidence).

The two dimensions (truth + authority) must be tracked independently.

## Promotion Formula

```
M = P_reuse × I_decision × R_evidence × S_retrieval - C_maintenance - R_privacy

M ≥ 0.55 → eligible for governed promotion (M3 → M4)
0.30-0.55 → temporary (keep in M3, re-evaluate)
< 0.30 → do not promote (let cool, may discard)
```

Hard gates (non-negotiable):
- Contested memory → REJECTED (regardless of score)
- Independent sources < minimum → REJECTED
- Confidence < truth class ceiling → cannot promote

## Outcome Attribution (Generation 3.5)

The minimum viable measurement spine: three columns.

| Column | Type | Purpose |
|--------|------|---------|
| `memory_id` | string | Which memory was used |
| `decision_id` | string | Which decision used it |
| `outcome_useful` | boolean | Did the decision improve? |

This creates a feedback loop: memories that improve decisions get promoted, memories that don't get decayed.

## Immune-to-Decay Flag

Constitutional memories (niat, scars, sovereign boundaries) must NEVER decay.
Use `immune_to_decay: true` for:
- Sovereign boundaries
- Scar epistemology entries
- Constitutional rules
- Niat (intention) records

## Gödel Lock in Memory Context

The Gödel lock means: **memory cannot certify its own value.**

- A memory cannot promote itself
- A memory cannot expand its own authority
- A memory cannot declare itself immune to decay (only sovereign can)
- A memory's value must be measured by external outcome, not internal confidence
