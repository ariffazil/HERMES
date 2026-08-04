# HERMES-ASI Multimodal Capability Matrix

> Source: Xiaomi MiMo docs + MiniMax docs + T0 live verification (2026-08-04)
> Verified by: Kimi K3/FI-008 (direct API probes) + Hermes (docs cross-ref)
> Status: AUTHORITATIVE — treat as source of truth for routing decisions

---

## Architecture Note

Agents call providers **direct** (via `~/.hermes/config.yaml` provider URLs), NOT via LiteLLM proxy.
LiteLLM `:4000` is health probe target + FED route metadata source only.
Do NOT route multimodal calls through LiteLLM — they will fail.

---

## Provider Endpoints

| Provider | Endpoint | Balance | Notes |
|---|---|---|---|
| **MiMo** (primary) | `https://token-plan-sgp.xiaomimimo.com/v1` | $10 (Track B, manual) | Token Plan SGP. MIMO_API_KEY |
| **MiniMax** (fallback) | `https://api.minimax.io/v1` | $0 (empty) | MINIMAX_API_KEY. Dead until top-up |
| **MiMo docs** | `https://api.xiaomimimo.com/v1` | — | Docs use this. Same vendor, different gateway |

---

## Capability Matrix

### TEXT CHAT
- **Models:** `mimo-v2.5-pro`, `mimo-v2.5`, `minimax-m3`
- **Status:** ✅
- **How:** Standard `messages=[{role, content}]` — no extra flags needed
- **Context:** 1M tokens (MiMo V2.5)
- **Max output:** 131,072 tokens

### DEEP THINKING (CoT)
- **Models:** `mimo-v2.5-pro`, `mimo-v2.5`
- **Status:** ✅ **ON by default**
- **Force ON:** `extra_body={"thinking": {"type": "enabled"}}`
- **Force OFF:** `extra_body={"thinking": {"type": "disabled"}}`
- **Note:** When ON, `temperature` and `top_p` are **forced to 1.0 / 0.95** — custom values ignored
- **Streaming:** First streams `reasoning_content` chunks, then `content` chunks
- **Multi-turn:** MUST pass back `reasoning_content` field in assistant messages containing tool calls. Missing field → **400 error** on some Xiaomi plans.

### IMAGE UNDERSTANDING
- **Model:** `mimo-v2.5` (**NOT** -pro)
- **Status:** ✅ (verified T0: image_tokens=1024)
- **Input format:**
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "text", "text": "describe this image"},
        {"type": "image_url", "image_url": {"url": "https://..."}}
    ]
}]
```
- **Also:** Base64 encoding supported. Multi-image input supported.
- **Verify:** Check `usage.completion_tokens > 0` in response
- **Restrictions:** No local file upload. URL or Base64 only.

### AUDIO UNDERSTANDING
- **Model:** `mimo-v2.5`
- **Status:** ✅ (docs confirmed, not T0 tested from VPS)
- **Input format:**
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "input_audio", "input_audio": {"data": "https://..."}},
        {"type": "text", "text": "describe the audio"}
    ]
}]
```
- **Formats:** MP3, WAV, FLAC, M4A, OGG
- **Size limits:** URL ≤100MB, Base64 ≤50MB
- **Token calc:** `total_tokens ≈ audio_duration_seconds × 6.25`
- **Note:** ≠ STT (Whisper). Audio understanding = semantic Q&A over audio content.

### VIDEO UNDERSTANDING
- **Model:** `mimo-v2.5`
- **Status:** ✅ (docs confirmed, not T0 tested from VPS)
- **Input format:**
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "video_url", "video_url": {"url": "https://..."}, "fps": 2, "media_resolution": "default"},
        {"type": "text", "text": "describe the video"}
    ]
}]
```
- **Params:** `fps` (default 2, max ~5), `media_resolution` ("default" | "max")
- **Max frames:** 2048
- **Mute option:** `mute=True` skips audio token calculation
- **Cold start:** 30-60s first hit, up to 180s for video
- **Token calc:** Complex — vision tokens + timestamp tokens + audio tokens (if not muted)

### STRUCTURED OUTPUT (JSON Mode)
- **Models:** `mimo-v2.5-pro`, `mimo-v2.5`
- **Status:** ✅
- **How:**
```python
response_format={"type": "json_object"}
```
- **Must:** Instruct model explicitly in system/user message to return JSON only
- **Post-validate:** Use `jsonschema` library — model may omit required keys
- **Streaming:** Supported — concatenate chunks client-side before parse

### WEB SEARCH
- **Models:** `mimo-v2.5-pro`, `mimo-v2.5`
- **Status:** ⚠️ **Requires MiMo Console plugin activation** (separate billing)
- **Cost:** $5 per 1,000 requests (overseas) / ¥16 (China)
- **How:**
```python
tools=[{
    "type": "web_search",
    "max_keyword": 3,        # limit keywords per round
    "force_search": True,    # force even if model thinks it's not needed
    "limit": 1,              # results per keyword
    "user_location": {"type": "approximate", "country": "MY", "region": "KL", "city": "Kuala Lumpur"}
}]
```
- **Note:** One search round may fire multiple keyword searches concurrently. `max_keyword` controls cost.
- **5-min cache:** After enabling/disabling plugin, takes 5 min to take effect.

### FUNCTION CALLING
- **Status:** ✅
- **How:** Standard OpenAI-compatible `tools` array with `function` type
- **Supported:** Parallel tool calls, multi-turn tool loops

---

## Quick Reference by Use Case

| Use case | Model to call | Endpoint |
|---|---|---|
| Casual chat | `mimo-v2.5-pro` | MiMo SGP |
| Deep reasoning | `mimo-v2.5-pro` (thinking ON by default) | MiMo SGP |
| Analyze image | `mimo-v2.5` (NOT -pro) | MiMo SGP |
| Understand audio | `mimo-v2.5` | MiMo SGP |
| Understand video | `mimo-v2.5` | MiMo SGP |
| JSON extraction | `mimo-v2.5-pro` | MiMo SGP |
| Web search | `mimo-v2.5-pro` (plugin ON) | MiMo SGP |
| TTS (speech) | MiniMax `speech-2.8-hd` | MiniMax |
| Music generation | MiniMax `music-3.0` | MiniMax |
| Video generation | MiniMax `H3` | MiniMax |

---

## Known Gotchas

1. **`mimo-v2.5-pro` ≠ `mimo-v2.5`** — Pro = deep thinking (text-only routing historically), base = multimodal. They share endpoint but have different strengths.
2. **Thinking mode locks temp/top_p** — Can't customize when thinking is ON.
3. **reasoning_content echo** — Must pass back in multi-turn or risk 400/hallucination.
4. **MiniMax balance $0** — Fallback is dead until top-up.
5. **MiMo Token Plan SGP** — Cold start 30-60s per modality. Plan timeouts accordingly.
6. **Web search billing separate** — Token fees + per-request fees stack.
7. **Local file upload NOT supported** — Must use URL or Base64.
8. **Audio ≠ STT** — Understanding (semantic Q&A) ≠ transcription (Whisper). Different models, different APIs.

---

*Last updated: 2026-08-04 22:28 MYT*
*Next review: When MiMo or MiniMax release new model versions*
