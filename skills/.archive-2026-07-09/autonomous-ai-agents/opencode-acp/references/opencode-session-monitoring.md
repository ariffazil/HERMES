# OpenCode Session Monitoring (CORRECTED)

> **Updated 2026-07-10** — SQLite approach is WRONG. OpenCode session state lives in JSON, not SQLite.

## Session State Location

Sessions are tracked in:
```
/root/.openclaw/agents/opencode/sessions/sessions.json
```

Individual session trajectories in `.jsonl` files under the same directory.

## sessions.json Structure

Top-level keys = session identifiers:
```
agent:opencode:main              — main interactive session
agent:opencode:main:heartbeat    — heartbeat/isolated session
agent:opencode:direct:<id>       — DM sessions per Telegram user
```

Each value is a dict with:
- `sessionId` — UUID of the session
- `sessionStartedAt` — Unix ms timestamp
- `updatedAt` — Unix ms timestamp (recency indicator)
- `lastInteractionAt` — Unix ms timestamp (if present)
- `sessionFile` — path to `.jsonl` trajectory file (may not exist)
- `abortedLastRun` — boolean, check if last run was aborted
- `authProfileOverride` — auth profile in use
- `skillsSnapshot.skills[]` — list of loaded skills at session start

## Reading a Session Trajectory

Trajectory files are NDJSON (newline-delimited JSON), one event per line.

Event types in the file:
- `{"type":"session", ...}` — session metadata
- `{"type":"model_change", ...}` — model/provider switch
- `{"type":"thinking_level_change", ...}` — thinking mode change
- `{"type":"message", "message":{"role":"user|assistant|toolResult", "content":[...]}}` — actual messages
- `{"type":"custom", "customType":"openclaw:prompt-error", ...}` — errors/aborts
- `{"type":"custom", "customType":"model-snapshot", ...}` — model snapshot events

```python
import json

path = "/root/.openclaw/agents/opencode/sessions/<session-id>.jsonl"
messages = []
with open(path) as f:
    for line in f:
        line = line.strip()
        if line:
            messages.append(json.loads(line))

# First event = session metadata
print(messages[0])

# Last few events = end state
for m in messages[-3:]:
    print(m.get('type'), m.get('message', {}).get('role'))
```

## Key Queries

```python
import json
from datetime import datetime

with open("/root/.openclaw/agents/opencode/sessions/sessions.json") as f:
    data = json.load(f)

for key, s in data.items():
    sid = s.get('sessionId', '?')
    updated = s.get('updatedAt', 0)
    age_ms = datetime.now().timestamp() * 1000 - updated
    print(f"{key}")
    print(f"  sessionId: {sid}")
    print(f"  updated: {datetime.fromtimestamp(updated/1000)}")
    print(f"  age: {age_ms/86400000:.1f} days")
    print(f"  aborted: {s.get('abortedLastRun')}")
    print(f"  sessionFile: {s.get('sessionFile')}")
```

## Finding the Active Session

```bash
# Which process is running opencode interactively?
ps aux | grep opencode | grep -v grep

# CPU time tells you what's currently active vs old
# pts/2 with high CPU time = live interactive session
```

## Live Process Signals

```
opencode serve :4096      — API server (background, always on)
openclaw gateway          — Telegram bridge (background, always on)
opencode                  — interactive CLI (pts/N, human present)
opencode-bot bot.py       — Telegram bot handler
```

## Common Issues

| Symptom | Likely Cause |
|---|---|
| `sqlite3.OperationalError: no such table: sessions` | Wrong DB path — sessions are in JSON, not SQLite |
| `abortedLastRun: True` | Session was interrupted (rate limit, abort, timeout) — not stuck, just incomplete |
| Session shows Jun date but process running | Stale JSON state — process is live but sessions.json wasn't updated (normal for old sessions) |

## What SQLite IS actually used for

There IS a SQLite DB at `/root/.local/share/opencode/opencode.db` but it has a different schema (not sessions). It may contain tool-use history or other OpenCode internals — the `sessions` table does not exist there.

## OLD (WRONG) SQLite approach

The deprecated approach tried:
```sql
SELECT * FROM session WHERE time_archived IS NULL ORDER BY time_updated DESC;
```
This fails because there is no `session` table. Discard this approach entirely.
