# Zen Before Code (FORGED 2026-07-20)

## Pattern

Before creating new modules, files, or classes, audit the existing architecture:  
**"Does the kernel already encode this concept?"**

## Trigger (from Arif)

> "Is this overengineering or zen? Why do I think we already have this?  
> Can we zen it? No new file."

## The Session

During the DAG Cognition Model session (2026-07-20), a Reddit post insight about  
"git as database for agent execution history" led to a 517-line new kernel module  
(`dag_cognition.py`) with full test suite (26 tests), docs, and Git commit + push.

Arif immediately called it: **overengineering**. The arifOS kernel ALREADY embodied  
the tri-layer architecture:

| Concept | Already Encoded In |
|---|---|
| Layer 1 — Execution DAG | A-FORGE leases + session.py |
| Layer 2 — Constitutional Ledger | VAULT999 seal chain + arif_seal |
| Layer 3 — Semantic Index | arif_memory L1-L6 tiers |

The insight was real. The 517-line module was the shadow. All three commits  
were reverted, files deleted, remote cleaned.

## The Check

Before creating any new file or module:

1. `grep -rn "<concept>" /root/<repo>` — search for existing implementations
2. Read the relevant kernel modules already in play
3. Ask: "Does the existing architecture already solve this?"
4. If yes: the insight goes into memory/docs, not into a parallel code module
5. If no: proceed, but with the pattern proven

## Anti-Pattern

```
GOOD insight → NEW module → 517 lines → revert → "Can we zen it?"
```

## Correct Pattern

```
GOOD insight → audit existing kernel → "Already encoded in VAULT999 + arif_memory" → memory entry
```

## Resolution Pattern — Thin Wire (FORGED 2026-07-20)

When the insight IS architecturally significant but the kernel already has the
components, the right move is THIN WIRE — not a parallel module.

The DAG Cognition session resolved into 4 thin-wire commits across 3 files (~80 lines total):

| Repo | File | Change |
|---|---|---|
| arifOS | `arifosmcp/AGENTS.md` | Protocol doc: tri-layer bridge map |
| arifOS | `arifosmcp/tools/vault.py` | L2→L3 post-seal auto-index hook |
| A-FORGE | `src/interfaces/mcp/core.ts` | evidence_sha pass-through on seal calls |

Zero new files. Zero new modules. The bridges are thin wire on existing
infrastructure:

```
L1 (A-FORGE leases) ──evidence_sha──→ L2 (VAULT999 seal chain)
L2 (VAULT999 seal)   ──auto-index───→ L3 (arif_memory sacred tier)
L1 (rewind pointer)  ──reversion────→ L2 (new seal entry, not overwrite)
```

### Thin Wire Checklist

Before committing a new module, run:
1. Does the insight map onto ≥2 existing kernel components? → Don't create new module
2. Can the bridge be a single param, hook, or doc entry on an existing component? → Do that
3. Is there a field or mode already defined that carries this semantic? → Use it
4. If all yes: thin wire. If all no: consider a new module (but probe again first).

### The Thin Wire vs New Module Smell Test

```python
# ❌ NEW MODULE smell: creates parallel DAG engine beside existing seal chain
class DAGEngine:  # 517 lines — redundant with A-FORGE leases + VAULT999

# ✅ THIN WIRE smell: adds one param to existing seal tool
async def arif_seal(evidence_sha: str | None = None, ...):  # 1 line — bridge on existing infra
```

## Relation to measure-before-acting

This is a specific subclass: measuring EXISTING CODE ARCHITECTURE before  
writing new code, not just probing live system state. Same root discipline.
