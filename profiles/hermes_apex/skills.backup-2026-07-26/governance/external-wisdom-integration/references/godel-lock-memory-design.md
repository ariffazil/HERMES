# Gödel Lock — Governed Memory Design Spec

> Extracted from 2026-07-12 session: memory architecture + industry maturity assessment.

## The Trust Bootstrap Paradox

Memory cannot certify itself. To determine whether a memory is trustworthy, you already need trusted evidence, provenance, policy, and judgment. The memory system needs an **external authority** — arifOS F1-F13.

## The Gödel Lock (6 checks)

Every memory entry must pass all 6:

| ID | Check | Fails If |
|---|---|---|
| GÖDEL-1 | Provenance required | No `provenance.source` |
| GÖDEL-2 | Truth class required | No valid OBS/DER/INT/SPEC |
| GÖDEL-3 | OBS needs evidence | Truth=OBS but no evidence/receipts |
| GÖDEL-4 | Constitutional needs ratification | Authority=constitutional but no `ratified_by` |
| GÖDEL-5 | Confidence ceiling | Confidence > max for truth class (OBS=0.90, DER=0.85, INT=0.75, SPEC=0.50) |
| GÖDEL-6 | No self-authorization | `self_authorized=True` |

## Asymmetric Authority Rule

> Memory may automatically reduce authority. Memory may not automatically increase authority.

A remembered scar can trigger HOLD. A remembered success cannot independently grant SEAL.

## Truth Classes (F2 TRUTH)

| Class | Max Confidence | Meaning |
|---|---|---|
| OBS | 0.90 | Directly observed from source |
| DER | 0.85 | Mechanically derived from observations |
| INT | 0.75 | Interpreted from evidence |
| SPEC | 0.50 | Hypothesis requiring testing |

## Authority Levels

| Level | Weight | May Change Routing? | May Restrict Tools? |
|---|---|---|---|
| constitutional | 1.0 | Yes | Yes |
| verified | 0.8 | Yes | No |
| advisory | 0.5 | No | No |
| provisional | 0.3 | No | No |
| blocked | 0.0 | No | No |

## Memory Entry Schema

```json
{
  "id": "mem-xxx",
  "content": "...",
  "truth": {"class": "INT", "confidence": 0.70},
  "authority": {
    "level": "advisory",
    "may_inform_reasoning": true,
    "may_change_routing": false,
    "may_restrict_tools": false,
    "may_expand_tools": false,
    "self_authorized": false
  },
  "provenance": {
    "source": "session:abc",
    "evidence": "...",
    "source_receipts": []
  },
  "applicability": {
    "task_classes": ["*"],
    "models": ["*"],
    "valid_until": "2026-08-12T..."
  },
  "lifecycle": {
    "state": "active",
    "created_at": "...",
    "decay": {
      "confidence_per_month": 0.05,
      "review_after": "2026-08-12T...",
      "expires_on_model_change": false
    }
  }
}
```

## 7 Memory Paradoxes (reference)

1. More memory can make the agent less intelligent
2. Remembering errors converts hallucination into history
3. Personalization can imprison the human
4. Self-editable memory enables learning and self-corruption
5. Compression preserves continuity by destroying detail
6. Retrieval relevance is not decision importance
7. Forgetting is both a defect and an intelligence function

## Industry Maturity (2026)

| Capability | Industry | arifOS |
|---|---|---|
| Persisting history | 9/10 | 8/10 |
| Vector retrieval | 8/10 | 7/10 |
| Temporal contradiction handling | 4/10 | 3/10 |
| Safe autonomous writing | 3/10 | 4/10 |
| Causal value attribution | 2/10 | 1/10 |
| Governed forgetting | 3/10 | 2/10 |
| Memory poisoning resistance | 2/10 | 3/10 |
| Memory-driven authority changes | 2/10 | 1/10 |
