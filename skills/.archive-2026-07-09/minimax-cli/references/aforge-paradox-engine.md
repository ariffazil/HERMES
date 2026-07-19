# A-FORGE Paradox Engine — Pre-Existing Architecture

> Discovered 2026-07-11. A-FORGE already has a Paradox Engine at `paradox-engine/models.py`.

## What Exists

**File:** `/root/A-FORGE/paradox-engine/models.py` (223 lines)

### 16-Dim Somatic Feature Vector

| Dim | Label | Range | Meaning |
|---|---|---|---|
| 0 | valence | [-1, +1] | negative ↔ positive |
| 1 | arousal | [0, 1] | calm ↔ activated |
| 2 | tension | [0, 1] | relaxed ↔ taut |
| 3 | depth | [0, 1] | surface ↔ profound |
| 4 | duration_feel | [0, 1] | momentary ↔ enduring |
| 5 | density | [0, 1] | sparse ↔ dense |
| 6 | warmth | [0, 1] | cold ↔ warm |
| 7 | weight | [0, 1] | light ↔ heavy |
| 8 | direction | [0, 1] | inward ↔ outward |
| 9 | stability | [0, 1] | unstable ↔ grounded |
| 10 | spiritual | [0, 1] | secular ↔ sacred |
| 11 | cultural_weight | [0, 1] | universal ↔ culturally-specific |
| 12 | paradox_affinity | [0, 1] | resolves-easily ↔ holds-tension |
| 13 | breath | [0, 1] | held ↔ flowing |
| 14 | silence | [0, 1] | filled ↔ quiet |
| 15 | emergence | [0, 1] | known ↔ arising |

### ContradictionType Enum

- `CONTRADICTORY` — oppose each other
- `COMPLEMENTARY` — coexist in Melayu somatic space (sedih + syukur)
- `NEUTRAL` — no strong relation
- `PARADOXICAL` — can sustain tension (emergence candidate)

### Key Classes

- **MotifState** — somatic_vector (16-dim) + semantic_embedding (384-dim) + cultural_origin + decay/boost
- **ParadoxState** — tension, duration, resolution_blocked, emerged_motif, peak_tension, maturation_candidate
- **SomaticSnapshot** — tick-level capture with `to_agent_context()` → LLM-readable text

### GENESIS Documents

- `GENESIS/006_PETRONAS_PARADOX.md` — PETRONAS case study as paradox exemplar
- `GENESIS/008_NARRATIVE_TENSION_KERNEL.md` — 7 tension classes for text analysis (PROMISE_VS_OUTCOME, VOICE_ASYMMETRY, etc.)

## Integration With music-eval/

The music-eval pipeline (at `/root/music-eval/`) provides signal observers that feed INTO the A-FORGE somatic model:

```
Audio DSP (librosa) → MotifState (16-dim) → ParadoxEngine tick → SomaticSnapshot → LLM context
Telegram topology  → MotifState (16-dim) ↗
Session events     → MotifState (16-dim) ↗
```

## What's Missing (as of 2026-07-11)

1. The A-FORGE models.py has dataclasses but no tick loop implementation — `paradox_engine_v2.py` in music-eval has the tick loop
2. Signal observers (Telegram, audio, session) need to output 16-dim vectors, not 13-dim MFCC
3. The `SomaticSnapshot.to_agent_context()` method is the bridge to LLM — needs wiring to arifOS kernel
4. Cultural manifold (Minang, Zapin, Asli, Joget) needs mapping to 16-dim somatic space
