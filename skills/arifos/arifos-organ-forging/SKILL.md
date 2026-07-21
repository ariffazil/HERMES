---
name: arifos-organ-forging
description: Forge new constitutional organs in arifOS — vector indexing, dual-gate architecture, EMD pipeline integration, Qdrant backfill, derived-view enrichment.
---

# arifOS Organ Forging

Forge new governed organs in the arifOS federation. An "organ" is a multi-component subsystem with vector indexing, constitutional gates, and EMD pipeline integration. Distinct from simple runtime modules (~250-line utilities under `arifosmcp/runtime/`).

## When to Use

When the user describes a new constitutional capability that needs:
- Qdrant vector indexing (precedent, evidence, memory)
- Dual-gate architecture (geometric + structural filters)
- EMD pipeline integration (ENCODE/METABOLIZE/DECODE phases)
- Backfill of historical data
- Blast radius classification (L1_LOCAL / L2_SYSTEM / L3_CRITICAL)
- Post-seal hooks in VAULT999

NOT for: simple runtime utilities, single-file tools, config changes.

## The Forge Sequence

Every organ follows this sequence. Never skip phases.

### Phase 0: Blueprint Ratification
- Define the organ's architecture on paper first
- Map to Ostrom's CDPs (boundaries, monitoring, graduated sanctions, polycentric)
- Map to APEX equation (what does this do to η?)
- Ratify with sovereign before ANY code

### Phase 1: Core Components
Build in this order — each depends on the prior:

1. **Schema** — blast_radius / consequence_class on the seal or input
2. **Vectorizer** — Qdrant collection + embed + backfill script
   - Use `arifosmcp.intelligence.embeddings.embed()` (BGE-M3, 1024-dim)
   - Collection: COSINE distance, 1024-dim
   - Backfill MUST handle: batching (10/batch), cooldown (3s), exponential-backoff retry
   - Qdrant point IDs: UUIDv5 deterministic (`uuid.uuid5(NAMESPACE_OID, f"vault999:{entry_id}")`)
   - `query_points(query=vector, ...).points` — NOT `client.search()` (v1.x API)
3. **Gate** — dual-gate architecture
   - GATE 1: Cosine similarity ≥ 0.95 (Geometric Intuition)
   - GATE 2: Payload filter on blast_radius (Structural Hard-Filter)
   - Ω₀ Trigger: ambiguous context → HOLD for 888
4. **Post-seal hook** — wire into vault.py after EUREKA777 hook
5. **Backfill** — run against seal_chain.jsonl ONLY (not outcomes.jsonl)

### Phase 2: EMD Wiring
- Inject at ENCODE phase (after AKAL friction, before mode dispatch)
- Pattern:
  ```
  prl_result = prl_precheck(query, blast_radius)
  if hold_for_888: return HALT (zero LLM tokens)
  if block_precedent: attach to context
  else: pass through silently
  ```
- Non-blocking — gate failure never stops reasoning

### Phase 3: Deploy and Test
- `make deploy-local` (requires pushed commits)
- Silence test: standard query → PRL passes through silently
- Halt test: query mirroring a sealed precedent → Ω₀ or τ ≥ 0.95 trigger
- SURFACE-GATE must remain green (all 8 tools pinned)

## P6: Derived-View Enrichment

Historical VAULT999 entries lack rich semantic content. The enrichment is a DERIVED VIEW — it NEVER mutates the immutable ledger.

### `_synthesize_vector_text(entry)` — Build dense embedding document
Extract: Domain Category, Execution Action, Operational Context, Blast Radius, Verdict, Actor.

### `_infer_category(action, metadata)` — Structural heuristics
Map action patterns to domain categories:
- `surface_gate.*` → `security.surface_control`
- `vector.* / qdrant.*` → `database.vector_index`
- `emd.* / prl.*` → `architecture.emd_pipeline`
- `geox / basin / seismic` → `geoscience.earth_model`
- `seal / judge / verdict` → `governance.constitutional`

### `_build_enriched_payload()` — Enhanced Qdrant schema
Add `enriched_category`, `derived_semantic_text`, `is_derived: true`, `vault_seq`, `vault_hash`.

## Key Pitfalls

### Split-Brain Implementations
When multiple agents (OpenCode, Forge, Kimi, Hermes) work on the same organ, check for parallel implementations BEFORE continuing. Probe the filesystem:
```
search_files(pattern='vault_vectorizer.py', path='/root')
```
Archive dead paths with `.bak-<agent>-<date>` suffix. Commit the canonical version.

### Qdrant Point ID Format
Integer IDs from VAULT999 are rejected. Use UUIDv5 deterministically. Never use raw strings or integers.

### Qdrant API
`client.search()` does NOT exist. Use `client.query_points(query=vector, query_filter=..., limit=N, score_threshold=0.95, with_payload=True).points`

### Collection Dimension Consistency
BGE-M3 = 1024-dim. nomic-embed-text = 768-dim. Never mix. The `embed()` function from `arifosmcp.intelligence.embeddings` handles BGE-M3. Always specify `dim=1024`.

### τ Threshold Design
The 0.95 floor means the default state is SILENCE. Historical infrastructure seals won't trigger. Only new seals with rich, domain-specific reasons will compound. This is correct behavior — not a bug. The institution compounds forward, not backward.

### outcomes.jsonl
Contains string entries and 4567 lines. Use `seal_chain.jsonl` (230 lines, structured dicts) for backfill. Add `isinstance(entry, dict)` guard.

## Commands Reference

```bash
# Backfill
cd /root/arifOS && PYTHONPATH=src uv run python -c "
from arifosmcp.tools.vault_vectorizer import backfill_historical
r = backfill_historical(vault_dir='/root/.local/share/arifos/vault999', batch_size=10, batch_cooldown=3.0)
print(r)
"

# Check Qdrant
PYTHONPATH=src uv run python -c "
from qdrant_client import QdrantClient
c = QdrantClient(url='http://localhost:6333')
print(c.count('arifos_precedent', exact=True))
"

# Deploy
cd /root/arifOS && git push origin main && make deploy-local
```

## References

- `references/prl-forge-2026-07-20.md` — Full PRL implementation trace
- Root skill: `arifos-runtime-module-authoring` — for simple runtime modules

## APEX Equation Impact

Every new organ shifts η upward. Key principle: **η should never reach 1.00.**

- η = 0.55: Pre-PRL (governance overhead + amnesia + inconsistency)
- η = 0.78: Post-PRL (precedent auto-injection)
- η = 0.87: Theoretical maximum for governed intelligence
- Remaining 13% = W_scar tax — irreducible sovereign domain (new-class decisions, F13 override)

An η of 1.00 is NOT efficiency — it's a rogue system. The gap is the cost of staying human.

## The Architect Trap

The sovereign (F13) is above the system but still subject to human cognitive traps:
- Certainty, inconsistency, emotional reactivity, self-justification
- Phase 2 Meta-Precedent Review partially addresses this (auditing W_scar classifications)
- Full "Sovereign Trap" countermeasure would require authority the system can never have
- This is correct — the boundary between institution and sovereign is non-negotiable

## Arif's Terminal Preference

Arif hates typing in terminals. "Aku benci terminal weiiii." When providing commands:
- Use single-line `uv run python -c "..."` one-liners, not multi-step SSH sessions
- Execute directly via MCP tools when possible
- When a seal requires sovereign authority, call arif_seal via MCP rather than asking Arif to SSH
- Prefer `python3 << 'EOF' ... EOF` heredocs for multi-line scripts

## Deploy Gotchas

- `make deploy-local` fails if local HEAD ≠ origin/main → `git push origin main` first
- SURFACE-GATE pre-commit hook verifies 8 MCP tools match live surface
- Conformance spine runs post-deploy; 7/9 → 9/9 fix pattern: v2 envelope compatibility
- Kernel version shows as `kanon-YYYY.MM.DD+<commit>` after deploy

## Verdicts

DITEMPA BUKAN DIBERI. Every organ is forged through trace, not declared into existence.
