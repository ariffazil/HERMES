---
name: agent-output-harvesting
category: governance
description: Monitor spawned agent sessions (OpenCode, Claude Code, Codex, etc.) and extract their outputs back into the conversation. Cross-agent coordination pattern for Hermes.
---

# Agent Output Harvesting

When the user spawns another agent (especially OpenCode / 🔥FORGE) on a subtask and asks Hermes to "monitor and extract", use this pattern instead of waiting passively.

## 1. Detect the spawned agent

```bash
# Find OpenCode / agent processes
pgrep -a opencode
pgrep -a "code"
```

Check:
- Is it running? What PID?
- What's its cwd? (`/proc/<PID>/cwd`)
- What PTY is it on? (`/proc/<PID>/fd/1 → /dev/pts/N`)
- Is there an existing MCP/bot bridge? (e.g. `opencode-bot` for Telegram)

## 2. Set up a file watcher

```bash
cat > /tmp/monitor_agent.sh << 'SCRIPT'
#!/bin/bash
WATCH_DIRS="/root /tmp /root/.opencode /root/A-FORGE /root/docs"
OUTPUT_FILE="/tmp/agent_monitor_output.txt"

while true; do
    NEW_FILES=$(find $WATCH_DIRS -mmin -10 -type f \( -name "*.md" -o -name "*.txt" -o -name "*.json" \) 2>/dev/null | sort -u)
    if [ -n "$NEW_FILES" ]; then
        echo "[$(date '+%H:%M:%S')]" >> "$OUTPUT_FILE"
        echo "$NEW_FILES" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
    fi
    sleep 15
done
SCRIPT
```

Run as background process:

```bash
kill $(pgrep -f monitor_agent.sh) 2>/dev/null
/tmp/monitor_agent.sh &
```

## 3. Poll for output

```bash
cat /tmp/agent_monitor_output.txt  # check watcher
ls -lt /tmp/ | head -20            # check for new files
find /tmp -name "*.md" -mmin -5    # find very recent files
```

For each new file:
- `cat /path/to/file` or `read_file()` to inspect
- Extract relevant content
- Present to user with summaries/headings

## 4. Standard output locations

| Agent | Likely output dir | File types |
|---|---|---|
| OpenCode (CLI) | `/root/` (cwd) | `.md`, code changes |
| OpenCode (server) | `/tmp/` | Session artifacts |
| OpenCode / FORGE bot | Telegram DM | Forwarded by user |
| A-FORGE | `/root/A-FORGE/forge_work/` | `.md` receipts |

## 5. Pitfalls

- **OpenCode stdout goes to PTY** — you cannot `cat /proc/PID/fd/1` for content; it's a pipe. Rely on file outputs.
- **`notify_on_complete=true`** blocks `watch_patterns` — they are mutually exclusive. For monitor scripts use `background=true` alone and poll manually.
- **Tmp files may be owned by another user** (`ariffazil`, `arifos`) — `cat` as root may fail. Use `sudo -u <user>` or check permissions first.
- **Don't duplicate effort** — if there's already a watcher running (`pgrep -f monitor_agent`), reuse it or kill and restart.
- **Time-matching** — use `-mmin` with a window broad enough to catch the agent's entire run, not just the last check cycle.

## 6. Report format

After extracting, present to user in a compact table:

```markdown
## 📦 Results from [Agent Name]

| File | Content Summary |
|---|---|
| `path/to/file.md` | Key findings, decisions, outputs |
| `path/to/result.json` | Structured data |

[Bullet list of actionable outputs]
```
