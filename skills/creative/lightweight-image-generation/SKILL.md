---
name: lightweight-image-generation
description: "Generate images without heavy local installs — free APIs (Pollinations.ai), pre-generated galleries (Generated Photos), and quick alternatives"
version: 2.3.0
tags: [image-generation, free-api, pollinations, ai-faces, lightweight, fallback, malay-phenotype, nsfw, venice]
metadata:
  hermes:
    category: creative
    related_skills: [comfyui, minimax-cli, token-plan-image, mulerouter-media]
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
- **Vision QC can fail** — `vision_analyze()` may return 404 model errors if the active model doesn't support vision natively or the vision endpoint is degraded. Fall back to `mmx vision describe` (MiniMax Token Plan, separate credit pool) or describe the image manually based on known metadata (file size, resolution, model used).
- **Key types:** `sk_...` = secret key (server only). `pk_...` = publishable key (safe for browsers). Get keys at enter.pollinations.ai.
- **Model selection on free tier** — The free GET endpoint at `image.pollinations.ai` defaults to FLUX. To use a different free model, add `&model=sana` (NVIDIA SANA Sprint 1.6B, near-instant). Verified 2026-07-30: `model=sana` works on the free GET endpoint without auth.

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
> **Image model priority:** MiniMax image-01 → MuleRouter GPT Image 2 / Wan 2.6 T2I → Pollinations FLUX → Pollinations SANA

| Need | Tool |
|------|------|
| Malay/SEA phenotype, realism | **MiniMax image-01** — see [`minimax-cli` 🧬 Phenotype](../minimax-cli/SKILL.md#-phenotype) |
| Quick free draft | Pollinations.ai (free public tier) |
| Compositional/overlay visuals (text, split, silhouette) | **PIL/Pillow** — local Python, no API needed |
| Pre-generated face | Generated Photos |
| Video | MiniMax (`mmx video`) or MuleRouter (Veo/Wan T2V via curl) | See `mulerouter-media` skill `references/video-generation-mulerouter.md` |
| NSFW API-first (paid) | **Venice.ai** — Pro sub ~$8-18/mo, OpenAI-compatible at `https://api.venice.ai/api/v1`, `safe_mode: false` + Lustify SDXL / Z-Image Turbo. No data retention. |
| NSFW local (free) | **Stable Diffusion** via ComfyUI / AUTOMATIC1111. Zero restrictions. Needs GPU. |
| NSFW web (freemium) | **SeaArt** — browser-based, free tier available |

**Full provider comparison:** `references/nsfw-providers.md`

**Selection rules:** See [`minimax-cli` 🔥 Generate](../minimax-cli/SKILL.md#-image-generation--primary-for-malaysea--realism) for full capability matrix and contrast data.

### 🧩 MuleRouter — Multimodal Gateway (Image + TTS + Music + Video + LLM)

**MuleRouter** (`https://api.mulerouter.ai`) is a **multimodal AI API gateway** — not just text LLM routing. It hosts image generation (GPT Image 2, Wan 2.6 T2I), TTS (MiniMax Speech 2.8 HD), music (MiniMax Music 2.5), video, AND text LLM chat. Think of it as OpenRouter but focused on media generation alongside LLM.

**Image generation via MuleRouter:**

| Model | Endpoint | Status |
|-------|----------|--------|
| **GPT Image 2** | `/vendors/openai/v1/gpt-image-2/generation` | ✅ Tested 2026-07-30 |
| **Wan 2.6 T2I** | `/vendors/alibaba/v1/wan2.6-t2i/generation` | ✅ Script ready |
| **Veo 3.1 Fast** | `/vendors/google/v1/veo/generation` | ✅ Tested 2026-07-30 |
| **Wan 2.6 T2V** | `/vendors/alibaba/v1/wan2.6-t2v/generation` | ✅ Tested 2026-07-30 |

**Script:** `/root/HERMES/scripts/mulerouter-image.py` (196 lines, functional)

**Usage:**
```bash
source /root/.secrets/kunci-mas.env
python3 /root/HERMES/scripts/mulerouter-image.py \
  --prompt "your prompt" \
  --model gpt \
  --size "1024x1024" \
  --format png \
  --output /tmp/mr_output.png \
  --timeout 120
```

**Pitfall:** `--size` expects exact format like `1024x1024` (not `square`). `--format` expects `png`, `jpeg`, or `webp` (not `jpg`).

**Where MuleRouter fits in the image model order:**

| Priority | Engine | Best For | Cost |
|----------|--------|----------|------|
| 1 | **MiniMax image-01** | SEA/SE Asian phenotype, realism | Token Plan quota |
| 2 | **MuleRouter GPT Image 2** | Fast, high quality, OpenAI-compatible | MuleRouter API key |
| 3 | **MuleRouter Wan 2.6 T2I** | Alibaba's Wan model via MuleRouter | MuleRouter API key |
| 4 | **Pollinations FLUX** (free) | Always available, no auth | Free |
| 5 | **Pollinations SANA** (free) | Fastest, near-instant | Free |

**Vision QC via MuleRouter:** After generating an image, route the analysis through MuleRouter → qwen-vl-max for a second-opinion quality check. This is a valid use of MuleRouter in the image pipeline — separate from pixel generation.

## 🚀 Multi-Engine Parallel Fallback

When generating images, **fire available engines in parallel** rather than serial fallback. Parallel execution is faster and lets you compare quality across engines in one pass.

### The Pattern

```
1. Fire all available engines simultaneously (parallel terminal calls)
2. Collect results as they arrive
3. Run vision_analyze() on each to evaluate quality
4. Present the best result(s) to the user
```

### Engine Priority & Characteristics

| Priority | Engine | Best For | Output Location | Failure Mode |
|----------|--------|----------|----------------|--------------|
| 1 | **Mage-Flow** (Modal GPU) | Highest quality, 4-step turbo | MCP returns path | 500 error, cold start 60-90s |
| 2 | **MiniMax image-01** | **SEA/SE Asian phenotype, realism** | Auto-saves to cwd as `image_XXX.jpg` | API quota, rate limit |
| 3 | **MuleRouter GPT Image 2** | Quality, clothed portraits, 4K | Async task → download URL | Safety filter (blocks shirtless), timeout |
| 4 | **MuleRouter Wan 2.6 T2I** | Shirtless/fitness, fast, alternative | Async task → download URL | Timeout (less common) |
| 5 | **Qwen Token Plan** (qwen-image-2.0-pro) | Text+image edit, generic | Signed URL → download | InvalidApiKey (expired key), quota exhausted |
| 6 | **Pollinations FLUX** (free tier) | Always available, no auth | Download via curl | Rate limit (JSON disguised as JPEG) |
| 7 | **Pollinations SANA** (free tier) | Fastest, near-instant draft | Download via curl | Rate limit |

### Parallel Execution Example

```bash
# Fire MiniMax + Pollinations in parallel
mmx image generate --prompt "..." --size 1024x1024 --output json &
curl -sL --max-time 90 "https://image.pollinations.ai/prompt/...?width=1024&height=1024&nologo=true&enhance=true&seed=42" -o /tmp/polli.jpg &
wait

# Verify each output
file /tmp/polli.jpg
file ./image_001.jpg

# Compare quality
vision_analyze(image_url="/tmp/polli.jpg", question="Describe quality and subject")
vision_analyze(image_url="./image_001.jpg", question="Describe quality and subject")
```

### Key Practices

- **Do NOT sequence engines one-by-one** — fire parallel, collect results, pick best
- **Always verify with `file`** after each download — Pollinations rate-limit returns JSON disguised as JPEG
- **vision_analyze feedback loop** — after generation, evaluate aesthetic match before presenting. Query: "Describe the image quality, the subject, lighting, and composition in detail."
- **Prompt length matters** — very long prompts (>200 chars) on Pollinations free tier increase timeout risk. Use `--max-time 90` minimum. Shorter prompts respond faster.
- **MiniMax saves to cwd** — output lands in current directory as `image_001.jpg`, `image_002.jpg`, etc. No `-o` flag needed.
- **Qwen key expiry** — returns HTTP 200 with `code: "InvalidApiKey"` (not 401). Check `$QWEN_API_KEY` is set and valid before calling. Rotate at dashscope.aliyuncs.com.

### When All Engines Fail

PIL/Pillow is always installed and can produce compositional visuals: gradient backgrounds, text overlay, split compositions, silhouette art. See `image-text-editing` and `screenshot-editing` skills for code patterns.

## 📊 Multi-Model Comparison Methodology

When the user asks you to test ALL available image generation routes (or you need to pick the best engine for a specific prompt), use this systematic comparison workflow:

### Step 1: Inventory Available Engines

Check which engines are reachable before generating:

| Engine | Check Command | Expected Signal |
|--------|---------------|-----------------|
| Mage-Flow | `mage_health()` | `status: "healthy"` or `"degraded"` |
| MiniMax | `mmx auth status` | `method: "api-key"` |
| MuleRouter GPT/Wan | `source /root/.secrets/kunci-mas.env && echo $MULEROUTER_API_KEY` | Non-empty key |
| Pollinations FLUX | `curl` to free endpoint | HTTP 200, JPEG response |
| Pollinations SANA | `curl` with `model=sana` | HTTP 200, JPEG response |
| Qwen Token Plan | env var `$QWEN_API_KEY` | Non-empty, not expired |

### Step 2: Generate Same Prompt Across All Engines

Use a **consistent prompt** across all engines. Save each result with a distinct filename:

```bash
# MiniMax
mmx image generate --prompt "YOUR PROMPT" --aspect-ratio 1:1 --non-interactive
cp image_001.jpg /tmp/comparison_minimax.jpg

# MuleRouter GPT Image 2
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-image.py --prompt "YOUR PROMPT" --model gpt --size 1024x1024 --format png --output /tmp/comparison_mr_gpt.png --timeout 180

# MuleRouter Wan 2.6 T2I
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-image.py --prompt "YOUR PROMPT" --model wan --size 1024x1024 --output /tmp/comparison_mr_wan.png --timeout 120

# Pollinations FLUX
curl -sL --max-time 90 "https://image.pollinations.ai/prompt/YOUR_PROMPT%20ENCODED?width=1024&height=1024&nologo=true&enhance=true&seed=42" -o /tmp/comparison_flux.jpg

# Pollinations SANA
curl -sL --max-time 90 "https://image.pollinations.ai/prompt/YOUR_PROMPT%20ENCODED?width=1024&height=1024&nologo=true&enhance=true&model=sana&seed=123" -o /tmp/comparison_sana.jpg

# Verify ALL are real images
file /tmp/comparison_*.jpg /tmp/comparison_*.png
```

### Step 3: Run Vision Analysis on Each

```bash
vision_analyze(image_url="/tmp/comparison_minimax.jpg", question="Describe quality, subject, lighting, composition, realism, phenotype accuracy.")
vision_analyze(image_url="/tmp/comparison_flux.jpg", question="Same.")
vision_analyze(image_url="/tmp/comparison_sana.jpg", question="Same.")
```

**Pitfall:** `vision_analyze()` may fail with 404 on some providers. Have fallback ready: `mmx vision describe --file /tmp/comparison_minimax.jpg --non-interactive` (MiniMax Token Plan) or manual quality assessment based on file size, resolution, and known model characteristics. MuleRouter vision (qwen-vl-max) is another option for public URLs.

### Step 4: Build Comparison Table

Compare across these dimensions:

| Dimension | Engine A | Engine B | Engine C |
|-----------|:--------:|:--------:|:--------:|
| Resolution | 1024×1024 | 768×768 | 768×768 |
| File size | 200KB | 63KB | 67KB |
| Phenotype accuracy | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Realism | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Lighting | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Cost | Quota | Free | Free |
| Gen time | ~15s | ~4s | ~3s |

### Step 5: Present Ranked Results

Deliver all images to the user with a clear ranking. MiniMax almost always wins for people/portraits, Pollinations for fast free drafts.

### Step 6: Save Comparison Data

If the comparison reveals non-trivial quality differences worth preserving, add a reference file at `references/<topic>-comparison-<date>.md` under this skill.

## ⚠️ Edge Cases

1. **Pollinations rate limit (disguised as image)** — Returns JSON error `{"error":"Too Many Requests","message":"Queue full for IP: ..."}` as a ~1KB file with `.jpg` extension. **Always verify output with `file` command after download.** If it says "JSON text data" or file size < 5KB, it's a rate limit error, not an image. Fix: `sleep 10 && curl ...` with `--max-time 120`. Same IP can queue ~1 request at a time.
2. **Pollinations timeout** — some prompts take 60s+. Use `--max-time 90` for first attempt, `--max-time 120` for retry.
3. **Authenticated API key balance** — authenticated POST may return HTTP 402 with `{"error":"Insufficient balance"}`. The key authenticated but has no credits left. Check balance at enter.pollinations.ai.
4. **Model name mismatch** — GET uses query param `model=flux`; POST JSON uses `"model":"flux"`. DON'T mix the two shapes.
5. **Generated Photos signature** — NEVER modify the URL path. Copy exact.
6. **Face detection bias** — free face generators have poor Malay/SEA representation. Most are white/East Asian. When generating SEA/Malay faces, the model may default to East Asian features. Prompt with specific ethnic descriptors but accept the limitation.
6. **Pollinations paid API zero balance** — `sk_` key authenticates (`GET /v1/models` works) but `POST /v1/images/generations` returns `402 PAYMENT_REQUIRED` with `"Insufficient balance"`. The key being valid doesn't mean you can generate. Check balance first, or fall back to the free public tier at `image.pollinations.ai/prompt/...` which works without auth.\n7. **Mage MCP timeout on cold start** — Mage-Flow (Modal serverless GPU) cold start can take 60-90s. Default 120s MCP timeout may be too tight. Fall back to Pollinations free tier for quick results, or retry after warm-up.
8. **Reverse image search** — AI-generated faces from these services can sometimes be detected. For catfish detection, always recommend Google reverse image search.
9. **PIL/Pillow as MCP fallback** — When all remote image gen tools fail (Mage 500, Pollinations timeout, MiniMax quota, MuleRouter timeout), PIL/Pillow is already installed and can produce compositional visuals. Use for: symbolic split-face compositions, gradient backgrounds, text overlay on dark canvases, silhouette art, grain textures, red-eye accents. The `image-text-editing` and `screenshot-editing` creative skills have PIL code patterns to reference.
10. **MuleRouter GPT Image 2 safety filter** — Blocks shirtless/bodybuilding prompts. Use Wan 2.6 T2I (--model wan) or MiniMax image-01 instead. See `mulerouter-media` skill reference `gpt-image-2-safety-filter.md`.
11. **MuleRouter parameter format** — --size expects exact format like 1024x1024 (not square). --format expects png, jpeg, or webp (not jpg).
12. **MuleRouter polling timeout** — GPT Image 2 tasks can take 2+ minutes. Default --timeout 120 may be too short. Use --timeout 180 or check task status manually.
