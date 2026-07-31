# MuleRouter Evaluation — 2026-07-30

**Status:** ✅ LIVE — integrated as Hermes default provider + multimodal layer.
**Type:** API gateway aggregator (multimodal AI)
**Base URL:** `https://api.mulerouter.ai/vendors/openai/v1` (NOT bare `/v1`)
**Docs:** `https://mulerouter.ai/docs/`
**Key env:** `MULEROUTER_API_KEY`

## What It Offers

| Capability | Endpoint | Models |
|------------|----------|--------|
| Chat/LLM | `/vendors/openai/v1/chat/completions` | deepseek-v4-flash, deepseek-v4-pro, qwen3.7-max, qwen3-max, gpt-5.5, grok-4, kimi-k2.6, glm-5.1, qwen3-omni-flash, and 20+ more |
| Vision | Chat completions with `image_url` content | qwen-vl-max, qwen3-vl-plus, qwen3-vl-flash, qwen3-omni-flash |
| Image gen | Async task: `/vendors/openai/v1/gpt-image-2/generation` | GPT Image 2, Midjourney, Nano Banana 2/Pro, Qwen Image Max |
| Video gen | Async task | Wan 2.1-2.6, Kling V3/V3 Omni, Midjourney Video |
| TTS | Async task: `/vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation` | MiniMax Speech 2.8 HD/Turbo (voice_id: `Wise_Woman`) |
| Music | Async task | MiniMax Music 2.5/2.0 |

## What's Missing vs Arif's Current Stack

| Need | Current | MuleRouter | Gap? |
|------|---------|-----------|------|
| Primary LLM (DeepSeek V4 Flash) | MuleRouter (Hermes default) | ✅ **AVAILABLE** — deepseek-v4-flash and deepseek-v4-pro via `/v1/models` | **RESOLVED 2026-07-30** |
| Vision enrich (Telegram, base64) | OpenRouter → Qwen VL Plus | ⚠️ URL-only — rejects `data:` URIs | **CONSTRAINT** (not a gap — architecture limitation) |
| STT | OpenAI Whisper / local faster-whisper | ❌ Not documented | **GAP** |
| TTS | MiMo + Edge fallback | ✅ MiniMax Speech 2.8 HD (verified working) | ✅ Alternative, verified |
| Video gen | ❌ None | Wan 2.6, Kling V3, MJ | ✅ **UNIQUE VALUE** |
| Music gen | MiniMax MCP (direct) | MiniMax Music 2.5 | ✅ Same models, different pipe |
| Image gen | Mage MCP (local, Modal) | GPT Image 2 (verified working) | ✅ Alternative, verified |
| Fixed pricing | MuleRouter fixed | ✅ Fixed pricing | ✅ Now primary for swarm traffic |

## Provider Comparison Details

### Billing
- **MuleRouter:** Satu API key, satu bill. Fixed pricing — doesn't change with demand. Pay-as-you-go.
- **OpenRouter:** Floating pricing ("harga yahudi"). Topup $5 minimum. Prices change by demand.
- **Direct:** Fixed per-provider rates. Multiple API keys, multiple bills.

### Vendor Path Architecture
MuleRouter uses `/vendors/<provider>/...` paths that mirror upstream APIs. **Critical: the bare `/v1/` prefix does NOT work** — `https://api.mulerouter.ai/v1/chat/completions` returns 404. The correct base is `https://api.mulerouter.ai/vendors/openai/v1`. This was discovered through trial and error — the docs' "industry aliases" claim was misleading. All Hermes config and scripts must use the `/vendors/` prefixed path.

### Async Task Model (All Generation Endpoints)
Non-chat capabilities (image, TTS, video, music) use the same async pattern:
1. `POST` → returns `{"task_info": {"id": "...", "status": "pending"}}`
2. Poll `GET /.../{task_id}` until `status: "completed"` or `"failed"`
3. Completed response contains the result URL (images[], audios[], etc.)

### GPT Image 2 — Verified (2026-07-30)
```
POST /vendors/openai/v1/gpt-image-2/generation
GET  /vendors/openai/v1/gpt-image-2/generation/{task_id}
```
Body: `{"prompt":"...", "quality":"high|medium|low|auto", "size":"1024x1024", "n":1, "format":"png|jpeg|webp"}`
Result: 1024x1024 PNG, 248KB — expected quality.

### MiniMax TTS — Verified (2026-07-30)
```
POST /vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation
POST /vendors/minimax/v1/speech-2.8-turbo/text-to-speech/generation
```
Body: `{"prompt":"Text to speak", "voice_setting":{"voice_id":"Wise_Woman","speed":1.0,"vol":1.0,"pitch":0}, "output_format":"url"}`
Known voice IDs: `Wise_Woman` (confirmed working), `male-qn-qingshu` (verify others)
Result: 8.4s BM MP3, 128kbps, 32kHz mono, 136KB.

## Why Not All-In MuleRouter

1. **No STT** — Arif uses voice messages via Telegram. Without speech-to-text, can't close the loop on satu roof.
2. **Base64 vision** — MuleRouter rejects `data:` URIs. The PRMT pipeline encodes Telegram images as base64 → MuleRouter can't process them. This is an architecture constraint, not a provider gap — URL-based vision (agent-initiated) works fine.
3. **Constitutional redundancy** — OpenRouter's multi-provider DeepSeek topology is still required for 888-APEX / 999-SEAL judgment. MuleRouter has a single DeepSeek endpoint — no failover.
4. **DeepSeek reasoning speed** — MuleRouter's DeepSeek V4 Pro is 6.4s on reasoning vs OpenRouter direct-to-DeepSeek which is faster hitting the native API.

## Recommended Integration Path (LIVE 2026-07-30)

**Hybrid — Wolf Cabinet 3-layer:**

| Layer | Provider | Why |
|-------|----------|-----|
| Δ Perception (chat, vision, TTS, image) | **MuleRouter** | Satu key, fixed price, multimodal |
| Ω Judgment (constitutional) | **OpenRouter** | Multi-provider DeepSeek redundancy |
| Ψ Survival (local) | **Ollama** | Sovereign, always available |

See `/root/AAA/registries/models/MULEROUTER_API_REFERENCE.md` for full API reference.
