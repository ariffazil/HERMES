# Arif Voice Note Proxy Pattern

When Arif is physically with someone and says "jawab dalam voice note," "bagitau sat kawan aku," or similar, he wants a **voice note in his voice** that speaks directly **to the third party**, not to him.

## Pattern Recognition

**Triggers:**
- "jawab dalam voice note" (answer in voice note)
- "bagitau sat kawan aku" (tell my friend briefly)
- "I'm with [name]. Jawab dalam voice note."
- "bagitau [name] kenapa..."

**What this means:**
- Arif is in the room with someone (e.g., Ezriq, Syed, Khairuddin)
- He wants you to articulate something he believes to that person
- He plays the voice note aloud — the third party hears it
- You are speaking **as Arif's proxy**, not to Arif

## Voice Configuration

```bash
edge-tts --voice ms-MY-OsmanNeural --rate=+5% -f /tmp/script.txt --write-media /tmp/output.mp3
ffmpeg -y -i /tmp/output.mp3 -c:a libopus -b:a 32k -ac 1 /tmp/output.ogg
```

Deliver with `MEDIA:/tmp/output.ogg`

## Writing Style for Proxy Voice Notes

1. **BM casual, conversational** — Arif's natural voice. "Kau" not "Anda." Code-switch English for technical terms.
2. **Direct address to third party** — You're speaking TO them, not ABOUT them. "Kau tengok..." not "Dia tengok..."
3. **Punchy, opinionated** — Arif's views, unflinching. No hedging, no "some people think."
4. **Short paragraphs** — ~30-90 seconds total. People listen in a room, not with headphones.
5. **End with a point** — Conclusion or action, not a fade-out.
6. **No markdown, no links** — This is spoken audio. Spell out numbers naturally.

## Session Examples

### 2026-07-22: Kernel vs LLM (to Ezriq)
Arif: "I'm with ezriq. Jawab dalam voice note. Kenapa kernel more important than ai llm"
→ Generated ~90s voice note in ms-MY-OsmanNeural +5%, BM casual. Explained kernel = steering wheel + brakes + constitution, LLM = engine only.

### 2026-07-22: Coding is obsolete (to Ezriq)
Arif: "Bagitau sat kawan aku kenapa sekarang sia2 belajar bahasa coding. Anak dia dok belajar coding"
→ Generated ~2min voice note. Argued AI agents now write better code, syntax learning = calligraphy after printing press, real value is systems thinking + governance + taste.

## Key Distinction from Normal Voice Mode

| Normal Voice Mode | Proxy Voice Note |
|---|---|
| Arif IS the audience | Third party IS the audience |
| "Voice mode" / "voice kan" | "Bagitau [name]..." / "Jawab untuk [name]" |
| Content = for Arif's consumption | Content = Arif's opinion, delivered TO someone else |
| Tone = informational | Tone = persuasive, opinionated, personal |

## OGG Conversion

For Telegram voice bubbles, convert MP3 to OGG with ffmpeg:

```bash
ffmpeg -y -i /tmp/input.mp3 -c:a libopus -b:a 32k -ac 1 /tmp/output.ogg
```

OGG with opus codec at 32kbps mono renders natively as a voice bubble on Telegram.
