# Auxiliary Vision Provider Routing — Debugging Guide

> When `vision_analyze` fails or uses the wrong model/provider, this is how to trace it.

## The Problem Pattern

User has `auxiliary.vision.provider` set explicitly in `config.yaml`, but `vision_analyze` routes to a different provider (often the session model's native provider) and fails.

**Seen symptom:** `"Gemini HTTP 404 (NOT_FOUND): models/mimo-v2.5-pro is not found for API version v1beta"` — even though `auxiliary.vision.provider: bailian-token-plan` is set.

## Resolution Chain (Source: `agent/auxiliary_client.py`)

### 1. Entry: `vision_analyze_tool()` in `tools/vision_tools.py`

```python
# Line ~967
call_kwargs = {
    "task": "vision",       # ← this drives provider resolution
    "messages": messages,
    "temperature": 0.1,
    "max_tokens": 2000,
    "timeout": 120.0,
}
if model:                   # only set if caller passed a model
    call_kwargs["model"] = model
response = await async_call_llm(**call_kwargs)
```

### 2. `async_call_llm(task="vision")` → `resolve_vision_provider_client()`

Located at line 4580 in `auxiliary_client.py`. Resolution order:

```
_resolve_task_provider_model("vision", provider, model, base_url, api_key)
    ↓ reads auxiliary.vision.provider from config
    ↓ reads auxiliary.vision.model from config
    ↓ returns (requested, resolved_model, resolved_base_url, resolved_api_key, resolved_api_mode)

_normalize_vision_provider(requested)
    ↓ calls _normalize_aux_provider()
    ↓ maps aliases (e.g. "google" → "gemini")
    ↓ "bailian-token-plan" passes through unchanged
```

### 3. Decision tree after normalization

```
if resolved_base_url:
    → use direct endpoint override
elif requested == "auto":
    → AUTO-DETECTION CHAIN:
       1. Main provider + _PROVIDER_VISION_MODELS[provider] override
          (e.g. xiaomi → mimo-v2-omni if mapped)
       2. OpenRouter (gemini-3-flash-preview)
       3. Nous Portal (gemini-3-flash-preview)
       4. None
elif requested in _VISION_AUTO_PROVIDER_ORDER:
    → _resolve_strict_vision_backend(requested)
elif requested == "zai":
    → special ZAI handling
else:
    → _get_cached_client(requested, ...) ← THIS IS THE PATH FOR explicit providers
```

### 4. The `_main_model_supports_vision()` gate (auto mode only)

When `requested == "auto"`, the chain checks if the main model supports vision:

```python
# Line ~4493
def _main_model_supports_vision(provider, model):
    # checks model metadata for supports_vision=True
    # if False → falls through to aggregator chain
```

If the main model reports `supports_vision=False`, auto mode skips it and tries OpenRouter/Nous.

### 5. `_PROVIDER_VISION_MODELS` mapping

When auto mode uses the main provider, it checks for a vision-specific model override:

```python
# Line ~359 — comment says:
# "xiaomi → mimo-v2-omni"
# "zai → glm-5v-turbo"
```

If the main provider is xiaomi and auto mode is active, it MAY use `mimo-v2-omni` instead of the session model.

## Why Config Gets Ignored

**Most common cause:** `image_input_mode: auto` in config triggers the `decide_image_input_mode()` function in `image_routing.py`. When `auxiliary.vision.provider` is explicitly set (not "auto"), this SHOULD force the text pipeline (vision_analyze). But:

1. The gateway's inline image handling may use a DIFFERENT code path than `vision_analyze_tool()`
2. The Gemini native adapter (`gemini_native_adapter.py`) may intercept before auxiliary resolution
3. The error message "Gemini HTTP 404" comes from `GeminiNativeClient` (line 783: `f"Gemini HTTP {status} ({err_status}): {err_message}"`)

**Key insight:** The `vision_analyze` TOOL uses `async_call_llm(task="vision")` which goes through auxiliary resolution. But user-attached images on the conversation turn may be handled by `image_routing.py` → `decide_image_input_mode()` → native attachment to the session model's provider. These are TWO DIFFERENT CODE PATHS.

## Debugging Steps

```bash
# 1. Check what's configured
grep -A5 "vision:" ~/.hermes/config.yaml

# 2. Check image_input_mode
grep "image_input_mode" ~/.hermes/config.yaml
# "auto" = system decides; "native" = attach to session model; "text" = always use vision_analyze

# 3. Check if the auxiliary vision provider is callable
# (bailian-token-plan with qwen3.7-max should work)
curl -sS -H "Authorization: Bearer $QWEN_API_KEY" \
  https://token-plan-sgp.xiaomimimo.com/v1/models | head -c 500

# 4. Check the actual error source
# "Gemini HTTP 404" = GeminiNativeClient was used → config was NOT respected
# "401 Unauthorized" = provider resolved but key is wrong
# "model not found" = provider resolved but model ID is wrong
```

## Config That Should Work

```yaml
# ~/.hermes/config.yaml
image_input_mode: text          # ← forces vision_analyze for user images

auxiliary:
  vision:
    provider: bailian-token-plan
    model: qwen3.7-max          # ← must be a vision-capable model on this provider
    base_url: ''
    api_key: ''
    timeout: 120
    extra_body: {}
    download_timeout: 30
```

**Critical:** `image_input_mode: text` forces ALL user-attached images through `vision_analyze_tool()` → auxiliary resolution chain. `image_input_mode: auto` may bypass auxiliary entirely for native-vision-capable session models.

## Key Files

| File | Role |
|---|---|
| `agent/auxiliary_client.py` | Provider resolution for all auxiliary tasks (vision, compression, web_extract) |
| `agent/image_routing.py` | Decides native vs text pipeline for user-attached images |
| `tools/vision_tools.py` | The `vision_analyze_tool()` implementation |
| `agent/gemini_native_adapter.py` | Gemini native client (produces the "Gemini HTTP 404" error) |
| `~/.hermes/config.yaml` lines 219, 353-359 | `image_input_mode` and `auxiliary.vision` config |

## Provider Vision Capability Matrix

| Provider | Has vision models? | Default vision model |
|---|---|---|
| xiaomi-mimo | Yes (mimo-v2-omni) | mimo-v2-omni (via _PROVIDER_VISION_MODELS) |
| bailian-token-plan | Yes (qwen3.7-max supports vision) | qwen3.7-max |
| opencode-go | Yes (via aggregator) | gemini-3-flash or qwen3.7-max |
| OpenRouter | Yes | google/gemini-3-flash-preview |
| Nous Portal | Yes | google/gemini-3-flash-preview |

## Related

- `hermes-provider-setup` SKILL.md — main provider registration
- `systematic-debugging` skill — the Phase 1 methodology that applies here (read error → trace source → find root cause)
