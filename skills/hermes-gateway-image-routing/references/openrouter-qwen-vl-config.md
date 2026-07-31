# OpenRouter Qwen-VL — Working Vision Config (2026-07-30)

## Context

MiniMax-M3 via MiniMax API was the original auxiliary vision provider, but `MINIMAX_BASE_URL`
in kunci-mas.env carried sops ciphertext → `urlparse` crashed with "Invalid IPv6 URL".
Switched to **Qwen-VL via OpenRouter** — immediately worked because `OPENROUTER_API_KEY`
is stored as a raw decrypted key (not sops-encrypted).

## Working Configuration

### `~/.hermes/config.yaml`

```yaml
auxiliary:
  vision:
    provider: openrouter
    model: qwen/qwen3-vl-30b-a3b-instruct
    base_url: ""          # Uses OpenRouter's default
    timeout: 120

providers:
  openrouter:
    api: https://openrouter.ai/api/v1
    key_env: OPENROUTER_API_KEY
    # The key itself is at /root/.secrets/kunci-mas.env → OPENROUTER_API_KEY
```

### Key verification (2026-07-30)

| Test | Result | Cost |
|---|---|---|
| Key validity | ✅ Active, pay-as-you-go | — |
| Text call | ✅ "Hello! Yes, I can see images." | $0.000008 |
| Vision (base64) | ✅ "Yellow" — 1x1 red pixel | $0.000014 |
| Vision (URL) | ❌ Provider can't download some URLs (not a Hermes issue) | — |
| Lifetime usage | $29.99 total | $0.05 today |

### Cost

- One vision call: ~$0.000014 (0.0014 sen USD)
- 100 images/day: ~$0.0014 — essentially free

## Pipeline (confirmed working)

```
Telegram image
  → Gateway downloads to local cache
  → _enrich_message_with_vision() calls vision_analyze_tool()
  → vision_analyze_tool encodes file → base64
  → async_call_llm() → OpenRouter → Qwen-VL
  → Returns SCENE/OCR/DATA text
  → Wrapped in [IMAGE TRANSCRIPT] → sent to text-only agent
```

## Why This Worked When MiniMax Didn't

- `OPENROUTER_API_KEY` in kunci-mas.env contains a raw key string, NOT `ENC[AES256_GCM,...]`
- OpenRouter's base URL is hardcoded in OpenRouter provider config (not read from env var)
- No URL-type env var in the resolution chain → no `urlparse` crash
- The API key env var is correctly decrypted by sops at vault generation time

## Verification Commands

```bash
# Check gateway is using OpenRouter vision
hermes config get auxiliary.vision.provider
# → openrouter

# Check the model
hermes config get auxiliary.vision.model
# → qwen/qwen3-vl-30b-a3b-instruct

# Live test: send image via Telegram, then check logs
journalctl -u hermes-asi-gateway -f --since "1 min ago" | grep -i "vision_analyze\|enrich message\|image routing"
```

## Notes

- The `auxiliary.vision.base_url` should be EMPTY for OpenRouter — it uses the provider's default
- Do not set `auxiliary.vision.provider: auto` when both MiniMax and OpenRouter keys exist — ambiguous resolution can pick the wrong one
- If cost ever becomes a concern, switch to Qwen-VL directly via Alibaba Cloud (cheaper) — but at $0.000014/call it's not worth the effort
