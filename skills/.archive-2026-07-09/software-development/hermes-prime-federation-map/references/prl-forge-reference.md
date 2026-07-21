# PRL — Precedent Retrieval Layer (Forged 2026-07-20)

The PRL is arifOS's institutional hippocampus — a geometric immune system that auto-retrieves past sovereign verdicts (VAULT999) and enforces them as constitutional constraints before any LLM reasoning cycle executes.

## Architecture Overview

```
arif_seal(blast_radius="L2_SYSTEM", payload="...")
    ↓
  SEAL verdict in VAULT999 (seal_chain.jsonl)
    ↓
  prl_post_seal_hook() → vectorize_seal()
    ↓
  Qdrant "arifos_precedent" (1024-dim COSINE, BGE-M3)
    ↓
  arif_think ENCODE phase:
    prl_precheck(query, blast_radius)
    ├─ τ ≥ 0.95 + payload filter match → inject precedent constraint
    ├─ Ω₀ ambiguity → HALT, return HOLD (zero LLM tokens)
    └─ τ < 0.95 → silent pass-through (sub-millisecond)
```

## Dual-Gate Architecture

| Gate | Mechanism | Purpose |
|---|---|---|
| **GATE 1** | Cosine similarity ≥ 0.95 | Geometric pattern matching |
| **GATE 2** | Qdrant payload filter on blast_radius | Structural consequence boundary |
| **Ω₀ Trigger** | EMD context ambiguity detection | HALT when precedent matched but context unclear |

## Blast Radius Tiers

| Tier | Scope | Examples |
|---|---|---|
| **L1_LOCAL** | Reversible, single file/session | Text formatting, naming conventions, citation rules |
| **L2_SYSTEM** | Modifies config, multi-agent state | Surface gate changes, tool registration |
| **L3_CRITICAL** | Irreversible, data destruction, external | Database drops, Caddy reload, secret rotation |

## Qdrant Technical Pitfalls

### Point ID format — UUIDs ONLY
Qdrant rejects integer IDs. Use deterministic UUIDv5:
```python
import uuid
qdrant_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f"vault999:{entry_id}"))
```

### API method — `query_points`, NOT `search`
Qdrant client v1.x uses `client.query_points()`, not `client.search()`:
```python
results = client.query_points(
    collection_name="arifos_precedent",
    query=vector,
    query_filter=payload_filter,
    limit=top_k,
    score_threshold=0.95,
    with_payload=True,
).points
```

### Collection dimension must match embedding model
- BGE-M3 → 1024-dim (used by arifOS `arifosmcp.intelligence.embeddings.embed()`)
- nomic-embed-text → 768-dim (used by standalone scripts, deprecated for PRL)
- Mismatch → "Wrong input: Vector dimension error: expected dim: X, got Y"

## BGE-M3 Cosine Calibration

From live testing 2026-07-20 with 140+ enriched vectors:

| Query Type | Typical τ |
|---|---|
| Exact/verbatim match against derived text | **1.000** |
| Semantically related domain query | 0.74–0.78 |
| Random query against sparse historical seal | 0.67–0.70 |

**Implication:** τ=0.95 with BGE-M3 requires near-verbatim structural isomorphism. Semantically related but not identical queries cluster at ~0.77. This is correct behavior for a general embedding model — the threshold is calibrated for precision, not recall.

## Ollama Backfill Pattern

For batch embedding 200+ entries through local Ollama without timeouts:

```python
batch_size = 10           # Process 10 at a time
batch_cooldown = 3.0      # 3s between batches
exponential_backoff = [2, 4, 8, 16]  # seconds per retry

# Embedding call MUST have timeout + retry
def _embed_with_retry(text, dim=1024, max_retries=4):
    for attempt in range(max_retries + 1):
        try:
            return embed(text, dim=dim)
        except Exception:
            if attempt < max_retries:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"Embed failed after {max_retries} retries")
```

OLLAMA_URL must be `http://localhost:11434/api/embed` (not just the base URL).

## arif_seal Pitfalls

### Returns Pydantic model, NOT dict
```python
# WRONG
r = await arif_seal(...)
print(r.get('verdict'))  # AttributeError: 'SealOutput' object has no attribute 'get'

# CORRECT
print(r.verdict)  # Pydantic attribute access
print(r.entry_id)
print(r.blast_radius)
```

### Requires authenticated session for SEAL
`OBSERVE_ONLY` sessions return `HOLD: MISSING_WITNESS` or `888_HOLD: IRREVERSIBLE requires non-anonymous actor_id`. Only sovereign-authenticated sessions can seal.

### Payload can be lost
The `arif_seal` terminal command can complete with `verdict=SEAL` but empty payload if called incorrectly. Always verify the seal was written to `seal_chain.jsonl` after execution.

## Post-Seal Hook Pattern

In `vault.py`, after EUREKA777 and Route 3 hooks:
```python
# After successful seal, vectorize into PRL
from arifosmcp.tools.vault_vectorizer import prl_post_seal_hook
prl_post_seal_hook(entry_id, payload, blast_radius, session_id)
```

The hook embeds a DERIVED SEMANTIC DOCUMENT (not raw JSON) using `_synthesize_vector_text()`, which extracts: domain category, execution action, operational context, blast radius, verdict, actor. The raw JSON payload is stored in Qdrant for audit.

## Enrichment Protocol (P6)

Historical seals are sparse (action names, generic verdicts). The enrichment layer derives semantic density:
1. `_infer_category(action)` → maps action strings to 9 domain categories (security.surface_control, database.vector_index, architecture.emd_pipeline, etc.)
2. `_synthesize_vector_text(entry)` → builds multi-field derived document for embedding
3. `_build_enriched_payload()` → enhanced Qdrant schema with `enriched_category`, `derived_semantic_text`, `is_derived`

**Critical invariant:** VAULT999 seal_chain.jsonl is NEVER modified. All enrichment is in the derived view only (Qdrant payload).

## File Locations (Canonical)

| Component | Path | Status |
|---|---|---|
| PRL gate | `/root/arifOS/arifosmcp/tools/prl_gate.py` | ✅ Canonical, committed |
| Vectorizer | `/root/arifOS/arifosmcp/tools/vault_vectorizer.py` | ✅ Canonical, committed |
| EMD wiring | `/root/arifOS/arifosmcp/tools/reason.py` (line 1036) | ✅ Deployed |
| Blast radius | `/root/arifOS/arifosmcp/tools/vault.py` (line 58) | ✅ Deployed |
| Qdrant collection | `arifos_precedent` (localhost:6333) | ✅ 140+ vectors |
| Dead code | `/root/arifOS/arifosmcp/prl/*.bak-kimi-*` | 📦 Archived |
| Dead code | `/root/.agents/lib/` | 📦 Forge standalone |

## Honest Carry-Forward

1. τ=0.95 won't fire on historical seals — BGE-M3 clusters at ~0.77 for semantic matches. Only near-verbatim queries trigger.
2. The first sovereign antibody exists (Morley et al 2023 citation rule) but at τ=0.75 for natural queries.
3. 28 historical entries in seal_chain.jsonl cannot be indexed (no entry_id — key rotations, epochs, actor signatures).
4. Post-seal hook vectorizes with entry_id + blast_radius template, not full derived text — future seals need richer context passed through the hook.
