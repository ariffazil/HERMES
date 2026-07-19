---
name: lightweight-image-generation
description: "Generate images without heavy local installs — free APIs, pre-generated galleries, and quick alternatives when ComfyUI/SD isn't available."
version: 1.0.0
tags: [image-generation, free-api, pollinations, ai-faces, lightweight, fallback]
metadata:
  hermes:
    category: creative
    related_skills: [comfyui, minimax-cli]
---

# Lightweight Image Generation

Free, no-install image generation for when ComfyUI isn't available or overkill.

## Pollinations.ai — Free Text-to-Image

Best option for quick AI image generation. No API key, no auth, no rate limit.

```bash
# URL-encode the prompt
curl -sL "https://image.pollinations.ai/prompt/YOUR_PROMPT%20HERE?width=512&height=512&nologo=true&seed=42" \
  -o /tmp/generated.jpg
```

**Parameters:**
- `width` / `height` — image dimensions (default 512)
- `nologo=true` — remove watermark
- `seed` — reproducible generation (any integer)
- Uses FLUX model under the hood

**Tips:**
- Prompt must be URL-encoded (`%20` for spaces, `%2C` for commas)
- Timeout 30-60s typical — generous with `curl --max-time 90`
- Returns JPEG directly (not JSON)
- Good for: realistic portraits, scenes, objects, creative concepts
- Quality: comparable to SDXL, decent for social media / casual use

**Example prompts:**
```
handsome muscular malay man gym selfie realistic portrait
beautiful malay woman wearing hijab studio portrait professional
kuala lumpur skyline sunset photorealistic
```

## Generated Photos — Pre-Generated AI Faces

2.6M+ photorealistic AI faces that don't belong to real people.
Gallery: `https://generated.photos/faces`

### Downloading (Signature-Locked CDN)

```bash
# Step 1: Navigate to gallery in browser, get image URLs
# Step 2: Download with EXACT URL (can't resize!)
curl -sL -H "Referer: https://generated.photos/" \
  "https://images.generated.photos/<SIGNATURE>/rs:fit:256:256/<PATH>" \
  -o /tmp/face.jpg
```

**Critical pitfalls:**
- CDN URLs are **signature-locked**. Changing `rs:fit:256:256` to `rs:fit:512:512` returns `{"detail":"Bad Signature"}`
- Must use the **exact URL** as it appears on the page
- Must include `Referer: https://generated.photos/` header
- Gallery is a **SPA** — URL params like `?ethnicity=asian` don't work; must use in-page JS filters
- `thispersondoesnotexist.com` is **DEFUNCT** (domain for sale as of 2026-07)

### Filtering by ethnicity/gender

The SPA filter requires JavaScript interaction. Use `browser_click` on filter buttons:
1. Navigate to `https://generated.photos/faces`
2. Click "Ethnicity" button → click "Asian" / "Black" / etc.
3. Get image URLs from `browser_get_images()`
4. Download with exact URLs + Referer header

**Note:** "Asian" category is mostly East Asian (Chinese/Japanese/Korean). Limited Southeast Asian / Malay faces.

## Decision Tree

| Need | Tool | Install? |
|------|------|----------|
| Quick image, any quality | Pollinations.ai | None |
| AI-generated face (fake person) | Generated Photos | None (browser) |
| High-quality, specific style | ComfyUI / SDXL | GPU + install |
| Video generation | MiniMax (`mmx video`) | npm install |
| Image from text, API | MiniMax (`mmx image`) | npm install |

## Pitfalls

1. **Pollinations rate limit (disguised as image)** — Returns JSON error `{"error":"Too Many Requests","message":"Queue full for IP: ..."}` as a ~1KB file with `.jpg` extension. **Always verify output with `file` command after download.** If it says "JSON text data" or file size < 5KB, it's a rate limit error, not an image. Fix: `sleep 10 && curl ...` with `--max-time 120`. Same IP can queue ~1 request at a time.
2. **Pollinations timeout** — some prompts take 60s+. Use `--max-time 90` for first attempt, `--max-time 120` for retry.
3. **Generated Photos signature** — NEVER modify the URL path. Copy exact.
4. **Face detection bias** — free face generators have poor Malay/SEA representation. Most are white/East Asian. When generating SEA/Malay faces, the model may default to East Asian features. Prompt with specific ethnic descriptors but accept the limitation.
5. **Reverse image search** — AI-generated faces from these services can sometimes be detected. For catfish detection, always recommend Google reverse image search.
