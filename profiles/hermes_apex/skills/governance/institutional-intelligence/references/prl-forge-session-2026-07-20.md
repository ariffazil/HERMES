# PRL Forge Session — 2026-07-20

## Files Forged

| File | Purpose |
|---|---|
| `arifosmcp/prl/__init__.py` | Public API: PrlGate, PrlGateResult, classify_blast_radius |
| `arifosmcp/prl/prl_gate.py` | Dual-Gate: payload filter + τ≥0.95 + Ω₀ trigger |
| `arifosmcp/prl/vault_vectorizer.py` | VAULT999 → Qdrant arifos_precedent, BAAI/bge-m3 |
| `arifosmcp/prl/prl_emd_hook.py` | EMD integration hook, non-fatal, kill-switch |
| `arifosmcp/schemas/verdict.py` | +BlastRadius enum, +SealOutput.blast_radius field |
| `arifosmcp/tools/vault.py` | +blast_radius param, +post-seal PRL auto-vectorize |
| `arifosmcp/tools/vault_vectorizer.py` | Bridge hook (arif_seal calls this → delegates to prl/) |
| `arifosmcp/runtime/mind_reason.py` | EMD wire: PRL injection BEFORE call_llm() |
| `tests/test_prl.py` | 17/17 pass, 2 Qdrant-dependent skipped |
| `/root/.agents/lib/vault_vectorizer.py` | OpenCode's Ollama-based vectorizer (nomic-embed-text) |

## Ollama Backfill Pattern

**Problem:** Ollama timeouts when embedding 230 seals sequentially. Local GPU queue overwhelmed.

**Fix:** Exponential backoff retry pattern for get_embedding():
- `timeout=15` per request (not 60)
- On 408/429/502/503/504 → retry with `backoff_factor ** attempt` delay
- Max 4 retries, max delay 30s
- Batch chunking: embed 10, sleep 1s cooldown, upsert 25
- Graceful degradation: skip failing seals, continue the rest

**Commits:**
- `c96ced398` — PRL Phase 1: BlastRadius + Dual-Gate + Vectorizer baseline
- `46fedcd2b` — PRL EMD wire: inject precedent constraints into arif_think LLM pipeline
- `2fb1090b8` — Conformance spine: 7/9 → 9/9, v2 envelope compatibility fix

## Key Architectural Decisions

1. **blast_radius at seal time, NOT at query time:** Sovereign classifies consequence. PRL enforces compartmentalisation. Auto-classification at query time is heuristic only.
2. **τ = 0.95, not 0.70-0.80:** Demand near-isomorphic structural alignment. Default is silence, not "maybe."
3. **Ω₀ bypasses LLM entirely:** Zero tokens, zero hallucination risk on ambiguity.
4. **Recency-bias injection:** Constraint appended at END of prompt, not prepended.
5. **η_max = 0.87:** The 13% W_scar tax is the irreducible sovereign domain.
