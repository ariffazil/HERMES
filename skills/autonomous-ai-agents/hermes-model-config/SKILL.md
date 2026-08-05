---
name: hermes-model-config
description: Diagnose and configure model selection, context length, fallback cascades, and provider routing for Hermes Agent — especially when models route through LiteLLM proxy and context detection fails. Use when context window is wrong, model resolution fails, fallback cascade needs tuning, or provider costs need optimization.
---

# Hermes Model Config

Configure and diagnose model selection in Hermes Agent, especially when models route through LiteLLM proxy and auto-detection fails.

## Context length detection failure (probe-down)

**Symptom:** agent.log shows `"Could not detect context length for model 'X' at http://127.0.0.1:4000/v1 — defaulting to 256,000 tokens (probe-down)."`

**Root cause:** LiteLLM proxy's `/v1/models` endpoint returns `context_length: null` for some models (confirmed: MiMo V2.5, MiniMax M3). Hermes probes the proxy → gets null → falls back to 256k default.

**Fix:** Set `model.context_length` explicitly in `config.yaml`:
```yaml
model:
  default: hermes-asi
  provider: openai-api
  context_length: 1048576  # or appropriate value
```

**How to find the real context window:**
1. Check `models_dev_cache.json` — contains all known models with context/output limits
2. For cascade models, check EACH fallback's context (the cascade can only use the MINIMUM)
3. Current hermes-asi cascade (verified 2026-08-05):

| Fallback | Model | Real context | Cost tier |
|---|---|---|---|
| 1° | MiMo V2.5 | 1M (1,048,576) | $0.14/$0.28 (≤256k) / $0.8/$4 (>256k) |
| 2° | MiniMax M3 | 1M (1,048,576) | $0.3/$1.2 |
| 3° | DeepSeek V4 Flash | 1M (1,000,000) | $0.14/$0.28 |
| 4° | Qwen 3.6 Flash | 1M (via Aliyun) | varies |

**Cost-aware context cap:** MiMo V2.5 has a pricing tier boundary at 256k. Context ≤256k costs $0.14/M input; above costs $0.8/M (5.7x more). For SOUL role (Telegram bridge, typically <50k tokens), 256k cap is cost-optimal. For complex multi-tool sessions, set to 1M.

## Config location trap

- Active home: `HERMES_HOME=/usr/local/lib/hermes-agent/config.yaml` — this is what the gateway reads
- Legacy home: `/root/.hermes/config.yaml` — may still have stale model config (bot_token_env, etc.)
- LiteLLM config: `/root/A-FORGE/litellm-config.yaml` — defines the cascade and model aliases

Editing the wrong file = changes that never take effect.

## Cascade configuration

The `hermes-asi` model name maps to a 4-model fallback cascade in LiteLLM:
```
# /root/A-FORGE/litellm-config.yaml
- model_name: hermes-asi
  litellm_params:
    model: openai/mimo-v2.5
    api_base: https://token-plan-sgp.xiaomimimo.com/v1
    api_key: os.environ/MIMO_API_KEY
```
Each fallback entry with the same `model_name` creates a cascade. Order = priority (first alive wins).

## Diagnosing which model actually served

```bash
# agent.log shows model per turn:
grep "turn_context" /usr/local/lib/hermes-agent/logs/agent.log | grep -oE "model=[^ ]+ provider=[^ ]+" | sort | uniq -c | sort -rn
```

## Known model registry

Models with context >200k in `models_dev_cache.json` (180 providers, check with jq):
```bash
jq '[.[] | .models | to_entries[] | select(.value.limit.context >= 200000) | {model: .key, context: .value.limit.context}]' /usr/local/lib/hermes-agent/models_dev_cache.json
```

## Multimodal routing (image/audio/video through LiteLLM)

**Symptom:** Sending an image to `hermes-asi` returns `NotFoundError: No endpoints found that support image input` — even though the upstream model supports vision.

**Root cause:** Two config layers must both declare multimodal support:

1. **LiteLLM config** (`/root/A-FORGE/litellm-config.yaml`) — each model entry needs:
   ```yaml
   - model_name: hermes-asi
     litellm_params:
       model: openai/mimo-v2.5
       supports_image_input: true  # ← REQUIRED
       mode: chat                  # ← REQUIRED
   ```
   Without these, LiteLLM rejects any request with `image_url` content parts.

2. **Hermes config** (`/root/HERMES/config.yaml`) — the `model:` block needs:
   ```yaml
   model:
     supports_vision: true
     supports_audio: true
     supports_video: true
     image_input_mode: auto  # auto = send as vision tokens when model supports it
   ```
   `image_input_mode: text` (old default) converts images to text descriptions — never sends pixels. `auto` sends as native vision tokens.

**Verification:**
```bash
# Text-only should always work:
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"ping"}]}' | jq .choices[0].message.content

# Multimodal should no longer 404 at routing layer:
# (may still 400 at provider if image format is wrong — that's provider, not routing)
```

**Known gap (2026-08-05):** MiMo v2.5 API rejects URL-based images with `Param Incorrect` — likely needs base64 encoding. Federation routing is correct; provider format is the remaining issue.

**Capability matrix after fix:**

| Path | Text | Image | Audio | Video |
|---|---|---|---|---|
| hermes-asi | ✅ | ✅ routing open | ⚠️ MiMo | ⚠️ MiMo |
| hermes-asi-vision | ✅ | ✅ | — | — |
| asi-555-audio | ✅ | — | ✅ | — |
| asi-555-video | ✅ | — | — | ✅ |

## Pitfalls

- `hermes-asi` is NOT a model — it's a LiteLLM cascade alias. The actual model varies per request.
- LiteLLM proxy requires API key for `/v1/models` — probe from Hermes (no key) gets auth error → probe-down → 256k default.
- MiMo V2.5 pricing tier boundary at 256k: going beyond costs 5.7x more per token.
- `models_dev_cache.json` is stale (downloaded periodically) — verify against live API docs for critical decisions.
