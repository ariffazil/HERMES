---
name: akal-cognitive-invariants
description: "AKAL (عقل) — Five cognitive kernel invariants + three APEX dial integrations (PRESENT, ENERGY-ENTROPY, AMANAH). Wired into live kernel. All 5 MCP tools call AKAL hooks."
version: "2.2"
author: ARIF (F13)
date: 2026-07-11
triggers:
  - "Any governed cognitive action requiring friction assessment, novelty enforcement, shadow self-audit, dual evaluation, or latency gating"
  - "Designing or auditing agentic cognition systems"
  - "Wiring cognitive invariants into existing kernel organs"
floor_binding: [F1, F2, F4, F5, F6, F7, F9, F11, F13]
related_skills: [akal-civilizational-frame, measure-before-acting, seven-zen-organs-enforcement, apex-governance, temporal-constitution, temporal-consequence-engine]
supersedes: clap-v1-cognitive-level-assertion, clap-v2-cognitive-kernel-invariants
---

# AKAL — Cognitive Kernel Invariants

> عقل = intellect, the faculty that distinguishes.
> Part of APEX THEORY. Not a module. A law of cognition.
> Organs stay organs. Kernel stays kernel. AKAL is the physics they all obey.

## The One Sentence

An agent can prove something is correct. Only a sovereign can decide if it is good.

## Origin

Bloom's Taxonomy (6 cognitive levels) was mapped onto the arifOS 000→999 metabolic cycle. The insight: cognition isn't a linear staircase — it's a three-layer stack where the sovereign participates above and within the loop, not only at the final verdict.

The five invariants emerged from diagnosing live kernel behavior: the kernel had the *bones* (multi-step reasoning, constitutional floors, sovereign gating) but not the *physics* (friction scoring, shadow content, novelty gates, latency enforcement).

## The Three-Layer Stack

```
Layer 0 — SOVEREIGN METACOGNITION (L0)     [SOVEREIGN ONLY]
    observe the observer · catch bias · maintain agency

Layer 1 — SOVEREIGN JUDGMENT (L5b)          [SOVEREIGN ONLY]
    ethics · values · worth · responsibility · consequences

Layer 2 — AGENT COGNITION (L1 → L5a)       [AGENT]
    L1 REMEMBER → L2 UNDERSTAND → L3 APPLY → L4 ANALYZE → L5a VERIFY
```

**The agent owns L1-L5a. The sovereign owns L5b and L0.**

L0 (Metacognition) is not a gate — it's a posture. The sovereign must periodically ask: "Am I thinking, or is the agent thinking for me?" No kernel verb. No receipt. It's the shadow witness.

## The Five Invariants

### I1 — Difficulty-as-Signal (Friction)

**Wired into:** 333_MIND (`tools/reason.py`)

Friction becomes a governance signal, not a UX bug. If problem complexity >= threshold, shallow completion is INVALID.

Signals detected: ambiguity, novelty, contradiction, identity_stakes, blast_radius, cross_domain.

Scoring: weighted sum normalized to [0,1]. Thresholds:
- LOW (< 0.30): fast pipeline, single pass OK
- MEDIUM (0.30-0.60): standard pipeline
- HIGH (0.60-0.80): deep pipeline, escalation required
- CRITICAL (≥ 0.80): full ascent + sovereign engagement

**API:**
```python
from arifosmcp.core.akal import score_friction, should_escalate, required_pipeline, FrictionResult
result = score_friction(query, blast_radius="high", cross_organ=True)
if should_escalate(result):
    pipeline = required_pipeline(result)  # e.g. ['L1','L2','L3','L4','L5a','L5b']
```

**Wiring hook:** `akal_pre_think()` in `arifosmcp.core.akal_wiring`

### I2 — Shadow Observer (Metacognitive Debugging)

**Wired into:** 555_HEART (`tools/heart.py`)

Every high-stakes reasoning pass must emit a self-audit trace. The agent watches itself think.

Required fields: assumptions, missing_data, shortcuts, likely_biases, tribal_frames.

Validation rejects: empty traces, generic cop-outs ("none", "n/a", "no assumptions").

**API:**
```python
from arifosmcp.core.akal import emit_shadow, validate_shadow, ShadowTrace, SHADOW_REQUIRED_FIELDS
trace = emit_shadow(assumptions=[...], missing_data=[...], shortcuts=[...], likely_biases=[...], tribal_frames=[...])
if not trace.valid:
    # Shadow trace has violations — HOLD
```

**Wiring hook:** `akal_post_critique()` in `arifosmcp.core.akal_wiring`

### I3 — Novelty Requirement (Synthesis over Regurgitation)

**Wired into:** 777_FORGE (`tools/forge.py`)

The kernel's job is not to repeat the world — it must restructure it.

Content classification: DERIVED (copied/summarized) vs SYNTHESIZED (new structure/mapping/reframing).

Thresholds: ≥ 20% SYNTHESIZED for complex tasks. > 90% DERIVED = regurgitation → HOLD.

**API:**
```python
from arifosmcp.core.akal import tag_novelty, enforce_novelty, NoveltyChunk, ChunkType
chunks = [NoveltyChunk(text, ChunkType.SYNTHESIZED, evidence="...")]
result = tag_novelty(chunks)
action = enforce_novelty(result)  # "PROCEED" | "SECOND_PASS" | "HOLD"
```

**Wiring hook:** `akal_pre_forge()` in `arifosmcp.core.akal_wiring`

### I4 — Value-Weighted Verdict (L5a/L5b Split)

**Wired into:** 888_JUDGE (`runtime/kernel/judge.py`)

"Can we do this?" is agentic. "Should we do this?" is sovereign.

- L5a VERIFY (agent): coherence, evidence_validity, logic_consistency, reasoning_chain
- L5b JUDGE (sovereign): harm_assessment, dignity_impact, long_term_consequences, value_alignment

For HIGH/IRREVERSIBLE blast radius, L5b is mandatory. No SEAL without sovereign.

**API:**
```python
from arifosmcp.core.akal import dual_evaluate, DualVerdict, L5A_FIELDS, L5B_FIELDS
verdict = dual_evaluate(coherence=0.9, evidence_validity=0.8, ..., blast_radius="irreversible")
if verdict.judge.sovereign_required:
    # Cannot proceed without sovereign L5b
```

**Wiring hook:** `akal_pre_judge()` in `arifosmcp.core.akal_wiring`

### I5 — Deliberate Latency (Intentionality over Velocity)

**Wired into:** 999_VAULT (`runtime/kernel/seal.py`) + `core/latency_budget.py`

Speed is a risk factor, not a virtue, for deep cognition.

Blast radius classes:
- LOW: single pass, no cooling
- MEDIUM: 2-phase minimum, branching required
- HIGH: multi-pass + branching + cooling
- IRREVERSIBLE: 3 passes + branching + 5min cooling + sovereign second-look

**API:**
```python
from arifosmcp.core.akal import blast_class, cooling_requirement, BlastClass
bc = blast_class("irreversible")
req = cooling_requirement(bc)  # LatencyRequirement with min_passes, cooling_seconds, etc.
```

**Wiring hook:** `akal_pre_seal()` in `arifosmcp.core.akal_wiring`

## Wiring Pattern

AKAL is NOT a standalone package. It's one file (`core/akal.py`) that existing organs import from. The wiring module (`core/akal_wiring.py`) provides thin pre/post hooks:

```
arifosmcp/core/akal.py          ← invariant definitions + scoring (735 lines)
arifosmcp/core/akal_wiring.py   ← integration hooks for each organ
  akal_pre_think()    → 333_MIND entry
  akal_post_critique() → 555_HEART exit
  akal_pre_forge()    → 777_FORGE entry
  akal_pre_judge()    → 888_JUDGE entry
  akal_pre_seal()     → 999_VAULT entry
```

**Rule:** No new package. No new directory. One module, five invariants, wired into existing organs. The organs stay organs.

## Kernel Transformation (000→999)

| Stage | Before AKAL | After AKAL |
|---|---|---|
| 000 | load invariants | cognitive priming |
| 111 | observe | friction + blast radius detection |
| 333 | understand | governed reasoning (friction-aware) |
| 555 | apply | self-observing execution (shadow trace) |
| 777 | analyze | enforced synthesis (novelty gate) |
| 888 | evaluate | VERIFY (agent) + JUDGE (sovereign) |
| 999 | seal | ethical irreversible creation (latency + cooling) |

## APEX Theory — Four Constitutional Dials

AKAL is ONE of four dials in APEX THEORY. The kernel has all four (~327KB of physics), but only AKAL was wired into the 000→999 cycle until 2026-07-11. The other three were built months ago but lived as isolated modules.

| Dial | What It Does | Module(s) | Size | Wired Into |
|---|---|---|---|---|
| **AKAL** (intellect) | Friction, shadow, novelty, values, latency | `core/akal.py` | 50KB | All 5 hooks |
| **PRESENT** (reality) | Truth classification, organ attestation, honesty ratio | `sensing_protocol.py`, `attestation_verifier.py` | 168KB | `akal_pre_think()` |
| **ENERGY-ENTROPY** (cost) | Landauer bound, entropy tracking, thermodynamic budget | `thermodynamics_hardened.py`, `entropy_governor.py` | 61KB | `akal_pre_seal()` |
| **EXPLORATION-AMANAH** (custody) | Reversibility classification, HARAM blocking, cooldown | `reversibility_engine.py`, `amanah_gate.py` | 47KB | `akal_pre_forge()` |

**Temporal Layer (2026-07-13):** A fifth temporal dimension was added via the Temporal Constitution and Temporal Consequence Engine. The five temporal dials (τ, λ, κ, α, ΔS_t) sit on top of the existing four dials, adding horizon, decay, cadence, anomaly, and entropy trajectory to the cognitive invariants. See `temporal-constitution` and `temporal-consequence-engine` skills. The temporal layer is the machine that turns AKAL from a snapshot evaluator into a trajectory evaluator.

**Integration lesson:** We almost built three new modules before discovering all four dials already existed. The kernel had 327KB of physics scattered across 20+ modules. The fix was not new code — it was 15 import statements and 15 function calls wiring existing modules into AKAL's hooks. **Always audit existing code before building new.**

### Three-Dial Wiring Into AKAL

**PRESENT into `akal_pre_think()`:**
```python
from arifosmcp.runtime.sensing_protocol import SenseInput, InputSpec, InputType, SensingMode, classify_truth_class
si = SenseInput(input=InputSpec(type=InputType.QUERY, value=query, mode=SensingMode.GOVERNED))
tc = classify_truth_class(si)
# unknown/ambiguous truth class → boost friction +0.15
```

**ENERGY-ENTROPY into `akal_pre_seal()`:**
```python
from arifosmcp.core.physics.thermodynamics_hardened import check_landauer_bound
landauer = check_landauer_bound(compute_ms=est_ms, tokens_generated=est_tokens, entropy_reduction=1.0)
# Landauer violated → block seal
```

**AMANAH into `akal_pre_forge()`:**
```python
from arifosmcp.core.reversibility_engine import classify_action
rev = classify_action("arif_forge", {"mode": "generate", "query": output_text[:200]})
# irreversible/critical → upgrade PROCEED to HOLD
```

**Design rule:** All three dials are ADVISORY — they boost friction, upgrade actions, add metadata, but never block on their own. Only sovereign (L5b JUDGE) can block. Physics informs, sovereignty decides.

## Diagnostic Results (2026-07-11)

Live kernel audit against all five invariants:

| # | Invariant | Status | Evidence |
|---|---|---|---|
| I1 | Friction | PARTIAL | Multi-step reasoning exists but no explicit friction detector |
| I2 | Shadow | PARTIAL | Structure exists but MiniMax-M3 schema violation on content |
| I3 | Novelty | MISSING | No source-vs-synthesis splitting |
| I4 | Dual Eval | EXISTS | arif_judge correctly enforces sovereign gating |
| I5 | Latency | PARTIAL | Branching exists organically but not gated by blast radius |

Score: 1 EXISTS, 3 PARTIAL, 1 MISSING. AKAL + wiring closes all gaps.

## Naming Convention

AKAL is Malay/Arabic. Fits the kernel's naming philosophy:
- SABAR (patience), MARUAH (dignity), BIJAKSANA (wisdom), DITEMPA (forged)
- AKAL (intellect) = the faculty that distinguishes

**Anti-pattern:** Do NOT create standalone acronym packages (e.g., "CLAP"). Cognitive invariants are physics that live inside existing organs, not separate modules.

## Escape Hatches

Not every interaction requires full AKAL ascent:

| Scenario | Minimum Levels | Invariants Active |
|---|---|---|
| Simple retrieval | L1 only | None |
| Factual Q&A | L1 → L2 | I2 (shadow: tag uncertainty) |
| Routine execution | L1 → L3 | I1 (friction check) |
| Diagnostic/audit | L1 → L4 | I1 + I2 + I3 |
| Governed decision | L1 → L5b | ALL FIVE |
| Irreversible / SEAL | L1 → L6 | ALL FIVE + cooling time |

---

*v1.0 — 2026-07-11. AKAL is part of APEX THEORY. Five invariants. One file. Wired into existing organs.*
*DITEMPA BUKAN DIBERI*
