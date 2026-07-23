# OpenCode Zen & Go — Live Model Lists (verified 2026-07-24)

Probed via `GET /zen/v1/models` and `GET /zen/go/v1/models` with live API keys.
These are the actual models the API serves — the published docs may lag.

## OpenCode Zen (57 models)

Endpoint: `https://opencode.ai/zen/v1`
Auth: `Authorization: Bearer $OPENCODE_ZEN_API_KEY`

```
claude-fable-5, claude-opus-4-8, claude-opus-4-7, claude-opus-4-6, claude-opus-4-5,
claude-sonnet-5, claude-sonnet-4-6, claude-sonnet-4-5, claude-haiku-4-5,
gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.4-pro,
gpt-5.4-mini, gpt-5.4-nano, gpt-5.3-codex, gpt-5.3-codex-spark, gpt-5.2, gpt-5.2-codex,
gpt-5.1, gpt-5.1-codex, gpt-5.1-codex-max, gpt-5.1-codex-mini, gpt-5, gpt-5-codex, gpt-5-nano,
gemini-3.6-flash, gemini-3.5-flash, gemini-3.5-flash-lite, gemini-3.1-pro, gemini-3-flash,
grok-4.5, grok-build-0.1,
qwen3.6-plus, qwen3.5-plus,
deepseek-v4-pro, deepseek-v4-flash, deepseek-v4-flash-free,
minimax-m3, minimax-m2.7, minimax-m2.5,
glm-5.2, glm-5.1, glm-5,
kimi-k2.7-code, kimi-k2.6, kimi-k2.5,
mimo-v2.5-free, big-pickle, laguna-s-2.1-free, north-mini-code-free, nemotron-3-ultra-free
```

**Not on Zen (Go-only):** qwen3.7-plus, qwen3.7-max, mimo-v2.5-pro, mimo-v2.5, mimo-v2-pro, mimo-v2-omni, hy3, hy3-preview, kimi-k3

## OpenCode Go (23 models)

Endpoint: `https://opencode.ai/zen/go/v1`
Auth: `Authorization: Bearer $OPENCODE_GO_API_KEY`

```
minimax-m3, minimax-m2.7, minimax-m2.5,
kimi-k3, kimi-k2.7-code, kimi-k2.6, kimi-k2.5,
glm-5.2, glm-5.1, glm-5,
deepseek-v4-pro, deepseek-v4-flash,
qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.5-plus,
mimo-v2-pro, mimo-v2-omni, mimo-v2.5-pro, mimo-v2.5,
hy3, hy3-preview,
grok-4.5
```

## API Mode Routing (verified)

Per `opencode_model_api_mode()` in `hermes_cli/models.py`:

| Provider | Model prefix | API mode | Tested |
|---|---|---|---|
| opencode-zen | `claude-*` | `anthropic_messages` | ✅ 200 |
| opencode-zen | `gpt-*` | `codex_responses` | (not tested) |
| opencode-zen | `qwen*` | `anthropic_messages` | ✅ 200 |
| opencode-zen | all others | `chat_completions` | ✅ 200 (deepseek, glm, minimax) |
| opencode-go | `minimax-*`, `qwen*` | `anthropic_messages` | (not tested) |
| opencode-go | all others | `chat_completions` | ✅ 200 (deepseek) |

## Pricing Notes

- Go: $5 first month, $10/month. $60 monthly usage cap. DeepSeek V4 Pro ~$0.435/$0.87 per 1M tokens.
- Zen: Pay-as-you-go. DeepSeek V4 Pro $1.74/$3.48 per 1M tokens (4× Go price for same model).
- For open models, use Go (cheaper). For Claude/GPT/Gemini, use Zen (only option).
