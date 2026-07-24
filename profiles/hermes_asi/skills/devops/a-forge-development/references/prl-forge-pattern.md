# PRL (Precedent Retrieval Layer) Forge Pattern

Forged 2026-07-20 across Hermes + OpenCode + Kimi + Forge.  Updated 2026-07-20 with
live deployment findings.

## Architecture: Dual-Gate Precedent Enforcement

```
Query → blast_radius classification → Qdrant payload-filtered search
  → τ≥0.95 cosine check → Ω₀ ambiguity detection
  → PRL_MATCH (inject constraint) | PRL_NONE (proceed) | PRL_OMEGA0_HOLD
```

**Canonical files (live in production, kanon-2026.07.20):**
- `/root/arifOS/arifosmcp/tools/vault_vectorizer.py` — **CANONICAL** 1024-dim BGE-M3 vectorizer with P6 enrichment
- `/root/arifOS/arifosmcp/tools/prl_gate.py` — **CANONICAL** Dual-Gate (payload filter + τ≥0.95 + Ω₀) + `prl_precheck()` + `inject_prl_constraint()`
- `/root/arifOS/arifosmcp/tools/reason.py` — PRL gate wired into `arif_think` ENCODE phase (after AKAL friction, before mode dispatch)
- `/root/arifOS/arifosmcp/tools/vault.py` — `blast_radius` param on `arif_seal` + `prl_post_seal_hook()` post-seal hook
- `/root/arifOS/arifosmcp/tools/meta_precedent_review.py` — Phase 2 async audit engine
- `/root/arifOS/arifosmcp/tools/judge.py` — `blast_radius` accepted in context dict
- `/root/.local/share/arifos/vault999/seal_chain.jsonl` — canonical seal source (**NOT** outcomes.jsonl)

**Archived / dead code:**
- `/root/arifOS/arifosmcp/prl/*.bak-kimi-2026-07-20` — Kimi's parallel implementation (358+351 lines, archived)
- `/root/.agents/lib/vault_vectorizer.py` — Forge standalone (768-dim nomic-embed-text, archived)
- `/root/.agents/lib/prl_gate.py` — Forge standalone (not connected to arifOS)

**Key architectural decision — canonical path:** We resolved a 3-way split-brain:
1. Arif's original: `/root/.agents/lib/` (768-dim, dead)
2. Kimi's: `/root/arifOS/arifosmcp/prl/` (1024-dim, archived)
3. Canonical: `/root/arifOS/arifosmcp/tools/` (1024-dim, deployed, git-tracked)

## EMD Wiring — The Injection Pattern

PRL runs in `arif_think` at the ENCODE phase (after AKAL friction, before any LLM cycles):

```python
# arifosmcp/tools/reason.py — arif_think function
_prl_result = _prl_precheck(query or "", _blast_radius)

if _prl_result.get("hold_for_888"):       # Ω₀ trigger
    return Synthesis(HOLD)                 # Hard halt, zero LLM tokens burned

if _prl_result.get("block_precedent"):     # τ ≥ 0.95
    context["prl_precedent"] = _prl_result # Attach for downstream injection
    context["_prl_tau_max"] = _prl_result.get("tau_max", 0.0)

# τ < 0.95 → pass-through (zero latency, sub-millisecond Qdrant ping)
# PRL error → pass-through (non-blocking, never blocks reasoning)
```

## P6 Enrichment: The Complete Pattern

Built three functions in `vault_vectorizer.py`:

### 1. `_infer_category(action, metadata)` — Structural Heuristics
9 domain categories inferred from action strings:
- `surface_gate.*` → `security.surface_control`
- `vector.*` / `qdrant.*` → `database.vector_index`
- `emd.*` / `prl.*` / `gate.*` → `architecture.emd_pipeline`
- `file_write` / `forge` / `mutate` → `system.code_generation`
- `init` / `session` / `bootstrap` → `governance.session_lifecycle`
- `seal` / `judge` / `verdict` → `governance.constitutional`
- `geox` / `basin` / `seismic` → `geoscience.earth_model`
- `wealth` / `capital` → `finance.capital_intelligence`

### 2. `_synthesize_vector_text(entry)` — Dense Semantic Document
Builds multi-field text for BGE-M3 embedding WITHOUT mutating seal_chain.jsonl:
```
Domain Category: geoscience.earth_model
Execution Action: mcp.call.geox.basin.ok
Operational Context: tool: basin | source: aaa-a2a-gateway
Blast Radius Authority: L2_SYSTEM
Institutional Verdict: SEAL
Actor: aaa-bridge
```

### 3. `_build_enriched_payload(...)` — Enhanced Qdrant Schema
Qdrant payload includes BOTH the original seal data AND derived fields:
- `enriched_category` — inferred domain
- `derived_semantic_text` — the embedded text
- `is_derived: True` — marks enriched entries
- `payload_summary` — raw JSON (first 500 chars, for audit)
- Original seal fields: `entry_id`, `blast_radius`, `vault_seq`, `vault_hash`, etc.

## Critical Pitfall: outcomes.jsonl ≠ seal_chain.jsonl

**outcomes.jsonl** is a tool-call log (actions: terminal, patch, read_file) — 4567 entries of flat execution records. Every entry has `action: "terminal"` or `action: "patch"`. Embedding this produces useless clusters.

**seal_chain.jsonl** is the sovereign seal chain (~230 entries) with `payload.action` like `mcp.call.geox.basin.ok`, `forge.deliver.seal_chain.js`, `a2a.general` — rich semantic diversity. This is the CORRECT source for PRL vectors.

**Also:** outcomes.jsonl contains string entries (not dicts) that crash the backfill. Always `isinstance(entry, dict)` guard when reading.

## Qdrant Point ID Format — Critical Pitfall

Qdrant requires UUIDs or unsigned integers for point IDs. Integer `seq` values (1, 2, 3...) are rejected:
```
"value 1 is not a valid point ID, valid values are either an unsigned integer or a UUID"
```

**Fix:** Convert entry IDs to deterministic UUIDs:
```python
qdrant_point_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f"vault999:{entry_id}"))
```

The same VAULT999 entry always maps to the same Qdrant point (idempotent backfills).

## Qdrant Client API — `query_points` not `search`

Qdrant client v1.x uses `client.query_points()`, not `client.search()`:
```python
results = client.query_points(
    collection_name="arifos_precedent",
    query=vector,
    query_filter=Filter(...),
    limit=top_k,
    score_threshold=0.95,
    with_payload=True,
).points  # ← .points to get the list
```

## BGE-M3 Cosine Calibration — τ Threshold Reality

**Critical finding (2026-07-20):** BGE-M3 (1024-dim) cosine similarity:
- **τ=1.000** — verbatim text match (same derived text)
- **τ≈0.74-0.78** — semantically related domain queries
- **τ≈0.77** — highly specific queries about domain content

The τ≥0.95 threshold requires **near-verbatim** text match with BGE-M3. Semantically related but not identical text clusters at 0.74-0.78.

**This is NOT a bug.** It's the correct behavior of a general-purpose embedding model. τ≥0.95 means "structurally isomorphic text" — the institution should only fire on very close matches.

**For higher recall:** consider a dual-tier approach (0.95 LAW + 0.80 ADVISORY) or fine-tune embeddings for constitutional/legal text.

## Backfill Resilience — Batches + Retry + Cooldown

When embedding 200+ entries via local BGE-M3:

```python
# batch_size=10, batch_cooldown=3.0 seconds between batches
# Exponential backoff: 2s → 4s → 8s → 16s for transient failures

for batch_idx in range(batch_count):
    for entry in batch:
        vector = _embed_with_retry(summary_text, dim=1024, max_retries=4)
        client.upsert(...)
    time.sleep(batch_cooldown)  # Let Ollama queue clear
```

**Key settings:**
- `batch_size=10` (never >10 — overwhelms local Ollama)
- `batch_cooldown=3.0s` between batches
- `max_retries=4` with exponential backoff (2, 4, 8, 16 seconds)
- `timeout=15` for Ollama HTTP (not 30+)
- 230 entries → ~60 seconds total

## arif_seal from Terminal — SealOutput is Pydantic, not dict

When calling `arif_seal` from terminal Python:
```python
import asyncio
from arifosmcp.tools.vault import arif_seal
r = asyncio.run(arif_seal(mode="seal", ...))
# r is SealOutput (Pydantic model) — use r.verdict, r.entry_id, NOT r.get()
print(f"verdict={r.verdict} entry={r.entry_id}")
```

**Pitfall:** The kernel may return HOLD: MISSING_WITNESS — requires tri-witness (F3) for irreversible seals. Sovereign must seal through authenticated MCP session with full witness channels.

## Post-Seal Hook Pattern

After every successful `arif_seal`, the post-seal hook fires in vault.py:
```python
# Around line 527 in vault.py, after EUREKA777 hook
if result.get("verdict") == "SEAL":
    from arifosmcp.tools.vault_vectorizer import prl_post_seal_hook
    prl_post_seal_hook(entry_id, payload, blast_radius, session_id)
```

This ensures every new seal is automatically vectorized into Qdrant.

## Phase 2: Meta-Precedent Review

`/root/arifOS/arifosmcp/tools/meta_precedent_review.py` — async audit engine:
- Clusters Qdrant vectors by `enriched_category`
- Computes cluster median `blast_radius`
- Flags entries with deviant classifications AND cosine ≥ 0.70 to centroid
- Output: `/root/forge_work/YYYY-MM-DD/review_required.json`
- Non-mutating — read-only Qdrant access
- Currently manual run; cron deferred until precedent density justifies it

## Conformance Spine v2 Envelope Fix

When arifOS response envelope changed:
- `kernel` and `observe_only` are no longer top-level fields in v2 envelope
- `called_from_kernel` signals v2 envelope
- Fix: probe both extracted dict AND raw parsed dict
- Commit `2fb1090b8`: spine 7/9 → 9/9
