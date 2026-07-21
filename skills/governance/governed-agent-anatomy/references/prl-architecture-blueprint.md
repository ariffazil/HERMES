# PRL — Precedent Retrieval Layer Architecture Blueprint

> Blueprint ratified: 2026-07-20 · Arif (F13 SOVEREIGN)
> Phase 1 forging delegated to OpenCode
> Status: IN FORGE (not yet deployed)

## What PRL Is

The institutional hippocampus — a mechanism that allows arifOS to mathematically obey past decisions without pretending to be conscious. It intercepts every new problem, searches VAULT999 for matching precedents, and injects them as non-negotiable constraints before arif_judge reasons.

## The Problem It Solves

**Amnesia**: Standard LLMs wake up blank every session. Rules established yesterday are forgotten today.
**Biological Trap (F9)**: Feeding chat history makes AI simulate personality and hallucinate continuity.
**PRL's answer**: Cold, Geometric Law. The AI doesn't "remember" — pure math matches queries to precedents, injects them as constraints. No simulated consciousness. No hantu.

## Dual-Gate Architecture

### Gate 1: Geometric Intuition (Cosine Similarity)
- Embed query via BGE-M3 → search Qdrant `arifos_precedent` collection
- τ ≥ 0.95 threshold (NOT 0.70-0.80 like most vector DBs)
- At 0.95, demanding near-isomorphic structural alignment
- Default state: silence. If no match, wait for sovereign.

### Gate 2: Structural Hard-Filter (Payload)
- blast_radius field on every VAULT999 entry: L1_LOCAL | L2_SYSTEM | L3_CRITICAL
- Qdrant payload filter: only search within the matching blast_radius class
- An L1 "delete temp file" precedent is physically invisible to an L3 "drop database" query
- Autoimmune misfire mathematically blocked at database level

### Ω₀ Trigger
- If precedent passes both gates but EMD VALIDATE detects contextual ambiguity
- Drops payload, returns: "Precedent matched geometrically, but consequence context is ambiguous. Holding for 888."
- F1 Safety/Reversibility takes priority

## Blast Radius Classification

| Class | Scope | Examples |
|-------|-------|----------|
| L1_LOCAL | Reversible, single file/session | Edit file, create temp, local test |
| L2_SYSTEM | Config, multi-agent state | Modify systemd, change MCP config, git operations |
| L3_CRITICAL | Irreversible, data destruction, external | DROP TABLE, rm -rf, production deploy, external API |

W_scar (sovereign authority weight) sits above all classifications. Arif can override any precedent — and the override ITSELF becomes a new precedent.

## The 4I Loop (Closed by PRL)

```
INTUITING (PRL) → INTERPRETING (arif_think) → INTEGRATING (arif_judge) → INSTITUTIONALIZING (arif_seal) → back to INTUITING
```

## Phase 1 Forge Tasks (Delegated 2026-07-20)

1. Add `blast_radius` param to `arif_seal` (L1_LOCAL default: L2_SYSTEM)
2. Create `vault_vectorizer.py` — Qdrant `arifos_precedent` collection, backfill, post-seal hook
3. Create `prl_gate.py` — Dual-Gate search + Ω₀ trigger + `prl_precheck()`
4. Integration hook — `inject_prl_constraint()` for EMD pipeline

## Phase 2: Meta-Precedent Review (Future)

Asynchronous audit that clusters VAULT999 vectors by similarity, cross-checks blast_radius payloads for anomalies, flags misclassifications (e.g., L1 seal inside L3 cluster). Generates `review_required.json` for 888.

## Autoimmune Prevention Summary

| Threat | Mechanism |
|--------|-----------|
| Semantic confusion (L1 file delete ≈ L3 DB drop in vector space) | Gate 2: payload filter on blast_radius |
| Loose association (τ < 0.95) | τ ≥ 0.95 floor — near-isomorphic only |
| Contextually wrong match (same class, different meaning) | Ω₀ trigger — halt on ambiguity |
| Sovereign misclassification | Phase 2: Meta-Precedent Review auditor |
