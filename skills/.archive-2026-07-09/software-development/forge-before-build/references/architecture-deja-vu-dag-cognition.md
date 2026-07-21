# architecture-deja-vu — DAG Cognition Model Case Study

**Date:** 2026-07-20
**Session:** Arif reviews Reddit post about git-as-agent-DB

## The Trigger

Reddit post by u/Square_Light1441 on r/AgentsOfAI: "I stopped building a database for my AI agents and just used git."

Core insight: Agent cognition is not a mutable table of facts; it is an immutable,
branching timeline of decisions. Git's DAG model (branches, commits, reflog, plumbing)
natively solves the hardest problems in agentic systems.

## The Overengineering

Hermes built a 525-line `dag_cognition.py` module implementing:
- `DAGNode` — hashed, timestamped commit node
- `DAGSession` — session with branches and subagents
- `DAGEngine` — commit_turn, create_subagent, complete_subagent, rewind
- `TriLayerArchitecture` — L1 (DAG) / L2 (VAULT999) / L3 (Vector Index)
- `SealEvidencePayload` — evidence payload for vault sealing

## Arif's Zen Intervention

> "Is this overengineering or zen?? Why do I think we already have this?? Can we zen it?? No new file."

## What Already Existed

| dag_cognition.py class | Already exists as... |
|---|---|
| `DAGNode` | Every `arif_seal` entry (SHA, timestamp, payload, trailers, epistemic label) |
| `DAGSession` | `arif_init` session + session token + `arif_memory` trail |
| `DAGEngine.commit_turn` | `arif_seal` mode=seal — the vault IS the commit engine |
| `DAGEngine.create_subagent` | `arif_forge` with lease — subagent spawning already exists |
| `DAGEngine.complete_subagent` | Subagent-Result trailer in seal metadata |
| `DAGEngine.rewind` | New concept — but expressed as `reversion_event` field on SealOutput |
| `TriLayerArchitecture` | Documentation header, not code |
| `SealEvidencePayload` | `evidence_sha` field on `SealOutput` |

## The Zen Fix

- **Deleted:** `dag_cognition.py` (525 lines), `test_dag_cognition.py` (382 lines), `__init__.py` imports
- **Kept:** Two fields on `SealOutput`:
  - `evidence_sha: str | None` — terminal SHA of subagent execution branch
  - `reversion_event: dict | None` — {previous_sha, reason, new_sha}
- **Result:** 958 lines → 20 lines. Zero new files. Backward compatible.

## The Lesson

The EUREKA was real but the architecture already had it. `arif_seal` entries are DAG nodes.
VAULT999 is the commit log. The Reddit post confirmed what arifOS already built — it didn't
teach us something new. The zen is removing the lesson plan and keeping the vocabulary.

## Pattern Recognition

When you find yourself writing a new class that has a 1:1 mapping to an existing concept:
1. Stop.
2. Map each method to the existing tool/entity.
3. If the mapping is complete, add a field, not a file.
4. If the mapping is partial, add a MODE to the existing tool, not a new tool.
5. Only create a new module when no existing surface can carry the concept.
