# PRL Forge Patterns — Qdrant + Embedding + Constitutional Injection

> **Session:** 2026-07-20 — PRL Phase 1 Forge
> **Context:** Building the Precedent Retrieval Layer on top of VAULT999
> **Files:** vault_vectorizer.py, prl_gate.py, reason.py (arif_think),
>   vault.py (arif_seal)

## Pattern 1: Qdrant UUID v5 for Deterministic Point IDs

Qdrant requires UUIDs or unsigned integers as point IDs. When indexing from
a sequential ledger (VAULT999 `seq` values like 1, 2, 3...), convert to UUIDs:

```python
import uuid

entry_id = str(raw_seq)
qdrant_point_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f"vault999:{entry_id}"))
```

**Why UUID v5:** Deterministic — the same `entry_id` always maps to the same
point. Namespace OID ensures no collision with UUIDs from other sources.

**Pitfall:** Qdrant rejects string integers ("1", "2") as point IDs.
Error: `"value 1 is not a valid point ID, valid values are either an
unsigned integer or a UUID"`. Always UUID-encode.

## Pattern 2: query_points() — NOT search()

Qdrant Python client v1.x uses `query_points()`, not `search()`:

```python
# CORRECT (v1.x):
results = client.query_points(
    collection_name="collection",
    query=vector,               # NOT query_vector
    query_filter=payload_filter,
    limit=top_k,
    score_threshold=0.95,
    with_payload=True,
).points                      # .points to get the list

# WRONG (removed in v1.x):
results = client.search(       # AttributeError
    collection_name="...",
    query_vector=vector,        # Wrong kwarg name
)
```

**Pitfall:** If the code uses `client.search(...)`, the error is:
`'QdrantClient' object has no attribute 'search'`

## Pattern 3: Dimension Matching

The Qdrant collection vector size MUST match the embedding function output.

```python
# Check what the embed function returns:
v = embed("test", dim=1024)  # returns 1024-dim vector

# Collection must match:
client.create_collection(
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)
```

**Pitfall:** Mismatch error: `"Wrong input: Vector dimension error: expected
dim: 768, got 1024"`. This happens when nomic-embed-text (768-dim) was used
to create the collection but BGE-M3 (1024-dim) is used for embedding, or
vice versa.

**Fix:** Drop and recreate the collection with the correct dimension:
```python
client.delete_collection(collection_name)
client.create_collection(..., vectors_config=VectorParams(size=1024, ...))
```

## Pattern 4: Batch + Cooldown + Exponential Backoff for Local Embedding

Local Ollama nomic-embed-text/bge-m3 can't handle rapid sequential requests.
Each embedding call takes ~2-4 seconds. Pushing 230 requests without
throttling causes timeouts and dropped connections.

```python
def _embed_with_retry(text: str, dim: int, max_retries: int = 4) -> list[float]:
    """Exponential backoff: 2s → 4s → 8s → 16s"""
    for attempt in range(max_retries + 1):
        try:
            return embed(text, dim=dim)
        except Exception as exc:
            if attempt < max_retries:
                wait = 2 ** (attempt + 1)
                time.sleep(wait)

def backfill(batch_size=10, cooldown=3.0):
    for batch in chunks(entries, batch_size):
        for entry in batch:
            vector = _embed_with_retry(payload, dim=1024)
            client.upsert(...)
        time.sleep(cooldown)  # let Ollama queue clear
```

**Key parameters:**
- `batch_size=10`: Process 10 entries, then cooldown
- `cooldown=3.0`: 3 seconds between batches — lets GPU memory clear
- `max_retries=4`: Exponential backoff 2/4/8/16s — catches transient Ollama overload

## Pattern 5: JSONL Entry Guards

VAULT999 seal_chain.jsonl may contain non-dict entries (strings, mixed
formats). Always guard:

```python
for line in f:
    try:
        entry = json.loads(line)
        if not isinstance(entry, dict):
            continue  # skip non-dict entries
        raw_id = entry.get("entry_id", entry.get("seq", ""))
        if raw_id is None or raw_id == "":
            continue  # skip entries without IDs (key rotations, epochs)
    except json.JSONDecodeError:
        continue  # skip malformed lines
```

**Pitfall:** Without the `isinstance(entry, dict)` guard, string entries
cause: `AttributeError: 'str' object has no attribute 'get'`

## Pattern 6: ENCODE-Phase Gate Injection

The PRL gate runs at the ENCODE phase — after session auth, before any LLM
cycles. Pattern from `arif_think` in reason.py:

```python
# After AKAL friction, before mode dispatch:
try:
    from prl_gate import prl_precheck
    result = prl_precheck(query, blast_radius)

    if result.get("hold_for_888"):
        # Ω₀ TRIGGERED — hard HALT, zero tokens burned
        return Synthesis(verdict="HOLD", ...)

    if result.get("block_precedent"):
        # Attach precedent to context for downstream injection
        context["prl_precedent"] = result
except Exception:
    pass  # PRL is non-blocking — silence on error is correct
```

**Key properties:**
- Non-blocking — PRL error never blocks reasoning
- Zero-latency default — τ < 0.95 returns instantly
- Ω₀ trigger bypasses LLM entirely — no tokens, no hallucination risk

## Pattern 7: ΔS < 0 Forge Discipline

The sequence Arif enforced for PRL:

1. **Blueprint → Ratify** (discussion, not code)
2. **Build foundation first** (vault_vectorizer + prl_gate, no wiring)
3. **Backfill and verify** (120 vectors indexed, Qdrant confirmed)
4. **Commit baseline** (rollback point established)
5. **Wire into critical path** (arif_think ENCODE phase)

**Rule:** Never wire a new gate into the critical path until the data
substrate (Qdrant, embeddings) is verified. F1: if the wire shorts, rewind
to the baseline commit without data loss.

## Pattern 8: SURFACE-GATE Pre-Commit Hook

arifOS has a pre-commit hook that validates all 8 public MCP tools match
the live surface before allowing commits:

```
[SURFACE-GATE] Running surface-map drift check...
[SURFACE-GATE] 🔴 STRICT MODE
🔍 Probing live MCP surface...
   Live MCP tools: 8
✅ SURFACE PINNED — Live tools match surface-map declarations.
```

This prevents tools from being added/removed without registry updates.
All 8 tools were preserved: arif_init, arif_observe, arif_think, arif_route,
arif_memory, arif_judge, arif_forge, arif_seal.

## Commit History

```
4edd04ffc feat: wire PRL gate into arif_think ENCODE phase  (+43 lines)
ec94c2f54 fix: PRL Phase 1 hardening — UUID Qdrant IDs...     (+148/-31)
924ed1cd8 feat: forge PRL Phase 1 — vault_vectorizer + prl... (+636/-6)
```

## Key Files

- `/root/arifOS/arifosmcp/tools/vault_vectorizer.py` — Qdrant index + backfill
- `/root/arifOS/arifosmcp/tools/prl_gate.py` — Dual-gate query + precheck + constraint injection
- `/root/arifOS/arifosmcp/tools/reason.py` — arif_think ENCODE-phase PRL gate (line ~1034)
- `/root/arifOS/arifosmcp/tools/vault.py` — blast_radius on arif_seal + post-seal hook
- Qdrant collection: `arifos_precedent` (1024-dim, COSINE, 120 vectors)
