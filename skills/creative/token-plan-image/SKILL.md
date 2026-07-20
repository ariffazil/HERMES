---
name: "token-plan-image"
description: "Call the Qwen Token Plan text-to-image / image-edit models (qwen-image-2.0, qwen-image-2.0-pro, wan2.7-image, wan2.7-image-pro) to generate or edit images from a text description. Activates when the user asks to draw, render, generate, or edit an image. For Malay/SEA phenotype prompts, prefer minimax-cli (MiniMax image-01)."
version: 2.0.0
tags: [qwen, token-plan, image-generation, text-to-image, image-editing]
metadata:
  hermes:
    category: creative
    related_skills: [minimax-cli, lightweight-image-generation]
  forge_policy: "/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md"
---

Call the Qwen Token Plan multimodal-generation API to generate (or edit) an image based on a description.

User request: $ARGUMENTS

## Inputs to extract

Parse `$ARGUMENTS` and pull out (with defaults shown):

- **prompt** (required): the image description / edit instruction
- **model** (default `qwen-image-2.0`): one of `qwen-image-2.0`, `qwen-image-2.0-pro`, `wan2.7-image`, `wan2.7-image-pro`
- **size** (default `1024*1024`): `1024*1024`, `1280*1280`, `720*1280`, `1280*720`, or any `W*H` accepted by the model
- **n** (default `1`): number of images (1–4)

## Step 1 — Call the API (use bash via terminal / shell tool)

The auth token is `$QWEN_API_KEY` (already in the shell environment, sourced from `/root/.secrets/qwen.env` or `/root/.openclaw/.env`).

```bash
curl -s -X POST "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<MODEL>",
    "input": {
      "messages": [
        { "role": "user", "content": [ { "text": "<PROMPT>" } ] }
      ]
    },
    "parameters": { "size": "<SIZE>", "n": <N> }
  }'
```

If the response is HTTP 400 with `code: "Throttling.AllocationQuota"` → token-plan quota exhausted. Tell the user to top up at https://home.qwencloud.com/billing/subscription/token-plan and stop.

If the response is HTTP 401 → token invalid. Tell the user to rotate `QWEN_API_KEY` in `/root/.secrets/qwen.env` and re-source.

If the response is HTTP 200 with `code: "InvalidApiKey"` → the API key has valid format but is expired/deactivated. This is distinct from 401 (bad format) — DashScope returns 200 with an error body. Tell the user the key needs renewal at https://home.qwencloud.com/billing/subscription/token-plan. Rotate key in `/root/.secrets/qwen.env` and re-source. Proven 2026-07-20: `sk-sp-D.IPRH...` returned `{"code":"InvalidApiKey","message":"Invalid API-key provided."}`.

**Pre-flight:** Before calling the API, verify the key is set and healthy: `echo $QWEN_API_KEY` should be non-empty. Expired keys fail with 200+InvalidApiKey, not 401 — easy to miss.

## Step 2 — Extract image URLs

The response JSON shape:

```json
{
  "output": {
    "choices": [
      {
        "message": {
          "content": [
            { "image": "https://<signed-url>" }
          ]
        }
      }
    ]
  }
}
```

Walk every `output.choices[*].message.content[*].image` URL.

## Step 3 — Download the images

For each URL, download to current working directory:

```bash
curl -sL -o "generated_$(date +%Y%m%d_%H%M%S)_<i>.png" "<URL>"
```

If `Content-Type` from the response header is `image/jpeg` change the extension to `.jpg`; if `image/webp` to `.webp`. PNG is the default.

## Step 4 — Report

Print to the user:

- The exact local file path(s) generated
- The model + size used
- A one-line description of the image (re-read the prompt)

## Notes

- Token Plan image generation is billed from Credits at the same rate as text — no extra surcharge.
- `qwen-image-2.0-pro` and `wan2.7-image-pro` are higher quality / slower; default `qwen-image-2.0` is fastest.
- For image-editing (input image + edit prompt), use `wan2.7-image-pro` with `input.messages[0].content = [{ "image": "<input_url>" }, { "text": "<edit prompt>" }]`.
- Quota: each generation consumes Credits; check `usage` block in response for cost.

---

## Model Selection (Federation Policy, 2026-07-20)

> **Policy:** `/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md`
> Qwen Token Plan is ONE option — NOT always the best option.

### When to use Qwen vs MiniMax vs Pollinations

| Condition | Use | Why |
|-----------|-----|-----|
| Malay/SEA phenotype required | MiniMax image-01 | Strongest SEA phenotype reading |
| Realism-critical / studio quality | MiniMax image-01 | Natural skin texture, stable anatomy |
| Text+image editing (input + edit prompt) | Qwen wan2.7-image-pro | Only model supporting image input |
| Generic, non-phenotype-specific | Qwen image-2.0 | Fast, good quality, same quota pool |
| Free prototyping / quick draft | Pollinations | Zero cost |

### Prompt Decomposition for Culturally-Loaded Prompts

When receiving Malay/SEA slang, decompose into explicit attributes BEFORE calling the API:

| Slang | Decomposition |
|-------|--------------|
| `abang sado` | {male, Southeast Asian Malay, muscular build, shirtless, fitness, gym or studio} |
| `Melayu` | {Southeast Asian Malay ethnicity, natural skin texture, dark hair, brown eyes} |
| `amoi` | {female, Southeast Asian Chinese/Malay phenotype, young adult} |
| `mat rempit` | {male, Malay, young, motorcycle, street, urban Malaysia} |

**Rule:** Never rely on the model inferring ethnicity from slang alone. Add explicit phenotype tokens.

### Contrast Data — Why MiniMax Wins for Malay

"Abang sado" test (2026-07-20): MiniMax produced 1024×1024, 184KB, strong SEA features. Pollinations produced 768×768, 73KB, Westernized generic output.

**Default chain for federation surfaces:**
1. MiniMax image-01 (Malay/SEA, realism)
2. Qwen image-2.0-pro (generic high-quality)
3. Pollinations (free, last resort)