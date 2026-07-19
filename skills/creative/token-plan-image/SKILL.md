---
name: "token-plan-image"
description: "Call the Qwen Token Plan text-to-image / image-edit models (qwen-image-2.0, qwen-image-2.0-pro, wan2.7-image, wan2.7-image-pro) to generate or edit images from a text description. Activates when the user asks to draw, render, generate, or edit an image."
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