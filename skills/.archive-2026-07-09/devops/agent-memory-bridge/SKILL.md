---
name: agent-memory-bridge
description: >
  Bridge OpenClaw session logs to arifOS L4 (Postgres), L5 (Graphiti), L6 (Vault999).
  Extract facts, decisions, and verdicts from sessions and persist them to the
  constitutional memory substrate. USE WHEN: "sync session to arifOS",
  "bridge memory", "session to vault", "extract to Graphiti".
---

# Agent Memory Bridge

**Connects OpenClaw session context → arifOS constitutional memory layers.**

## The Problem

OpenClaw has `openclaw-memory` (community SQLite + x402). arifOS has L1–L6 (ephemeral → vault). They are separate stores. Key decisions made in OpenClaw sessions don't automatically reach Vault999.

## What It Bridges

### OpenClaw Session → arifOS L4 (Postgres)
```bash
# Export recent session events to Postgres
# Table: session_events (session_id, actor_id, event_type, payload, timestamp)
psql $ARIFOS_CONN -c "
INSERT INTO session_events (session_id, actor_id, event_type, payload, timestamp)
SELECT 'session_$(date +%Y%m%d)', 'openclaw', 'skill_audit',
  json_build_object('skill', '$SKILL', 'action', '$ACTION', 'ts', NOW()),
  NOW()
ON CONFLICT DO NOTHING;
"
```

### OpenClaw Session → arifOS L5 (Graphiti)
```
# Create entity links in Graphiti
# e.g., "user:arif" → performed → "skill:deep-research"
# e.g., "session:X" → used → "model:minimax-m2.7"
# e.g., "agent:openclaw" → decided → "verdict:SEAL"
```

### Critical Decisions → arifOS L6 (Vault999)
Sealed entries:
- `888_JUDGE` verdicts
- Constitutional floor violations detected
- Model fallback events (DeepSeek 402)
- Federation node failures
- Security audit results

## Bridge Triggers

| Session Event | → arifOS Layer |
|---|---|
| Skill installed/removed | L4 Postgres |
| MCP crash/restart | L4 + L5 |
| Constitutional audit result | L6 Vault999 |
| Model switch | L4 |
| Security finding | L6 Vault999 |
| Human veto | L5 Graphiti + L6 |

## Usage

```bash
# Bridge last session's key decisions to arifOS
bridge-session --session-id omega-forge-2026-05-17 --layers l4,l5,l6

# Bridge a specific verdict
bridge-verdict --verdict SEAL --actor Arif --context "DeepSeek 402 hotfix"

# Full sync of recent sessions
bridge-recent --hours 24 --confirm
```

## Skills Used

- `arifos-memory` (L3–L6 access)
- `session-logs` (read session history)
- `arif_vault_seal` (L6 immutable ledger)
