# OpenCode Execution Logistics

> Runtime behaviours and workarounds when delegating multi-phase work to `opencode run` (DeepSeek V4 Pro, 1M ctx).

## Config Collision

**Symptom:** `Error: Configuration is invalid at /root/AAA/opencode.json — Unrecognized keys: id, name, class...`

**Root cause:** OpenCode scans the directory tree from CWD upward for `opencode.json`. The AAA agent-card (`/root/AAA/opencode.json`) has non-OpenCode keys that the parser rejects.

**Fix:** Set `workdir` to a repo without a conflicting `opencode.json`:
```
terminal(command="opencode run '...'", workdir="/root/A-FORGE")
```
Or temporarily rename the conflicting file:
```
mv /root/AAA/opencode.json /root/AAA/opencode.json.bak
# ... run opencode ...
mv /root/AAA/opencode.json.bak /root/AAA/opencode.json
```

## Multi-Phase Execution via `opencode run`

`opencode run` with a single comprehensive prompt handles complex multi-phase work (14+ tasks across multiple repos) better than interactive TUI. The model:
- Auto-creates a todos checklist
- Works through phases sequentially
- Executes shell commands, git ops, tests, and restarts autonomously
- Reports progress with the checklist

**Recommended timeout:** 600s (10 min) for federation-scale task maps. DeepSeek V4 Pro streaming keeps the connection alive.

### Prompt Structure That Works

```
TITLE

CURRENT STATE:
- Key facts about repo state, dirty files, kernel health

PHASE A — Quick Wins
1. Task description with exact commands
2. ...

PHASE B — Main Work
Phase 0: git status + checkpoints
Phase 1: ...
...

REPORT: After each phase, say "✅ PHASE X COMPLETE" or "❌ PHASE X FAILED: reason"

RULES:
- Specific file-add rules (no git add -A)
- What NOT to touch
- What to skip
```

### What the Model Actually Does

From observation (19:53 MYT run, DeepSeek V4 Pro):
1. Sources secrets via inline bash
2. Creates a markdown tick list tracking all phases
3. Executes commands in dependency order
4. Reports `✅ PHASE X COMPLETE` after each
5. Commits code with conventional-commit messages
6. Runs tests, reports pass/fail per test file
7. Restarts services and verifies health after deploy
8. Emits VAULT999 seal at end

## TUI vs `run` Mode

| Aspect | Interactive TUI | `opencode run` |
|--------|----------------|----------------|
| Needs pty | Yes (`pty=true`) | No |
| Needs background | Yes (`background=true`) | No |
| Submitting text | `process(submit)` + extra Enter | Just include in `run '...'` arg |
| Monitoring | `process(poll/log)` calls | Wait for terminal return |
| Output | Streaming in PTY buffer | Full output on completion |
| Timeout handling | Background (no timeout) | Set `timeout=N` in terminal call |
| Best for | Iterative work needing input | Bounded multi-step automation |

## DeepSeek V4 Pro Notes

- Works reliably with OpenCode for long-running autonomous execution
- `--model deepseek/deepseek-v4-pro` works with both `run` and TUI
- `--title` only works with `opencode run` (not TUI)
- No timeout issues on 600s runs with streaming
- `deepseek/deepseek-v4-pro` is the provider/model format (not `deepseek-v4-pro` alone)

## Verified Session (2026-07-22)

The AGY-STABILIZATION run completed 14 tasks across arifOS, A-FORGE, AAA, and WELL repos:
- 6/6 organ health checks
- 2 git commits (ZEN docs + AGY stabilization)
- 18/18 pytest pass on arifOS
- arifOS restart with health verification
- VAULT999 seal emitted
- Duration: ~5 min via `opencode run` with 600s timeout
- Model: `deepseek/deepseek-v4-pro`
