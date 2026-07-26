# Kimi Code Spawning Guide

**Binary:** `/root/.kimi-code/bin/kimi`

## Flags

| Flag | Purpose | Combines With |
|------|---------|---------------|
| `-p, --prompt <text>` | Run one prompt non-interactively | **NOT** with `--auto` |
| `--auto` | Auto-approve all actions (interactive) | **NOT** with `-p/--prompt` |
| `-y, --yolo` | Auto-approve all actions (alias for --auto) | Interactive only |
| `-m, --model <alias>` | Model alias from config.toml | Any |
| `-S, --session [id]` | Resume session | Interactive |
| `-c, --continue` | Continue last session for cwd | Interactive |
| `--plan` | Start in plan mode | Interactive |
| `acp` | Run as ACP server over stdio | — |
| `server` | Run local REST + WebSocket + web UI | — |

## Key Learning

**`--auto` and `--prompt` are mutually exclusive.** `--prompt` already runs non-interactively — it sends one prompt and returns the output. `--auto` is an interactive flag that skips approval prompts. Don't combine them:

```bash
# WRONG — error: "Cannot combine --prompt with --auto"
kimi --auto -p "implement feature X"

# RIGHT
kimi -p "implement feature X"
```

## Background Execution

```bash
# Spawn and get notified when done
cd /root/AAA && /root/.kimi-code/bin/kimi -p "$(cat scope.md)" 2>&1

# Or via terminal with background + notify
terminal(command="cd /root/AAA && /root/.kimi-code/bin/kimi -p \"$(cat scope.md)\" 2>&1", background=true, notify_on_complete=true)
```

## Model Config

Config at `/root/.kimi-code/config.toml` — starts empty so built-in defaults apply. `kimi provider` command manages LLM providers non-interactively.

**Provider config** lives transparently (visible via `kimi provider list`) but model entries are not stored in config.toml by default. If `-p` fails with `config.invalid: Model not configured`, the model alias from `provider list` is not registered in toml. Fix:

```bash
# 1. Check available providers and their model aliases
kimi provider list
# Example output:
#   managed:kimi-code  type=kimi  models=2  source=oauth
#   minimax-coding-plan  type=anthropic  models=7  source=inline
#   Default model: minimax-coding-plan/MiniMax-M3

# 2. Set default_model in config.toml
cat > ~/.kimi-code/config.toml << 'EOF'
default_model = "minimax-coding-plan/MiniMax-M3"
EOF

# 3. Or pass explicitly via -m flag (overrides config)
kimi -m "minimax-coding-plan/MiniMax-M3" -p "your prompt here"
```

**Fallback when CLI fights you:** If Kimi Code keeps failing on model config, use `delegate_task` instead — it spawns a subagent with Hermes' own model, no external CLI setup needed. Same execution, zero config debugging.
