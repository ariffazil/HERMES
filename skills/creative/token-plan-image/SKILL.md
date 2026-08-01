---
name: "token-plan-image"
description: "Call the Qwen Token Plan text-to-image / image-edit models (qwen-image-2.0, qwen-image-2.0-pro, wan2.7-image, wan2.7-image-pro) to generate or edit images from a"
version: 2.0.0
tags: [qwen, token-plan, image-generation, text-to-image, image-editing]
metadata:
  hermes:
    category: creative
    related_skills: [minimax-cli, lightweight-image-generation, mulerouter-media]
---

Call the Qwen Token Plan multimodal-generation API to generate (or edit) an image based on a description.

User request: $ARGUMENTS

## Inputs to extract

Parse `$ARGUMENTS` and pull out (with defaults shown):

- **prompt** (required): the image description / edit instruction
- **model** (default `qwen-image-2.0`): one of `qwen-image-2.0`, `qwen-image-2.0-pro`, `qwen-image-edit-max`, `qwen-image-edit-plus`, `qwen-image-edit`, `wan2.7-image`, `wan2.7-image-pro`, `wan2.6-image`
- **size** (default `1024*1024`): `1024*1024`, `1280*1280`, `720*1280`, `1280*720`, `1K`, `2K`, or any `W*H` accepted by the model
- **n** (default `1`): number of images (1–6 for most models; `qwen-image-edit` only supports 1)

## Step 1 — Call the API (use bash via terminal / shell tool)

**Auth:** `source /root/.secrets/kunci-mas.env` → use `$QWEN_BAILIAN_KEY`.
**Endpoint:** `https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

⚠️ **The old endpoint `dashscope-intl.aliyuncs.com` with `$QWEN_API_KEY` is EXPIRED (confirmed 2026-08-01, returns 401 InvalidApiKey).** Always use the token-plan endpoint with `QWEN_BAILIAN_KEY`.

```bash
source /root/.secrets/kunci-mas.env
curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWEN_BAILIAN_KEY" \
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

If the response is HTTP 400 with `code: "IPInfringementSuspect"` → prompt triggered IP/safety filter. **Fix:** remove brand names (magazine titles, product names), aggressive/violent language ("predatory", "killer gaze"), and overly specific pop-culture references. Simplify the prompt and retry. Proven 2026-08-01: prompt with "Iron Man Magazine", "predatory gaze", "jaw clenched" triggered it; removing those passed.

If the response is HTTP 401 or 200 with `code: "InvalidApiKey"` → key expired. Rotate `QWEN_BAILIAN_KEY` in `/root/.secrets/kunci-mas.env`.

**Pre-flight:** `source /root/.secrets/kunci-mas.env && echo $QWEN_BAILIAN_KEY` should be non-empty.

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
- Quota: each generation consumes Credits; check `usage` block in response for cost.

## 🖼️ Image Editing (wan2.7-image-pro)

For image editing, use `wan2.7-image-pro` with image(s) + text instruction in `content`:

```json
{
  "model": "wan2.7-image-pro",
  "input": {
    "messages": [{
      "role": "user",
      "content": [
        { "image": "data:image/jpeg;base64,<BASE64>" },
        { "text": "Edit instruction here" }
      ]
    }]
  },
  "parameters": { "size": "2K", "n": 1 }
}
```

**Multi-image fusion** (up to 9 input images): provide multiple `{"image": ...}` entries before the `{"text": ...}` entry. Image order matters — "Image 1" in the prompt refers to the first image entry, "Image 2" to the second, etc. Use case: take subject from Image 1, apply style/lighting/mood from Image 2.

**Size presets for edit mode:** `"1K"` (~1024×1024 total px, preserves aspect ratio) or `"2K"` (~2048×2048 total px, default). Can also use exact `"W*H"` (768×768 to 2048×2048).

**⚠️ Base64 payload pitfall:** A single JPEG image base64-encoded is ~130KB+. Shell argument limits (`ARG_MAX`) will reject inline `-d '{...}'` with base64 data. **Always write the JSON payload to a file first** (via `execute_code` / Python), then pass with `-d @/tmp/payload.json`:

```python
# In execute_code:
import base64, json
with open("image.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
payload = {"model": "wan2.7-image-pro", "input": {"messages": [{"role": "user", "content": [{"image": f"data:image/jpeg;base64,{b64}"}, {"text": "edit prompt"}]}]}, "parameters": {"size": "2K", "n": 1}}
with open("/tmp/payload.json", "w") as f:
    json.dump(payload, f)
```
```bash
# Then in terminal:
curl -s -X POST "$ENDPOINT" -H "Authorization: Bearer $QWEN_BAILIAN_KEY" -H "Content-Type: application/json" -d @/tmp/payload.json
```

**Multi-variant QC workflow (proven 2026-08-01):** For "make it hotter/better" requests, generate `n: 2` variants, download both, then run `mmx vision describe` on each to compare. Deliver both to user for selection. The vision QC catches silent failures (wrong pose, missing elements, sanitization) that you can't see as a text-only model.

```bash
# QC each variant
source /root/.secrets/kunci-mas.env
mmx vision describe --file /tmp/variant_1.png --non-interactive 2>&1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('content','')[:600])"
```

**Docs:** https://docs.qwencloud.com/developer-guides/image-generation/wan-image-editing
**Proven prompts:** See `references/fitness-edit-prompts.md` for IPInfringementSuspect workarounds, multi-image fusion patterns, and vision QC workflow.

---

## 🧭 Route

> **Canonical model-selection lives in [`minimax-cli`](../minimax-cli/SKILL.md#-image-generation--primary-for-malaysea--realism).**  
> **Image model priority:** MiniMax image-01 → MuleRouter GPT Image 2 / Wan 2.6 T2I → Pollinations FLUX → Pollinations SANA

**When to use Qwen over MiniMax:**
- **Image editing / style transfer / multi-image fusion** → Qwen wan2.7-image-pro (MiniMax has NO edit capability, only text-to-image)
- **Text-to-image with SEA/Malay phenotype** → MiniMax image-01 still primary
- **Text-to-image generic / non-phenotype** → Qwen qwen-image-2.0-pro
- **Shirtless fitness editing from existing photo** → Qwen wan2.7-image-pro (passes safety filter for fitness content in edit mode)

**Prompt decomposition for Malay slang:** See [`minimax-cli` 🧬 Phenotype](../minimax-cli/SKILL.md#-phenotype). Add explicit "Southeast Asian Malay" tokens. Never rely on slang alone.

**Default chain:** MiniMax image-01 (SEA/realism) → Qwen image-2.0-pro (generic) → Pollinations (free).