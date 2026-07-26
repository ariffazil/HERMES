# Derived Semantic Views Over Immutable Data

Pattern forged 2026-07-20 during PRL Phase 1 (P6 enrichment).

## The Problem

You have an immutable, hash-chained, ed25519-signed ledger (VAULT999 seal_chain.jsonl).
The entries contain sparse structured data — verdict codes, action names, actor IDs —
but lack the semantic density needed for vector similarity matching.

You CANNOT modify the ledger (F1 AMANAH, F2 TRUTH — cryptographic chain integrity).

## The Solution: Derived-View Architecture

Build a **non-destructive enrichment layer** that:
1. Reads the immutable source (read-only)
2. Synthesizes a semantically dense document from sparse fields
3. Embeds the derived text (not the raw source)
4. Stores BOTH the derived embedding AND the original payload in the search index

```
VAULT999 (Immutable Ledger)
  [230 JSONL Receipts]
       │
       ▼ (Read-Only)
┌──────────────────────────────────────┐
│  vault_vectorizer.py (Enrichment)     │
│                                       │
│  1. Parse payload.action + metadata   │
│  2. Infer category from action        │
│  3. Synthesize derived document       │
│  4. Embed derived text (not raw JSON) │
└──────────────────────────────────────┘
       │
       ▼ (1024-dim BGE-M3)
Qdrant (arifos_precedent)
  payload: { original fields + enriched_category + derived_semantic_text }
```

## Implementation Pattern

### 1. Category Inference from Structural Heuristics

```python
def _infer_category(action: str) -> str:
    """Derive domain category from action string patterns."""
    action_lower = str(action).lower()

    HEURISTICS = {
        "security.surface_control": ["surface_gate", "surface.pin"],
        "database.vector_index": ["vector", "qdrant", "embed", "upsert"],
        "architecture.emd_pipeline": ["emd", "prl", "gate", "precedent"],
        "system.code_generation": ["file_write", "forge", "mutate", "commit"],
        "governance.session_lifecycle": ["init", "session", "bootstrap"],
        "governance.constitutional": ["seal", "judge", "verdict", "hold"],
        "geoscience.earth_model": ["geox", "basin", "seismic", "well"],
        "finance.capital_intelligence": ["wealth", "capital", "npv", "irr"],
    }

    for category, keywords in HEURISTICS.items():
        if any(kw in action_lower for kw in keywords):
            return category
    return "UNCATEGORIZED"
```

### 2. Dense Document Synthesis

```python
def _synthesize_vector_text(entry: dict) -> str:
    """Build a semantically dense document for embedding."""
    payload = entry.get("payload", {})
    action = payload.get("action", "")
    verdict = entry.get("verdict", "SEAL")
    blast_radius = entry.get("blast_radius", "L2_SYSTEM")
    actor = entry.get("actor", "")

    metadata = payload.get("metadata", {})
    context_parts = []
    for key in ("reason", "query", "tool_name", "target_file"):
        val = metadata.get(key, "")
        if val:
            context_parts.append(f"{key}: {str(val)[:200]}")

    category = entry.get("category") or _infer_category(action)

    return (
        f"Domain Category: {category}\n"
        f"Execution Action: {action}\n"
        f"Operational Context: {' | '.join(context_parts) or 'no_context_available'}\n"
        f"Blast Radius Authority: {blast_radius}\n"
        f"Institutional Verdict: {verdict}\n"
        f"Actor: {actor}"
    )
```

### 3. Enhanced Qdrant Payload

```python
def _build_enriched_payload(entry, entry_id, blast_radius, derived_text, raw_json):
    """Store BOTH original and derived data."""
    return {
        "entry_id": entry_id,
        "blast_radius": blast_radius,
        "payload_summary": raw_json[:500],    # Original (for audit)
        "enriched_category": category,         # Derived
        "derived_semantic_text": derived_text, # Derived (this was embedded)
        "is_derived": True,                    # Marks enriched entries
    }
```

## Key Principles

1. **Never mutate the source.** Original JSON preserved in `payload_summary`.
2. **Derived fields are clearly marked.** `is_derived: True` flag.
3. **Index is disposable.** Drop Qdrant, re-run backfill — truth is in VAULT999.
4. **Embed the derived text, store the original.** Vector comes from synthesis; payload has raw JSON for audit.
5. **Deterministic IDs.** `uuid.uuid5(NAMESPACE_OID, f"vault999:{entry_id}")` for idempotent re-runs.

## Forward vs Backward

- **Backfill:** Use `_infer_category()` for historical entries lacking category tags.
- **Forward:** New seals should include explicit `blast_radius`, `category`, `reason` so enrichment is unnecessary.
