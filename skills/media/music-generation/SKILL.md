---
name: music-generation
description: "Full music generation pipeline — concept → lyrics → cultural research → AI generation → delivery"
version: 1.1.0
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
  - cover song
  - cover version
  - cover
  - replicate song
  - exact song
  - versi
  - lagu asal
  - ai cover
---

# Music Generation Pipeline

End-to-end music generation across multiple engines. Use the right engine for the job.

---

## 1. Engine Selection

| Engine | Best for | Setup | Speed |
|---|---|---|---|
| **MuleRouter (MiniMax 2.5)** | **Default — no GPU, same key as chat** | `mulerouter-music.py` in Hermes scripts | ~60-120s |
| **MiniMax (mmx)** | Quick generation, any genre, lyrics + prompt | `mmx auth login --api-key <key>` — ready | ~90s per song |
| **HeartMuLa** | Open-source local generation, full control | Clone + venv + GPU (6GB+ VRAM) | ~4min on GPU |
| **AudioCraft/MusicGen** | Instrumental, ambient, text-to-music | pip install audiocraft | Varies |
| **Suno** | Highest quality vocals, complex arrangements | Web UI, no CLI | External |

**Default path:** MuleRouter MiniMax 2.5 (`mulerouter-music.py`) — same key as chat, no separate billing.

### MuleRouter MiniMax Music 2.5 Command

```bash
source /root/.secrets/kunci-mas.env && /root/HERMES/scripts/mulerouter-music.py \
  --prompt "Acoustic indie folk, gentle and reflective mood" \
  --lyrics "[Verse]\nSitting by the window\n[Chorus]\nTomorrow will bring a new day" \
  --output /tmp/song.mp3 \
  --timeout 180
```

**Key notes:**
- `--lyrics` (or `--lyrics-file`) is **required** — even for instrumental, pass `--lyrics "[Instrumental]"`
- Malay mode: `--malay` adds Nusantara genre cues to the prompt
- Supports [Verse], [Chorus], [Bridge], [Outro] lyric tags
- Full lyrics pipeline: research → write lyrics → generate → send via `MEDIA:`

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
   - **Instruments** — saluang, rebab, talempong, gandang, accordion for Minang; gambus, marwas for Zapin; gamelan for Javanese
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
- **"Same title, different song" trap** — one folk song title can index completely different versions with different languages, themes, and lyrics. E.g. "Kaparinyo" has a Minang folk version (Minang dialect, about farewell, refrains "Ondeh sayang" / "Yo malang") AND a separate Malay wedding version by S.M. Salim & Fazidah Joned (standard Malay, about bride and groom, refrain "Alah sayang"). Always identify WHICH version the user means — don't assume a title uniquely identifies a song in Nusantara folk. When in doubt, ask which artist/era.

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

### Somatic Parameter Injection (PULSE / SOUL / FLOW)

A proven prompt engineering pattern for culturally-specific traditional music. Instead of a flat list of descriptors, target three somatic layers that the generation model's latent space maps to distinct musical dimensions:

| Parameter | Target | What it controls |
|-----------|--------|-----------------|
| **PULSE** | Rhythm & tempo | The body — foot-tap, dance feel, percussion foundation |
| **SOUL** | Timbre & instrumentation | The heart — cultural resonance, instrument authenticity |
| **FLOW** | Structure & dynamics | The mind — cyclic patterns, entropy balance, engagement |

**Pattern:**
```
Traditional [Culture] [genre] folk song '[Song Name]'. Featuring [PULSE instruments]. [SOUL instruments]. [Mood], [cultural context], [tempo] traditional dance feel. [Production quality], [texture].
```

**Tested example (Kaparinyo, 2026-07-30):**
```
Traditional Minangkabau acoustic folk song 'Kaparinyo'. Featuring driving rebana drum rhythms, rhythmic talempong chimes, bright accordion, and soulful saluang bamboo flute. Joyful, rhythmic, Nusantara heritage, mid-tempo traditional dance feel. High fidelity, organic acoustic instruments, clear cultural texture.
```

**Key insight:** Naming the song explicitly in the prompt anchors the model's latent space better than just describing the style. The somatic param targets let you pack many authentic elements without triggering the "over-produced" degradation — because they're all coherent with the same cultural tradition, not competing production styles.

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
- **NUANCE:** A detailed prompt is fine when ALL elements are coherent within the same cultural tradition (see §4 Somatic Parameter Injection). The degradation happens when the prompt mixes competing production styles (e.g. "orchestral strings + 808 kick + gamelan + electric guitar") — not when it packs many authentic traditional elements together. Rule of thumb: if a human musician from that tradition would recognise every element, it's coherent; if you're mashing genres, it's over-produced.

## 6. Text-to-Music vs Voice Conversion — Expectation Setting

This is the most common expectation gap when users ask for AI music. Two fundamentally different technologies exist, and confusing them produces frustration.

### Text-to-Music Generation (What This Skill Covers)

| | |
|---|---|
| **How it works** | AI creates a **new song from scratch** — melody, chords, arrangement, vocals — based on a text prompt + lyrics |
| **Tools** | MuleRouter MiniMax Music 2.5, Suno, Udio, AudioCraft, HeartMuLa |
| **Output** | An **original** composition inspired by the prompt. It will NOT sound like an existing recording. |
| **Best for** | Creating original songs, demos, jingles, traditional-style music that doesn't exist yet |
| **Limitation** | Cannot replicate a specific artist's voice, melody, or arrangement |

### Voice Conversion (RVC — What YouTube Covers Use)

| | |
|---|---|
| **How it works** | Takes an **existing recording**, isolates the vocal (stem separation), and swaps the voice timbre via a trained model. The instrumental, melody, timing, and phrasing stay 100% intact. |
| **Tools** | RVC (open-source, needs GPU), Kits.ai (hosted, licensed voices), Lalal.ai / Moises (stem separation) |
| **Output** | An **exact cover** — same song, different voice. Sounds almost identical to the original because the instrumental is the original. |
| **Best for** | Making existing songs sound like they're sung by a different voice |
| **Limitation** | Needs the original audio file + a voice model. Not available via a single API call. |

### Decision Tree

When a user asks for a song:

```
User asks: "Make me [song name]"
├─ Is it an existing song they want to hear?
│  ├─ YES → Find the original recording and deliver the link/file
│  └─ NO → Continue
├─ Do they want an exact cover (same melody/arrangement, different voice)?
│  ├─ YES → Voice conversion route (RVC/Kits.ai) — requires GPU, setup, original audio
│  └─ NO → Continue
└─ Do they want a new original song in the style of [tradition/song]?
   └─ YES → Text-to-music generation (this skill) — research → prompt → lyrics → generate
```

### Pitfall — Expectation Mismatch

- **When a user says "make Kaparinyo"** — clarify: do you want the original recording, an AI cover (same melody, generated voice), or a new original in the style of that folk tradition?
- **Text-to-music generates NEW music** — it does not "play" an existing song. If the user wants the actual song, find the original recording. If they want an exact cover, that's the RVC path (requires separate setup).
- **Be upfront about the limitation** — don't let the user discover the gap after generation. Say clearly: "I can generate a new version in the style of the tradition, but it will not sound like the original recording by [artist]."
- **The "same title, different song" trap is amplified here** — a user might expect the exact melody of one version while you're generating lyrics from a different version. Always confirm which version/artist they mean.

### Voice Conversion Setup (for reference, not a turnkey Hermes tool)

Setting up RVC for exact covers requires:
1. **NVIDIA GPU** (or Google Colab/Hugging Face session)
2. **RVC WebUI** clone + install (~1hr setup)
3. **Voice model** — train from 5-10min of clean target audio, or download community models
4. **Stem separation** — Lalal.ai / Moises to isolate vocal from instrumental
5. **Conversion** — feed dry vocal into RVC, adjust pitch/index ratio, export
6. **Mixing** — EQ, de-ess, compress, blend with instrumental, reverb last

This is a separate toolchain from the text-to-music pipeline. Not available as a one-command Hermes action. For users who want this workflow, point them to Kits.ai (hosted, licensed voices) or the open-source RVC community.

## 7. AI Cover Pipeline (yt-dlp → Demucs → RVC → FFmpeg)

When the user wants an **exact AI cover** (same song, different voice) — not a new original generation — use this pipeline. It requires the original audio, stem separation, and voice conversion.

**Pipeline overview:**
```
Source Audio (YouTube)  →  Stem Separation (Demucs)  →  Voice Conversion (RVC)  →  Final Mix (FFmpeg)
```

### 7.1 Source Acquisition (yt-dlp)

Download the original track as lossless WAV:

```bash
yt-dlp -x --audio-format wav --audio-quality 0 -o "/tmp/original.wav" "YOUTUBE_URL"
```

**⚠️ YouTube Bot Detection (2026):** YouTube now blocks anonymous requests from data center IPs. If you get:
```
ERROR: Sign in to confirm you're not a bot
```
You need YouTube cookies from a logged-in browser. See `youtube-content` skill § "YouTube Auth" for the cookie export workflow. TL;DR:
```bash
yt-dlp -x --audio-format wav --audio-quality 0 -o "/tmp/original.wav" "YOUTUBE_URL" \
  --cookies /root/.secrets/yt-cookies.txt
```

**Tested approaches that fail without cookies:**
- `--extractor-args "youtube:player_client=web/android"` — blocked
- `--user-agent` spoofing — blocked
- `--throttled-rate`, `--sleep-requests` — blocked
- Invidious/Piped instances — all down or endpoint-disabled as of mid-2026
- MP3 aggregator sites (GudangLagu321, etc.) — JS-based wrappers over YouTube, same block

**Alternatives when YouTube is blocked:**
- Search for the track on SoundCloud, Archive.org, or Bandcamp
- Use the browser tool to play the video and capture audio (requires the video to be playable without sign-in)
- If the user already has the MP3, skip download

### 7.2 Stem Separation (Demucs)

**Installation:**
```bash
pip install demucs --break-system-packages
```

Demucs 4.x ships with `htdemucs` (Hybrid Transformer Demucs) — the default model.

**Usage:**
```bash
# Two-stem separation: vocals + everything else
demucs --two-stems vocals -n htdemucs /tmp/original.wav

# Output is in /tmp/separated/htdemucs/<filename>/
ls /tmp/separated/htdemucs/original/
# → vocals.wav  no_vocals.wav
```

**CPU vs GPU:**
- **No GPU:** Works on CPU. A 4:43 track takes ~3-4 minutes. A 30s test segment takes ~24s.
- **With GPU (CUDA):** Add `--device cuda` for ~5-10x speedup. Check with `python3 -c "import torch; print(torch.cuda.is_available())"`.

**Verification test:**
```bash
ffmpeg -i /tmp/original.mp3 -t 30 /tmp/test_short.wav -y
demucs --two-stems vocals -n htdemucs /tmp/test_short.wav
ffprobe /tmp/separated/htdemucs/test_short/vocals.wav
```

### 7.3 Voice Conversion (RVC)

**Requirements:**
- **NVIDIA GPU (CUDA)** — RVC is extremely slow on CPU (10-30x real-time).
- **Pre-trained voice model** (`.pth` file) — train your own (5-10min clean target audio) or download community models from HuggingFace.
- **Optional:** `.index` file for improved pronunciation/accent.

**rvc-python CLI:**
```bash
pip install rvc-python
python3 -m rvc_python cli \
  -i "/tmp/separated/htdemucs/original/vocals.wav" \
  -o "/tmp/converted_vocals.wav" \
  -mp "/root/HERMES/models/rvc/target_voice.pth" \
  -index "/root/HERMES/models/rvc/target_voice.index"
```

**Where to get voice models:**
- Train your own: https://github.com/RVC-Project/RVC
- HuggingFace: search "rvc model" for community models
- Cloud GPU: Google Colab + RVC for inference without local GPU

**⚠️ If no GPU and no model:** Skip this step. Use original vocals as-is for a "dry" mix.

### 7.4 Final Mix (FFmpeg)

Merge the instrumental stem with the (optionally converted) vocals:

```bash
ffmpeg -i "/tmp/separated/htdemucs/original/no_vocals.wav" \
       -i "/tmp/converted_vocals.wav" \
       -filter_complex "amix=inputs=2:duration=longest:dropout_transition=2" \
       -c:a pcm_s16le \
       "/tmp/Kaparinyo_AI_Cover.wav" -y
```

### 7.5 Pre-built Pipeline Script

A comprehensive bash script at:
**`/root/HERMES/scripts/kaparinyo-pipeline.sh`**

```bash
# Full pipeline with YouTube cookies
./kaparinyo-pipeline.sh --cookies /root/.secrets/yt-cookies.txt

# Skip download (use existing WAV)
./kaparinyo-pipeline.sh --skip-download

# Skip RVC (no voice model / no GPU)
./kaparinyo-pipeline.sh --skip-download --skip-rvc
```

The script handles: cookie management, CPU/GPU auto-detection, model existence checks, FFmpeg mixing, and file info output.

### 7.6 Decision Tree for AI Cover Requests

```
User: "Make an AI cover of [song]"
├─ Do we have the original audio?
│  ├─ NO → Can we download it?
│  │  ├─ YES (YouTube cookies) → yt-dlp
│  │  └─ NO → Tell user: need source audio
│  └─ YES → Proceed
├─ Do we have a target voice model?
│  ├─ NO → Tell user: need RVC .pth model
│  └─ YES → Proceed
├─ Do we have GPU?
│  ├─ NO → Warn: RVC will be slow, consider --skip-rvc
│  └─ YES → Proceed
└─ Do we have Demucs?
   ├─ NO → pip install
   └─ YES → Run pipeline
```

### 7.7 Pitfalls

- **YouTube bot detection is systemic** — not fixable by tweaking flags. Only reliable bypass is cookies from a logged-in browser.
- **Demucs on CPU is slow but viable** — ~4 min for a 4:43 track. Acceptable for one-off jobs.
- **RVC without GPU is impractical** — warn the user upfront. Skip the step if no GPU.
- **No community models for niche artists** — Malay 60s/70s artists (S.M. Salim, Saloma) have no pre-trained RVC models. Training requires 5-10min clean vocal audio.
- **WAV files are large** — a 4:43 track at 44.1kHz/16-bit stereo is ~48MB. Budget ~500MB for the full pipeline with intermediates.
- **Copyright considerations** — W_scar at 888 prohibits YouTube dataset extraction for training. One-off download for personal use is generally tolerated, but distributing separated stems or converted covers may infringe copyright. Inform the user.

## 8. References

- `references/minang-lyrics-bank.md` — Authentic Minangkabau folk lyrics collected during sessions (kaparinyo, etc.)
- `references/malay-vocal-personas.md` — Malay artist vocal persona prompts for MiniMax/Suno
- `references/engine-comparison.md` — Quality comparison across engines for different genres
