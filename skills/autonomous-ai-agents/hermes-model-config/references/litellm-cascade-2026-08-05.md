# hermes-asi LiteLLM Cascade — Session Detail (2026-08-05)

## Full LiteLLM config for hermes-asi (from /root/A-FORGE/litellm-config.yaml)

```yaml
# Cascade: MiMo V2.5 (primary) → MiniMax M3 → DeepSeek V4 Flash → Qwen 3.6 Flash
- model_name: hermes-asi
  litellm_params:
    model: openai/mimo-v2.5
    api_base: https://token-plan-sgp.xiaomimimo.com/v1
    api_key: os.environ/MIMO_API_KEY
    request_timeout: 45
- model_name: hermes-asi
  litellm_params:
    model: openai/MiniMax-M3
    api_base: https://api.minimax.io/v1
    api_key: os.environ/MINIMAX_API_KEY
    request_timeout: 30
- model_name: hermes-asi
  litellm_params:
    model: openai/deepseek-v4-flash
    api_base: https://api.deepseek.com/v1
    api_key: os.environ/DEEPSEEK_API_KEY
    request_timeout: 30
- model_name: hermes-asi
  litellm_params:
    model: openai/qwen3.6-flash
    api_base: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    api_key: os.environ/QWEN_BAILIAN_KEY
    request_timeout: 30
```

## LiteLLM process

- PID: 4125293 (started 03:33)
- Config: `/root/A-FORGE/litellm-config.yaml`
- Port: 4000 (bound to 100.64.0.2 — Tailscale)
- Postgres: arifos_admin@litellm (Docker, 172.21.0.1)
- RPM limits: hermes-asi: 60/min, global: 300/min

## Other cascade aliases in the same config

- `hermes-asi-vision` — mimo-v2.5 + qwen3.7-plus (multimodal)
- `asi-555-audio` — mimo-v2.5 (audio lane)
- `codex` — deepseek-v4-flash (OpenAI Responses API)
- `opencode` — 60 RPM, likely deepseek or similar

## Context window verification

Each model's context from `models_dev_cache.json` (verified 2026-08-05):

| Model | Context | Output | Input cost/M | Output cost/M |
|---|---|---|---|---|
| MiMo V2.5 | 1,048,576 | 131,072 | $0.14 (≤256k) / $0.8 (>256k) | $0.28 / $4 |
| MiniMax M3 | 1,048,576 | 128,000 | $0.30 | $1.20 |
| DeepSeek V4 Flash | 1,000,000 | 384,000 | $0.14 | $0.28 |
| Qwen 3.6 Flash | 1,000,000+ | varies | varies | varies |

Cascade minimum effective context = min(all) = **1,000,000** (DeepSeek V4 Flash limits the cascade).

## Cost analysis for SOUL role

Telegram gateway SOUL role typically uses <50k tokens per turn. At 50k tokens:
- MiMo V2.5: $0.007 input + $0.014 output = ~$0.021/turn
- DeepSeek V4 Flash: same $0.007 + $0.014 = ~$0.021/turn
- MiniMax M3: $0.015 + $0.06 = ~$0.075/turn (2.6x more expensive)

At 100k tokens (complex multi-tool session):
- MiMo V2.5: $0.014 + $0.028 = ~$0.042/turn (still in ≤256k tier)
- MiMo V2.5 at 300k: $0.24 + $1.20 = ~$1.44/turn (jumped to >256k tier!)
