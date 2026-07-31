# MuleRouter Integration

## What It Is

MuleRouter (`https://mulerouter.ai`) is a multimodal AI API gateway — like OpenRouter but focused on image/video/music/speech generation alongside LLM chat. One API key gives access to multiple providers (Qwen, MiniMax, Wan, Kling, Midjourney, OpenAI, Anthropic, Google) through a unified interface.

**Key registered:** `MULEROUTER_API_KEY` in `/root/.secrets/kunci-mas.env` (sk-mr-c80b...ca7)
**Base URL:** `https://api.mulerouter.ai`
**Auth:** Bearer token in Authorization header
**PAYG model:** Credit-based topup (same friction as OpenRouter)

## Available Models

| Category | Models | MuleRouter model ID |
|---|---|---|
| LLM/Chat | Qwen3.7 Max, Qwen3.6 Plus/Flash, GPT 5.5/5.4, Grok 4, GLM 5.1 | `qwen3.7-max`, `grok-4`, etc. |
| Vision/LLM | Qwen3 VL Plus, Qwen3 VL Flash, Qwen VL Max, Qwen3 Omni Flash/Plus | `qwen3-vl-plus`, `qwen3-vl-flash`, `qwen-vl-max` |
| Image gen | GPT Image 2, Nano Banana 2/Pro, Qwen Image Max, Midjourney | Async task pattern |
| Video gen | Wan 2.6/2.5/2.2/2.1, Kling V3/V3 Omni, Midjourney Video | Async task pattern |
| TTS | MiniMax Speech 2.8 HD/Turbo | Async task pattern |
| Music | MiniMax Music 2.5/2.0 | Async task pattern |

## Test Results (2026-07-30)

### Text Chat
```bash
curl -s "https://api.mulerouter.ai/vendors/openai/v1/chat/completions" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3-vl-plus", "messages": [{"role": "user", "content": "Hello"}]}'
```
✅ 13 prompt tokens, correct response

### Vision — Image URL
```bash
curl -s "https://api.mulerouter.ai/vendors/openai/v1/chat/completions" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-vl-plus",
    "messages": [{"role": "user", "content": [
      {"type": "text", "text": "What color is this?"},
      {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"}}
    ]}]
  }'
```
✅ "Multicolored" — 83 image tokens, 19 text tokens

### Vision — Base64 (data: URI)
❌ Returns: `{"error": {"code": "invalid_request", "message": "Bad request - check request format and parameters"}}`

**Conclusion:** MuleRouter does NOT support base64-encoded images via data: URIs. Only publicly accessible image URLs work.

## Impact on PRMT Pipeline

Hermes' `vision_analyze_tool` downloads Telegram images to local files, then encodes them as base64 data: URIs for the LLM API call. Since MuleRouter rejects data: URIs, it CANNOT serve as the `auxiliary.vision.provider` for the default PRMT pipeline.

**Workaround:** Upload the image to a temporary URL first, then pass the URL. Not worth the complexity — OpenRouter already handles base64 correctly.

## When to Use MuleRouter

| Use Case | Viable? | Notes |
|---|---|---|
| Auxiliary vision (PRMT) | ❌ | Base64 limitation — use OpenRouter |
| TTS fallback (replace MiMo) | ✅ | MiniMax Speech 2.8 HD/Turbo via async tasks |
| Image generation | ✅ | GPT Image 2, Nano Banana, Midjourney |
| Video generation | ✅ | Wan 2.6, Kling V3 |
| Music generation | ✅ | MiniMax Music 2.5 |
| Text-only LLM fallback | ✅ | Drop-in via /vendors/openai/v1/chat/completions |

## Pricing Notes

- Both OpenRouter and MuleRouter use **credit-based topup** — same payment friction
- MuleRouter claims "negotiated higher-tier service levels through aggregated purchasing"
- Exact pricing per model was not extractable from the JS-rendered site — check console
- `image_tokens` field in the response (83 tokens for Example.jpg) is useful for cost estimation

## Key Lessons

1. **Base64 vision only works on OpenRouter** (and direct providers) — MuleRouter rejected data: URIs
2. **MuleRouter endpoint path** is `/vendors/openai/v1/chat/completions`, NOT `/v1/chat/completions`
3. **Single key for all modalities** — reducing key management if you switch entirely
4. **Credit-based** same as OpenRouter — doesn't solve the topup friction problem
