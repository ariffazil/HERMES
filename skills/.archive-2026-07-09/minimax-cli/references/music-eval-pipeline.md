# Music Evaluation Pipeline — /root/music-eval/

> Built 2026-07-11. Complete toolkit for evaluating AI-generated music against genre profiles.

## Architecture

```
Audio file → evaluator.py (genre scoring)
           → somatic_scoring.py (4-input embodiment scoring)
           → paradox_engine_v2.py (contradiction detection + resolution blocking)
           → motif_memory.py (chroma-based motif tracking + callbacks)
           → signal_observer.py (Telegram message → MotifState mapper)
```

## Files

| File | Purpose | Status |
|---|---|---|
| `evaluator.py` | Genre-based scoring (PASS/RETUNE/REJECT) against 5 profiles | ✅ Working |
| `cli.py` | CLI: evaluate, generate, loop (generate→score→regenerate) | ✅ Working |
| `profiles.yaml` | Genre profiles: minang_inang, zapin, asli, joget, generic | ✅ Working |
| `motif_state.py` | MotifState, ParadoxState, SomaticTick dataclasses | ✅ Working |
| `paradox_engine_v2.py` | Tick-based paradox engine with resolution blocking + maturation | ✅ Working |
| `signal_observer.py` | Telegram message topology → MotifState mapper | ✅ Working |
| `motif_memory.py` | Chroma-based motif fingerprinting + callback detection | ✅ Working |
| `somatic_scoring.py` | 4-input DSP embodiment scoring | ✅ Built (segfaults on some librosa features) |
| `paradox_engine.py` | v1 DSP-only paradox detection (MFCC clustering) | ✅ Working |

## CLI Usage

```bash
# Evaluate a track against a genre
python3 cli.py evaluate /tmp/song.mp3 --genre minang_inang

# Generate + evaluate (calls mmx-cli then scores)
python3 cli.py generate --prompt-file tags.txt --lyrics-file lyrics.txt --genre minang_inang

# Generate → evaluate → regenerate if REJECT → return best
python3 cli.py loop --prompt-file tags.txt --lyrics-file lyrics.txt --genre minang_inang --max-attempts 3
```

## Genre Profiles (profiles.yaml)

| Genre | Tempo | Brightness | Entropy | Dynamics | Noisiness | Onset |
|---|---|---|---|---|---|---|
| minang_inang | 80-110 | 1800-2800 | 6.5-8.0 | 0.15-0.45 | 0.05-0.15 | 0.3-1.2 |
| zapin | 100-130 | 2000-3200 | 6.8-8.2 | 0.20-0.50 | 0.06-0.18 | 0.5-1.5 |
| asli | 70-100 | 1500-2500 | 6.0-7.5 | 0.10-0.35 | 0.04-0.12 | 0.2-1.0 |
| joget | 110-140 | 2200-3500 | 7.0-8.5 | 0.25-0.55 | 0.07-0.20 | 0.6-1.8 |
| generic | 60-180 | 1000-5000 | 5.5-8.5 | 0.05-0.60 | 0.03-0.25 | 0.1-2.0 |

## Proven Results

| Track | Genre | Verdict | Score |
|---|---|---|---|
| kaparinyo.mp3 (generic tags) | minang_inang | RETUNE | 50% (tempo too fast) |
| kaparinyo_minang.mp3 (Minang tags) | minang_inang | PASS | 83% (5/6 metrics in range) |

## A-FORGE Paradox Engine (pre-existing)

A-FORGE already has `paradox-engine/models.py` (223 lines) with:
- **16-dim somatic feature vector** (valence, arousal, tension, depth, warmth, spiritual, paradox_affinity, breath, silence, emergence, etc.)
- **ContradictionType enum**: CONTRADICTORY | COMPLEMENTARY | NEUTRAL | PARADOXICAL
- **Hybrid approach**: somatic_vector + semantic_embedding
- **SomaticSnapshot.to_agent_context()**: converts state to LLM-readable text
- **Narrative Tension Kernel** (GENESIS/008): 7 tension classes for text analysis

### Integration Path

```
A-FORGE models.py (16-dim somatic model) ← THE SUBSTRATE
signal_observer.py (Telegram → MotifState) ← SIGNAL SOURCE 1
audio_to_motifs() (audio DSP → MotifState) ← SIGNAL SOURCE 2
evaluator.py (genre compliance) ← SIGNAL SOURCE 3
         ↓ feeds into
Paradox Engine tick loop ← THE LOAD-BEARING MODULE
         ↓ outputs
SomaticSnapshot.to_agent_context() ← LLM-READABLE STATE
         ↓ governed by
arifOS F1-F13 + arif_judge ← CONSTITUTIONAL LAYER
```
