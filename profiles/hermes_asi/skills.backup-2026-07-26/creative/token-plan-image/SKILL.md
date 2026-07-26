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

## 📋 Notes

- Token Plan image generation is billed from Credits at the same rate as text — no extra surcharge.
- `qwen-image-2.0-pro` and `wan2.7-image-pro` are higher quality / slower; default `qwen-image-2.0` is fastest.
- For image-editing (input image + edit prompt), use `wan2.7-image-pro` with `input.messages[0].content = [{ "image": "<input_url>" }, { "text": "<edit prompt>" }]`.
- Quota: each generation consumes Credits; check `usage` block in response for cost.

---

## 🧭 Route

> **Canonical model-selection lives in [`minimax-cli`](../minimax-cli/SKILL.md#-image-generation--primary-for-malaysea--realism).**
> **Policy:** `/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md`

**When to use Qwen over MiniMax:** Text+image editing (`wan2.7-image-pro` — only model supporting image input). Generic prompts where phenotype doesn't matter. When MiniMax quota is exhausted.

**Prompt decomposition for Malay slang:** See [`minimax-cli` 🧬 Phenotype](../minimax-cli/SKILL.md#-phenotype). Add explicit "Southeast Asian Malay" tokens. Never rely on slang alone.

**Default chain:** MiniMax image-01 (SEA/realism) → Qwen image-2.0-pro (generic) → Pollinations (free).