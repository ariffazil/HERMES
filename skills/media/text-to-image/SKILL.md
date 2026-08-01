---
name: token-plan-image
description: "Generate images via QwenCloud Token Plan. Activates when user asks to draw, generate images, or create visual content."
---

# Token Plan Image Generation

Call the Token Plan multimodal API to generate images from text descriptions.

## Supported models

| Model | Quality | Speed |
|-------|---------|-------|
| `wan2.7-image-pro` | High | Slower |
| `wan2.7-image` | Standard | Faster |

## Usage

```bash
curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer ${QWEN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.7-image",
    "input": {
      "messages": [{"role":"user","content":[{"text":"<prompt>"}]}]
    },
    "parameters": {"size":"1024*1024"}
  }'
```

## Response

Extract image URL from `output.choices[*].message.content[*].image`.

## Steps

1. Extract prompt from user request
2. Determine model (default: `wan2.7-image`) and size (default: `1024*1024`)
3. Call API with `QWEN_API_KEY` from `/root/.secrets/kunci-mas.env`
4. Extract image URL from response
5. Download: `curl -s -o "generated_$(date +%Y%m%d_%H%M%S).png" "<URL>"`
6. Display file path

## Notes

- Billed in Credits from Token Plan quota
- Async model — response may take 10-30s
- Available sizes: 1024*1024, 720*1280, 1280*720, etc.
