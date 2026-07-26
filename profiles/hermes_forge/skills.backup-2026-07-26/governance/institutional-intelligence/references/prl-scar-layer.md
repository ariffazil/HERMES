# Precedent Retrieval Layer (PRL) — The Scar Layer

> Sessions: 2026-07-20. Arif's architectural design + Phase 1 forge.
> Phase 1 commit: `924ed1cd8` — vault_vectorizer.py, prl_gate.py, blast_radius on arif_seal.
> 120 vectors indexed in Qdrant `arifos_precedent` (1024-dim COSINE).

## What PRL Is

The PRL is a **geometric enforcement layer** that intercepts every new query to arifOS, searches VAULT999 for matching sealed precedents via vector similarity, and injects binding constraints BEFORE the agent generates output.

It is NOT memory in the biological sense. It does not "remember." It uses **cosine similarity** to detect that a new query is near a past verdict in vector space, then enforces the governing rule from that verdict.

## Three Paths to AI Consistency

| Path | Mechanism | Problem |
|------|-----------|---------|
| Blank Slate | No memory. Fresh every session. | Amnesia. Sovereign carries cognitive burden. |
| Biological Trap | Feed past conversations as context. | F9 violation. AI simulates a ghost. Hallucinated continuity. HANTU. |
| **Cold Geometric Law (PRL)** | Vector match → inject binding constraint. | NO memory. NO personality. Just constraint propagation. |

## Why "Scar Layer"

`W_scar` = the weight of the scar. The deeper the precedent (more weight), the harder it binds.

PRL doesn't retrieve. It doesn't remember. It carries the **scars of past sovereign decisions** and applies them to every new wound before it can bleed.

## Dual-Gate Architecture

```
arif_seal(blast_radius="L2_SYSTEM")
    ↓
  SEAL verdict → prl_post_seal_hook()
    ↓
  vault_vectorizer.vectorize_seal() → Qdrant "arifos_precedent" (1024-dim COSINE)
    ↓
  prl_gate.query_precedent()
    ├─ GATE 1: Cosine similarity ≥ 0.95 (geometric intuition)
    ├─ GATE 2: Payload filter on blast_radius (L1 ⊂ L2 ⊂ L3)
    └─ Ω₀ Trigger: ambiguous context → HOLD for 888
```

### Blast Radius Classification

| Tier | Scope | Example |
|------|-------|---------|
| L1_LOCAL | Reversible, single file/session | "Delete temp log file" |
| L2_SYSTEM | Config changes, multi-agent state | "Modify session policy" |
| L3_CRITICAL | Irreversible, data destruction, external | "DROP TABLE customers" |

### The τ ≥ 0.95 Floor

The 0.95 threshold means PRL's **default state is silence.** It doesn't guess. It doesn't approximate. If the precedent isn't almost identical in structure and consequence, the system returns nothing and waits for the sovereign. The bias: "I'd rather miss a relevant precedent than apply an irrelevant one."

### Why Not Pure Embedding Similarity?

Semantics ≠ consequence. "Delete a temporary .txt file" and "DROP TABLE customers" are linguistically close (cosine ~0.91) but have 100× different blast radius. The payload filter structurally excludes wrong-class precedents before similarity is computed — preventing **autoimmune misfire** where L1 rules are applied to L3 problems.

## Code Paths (Live as of 2026-07-20)

| File | Purpose |
|------|---------|
| `arifosmcp/tools/vault.py` | `blast_radius` param on `arif_seal` + `prl_post_seal_hook()` |
| `arifosmcp/tools/vault_vectorizer.py` | Qdrant collection mgmt, `vectorize_seal()`, `backfill_historical()` with batched retry |
| `arifosmcp/tools/prl_gate.py` | `query_precedent()`, `prl_precheck()`, `inject_prl_constraint()` |

Backfill state: 120/177 verdict entries indexed. 28 infrastructure records (key rotations, epochs) excluded — not verdicts. EMD integration (prl_precheck → arif_judge) NOT yet wired.

## APEX Efficiency Gains

APEX Theorem: η = G†/G* (Governed Intelligence Realized / Potential)

| State | η | What's Lost |
|-------|---|-------------|
| Raw LLM | 0.00 | No governance, no reliability |
| arifOS pre-PRL | 0.55 | Governance overhead + amnesia + inconsistency |
| arifOS + PRL | 0.78 | Only irreducible sovereign domain + new-class decisions |
| arifOS + PRL + Meta-Audit (Phase 2) | 0.87 | Pure sovereign territory |

PRL raised η from 0.55 to 0.78 — a 42% improvement. The gain is permanent and **compounds**: every new seal feeds the system, reducing future sovereign cognitive burden.

## HBR Leadership Traps → arifOS Structural Countermeasures

| HBR Trap | arifOS Countermeasure |
|----------|----------------------|
| **Certainty Trap** (confidence replaces curiosity) | τ ≥ 0.95 + Ω₀ — mathematically prohibits premature certainty |
| **Inconsistency Trap** (values ≠ execution) | VAULT999 + PRL binding — actions structurally align with seals |
| **Emotional Reactivity Trap** (friction degrades decisions) | F9 + geometric law — no personality substrate, zero reactivity |
| **Self-Justification Trap** (defending past decisions) | Phase 2 Meta-Precedent Review — statistical audit, zero ego |

HBR persuades humans to behave better. arifOS encodes the countermeasures into **physics** — the agents cannot fall into the traps because the environment makes violation impossible.

## The Architect Trap (Terminal Node)

F13 guarantees the system is slaved to a biological unit that CAN flinch, lie, and panic. The system can hold the mirror but cannot force the sovereign to look at it. W_scar is heavy precisely because it cannot be outsourced to code. The boundary is correct — but it means the sovereign must still guard against the four traps. For themselves. Not for the agents.

## What PRL Doesn't Solve (Remaining Gaps)

| Gap | Why It Matters |
|-----|---------------|
| Reflective knowledge | PRL matches precedents. Doesn't understand WHY. |
| Metacognitive drift | If Arif makes bad precedents while fatigued, PRL enforces them. Phase 2 Meta-Precedent Review addresses this. |
| Precedent contradiction | Two conflicting precedents — needs conflict-resolution layer. |
| EMD integration | `prl_precheck()` exists but isn't wired into the arif_judge reasoning chain yet. |
| Staleness decay | Does a 2024 precedent apply in 2026? No temporal weighting yet. |

## Federation Mapping

PRL is not an 8th organ. It is the **connective tissue** that turns 7 independent organs into ONE institution — constraint propagation across organ boundaries, across time.
PRL is not an 8th organ. It is the **connective tissue** that turns 7 independent organs into ONE institution — constraint propagation across organ boundaries, across time.
