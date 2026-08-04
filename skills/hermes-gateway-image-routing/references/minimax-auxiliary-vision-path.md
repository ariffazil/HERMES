# MiniMax Auxiliary Vision Path

> Source: Audit session 2026-08-04. MiniMax M3 is Hermes' auxiliary vision provider.
> Config: auxiliary.vision.provider=minimax, auxiliary.vision.model=minimax-m3

## Current State (2026-08-04)

The Hermes auxiliary vision path uses MiniMax M3 (pay-as-you-go) to convert images to text transcripts before sending to the text-only primary model.

### Config
```yaml
auxiliary:
  vision:
    provider: minimax
    model: minimax-m3
    api_key: '{env:MINIMAX_API_KEY}'
```

### Key Facts
- API Key: pay-as-you-go (sk-cp-*), NOT Subscription Key
- Endpoint: https://api.minimax.io/v1 (OpenAI compat)
- Anthropic compat: https://api.minimax.io/anthropic (separate endpoint, same key)
- M3 is multimodal (1M context, vision-capable)
- M3 has permanent 50% discount: $0.30/M input, $1.20/M output

## MiniMax Key Types (Critical Gotcha)

| Type | Format | Use | NOT interchangeable |
|---|---|---|---|
| API Key | sk-cp-* | Pay-as-you-go balance | Cannot use for Token Plan |
| Subscription Key | Different format | Token Plan quotas | Cannot use for pay-as-you-go |

The key in MINIMAX_API_KEY is a pay-as-you-go API Key. Token Plan features (M3/M2.7 in subscription quota) require a separate Subscription Key.

## Balance Check

FED token_bank.db caches balance. It may show $0 while the key is actually live.

```bash
# Check FED cached balance
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT balance_usd, last_updated FROM providers WHERE provider_name='minimax';"

# Actually verify key works (bypass cache)
source /root/.secrets/kunci-mas.env && \
curl -s "https://api.minimax.io/v1/models" -H "Authorization: Bearer $MINIMAX_API_KEY" | \
python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data',[])))"
```

If curl returns model count > 0, key is live regardless of FED balance.

## Key Expiry Failure Mode

When MiniMax key expires or has $0 balance, the failure manifests as:
```
litellm.NotFoundError: No endpoints found that support image input.
```

This is INVISIBLE as a key issue. The proxy blames routing. Always curl the provider directly before attributing to config.

## Available Models (pay-as-you-go)

| Model | Input/M | Output/M | Context | Notes |
|---|---|---|---|---|
| MiniMax-M3 | $0.30 | $1.20 | 1M | Multimodal, vision, flagship |
| MiniMax-M2.7 | $0.30 | $1.20 | 200K | Agentic, tool use |
| MiniMax-M2.5 | $0.30 | $1.20 | 200K | Reasoning |
| MiniMax-M2.1 | $0.30 | $1.20 | 200K | 230B MoE, 10B active |
| MiniMax-M2 | $0.30 | $1.20 | 200K | Legacy |

M3 context pricing: ≤512k tokens = standard rate. >512k = 2x rate.

## Token Plan (if subscribed)

| Tier | Price | Covers |
|---|---|---|
| Plus | $20/mo | M3/M2.7/image/speech/music (NO H3 video) |
| Max | $50/mo | Daily coding + multimodal |
| Ultra | $120/mo | Heavy agent workflows |

Token Plan quota covers: text, image, speech, music.
Token Plan quota does NOT cover: H3 video, voice design, rapid voice cloning.

Credits: 1000 credits = $1, valid 365 days, overflow from Token Plan quota.

## Non-Vision MiniMax Capabilities

These are available through the same API key but NOT through Hermes auxiliary vision path:

| Capability | Endpoint | Cost |
|---|---|---|
| TTS (speech-2.8-hd) | /v1/t2a | $100/M chars |
| TTS (speech-2.8-turbo) | /v1/t2a | $60/M chars |
| Image generation (image-01) | /v1/image_generation | $0.0035/image |
| Music (music-3.0) | /v1/music | $0.15/5min |
| Voice clone | /v1/voice_clone | $1.50/voice |
| Voice design | /v1/voice_design | $3/voice |
| Video (H3) | /v1/video_generation | $0.08-$0.13/sec |
| Web search | MCP server | $0.01/request |

## Failure Chain for Image Enrichment

```
User sends image via Telegram
  → Hermes decides image_input_mode (text or native)
  → If text: _enrich_message_with_vision()
  → Calls auxiliary vision provider (MiniMax M3)
  → MiniMax returns SCENE/OCR/DATA/IDENTITY text
  → Prepended as [IMAGE TRANSCRIPT] to user message
  → Primary model (text-only) processes transcript
```

If MiniMax fails:
1. Check key works: curl /v1/models
2. Check balance: pay-as-you-go may have $0
3. Check endpoint: api.minimax.io/v1 (not api.xiaomimimo.com)
4. Check model name: minimax-m3 (lowercase, hyphen)
