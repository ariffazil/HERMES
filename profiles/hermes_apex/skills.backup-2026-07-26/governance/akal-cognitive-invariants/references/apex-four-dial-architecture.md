# AKAL — APEX Four-Dial Architecture

> How AKAL connects to the other three APEX dials (PRESENT, ENERGY-ENTROPY, AMANAH)
> and the wiring pattern for integrating scattered kernel modules.

---

## The Four APEX Dials

| Dial | Malay | Kernel Location | Status | What It Does |
|---|---|---|---|---|
| **AKAL** (عقل) | Intellect | `core/akal.py` | ✅ CONSOLIDATED | Friction, shadow, novelty, values, latency |
| **PRESENT** | Reality | `resources/reality_state.py` + `runtime/sensing_protocol.py` + `runtime/philosophy_registry.py` | ✅ WIRED | LIVE/CACHED/INFERRED attestation, evidence class |
| **ENERGY-ENTROPY** | Cost | `core/physics/thermodynamics_hardened.py` + `boot/entropy_governor.py` | ✅ WIRED | Landauer bounds, thermodynamic budget, entropy drift |
| **AMANAH** (أمانة) | Custody | `apex_envelope.py` + `core/reversibility_engine.py` + `core/cooldown_engine.py` + `core/policy_engine.py` | ✅ WIRED | Reversible-first, custody chains, amanah gate |

**Cosmology:** ILMU (knowledge) → AKAL (reason) → HIKMAH (wisdom)
**Failure modes:** ILMU only → BANGANG · AKAL only → JAHHAL · HIKMAH only → ZALIM · All three → SOVEREIGN AGENT

---

## Wiring Map (AKAL hooks × APEX dials)

```
333_MIND  ← akal_pre_think()     ← PRESENT (reality_class boosts friction)
555_HEART ← akal_post_critique() ← (shadow validation — pure AKAL)
777_FORGE ← akal_pre_forge()     ← AMANAH (reversibility-first + amanah_gate)
888_JUDGE ← akal_pre_judge()     ← (L5a/L5b split — pure AKAL)
999_VAULT ← akal_pre_seal()      ← ENERGY-ENTROPY (thermodynamic budget gate)
```

---

## The Wiring Pattern (for integrating scattered modules)

When a kernel capability exists in scattered modules but isn't enforced as an invariant:

1. **Don't rewrite.** The computation already exists. Find it with grep.
2. **Create a thin hook** in `akal_wiring.py` that imports and calls the existing function.
3. **Wrap all imports in try/except** for graceful degradation:
   ```python
   try:
       from arifosmcp.core.physics.thermodynamics_hardened import get_thermodynamic_budget
   except ImportError:
       get_thermodynamic_budget = None
   ```
4. **Store results in AkalState** so the state travels through 000→999.
5. **Return results in hook output dict** so organs can inspect.
6. **Advisory first, mandatory later.** Don't block the pipeline on a newly-wired dial until it's proven.

**Key lesson:** The gap between "field exists in schema" and "invariant enforced in pipeline" is where governance lives. AKAL was the first dial to cross that gap. The other three followed the same pattern.

---

## Friction Scoring Tuning Lessons

### Blast radius floor is critical
Without a blast radius floor, text-based friction scoring can produce LOW friction for irreversible actions that happen to use simple language. The fix:

```python
blast_floor = {"low": 0.0, "medium": 0.25, "high": 0.50, "irreversible": 0.80}
score = max(score, blast_floor.get(blast_radius, 0.0))
```

**Rule:** Irreversible actions can NEVER be low-friction. The blast radius floor ensures this.

### Pattern banks need domain vocabulary
Initial regex patterns were too narrow:
- `\bpermanent\b` didn't match "permanently" — fix: `\bpermanently?\b`
- "seismic" wasn't in cross_domain — fix: add domain terms
- "career" wasn't in stakes — fix: add human-impact terms

**Rule:** Pattern banks must include the vocabulary the ACTUAL queries use, not just abstract terms.

### Weights should favor blast_radius
Initial weights gave blast_radius 0.20 (same as novelty). After tuning: blast_radius gets 0.30 — the single most important signal.

---

## AkalState Fields (complete)

```python
@dataclass
class AkalState:
    # AKAL invariants (I1-I5)
    friction: FrictionResult | None      # I1 — 333_MIND
    shadow: ShadowTrace | None           # I2 — 555_HEART
    novelty: NoveltyResult | None        # I3 — 777_FORGE
    values: DualVerdict | None           # I4 — 888_JUDGE
    latency: LatencyRequirement | None   # I5 — 999_VAULT

    # APEX dials
    reality_class: str | None            # PRESENT: LIVE|CACHED|INFERRED|UNKNOWN
    thermo_exhausted: bool | None        # ENERGY-ENTROPY: budget status
    reversibility_level: str | None      # AMANAH: reversible|partial|irreversible

    # Metadata
    created_at: float
    cycle_stages: list[str]
```

---

## Key Paths

| What | Path |
|---|---|
| AKAL core | `/root/arifOS/arifosmcp/core/akal.py` |
| AKAL wiring | `/root/arifOS/arifosmcp/core/akal_wiring.py` |
| Epistemic state | `/root/arifOS/arifosmcp/core/epistemic_state.py` |
| Philosophy registry | `/root/arifOS/arifosmcp/runtime/philosophy_registry.py` |
| Thermodynamics | `/root/arifOS/arifosmcp/core/physics/thermodynamics_hardened.py` |
| Reversibility engine | `/root/arifOS/arifosmcp/core/reversibility_engine.py` |
| Amanah gate | `/root/arifOS/arifosmcp/apex_envelope.py` |
| Sensing protocol | `/root/arifOS/arifosmcp/runtime/sensing_protocol.py` |

---

*v1.0.0 — 2026-07-11. APEX four-dial architecture. All dials wired.*
*DITEMPA BUKAN DIBERI*
