# OpenCode Model Resolution — Precedence Chain

**Discovered: 2026-07-10** — Model kept reverting to `mimo-v2.5-pro` despite config changes.

## Model Resolution Hierarchy (highest → lowest priority)

```
1. agent[agent_name].model      ← overrides everything else
2. opencode run --model FLAG   ← CLI flag (works when auth allows)
3. opencode.json model field   ← workspace (~/.openclaw/workspace/opencode/) OR home (~/.config/opencode/)
4. model.json recent/favorite  ← state file (~/.local/state/opencode/) used as fallback
```

**Root cause discovered:** `opencode.json` had `model: "opencode-go/deepseek-v4-flash-free"` set correctly, BUT the `agent.forge.model` override inside the same file was still `"tokenplan-mimo/mimo-v2.5-pro"`. The agent override wins — so every `opencode run` used mimo regardless of the top-level model setting.

## Fix Applied

```python
# ~/.config/opencode/opencode.json
# BEFORE (broken — agent model override wins):
d["agent"]["forge"]["model"] = "tokenplan-mimo/mimo-v2.5-pro"

# AFTER (fixed):
d["agent"]["forge"]["model"] = "opencode-go/deepseek-v4-flash-free"
```

## State File: model.json

`~/.local/state/opencode/model.json` tracks `recent` models and `favorite` list. Can influence selection when config is ambiguous. Update it if you want a specific model to be sticky:

```json
{
  "recent": [{"providerID": "opencode-go", "modelID": "deepseek-v4-flash-free"}],
  "favorite": ["opencode-go/deepseek-v4-flash-free"]
}
```

## Working Free Models (opencode-go provider)

`opencode-go` provider uses free models — **no API key required**:

| Model | Status | Notes |
|-------|--------|-------|
| `opencode-go/deepseek-v4-flash-free` | ✅ WORKS | Primary free model |
| `opencode-go/big-pickle` | ✅ WORKS | Small model |
| `opencode-go/deepseek-v4-pro` | ❌ Missing API key | Governor blocks |
| `opencode-go/kimi-k2.7-code` | ❌ Missing API key | |
| `opencode-go/deepseek-v4-flash-free` | ✅ Works via `--model` flag too | |

## Governor Blocks Non-Free Models

Even with `--model deepseek/deepseek-v4-flash` flag → `"Error: Unauthorized: Authentication Fails (governor)"`.

The `opencode-go` provider bypasses this because it routes through OpenCode's internal free-tier routing, not the per-provider auth system.

## Verification Command

```bash
timeout 20 opencode run "model name" 2>&1 | head -3
# Should show: > forge · deepseek-v4-flash-free
# NOT:        > forge · mimo-v2.5-pro
```

## Debugging Path

If model is wrong despite config changes:
1. Check `~/.config/opencode/opencode.json` → top-level `model` field
2. Check `~/.config/opencode/opencode.json` → `agent[forge/auditor/ops].model` overrides
3. Check `~/.local/state/opencode/model.json` → `recent` list (state file)
4. Check `~/.openclaw/workspace/opencode.json` → workspace-level model
5. Try `opencode --model opencode-go/deepseek-v4-flash-free run "test"` — if this works, the provider is fine, the config precedence is the issue
