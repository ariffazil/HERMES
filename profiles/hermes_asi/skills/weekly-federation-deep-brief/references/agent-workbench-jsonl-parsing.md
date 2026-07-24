# Agent-Workbench JSONL Telemetry — Parsing Recipes

Verified 2026-07-12. These files look like JSONL (`.jsonl` extension) but they are not strict JSONL — `json.loads(content)` on the whole file fails. Verified recipes below.

## The Trap

```python
# WRONG — fails with "Extra data: line N column 1"
with open(file) as f:
    data = json.loads(f.read())
```

Files in `/root/.agent-workbench/telemetry/seal-session_*.jsonl` contain **multiple JSON objects**, one per line, but the file may also have trailing whitespace or non-JSON lines. `json.loads(content)` parses the first object, then chokes on the second.

## The Recipe (line-by-line, skip blanks)

```python
import json, glob
from collections import Counter

events = Counter()
verdicts = Counter()
sessions_per_day = Counter()

for f in sorted(glob.glob('/root/.agent-workbench/telemetry/seal-session_*.jsonl')):
    try:
        content = open(f).read()
        for line in content.split('\n'):
            line = line.strip()
            if not line.startswith('{'):  # skip blanks, comments, BOM
                continue
            try:
                d = json.loads(line)
            except: 
                continue  # skip malformed lines silently
            events[d.get('type','?')] += 1
            verdicts[d.get('verdict','?')] += 1
            ts = d.get('timestamp','')
            if ts:
                sessions_per_day[ts[:10]] += 1
    except Exception as e:
        pass
```

## Event Schema (verified)

Each object is an `aaa-stop-seal` event with this shape:

```json
{
  "type": "aaa-stop-seal",
  "timestamp": "2026-07-12T14:14:13Z",
  "session_id": "session_73f5a5a6-a0af-47de-9e44-ba254031951b",
  "epoch": 1783865653,
  "thermodynamics": {
    "dS_session_avg": 0.0,
    "dS_session_max": 0.0,
    "chaos_trend": "stable",
    "rollback_coverage": "unknown"
  },
  "telemetry": {
    "session_events": 0,
    "high_risk_actions": 0,
    "hold_recommended_count": 0,
    "tier_a_touches": 0,
    "cross_repo_touches": 0,
    "background_tasks_running": false
  },
  "dirty_repos": ["arifOS", "A-FORGE", "WEALTH"],
  "unresolved_warnings": ["Dirty repos: arifOS A-FORGE WEALTH "],
  "verdict": "STABLE_WITH_WARNINGS",
  "seal_note": "Session closed with full thermodynamic telemetry."
}
```

**Key fields to surface in the brief:**

- `verdict` — usually `STABLE_WITH_WARNINGS`. The "warnings" are dirty repos at session close.
- `dirty_repos` — which organs had uncommitted state when the session ended. **Persistence pattern:** if `arifOS`/`A-FORGE`/`geox` show up in dirty_repos across multiple sessions in a week, the post-seal sweep didn't fully clean them.
- `unresolved_warnings` — human-readable list. The dominant one is dirty-repos carryover.
- `telemetry.session_events` — if 0, the session was idle/clean. Non-zero means work happened.

## Run-2 Findings (2026-07-12)

- 7 telemetry events total across the week. 0 had any session activity (`session_events: 0`).
- Dominant verdict: `STABLE_WITH_WARNINGS` (7/7).
- Dirty repos at session close (most common): `A-FORGE` (7), `geox` (6), `arifOS` (5), `WEALTH` (3).
- **Implication for the brief:** the system is closing sessions cleanly but carries uncommitted state between them. The post-seal sweep on 12 Jul (seq=54) closed most of it.

## Companion Source: VAULT999 seal_chain.jsonl

This file IS strict JSONL — one JSON object per line, no extra data. It parses cleanly with the standard `for line in f: json.loads(line)` pattern.

```json
{
  "seq": 1,
  "prev_hash": "sha256:0",
  "this_hash": "sha256:f991f49e3cb6939de4ac8ff5838155d64a52f4c403333e4e548d463038b2c358",
  "payload": {
    "agent_id": "aaa-bridge",
    "action": "mcp.call.aforge.shell.ok",
    "payload": {
      "task_id": "task-001",
      "status": "COMPLETED",
      "routing": "aforge",
      "tool": "shell"
    },
    "epoch": "2026-07-04T10:39:55.579Z",
    "verdict": "SEAL",
    "human_ratifier": "arif",
    "human_signature": "SIG_AAA_GATEWAY_MR68DGVV",
    "ratified_at": "2026-07-04T10:39:55.579Z",
    "irreversibility_ack": true,
    "irreversibility_class": "LOW_RISK_DIRECT",
    "tags": ["aaa", "a2a", "audit"],
    "metadata": {"source": "aaa-a2a-gateway", "protocol": "A2A/AAA-v1.0", "tool": "shell"}
  },
  "epoch": "2026-07-04T10:39:55.580Z",
  "actor": "aaa-bridge",
  "verdict": "SEAL"
}
```

**Top-level keys:** `seq` (int), `prev_hash` (sha256 chain), `this_hash` (sha256), `payload` (nested dict with the real action), `epoch` (top-level timestamp), `actor`, `verdict`.

**Common actors seen:** `aaa-bridge`, `arif`/`ARIF`/`Arif` (case-variant — normalize), `grok-build`, `opencode-333`, `codex`, `forge-000-omega`, `hermes-cognitive`, `openclaw-anon`, `FORGE-000Ω`.

**Common actions:** `mcp.call.<organ>.<tool>.ok` / `.dependency_error`, `session.seal`, `kernel.zen_audit.seal`.

**Verdict vocabulary:** `SEAL` (33%), `HOLD` (52% — dominant this week!), `PROCEED`, `SABAR_HOLD`. **The high HOLD rate is normal during consolidation epochs** — the system is choosing to refuse seals rather than rubber-stamp them.

## Companion Source: Identity Drift Watchdog

```bash
# Triggered daily; writes a passive flag if identity hash drifts
cat /root/A-FORGE/forge_work/identity-drift-watchdog/DRIFT.flag.json
```

Schema (verified 2026-07-12 15:00 UTC):
```json
{
  "detected_at": "2026-07-12T15:00:01Z",
  "session_anchor": "SEAL-2751ad53b5d04c50",
  "baseline": "/root/.local/share/arifos/identity-fingerprint-baseline.sha256",
  "diff_kind": "hash_mismatch",
  "action": "next_arif_init_must_surface"
}
```

**Interpretation:** `hash_mismatch` + `next_arif_init_must_surface` means the watchdog detected a fingerprint drift and flagged the NEXT session-init to surface it (not auto-fix). This is a **passive detection pattern**, not a hard alert. Surface in the brief as "the system noticed something and chose to wait for human attention."

## Consolidation-Cadence Pattern

Sundays are the system's natural consolidation pivot. Evidence (run 2):
- Sun 5 Jul: 45 seal-chain entries (largest single-day burst in the week).
- Sun 12 Jul: 1 Consolidation Epoch seal (seq=53) + 1 post-sweep seal (seq=54) + the weekly brief itself.

**Implication:** when running the brief on Sunday, expect to find consolidation-pattern artifacts at both ends of the week (last Sunday's burst + today's epoch). Frame the brief with this cadence visible.