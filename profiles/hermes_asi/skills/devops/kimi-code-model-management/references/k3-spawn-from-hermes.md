# K3 Subagent Spawn Pattern (from Hermes)

> **When:** Delegating heavy multi-step execution tasks to Kimi K3 (2.8T MoE) as a background subagent from within a Hermes session.
> **Why:** K3's reasoning depth + tool-using capability handles complex filesystem tasks (multi-file edits, git hooks, doc updates) that benefit from a dedicated agent context.
> **Date:** 2026-07-20

## Invocation

```bash
cd /root && /root/.kimi-code/bin/kimi \
  -p "<self-contained task prompt>" \
  --output-format text \
  --model kimi-code/k3
```

## Hermes terminal() Wrapper

```python
terminal(
    command="cd /root && /root/.kimi-code/bin/kimi -p \"...\" --output-format text --model kimi-code/k3",
    pty=True,           # Kimi is an interactive CLI
    background=True,     # Long-running
    notify_on_complete=True,  # Get notified when done
    timeout=600,         # 10 min for complex multi-file tasks
)
```

## Flags

| Flag | Required? | Why |
|---|---|---|
| `-p "<prompt>"` | Yes | Task prompt. Cannot combine with `-y`. |
| `--output-format text` | Yes | Without it, `-p` mode returns streaming JSON (unreadable). |
| `--model kimi-code/k3` | Yes | Explicitly pin K3. Without it, may silently fall back to MiniMax. |
| `-y` / `--yolo` | NO | Conflicts with `-p`. Returns `error: Cannot combine --prompt with --yolo`. |

## Task Prompt Structure

Self-contained, no reliance on Hermes session context. Best structure:

```
You operate under arifOS sovereign federation.
Do not reimplement existing tools. Work directly on the filesystem.

## TASK 1: <clear goal>
<specific instructions — files to read, changes to make, constraints>

## TASK 2: <clear goal>
<specific instructions>

Report succinctly: what you changed in each file, file paths, and results.
```

## Pitfalls

- **AGENTS.md context injection**: Running from a project dir with AGENTS.md injects it as system prompt, which can override model identity. Run from `/root` or `/tmp` to isolate.
- **Silent fallback**: If OAuth is expired, K3 silently falls back to MiniMax-M3. The response says "MiniMax" and you won't know K3 was skipped. Always check the model name in the response.
- **Amend recursion**: When K3 uses `git commit --amend` in a hook, it must guard against recursion (e.g., `WELL_VERSION_HOOK=1` env var).
- **Pre-amend SHA caveat**: When a hook embeds the commit SHA into a file and then amends, the embedded SHA is the pre-amend value. This is inherent — one-commit drift on every version-bind hook. The next commit corrects it.

## When to Use K3 vs Other Subagents

| Task | Best Agent | Why |
|---|---|---|
| Multi-file refactor + doc sync | K3 | Deep reasoning, git-aware |
| Git hook authoring | K3 | Handles amend recursion, edge cases |
| Heavy codebase analysis | K3 | 2.8T MoE, 1M context |
| Quick single-file edit | Hermes (patch/terminal) | Overkill to spawn subagent |
| Web research | Hermes (web_search) | K3 is filesystem-only via kimi-code |
| PR review | OpenCode or Claude Code | Those have dedicated review modes |
