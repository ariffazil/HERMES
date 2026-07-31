---
name: minimax-cli
description: "MiniMax multimodal via mmx-cli — TTS, video, music, image, vision, search. Image generation is PRIMARY choice for Malay/SEA phenotype and"
version: 2.5.0
tags: [minimax, tts, video, music, image, vision, multimodal, malay-phenotype, image-generation, logo-design]
metadata:
  hermes:
    category: creative
    requires: [mmx-cli]
    related_skills: [token-plan-image, lightweight-image-generation, mulerouter-media]
---

# MiniMax CLI (mmx-cli)

MiniMax multimodal capabilities via `mmx` CLI. Token Plan subscription required.

## Prerequisites

- `npm install -g mmx-cli`
- `mmx auth login --api-key <sk-cp-key>`
- Region auto-detected from key (global/cn)

## Commands

| Capability | Command | Example |
|---|---|---|
| Text chat | `mmx text chat --message "..."` | `mmx text chat --message "Explain NPV"` |
| TTS | `mmx speech synthesize --text "..." --out voice.mp3` | `mmx speech synthesize --text "Hello" --out hi.mp3` |
| Image gen | `mmx image generate --prompt "..."` | `mmx image generate --prompt "sunset ocean" --aspect-ratio 16:9` |
| Video gen | `mmx video generate --prompt "..."` | `mmx video generate --prompt "cat at sunset"` |
| Music gen | `mmx music generate --prompt "..."` | `mmx music generate --prompt "jazz summer" --out jazz.mp3` |
| Music gen (lyrics) | `mmx music generate --prompt-file tags.txt --lyrics-file lyrics.txt --out song.mp3` | See Music Generation Workflow below |
| Vision | `mmx vision describe --file image.png` | `mmx vision describe --file photo.jpg` |
| Web search | `mmx search query --query "..."` | `mmx search query --query "oil price today"` |
| Quota | `mmx quota` | Check remaining Token Plan balance |
| Auth status | `mmx auth status` | Verify login + region |

## Global flags

- `--api-key <key>` — override auth
- `--region global|cn` — force region
- `--output json|text` — output format
- `--timeout <seconds>` — request timeout (default 300)
- `--non-interactive` — CI/agent mode (no prompts)

## Output

Files saved to `minimax-output/` in cwd. When using from Hermes, display media directly in output.

## Quota

- Monthly Max: ~5.1B M3 tokens, 3 video/day, 21 video/week
- General models + video + speech + music + image share one quota bar
- 5-hour rolling window + weekly window
- TTS free for limited time (doesn't consume quota)

---

## 🔥 Image Generation — PRIMARY for Malay/SEA + Realism

> **Verdict:** MiniMax image-01 is the DEFAULT for federation image generation. MuleRouter GPT Image 2 / Wan 2.6 T2I for secondary. Pollinations only for free prototyping.  
> **Full image model priority:** MiniMax image-01 → MuleRouter GPT Image 2 → MuleRouter Wan 2.6 T2I → Pollinations FLUX → Pollinations SANA

### Basic Usage

```bash
mmx image generate --prompt "your prompt" --aspect-ratio 1:1 --non-interactive
```

**Aspect ratios:** `1:1` (default), `16:9`, `9:16`, `4:3`, `3:4`

**Critical pitfall:** `--output` flag is **IGNORED** by `mmx image generate`. Every call saves to `image_001.jpg` in the **current working directory** (not `minimax-output/`). A second call **overwrites** `image_001.jpg` — it does NOT auto-increment to `image_002.jpg`. The CLI warns `overwriting existing file: image_001.jpg` on collision.

**Workflow for multiple generations:**
```bash
mmx image generate --prompt "..." --aspect-ratio 1:1 --non-interactive
cp image_001.jpg /tmp/logo_v1.jpg   # save BEFORE next generation

mmx image generate --prompt "..." --aspect-ratio 1:1 --non-interactive
cp image_001.jpg /tmp/logo_v2.jpg   # now safe
```

Proven 2026-07-20, overwrite behavior confirmed 2026-07-23.

### 🧬 Phenotype

MiniMax image-01 has the strongest SEA/Malay phenotype reading of all available models. When generating images of people:

| Model | SEA Phenotype | Realism | Use Case |
|-------|--------------|---------|----------|
| **MiniMax image-01** | ⭐⭐⭐ Strong | ⭐⭐⭐ Studio-grade | Malay/SEA prompts, realism-critical |
| **MuleRouter GPT Image 2** | ⭐⭐ Moderate | ⭐⭐⭐ High | Fast, high quality, OpenAI-compatible |
| **MuleRouter Wan 2.6 T2I** | ⭐⭐ Moderate | ⭐⭐ Good | Alibaba's Wan model via MuleRouter |
| Qwen image-2.0 | ⭐⭐ Moderate | ⭐⭐ Good | Generic, non-phenotype |
| Pollinations FLUX | ⭐ Weak | ⭐⭐ Decent | Free drafts only |
| Pollinations SANA | ⭐⭐ Moderate | ⭐⭐ Good | Fastest free option, near-instant |

**Prompt decomposition for Malay slang:**

| Slang | Explicit decomposition |
|-------|----------------------|
| `abang sado` | male, Southeast Asian Malay, muscular build, shirtless, fitness, gym or studio |
| `Melayu` | Southeast Asian Malay ethnicity, natural skin texture, dark hair, brown eyes |
| `amoi` | female, Southeast Asian Chinese/Malay phenotype, young adult |
| `mat rempit` | male, Malay, young, motorcycle, street, urban Malaysia |

**Rule:** Never rely on the model inferring ethnicity from slang alone. Always add explicit "Southeast Asian Malay" or equivalent phenotype tokens.

### 🛡️ Safety

When prompt contains `shirtless`, `abang sado`, `bodybuilding`, `gym`, `fitness`:

- **Default context:** gym, studio, outdoor fitness — NOT bedroom, private, intimate
- **Pose:** physique display, athletic, flexing — NOT sexualized, suggestive
- **Framing:** full body or torso, fitness lighting — NOT cropped, intimate angles
- **Add explicit context:** "in a gym", "studio lighting", "fitness photography"

Both MiniMax and Pollinations enforce NSFW filters. MiniMax provides cleaner, more professional fitness-aesthetic results.

### 🎨 Logo & Branding Generation

MiniMax image-01 is the primary tool for bot/agent profile logos. The model is strong at cyberpunk/sci-fi aesthetic but needs precise genre anchoring.

**Workflow: iterative refinement**

```bash
# 1. Generate initial version
mmx image generate --prompt "..." --aspect-ratio 1:1 --non-interactive
cp image_001.jpg /tmp/logo_v1.jpg

# 2. Vision-analyze (use vision_analyze tool or mmx vision describe)
#    Check: clear letter shape? correct aesthetic? thumbnail-suitable?

# 3. Refine prompt based on feedback
mmx image generate --prompt "..." --aspect-ratio 1:1 --non-interactive
cp image_001.jpg /tmp/logo_v2.jpg

# 4. Verify v2 → upload if approved
```

**Pitfall: genre drift without explicit aesthetic anchors**

The model can interpret "forged metal" as dark fantasy/volcanic instead of cyberpunk. Always anchor the aesthetic explicitly:

| Weak prompt | Strong prompt |
|---|---|
| `forged metal A logo, dark background` | `cyberpunk forged metal A logo, neon cyan and magenta edge lighting, circuit traces, dark void background` |
| `industrial forge logo` | `cyberpunk industrial forge logo, neon circuit traces, holographic edge glow, not dark fantasy, not volcanic` |

**Proven 2026-07-24:** Forge logo v1 was dark fantasy volcanic — beautiful but wrong genre. v2 with explicit "cyberpunk, neon, circuit traces" passed. Hermes logo v1 had Omega symbol — v2 removed it and added "neural network crown" at apex.

**Prompt structure for cyberpunk logos:**
1. **Subject**: bold letter A, centered, forged metal texture
2. **Aesthetic**: cyberpunk, neon edge lighting, circuit board engravings
3. **Colors**: specify dual-tone (e.g., crimson red + electric blue, cyan + magenta)
4. **Distinctive element**: neural crown, claw blades, molten core — one unique feature
5. **Background**: dark void, no text, no extra symbols
6. **Format**: 1:1 square, thumbnail-suitable, strong silhouette

**Profile photo upload workflow:**
```python
import requests, json
with open("/tmp/logo_v2.jpg", "rb") as photo:
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/setMyProfilePhoto",
        data={"photo": json.dumps({"type": "static", "photo": "attach://myfile"})},
        files={"myfile": ("logo.jpg", photo, "image/jpeg")}, timeout=15
    )
```

### ⚖️ Contrast

Same prompt `shirtless abang sado, Malay, realistic, studio lighting`:

| Dimension | MiniMax image-01 | Pollinations FLUX | Pollinations SANA |
|-----------|-----------------|-------------------|-------------------|
| Resolution | 1024×1024 ✅ | 768×768 | 768×768 |
| File size | 200KB ✅ | 63KB | 67KB |
| Malay phenotype | Strong SEA reading ✅ | Ambiguous/Westernized | Moderate, tanned |
| Realism | Studio-grade, natural ✅ | AI-exaggerated, plastic | High, scar detail |
| Prompt understanding | "Abang sado" nailed ✅ | Generic buff guy | Good chest focus |
| Cost | Token Plan quota | Free | Free |
| Gen speed | ~15s | ~4s | **~3s** ✅ |

**Verdict:** MiniMax wins clean. For any prompt where Malay/SEA phenotype or realism matters, MiniMax is mandatory. SANA is a credible free alternative for speed-critical drafts. Full comparison data at `../lightweight-image-generation/references/multi-model-comparison-2026-07-30.md`.

---

## 🎤 Speech

When Arif requests voice messages (TTS), use this fallback order:

1. **Built-in `text_to_speech` tool** — uses OpenAI by default, fast, good quality. Fails on quota (429).
2. **`edge-tts` CLI** — free, no API key, good Malay voice. Install: `pip install edge-tts --break-system-packages`
   ```bash
   # Malay male voice
   edge-tts --text "your text" --voice ms-MY-OsmanNeural --write-media /tmp/tts_output.mp3
   # Malay female voice
   edge-tts --text "your text" --voice ms-MY-YasminNeural --write-media /tmp/tts_output.mp3
   ```
   Send with `MEDIA:/tmp/tts_output.mp3` in response.
3. **`mmx speech synthesize`** — MiniMax TTS, quota-based but high quality.

**When user says "voice" or "TTS":** try built-in first → if 429 → fall back to edge-tts immediately (no need to ask).

### 🗣️ BM Voice Note Responses ("jawab dalam voice note")

When Arif explicitly says "jawab dalam voice note" or the response is clearly for a voice message to another person:

1. **Go directly to edge-tts** — skip built-in text_to_speech. Malay quality is the priority, not speed.
2. **Voice:** `ms-MY-OsmanNeural` (male, BM casual). This is Arif's preferred voice for himself.
3. **Text style for voice notes:**
   - Concise BM casual — 30-60 seconds spoken (roughly 100-200 words)
   - No markdown formatting (it's spoken, not read)
   - Conversational tone, direct address to the listener
   - Short sentences — easier to follow when spoken
   - No parentheticals, no citations, no table structures — pure speech flow
4. **Verify before sending:** always `ls -lh` and `file` to confirm the MP3 is valid
5. **Send with:** `MEDIA:/tmp/<filename>.mp3`

**Pitfall:** Don't try to speak markdown tables, code blocks, or formatted structures in a voice note. Rewrite as conversational explanation.

## 🎵 Music

Full song generation from lyrics + genre tags. Two input files required:

**1. Tags file** (`tags.txt`) — comma-separated genre, mood, instrument tags, no spaces after commas:
```
traditional malay folk,acoustic guitar,gamelan,kompang,joyful,warm,nostalgic,female vocal
```

**2. Lyrics file** (`lyrics.txt`) — bracketed structural tags:
```
[Intro]

[Verse]
Your lyrics here...

[Chorus]
Chorus lyrics...

[Bridge]
Bridge lyrics...

[Outro]
```

**3. Generate:**
```bash
mmx music generate \
  --prompt-file tags.txt \
  --lyrics-file lyrics.txt \
  --out song.mp3 \
  --non-interactive
```

**Output:** MP3, auto-selects model (music-2.6 as of 2026-07). ~4.2MB for a ~3min song, 256kbps stereo 44.1kHz.

**Quick prompt-only (no lyrics):**
```bash
mmx music generate --prompt "jazz piano,relaxing,lo-fi" --out lofi.mp3
```

**Workflow for Telegram delivery:**
1. Write tags to `/tmp/song_tags.txt`
2. Write lyrics to `/tmp/song_lyrics.txt`
3. Run `mmx music generate` with `--out /tmp/song.mp3`
4. Verify with `ls -lh /tmp/song.mp3 && file /tmp/song.mp3`
5. Send with `MEDIA:/tmp/song.mp3` in response

**Auth key:** `source /root/.secrets/vault.env` → `MINIMAX_API_KEY` (sk-cp- prefix, Token Plan).

### Cultural/Traditional Song Research Protocol

When user requests a song in a specific cultural/traditional style (e.g., "Kaparinyo", "dondang sayang", "keroncong"):

1. **Research BEFORE generating.** Search for the song's actual origins, regional variant, and musical characteristics. Many folk songs have regional variants with different lyrics and instrumentation.
2. **Use authentic lyrics** — not generic placeholder lyrics. Search for the actual traditional text (often in regional language, not standard Malay/Indonesian).
3. **Match instrumentation to tradition** — e.g., Kaparinyo is Gamad style (violin, accordion, Portuguese guitar, gandang drums), not gamelan.
4. **Distinguish similar songs** — "Kaparinyo" (Minangkabau/Gamad from West Sumatra) ≠ "Burung Kakak Tua" (Ambon/Moluccas). Research prevents conflation.

### Audio Evaluation

Two tools for evaluating generated music:

- **`scripts/akal_somatic_scoring.py`** — ffmpeg-only audio scoring. Three checks: PULSE (temporal fidelity), SOUL (cultural alignment), FLOW (entropy equilibrium). No librosa needed. Returns JSON verdict (SEAL/SABAR/HOLD).
- **`templates/cultural_manifold.json`** — Reusable schema for culturally-grounded music generation. Defines identity, structural priors, harmonic constraints, timbre palette, lyric constraints, and evaluation thresholds. Copy and modify for other traditions (Zapin, Asli, Dondang Sayang, etc.).

### Music Evaluation Pipeline

Full evaluation toolkit at `/root/music-eval/` — genre scoring, somatic analysis, paradox engine, motif memory, Telegram signal observer. See `references/music-eval-pipeline.md` for architecture, CLI usage, and A-FORGE integration path. A-FORGE already has `paradox-engine/models.py` with 16-dim somatic vectors — see `references/aforge-paradox-engine.md`.

### Related References

- `references/hermes-telegram-image-routing.md` — Full decision trace for Telegram image routing: 3 pathways compared, config pitfalls, code locations, A2A EMD gate limitation**
- `references/jina-reader-medium.md` — Reading Medium/Cloudflare-protected articles via Jina Reader
- `references/cross-organ-wiring-pattern.md` — Wiring external engines into arifOS kernel (enforcement gates)

## 👁️ Vision

### Basic Usage

```bash
# Auth (once per session — key is in kunci-mas.env)
source /root/.secrets/kunci-mas.env  # or vault.env
mmx auth login --api-key "$MINIMAX_API_KEY" --non-interactive

# Analyze any image
mmx vision describe --file /path/to/image.jpg --non-interactive 2>&1
```

**What it can read from a trading chart:**
- Price levels (current, high, low, order levels)
- Chart pattern (downtrend, consolidation, flag, pennant)
- Timeframe (H1, H4 visible from the chart header)
- Support/resistance zones
- Pending orders (buy/sell limits, stop losses)

### Hermes Image Pipeline Integration

MiniMax vision is the **preferred vision provider** when the Hermes gateway receives an image via Telegram but the primary model chain fails (credit exhausted on OpenRouter/DeepSeek, 413 payload too large).

**Why MiniMax wins for vision:**
- Token Plan subscription has a **separate credit pool** from OpenRouter/DeepSeek
- No per-token billing — quota-based (monthly ~5.1B M3 tokens)
- Works independently of ASI/AGI bot credit balances
- `mmx-cli` already installed and authenticated

#### Pathway comparison: how images reach the agent

The Hermes gateway has 3 paths for user-attached images on text-only primary models (DeepSeek V4 Flash):

**Path A — Path B model swap (fragile, not recommended)**
When `_decide_image_input_mode` returns `"text"`, the gateway temporarily swaps the agent's model to `auxiliary.vision.*` before `run_conversation()`. Images are attached as native pixels. After the turn, the original model is restored.

⚠️ **CASCADE FAILURE MODE:** If the swapped model fails (auth, provider down), the image bytes are already in context. Every fallback model (llama, groq, openrouter, tokenrouter) receives `image_url` parts that text-only models can't process → 413 → compression → 413 → dead. No recovery.

**Path B — `_enrich_message_with_vision` transcript pipeline (robust, preferred)**
The gateway calls `vision_analyze_tool()` with MiniMax-M3 via `auxiliary.vision` config. The vision model describes the image (SCENE/OCR/DATA sections). That description is prepended as `[IMAGE TRANSCRIPT]` text. The primary model (DeepSeek) responds based on the text transcript. **If vision fails**, the primary model still works with the original caption — no cascade, no 413.

**Path C — Agent-initiated manual analysis (most reliable, last resort)**
When both automated paths fail, run `mmx vision describe --file /path/to/image.jpg` via terminal and pipe the description into context. This bypasses the entire gateway pipeline and uses the Token Plan directly.

**⚠️ THE HALLUCINATION KILL CHAIN (critical to understand):**

When `_enrich_message_with_vision` calls `vision_analyze_tool()` but the API call **fails silently** (e.g. `api_key: ''` → auth error), the event is still forwarded to the primary model with the original prompt that says "analyse this image". A text-only model (DeepSeek V4 Flash, `supports_vision: false`) receives this prompt but **cannot see the image**. Instead, it hallucinates image content from stale session context (past conversations about food → "char koay teow"). **This is a pipeline failure**, not a model hallucination — a blind model is asked to describe something it cannot see.

**Detection:** When the model gives a lengthy, specific image description on a text-only model, suspect silent vision failure:
```bash
# 1. Is the vision provider API key set?
grep -A4 'auxiliary:' /root/.hermes/config.yaml | grep -A4 'vision:' | grep api_key

# 2. Is MINIMAX_BASE_URL plaintext (not sops encrypted)?
source /root/.secrets/kunci-mas.env && echo $MINIMAX_BASE_URL

# 3. Does the vision endpoint work?
curl -s https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"minimax-m3","messages":[{"role":"user","content":[{"type":"text","text":"hi"}]}]}'
```

**Fixed config (2026-07-30):**
```yaml
auxiliary:
  vision:
    provider: minimax
    model: minimax-m3
    base_url: https://api.minimax.io/v1
    api_key: '${MINIMAX_API_KEY}'
model:
  supports_vision: false
```

#### Preferred config (as of 2026-07-30):

```yaml
auxiliary:
  vision:
    provider: minimax
    model: minimax-m3         # ✅ Confirmed — works via OpenAI-compatible endpoint
    timeout: 120
```

Also ensure `model.supports_vision: false` in the `model:` section — setting it `true` on a text-only model like DeepSeek V4 Flash short-circuits all routing logic and sends raw pixels to an API that can't process them.

**Confirmed (2026-07-30):** `minimax-m3` is the correct model name for the OpenAI-compatible chat completions endpoint at `https://api.minimax.io/v1/chat/completions`. It accepts `image_url` content type, processes 1280×720 images in ~3s, returns 200. No `mmx-cli` wrapper needed — direct REST call works with `MINIMAX_API_KEY` from kunci-mas.env.

**Why this works when all other providers fail:**
- MiniMax Token Plan has a **separate credit pool** from OpenRouter/DeepSeek/TokenRouter
- No per-token billing — quota-based monthly subscription (~5.1B M3 tokens)
- Works independently of ASI/AGI bot credit balances (proven 2026-07-30: TokenRouter $-0.04, OpenRouter $0, Groq 6K TPM — all failed, MiniMax succeeded)

**Pattern — Manual fallback when automated pipelines fail:**
```bash
# Image arrives in /root/HERMES/image_cache/ or /root/HERMES/media/
mmx vision describe --file /path/to/image.jpg --non-interactive 2>&1
```
Pipe the description back as context. This bypasses the broken OpenRouter/Qwen chain entirely.

**Pitfall — `delegate_task` does not help for vision:**
Subagents spawned via `delegate_task` **inherit the parent model** (DeepSeek V4 Flash). The child cannot see images natively either. For delegated vision, the child would need explicit model override or access to `mmx vision describe` as a tool — which adds complexity (2 round trips, file path passing) without solving the root problem.

**Pitfall — minimax-mcp has NO vision analysis:**
The official `minimax-mcp` GitHub repo provides generation tools only (text_to_audio, text_to_image, generate_video, music_generation). It does NOT include any vision/analysis/image-description capabilities. For image analysis, use MiniMax-M3 via the `minimax` provider or `mmx vision describe` CLI.

**Pitfall — A2A gateway cannot route simple vision tasks:**  
AAA (`:3001`) exposes an A2A v1.0 endpoint (`POST /a2a`, requires `A2A-Version: 1.0` header). However, all incoming tasks are gated by **EMD validation** (tri-witness threshold W3 ≥ 0.3). Anonymous/spawned agents get W3=0.1 and are blocked:
```
EMD_VALIDATION_BLOCKED: External payload failed tri-witness threshold.
W3=0.1, threshold=0.3
```
To bypass this, the caller needs Ed25519 identity binding through `arif_init`. For a simple "analyze this image" task, the EMD gate is **overweight governance** — the 4-hop round trip (Hermes → A2A gate → EMD → OpenClaw → MiniMax → back) adds latency, complexity, and a governance failure mode that doesn't improve the outcome over a direct API call. Use the `auxiliary.vision` provider or `mmx vision describe` for vision tasks instead.

**OpenClaw A2A registration (2026-07-30):** OpenClaw is now registered in the AAA federation as an A2A agent:
- Agent card: `https://aaa.arif-fazil.com/a2a/openclaw/agent-card.json`
- A2A endpoint: `https://aaa.arif-fazil.com/a2a/openclaw`
- Skills registered: 21 (but zero vision skills)
- Topological role: Metabolizer
- Federation agents: 333-AGI · 555-ASI · 888-APEX · antigravity · openclaw

To route vision through OpenClaw, a vision skill must be built and registered in its A2A agent card first.

**Pitfall — Dual gateway processes cause 409 Conflict errors:**  
If the Hermes gateway restart (`--replace` flag) doesn't properly terminate the old process, two gateway processes poll the same Telegram bot token. This manifests as:
```
⚠️ The model provider failed after retries.
→ fallback → compression → 413 → dead
```
The error looks like a model/provider failure but is actually a **Telegram 409 Conflict** (two long-poll connections on the same token). Fix: `kill <old_pid>` then verify only one gateway process remains:
```bash
ps aux | grep 'gateway run' | grep -v grep
```

**Pitfall — Default config traps:**
- `/root/HERMES/config.yaml` had `model.supports_vision: true` declared on DeepSeek V4 Flash (text-only) — this poisoned the image routing: `decide_image_input_mode` returned `"native"` immediately, bypassing all fallback logic and sending raw pixels to DeepSeek's API which can't process them. **Fix:** set `supports_vision: false` for text-only models.
- Same config had `auxiliary.vision.provider: openrouter` (changed to `minimax` 2026-07-30)
- OpenRouter credits deplete independently and often run out faster than MiniMax Token Plan
- The 413 cascade can be avoided by routing to `_enrich_message_with_vision` *before* the full fallback chain exhausts
- Do NOT send the full chat history + image to MiniMax — extract the image first, describe it, then inject the description as text

## ⚠️ Edge Cases

- **Quota exhausted (429) — vision fallback chain.** (1) Anthropic API if `ANTHROPIC_API_KEY` has credits; (2) MiMo API if `MIMO_API_KEY` has Token Plan credits; (3) `tesseract` OCR as last resort.
- **`vision_analyze()` 404 model errors** — When the active model does not support vision natively (e.g. DeepSeek V4 Flash), `vision_analyze()` may return 404 with `"models/... is not found"`. This is not a vision failure — it's a routing failure. Fall back to `mmx vision describe --file <path>` which uses MiniMax Token Plan's separate credit pool.
- 401 after login → set region manually: `mmx config set --key region --value global`
- **`mmx image generate --output` is ignored** — files save as `image_001.jpg` in current working directory.
- Key prefix `sk-cp-` = Token Plan (subscription), not pay-as-you-go
- Video is async — poll with `mmx video task get --task-id <id>`, then download
- Old SSE MCP servers (minimax-media :18090, minimax-code :18091) are DEAD. Use mmx-cli or stdio minimax-coding-plan-mcp instead
- Output files go to `minimax-output/` in cwd (except image — goes to cwd root)
- Vision fallback priority: MiniMax (Token Plan) → Anthropic → MiMo → tesseract. MiniMax should be FIRST, not last, because Token Plan is a separate credit pool from OpenRouter/DeepSeek.
- When Hermes gateway crashes on image payload (413 / credit exhausted), do NOT let the full fallback chain run. Intercept early: run `mmx vision describe` on the saved image directly, inject the description as text into context, continue with primary model. This avoids the death spiral of compression → 413 → garbage.
- "Gemini proposes, Hermes builds" — BUILD what Gemini proposes, don't just critique

---

*Forged: 2026-07-09 · Upgraded: 2026-07-20 (Image Generation + Malay Phenotype) · Upgraded: 2026-07-30 (Path B failure cascade + A2A EMD gate + dual-gateway 409 + reference file) · Upgraded: 2026-07-30 (Hallucination kill chain api_key + sops MINIMAX_BASE_URL + config pitfalls table) · Corrected: 2026-07-30 (removed phantom policy ref, added MuleRouter to image model priority)*
*DITEMPA BUKAN DIBERI*
