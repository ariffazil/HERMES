# MiMo V2.5 Series — Multimodal Configuration Reference (2026-07-18)

## Models (capability matrix — verified 2026-07-18 live benchmark)

| Model ID | Type | Capabilities | Cost (per MTok input, pay-per-usage) |
|----------|------|-------------|---------------------------------------|
| `mimo-v2.5-pro-ultraspeed` | **Text, ultra-fast** | Deep thinking, DFlash parallel decoding, 1M context, 128K output, 490-1000 tok/s | $1.305 (cache hit $0.0108) |
| `mimo-v2.5-pro` | Text reasoning | Deep thinking, structured output, tool calling, 1M context | $0.435 (cache hit $0.0036) |
| `mimo-v2.5` | **Multimodal** | Image + audio + video understanding, 1M context | $0.14 (cache hit $0.0028) |
| `mimo-v2.5-asr` | Speech recognition | Audio → text | $0.074 per audio hour |
| `mimo-v2.5-tts` | Speech synthesis | Text → speech (voice clone, voice design variants available) | FREE (limited time promotion) |

**Critical insight:** UltraSpeed is **TEXT-ONLY** despite the "Pro" branding. To get multimodal coverage while keeping UltraSpeed as the default, mark it `supports_vision: false` and route images to `mimo-v2.5` via `auxiliary.vision`. See "Pitfall: supports_vision flag" in SKILL.md.

## Pay-per-usage vs Token Plan endpoints (verified 2026-07-18)

| Endpoint | Key prefix | Use case |
|---|---|---|
| `https://api.xiaomimimo.com/v1` | `sk-` | **Pay-per-usage** (newer, default) |
| `https://api.xiaomimimo.com/anthropic` | `sk-` | Claude Code (Anthropic protocol) |
| `https://token-plan-sgp.xiaomimimo.com/v1` | `tp-` | Token Plan subscription (Singapore) |
| `https://token-plan-sgp.xiaomimimo.com/anthropic` | `tp-` | Token Plan SGP for Claude Code |

Both endpoints serve the same models. Register both providers if you have both keys (different billing).

## Auth headers (verified 2026-07-18)

Both work on every endpoint above:
- `Authorization: Bearer <KEY>` (OpenAI-compat, default for curl/Hermes/OpenCode)
- `api-key: <KEY>` (vendor's preferred per mimo.mi.com docs)

Pick Bearer for OpenAI-compat clients. The doc page lists both as supported — don't assume one is broken because the other fails.

## Provider config — pay-per-usage example

```yaml
providers:
  mimo-platform:
    name: Xiaomi MiMo Platform (pay-per-usage)
    api: https://api.xiaomimimo.com/v1
    key_env: MIMO_PLATFORM_API_KEY
    transport: openai_chat
    models:
      - { id: mimo-v2.5-pro-ultraspeed, name: "MiMo V2.5 Pro UltraSpeed (1000 tok/s)" }
      - { id: mimo-v2.5-pro,            name: "MiMo V2.5 Pro (text, deep thinking)" }
      - { id: mimo-v2.5,                name: "MiMo V2.5 (multimodal)" }
      - { id: mimo-v2.5-asr,            name: "MiMo V2.5 ASR" }
      - { id: mimo-v2.5-tts,            name: "MiMo V2.5 TTS" }
      - { id: mimo-v2.5-tts-voicedesign, name: "MiMo V2.5 TTS VoiceDesign" }
      - { id: mimo-v2.5-tts-voiceclone,  name: "MiMo V2.5 TTS VoiceClone" }
```

## Provider config — Token Plan SGP example (existing)

```yaml
providers:
  xiaomi-mimo:
    name: Xiaomi MiMo (Token Plan SGP)
    api: https://token-plan-sgp.xiaomimimo.com/v1
    key_env: XIAOMI_API_KEY
    transport: openai_chat
    models:
      - id: mimo-v2.5-pro
        name: MiMo-V2.5-Pro
      - id: mimo-v2.5
        name: MiMo-V2.5
```

## Auxiliary vision config (forces image routing when main model is text-only)

```yaml
auxiliary:
  vision:
    provider: mimo-platform       # or xiaomi-mimo for Token Plan
    model: mimo-v2.5              # the multimodal variant — NOT pro, NOT ultraspeed
    timeout: 120

model:
  default: mimo-v2.5-pro-ultraspeed
  supports_vision: false          # CRITICAL — force auxiliary routing

agent:
  image_input_mode: auto
```

## MiMo V2.5 capabilities (from vendor docs)

- **Image understanding**: up to 16M pixels per image, multi-image input
- **Video understanding**: up to 2h video, 2GB max
- **Audio understanding**: accepts audio input for analysis
- **Speech recognition (ASR)**: dedicated model, billed per audio duration
- **Speech synthesis (TTS)**: text-to-speech with voice clone and voice design variants
- **Deep thinking**: mimo-v2.5-pro and UltraSpeed support extended reasoning chains
- **Structured output**: JSON output from visual/text input
- **Tool calling**: function calling support on mimo-v2.5-pro and UltraSpeed
- **Web search**: built-in web search capability (all three text models)

## UltraSpeed benchmark — 2026-07-18 (api.xiaomimimo.com, pay-per-usage)

| Test | Pro | **UltraSpeed** | mimo-v2.5 multimodal |
|---|---|---|---|
| Latency (simple fact) | 1.14s | **0.75s** (35% faster) | 2.56s (reasoning heavy) |
| Throughput (500 tok) | 11.0s @ 45 tok/s | **3.2s @ 156 tok/s** (3.4× faster) | 14.0s @ 36 tok/s |
| Native decode TPS | n/a | **485-490 tok/s** (DFlash) | n/a |
| Reasoning tokens (logic problem) | 0 | 237 | 383 |
| Web search tool | ✓ | ✓ | ✓ |
| Image input | ✗ 404 | ✗ silent drop | ✓ accepts |

## V2 deprecation notice

MiMo-V2 series (mimo-v2-pro, mimo-v2-omni, mimo-v2-tts) deprecated June 30, 2026.
Migrate to V2.5 series. V2 models may still work but will be removed.

## Hermes native support gaps

| MiMo capability | Hermes native? | Current Hermes alternative |
|----------------|---------------|---------------------------|
| Vision (auxiliary) | ✅ via auxiliary.vision | — |
| Main model | ✅ via model.default | — |
| STT (ASR) | ❌ | local faster-whisper, groq, openai whisper, mistral |
| TTS | ✅ as of 2026-07-08 via tts.mimo block | edge (free), elevenlabs, openai, minimax, mistral, neutts |

## Token plan pricing (from vendor FAQ)

- Packages: Lite, Standard, Pro, Max (monthly or annual)
- Night discount (0:00-8:00 Beijing Time = 16:00-24:00 UTC): 0.8x consumption coefficient
- First purchase: 12% off (one-time)
- Annual subscription: 12% off vs monthly
- TTS all models: FREE for limited time

## Probe command (pay-per-usage)

```bash
curl -sS -H "Authorization: Bearer $MIMO_PLATFORM_API_KEY" \
  https://api.xiaomimimo.com/v1/models | python3 -c "
import sys,json
d=json.load(sys.stdin)
for m in d.get('data',[]): print(m['id'])
"
# Output (2026-07-18):
# mimo-v2.5
# mimo-v2.5-asr
# mimo-v2.5-pro
# mimo-v2.5-pro-ultraspeed
# mimo-v2.5-tts
# mimo-v2.5-tts-voiceclone
# mimo-v2.5-tts-voicedesign
```

## Availability on other providers

MiMo V2.5 models are also available through OpenCode Go (proxy):

| Provider | Model | Rate limit (Go sub) |
|----------|-------|-------------------|
| mimo-platform (direct pay-per-usage) | mimo-v2.5-pro | Per-token billing |
| mimo-platform (direct pay-per-usage) | mimo-v2.5-pro-ultraspeed | Per-token billing, peak 1000 tok/s |
| mimo-platform (direct pay-per-usage) | mimo-v2.5 | Per-token billing |
| xiaomi-mimo (direct Token Plan SGP) | mimo-v2.5-pro | Token Plan quota |
| xiaomi-mimo (direct Token Plan SGP) | mimo-v2.5 | Token Plan quota |
| opencode-go (proxy) | mimo-v2.5-pro | 3,250 req/5h |
| opencode-go (proxy) | mimo-v2.5 | 30,100 req/5h |
| opencode-go (proxy) | mimo-v2.5-free | Free tier, daily quota |

**NOTE:** OpenCode Go does NOT serve `mimo-v2.5-pro-ultraspeed` as of 2026-07-18 — only Pro, mimo-v2.5, and free variants. For UltraSpeed use `mimo-platform` direct.

Direct provider is preferred for primary use (better rate limits, full multimodal). OpenCode Go is useful as a cross-proxy fallback when direct MiMo quota exhausted.
