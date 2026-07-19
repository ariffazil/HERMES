# Rasa Witness Framework — Telemetry vs Human Meaning

> Emerged from ChatGPT critique of Hermes' rasa/telemetry conflation (2026-07-12).
> Implemented: `/root/WELL/governance/RASA_WITNESS_CONTRACT.md`
> Runtime: `/root/WELL/gate/rasa_witness.py`
> Tests: `/root/WELL/tests/test_rasa_witness.py` (30/30 pass)
> VAULT999: Seal #60 (2026-07-12)

## The Category Error (do not repeat)

**Wrong:** "Humans bridge rasa through behavior. AI bridges through data. Same inference problem, different inputs."

**Why it's wrong:** Same epistemic structure (infer from signals → uncertain model), but different ontological relationship to being. Humans share embodiment, comparable nervous systems, reciprocal vulnerability. AI has sensor values and statistical associations. "Same inference problem" ≠ "same kind of knower."

## The Three Layers (always separate)

| Layer | What it is | What it can do |
|-------|-----------|---------------|
| **Telemetry** | HRV, sleep, stress, energy measurements | Observe physiology. Nothing more. |
| **State estimation** | Probabilistic latent state (arousal, fatigue) | Estimate with uncertainty. Every signal has multiple explanations. |
| **Rasa** | First-person felt meaning | Only the human can assign this. Freddy T-Rex example: sensor detects arousal reduction near object, cannot derive WHY it feels safe. |

## The Seven Invariants (RWC-1 through RWC-7)

1. **Self-report has semantic sovereignty** — human defines meaning, telemetry supplements
2. **Telemetry is non-specific** — every signal retains alternative explanations
3. **State is not cause** — "elevated arousal" is admissible, "you are afraid of X" requires human confirmation
4. **Observation is not niat** — no biometric reveals sincerity, morality, or hidden motive
5. **Intervention follows uncertainty** — higher uncertainty → gentler language, fewer assumptions
6. **Output is posture, not diagnosis** — `reduce_load`, `ask_permission`, `defer_decision`, not "you are anxious"
7. **Human can refuse interpretation** — refusal is not evidence of concealment

## Interaction Posture States

| Posture | When |
|---------|------|
| `normal` | No divergence detected |
| `reduce_load` | Lower cognitive demand |
| `ask_permission` | Seek consent before continuing |
| `defer_decision` | No irreversible actions |
| `suggest_rest_or_support` | Recommend, don't declare |
| `surface_mismatch_silently` | Log + adjust, don't announce |

## Correct vs Wrong Output

**Wrong:** "Your HRV proves you are anxious despite saying you are okay."
**Correct:** "Your physiological load appears elevated relative to baseline. That can have many causes. You reported feeling okay, so I will not assign a meaning to it."

## What WELL Actually Is

Not a qualia detector. Not an empathy simulator. Not a biometric lie detector.

WELL is a: **somatic context and dignity-preserving interaction regulator.**

Purpose: notice the ground may be moving, avoid building heavier structures during instability, ask the person what is happening, never confuse the seismograph with the earth.

## Implementation Details

**Runtime module:** `gate/rasa_witness.py` (350 lines)
- `BiometricObservation` dataclass with TTL, quality, deviation_sigma
- `SelfReport` with refusal detection (RWC-7)
- `MismatchResult` with posture recommendation
- `detect_mismatch()` — core evaluation
- `scan_prohibited_conclusions()` — regex scanner for diagnostic language
- `enforce_posture_language()` — replaces diagnostic text with posture-appropriate alternatives
- `rasa_witness_gate()` — reads state.json, constructs observations, evaluates

**Gate integration:** `well_gate.py` `reflect_readiness()` now returns 5-tuple (status, msg, score, violations, rasa_witness). Backward-compatible — 5th element is new.

**Prohibited conclusion patterns:**
- "you are anxious/afraid/scared/depressed/hiding/lying"
- "your body says/telemetry proves/reveals"
- "the system understands/knows/feels"
- "hidden motive/concealing/repressing"

**Test coverage:** 30 tests across 8 classes:
- RWC-1: Self-report sovereignty (2 tests)
- RWC-2: Non-specific telemetry (2 tests)
- RWC-3: State ≠ cause (5 tests)
- RWC-4: Observation ≠ niat (2 tests)
- RWC-5: Uncertainty-driven intervention (5 tests)
- RWC-6: Posture not diagnosis (3 tests)
- RWC-7: Human refusal (2 tests)
- Integration: well_gate.py (3 tests)
- Edge cases (6 tests)
