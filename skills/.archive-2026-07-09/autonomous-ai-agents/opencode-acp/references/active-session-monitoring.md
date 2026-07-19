# Active Session Monitoring — When OpenCode Was NOT Spawned By Hermes

> **Created 2026-07-16** — pattern from managing forge_visual_qa build session

## The Scenario

User starts OpenCode interactively (`opencode` on pts/N). Hermes is asked to "manage it" or "check on it." The `process()` tools are NOT available because Hermes didn't spawn the session.

## Step-by-Step Monitoring Protocol

### 1. Find the Process
```bash
ps aux | grep -E 'opencode|openclaw' | grep -v grep | grep -v earlyoom
```
Look for: PID, CPU%, TTY (pts/N), elapsed time. High CPU = actively working.

### 2. Determine Working Directory
```bash
ls -la /proc/<PID>/cwd
# → /root (federation root) or /path/to/specific/project
```

### 3. Detect What It's Building
```bash
# Files modified in last N minutes in likely target repos
find /root/A-FORGE/src -name "*.ts" -newer /root/A-FORGE/package.json -mmin -15

# Git status for untracked/modified files
cd /root/A-FORGE && git status --short
# ?? = new files (agent created them)
# M  = modified files (agent changed them)
```

### 4. Read the Artifacts
```bash
# Read new tool files
cat /root/A-FORGE/src/infrastructure/tools/NewTool.ts

# Read test files
cat /root/A-FORGE/test/new_tool.test.ts

# Read contract docs
cat /root/A-FORGE/docs/MCP-TOOL-CONTRACT-NewTool.md
```

### 5. Verify Quality
```bash
# Run tests
cd /root/A-FORGE && npx tsx test/new_tool.test.ts 2>&1

# Check compilation
cd /root/A-FORGE && npm run build 2>&1

# Check for lint issues
cd /root/A-FORGE && npx eslint src/infrastructure/tools/NewTool.ts 2>&1
```

### 6. Triage Failures
For each test failure:
1. Read the test assertion
2. Read the implementation code it tests
3. Determine: test bug (assertion wrong) vs implementation bug (code wrong)
4. Fix accordingly

### 7. Report Status
Format as table:
| Component | Status | Quality |
|---|---|---|
| Tool file | ✅ Written | Strong — state machine correct |
| Tests | ✅ 26/26 pass | Good coverage |
| Contract doc | ✅ Written | Comprehensive |
| MCP wiring | ❌ Not done | Needs server.tool() registration |
| Build | ❌ Not verified | Need npm run build |

## Concurrent Modification Handling

When OpenCode is actively modifying files while you're reading/patching:

1. **Read before every patch** — don't rely on a read from 2 tool calls ago
2. **If patch fails** with "Found N matches" or "old_string not found" → re-read the file, the content changed
3. **Don't race** — if OpenCode is at 170% CPU and actively writing, let it finish a cycle before patching

## What You CAN'T Do (process() unavailable)

- `process(action="poll")` — not your process
- `process(action="submit")` — can't send input
- `process(action="log")` — can't read stdout directly
- `process(action="kill")` — not your process to kill

## What You CAN Do

- Read files on disk (the artifacts)
- Run tests independently
- Fix bugs in the code
- Check git status
- Monitor process via ps/top
- Report status to the user
