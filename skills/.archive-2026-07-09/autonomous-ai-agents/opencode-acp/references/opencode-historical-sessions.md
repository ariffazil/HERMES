# Reading Completed OpenCode Sessions from JSONL Files

When you need to read what happened in a FINISHED OpenCode session (not live monitoring via SQLite).

## File Locations

```
/root/.openclaw/agents/opencode/sessions/
├── sessions.json                          — session index (agent IDs → session IDs)
├── <uuid>.jsonl                           — session messages (OpenCode native format)
├── <uuid>.trajectory.jsonl               — OpenClaw trajectory/tracing events
├── sessions.json.bak.<timestamp>          — backups
```

Also check: `/root/.arifos/agents/opencode/sessions/` (secondary location, may have only config).

## Step 1: Find latest session

```bash
ls -lt /root/.openclaw/agents/opencode/sessions/*.jsonl | head -3
```

## Step 2: Read session summary

```python
import json
path = '/root/.openclaw/agents/opencode/sessions/<uuid>.jsonl'
with open(path) as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    msg = json.loads(line)
    if msg.get('type') != 'message':
        continue
    inner = msg.get('message', {})
    role = inner.get('role', '?')
    content = inner.get('content', '')
    
    # Content can be list (multimodal) or string
    if isinstance(content, list):
        texts = [p['text'] for p in content if p.get('type') == 'text']
        tools = [f"TOOL:{p.get('name','')}" for p in content if p.get('type') == 'tool_use']
        results = [f"RESULT:{str(p.get('content',''))[:100]}" for p in content if p.get('type') == 'tool_result']
        content_str = ' '.join(texts + tools + results)
    elif isinstance(content, str):
        content_str = content
    else:
        continue
    
    ts = str(msg.get('timestamp',''))[:19]
    if content_str.strip():
        print(f'[{i}] {ts} {role}: {content_str[:200]}')
```

## Step 3: Read trajectory for completion status

```python
path = '/root/.openclaw/agents/opencode/sessions/<uuid>.trajectory.jsonl'
with open(path) as f:
    lines = f.readlines()

for line in lines:
    msg = json.loads(line)
    etype = msg.get('type','')
    if etype == 'session.started':
        print(f"STARTED: {msg.get('data',{}).get('trigger','?')}")
    elif etype == 'prompt.submitted':
        print(f"PROMPT: {msg.get('data',{}).get('prompt','')[:200]}")
    elif etype == 'session.ended':
        data = msg.get('data',{})
        print(f"ENDED: status={data.get('status')} aborted={data.get('aborted')} timeout={data.get('timedOut')} reason={str(data.get('promptError',''))[:100]}")
```

## JSONL Message Structure

Each line is a JSON object. The `type` field determines the wrapper:

| type | meaning | actual content in |
|---|---|---|
| `session` | Session metadata (id, cwd, timestamp) | top-level fields |
| `model_change` | Model switch event | top-level fields |
| `message` | User/assistant/tool content | `message.role`, `message.content` |
| `custom` | Plugin-specific events | varies |

For `type: "message"`, the structure is:
```json
{
  "type": "message",
  "id": "a13b9b75",
  "parentId": "3aca0a31",
  "timestamp": "2026-06-28T19:47:47.230Z",
  "message": {
    "role": "user",
    "content": [
      {"type": "text", "text": "TASK: ..."},
      {"type": "tool_use", "name": "bash", ...}
    ]
  }
}
```

## Pitfalls

- `sessions.json` maps agent routing IDs (e.g., `agent:opencode:main`), NOT session UUIDs. The UUID→content mapping is in the individual `.jsonl` files.
- The `message.content` field is **usually a list** of content parts, NOT a string. Always check `isinstance(content, list)` first.
- Tool results in the JSONL show full paths — they may contain PII-sensitive file paths.
- The `.trajectory.jsonl` has different schema than `.jsonl` — trajectory uses `data` field, not `message`.
- Sessions from before June 2026 may have different format (version `2` vs `3`).
- The `session.ended` trajectory entry is the most reliable completion status check.
