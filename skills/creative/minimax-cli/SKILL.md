---
name: minimax-cli
description: "MiniMax multimodal via mmx-cli — TTS, video, music, image, vision, search. Image generation is PRIMARY choice for Malay/SEA phenotype and realism-critical surfaces."
version: 2.0.0
tags: [minimax, tts, video, music, image, vision, multimodal, malay-phenotype, image-generation]
metadata:
  hermes:
    category: creative
    requires: [mmx-cli]
    related_skills: [token-plan-image, lightweight-image-generation]
  forge_policy: "/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md"
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

> **Policy:** `/root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md`
> **Verdict:** MiniMax image-01 is the DEFAULT for federation image generation. Pollinations only for free prototyping.

### Basic Usage

```bash
mmx image generate --prompt "your prompt" --aspect-ratio 1:1 --non-interactive
```

**Aspect ratios:** `1:1` (default), `16:9`, `9:16`, `4:3`, `3:4`

**Critical pitfall:** `--output` flag is **IGNORED** by `mmx image generate`. Files always save as `image_001.jpg`, `image_002.jpg`, etc. in the **current working directory** (not `minimax-output/`). After generation, find with `ls -lt | head` and `cp` to your desired path. Proven 2026-07-20.

### 🧬 Phenotype

MiniMax image-01 has the strongest SEA/Malay phenotype reading of all available models. When generating images of people:

| Model | SEA Phenotype | Realism | Use Case |
|-------|--------------|---------|----------|
| **MiniMax image-01** | ⭐⭐⭐ Strong | ⭐⭐⭐ Studio-grade | Malay/SEA prompts, realism-critical |
| Qwen image-2.0 | ⭐⭐ Moderate | ⭐⭐ Good | Generic, non-phenotype |
| Pollinations | ⭐ Weak | ⭐⭐ Decent | Free drafts only |

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

### ⚖️ Contrast

Same prompt `shirtless abang sado, Malay, realistic, studio lighting`:

| Dimension | MiniMax image-01 | Pollinations |
|-----------|-----------------|--------------|
| Resolution | 1024×1024 ✅ | 768×768 |
| File size | 184KB ✅ | 73KB |
| Malay phenotype | Strong SEA reading ✅ | Ambiguous/Westernized |
| Realism | Studio-grade, natural ✅ | AI-exaggerated, plastic |
| Prompt understanding | "Abang sado" nailed ✅ | Generic buff guy |
| Cost | Token Plan quota | Free |

**Verdict:** MiniMax wins clean. For any prompt where Malay/SEA phenotype or realism matters, MiniMax is mandatory.

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

- `references/jina-reader-medium.md` — Reading Medium/Cloudflare-protected articles via Jina Reader
- `references/cross-organ-wiring-pattern.md` — Wiring external engines into arifOS kernel (enforcement gates)

## 👁️ Vision

```bash
# Auth (once per session — key is in vault.env)
source /root/.secrets/vault.env
mmx auth login --api-key "$MINIMAX_API_KEY" --non-interactive

# Analyze chart screenshot
mmx vision describe --file /path/to/chart.jpg --non-interactive 2>&1
```

**What it can read from a trading chart:**
- Price levels (current, high, low, order levels)
- Chart pattern (downtrend, consolidation, flag, pennant)
- Timeframe (H1, H4 visible from the chart header)
- Support/resistance zones
- Pending orders (buy/sell limits, stop losses)

## ⚠️ Edge Cases

- **Quota exhausted (429) — vision fallback chain.** (1) Anthropic API if `ANTHROPIC_API_KEY` has credits; (2) MiMo API if `MIMO_API_KEY` has Token Plan credits; (3) `tesseract` OCR as last resort.
- 401 after login → set region manually: `mmx config set --key region --value global`
- **`mmx image generate --output` is ignored** — files save as `image_001.jpg` in current working directory.
- Key prefix `sk-cp-` = Token Plan (subscription), not pay-as-you-go
- Video is async — poll with `mmx video task get --task-id <id>`, then download
- Old SSE MCP servers (minimax-media :18090, minimax-code :18091) are DEAD. Use mmx-cli or stdio minimax-coding-plan-mcp instead
- Output files go to `minimax-output/` in cwd (except image — goes to cwd root)
- "Gemini proposes, Hermes builds" — BUILD what Gemini proposes, don't just critique

---

*Forged: 2026-07-09 · Upgraded: 2026-07-20 (Image Generation + Malay Phenotype section)*
*Policy: /root/A-FORGE/forge_work/2026-07-20/model-selection-policy.md*
*DITEMPA BUKAN DIBERI*
