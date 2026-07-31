# MuleRouter Integration Transcript — 2026-07-30 (Session 2: TTS & Image Gen)

**Status:** ✅ LIVE — Hermes default provider + multimodal layer.
**Key env:** `MULEROUTER_API_KEY` → `/root/.secrets/kunci-mas.env`

## Session 2.5: 413 Cascade Fix & Auxiliary Vision Alignment (2026-07-30b)

### The 413 Cascade Root Cause

**Problem:** User sent an image via Telegram. The fallback cascade failed completely:
1. MuleRouter deepseek-v4-flash (primary) — text-only model, image bytes too large → fail
2. TokenRouter deepseek-v4-pro — fail
3. OpenRouter auto-beta — fail
4. Groq — 413 Payload Too Large
5. Compression attempted 3 times — still 413
6. All MuleRouter vision fallbacks also failed

**Root cause: Provider mismatch between primary and auxiliary vision.**

| Setting | Value | Problem |
|---------|-------|---------|
| `model.provider` | `mulerouter` | ← Primary changed to MuleRouter |
| `auxiliary.vision.provider` | `openrouter` | ← Still on OpenRouter! |
| `auxiliary.vision.model` | `qwen/qwen2.5-vl-72b-instruct` | ← Old model |

When OpenRouter enrichment failed (empty transcript), the raw image bytes were forwarded to MuleRouter's text-only DeepSeek Flash → 413. The two providers had different failure domains: OpenRouter had a stale/expired model config, MuleRouter had no vision capability on deepseek-v4-flash.

**Fix (applied):**
| Setting | After |
|---------|-------|
| `auxiliary.vision.provider` | `mulerouter` |
| `auxiliary.vision.model` | `qwen-vl-max` |
| `image_input_mode` | `text` (single declaration at root level) |

**Lesson:** When changing `model.provider`, the `auxiliary.vision.provider` MUST be aligned to the same provider family. The enrichment and the primary must share the same failure domain — if the provider is down, both fail together (correct behavior: vision enrich fails → agent says "sorry can't see" instead of 413 cascade).

### Gateway Ops: Systemd vs User Service

The ASI bot runs via `systemctl restart hermes-asi-gateway.service`, which executes `/usr/local/bin/hermes-gateway-secure.sh`. This script sources `/root/AAA/agents/hermes-asi/runtime/.env` and unsets `OPENAI_BASE_URL` to prevent routing poisoning.

`hermes gateway start` runs a SEPARATE user service with different env vars. Running BOTH creates competing gateway instances that fight over Telegram polling.

**Rule for ASI bot config changes:** Only use `systemctl restart hermes-asi-gateway.service`. Never `hermes gateway start` for production.


### GPT Image 2 — Verified Working
**Endpoint:** `POST /vendors/openai/v1/gpt-image-2/generation`
**Poll:** `GET /vendors/openai/v1/gpt-image-2/generation/{task_id}`

Body:
```json
{
  "prompt": "A red circle on white background, minimal",
  "quality": "high",
  "size": "1024x1024",
  "n": 1,
  "format": "png"
}
```
**Quality values:** `high`, `medium`, `low`, `auto` (NOT `standard`)
**Result:** 1024x1024 PNG, 248KB. Task completed in ~5s.

### MiniMax Speech 2.8 HD TTS — Verified Working
**Endpoint:** `POST /vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation`
**Poll:** `GET /vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation/{task_id}`

Body:
```json
{
  "prompt": "Assalamualaikum. Ini adalah ujian suara dari MuleRouter.",
  "voice_setting": {
    "voice_id": "Wise_Woman",
    "speed": 1.0,
    "vol": 1.0,
    "pitch": 0
  },
  "output_format": "url"
}
```
**Voice IDs:** `Wise_Woman` ✅. `male-qn-qingshu` ❌ does not exist.
**Result:** 8.4s BM MP3, 128kbps, 32kHz mono, 136KB. Completed in ~3s.

Also available: **Turbo** variant at `speech-2.8-turbo` (faster, lower quality).

### Async Task Pattern (All Generation Endpoints)
All non-chat endpoints use the same async pattern:
1. `POST` → `{"task_info": {"id": "...", "status": "pending"}}`
2. Poll `GET /.../{task_id}` until `status: "completed"` or `"failed"`
3. Result contains URL (images[], audios[], etc.)

## Integration Steps (Session 1)

1. **Key staged** — replaced `«redacted:sk-…»` placeholder with real key in kunci-mas.env (line 294)
2. **Provider registered** — added `mulerouter` provider to `/root/.hermes/config.yaml` with 8 models
3. **Fallback chain** — inserted at Positions 2 (qwen3-max, 30s) and 3 (qwen-vl-max, 30s)
4. **Tested** — all 3 endpoints confirmed working

## Provider Config (Live)

```yaml
mulerouter:
  name: MuleRouter (multimodal — Qwen, Grok, GPT, Wan, MiniMax)
  api: https://api.mulerouter.ai/vendors/openai/v1
  key_env: MULEROUTER_API_KEY
  transport: openai_chat
  models:
    - id: qwen3-max
      name: Qwen3 Max — fast text (1015ms)
    - id: qwen3-omni-flash
      name: Qwen3 Omni Flash — omni vision+text (1030ms)
    - id: qwen-vl-max
      name: Qwen VL Max — best vision quality (1883ms)
    - id: qwen3-vl-plus
      name: Qwen3 VL Plus — vision quality (2282ms)
    - id: qwen3.6-flash
      name: Qwen3.6 Flash — cheapest fast text
    - id: qwen3.7-max
      name: Qwen3.7 Max — reasoning heavy (5810ms)
    - id: gpt-5.5
      name: GPT 5.5
    - id: grok-4
      name: Grok 4
    - id: deepseek-v4-flash
      name: DeepSeek V4 Flash — fast text via MuleRouter
    - id: deepseek-v4-pro
      name: DeepSeek V4 Pro — constitutional via MuleRouter (backup)
```

**Note:** The `api` URL omits `/chat/completions` — Hermes' OpenAI-compatible transport appends that suffix automatically. Setting it to the full path results in double suffix (`.../v1/chat/completions/chat/completions`).

## Endpoint Tests (curl, all ✅)

### Test 1: Text (qwen3-omni-flash)
```bash
curl -s "https://api.mulerouter.ai/vendors/openai/v1/chat/completions" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-omni-flash","messages":[{"role":"user","content":"Say MuleRouter works in 3 words."}],"max_tokens":30}'
```
→ `"Route, Transform, Deliver"` ✅

### Test 2: Text (qwen3-max)
```bash
curl -s "https://api.mulerouter.ai/vendors/openai/v1/chat/completions" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-max","messages":[{"role":"user","content":"Say MuleRouter works in 3 words."}],"max_tokens":30}'
```
→ `"MuleRouter works seamlessly."` ✅

### Test 3: Vision URL (qwen-vl-max)
```bash
curl -s "https://api.mulerouter.ai/vendors/openai/v1/chat/completions" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-vl-max","messages":[{"role":"user","content":[{"type":"text","text":"What colors? Answer in 3 words."},{"type":"image_url","image_url":{"url":"https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"}}]}],"max_tokens":30}'
```
→ `"Blue, white, black"` (83 image tokens) ✅

## Fallback Chain (Live)

```
 1. tokenrouter/deepseek-v4-pro          (20s) — reasoning reserve
 2. qwen3-max                            (30s) ← MULEROUTER
 3. qwen-vl-max                          (30s) ← MULEROUTER
 4. openrouter/auto-beta                 (60s) — smart failover
 5. groq/llama-3.1-8b-instant           (20s)
 6. sea-lion/Qwen-SEA-LION-v4           (20s)
 7. gemini-2.5-flash                     (20s)
 8. tokenrouter/MiniMax-M3              (20s)
 9. tokenrouter/z-ai/glm-5.2           (20s)
10. openrouter/free                      (60s)
11. ollama/qwen2.5-coder:3b             (20s)
```

## Key Constraints Discovered

1. **DeepSeek models NOW AVAILABLE** — Initially MuleRouter only had Qwen, GPT, Grok. As of 2026-07-30 testing, `/v1/models` returns deepseek-v4-flash AND deepseek-v4-pro. Both work via MuleRouter's `/vendors/openai/v1/chat/completions` endpoint. DS Flash returns `reasoning_content` field (DeepSeek-native thinking format) before `content` — need higher `max_tokens` to see actual content after reasoning tokens are consumed.
2. **No base64 vision** — `/v1/chat/completions` rejects `data:` URIs. Only publicly accessible image URLs work. This makes MuleRouter unusable as Hermes' `auxiliary.vision.provider` (Telegram images are encoded as base64).
3. **Endpoint path** — Use `/vendors/openai/v1/chat/completions`. The bare `/v1/chat/completions` returns 404 on `api.mulerouter.ai`. The website at `mulerouter.ai` also 404s on `/v1/chat/completions` — only the `/vendors/openai` prefix works.
4. **Hermes Openai-compatible base URL** — In Hermes `config.yaml`, set `api: https://api.mulerouter.ai/vendors/openai/v1` (NOT `/v1/chat/completions`). The Hermes transport appends `/chat/completions` automatically, so the full URL becomes `.../vendors/openai/v1/chat/completions` ✓.
5. **`hermes config set model.provider` TRUNCATES the model block** — Running `hermes config set model.provider mulerouter` replaces the ENTIRE `model:` YAML block with just `provider` and `default`, dropping `supports_vision`, `request_timeout`, `context_length`, `max_tokens`, and `timeout`. Always fix via sed or python3 after: `sed -i 's/provider: old/provider: new/' /root/.hermes/config.yaml`. Backup is auto-created at `config.yaml.corrupt.<timestamp>.bak`.

## Available Models (Live, 2026-07-30)

Confirmed via `GET /vendors/openai/v1/models`:

deepseek-v4-flash, deepseek-v4-pro, glm-5.1, gpt-5.4, gpt-5.4-mini, gpt-5.4-nano, gpt-5.5, gpt-5.6-luna, gpt-5.6-sol, gpt-5.6-terra, grok-4, grok-4-20-non-reasoning, grok-code-fast-1, kimi-k2.6, qwen-flash, qwen-plus, qwen-vl-max, qwen3-max, qwen3-max-2026-01-23, qwen3-omni-flash, qwen3-vl-flash, qwen3-vl-plus, qwen3.5-flash, qwen3.5-omni-flash, qwen3.5-omni-plus, qwen3.5-plus, qwen3.6-flash, qwen3.6-max-preview, qwen3.6-plus, qwen3.7-max, qwen3.7-plus

## Per-Agent Routing Strategy (Proposed)

| Agent | Text | Via | Vision | Via |
|---|---|---|---|---|
| 333-AGI / OpenCode | deepseek-v4-pro | OpenRouter | qwen-vl-max | MuleRouter |
| Hermes (chat) | deepseek-v4-flash | OpenCode Go | qwen3-omni-flash | MuleRouter |
| 555-ASI (research) | qwen3-max | MuleRouter | qwen3-vl-plus | MuleRouter |
| 888-APEX (verdict) | deepseek-v4-pro | OpenRouter ONLY | N/A | — |
| GEOX Δ (seismic) | deepseek-v4-pro | OpenRouter | qwen-vl-max | MuleRouter |
| Recovery | qwen2.5:3b | Ollama | — | — |
