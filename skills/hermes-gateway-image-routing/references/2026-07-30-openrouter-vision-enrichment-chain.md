# OpenRouter Vision Enrichment Chain — 2026-07-30

## Context
Session where image enrichment via Telegram gateway was fully broken. Root cause: three-layer failure chain. Fix required provider migration from MiniMax-M3 to OpenRouter + Qwen2.5-VL-72B.

## Failure Chain

```
User sends image → Gateway calls _enrich_message_with_vision()
  → Layer 1: MiniMax MCP server dead (crashes on launch, parked after 3 attempts)
  → Layer 2: OpenRouter marked unhealthy (payment/credit error, 600s circuit-break)
  → Layer 3: Main model DeepSeek V4 Flash doesn't support image_url content type
  → 400 error: "unknown variant 'image_url', expected 'text'"
  → [IMAGE TRANSCRIPT] never generated
  → Raw image path dumped to agent context
  → Agent can't see image
```

## Log Evidence

```
Jul 30 12:55:22 WARNING mcp_tool: MCP server 'minimax' failed connection after 3 attempts
Jul 30 12:55:47 WARNING auxiliary_client: Auxiliary: marking openrouter unhealthy for 600s
Jul 30 12:55:48 ERROR vision_tools: Error: unknown variant 'image_url', expected 'text'
```

## Fix Applied

### Config changes (hermes config set)

| Key | Before | After |
|---|---|---|
| `auxiliary.vision.provider` | (empty/minimax) | `openrouter` |
| `auxiliary.vision.model` | (empty/qwen/qwen-vl-plus) | `qwen/qwen2.5-vl-72b-instruct` |
| `auxiliary.vision.base_url` | `https://api.minimax.io/v1` | `''` (cleared) |
| `auxiliary.vision.api_key` | (was set) | `''` (cleared) |

### Model Name Pitfall

`qwen/qwen-vl-plus` is **deprecated** on OpenRouter. The API returns:
```
404 - {'error': {'message': 'No endpoints found for qwen/qwen-vl-plus.'}}
```

Replace with one of:
- `qwen/qwen2.5-vl-72b-instruct` (tested working, 200 OK)
- `qwen/qwen3-vl-32b-instruct`
- `qwen/qwen3-vl-8b-instruct`

### Gateway Restart Required

Config changes take effect only after gateway restart. Cannot `systemctl restart hermes-asi-gateway` from within the gateway session (it kills the agent). Must be done from a separate shell or at session end.

## Verification

Test call that confirmed the fix works:
- Model: `qwen/qwen2.5-vl-72b-instruct`
- Status: 200 OK
- Tokens: 1254 in / 303 out
- Image: 1280x960 JPEG PETRONAS event announcement screen
- Cost: ~$0.000014 per call

## OpenRouter Model Discovery

To find available Qwen VL models:
```python
import requests
resp = requests.get("https://openrouter.ai/api/v1/models",
    headers={"Authorization": "Bearer $OPENROUTER_API_KEY"})
for m in resp.json()['data']:
    if 'qwen' in m['id'] and ('vl' in m['id'] or 'vision' in m['id']):
        print(m['id'])
```

## Key Lessons

1. Always check ALL three layers in gateway logs — don't stop at the first error
2. Model names change on OpenRouter without notice — verify before setting
3. OpenRouter payment errors circuit-break for 600s — a single failed call poisons all subsequent calls
4. MiniMax MCP server is unreliable — prefer HTTP-based auxiliary providers
5. Base64 vision calls from Python work reliably; curl inlining fails for images >50KB
