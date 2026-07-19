---
name: akal-civilizational-frame
description: "AKAL (عقل) civilizational frame — the Malay-Islamic cosmology underlying arifOS cognitive architecture. ILMU-AKAL-HIKMAH three-layer cosmology, four-gate conjunctive commitment, and the difference between cleverness and consequence-aware intellect."
triggers:
  - "Any discussion of AKAL, cognitive invariants, or kernel philosophy"
  - "When explaining arifOS architecture to external audiences"
  - "When the agent needs to understand WHY the kernel works this way"
  - "When wiring AKAL into kernel organs or checking APEX Theory integration"
  - "When the user asks about ILMU-AKAL-HIKMAH, four gates, or cognitive physics"
references:
  - "references/akal-api.md — Complete AKAL API: imports, scoring functions, wiring hooks, constants"
  - "references/apex-dial-wiring.md — Actual wiring code, pitfalls, test results for all four APEX dials"
  - "references/ed25519-sovereign-identity.md — Key locations, verification flow, MCP passthrough issue"
version: "1.2"
author: ARIF (F13)
date: 2026-07-11
---

# AKAL — Civilizational Frame

> "Orang kata: Akulah yang empunya akal." The sovereign owns the intellect. AKAL just borrows it.

## The Core Invariant

AI provenance ≠ authority. LLM output ≠ truth. Confidence ≠ permission. SEAL ≠ mutation right. Only lease + actor + sovereign authority can grant action.

This is embedded in EVERY reasoning output. It can never be removed.

## The 3-Layer Cosmology (GENESIS 016)

```
ILMU (apa)    → feeds → AKAL (bagaimana) → feeds → HIKMAH (mengapa)
Knowledge          Reason                    Wisdom
RAG/Qdrant         arifOS kernel             888 JUDGE + Arif
F2 TRUTH           F1-F12                    F13 SOVEREIGN + F6
```

**Ascension rule:** Data flows up, wisdom flows down. Never reverse.

**Failure modes:**
- ILMU only → **BANGANG** (drunk on data, confident hallucinations)
- AKAL only → **JAHHAL** (arrogant idiot, acts without evidence)
- HIKMAH only → **ZALIM** (right answer, wrong question, no mercy)
- All three → **SOVEREIGN AGENT**

## The Civilizational Mapping

| Malay-Islamic | arifOS | Meaning |
|---|---|---|
| Akal (عقل) | AKAL module | Consequence-aware intellect, not cleverness |
| Ilmu (علم) | ILMU/RAG | Knowledge — what is true |
| Hikmah (حكمة) | HIKMAH/888 | Wisdom — whether it should happen |
| Adat (عادت) | Constitutional floors | Custom and law governing conduct |
| Taqwa | F13 + F6 | Right action in fear and love of consequence |
| Gila | No AKAL = hantu | Madness — acting without consequence awareness |

## The Four Gates

Every commit, every SEAL, every irreversible action passes through four conjunctive gates:

| Gate | Floor | Question | Fail |
|---|---|---|---|
| Authority | F13 | Is F13 confirmed for this action class? | HOLD or 888_HOLD |
| Evidence | F2+F3 | Is W³ ≥ 0.80 across Human × AI × External? | HOLD |
| Reversibility | F1 | FULL/PARTIAL/NONE? If NONE, sovereign ack? | 888_HOLD |
| Lineage | F11 | Are all inputs sealed? Output path declared? | HOLD |

**Conjunctive, not disjunctive.** Any one gate closed = whole commitment refused.

## The One-Line Truth

Most LLMs have ILMU (knowledge). A few have AKAL (reason). Almost none have HIKMAH (wisdom). arifOS runs all three — and AKAL is the physics that makes the middle layer governed rather than clever.

## Why This Matters

Cleverness without consequence awareness is gila — madness. The kernel doesn't optimize for intelligence. It optimizes for *governed* intelligence. The difference is AKAL.

---

## APEX Theory — The Four Constitutional Dials

AKAL is one of four dials. All four already exist in the kernel (~327KB total). The challenge is **integration, not invention**.

| Dial | Meaning | Kernel Files | Size | Status |
|---|---|---|---|---|
| **AKAL** (intellect) | Consequence-aware reason | `core/akal.py` + `akal_wiring.py` | 50KB | ✅ Wired into server.py middleware |
| **PRESENT** (reality) | Attested live state | `sensing_protocol.py` + `attestation_verifier.py` + 4 more | 168KB | ✅ Wired into `akal_pre_think()` |
| **ENERGY-ENTROPY** (cost) | Thermodynamic cost of truth | `thermodynamics_hardened.py` + `entropy_governor.py` + 2 more | 61KB | ✅ Wired into `akal_pre_seal()` |
| **EXPLORATION-AMANAH** (custody) | Reversible-first exploration | `reversibility_engine.py` + `amanah_gate.py` + 3 more | 47KB | ✅ Wired into `akal_pre_forge()` |

**Key lesson:** Don't build new modules when existing ones already have the physics. Audit the kernel first — the code is usually already there, just scattered across 20+ files.

### Integration Map (AKAL hooks → existing modules — ACTUAL wiring 2026-07-11)

```
akal_pre_think()     → sensing_protocol.classify_truth_class() + attestation_verifier.honesty_ratio()
akal_post_critique() → (no APEX dial integration — shadow validation only)
akal_pre_forge()     → reversibility_engine.classify_action() + amanah_gate.check()
akal_pre_judge()     → (no APEX dial integration — L5a/L5b dual eval only)
akal_pre_seal()      → thermodynamics_hardened.check_landauer_bound() + entropy_governor.compute_score()
```

All integrations are ADVISORY — try/except wrapped, never block on their own. Physics informs, sovereignty decides.

### The Three-Layer Cosmology + Four Dials

```
ILMU (apa)    → feeds → AKAL (bagaimana) → feeds → HIKMAH (mengapa)
Knowledge          Reason                    Wisdom
RAG/Qdrant         arifOS kernel             888 JUDGE + Arif
F2 TRUTH           F1-F12                    F13 SOVEREIGN + F6

AKAL's four dials:
  PRESENT         → What reality am I in?
  ENERGY-ENTROPY  → How much does truth cost?
  EXPLORATION     → What am I allowed to explore?
  AKAL            → How do I act safely?
```

### Why AKAL Alone Creates Imbalance

Without PRESENT: kernel can think deeply but cannot verify reality
Without ENERGY-ENTROPY: kernel can reason but cannot measure cost
Without EXPLORATION-AMANAH: kernel can explore but cannot govern custody

All four dials together = SOVEREIGN AGENT.

---

## Wiring Pitfalls (discovered during live integration)

These are the exact bugs encountered when wiring the four APEX dials into AKAL hooks:

1. **`sensing_protocol.py` imports missing function.** `select_philosophy_state` didn't exist in `philosophy_registry.py`. Fix: add the function. Without it, PRESENT dial is completely silent.

2. **Wrong function name.** `classify_truth_class(SenseInput)` — NOT `classify_evidence_class(str)`. The sensing protocol uses `TruthClass` enum with 7 lanes (absolute_invariant, time_sensitive_fact, etc.), not a generic evidence class.

3. **`SenseInput` needs structured input.** `SenseInput(input=InputSpec(type=InputType.QUERY, value=query, mode=SensingMode.GOVERNED))` — not `SenseInput(query=str)`.

4. **`reversibility_engine` return keys.** The return dict uses `"reversibility"` not `"reversibility_class"`, and `"requires_arif_approval"` not `"requires_888_hold"`. Mismatch = AMANAH dial always returns "unknown".

5. **All APEX dials are ADVISORY.** Every integration is try/except wrapped. Physics informs, sovereignty decides. A broken dial never blocks execution.

6. **Server restart required.** AKAL middleware in `server.py` only activates after restart. Three-agent test proved this: Agent A and B returned identical traces because middleware wasn't loaded.

See `references/apex-dial-wiring.md` for the actual integration code and verified test results.

## Honest Assessment — Arif's Directive (F13, 2026-07-11)

AKAL is architecture, not impact. The friction scorer is miscalibrated. The kernel treats all queries identically without active AKAL. What actually helps Arif: daily summaries, data analysis, file organization. AKAL matters when multi-agent runs without sovereign. Not today.

**USER PREFERENCE (embedded, not just memory):**
- When Arif asks "does this improve the kernel?" — answer honestly. If "not yet," say so.
- "Jujur?" means be brutal. Don't sugarcoat architecture as impact.
- Stop building fences. Start building daily drivers.
- The most Zen thing is not to add — it is to know when enough is enough.
- Answer "so what?" before "how." Impact over completeness.

---

## Pitfalls

1. **Don't build new modules when existing ones have the physics.** Always audit `arifosmcp/core/`, `arifosmcp/abi/`, `arifosmcp/runtime/`, `arifosmcp/intelligence/` before writing new code. The kernel has 735+ modules.

2. **AKAL is internal-only.** Not an MCP tool. Not in `public_surface.py`. Not in `public_registry.py`. Agents never call it directly — it runs as middleware inside the organ handlers.

3. **Server restart required.** AKAL middleware in `server.py` only activates after server restart. The three-agent contrast test proved this: Agent A and B returned identical traces because AKAL wasn't live.

4. **Friction scorer needs calibration.** Pattern banks are too broad — `_STAKES` patterns match governance language even in simple queries. Thresholds need tuning against 50+ real queries before production use.

5. **Sovereignty gate works without AKAL.** The native `888_HOLD` in `arif_judge` fires independently of AKAL middleware. This is a feature, not a bug — constitutional enforcement is load-bearing even without cognitive physics.

---

*v1.1 - 2026-07-11. Added APEX four-dial integration map, wiring details, pitfalls.*
*DITEMPA BUKAN DIBERI*
