# OpenCode Auth Volatility (FORGED 2026-07-20)

## Pattern

OpenCode model authentication is VOLATILE across providers. Never assume a model works
based on config listing — always smoke-test before delegating real work.

## Known Auth State (2026-07-20)

All tested providers returned auth errors or timeouts:

| Model | Error |
|---|---|
| `tokenplan-mimo/mimo-v2.5-pro` | "Model not found" |
| `deepseek/deepseek-v4-pro` | "Unauthorized: Authentication Fails (governor)" |
| `minimax/MiniMax-M2.5` | "Model not found" |
| `opencode-go/opencode-go` | "Model not found" |
| `openrouter/deepseek/deepseek-v4-pro` | "Missing Authentication header" |
| `ollama/qwen2.5-coder:3b` | Timeout (60s) — model too small for complex tasks |

## Smoke Test

```bash
opencode run 'Respond EXACT: OK' --model <candidate> 2>&1
```

Success criteria: output contains `OK`, exit code 0, no provider/model/auth errors.

## Fallback Strategy

After 2 model failures:
1. **STOP cycling through models** — each failure wastes ~15 seconds and tokens
2. **Switch to direct Hermes execution** — use `delegate_task`, `patch`, `terminal`, `write_file`
3. Hermes tools are the reliable path. OpenCode is a convenience, not a dependency

## Why This Matters

During the DAG Cognition Model session (2026-07-20), 5 consecutive OpenCode model
attempts failed (~90 seconds wasted). The work was completed directly with Hermes
tools in parallel — faster than the OpenCode smoke tests combined.

## Relation to measure-before-acting

This is a specific subclass: measuring TOOL READINESS before depending on the tool.
Same as probing a service health endpoint before declaring it available.
