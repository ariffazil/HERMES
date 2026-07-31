# Case: `model.supports_vision: true` Pre-empts Path B

**Date:** 2026-07-30
**Symptom:** Images sent via Telegram were not visible to the agent. Path B (qwen-vl model override) never activated.

## Environment

- **Active model:** DeepSeek V4 Flash (`deepseek` provider)
- **Vision fallback:** `qwen/qwen3-vl-30b-a3b-instruct` via OpenRouter (Path B)
- **Config file:** `~/.hermes/config.yaml` (same inode as `/root/HERMES/config.yaml`)

## Root Cause

The config had:

```yaml
model:
  provider: deepseek
  supports_vision: true    # ← misconfigured
```

This caused `_lookup_supports_vision()` at `agent/image_routing.py:205` to return `True` immediately, before checking the actual model capability or falling through to `_explicit_aux_vision_override()`.

The decision chain:

```
_lookup_supports_vision("deepseek", "deepseek-v4-flash", cfg)
  → cfg["model"]["supports_vision"] == True
  → returns True immediately (line 207)
  → decide_image_input_mode returns "native"
  → Path B NEVER reached
```

## Fix

```
hermes config set model.supports_vision false
```

After the fix, the chain becomes:

```
_lookup_supports_vision returns False
_explicit_aux_vision_override(cfg) returns True (auxiliary.vision is configured)
decide_image_input_mode returns "text"
→ Path B: defers images as native, sets model override to qwen-vl
```

## Key Code Locations

| Component | File | Lines |
|---|---|---|
| Top-level override check | `/usr/local/lib/hermes-agent/agent/image_routing.py` | 203-207 |
| Full lookup | `/usr/local/lib/hermes-agent/agent/image_routing.py` | 373-415 |
| Decision entry point | `/usr/local/lib/hermes-agent/agent/image_routing.py` | 418-450 |
| Aux vision override check | `/usr/local/lib/hermes-agent/agent/image_routing.py` | 346-370 |
| Gateway decision call | `/usr/local/lib/hermes-agent/gateway/run.py` | 10508-10551 |
| Override consumption | `/usr/local/lib/hermes-agent/gateway/run.py` | 19080-19147 |

## Config Values (post-fix)

```yaml
model:
  provider: deepseek
  supports_vision: false

auxiliary:
  vision:
    provider: openrouter
    model: qwen/qwen3-vl-30b-a3b-instruct
    timeout: 120

providers:
  openrouter:
    api: https://openrouter.ai/api/v1
    key_env: OPENROUTER_API_KEY
    # ... models
```

## Verification

Gateway log entry after successful Path B routing:
```
Image routing: PATH B (text-only primary). N image(s) deferred — model override set to qwen-vl via OpenRouter.
```
