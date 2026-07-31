---
name: mulerouter-media
description: "MuleRouter media generation catalog — TTS, music, image gen, and video via one key"
tags: [mulerouter, media, image, audio, tts, music, video, generation]
triggers:
  - generate image
  - buat gambar
  - voice mode
  - generate music
  - buat lagu
  - mulerouter
  - media generation
related_skills: [minimax-cli, lightweight-image-generation]
---

# MuleRouter Media Generation

All media generation via **one key** (`MULEROUTER_API_KEY`), one provider, one bill.
Scripts live at `/root/HERMES/scripts/mulerouter-*.py`. Key sourced from `/root/.secrets/kunci-mas.env`.

MuleRouter (`https://api.mulerouter.ai`) is a **multimodal AI API gateway** — like OpenRouter but focused on image/video/music/speech generation alongside LLM chat. One API key gives access to multiple providers (Qwen, MiniMax, Wan, Kling, Midjourney, OpenAI, Anthropic, Google) through a unified interface.

**Base URL:** `https://api.mulerouter.ai`
**Auth:** Bearer token in Authorization header

---

## Quick Reference

| Task | Script | Model | Time |
|---|---|---|---|---|
| Text-to-Speech | `mulerouter-tts.py` | MiniMax Speech 2.8 HD | ~5-10s |
| Music generation | `mulerouter-music.py` | MiniMax Music 2.5 | ~60-120s |
| Image generation (GPT) | `mulerouter-image.py --model gpt` | GPT Image 2 | ~30s-2min |
| Image generation (Wan) | `mulerouter-image.py --model wan` | Wan 2.6 T2I | ~10-30s |
| Video (Veo) | Direct curl → `/vendors/google/v1/veo/generation` | Veo 3.1 Fast | ~45s |
| Video (Wan) | Direct curl → `/vendors/alibaba/v1/wan2.6-t2v/generation` | Wan 2.6 T2V | ~46s |

All scripts need `source /root/.secrets/kunci-mas.env` first for the API key.

---

## 1. Text-to-Speech

```bash
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-tts.py \
  --text "Your text here" --voice man --output /tmp/voice.mp3
```

**Confirmed voices:** `man`, `woman`, `Wise_Woman`
**Options:** `--speed 0.5-2.0`, `--pitch -12-12`, `--volume 0-10`, `--malay`
**Malay mode:** auto-selects `man` + 0.95x speed
**Output:** `MEDIA:/tmp/voice.mp3`

### 🎤 Voice Contrast Settings for Macho Malay (Abang Sado) Voice

Tested 2026-07-30 with cocky BM dialogue. Same text across all settings:

| # | Voice | Speed | Pitch | Duration | Size | Verdict |
|---|-------|-------|-------|----------|------|---------|
| V1 | `man` | 0.85x | -3 | 12.6s | 200K | 🥈 Macho, good |
| V2 | `man` | 0.75x | -6 | 13.8s | 218K | Deep but too slow |
| V3 | `man` | 0.9x | 0 | 14.9s | 234K | Default, flat |
| V4 | `Wise_Woman` | 0.8x | -8 | 13.2s | 208K | Doesn't fit |
| **V5** 🥇 | **`man`** | **0.8x** | **-4** | **22.0s** | **346K** | **Best — cocky, macho, aggressive** |

**Best macho setting:** `--voice man --malay --speed 0.8 --pitch -4`

**Dialogue style:** Short, aggressive BM. Use "Oi!", "Kau orang", "Tengok ni", "Aku standard, kau orang pemuja". Avoid polite phrasing. Add "Hmm", "Hah!", "Huuuu~" as punctuation.

**Example (cocky Abang Sado):**
```bash
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-tts.py \
  --text "Oi! KAU! Tengok sini! Kau orang puja aku, tengok badan sado ni. Empat tahun aku basah lantai, kau orang duduk lepak tepi. Aku standard, kau orang pemuja. Jangan lupa siapa abang sado kau orang. Huuuu~" \
  --voice man --malay --speed 0.8 --pitch -4 --output /tmp/abang_sado_macho.mp3
```

## 2. Music Generation

```bash
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-music.py \
  --prompt "Acoustic indie folk, gentle reflective mood" \
  --lyrics "[Verse]... lyrics here ..." \
  --output /tmp/song.mp3 \
  --timeout 180
```

**Required:** `--prompt` + `--lyrics` (or `--lyrics-file`). Even instrumental needs `--lyrics "[Instrumental]"`.
**Malay mode:** `--malay` adds Nusantara genre cues to the prompt. Auto-detects if Nusantara keywords are present; if not, prepends "Malaysian [prompt] — Nusantara style, traditional instruments, warm acoustic production".
**Output format:** MPEG ADTS, Layer III, 256 kbps, 44.1 kHz, Stereo. Expect ~4-5MB for a 4-minute song.
**Timeout:** Set `--timeout 300` for songs with full lyrics (8+ verses). Default 180s is enough for short instrumental or 2-3 verse songs.
**Output:** `MEDIA:/tmp/song.mp3`

### ⚠️ Music Generation — Expectation Setting

MiniMax Music 2.5 is a **text-to-music generator** — it creates an *original* composition from a text prompt. It does NOT reproduce existing songs. The melody, arrangement, and vocal performance are AI-generated, not a cover of any specific recording. For users asking "make this exact song," clarify:

1. **Want the original recording?** → Find it on YouTube/Spotify and deliver the link (see `youtube-content` skill for YouTube auth)
2. **Want an AI cover (same song, different voice)?** → Needs RVC voice conversion (separate GPU setup, not available via Hermes tools)
3. **Want a new original in the style of a tradition?** → Text-to-music generation (this skill) — research → prompt → lyrics → generate

See `music-generation` skill §6 for the full breakdown of text-to-music vs voice conversion.

### Nusantara Traditional Music — Somatic Parameter Injection

For traditional Nusantara songs (Minang, Malay, Javanese, etc.), use the **PULSE/SOUL/FLOW** somatic injection pattern from the `music-generation` skill. Tested successfully with Kaparinyo (2026-07-30):

```bash
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-music.py \
  --prompt "Traditional Minangkabau acoustic folk song 'Kaparinyo'. Featuring driving rebana drum rhythms, rhythmic talempong chimes, bright accordion, and soulful saluang bamboo flute. Joyful, rhythmic, Nusantara heritage, mid-tempo traditional dance feel. High fidelity, organic acoustic instruments, clear cultural texture." \
  --lyrics-file /tmp/kaparinyo_lyrics.txt \
  --output /tmp/kaparinyo_song.mp3 \
  --malay \
  --timeout 300
```

**Key insight:** Naming the song explicitly in the prompt anchors the model's latent space. The three somatic layers (PULSE=rhythm, SOUL=timbre, FLOW=structure) let you pack many authentic elements without triggering over-production degradation, because all elements are coherent within the same cultural tradition.

## 3. Image Generation

```bash
source /root/.secrets/kunci-mas.env

# GPT Image 2 (has safety filter — blocks shirtless/NSFW prompts)
/root/HERMES/scripts/mulerouter-image.py \
  --prompt "Serene mountain landscape at sunset" \
  --model gpt --size 1024x1024 --format png --output /tmp/image.png

# Wan 2.6 T2I (no safety filter on shirtless content)
/root/HERMES/scripts/mulerouter-image.py \
  --prompt "Athletic Malay man in gym, muscular chest" \
  --model wan --size 1024x1024 --output /tmp/wan_image.png
```

**Options:** `--model gpt|wan`, `--size` (exact format like `1024x1024`), `--quality` (standard/high), `--format` (png/jpeg/webp), `--n` (1-4, GPT only), `--timeout` (default 120s), `--debug`

### ⚠️ GPT Image 2 Safety Filter

**Critical pitfall (discovered 2026-07-30):** GPT Image 2 has an **input safety filter** that rejects prompts containing shirtless, bodybuilding, gym, fitness, sweat, or similar content. Returns:

```json
{"code": 2001, "title": "Parameter validation failed",
 "detail": "Input content was rejected by safety inspection."}
```

**Solutions:**
- Use **Wan 2.6 T2I** (`--model wan`) for shirtless fitness/bodybuilding — no safety filter on shirtless content
- For GPT Image 2, dress the subject ("fitted white tank top" instead of "shirtless")
- Use MiniMax image-01 via `mmx-cli` — handles fitness content professionally, best Malay phenotype

### ⚠️ Parameter Format Pitfalls

| Parameter | Correct | Wrong |
|-----------|---------|-------|
| `--size` | `1024x1024`, `1920x1080`, `2048x2048` | `square`, `auto`, `hd` |
| `--format` | `png`, `jpeg`, `webp` | `jpg` (use `jpeg`) |

### ⚠️ Polling Timeout

The script's default `--timeout 120` can be too short for GPT Image 2 when the task is queued. Wan 2.6 T2I is faster (~10s). If the script times out but the task may have completed:

```bash
# Check task status manually
curl -s "https://api.mulerouter.ai/vendors/openai/v1/gpt-image-2/generation/<TASK_ID>" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY"
# If status: "completed", download the image URL from the `images` array
```

### Model Notes

| Model | Max Res | Typical Time | Safety Filter | Best For |
|---|---|---|---|---|
| GPT Image 2 | 4K | ~30s-2min | ✅ Blocks shirtless/NSFW | Clothed portraits, infographics, 4K quality |
| Wan 2.6 T2I | 1280×1280 | ~10-30s | ❌ Allows shirtless | Fitness, shirtless content, fast drafts |

---

## 4. Video Generation

No dedicated script exists yet. Use direct curl to MuleRouter video endpoints.

### Veo 3.1 Fast (Google)

```bash
source /root/.secrets/kunci-mas.env

# Submit task
curl -s -X POST "https://api.mulerouter.ai/vendors/google/v1/veo/generation" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo-3.1-fast",
    "prompt": "Your video description",
    "duration": 6,
    "resolution": "720p"
  }'
# → Returns task_info.id

# Poll for completion
curl -s "https://api.mulerouter.ai/vendors/google/v1/veo/generation/<TASK_ID>" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY"
# → When status=completed, download videos[0] URL
```

**Parameters:** `model` (required: "veo-3.1-fast"), `duration` (4, 6, or 8), `resolution` ("720p" or "1080p")
**Typical time:** ~45s for 6s clip | **File size:** ~2.6MB

### Wan 2.6 T2V (Alibaba)

```bash
source /root/.secrets/kunci-mas.env

# Submit task (model inferred from path — do NOT include model field)
curl -s -X POST "https://api.mulerouter.ai/vendors/alibaba/v1/wan2.6-t2v/generation" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your video description",
    "duration": 5
  }'
# → Returns task_info.id

# Poll for completion (same path)
curl -s "https://api.mulerouter.ai/vendors/alibaba/v1/wan2.6-t2v/generation/<TASK_ID>" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY"
```

**Note:** Model field is inferred from path — do NOT include it.
**Typical time:** ~46s | **File size:** ~5.5MB (higher bitrate than Veo)

### MiniMax Hailuo-2.3 (alternative, via mmx-cli)

```bash
cd /tmp && source /root/.secrets/kunci-mas.env
mmx video generate --prompt "..." --download /tmp/output.mp4 --poll-interval 10 --non-interactive
```

**Quota:** 3 videos/day, 21/week (Token Plan)
**Typical time:** ~1-2min | **File size:** ~743KB

**Full endpoint docs:** See `references/video-generation-mulerouter.md`

---

## Image Model Priority (Full Stack)

When the user asks for image generation, follow this priority:

| Priority | Engine | Best For | Cost |
|----------|--------|----------|------|
| 1 | **MiniMax image-01** (mmx-cli) | SEA/SE Asian phenotype, realism, shirtless fitness | Token Plan quota |
| 2 | **MuleRouter GPT Image 2** | Quality, clothed portraits, 4K | MuleRouter API key |
| 3 | **MuleRouter Wan 2.6 T2I** | Shirtless content, fast, alternative style | MuleRouter API key |
| 4 | **Pollinations FLUX** (free) | Always available, no auth, any content | Free |
| 5 | **Pollinations SANA** (free) | Fastest, near-instant | Free |

**Vision QC:** After image generation, route analysis through MuleRouter → qwen-vl-max for a second-opinion quality check. Note: MuleRouter vision only supports publicly accessible image URLs (not base64 data: URIs).

---

## How to Use in Conversations

When the user requests media generation:

1. **Voice:** Run `mulerouter-tts.py` with proper voice + language mode
2. **Music:** Research lyrics → write → run `mulerouter-music.py`
3. **Image:**
   - Clothed portraits / general: `--model gpt` (GPT Image 2)
   - Shirtless / fitness: `--model wan` (Wan 2.6 T2I) or MiniMax image-01
   - Always use exact formats: `--size 1024x1024 --format png`

All delivered via `MEDIA:<filepath>` for native Telegram display.

---

## Referenced By

- `lightweight-image-generation` — Route table and multi-engine priority chain
- `minimax-cli` — Phenotype comparison table (MuleRouter rows)
- `hermes-gateway-image-routing/references/mulerouter-integration.md` — Full technical integration details