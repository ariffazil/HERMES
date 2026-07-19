---
name: opencode-acp
description: "Manage OpenCode ACP sessions from Hermes — spawn, delegate, attach, agent management"
version: 1.1.0
tags: [opencode, acp, delegation, coding, agent]
metadata:
  hermes:
    requires: [opencode]
---

# OpenCode ACP Integration for Hermes

Manage OpenCode coding sessions from Hermes via ACP (Agent Client Protocol).

## Prerequisites

- OpenCode v1.17.18+ installed (`npm install -g opencode`)
- Config at `/root/.config/opencode/opencode.json`
- Providers: opencode-go (primary/free), tokenplan-mimo (exhausted), qwen-token, minimax, deepseek
- Working model: `opencode-go/deepseek-v4-flash-free` (no API key needed)

## Method 1: delegate_task with ACP (Recommended)

Spawn OpenCode as an ACP subprocess for isolated coding tasks:

```python
delegate_task(
    goal="Build a REST API endpoint for /api/health",
    context="Working directory: /root/project. Model: opencode-go/deepseek-v4-flash-free.",
    acp_command="opencode",
    acp_args=["acp"],
    toolsets=["coding", "terminal", "file"]
)
```

### ACP Command Options

| Command | Purpose |
|---|---|
| `opencode acp` | Full ACP server (stdio mode) |
| `opencode acp --pure` | ACP without external plugins |
| `opencode acp --port <N>` | HTTP ACP server on port N |

### Model Selection

OpenCode reads from `/root/.config/opencode/opencode.json`:
- `model`: `opencode-go/deepseek-v4-flash-free` (primary — no API key needed)
- `agent.forge.model`: MUST match global `model` — this override wins over global config
- `small_model`: `opencode-go/big-pickle`

**Always update ALL agent model overrides AND the global model together.**

Override per-session via environment:
```python
delegate_task(
    goal="...",
    acp_command="opencode",
    acp_args=["acp"],
    # Model is controlled by opencode.json, not by delegate_task
)
```

## Method 2: Terminal Background (Long Tasks)

For long-running coding sessions:

```bash
# Start OpenCode in background
terminal(command="opencode acp --port 9090", background=true, notify_on_complete=false)

# Or via tmux for interactive
terminal(command="tmux new-session -d -s code1 'opencode'", timeout=10)
terminal(command="sleep5 && tmux send-keys -t code1 'Build auth middleware' Enter", timeout=15)
```

## Method 3: One-Shot (Fire and Forget)

```bash
# Query mode
opencode -q "Fix the import error in src/main.py"

# With specific model
opencode -q "Refactor this function" --model tokenplan-mimo/mimo-v2.5-pro
```

## Agent Management

```bash
# List agents
opencode agent list

# Create agent
opencode agent create --name "forge-worker" --model opencode-go/deepseek-v4-flash-free

# Agent types: build (primary), compaction, planner, text-to-image
```

## Server Modes

| Mode | Command | Use Case |
|---|---|---|
| ACP (stdio) | `opencode acp` | delegate_task integration |
| ACP (HTTP) | `opencode acp --port N` | Remote/multi-client |
| Headless | `opencode serve` | Background server |
| Web | `opencode web` | Browser UI |
| Attach | `opencode attach <url>` | Connect to running server |

## MCP Integration

OpenCode's MCP config at `/root/.config/opencode/opencode.json` section `mcp`:
- arifos, aforge, geox, wealth, well (federation organs)
- minimax (stdio, uvx minimax-coding-plan-mcp)
- github, docker, postgres, qdrant, etc.

Hermes and OpenCode share the same MCP servers — no duplication needed.

## References

- `references/opencode-session-monitoring.md` — query OpenCode SQLite DB for live session monitoring (active sessions, messages, tool calls, thinking text)

## Model Selection — CRITICAL: 3 places to update, not 1

**Working model (2026-07-10): `opencode-go/deepseek-v4-flash-free`**
- No API key needed — built into opencode-go provider
- Verified working: `timeout 20 opencode run --model opencode-go/deepseek-v4-flash-free "hi"` → success
- All other providers fail: deepseek/deepseek-v4-pro → "Unauthorized (governor)"; kimi → "Missing API key"

**The model is controlled in 3+ places — ALL must match:**

| File | Key path | Value to set |
|---|---|---|
| `~/.config/opencode/opencode.json` | `model` | `opencode-go/deepseek-v4-flash-free` |
| `~/.config/opencode/opencode.json` | `agent.{forge,auditor,ops,planner}.model` | `opencode-go/deepseek-v4-flash-free` |
| `~/.config/opencode/opencode.json` | `small_model` | `opencode-go/big-pickle` |
| `~/.local/state/opencode/model.json` | `recent[0]` | `{"providerID":"opencode-go","modelID":"deepseek-v4-flash-free"}` |
| `~/.local/state/opencode/model.json` | `favorite` | `["opencode-go/deepseek-v4-flash-free"]` |
| `~/.openclaw/openclaw.json` | `agents.defaults.model.primary` | `opencode-go/deepseek-v4-flash-free` |

**Why mimo-v2.5-pro kept returning despite config changes (root cause found 2026-07-10):**
The global `model` field in opencode.json was updated, but `agent.forge.model` was NOT — it stayed as `tokenplan-mimo/mimo-v2.5-pro`. Agent-level overrides win over global config. OpenCode CLI output `> forge · mimo-v2.5-pro` because the `forge` agent reads its own `model` field first.

**Verification — must show deepseek-v4-flash-free:**
```bash
timeout 20 opencode run "model name" 2>&1 | head -3
# Correct: > forge · deepseek-v4-flash-free
# Wrong:   > forge · mimo-v2.5-pro (agent.forge.model stale override still active)
```

**After any config change — restart serve:**
```bash
pkill -f "opencode serve"; sleep 2
opencode serve --hostname 127.0.0.1 --port 4096 &
sleep 5 && timeout 20 opencode run "model name" 2>&1 | head -3
```

**What does NOT work (2026-07-10):**
- `deepseek/deepseek-v4-flash` → "Unauthorized: Authentication Fails (governor)"
- `deepseek/deepseek-v4-pro` → "Unauthorized: Authentication Fails (governor)"
- `opencode-go/kimi-k2.7-code` → "Missing API key"
- `opencode-go/deepseek-v4-pro` → "Missing API key"

### DeepSeek Provider BaseURL Fix (discovered 2026-07-19)

OpenCode's deepseek provider config often has an incorrect baseURL that causes auth failures:

```
# WRONG in opencode.json (causes "Unauthorized: Authentication Fails (governor)"):
baseURL: https://api.deepseek.com/v1

# CORRECT — DeepSeek's OpenAI-compatible API does NOT use /v1 suffix:
baseURL: https://api.deepseek.com
```

**Fix command:**
```bash
python3 -c "
import json
d = json.load(open('/root/.config/opencode/opencode.json'))
d['provider']['deepseek']['options']['baseURL'] = 'https://api.deepseek.com'
json.dump(d, open('/root/.config/opencode/opencode.json', 'w'), indent=2)
"
```

**Note:** Even after fixing baseURL, the `deepseek` provider may STILL fail auth via OpenCode's `@ai-sdk/openai-compatible` npm adapter. Direct `curl` to `https://api.deepseek.com/chat/completions` with the same key works fine. This is an OpenCode adapter compatibility issue, not a key/balance problem. DeepSeek balance confirmed good ($47.41 as of 2026-07-19).

**Fallback:** When the `deepseek` provider fails in OpenCode despite correct config and valid key, do NOT keep debugging. The `opencode-go/deepseek-v4-flash-free` provider works (though slow on complex tasks). If that also fails or times out, execute the task directly through terminal/MCP tools instead.

## Pitfalls

- **Updating opencode.json `model` only = incomplete.** `agent.forge.model` override is separate and wins. Check BOTH when debugging model issues.
- **`opencode-go/deepseek-v4-flash-free` is the only free model that works immediately.** Everything else either needs a missing API key or hits the governor.
- **model.json in `~/.local/state/opencode/` caches recent models.** If the model still shows wrong after config fix, update the `recent` array and restart serve.
- **OpenCode serve must be restarted after any config change.** Config is read at startup, not per-request.

## Fallback: Execute Directly When OpenCode Fails

When ALL OpenCode providers error or time out, stop debugging. Execute the task directly:

```bash
# You have full access to:
# 1. Terminal (build, test, git, deploy)
# 2. MCP tools (arifOS, A-FORGE, GEOX, WEALTH, WELL)
# 3. execute_code (Python with hermes_tools)
# 4. Direct API calls (curl to DeepSeek etc.)

# Pattern:
terminal(command="cd /root/arifOS && ...")  # build/test
git commit + git push                          # commit
systemctl restart <service>                    # deploy
```

**When to fall back:**
- Every OpenCode provider returns auth/timeout errors
- User said "restart and finish" — execution speed matters more than tool purity
- Task is well-understood (you can read the code, you know what to change)

**Do NOT:**
- Keep debugging OpenCode providers for more than 3 attempts
- Tell the user "OpenCode is broken, can't proceed" — just execute directly
- Apologize for not using OpenCode — direct execution is valid governance

OpenCode stores session metadata in JSON, not SQLite. SQLite DB has NO sessions table.

```python
import json
from datetime import datetime
with open("/root/.openclaw/agents/opencode/sessions/sessions.json") as f:
    data = json.load(f)
# Keys: 'agent:opencode:main', 'agent:opencode:main:heartbeat', 'agent:opencode:direct:{chat_id}'
# Fields: sessionId, updatedAt, lastInteractionAt, abortedLastRun, sessionFile
for k, v in data.items():
    print(f"{k}: {datetime.fromtimestamp(v['updatedAt']/1000)} | aborted={v.get('abortedLastRun')}")
```

Process check — what's actually running NOW:
```bash
ps aux | grep -E 'opencode|openclaw' | grep -v grep | grep -v earlyoom
```
Expected live: openclaw gateway, opencode serve :4096, bot.py, opencode (pts/N interactive).

**KEY:** `abortedLastRun: True` = last run was interrupted/rate-limited (historical). Does NOT mean session is stuck. Check `ps aux` CPU time on pts/N for actual liveness.

Historical JSONL sessions: `/root/.openclaw/agents/opencode/sessions/{sessionId}.jsonl`

## OpenCode Bot (Telegram) — model hardcoded in bot.py

Bot path: `/root/.openclaw/workspace/bots/opencode-bot/bot.py`
Hardcoded at line ~79: `OPENCODE_MODEL = "minimax/MiniMax-M3"` (no key configured = fails silently)
Update this constant + restart whenever switching models.

## Agent Rotation (AGENTS.md mapping)

| Role | Agent | Model | Provider |
|---|---|---|---|
| OpenCode (primary) | build | **qwen3.7-max** | qwen-token |
| FORGE worker | build | GLM-5.2 | qwen-token |
| AUDITOR | build | DeepSeek V4 Pro | qwen-token |
| OPS | build | MiniMax M2.7 | minimax |
| PLAN | planner | Kimi K2.7 Code | qwen-token |

## Floor Score Correct-By-Design (TESTED 2026-07-10)

**NEVER flag these as failures when delegating to OpenCode or any external agent.**
When spawning agents, always state the correct thresholds explicitly — agents default to flat ≥0.80:

| Floor | Value | Meaning | Correct threshold |
|---|---|---|---|
| F7 HUMILITY | 0.04 | Within Ω₀ target range | Target: 0.03–0.05 |
| F9 ANTI-HANTU | 0.0 | Zero hallucination — perfect | Target: <0.30, 0.0 = optimal |

When delegating F1/F12 diagnostic work to OpenCode: *"F7=0.04 and F9=0.0 are correct-by-design. Ignore them."*

## Pitfalls

- OpenCode ACP reads its own config (`opencode.json`), NOT Hermes `config.yaml`
- Model selection is per-opencode.json, not per-delegate_task call
- ACP stdio mode is one-process-per-session (no sharing)
- OpenCode agents have their own permission configs — `opencode agent list` is massive, pipe through `jq` or grep
- `abortedLastRun: True` = historical interrupt, NOT current stuck state — always check process list
- opencode-bot has hardcoded model in bot.py — updating opencode.json does NOT update the bot's model

## Pitfall: SUBAGENT SUMMARIES CAN BE WRONG — verify by reading files (2026-07-10)

When delegating to subagents (via OpenCode or any `delegate_task` call), the agent's summary of what it built is NOT trustworthy on its own. The agent may:
- Build the wrong function (correct signature, wrong logic)
- Claim success but leave the code non-functional
- Miss a critical file or leave a stub

**Real incident (E1 arif_verify, 2026-07-10):**
- Subagent Task 1 summary claimed: "Implemented arif_verify in arifOS kernel"
- Reality: built `mode="verify"` (ledger chain verification) instead of `arif_verify(token, payload_hash)` (SEAL token vs command hash verification)
- Caught by: reading the actual file, not trusting the summary
- Fix: removed the wrong implementation, wrote the correct one locally

**The pattern that prevents this:**
```
1. Subagent returns → read the actual files it modified
2. Ask: "Does the code DO what the spec requires?"
   - Not: "Does the summary say it worked?"
   - Not: "Did the build pass?" (builds can pass with wrong logic)
3. If wrong → fix it locally, don't re-delegate
4. Commit with a note about what was corrected
```

**Verification checklist for delegated code:**
- [ ] Read the actual modified file(s)
- [ ] Check the function/class actually does what the spec requires
- [ ] Check for duplicate definitions (two functions with the same name)
- [ ] Check imports are resolved (Pyright "could not be resolved" = runtime import will fail)
- [ ] Run isolated unit test if logic is non-trivial
- [ ] Check the git diff matches the spec requirements

**Why re-delegation fails:** A subagent that built the wrong thing has demonstrated it doesn't understand the requirement correctly. Re-delegating gives it the same context and gets the same wrong answer. Fix it yourself.

### Skill symlinks: skill_manage creates in Hermes, NOT in other agent dirs

`skill_manage(action='create')` creates the SKILL.md in Hermes' skill directory (`/root/HERMES/skills/`). It does NOT auto-symlink to:
- `~/.claude/skills/` (Claude Code)
- `~/.openclaw/skills/` (OpenClaw)

**After creating a skill, manually symlink to both dirs:**
```bash
# For skills in subdirectories (e.g. autonomous-ai-agents/opencode-acp)
ln -sf /root/HERMES/skills/autonomous-ai-agents/<name>/SKILL.md ~/.claude/skills/<name>.md
ln -sf /root/HERMES/skills/autonomous-ai-agents/<name>/SKILL.md ~/.openclaw/skills/<name>.md

# For top-level skills (e.g. minimax-cli)
ln -sf /root/HERMES/skills/<name>/SKILL.md ~/.claude/skills/<name>.md
ln -sf /root/HERMES/skills/<name>/SKILL.md ~/.openclaw/skills/<name>.md
```

**Path note:** `/root/.hermes/skills/` is a symlink to `/root/HERMES/skills/` (same inode). Always use the canonical `/root/HERMES/skills/` path for symlinks to avoid nested symlink confusion.

**Caught by:** OpenCode forge agent audited disk after Hermes claimed "4 skills created" — found2/4 missing from OpenClaw. Signal was right (missing symlinks), diagnosis was wrong ("doesn't exist" vs "not symlinked").

## Pitfall: skill_manage creates in Hermes, doesn't auto-symlink to other agent dirs (2026-07-06)

`skill_manage(action='create')` writes to `/root/HERMES/skills/` (canonical, uppercase). But other agents read from their own skill directories:
- OpenClaw: `~/.openclaw/skills/`
- Claude: `~/.claude/skills/`
- Hermes: `~/.hermes/skills/` (symlink to `/root/HERMES/skills/`)

After creating a skill, manually verify and symlink:
```bash
# Verify canonical location
ls -la /root/HERMES/skills/<category>/<name>/SKILL.md

# Symlink to OpenClaw
ln -sf /root/HERMES/skills/<category>/<name>/SKILL.md ~/.openclaw/skills/<name>.md

# Symlink to Claude
ln -sf /root/HERMES/skills/<category>/<name>/SKILL.md ~/.claude/skills/<name>.md

# Verify all symlinks resolve
readlink -f ~/.openclaw/skills/<name>.md
readlink -f ~/.claude/skills/<name>.md
```

**Lesson from 2026-07-06:** Hermes sealed a receipt claiming4 skills were created. OpenCode's forge agent audited the disk and found2 symlinks missing in OpenClaw. The skills existed on disk (in subdirectories) but weren't symlinked. "Not at path X" ≠ "not on disk" — always check canonical source before declaring absence.

**Path confusion:** `/root/.hermes/skills` is a SYMLINK to `/root/HERMES/skills` (same inode). Always use the canonical uppercase path for symlinks. The lowercase path works for reads but may confuse agents that check `readlink`.

## Pitfall: don't blindly follow OpenCode's suggestions (2026-07-06)

When OpenCode (or any external agent) proposes a migration plan, verify against REALITY before executing. OpenCode may suggest changes based on its own config context, not yours.

**Arif's directive:** "dont simply follow opencode. zen it based on reality."

**Pattern:**
1. OpenCode says "do X" → check if X is already done in YOUR config
2. OpenCode references files that don't exist → skip those steps
3. OpenCode proposes MCP servers → verify ports are actually dead first
4. Cross-check every suggestion against live state (`ps aux`, `curl :port/health`, `cat config`)

**Example:** OpenCode proposed adding minimax-media/minimax-code MCP servers. Reality: systemd services were running but dead (404 on /health). The fix was stopping systemd + killing zombies + replacing with stdio — NOT following OpenCode's proposed config format.

## Session Monitoring

**Sessions live in JSON, not SQLite.** The old SQLite approach is deprecated.

Sessions tracked in: `/root/.openclaw/agents/opencode/sessions/sessions.json`

Live process signals:
```
opencode serve :4096      — API server (background, always on)
openclaw gateway          — Telegram bridge (background, always on)
opencode                  — interactive CLI (pts/N, human present)
opencode-bot bot.py       — Telegram bot handler
```

**Critical:** `ps aux | grep opencode` tells you what's live vs stale. CPU time on pts/N = active session. An `abortedLastRun: True` flag means interrupted/rate-limited — NOT stuck.

See `references/opencode-session-monitoring.md` for the correct JSON-based session reading pattern.

## Managing Active Sessions (Not Spawned Through Hermes)

When OpenCode is already running interactively on `pts/N` (started by the user, not via `terminal(background=true)`), you CANNOT use `process()` tools. Monitor via file system instead:

```bash
# 1. Find the process
ps aux | grep opencode | grep -v grep | grep -v earlyoom
# PID 224645  65% CPU  pts/2  opencode  ← active

# 2. Working directory
ls -la /proc/<PID>/cwd

# 3. What it's building (recent file changes)
find /root/A-FORGE/src -name "*.ts" -newer /root/A-FORGE/package.json -mmin -15
cd /root/A-FORGE && git status --short  # ?? = new, M = modified

# 4. Read the artifacts, run tests, triage failures
npx tsx test/new_tool.test.ts
```

**Status report pattern:** Component → Status → Quality table. Don't just say "it's working" — show test results, note TODOs, flag architectural concerns.

## Pitfall: Concurrent File Modification (2026-07-16)

**When OpenCode is running and modifying files at the same time you're patching them:**

OpenCode modifies files while you're reading/patching. A `patch()` call may fail with "Found N matches" or "old_string not found" because the file changed since your last read.

**Pattern:** Always re-read before retrying:
```
read_file → patch() → "Found N matches" → re-read_file → patch()
```

**Real incident:** Patching `forge_visual_qa.test.ts` while OpenCode was actively editing it. First patch succeeded; second patch failed because OpenCode had rewritten the same section between reads.

## Pitfall: Test Bug vs Implementation Bug Triage (2026-07-16)

When delegated code has test failures, distinguish:

| Type | Example | Fix |
|------|---------|-----|
| **Test bug** | Assertion checks `.includes("rejected")` but failure_reason says "zero confidence" (different condition triggered first) | Fix the test assertion |
| **Implementation bug** | `evaluateTriWitness` caps confidence internally for geometric mean but returns uncapped values in the output struct | Fix the code |

**How to tell:** Read BOTH the test AND the implementation. Don't just fix the test to pass — ask "is the test revealing a real bug?"

**Real incident (2026-07-16, forge_visual_qa):**
- Test "W1 REJECTED → consensus = false" failed on `failure_reason?.includes("rejected")`. Cause: W3 had confidence=0, so `anyZero` triggered before `anyRejected` — failure_reason was about zero, not rejection. Test bug: wrong assertion for the scenario.
- Test "confidence capped at 0.90" failed on `w1_vision.confidence <= 0.90`. Cause: `evaluateTriWitness` capped internally but returned original uncapped witness objects. Implementation bug: F7 HUMILITY floor not enforced in output. Fixed by spreading with capped values: `{ ...w1, confidence: w1c }`.

## Reading Historical (Completed) Sessions

When OpenCode has already finished and you need to read what happened — use the JSONL session files on disk. See `references/opencode-historical-sessions.md` for the full retrieval pattern (session location, JSONL parsing, trajectory status checks, pitfalls).

**Quick path:**
```bash
# Find latest completed session
ls -lt /root/.openclaw/agents/opencode/sessions/*.jsonl | grep -v trajectory | head -3
```

## Related Files

- `references/opencode-session-monitoring.md` — CORRECTED: JSON-based session monitoring (sessions.json + .jsonl files; SQLite approach deprecated, DB has no sessions table)
- `references/opencode-historical-sessions.md` — JSONL file format, session retrieval, trajectory status (COMPLETED sessions)
- `references/a2a-federation-audit.md` — A2A conformance audit recipe, warga verification, registry vs public distinction
- `references/active-session-monitoring.md` — managing OpenCode sessions NOT spawned through Hermes (ps/proc monitoring, concurrent modification, test triage)

## Agent Rotation (as of 2026-07-10)

| Role | Agent | Model | Provider |
|---|---|---|---|
| OpenCode (primary) | build | **deepseek-v4-flash-free** | opencode-go (free, no key) |
| FORGE worker | build | deepseek-v4-flash-free | opencode-go |
| AUDITOR | build | deepseek-v4-flash-free | opencode-go |
| OPS | build | deepseek-v4-flash-free | opencode-go |
| PLAN | planner | deepseek-v4-flash-free | opencode-go |

> **Mimo exhausted 2026-07-10.** Primary switched to `opencode-go/deepseek-v4-flash-free`.
> All agent overrides (`agent.forge.model`, etc.) MUST also be updated to match.

## Pitfall: Telegram Conflict — Multiple Bot Instances

**Symptom:** `telegram.error.Conflict: terminated by other getUpdates request`

**Root cause:** Old bot instance still connected to Telegram polling while a new one starts. Telegram only accepts one polling connection per bot token.

**Check:**
```bash
lsof -i :443 2>/dev/null | grep python3 | grep telegram | wc -l
# 2 connections = conflict. Should be 1 per bot.
```

**Fix — never kill the systemd instance directly:**
1. `systemctl stop opencode-bot` — stop systemd
2. Kill all orphaned manual instances: `pkill -9 -f "opencode-bot/bot.py"`
3. `systemctl start opencode-bot` — let systemd restart clean

**Never start bot.py manually** — systemd must own the single instance. Manual starts create conflicts.

**Note:** When bot restarts, Telegram holds the old session for ~60s. New instance shows Conflict errors during this window. Self-clears automatically.
