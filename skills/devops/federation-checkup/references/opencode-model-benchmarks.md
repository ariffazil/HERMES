# OpenCode Model Benchmarks — July 2026

## Verified Working Models

| Model ID | Provider | API Key Needed | CLI Works | Notes |
|---|---|---|---|---|
| `opencode-go/deepseek-v4-flash-free` | opencode-go | ❌ NONE | ✅ | **Primary fallback** |
| `opencode-go/big-pickle` | opencode-go | ❌ NONE | ✅ | Small model, fast |
| `deepseek/deepseek-v4-flash` | deepseek | ✅ DEEPSEEK_API_KEY | ✅ | Governor blocks pro |
| `qwen-token/qwen3.7-max` | qwen-token | ✅ QWEN_API_KEY | ✅ | Was primary, Jul 2026 |
| `tokenplan-mimo/mimo-v2.5-pro` | tokenplan-mimo | ✅ MIMO_API_KEY | ❌ | **EXHAUSTED Jul 2026** |

## Verified Broken Models

| Model ID | Error | Root Cause |
|---|---|---|
| `deepseek/deepseek-v4-pro` | `Unauthorized: Authentication Fails (governor)` | Governor config blocks this model tier |
| `minimax/MiniMax-M3` | `Unexpected server error` | MiniMax provider down or quota |
| `opencode-go/kimi-k2.7-code` | `Missing API key` | opencode-go needs kimi key not set |
| `tokenplan-mimo/mimo-v2.5-pro` | (exhausted) | MIMO_API_KEY quota depleted |

## Why Model Changes Fail Silently

When `agent.{role}.model` exists in `opencode.json`, it **always overrides** the top-level `model` field.
This is the override chain:

```
agent.forge.model         → HIGHEST (always wins)
top-level model           → IGNORED if forge.model exists
--model CLI flag         → IGNORED if forge.model exists
~/.local/state/model.json → fallback only
```

**The fix:** Update all four `agent.{forge,auditor,ops,planner}.model` fields + top-level `model` + `model.json`.

## Model vs Serve Restart

`opencode serve` reads config at startup. Model changes require:
```bash
pkill -f "opencode serve"; sleep 2
opencode serve --hostname 127.0.0.1 --port 4096 &
sleep 5
timeout 20 opencode run "model name" 2>&1 | head -5
```

Expected: `> forge · deepseek-v4-flash-free`
