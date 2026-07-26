---
name: tts-edge-fallback
description: "TTS fallback using edge-tts when OpenAI TTS quota is exhausted or unavailable. Free, local, supports Malay."
tags: [tts, voice, audio, telegram, fallback, malay]
---

# TTS Edge Fallback

When OpenAI TTS fails (429 quota exceeded or unavailable), use `edge-tts` as a free local fallback. Works well for Malay and English.

## Quick Command

```bash
edge-tts --text "Your text here" --voice ms-MY-OsmanNeural --write-media /tmp/tts_output.mp3
```

With rate/pitch tuning for more natural speech:
```bash
edge-tts --voice "ms-MY-OsmanNeural" --rate "+5%" --pitch "+0Hz" --text "..." --write-media /tmp/output.mp3
```

Then send with `MEDIA:/tmp/tts_output.mp3`

## Setup (one-time)

```bash
pip install edge-tts --break-system-packages
```

## Voice Options (Malay)

| Voice | Gender | Quality |
|-------|--------|---------|
| `ms-MY-OsmanNeural` | Male | Good |
| `ms-MY-YasminNeural` | Female | Good |

## TTS provider decision tree (2026-07-08)

Hermes TTS now supports multiple providers. Pick by language and quality needs:

| Provider | Free? | Malay quality | Penang dialect | Singing | Voice cloning | Best for |
|----------|-------|---------------|----------------|---------|---------------|----------|
| `edge` (ms-MY-Osman) | ✅ | Standard BM, not Penang | ❌ Standard BM only | ❌ | ❌ | Quick free fallback, standard Malay |
| `openai` (gpt-4o-mini-tts) | ❌ quota-billed | OK | ❌ | ❌ | ❌ | Production quality English |
| `mimo` (Xiaomi V2.5) | ✅ (limited time) | Good — voice design supports Penang description | ⚠️ achievable via description, not guaranteed | ✅ (built-in voices only) | ✅ (voiceclone model) | Custom voice, Penang-style |
| `elevenlabs` | ❌ quota-billed | OK multilingual | ⚠️ via voice cloning | ❌ | ✅ | Highest quality, paid |
| `minimax`, `mistral`, `neutts`, `piper` | varies | varies | varies | ❌ | ❌ | Niche use cases |

**Default chain:** `mimo` (if configured) → `openai` (if quota) → `edge-tts` (always free).

**Quality override for Malay:** When user explicitly asks for "elok sikit" / "better quality" / "yang bagus" voice in Malay, **prefer `edge-tts` over the default mimo provider**. Session evidence (2026-07-11): user rejected mimo TTS output as low quality, then accepted Edge TTS `ms-MY-OsmanNeural` with `--rate "+5%"`. The default `text_to_speech` tool routes through mimo which can produce robotic output for long BM text. Edge TTS with rate adjustment sounds more natural. Command:
```bash
edge-tts --voice "ms-MY-OsmanNeural" --rate "+5%" --pitch "+0Hz" --text "..." --write-media /tmp/output.mp3
```

**For Penang-style Malay specifically:** the only path that can hit a Penang accent is `mimo-v2.5-tts-voicedesign` with a description like *"A 35-year-old Malaysian Chinese male from Penang, conversational casual tone, mixes English and Bahasa Melayu naturally, warm and direct, slight northern Malaysian intonation."* Edge TTS `ms-MY-*` voices are Standard BM (DBP-style, not Penang). ElevenLabs can clone a real Penang voice with a sample — slower + paid.

## MiMo TTS quick reference

Add to `~/.hermes/config.yaml` under top-level `tts:` (NOT under `providers:`):

```yaml
tts:
  provider: mimo
  mimo:
    api: https://token-plan-sgp.xiaomimimo.com/v1
    key_env: MIMO_API_KEY
    model: mimo-v2.5-tts-voicedesign
    voice: default
    sample_rate: 24000
```

Then `hermes config set tts.provider mimo` to make it the default. Requires `MIMO_API_KEY` in `~/.hermes/.env` (or whichever `key_env` you declared).

**Three TTS models:**
- `mimo-v2.5-tts` — built-in voices, supports singing
- `mimo-v2.5-tts-voicedesign` — describe voice in natural language, no sample needed
- `mimo-v2.5-tts-voiceclone` — clone from audio sample (data URI base64)

**For Penang voice (the realistic path, 2026-07-08):**

The `text_to_speech` tool routes through whatever provider is configured. When user asks for "voice Penang" / "suara Penang" / "bahasa Penang" voice:

1. Confirm `mimo` is configured (see config above). If not, offer to add it.
2. Pick model: `voicedesign` (text-only description) is fastest, no sample needed. Use `voiceclone` only if user has a 30-60s audio sample of their target voice.
3. Generate test sample with a Penang-style description (see "For Penang-style Malay specifically" above).
4. Send via `MEDIA:/path/to/output.wav`.
5. If accent isn't Penang enough, iterate on the description: add words like "Penang", "northern Malaysian", "casual Penang conversational", "slight nasal intonation typical of Penang Chinese Malay speakers".

**Critical gotchas** (full detail in `references/mimo-tts-api-quirks.md`):
- For `mimo-v2.5-tts-voicedesign`: do NOT include `audio.voice` field — returns 400 "Param Incorrect". Voice design is text-described, not voice-id-selected.
- For `mimo-v2.5-tts-voiceclone`: the `audio.voice` field is REQUIRED and must be a `data:audio/<mime>;base64,<...>` data URI of the reference sample.
- The `audio.format` field supports `wav` and `pcm16`. Use `wav` for delivery (self-describing header).
- Audio is base64-encoded in `choices[0].message.audio.data`. Save to disk, verify RIFF header, then send with `MEDIA:`.
- Sample rate is 24kHz PCM16 mono. Telegram will accept WAV as a voice bubble.

## Voice Options (English)

| Voice | Gender | Quality |
|-------|--------|---------|
| `en-US-GuyNeural` | Male | Good |
| `en-US-JennyNeural` | Female | Good |

## "Nusantara Mode" (session-confirmed 2026-07-13)

When user says **"Nusantara mode"**, **"suara lain"** (different voice), or explicitly rejects the current voice → switch to **edge-tts** with Malay native voices. This is a strong preference signal — user wants authentic Malay pronunciation, not AI-accented BM.

```bash
edge-tts --voice ms-MY-OsmanNeural --file /tmp/content.txt --write-media /tmp/output.mp3 --rate="-5%"
```

- **OsmanNeural** (male) — warm, conversational, good for trading/analysis
- **YasminNeural** (female) — friendly, clear
- Use `--rate="-5%"` for dense content (numbers, analysis) — slower = clearer
- Use `--rate="+5%"` for casual/chat content — faster = natural

**Trigger detection:** User says "guna suara lain", "tukar suara", "Nusantara mode", "suara Melayu", "voice lain", "suara laki macho", "suara macho", "masculine voice" → immediate switch to edge-tts. Don't ask which voice, default to OsmanNeural. For "macho" / "laki" / "masculine" requests, always pick male voice (OsmanNeural), never YasminNeural.

## Trading/Analysis Voice Content (BM)

When generating voice notes for trading analysis in BM:

1. **Write for speech, not text** — remove markdown tables, symbols, formatting
2. **Spell out numbers naturally** — "$4,120" → "empat ribu seratus dua puluh dolar"
3. **Speak percentages** — "2%" → "dua peratus"
4. **Use conversational BM** — "Kau" not "Anda", "dia" not "pasaran" (when referring to gold/market)
5. **Structure with verbal markers** — "Yang bagus dulu" / "Sekarang yang tak bagus pula" / "Kesimpulan dia"
6. **Keep trading jargon in English** — "support", "resistance", "spread", "stop loss" — BM traders expect these
7. **End with action** — clear next step or recommendation
8. **Max ~4 minutes** of audio per note — split into segments if longer

### Daily Trader Briefing (proven 2026-07-18, SADO 8am cron)

For an automated daily market briefing to a Malaysian trader audience (e.g., cron `2258f1b3fa0e` → SADO group), use this **90-second template**:

```
edge-tts --voice ms-MY-OsmanNeural --rate "+5%" --file /tmp/syed_voice.txt --write-media /tmp/syed_voice.mp3
```

**Structure:**
1. Opening: "Abang [name], ni update gold [session]. Harga sekarang [spell out] dolar." (~10s)
2. Cerita: 2-3 sentences on what happened (drop/range/rebound) (~25s)
3. Levels: support + resistance, spelled out (~20s)
4. Trend: EMA200 direction + RSI state (~15s)
5. Verdict + action: SEAL/SABAR/HOLD/VOID + 1 specific trade action (~15s)
6. Close: "Trade selamat, [name]." (~5s)

**Number spelling rules for traders:**
- "$4,023" → "empat ribu dua puluh tiga dolar"
- "$67" → "enam puluh tujuh dolar"
- Whole prices keep "dolar"; ratios like 1:2 → "satu banding dua"
- RSI 63.6 → "enam puluh tiga perpuluhan enam"
- Round to whole numbers when possible — easier to follow
- Trading jargon stays English: "support", "resistance", "break", "stop loss"

**Multi-channel delivery rule:** When voice accompanies text + chart in a briefing, send **text first → chart → voice last**. Voice reinforces; doesn't replace.

**Skip voice when:** verdict is SABAR + state is Choppy. Text suffices for "jangan trade" alone.

Full template, verdict→action mapping, and worked example: see `syedos` skill → `references/voice-briefing-format.md`.

## Workflow

1. User requests voice message (triggers: "voice mode", "voice", "dalam voice", "buat voice", "hantar voice", "suara Penang", "voice Bahasa Penang", "TTS bahasa melayu", "voice elok", "yang bagus sikit", "Nusantara mode", "suara lain", "tukar suara")
2. **Voice override check:**
   - "Nusantara mode" / "suara lain" / "tukar suara" → edge-tts ms-MY-OsmanNeural (skip mimo)
   - "elok sikit" / "better quality" / "yang bagus" → edge-tts with `--rate "+5%"` (session-proven, 2026-07-11)
   - "Penang" / "suara Penang" → mimo voicedesign with Penang description
3. Try `text_to_speech` tool first (uses configured provider) — UNLESS voice override check routed elsewhere
4. If OpenAI 429 / quota error OR user rejects quality → fall back to `edge-tts` via terminal
5. If user explicitly wants Penang/Malaysian dialect → confirm `mimo` provider is configured; if not, walk through config
6. Generate with appropriate voice
7. Send file with `MEDIA:/path/to/file.{mp3,wav}`

### Converting existing text to voice

When user replies "Voice mode" or "voice" to a text response you already sent:
1. Take the content of your previous text response
2. Reformat for spoken delivery (remove markdown tables, links, formatting — make it flow naturally as speech)
3. Generate via configured provider
4. Send with `MEDIA:` prefix

### Proactive voice offer

When user seems mobile (in car, parking, gym, outdoors) and the response is informational:
- Offer voice: "Nak aku voice kan?"
- Or just send both text + voice proactively

## Pitfalls

- **Character limit**: edge-tts handles long text well, but keep under ~5000 chars per call for reliability
- **Malay pronunciation**: `ms-MY-OsmanNeural` handles Manglish/Malay mix reasonably well, but it's Standard BM — not Penang
- **File cleanup**: Files in `/tmp/` are ephemeral — fine for one-shot delivery
- **Telegram voice**: Telegram renders `.ogg` (Opus in OGG container) as voice bubbles with waveform UI. MP3 and WAV send as regular audio files — NOT voice bubbles. Always convert to OGG for voice notes:
  ```bash
  ffmpeg -y -i /tmp/output.mp3 -c:a libopus -b:a 32k -ac 1 /tmp/output.ogg
  ```
  Then deliver with `MEDIA:/tmp/output.ogg`. Proven 2026-07-22: two BM voice notes delivered successfully as OGG voice bubbles.
- **"Penang voice" expectation management**: edge-tts cannot do Penang. Honest framing beats pretending — tell user what's actually possible and what path gets closest (MiMo voicedesign with Penang description, or voiceclone with sample). Don't claim you'll deliver Penang when the underlying model is Standard BM.
- **MiMo `voicedesign` description quality matters more than length**: 1-2 sentences with specific dialect cues ("Penang", "northern Malaysian", "conversational casual") beats a 200-word essay. Test iteratively.
- **MiMo is free "for a limited time"** per their docs (verified 2026-07-08). Don't promise permanent free access.

## Reference

- `references/mimo-tts-api-quirks.md` — full MiMo V2.5 TTS API quirks
- `references/arif-voice-note-proxy.md` — Arif voice note proxy pattern: speaking to a third party in the room via voice note: the 400-error trap with `audio.voice` for voicedesign, base64-decoding recipe, working curl + Python examples, style control tokens for Penang voice, Hermes config integration, known limitations, and provider choice matrix.
