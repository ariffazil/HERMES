---
name: lightweight-image-generation
description: "Generate images without heavy local installs — free APIs (Pollinations.ai), pre-generated galleries (Generated Photos), and quick alternatives"
version: 2.2.0
tags: [image-generation, free-api, pollinations, ai-faces, lightweight, fallback, malay-phenotype, nsfw, venice]
metadata:
  hermes:
    category: creative
    related_skills: [comfyui, minimax-cli, token-plan-image]
  forge_policy: "/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md"
---

# Lightweight Image Generation

Free, no-install image generation for when ComfyUI isn't available or overkill.

## 🆓 Pollinations

Quick AI image generation. Two access tiers:

### Tier 1 — Unauthenticated (GET, no key needed)

The classic `image.pollinations.ai` endpoint. Completely free, no auth.

```bash
curl -sL "https://image.pollinations.ai/prompt/YOUR_PROMPT%20HERE?width=1024&height=1024&nologo=true&enhance=true&seed=42" \
  -o /tmp/generated.jpg
```

**Parameters:**
- `width` / `height` — image dimensions (up to 1024, default 768x768 for GET)
- `nologo=true` — remove watermark
- `enhance=true` — higher quality
- `seed` — reproducible generation (any integer)
- Model: default FLUX (unauthenticated tier)

### Tier 2 — Authenticated (Bearer key, full model access)

New API at `gen.pollinations.ai`. Uses `sk_` (secret) or `pk_` (publishable) keys. OpenAI-compatible.

```bash
# GET with auth (choose model)
curl -sL "https://gen.pollinations.ai/image/YOUR_PROMPT?model=flux&width=1024&height=1024&seed=42" \
  -H "Authorization: Bearer sk_..." \
  -o /tmp/generated.jpg
```

```bash
# OpenAI-compatible POST
curl -sX POST "https://gen.pollinations.ai/v1/images/generations" \
  -H "Authorization: Bearer sk_..." \
  -H "Content-Type: application/json" \
  -d '{"model":"flux","prompt":"YOUR PROMPT","size":"1024x1024","n":1}'
```

**Available image models** (see `/v1/models` or `/image/models`):
`flux` (default, good free), `zimage`, `gptimage`, `gptimage-large`, `gpt-image-2`, `seedream5`, `seedream5-pro`, `kontext`, `nanobanana`, `klein`, `sana`, `qwen-image`, `wan-image`, `ideogram-v4-turbo`, `recraft-v4.1-vector`.

**Available video models:** `veo`, `veo-1080p`, `wan`, `wan-fast`, `seedance`, `seedance-pro`, `nova-reel`.

**Common pitfalls:**
- Rate limit on unauthenticated GET returns JSON disguised as JPEG. Always `file /tmp/generated.jpg` to verify.
- Authenticated POST may return 402 if key balance exhausted (key authentications but budget empty).
- Model names in GET use query param `model=flux`; in POST use the JSON field `model`.

### Tips (both tiers)
- Prompt must be URL-encoded (`%20` for spaces, `%2C` for commas)
- Timeout: often <1s for simple, up to 60s for complex. Use `curl --max-time 120`.
- Returns JPEG directly on GET (not JSON) — **always verify with `file` command**
- **NSFW content IS generated** — The free public endpoint `image.pollinations.ai/prompt/...` generates NSFW content without needing any `safe` parameter and requires no auth. The paid `gen.pollinations.ai` endpoint supports `safe=false` query param but requires a valid API key WITH positive Pollen credit balance. A key that passes auth (`GET /v1/models` works) may still return `402 PAYMENT_REQUIRED` if balance is $0 — auth alone is insufficient. Top up at enter.pollinations.ai.
- **Quick NSFW fallback:** When authenticated key has zero balance, fall back immediately to the unauthenticated public endpoint `image.pollinations.ai/prompt/...` — no key needed, works for NSFW content without `safe=false`.
- Quality: FLUX model comparable to Midjourney. Good for realistic portraits, scenes, creative, NSFW fantasy.
- **Multi-seed iteration** — always generate 5+ seeds for variety; see `references/prompt-engineering.md`
- **Vision feedback loop** — after generation, call `vision_analyze()` to evaluate aesthetic match before refining. Prompt: "Describe the image quality, the subject, lighting, and composition in detail."
- **Key types:** `sk_...` = secret key (server only). `pk_...` = publishable key (safe for browsers). Get keys at enter.pollinations.ai.

## 👤 Faces

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

## 🚨 Critical Principle: Provider Guardrails ≠ Model Weights

**The same base model (FLUX, SDXL, etc.) can produce different outputs depending on the provider's infrastructure layer.** Never claim universal behavior. This is the single most common overclaim pattern — assume identical weights, assume safe_mode=off means 100% uncensored, assume auth = generation capability. All three are false without source verification.

```
Model weights (neutral)
    ↓
Provider safety layer (varies by provider)
    ├── Input filter (prompt blocking)
    ├── Output filter (NSFW image detection)
    ├── Account tier gating  
    ├── Safe mode toggle
    └── Budget / balance check
    ↓
Your output
```

**What CAN be safely stated (with source):**
- ✅ Pollinations public tier generates NSFW content without `safe=false` and requires no auth (verified by testing)
- ✅ Pollinations authenticated API returns 402 when balance is $0 — key auth alone ≠ generation capability
- ✅ Venice.ai documents `safe_mode: false` as a Pro-tier toggle in support docs
- ✅ Local ComfyUI has zero guard rails by default — but this is an implementation choice, not inherent to the model

**What CANNOT be claimed without source:**
- ❌ That `safe_mode: false` bypasses EVERYTHING universally (only that the toggle permits NSFW per policy)
- ❌ That identical weights are deployed across all providers (versions/fine-tunes differ per provider)
- ❌ That authenticating a key means generation will work (balance/budget gates still apply)
- ❌ That a model's behavior on one provider generalizes to another with the same model name

**F2 TRUTH compliance:** When describing provider behavior, attribute claims to documented sources. Use epistemic labels: `CLAIM` (assertion from source), `PLAUSIBLE` (likely but unverified), `ESTIMATE` (inferred). Never flatten "provider-side filter" into "model is uncensored."

## 💰 Pollinations Paid API (gen.pollinations.ai/v1)

Beyond the free public tier, Pollinations offers an OpenAI-compatible API at `https://gen.pollinations.ai/v1`. Requires an `sk_` secret key from enter.pollinations.ai.

```bash
# Check balance
curl "https://gen.pollinations.ai/v1/models" \
  -H "Authorization: Bearer sk_yourkey"

# Generate image (costs pollen credits)
curl -X POST "https://gen.pollinations.ai/v1/images/generations" \
  -H "Authorization: Bearer sk_yourkey" \
  -H "Content-Type: application/json" \
  -d '{"model":"flux","prompt":"...","n":1,"size":"1024x1024"}'
```

**Key facts:**
- `GET /v1/models` is free (no key needed for listing)
- Generation costs ~0.002 pollen per image
- `402 PAYMENT_REQUIRED` = key authenticated but balance exhausted
- Supports chat completions, image edits, audio transcription — full OpenAI-compatible surface
- `sk_` keys are secret — never ship to browser

## 🧭 Route

> **Canonical model-selection lives in [`minimax-cli`](../minimax-cli/SKILL.md#-image-generation--primary-for-malaysea--realism).**
> **Policy:** `/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md`

| Need | Tool |
|------|------|
| Malay/SEA phenotype, realism | **MiniMax image-01** — see [`minimax-cli` 🧬 Phenotype](../minimax-cli/SKILL.md#-phenotype) |
| Quick free draft | Pollinations.ai (free public tier) |
| Compositional/overlay visuals (text, split, silhouette) | **PIL/Pillow** — local Python, no API needed |
| Pre-generated face | Generated Photos |
| Video | MiniMax (`mmx video`) |
| NSFW API-first (paid) | **Venice.ai** — Pro sub ~$8-18/mo, OpenAI-compatible at `https://api.venice.ai/api/v1`, `safe_mode: false` + Lustify SDXL / Z-Image Turbo. No data retention. |
| NSFW local (free) | **Stable Diffusion** via ComfyUI / AUTOMATIC1111. Zero restrictions. Needs GPU. |
| NSFW web (freemium) | **SeaArt** — browser-based, free tier available |

**Full provider comparison:** `references/nsfw-providers.md`

**Selection rules:** See [`minimax-cli` 🔥 Generate](../minimax-cli/SKILL.md#-image-generation--primary-for-malaysea--realism) for full capability matrix and contrast data.

## ⚠️ Edge Cases

1. **Pollinations rate limit (disguised as image)** — Returns JSON error `{"error":"Too Many Requests","message":"Queue full for IP: ..."}` as a ~1KB file with `.jpg` extension. **Always verify output with `file` command after download.** If it says "JSON text data" or file size < 5KB, it's a rate limit error, not an image. Fix: `sleep 10 && curl ...` with `--max-time 120`. Same IP can queue ~1 request at a time.
2. **Pollinations timeout** — some prompts take 60s+. Use `--max-time 90` for first attempt, `--max-time 120` for retry.
3. **Authenticated API key balance** — authenticated POST may return HTTP 402 with `{"error":"Insufficient balance"}`. The key authenticated but has no credits left. Check balance at enter.pollinations.ai.
4. **Model name mismatch** — GET uses query param `model=flux`; POST JSON uses `"model":"flux"`. DON'T mix the two shapes.
5. **Generated Photos signature** — NEVER modify the URL path. Copy exact.
6. **Face detection bias** — free face generators have poor Malay/SEA representation. Most are white/East Asian. When generating SEA/Malay faces, the model may default to East Asian features. Prompt with specific ethnic descriptors but accept the limitation.
6. **Pollinations paid API zero balance** — `sk_` key authenticates (`GET /v1/models` works) but `POST /v1/images/generations` returns `402 PAYMENT_REQUIRED` with `"Insufficient balance"`. The key being valid doesn't mean you can generate. Check balance first, or fall back to the free public tier at `image.pollinations.ai/prompt/...` which works without auth.\n7. **Mage MCP timeout on cold start** — Mage-Flow (Modal serverless GPU) cold start can take 60-90s. Default 120s MCP timeout may be too tight. Fall back to Pollinations free tier for quick results, or retry after warm-up.
8. **Reverse image search** — AI-generated faces from these services can sometimes be detected. For catfish detection, always recommend Google reverse image search.
9. **PIL/Pillow as MCP fallback** — When all remote image gen tools fail (Mage 500, Pollinations timeout, MiniMax quota), PIL/Pillow is already installed and can produce compositional visuals. Use for: symbolic split-face compositions, gradient backgrounds, text overlay on dark canvases, silhouette art, grain textures, red-eye accents. The `image-text-editing` and `screenshot-editing` creative skills have PIL code patterns to reference.
