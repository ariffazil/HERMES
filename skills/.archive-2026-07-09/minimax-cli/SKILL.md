---
name: minimax-cli
description: "MiniMax multimodal via mmx-cli — TTS, video, music, image, vision, search"
version: 1.0.0
tags: [minimax, tts, video, music, image, vision, multimodal]
metadata:
  hermes:
    requires: [mmx-cli]
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

- Monthly Max: ~5.1B M3 tokens, 3 video/day,21 video/week
- General models + video + speech + music + image share one quota bar
- 5-hour rolling window + weekly window
- TTS free for limited time (doesn't consume quota)

## TTS Fallback Chain (Telegram voice messages)

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

## Music Generation Workflow (proven 2026-07-11)

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

**Proven example (2026-07-11):** Generic Kaparinyo vs researched Minangkabau/Gamad version with authentic Bahasa Minang lyrics. The researched version produced materially better results because tags matched the actual musical tradition (keroncong, Portuguese guitar, gandang) rather than generic "gamelan, kompang."

**Research sources:** Academic papers (ResearchGate), Wikipedia, YouTube traditional performances, Spotify/Smule for lyric verification. See `references/kaparinyo-research-example.md` for a full worked example.

### Audio Evaluation

Two tools for evaluating generated music:

- **`scripts/akal_somatic_scoring.py`** — ffmpeg-only audio scoring. Three checks: PULSE (temporal fidelity), SOUL (cultural alignment), FLOW (entropy equilibrium). No librosa needed. Returns JSON verdict (SEAL/SABAR/HOLD).
- **`templates/cultural_manifold.json`** — Reusable schema for culturally-grounded music generation. Defines identity, structural priors, harmonic constraints, timbre palette, lyric constraints, and evaluation thresholds. Copy and modify for other traditions (Zapin, Asli, Dondang Sayang, etc.).

### Music Evaluation Pipeline

Full evaluation toolkit at `/root/music-eval/` — genre scoring, somatic analysis, paradox engine, motif memory, Telegram signal observer. See `references/music-eval-pipeline.md` for architecture, CLI usage, and A-FORGE integration path. A-FORGE already has `paradox-engine/models.py` with 16-dim somatic vectors — see `references/aforge-paradox-engine.md`.

### Related References

- `references/jina-reader-medium.md` — Reading Medium/Cloudflare-protected articles via Jina Reader
- `references/cross-organ-wiring-pattern.md` — Wiring external engines into arifOS kernel (enforcement gates)

### Vision for Trading Chart Analysis (PROVEN 2026-07-18)

When the trading agent needs to analyze MT5/chart screenshots but the main model lacks native vision, MiniMax vision is the primary fallback. **This is WAJIB for any trading workflow** — the agent must be able to read chart patterns, S/R levels, and order levels from screenshots.

```bash
# Auth (once per session — key is in vault.env)
source /root/.secrets/vault.env
mmx auth login --api-key "$MINIMAX_API_KEY" --non-interactive

# Analyze chart screenshot
mmx vision describe --file /path/to/chart.jpg --non-interactive 2>&1

# JSON output includes:
#   .content      — the text description of the image
#   .base_resp    — status_code, status_msg
```

**Proven workflow (2026-07-18):**
```bash
# Step 1: Get the image (from user message, Telegram, etc.)
# Step 2: Run vision analysis
RESULT=$(mmx vision describe --file /root/.hermes/cache/images/img_xxx.jpg --non-interactive 2>&1)
# Step 3: Extract the analysis text
echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['content'])"
# Step 4: Combine with live API data for a complete picture
```

**What it can read from a trading chart:**
- Price levels (current, high, low, order levels)
- Chart pattern (downtrend, consolidation, flag, pennant)
- Timeframe (H1, H4 visible from the chart header)
- Support/resistance zones
- Pending orders (buy/sell limits, stop losses)
- Market status (open/closed)
- Volume bars and indicators

**When to use:** ANY time Arif or Syed sends a chart screenshot asking "what do you see" or "analisa chart ni". Never reply "sorry cannot see images" — this is now a solved problem.

**Quota check before use:** `mmx quota` — vision counts against the same Token Plan quota as text/video/music.

### Pitfalls

- **Quota exhausted (429) — vision fallback chain.** When `mmx vision describe` returns 429 (quota limit), try: (1) Anthropic API if `ANTHROPIC_API_KEY` has credits, direct `curl` to `/v1/messages` with base64 image; (2) MiMo API if `MIMO_API_KEY` has Token Plan credits; (3) `tesseract` OCR as last resort — extracts text (price levels, labels) but not candle patterns. Proven 2026-07-18: MiMo 429, Anthropic credit exhausted, but OCR successfully read XAUUSD chart levels from MT5 screenshot.
- 401 after login → set region manually: `mmx config set --key region --value global`
- **`mmx image generate --output` is ignored** — The `--output` flag on `mmx image generate` does NOT work. Files always save as `image_001.jpg`, `image_002.jpg`, etc. in the **current working directory** (not `minimax-output/`). After generation, find the file with `find /root -name "image_001.jpg" -newer /tmp/some_recent_file` or check `ls -lt` in the session cwd, then `cp` to your desired path. Proven 2026-07-20: specified `--output /tmp/abang_sado_minimax.jpg` but file landed at `/root/WELL/image_001.jpg`.
- Key prefix `sk-cp-` = Token Plan (subscription), not pay-as-you-go
- Video is async — poll with `mmx video task get --task-id <id>`, then download
- `npx skills add MiniMax-AI/cli -y -g` fails with "PromptScript does not support global skill installation" → manual symlink: `ln -sf ~/.hermes/skills/minimax-cli/SKILL.md ~/.claude/skills/minimax-cli.md` and same for `~/.openclaw/skills/`
- Output files go to `minimax-output/` in cwd, not to Hermes audio cache
- Old SSE MCP servers (minimax-media :18090, minimax-code :18091) are DEAD. Use mmx-cli or stdio minimax-coding-plan-mcp instead
- Built-in `text_to_speech` tool hits OpenAI 429 quota regularly — don't retry, fall back to edge-tts immediately
- **Byte-level Shannon entropy on MP3 is useless** — compressed audio shows ~99.6% entropy regardless of musical content. Don't attempt entropy analysis on mmx output without `librosa` for real spectral features.
- **librosa segfault on complex features** — `librosa.beat.beat_track()`, `chroma_cqt()`, and `mfcc()` may segfault (exit 139) on some numpy/librosa version combos. Use manual STFT-based analysis instead: `librosa.stft()` → `np.abs()` → compute entropy/centroid from magnitude matrix. See `references/librosa-analysis.md` for working code.
- **librosa synthetic vs real audio** — Some features (spectral_bandwidth, spectral_flatness, onset_strength, zero_crossing_rate) work on synthetic sine waves but segfault on real MP3/WAV files of >30s. The STFT-based manual approach in `references/librosa-analysis.md` works on both. Always test on a 30s WAV clip first before running on full tracks.
- **Reading Medium articles** — Medium is behind Cloudflare. `web_extract` fails, `?format=json` returns 403, RSS only has 10 most recent. Use **Jina Reader**: `curl -sL "https://r.jina.ai/https://medium.com/@user/article-slug" -H "Accept: text/plain"` returns clean markdown. Works for any Cloudflare-protected page. Store this as the primary Medium extraction method.
- **"Gemini proposes, Hermes builds"** — When user pastes Gemini output proposing architecture/frameworks/tools, DO NOT just contrast or critique. BUILD what Gemini proposes. The user is using Gemini for thinking and Hermes for execution. If Gemini says "pick one and I'll build it" but never builds — that's your job. The contrast is meaningless without delivery.
- **Music evaluation without librosa** — Use `scripts/akal_somatic_scoring.py` for ffmpeg-only audio scoring (PULSE/SOUL/FLOW). No librosa dependency. Usage: `python3 scripts/akal_somatic_scoring.py <audio.mp3>`. For cultural manifold evaluation, use `templates/cultural_manifold.json` as the reference schema.
