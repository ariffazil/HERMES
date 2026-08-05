# Three Clarifying Questions — Voice Note Template

When Arif asks for a voice note for someone else to deliberate a hard
decision, use this template. Adapt the wording to context.

## Pattern

```python
text_to_speech(
    text = """[Name], aku nak tanya kau tiga soalan. Jawab dalam hati kau dulu.
Tak payah bagitahu sesiapa. Tiga soalan je.

Soalan pertama. Kau bayangkan dua tahun dari sekarang. [State the imagined
scene — typically the "do nothing" path]. Kau rasa [legitimate positive
emotion] atau rasa [legitimate negative emotion]?

Soalan kedua. Kau bayangkan dua tahun dari sekarang. [State the "fight/act"
path with realistic cost]. Kau rasa [legitimate positive emotion] atau rasa
[legitimate negative emotion]?

Soalan ketiga. Soalan ni paling penting. Kau bayangkan [longer time horizon,
e.g. lima tahun dari sekarang]. Kau nak cakap apa kat diri kau sendiri?
Kau nak cakap "[path A frame]" atau kau nak cakap "[path B frame]"?

Tiga soalan tu. Jawab dalam hati kau. Jawapan kau tu — itu jawapan yang
betul. Bukan aku punya. Bukan peguam punya. Kau punya.

Ditempa bukan diberi. Peace out."""
)
```

## Voice Note Rules

- Under 60 seconds (test with `wc -c` on the text — ~15 chars/sec)
- Natural code-switching: Malay, English, casual register
- Address the person by their call name (e.g. "Abang Sado")
- Don't add "perlu pergi doktor" or other medical/professional framing
- End with a "peace out" or "take care" — soft close

## Voice Note Quality (CRITICAL)

The voice note goes to a REAL PERSON making a life decision. Quality matters.

**Before generating:**
1. Check provider: `grep -A5 'tts:' /root/.hermes/config.yaml`
2. If `tts.provider` = `edge` and recipient is Malay → warn user about quality
3. Edge TTS Malay (`ms-MY-OsmanNeural`) is robotic — acceptable only for
   internal drafts, NOT for sending to real people
4. Preferred providers for Malay: MiniMax > OpenAI > ElevenLabs > Edge

**If user says "teruk" or asks for better quality:**
- Check if MiniMax TTS is configured under `tts.minimax` in config.yaml
- If not configured: tell user "MiniMax TTS belum configure" — offer to fix
- Do NOT silently retry edge TTS multiple times — that wastes trust

**Pitfall:** Sending a robotic voice note to someone in distress destroys
credibility. Better to send clean text than bad audio.

## When to Use

- Medical negligence litigation decision
- Career/job change deliberation
- Relationship (marry/stay/leave)
- Investment/financial commitment
- Family dispute resolution

## When NOT to Use

- Technical decisions (use trade-off analysis instead)
- Decisions the user is making for themselves (different pattern)
- Crisis moments where action is needed (no time for deliberation)