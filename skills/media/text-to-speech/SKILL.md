---
name: token-plan-tts
description: "Generate speech audio via QwenCloud Token Plan TTS. Activates when user asks to speak text, generate audio, or convert text to voice."
---

# Token Plan Text-to-Speech

Call the Token Plan speech synthesis API via DashScope WebSocket SDK.

## Supported model

| Model | Description |
|-------|-------------|
| `qwen-audio-3.0-tts-plus` | High-quality TTS, multiple languages, voice cloning |

## Prerequisites

```bash
pip install dashscope
```

## Usage

```python
import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
from datetime import datetime

dashscope.api_key = os.environ.get("QWEN_API_KEY")
dashscope.base_websocket_api_url = "wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"

synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-plus",
  voice="longxiaochun",  # default voice
  format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
)

audio = synthesizer.call("<text>")
filename = f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
with open(filename, "wb") as f:
  f.write(audio)
print(f"Audio saved: {filename}")
```

## Available voices

Default: `longxiaochun`. Multiple voices available — see QwenCloud TTS docs for full list.

## Notes

- Billed in Credits from Token Plan quota
- Uses WebSocket protocol (not HTTP REST)
- Supports voice cloning from audio samples (separate API)
