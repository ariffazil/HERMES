# MiMo TTS API — Quirks, Gotchas, Working Recipes

**Verified 2026-07-08 against `https://token-plan-sgp.xiaomimimo.com/v1` (Xiaomi MiMo V2.5 series).**

## The three TTS models

| Model ID | Voice input | Singing | Voice cloning | Voice design |
|----------|-------------|---------|---------------|--------------|
| `mimo-v2.5-tts` | Built-in voice names (e.g. `default`) | ✅ | ❌ | ❌ |
| `mimo-v2.5-tts-voicedesign` | Text description in user message | ❌ | ❌ | ✅ natural language |
| `mimo-v2.5-tts-voiceclone` | Audio sample as base64 data URI | ❌ | ✅ | ❌ |

All three return 24kHz PCM16 mono audio, base64-encoded in `choices[0].message.audio.data`.

## Critical gotcha #1: `audio.voice` is model-specific

```python
# ✅ Works for mimo-v2.5-tts (built-in voice)
audio={"format": "wav", "voice": "default"}

# ❌ FAILS for mimo-v2.5-tts-voicedesign with HTTP 400 "Param Incorrect: audio.voice is not supported for voice design model"
audio={"format": "wav", "voice": "default"}  # for voicedesign: OMIT audio.voice entirely

# ✅ Works for mimo-v2.5-tts-voiceclone (voice MUST be a data URI of the reference audio)
audio={"format": "wav", "voice": "data:audio/mpeg;base64,<BASE64_OF_SAMPLE>"}
```

For `voicedesign`, the voice is described in the `messages[role=user].content` field as a natural-language description. Do NOT include `audio.voice` at all.

## Critical gotcha #2: audio response is base64 in `choices[0].message.audio.data`

The API returns JSON (NOT a raw audio stream) when `stream: false`. Audio is base64-encoded WAV (or PCM16) inside the `audio.data` field:

```json
{
  "id": "86edfd171a2448e1b30e6cd4620bf534",
  "choices": [{
    "message": {
      "role": "assistant",
      "audio": {
        "id": "feff075fcc1243878a2d54c9782e0eb0",
        "data": "UklGRiT+AQBXQVZFZm10IBAAAA..."  // <-- base64 WAV bytes
      }
    }
  }],
  "model": "mimo-v2.5-tts-voicedesign"
}
```

**Decode recipe:**
```python
import json, base64
with open('/tmp/response.json') as f:
    data = json.load(f)
audio_b64 = data['choices'][0]['message']['audio']['data']
audio_bytes = base64.b64decode(audio_b64)
# Verify WAV header before saving
assert audio_bytes[:4] == b'RIFF', f"Not a WAV: {audio_bytes[:4]}"
with open('/root/.hermes/audio_cache/output.wav', 'wb') as f:
    f.write(audio_bytes)
```

When `stream: true`, the API returns base64 chunks that must be concatenated and decoded (more complex — only needed for long-form TTS).

## Working curl recipe (voicedesign)

```bash
curl -sS -X POST "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions" \
  -H "Authorization: Bearer $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-tts-voicedesign",
    "messages": [
      {"role": "user", "content": "A 35-year-old Malaysian Chinese male from Penang, conversational casual tone, mixes English and Bahasa Melayu naturally, warm and direct, slight northern Malaysian intonation."},
      {"role": "assistant", "content": "Hangpa, bro. Ni suara test Penang style."}
    ],
    "audio": {"format": "wav"},
    "stream": false
  }' --max-time 60 -o /tmp/response.json
```

Then decode with the Python recipe above. Verified produces a valid WAV file with Penang-style voice on 2026-07-08.

## Working curl recipe (voiceclone)

```python
import base64, json, requests
with open("reference.mp3", "rb") as f:
    voice_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {MIMO_API_KEY}"},
    json={
        "model": "mimo-v2.5-tts-voiceclone",
        "messages": [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Text to speak in the cloned voice."}
        ],
        "audio": {
            "format": "wav",
            "voice": f"data:audio/mpeg;base64,{voice_b64}"
        }
    }
)
audio_b64 = response.json()['choices'][0]['message']['audio']['data']
with open("cloned_output.wav", "wb") as f:
    f.write(base64.b64decode(audio_b64))
```

## Style control

The MiMo V2.5 docs mention natural-language style control and "director mode" (character/scene/guidance three dimensions). For Penang voice, the **single most important** signal is the user's mention of "Penang" in the description. Other useful tokens:

- "Malaysian Chinese" / "Malay" / "Malaysian" — anchors regional identity
- "conversational" / "casual" / "direct" — softens formal-style default
- "warm" / "slight smile" — adds friendly tone
- "northern Malaysian intonation" / "slight nasal" — Penang-area accent cues
- "code-switches English" / "mixes English and Bahasa Melayu" — for Manglish speakers

**Test iteratively.** Generate → listen → adjust description. One good description often beats many; ~2 sentences is the sweet spot.

## Config integration with Hermes

The Hermes TTS layer (after the 2026-07-08 update) reads the `tts:` block in `~/.hermes/config.yaml`. The schema is:

```yaml
tts:
  provider: mimo         # or "openai", "edge", "elevenlabs", "minimax", "mistral", "neutts", "piper"
  mimo:
    api: <base_url>
    key_env: <ENV_VAR_NAME>
    model: <model_id>
    voice: <voice_id_or_default>
    sample_rate: 24000
```

Use `hermes config set tts.mimo.<key> <value>` to mutate. The `hermes config set tts.provider mimo` command switches the default.

## Why I split the config from `providers:`

The `providers:` block in `config.yaml` is for **text/chat inference** providers (LLMs). TTS is a separate concern with its own sub-block under `tts:`. Don't add TTS providers under `providers:` — Hermes won't pick them up. The same applies to STT (`stt:` block).

## Pricing

"Billing: Free for a limited time." (per the official docs at the time of writing, 2026-07-08). Check `https://platform.xiaomimimo.com/#/console/usage` for current usage and any pricing changes. Don't promise permanent free access.

## Known limitations

- No native streaming integration with the Hermes `text_to_speech` tool (it waits for full response, not chunks)
- No SSML or phoneme control (only natural-language style hints)
- Voiceclone reference sample is a SINGLE audio file, no per-language or per-style pinning
- No batch endpoint (one TTS call = one HTTP POST)

## When to choose another provider

| Need | Use |
|------|-----|
| Quickest free Standard BM | `edge` (ms-MY-OsmanNeural) |
| Highest quality English | `openai` (gpt-4o-mini-tts) or `elevenlabs` (multilingual_v2) |
| True Penang dialect (audio sample required) | `mimo-v2.5-tts-voiceclone` with Penang speaker sample |
| Custom voice design without audio sample | `mimo-v2.5-tts-voicedesign` |
| Singing synthesis | `mimo-v2.5-tts` (built-in voices only — voice design/clone don't support singing) |
