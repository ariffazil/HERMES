# Voice Note + Transcription Patterns for Trading Communication

## Generating Voice Notes (edge-tts)

Use `ms-MY-OsmanNeural` for Nusantara Malay voice. User preference confirmed 2026-07-13.

```bash
# Write explanation text
cat << 'EOF' > /tmp/explain.txt
Abang Sado, ni Hermes. [explanation in simple BM-English mix]
EOF

# Generate voice
edge-tts --voice ms-MY-OsmanNeural --text "$(cat /tmp/explain.txt)" --write-media /tmp/explain.ogg
```

**Rules:**
- Keep under 60 seconds (~150 words)
- Simple BM, no jargon
- Repeat key points
- End with clear action item
- Deliver BOTH text + voice (text for reading, voice for listening)

## Transcribing Audio (faster-whisper)

When user sends voice note, transcribe with faster-whisper (NOT whisper — numba/llvmlite broken).

```python
from faster_whisper import WhisperModel
model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe('/path/to/audio.mp3', language='ms')
for seg in segments:
    print(f'[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}')
```

**Pitfall:** Malay transcription is rough — BM-English mix confuses the model. Key numbers (prices, lot sizes) often misheard. Always verify with user if uncertain.

## When to Use Voice Notes

- User says "bagi voice note" or "explain kat dia"
- Explaining trading concepts to non-technical traders
- Direction confusion (long vs short)
- Trade setup explanation
- Alert interpretation

## Proven 2026-07-16

- edge-tts with ms-MY-OsmanNeural works for Malay voice notes
- faster-whisper works for Malay transcription (base model, CPU)
- User wants BOTH text (for reading) and voice (for listening) when explaining to traders
