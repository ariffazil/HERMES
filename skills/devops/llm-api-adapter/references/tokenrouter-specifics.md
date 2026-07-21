# TokenRouter Integration Specifics

Researched 2026-07-20. Deep-dive updated same day after full integration.

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/responses` | POST | Yes | Primary — send `{"model":"...","input":"..."}` |
| `/v1/models` | GET | Yes | **Returns 200** with full model list (113 models as of 2026-07-20) |
| `/v1/chat/completions` | POST | Yes | **404** — doesn't exist, use adapter |
| `/health` | GET | No | `{"status":"ok","message":"health"}` |

**Base URL:** `https://api.tokenrouter.com/v1` (prefer `.com` over `.io` — better error messages in Chinese)

## Critical Headers

TokenRouter CRASHES (returns 500 HTML) if these headers are missing:
```
Accept: application/json
User-Agent: Tokenrouter/Python 1.2.1
Content-Type: application/json
Authorization: Bearer sk-...
```

Without `Accept`+`User-Agent`, the server middleware crashes before reaching the auth layer — returns 500 HTML instead of 401 JSON. The SDK sends these automatically; raw curl/httpx does NOT.

## Domain Comparison

| Aspect | `api.tokenrouter.com` | `api.tokenrouter.io` |
|--------|----------------------|----------------------|
| Error language | Chinese (descriptive) | English (vague) |
| 401 inactive key | `"该令牌状态不可用"` | `"Unauthenticated."` |
| 403 model blocked | `"no access to model X"` | Same (English) |
| 503 no channel | `"No available channel"` | Same (English) |
| `/v1/models` | 200 | 404 |
| `/health` | 200 | 200 |
| Adapter target | **Use this** | Fallback only |

## API Key Formats & Lifecycle

**Two key types:**
- **Model-request key**: `sk-{36-char}` like `sk-8RwSRpWQKJbQjooUTcVIk3thqkLd0E6J6jt4FJvNk9MVtpSx` — used for `/v1/responses`
- **Management key**: `sk-FU{...}` — console-only, cannot make model requests (401)

**Key lifecycle stages discovered 2026-07-20:**
1. Created → **Inactive** (Chinese: `"该令牌状态不可用"`)
2. **Enable** in console → Active but may have model restrictions
3. **403 "no access to model"** → clear "Allowed Models" field (leave blank)
4. **503 "no channel"** → TokenRouter platform issue, not user-fixable
5. **200** → working

**Fixing keys (console steps):**
1. API Keys → click key → toggle **Enabled** ON
2. **Allowed Models** → leave BLANK (empty = allow all models)
3. Quota → Unlimited
4. Save → test with `curl /v1/responses`

No programmatic management API exists. Provider management is console-only.

## Model Naming Convention

TokenRouter uses `provider/model-name` format (with FORWARD SLASH `/`, NOT colon `:`):
```
anthropic/claude-sonnet-4
deepseek/deepseek-v4-pro
google/gemini-3.5-flash
openai/gpt-4o-mini
qwen/qwen3.7-max
x-ai/grok-4.20-beta
```

**Adapter model handling:** Only add `auto:` prefix when model has no `:` AND no `/`:
```python
if ":" not in model and "/" not in model and model != "auto":
    model = f"auto:{model}"
```

## Model Catalog (as of 2026-07-20)

113 models returned by `/v1/models`. Available types:
- **Text** (106 models): OpenAI, Anthropic, DeepSeek, Google, Qwen, xAI, MiniMax, Kimi, GLM, Mistral, ByteDance, NVIDIA, Tencent, Xiaomi, StepFun
- **Image** (5): seedream-4.5/5.0, gpt-5-image, mai-image-2.5
- **Video** (4): kling-v3, Hailuo-2.3, happyhorse-1.0-t2v
- **Audio** (2): gpt-audio, gpt-audio-mini
- **Multimodal** (Text+Image): gemini-3-pro-image-preview, gemini-3.1-flash-image-preview, gemini-2.5-flash-image
- **Multimodal** (Text+Video): qwen3.5-omni-plus
- **Embedding**: gemini-embedding-2

**WORKING models (200 on `/v1/chat/completions` via `api.tokenrouter.com`):**

ALL models work via `api.tokenrouter.com/v1/chat/completions` — the `.com` domain has full Chat Completions support. The `.io` domain is Responses API only.

Verified working (2026-07-20):
| Model | Provider |
|-------|----------|
| `deepseek/deepseek-v4-pro` | DeepSeek V4 Pro |
| `deepseek/deepseek-v4-flash` | DeepSeek V4 Flash |
| `z-ai/glm-5.2` | GLM 5.2 (FREE until Jul 25) |
| `MiniMax-M3` | MiniMax M3 |
| `google/gemini-3.5-flash` | Gemini 3.5 Flash |
| `xiaomi/mimo-v2.5-pro` | MiMo V2.5 Pro |
| `anthropic/claude-sonnet-4` | Claude Sonnet 4 |
| `google/gemini-3-flash-preview` | Gemini 3 Flash |
| `qwen/qwen3.7-max` | Qwen 3.7 Max |
| `x-ai/grok-4.20-beta` | Grok 4.20 Beta |

**Key lesson:** Use `api.tokenrouter.com` for Chat Completions. Use `api.tokenrouter.io` for Responses API. Different domains, different protocols.

Most models return 503 "No available channel" — this is a TokenRouter distributor platform issue. Only models with active upstream provider connections work.

## Response Format (Nested Output Array)

TokenRouter returns OpenAI Responses API format:
```json
{
  "id": "gen-1784508871-ZFTYDHM2EzZR6QfZ5dQ6",
  "object": "response",
  "model": "anthropic/claude-sonnet-4",
  "status": "completed",
  "output": [
    {
      "id": "msg_tmp_21n3l53nh83",
      "type": "message",
      "role": "assistant",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "text": "Hello world, how are you?",
          "annotations": [],
          "logprobs": []
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 13,
    "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0}
  }
}
```

**Parser logic (correct extraction):**
```python
raw_output = tr_data.get("output")
if isinstance(raw_output, list):
    for item in raw_output:
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    result_text = c.get("text")
```

Do NOT use `tr_data.get("output")` directly as a string — it's always an array.

## Error Code Reference

| HTTP | Error Message | Cause | Fix |
|------|--------------|-------|-----|
| 400 | varies | Bad request format, wrong endpoint type for model | Check model's `supported_endpoint_types` |
| 401 | "Unauthenticated." (.io) | Key not recognized | Verify key is active |
| 401 | "该令牌状态不可用" (.com) | Key exists but disabled | Console → Enable key |
| 403 | "no access to model X" | Model restriction on key | Clear Allowed Models field |
| 500 | HTML error page | Missing headers OR upstream routing crash | Add Accept+User-Agent headers; check provider config |
| 503 | "No available channel for model X" | No upstream provider connection | TokenRouter platform issue — not user-fixable |

## BYOK Headers

Pass provider keys inline to bypass console provider setup:
```
X-OpenAI-Key: sk-...
X-Anthropic-Key: sk-ant-...
X-Gemini-Key: ...
X-Mistral-Key: ...
X-DeepSeek-Key: sk-...
```

## Python SDK (tokenrouter v1.2.1)

Generated Stainless client. Auth uses `self.api_key` → `custom_auth` on httpx client (not simple Bearer).
```python
from tokenrouter import Tokenrouter
client = Tokenrouter(api_key="sk-...")
resp = client.responses.create(input="Hello", model="auto:balance", max_output_tokens=100)
```

SDK sends correct headers automatically (`Accept`, `User-Agent`, `x-stainless-*`).

## Adapter Deployment

⚠️ **ADAPTER DELETED 2026-07-20** — Not needed. `api.tokenrouter.com` has native `/v1/chat/completions`. Use direct provider config instead. The adapter was built for `.io`'s Responses API but `.com` makes it unnecessary. Template preserved at `templates/tokenrouter_adapter.py` for future reference only.

Direct Hermes provider config (what we use now):
```yaml
providers:
  tokenrouter:
    name: TokenRouter (Unified Gateway)
    api: https://api.tokenrouter.com/v1
    key_env: TOKENROUTER_API_KEY
    transport: openai_chat
    models:
      - id: deepseek/deepseek-v4-pro
      - id: deepseek/deepseek-v4-flash
      - id: MiniMax-M3
      - id: z-ai/glm-5.2
      - id: google/gemini-3.5-flash
      - id: xiaomi/mimo-v2.5-pro
```

If you ever need the adapter again (for `.io` Responses API or another non-Chat-Completions endpoint):
```bash
cd /root/scripts && python3 tokenrouter_adapter.py &
# But prefer probing .com first — saves hours.
```
