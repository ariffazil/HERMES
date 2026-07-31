# Hermes Telegram Image Routing — Decision Trace (2026-07-30)

## The problem

When a user sends a photo via Telegram to Hermes (running DeepSeek V4 Flash, text-only), image bytes need to reach a vision-capable model without causing a cascade failure.

## The three pathways

### Path 1 — `_enrich_message_with_vision` (deployed, robust ✅)
**Flow:** Telegram → download → `_decide_image_input_mode` → `"text"` → `_enrich_message_with_vision()` → calls `vision_analyze_tool()` → MiniMax-M3 via OpenAI API (base64 image) → returns `[IMAGE TRANSCRIPT]` text → DeepSeek Flash responds normally.

**Failure mode:** MiniMax API fails → `[couldn't analyze image]` text prepended → DeepSeek still responds. Single-hop. No cascade.

**Config required:**
```yaml
auxiliary:
  vision:
    provider: minimax
    model: minimax-m3
    timeout: 120
model:
  supports_vision: false        # CRITICAL — do NOT set true on text-only models
```

### Path 2 — Path B model swap (removed, fragile ❌)
**Flow:** Telegram → download → `_decide_image_input_mode` → `"text"` → set `_pending_vision_model_overrides` → swap agent model to minimax-m3 → attach native image → run → restore model.

**Failure mode:** If swapped model fails (auth, provider down), image bytes are already in context. Fallback models (llama, groq) get `image_url` parts they can't process → 413 → compression → 413 → dead. **No recovery.**

**Removed** from code in favour of Path 1 (2026-07-30).

### Path 3 — A2A delegation (governance-gated, impractical for vision ❌)
**Flow:** Hermes → POST a2a JSON-RPC to AAA `:3001/a2a` → EMD validation gate (needs W3 ≥ 0.3) → AAA routes to OpenClaw → OpenClaw runs vision → returns description.

**Failure mode:** EMD gate blocks unauthenticated agents (W3=0.1). Need Ed25519 identity binding through `arif_init` which is constitutional overhead for a simple vision call. 4 hops + governance gates = overweight for task.

## Key config pitfalls

| Config | Wrong value | Impact | Fix |
|--------|-------------|--------|-----|
| `model.supports_vision` | `true` on text-only model | `decide_image_input_mode` returns `"native"` → raw pixels sent to API that can't process them | Set `false` |
| Dual gateway processes | Two `gateway run --replace` alive | 409 Conflict on Telegram token → model "fails" with mysterious cascade | `kill <old_pid>` |
| `auxiliary.vision.provider` | `openrouter` | OpenRouter credits exhaust faster than MiniMax Token Plan | Use `minimax` |
| `auxiliary.vision.api_key` | `''` (empty) | Vision model call fails silently (auth error). **Kill chain:** vision fail → message continues to primary model → primary model is text-only but prompt says "analyze this image" → model hallucinates content from memory/context — NOT from the image. Hallucinated content looks plausible (built from real context fragments) so hard to detect. | Set to `${MINIMAX_API_KEY}` for direct MiniMax, or leave empty when `provider: openrouter` (OpenRouter resolves its own key) |
| `MINIMAX_BASE_URL` env var | `ENC[AES256_GCM,...]` (sops encrypted) | `urlparse` gets garbage → `"Invalid IPv6 URL"` → all MiniMax API calls fail. Propagates through `resolve_api_key_provider_credentials` → `raw_base_url` → `_wrap_if_needed` → `base_url_hostname` → crash. Note: `base_url` in config may be correct, but `_wrap_if_needed` uses `raw_base_url` (the decrypted value) not the corrected `base_url` — framework quirk. | Ensure env var is plain URL: `MINIMAX_BASE_URL=https://api.minimax.io` |
| `auxiliary.vision.base_url` | not set | Falls through to provider's default base_url, which may be wrong or come from sops-encrypted env var. | Set explicitly: `auxiliary.vision.base_url: https://api.minimax.io/v1` — overrides provider's auto-resolved URL |

## Code locations (Hermes gateway v33)

| Function | File | Line | Purpose |
|----------|------|------|---------|
| `_decide_image_input_mode()` | `gateway/run.py` | 15147 | Resolves routing for current model |
| `decide_image_input_mode()` | `agent/image_routing.py` | 418 | Core decision table |
| `_supports_vision_override()` | `agent/image_routing.py` | 180 | Checks `model.supports_vision` in config |
| `_explicit_aux_vision_override()` | `agent/image_routing.py` | 346 | Checks if `auxiliary.vision` is configured |
| `_enrich_message_with_vision()` | `gateway/run.py` | 15233 | Calls `vision_analyze_tool`, returns text |
| `_prepare_inbound_message_text()` | `gateway/run.py` | 10432 | Orchestrates image routing (Path 1 branch at line 10534) |
| `_handle_message_with_agent()` | `gateway/run.py` | 10879 | Consumes enriched text + runs agent |

## Testing MiniMax-M3 vision (2026-07-30)

Both URL-based and base64-encoded images tested:

```python
# OpenAI-compatible endpoint, works with standard chat/completions
curl -s https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax-m3",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
      ]
    }]
  }'
```

Response time: ~2-6s. Returns OpenAI-format response with `choices[0].message.content`.

## A2A endpoint (2026-07-30)

AAA at `127.0.0.1:3001`:
- A2A health at `GET /health`
- A2A send task at `POST /a2a` with `A2A-Version: 1.0` header
- Governed by EMD validation gate (W3 threshold 0.3)
- Returns `_membrane` envelope with actor, authority, verdict, receipt
- Authentication required for meaningful routing
