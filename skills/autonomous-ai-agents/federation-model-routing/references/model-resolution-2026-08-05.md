# Model Resolution Chain — 2026-08-05 probe data

## LiteLLM proxy location
- Proxy: socat tunnel at `127.0.0.1:4000` → `100.64.0.2:4000` (Tailscale)
- Auth: `$LITELLM_MASTER_KEY` from kunci-mas.env
- Config: remote (not on this box)

## Full model alias list (12 aliases, all with null limits)

```json
{
  "hermes-asi":     "openai/mimo-v2.5",
  "codex":          ["openai/deepseek-v4-flash", "openai/mimo-v2.5-pro", "openai/MiniMax-M3"],
  "opencode":       ["openai/deepseek-v4-flash", "openai/deepseek-v4-pro", "openai/mimo-v2.5-pro", "openai/MiniMax-M3"],
  "openclaw":       ["openai/MiniMax-M3", "openai/mimo-v2.5-pro"],
  "agi-333":        ["openai/deepseek-v4-pro", "openai/mimo-v2.5-pro", "openai/MiniMax-M3"],
  "asi-555":        ["openai/qwen3.6-flash", "openai/mimo-v2.5-pro", "openai/MiniMax-M3"],
  "apex-888":       ["openai/MiniMax-M3", "openai/deepseek-v4-pro"],
  "asi-555-vision": "openai/mimo-v2.5",
  "dispatch":       "openai/mimo-v2.5-pro",
  "hermes-asi-vision": "(not probed)",
  "asi-555-audio":  "(not probed)",
  "asi-555-video":  "(not probed)"
}
```

Note: multi-model aliases are LiteLLM routing groups (load balancing or fallback).

## Probe commands that worked

```bash
# List all models (needs auth header)
curl -s http://127.0.0.1:4000/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"

# Model info with resolution details
curl -s "http://127.0.0.1:4000/model/info" -H "Authorization: Bearer $LITELLM_MASTER_KEY"

# Filter for specific alias
curl -s "http://127.0.0.1:4000/model/info" -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  | jq '.data[] | select(.model_name == "hermes-asi")'
```

## hermes-asi full model_info response

```json
{
  "model_name": "hermes-asi",
  "litellm_params": {
    "api_base": "https://token-plan-sgp.xiaomimimo.com/v1",
    "model": "openai/mimo-v2.5",
    "request_timeout": 45,
    "use_in_pass_through": false,
    "use_litellm_proxy": false,
    "use_xai_oauth": false,
    "merge_reasoning_content_in_choices": false
  },
  "model_info": {
    "db_model": false,
    "direct_access": true,
    "max_tokens": null,
    "max_input_tokens": null,
    "max_output_tokens": null
  }
}
```

## MiMo V2.5 real limits (from models_dev_cache.json)

All providers agree on MiMo V2.5 limits:

| Provider | Context | Output |
|---|---|---|
| xiaomi (direct) | 1,048,576 | 131,072 |
| xiaomi-token-plan-sgp | 1,048,576 | 131,072 |
| xiaomi-token-plan-cn | 1,048,576 | 131,072 |
| openrouter | 1,050,000 | 131,072 |
| nano-gpt | 1,048,576 | 131,072 |
| huggingface | 262,144 | 131,072 ← different! |
| deepinfra | 262,144 | 16,384 ← different! |

**Key finding:** Same model, different providers = different limits. HuggingFace and DeepInfra report 262k, not 1M. The Xiaomi token plan endpoint is the one actually used by `hermes-asi`, and it supports 1M.

## Upstream endpoint

- URL: `https://token-plan-sgp.xiaomimimo.com/v1`
- Region: Singapore (SGP)
- Plan: Xiaomi token plan (prepaid credits)
- Auth: OpenAI-compatible API key

## Open questions (not yet resolved)

1. Where is the LiteLLM config file on the remote? (Needed to add max_input_tokens/max_output_tokens)
2. Should `hermes-asi` remain MiMo V2.5, or switch to DeepSeek V4 Flash for SOUL role?
3. Are the multi-model routing groups (codex, opencode, etc.) load-balancing or fallback? Need to check LiteLLM config for `routing_strategy`.
