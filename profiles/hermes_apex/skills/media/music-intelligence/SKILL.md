---
name: music-intelligence
description: "Governed music generation + somatic scoring pipeline. Generate music via MiniMax, analyze with DSP, score against cultural manifolds, iterate. Covers Nusantara folk (Minang, Zapin, Asli, Joget) and generic genres."
version: 1.0.0
tags: [music, audio, generation, somatic, scoring, cultural-manifold, nusantara, minmax, dsp]
metadata:
  hermes:
    tags: [music, audio, generation, somatic, scoring, cultural-manifold, nusantara]
    related_skills: [songwriting-and-ai-music, heartmula, minimax-cli, audiocraft-audio-generation]
---

# Music Intelligence — Governed Generation + Somatic Scoring

End-to-end pipeline: **Generate → Analyze → Score → Iterate** with cultural manifold constraints.

## When to Use

- User wants music generated with cultural/heritage constraints
- User wants to analyze audio for coherence, tension, paradox
- User wants to compare multiple generations objectively
- User asks about "somatic scoring," "cultural manifold," or "music governance"
- User asks to build music analysis into arifOS/WEALTH/WELL

## Architecture

```
Prompt + Cultural Manifold
         │
         ▼
    mmx music generate  (MiniMax music-2.6)
         │
         ▼
      Audio MP3
         │
         ▼
    Somatic Scoring Engine (scipy + numpy DSP)
         │
         ▼
    4-axis score: Temporal | Tension/Release | Paradox | Embodied
         │
         ▼
    Governance Verdict: SEAL | SABAR | HOLD
         │
         ▼
    Iterate or Deliver
```

## Step 1: Generate Music

Use `mmx music generate` (MiniMax CLI). See `minimax-cli` skill for auth/setup.

```bash
mmx music generate \
  --prompt "detailed style description with instruments, rhythm, mood, tempo" \
  --lyrics-file /tmp/lyrics.txt \
  --out /tmp/output.mp3 \
  --timeout 300
```

### Prompt Engineering for Cultural Music

**Generic prompt** → generic pop. **Heritage prompt** → authentic folk.

Prompt formula:
```
[region] [genre] [era/lineage], [vocal style], [instruments], 
[rhythm pattern], [scale type], [mood/atmosphere], [tempo BPM]
```

Example (Minangkabau Inang):
```
Traditional Minangkabau folk song reviving 1960s Gumarang era, 
female vocalist with warm bright controlled vibrato, 
saluang bamboo flute, rebab fiddle, talempong metallophone, gandang drums, 
inang joget dance rhythm starting slow ceremonial then rising, 
pentatonic Minang melodic phrases with ornamental trills, 
nostalgic affectionate village celebration, 
acoustic organic warm vintage, no electronic instruments, 95 BPM
```

### Lyrics

Use traditional dialect/proverbs when targeting heritage music. For Minang: "ondeh sayang," "yo malang," "kaparinyo," pantun structure. Research actual lyrics before writing — don't invent fake "traditional" lyrics.

## Step 2: Analyze Audio (DSP)

**CRITICAL: Do NOT use librosa `beat_track`, `chroma_*`, or `tonnetz`** — they segfault on numpy 2.4.6 (as of 2026-07-11). Use **scipy + numpy directly**.

### Working DSP Pipeline (scipy-only)

```python
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft as scipy_stft, find_peaks
from scipy.ndimage import uniform_filter1d
import subprocess

def load_audio(path, sr=22050):
    """Load any audio via ffmpeg → WAV → scipy (bypass librosa)"""
    tmp = "/tmp/_somatic_tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-i", path, "-ar", str(sr), "-ac", "1",
                     "-acodec", "pcm_s16le", tmp], capture_output=True, timeout=60)
    rate, data = wavfile.read(tmp)
    y = data.astype(np.float32) / 32768.0
    os.remove(tmp)
    return y, rate
```

### Available Features (scipy-only, no segfault)

| Feature | Method | Use for |
|---|---|---|
| STFT magnitude | `scipy.signal.stft` | All spectral features |
| RMS envelope | manual frame loop | Dynamics, phrasing |
| Spectral centroid | weighted mean of STFT | Timbre |
| Spectral bandwidth | weighted std of STFT | Harmonic richness |
| Spectral flatness | geometric/arithmetic mean ratio | Tonality vs noise |
| Spectral flux | frame-to-frame STFT diff | Onset detection |
| Spectral contrast | per-band percentile range | Paradox/polyphony |
| MFCC | DCT of log-mel approximation | Timbre fingerprint |
| Zero crossing rate | sign changes per frame | Roughness |
| Temporal autocorrelation | autocorrelation of flux | Tempo estimation |

### Features to AVOID (segfault on current numpy/librosa combo)

- `librosa.beat.beat_track` — segfault
- `librosa.feature.chroma_*` — segfault
- `librosa.feature.tonnetz` — segfault
- Calling too many librosa functions sequentially — accumulated memory corruption

## Step 3: Somatic Scoring (4 Inputs)

### Input A: Temporal Stability (weight: 0.25)
- **Onset CV**: coefficient of variation of spectral flux (lower = steadier)
- **Microtiming deviation**: IOI std/mean from onset peaks (lower = more regular)
- **Tempo autocorrelation**: peak in AC at musical lag range
- **BPM check**: in range [80, 130] for folk music

### Input B: Tension/Release (weight: 0.25)
- **Dynamic humanity**: RMS entropy vs ideal (~3.0 for human-like)
- **Tension cycle rate**: peaks in smoothed spectral flux per 10 seconds
- **Tension balance**: mean tension near 0.3 (not flat, not chaotic)

### Input C: Paradox Persistence (weight: 0.25)
- **Spectral contrast variance**: across 6 frequency bands (higher = more polyphonic)
- **MFCC delta entropy**: timbre change rate (higher = more evolving)
- Product normalized to [0, 1]

### Input D: Embodied Coherence (weight: 0.25)
- **Phrase regularity**: RMS zero-crossings vs expected (~2/sec for songs)
- **Timbre coherence**: 1/(1+centroid_CV) (stable timbre = higher)
- **Bandwidth score**: distance from 2000Hz ideal
- **Tonality**: 1 - flatness/0.4 (tonal = higher)

### Composite & Verdict

```python
somatic = 0.25*temporal + 0.25*tension + 0.25*paradox + 0.25*embodied

if somatic >= 0.6 and manifold_pass >= 3/4:
    verdict = "SEAL"
elif somatic >= 0.4:
    verdict = "SABAR"
else:
    verdict = "HOLD"
```

## Step 4: Cultural Manifold

JSON schema at `/root/arifos/schemas/cultural_manifold_minang_inang.json`.

Fields:
- `identity`: region, genre, heritage_lineage
- `structural_priors`: tempo_range, section_structure, call_and_response
- `harmonic_constraints`: scale_type, allowed_degrees, key_stability
- `timbre_palette`: core_instruments, forbidden_instruments
- `lyric_constraints`: structure, required_refrains, dialect
- `amanah_filters`: must_not, must_include, seal_requirements
- `evaluation_thresholds`: per-metric minimums

### Manifold Checks (4 binary tests)

```python
checks = {
    "tempo_in_range": 80 <= bpm <= 130,
    "not_overcompressed": onset_cv > 0.1,
    "not_too_flat": flatness < 0.4,
    "has_dynamics": rms_entropy > 1.5,
}
```

## Pitfalls

1. **Don't use librosa for DSP** — scipy+numpy works, librosa segfaults on current stack
2. **MP3 loudness normalization** — all MiniMax tracks come out ~-10 to -12 LUFS, 256kbps. The loudness norm check from ffmpeg is NOT differentiating — use spectral features instead
3. **BPM double-time** — onset peak detection often picks up half-beat intervals. If BPM > 180, halve it
4. **Prompt specificity ≠ better music** — tested: detailed Siti-style prompt produced WORSE temporal stability (0.392) than simpler authentic Minang prompt (0.624). Don't over-specify
5. **No GPU = no HeartMuLa/AudioCraft** — use mmx-cli (MiniMax API) for generation
6. **Segmentation fault accumulation** — even working librosa features crash after ~6 sequential calls. Use one scipy-based script per analysis run

## Existing Paradox Engine (A-FORGE) — Don't Rebuild, Wire It

**A-FORGE already has a full Paradox Engine on disk:**

| File | Lines | Content |
|---|---|---|
| `/root/A-FORGE/paradox-engine/models.py` | 223 | 16-dim somatic vector, MotifState, ParadoxState, SomaticSnapshot, `to_agent_context()` |
| `/root/A-FORGE/paradox-engine/engine.py` | 520 | ParadoxEngine core: tick, detect contradictions, maintain, block resolution |
| `/root/A-FORGE/paradox-engine/registry.py` | 893 | Motif/cultural manifold registry |

16-dim somatic vector: valence, arousal, tension, depth, duration_feel, density, warmth, weight, direction, stability, spiritual, cultural_weight, paradox_affinity, breath, silence, emergence.

arifOS kernel also has `arifosmcp/core/enforcement/somatic_loop.py` (139 lines) — machine telemetry → NOMINAL/STRESSED/CRITICAL, already wired into `arif_judge`.

**Gap:** Components exist but are NOT connected. Wiring task: A-FORGE engine → arifOS kernel → WELL somatic tools → music pipeline.

## Files

| File | Path |
|---|---|
| Somatic Engine | `/root/arifos/forge/music-intelligence/somatic_engine.py` |
| Cultural Manifold | `/root/arifos/forge/music-intelligence/cultural_manifold_minang_inang.json` |
| Analysis Report | `/root/arifos/forge/music-intelligence/report.json` |
| Paradox Engine (A-FORGE) | `/root/A-FORGE/paradox-engine/{models,engine,registry}.py` |
| Somatic Loop (arifOS) | `/root/arifOS/arifosmcp/core/enforcement/somatic_loop.py` |

## Results So Far (2026-07-11)

3 Kaparinyo tracks analyzed. **Winner: v2 Authentic Minang (SABAR 0.560)**.

| Track | BPM | TEMP | T/R | PARADOX | EMBODIED | SOMATIC |
|---|---|---|---|---|---|---|
| v1 Generic Malay | 118 | 0.513 | 0.524 | 0.445 | 0.718 | 0.550 |
| v2 Authentic Minang | 118 | 0.624 | 0.545 | 0.421 | 0.649 | 0.560 |
| v4 Siti Style | 144 | 0.392 | 0.530 | 0.367 | 0.720 | 0.502 |

Key finding: authentic lyrics + simpler prompt > detailed heritage prompt.
