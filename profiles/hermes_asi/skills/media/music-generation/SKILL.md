---
name: music-generation
description: "Full music generation pipeline — concept → lyrics → cultural research → AI generation → delivery. Covers MiniMax (mmx music generate), HeartMuLa, AudioCraft, and Suno prompt crafting. Includes the critical cultural authenticity workflow for traditional/folklore songs."
version: 1.0.0
tags: [music, audio, generation, minimax, heartmula, audiocraft, suno, folk, traditional, lyrics, kaparinyo]
metadata:
  hermes:
    tags: [music, audio, generation, minimax, heartmula, audiocraft, suno, folk, traditional, lyrics]
    related_skills: [minimax-cli, heartmula, songwriting-and-ai-music, audiocraft-audio-generation, audio-analysis]
triggers:
  - make a song
  - generate music
  - write a song about
  - buat lagu
  - create music
  - folk song
  - traditional song
  - lagu tradisional
  - zamani style
  - malay ballad
  - lagu melayu
  - pop melayu
  - buat lagu untuk
---

# Music Generation Pipeline

End-to-end music generation across multiple engines. Use the right engine for the job.

---

## 1. Engine Selection

| Engine | Best for | Setup | Speed |
|---|---|---|---|
| **MiniMax (mmx)** | Quick generation, any genre, lyrics + prompt | `mmx auth login --api-key <key>` — ready | ~90s per song |
| **HeartMuLa** | Open-source local generation, full control | Clone + venv + GPU (6GB+ VRAM) | ~4min on GPU |
| **AudioCraft/MusicGen** | Instrumental, ambient, text-to-music | pip install audiocraft | Varies |
| **Suno** | Highest quality vocals, complex arrangements | Web UI, no CLI | External |

**Default path:** MiniMax (`mmx music generate`) — fastest, no GPU needed, good quality.

### MiniMax Music Command

```bash
cd /tmp && mmx music generate \
  --prompt "style description with instruments, mood, tempo, vocal style" \
  --lyrics-file /tmp/lyrics.txt \
  --out /tmp/output.mp3 \
  --timeout 300
```

- Model: music-2.6 (auto-selected)
- Output: MP3, 256kbps, 44.1kHz stereo
- Lyrics file: plain text with [Verse], [Chorus], [Bridge], [Outro] structural tags
- No `--lyrics-file` = instrumental only

---

## 2. Cultural Authenticity Workflow (CRITICAL for Traditional Songs)

When the user asks for a traditional, folklore, or culturally specific song — **research before generating**. Generic lyrics with the cultural keyword sprinkled in will be rejected.

### Step-by-Step

1. **Identify the actual origin** — "kaparinyo" is Minangkabau, not generic Malay. "Zapin" is Arab-Malay. "Dikir barat" is Kelantanese. Know the specific tradition.

2. **Find authentic lyrics** — search for "[song name] lirik asli" / "original lyrics" / "traditional lyrics." Look for:
   - Archival sites (laguminanglamo.wordpress.com for Minang)
   - Spotify/YouTube for recorded versions by traditional artists
   - Ethnomusicology sources
   - The OG artists (Gumarang 1960s, Elly Kasim 1972 for kaparinyo)

3. **Identify signature elements** — every folk tradition has:
   - **Signature refrains** — "ondeh sayang" / "yo malang" for Minang
   - **Vocal style** — call-and-response, melismatic, communal
   - **Instruments** — saluang, rebab, talempong, gandang for Minang; gambus, marwas for Zapin; gamelan for Javanese
   - **Rhythm type** — inang, joget, asli, zapin, keroncong

4. **Style the AI prompt with specifics:**
   ```
   BAD:  "traditional Malay folk song"
   GOOD: "Minangkabau inang folk, saluang bamboo flute, rebab fiddle,
          gandang drums, talempong metallophone, call-and-response
          vocals, Minang dialect, slow graceful intro building to
          lively dance, acoustic organic, vintage recording quality,
          95 BPM, no modern pop production"
   ```

5. **Use real lyrics as the base** — don't rewrite folklore. Arrange traditional verses (in original dialect) into song structure. Add pantun or traditional poetry for bridges.

6. **Iterate** — first gen may be too modern. Re-prompt with stronger traditional cues. Exclude modern production terms explicitly.

### Pitfalls

- **Don't assume all "Malay folk" is the same** — Minang, Javanese, Bugis, Malay, Batak each have distinct musical traditions, instruments, and rhythms.
- **Don't translate dialect to standard BM** — the dialect IS the authenticity. "Babuai adiak" ≠ "selamat tinggal kawan."
- **AI models default to pop** — you must explicitly push toward traditional sound with instrument names and "acoustic organic" / "vintage" / "no modern pop production."
- **Repetition is tradition** — folk songs repeat the hook in every verse. Don't over-vary.
- **Pantun structure** — traditional Malay/Minang lyrics often use pantun (ABAB quatrain form). Preserve this.

---

## 3. Songwriting Structure Reference

Common skeletons — mix, modify, or throw out as needed:

```
ABABCB  Verse/Chorus/Verse/Chorus/Bridge/Chorus    (most pop/rock)
AABA    Verse/Verse/Bridge/Verse (refrain-based)    (jazz standards, ballads)
ABAB    Verse/Chorus alternating                    (simple, direct)
AAA     Verse/Verse/Verse (strophic, no chorus)     (folk, storytelling)
```

**Folk songs typically use AAA** — repetitive verse structure with a recurring hook/refrain. Don't force pop structure onto folk material.

### Lyric Bracket Tags (for AI engines)

```
[Intro] [Verse] [Verse 1] [Pre-Chorus] [Chorus]
[Post-Chorus] [Hook] [Bridge] [Interlude]
[Instrumental] [Instrumental Break] [Guitar Solo]
[Breakdown] [Build-up] [Outro] [Silence] [End]
```

Vocal performance: `[Whispered]` `[Spoken Word]` `[Belted]` `[Soulful]` `[Harmonies]`

---

## 4. Prompt Engineering for Music AI

### Style Description Formula
`Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics + BPM`

### Vocal Persona (for Suno/MiniMax)
Describe the VOICE, not just gender:
```
"A weathered village elder with a warm baritone, leading a communal
 sing-along, call-and-response style, starting intimate and building
 to joyful celebration"
```

### Phonetic Tricks (for AI singers)
- Spell words as they SOUND: "through" → "thru"
- Proper nouns have highest failure rate — test in short clip first
- Hyphenate to guide syllables: "Ka-pa-ri-nyo"
- ALL CAPS = louder; vowel extension = sustained note: "lo-o-o-ove"
- Spell out numbers: "24/7" → "twenty four seven"

---

## 5. Malay Pop Ballad Generation

When the user asks for a Malay pop song (e.g. "buat lagu Zamani style", "lagu Melayu", "pop melayu"), use the **ABABCB** structure (verse/chorus/verse/chorus/bridge/chorus) — NOT the AAA folk structure. Key differences from traditional folk:

### Malay Ballad Prompt Formula
```
[Genre] emotional pop ballad, powerful male/female vocalist with
rich warm vibrato and melismatic delivery, piano-driven arrangement,
lush string orchestra, gentle acoustic guitar, soft drums building
to dramatic crescendo, 1990s Malaysian pop ballad era, heartfelt
romantic [mood], slow tempo [68-85] BPM building to [80-95] BPM
on chorus, warm analog production, soaring vocal climax on final
chorus, acoustic organic warm, no electronic sounds
```

### Vocal Persona Reference
See `references/malay-vocal-personas.md` for artist-specific prompt snippets (Zamani, M. Nasir, Siti Nurhaliza, Awie, Ella, etc.)

### Lyrics Style
- BM (Bahasa Melayu) standard — not dialect
- Emotional, romantic, longing themes dominate
- Simple vocabulary, deep feeling — "Kembalilah sayang jangan kau pergi lagi"
- [Pre-Chorus] builds tension before the hook
- Bridge = most emotional moment, often spoken/whispered
- Outro = repeat chorus hook with ad-libs ("ooh", "yeah", artist name)

### Pitfall
- Don't over-produce the prompt. Tested: detailed Siti-style prompt produced WORSE temporal stability (0.392) than simpler authentic Minang prompt (0.624). Keep prompt focused on 3-4 key elements, not 15.

## 6. References

- `references/minang-lyrics-bank.md` — Authentic Minangkabau folk lyrics collected during sessions (kaparinyo, etc.)
- `references/malay-vocal-personas.md` — Malay artist vocal persona prompts for MiniMax/Suno
- `references/engine-comparison.md` — Quality comparison across engines for different genres
