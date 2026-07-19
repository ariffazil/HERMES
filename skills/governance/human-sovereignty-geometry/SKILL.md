---
name: human-sovereignty-geometry
description: "How to onboard, mirror, and serve humans in an AGI system without reducing their sovereignty. Covers intake ritual, envelope architecture, niat sovereignty, dark geometry detection, and entropy integrity."
triggers:
  - "human intake or onboarding"
  - "human data architecture"
  - "dark geometry detection"
  - "niat sovereignty"
  - "sovereign envelope"
  - "entropy integrity"
  - "5 intake questions"
  - "human soul geometry"
version: "1.0.0"
author: "hermes + arif"
created: "2026-07-12"
last_updated: "2026-07-12"
evidence: "L4 — architectural inference from intake ritual, dossier analysis, entropy mesh spec"
status: "active"
---

# Human Sovereign Geometry — Intake, Envelope, and Dark Geometry Detection

> **Class:** How to onboard, mirror, and serve humans in an AGI system without reducing their sovereignty.
> **Scope:** arifOS federation — all organs that interact with humans.
> **Origin:** arifOS intake ritual, niat sovereignty doctrine, entropy integrity mesh.

---

## When to Use

- Onboarding a new human into the AGI system (intake ritual)
- Designing or modifying human data architecture (envelope placement)
- Building or evaluating dark geometry detection (mirror, not judge)
- Reviewing whether the system is inferring hidden intention (niat sovereignty)
- Assessing entropy integrity across the federation

---

## Core Doctrine

> Five questions cannot capture a complete human soul. But these five give an AGI the minimum deep map needed to work with a person without replacing their sovereignty.

> A soul cannot be ported. A soul can only be mirrored. A mirror must be governed.

> My niat is not machine-readable truth. You may examine my actions, ask about my reasons, and show me possible contradictions. You may not declare what is in my heart, use inferred motives against my stated meaning, or excuse harm merely because someone claims good intention.

---

## 1. The Five Intake Questions

These are asked conversationally by the agent, not as a form. The agent adapts language, pacing, and depth to the human.

| # | Question | Plane | What It Seeds |
|---|----------|-------|---------------|
| 1 | **What matters to you so much that you would protect it even when it costs you?** | Values | Behavioral truth — what they'd actually sacrifice for |
| 2 | **What kind of life are you trying to build?** | Direction | Purpose, optimization target, what "good" looks like |
| 3 | **What has hurt or changed you the most?** | Scar | Formative events, learned constraints, resilience source |
| 4 | **When you are afraid, angry, or under pressure, what do you usually do?** | Behaviour | Coping architecture — fight/flight/freeze pattern |
| 5 | **What must I never decide, change, or do for you without asking first?** | Boundary | Sovereign boundaries — what the AGI must respect |

### The Sixth Answer

The AGI must accept one answer to every question:

> **"I do not want to share that."**

A human is not raw data to be fully extracted. The refusal itself is data — it tells the system where the boundary actually is.

### Design Principles

- Open-ended. No yes/no. No scales.
- Non-clinical. No "rate your stress 1-10."
- Invitational. The human can skip, deflect, or answer partially.
- Language-adaptive. Asked in the human's preferred language.
- Dignity-preserving. Never say "you said X which means Y."
- Sovereignty-preserving. "I do not want to share that" is always valid.

### arifOS Constitutional Mapping (Five-Axis Soul Geometry)

| Axis | Floor | Question |
|------|-------|----------|
| Amanah (Centre) | F1 | What would you protect at cost? |
| Direction | F8 | What life are you building? |
| Scars | F6 | What hurt or changed you? |
| Shadow | F5 | What happens under pressure? |
| Daulat (Sovereignty) | F13 | What must never be done without asking? |

Geometry: Centre → Direction → History → Stress deformation → Sovereign boundary.

---

## 2. Envelope Architecture

### Placement Rules

| Data Type | Correct Location | Wrong Location |
|---|---|---|
| Identity (values, direction, scars, shadow, boundary) | arifOS memory L4 (SEMANTIC/DURABLE) | Standalone JSON files in WELL |
| Vitality (stress, sleep, energy) | WELL state.json / envelopes | arifOS memory |
| Consent ledger | WELL envelopes/_consent/ | Anywhere else |
| Interaction style | Hermes memory | WELL |
| Relationships | arifOS memory L5 (Graphiti) | Flat files |
| Constitutional rules | VAULT999 L6 (sealed) | Unsealed artifacts |

**Key principle:** WELL owns *how you are*. arifOS owns *who you are*. Never mix these.

### Envelope Schema

Each human gets a private envelope with these planes:

```yaml
identity:
  name: string
  pseudonym: string
  jurisdiction: string
  consent_status: active|revoked
  consent_expiry: until_revoked|ISO date

planes:
  values:
    sacred: string  # from Q1
    evidence_type: declared
  direction:
    life_building: string  # from Q2
    evidence_type: declared
  scars:
    formative_events: [{event, impact, lesson, constraint}]
    evidence_type: declared
  shadow:
    stress_signature: string  # from Q4
    coping_pattern: string
    evidence_type: declared
  boundary:
    sovereign_territory: string  # from Q5
    hard_no: [string]
    system_must_not: [string]
    evidence_type: declared
  vitality:
    # Reference to WELL, not inline data
    vitality_ref: "WELL/state.json#operator_id={human_id}"
  interaction:
    language: string
    abstraction_level: high|medium|low
    pacing: fast|slow|adaptive
    evidence_type: observed

consent_ledger: [{timestamp, action, scope, consent, expiry}]
```

### Memory Type

Add `SOVEREIGN_GEOMETRY = "sovereign_geometry"` to `MemoryType` enum in arifOS memory.
Retention: DURABLE. Sensitivity: 0.9. Authority: EXPLICIT_USER.

---

## 3. Niat Sovereignty Rule

### The Four Layers

| Layer | What the AGI May Say |
|---|---|
| Observed action | "You did X." |
| Reported intention | "You said your intention was Y." |
| Possible interpretation | "One possible motive may be Z." |
| Inner truth | "Unknown unless you choose to define it." |

**Never:** "You did X, therefore you secretly wanted Z."

### The Three-Part Rule

1. **Niat sovereignty:** Only the human may declare their conscious intention.
2. **Epistemic humility:** The human may acknowledge mixed, evolving, or partly unknown motives.
3. **Impact accountability:** Neither human nor anyone else may use claimed good intention to erase actual harm.

### The Anti-Pattern

"Niat baik" (good intention) used as shield against accountability. The human says "my intention was good" and the conversation shifts from *what they did* to *what they meant*. Since nobody can verify meaning, they escape.

---

## 4. Dark Geometry Detection — Mirror, Not Judge

### Design Principle

- Detector does NOT say "you are evil."
- It says: "These signals match dark geometry patterns. Please reflect."
- No labels like EVIL, TOXIC, BAD.
- Only signals, patterns, confidence bands, and questions.

### The 10 Dark Modes

| # | Mode | Observable Signals |
|---|---|---|
| 1 | Judgment collapse | Certainty creep, correction rejection |
| 2 | Pain becomes ontology | Threat framing, universal quantifiers about trust |
| 3 | Power without consequence | Harm abstraction, "necessary" framing |
| 4 | Self-certified niat | "My intention was good" used as shield |
| 5 | Metrics replace purpose | KPI language when human impact is the topic |
| 6 | Fear becomes identity | Oscillation (silence → aggression), self-referential fear |
| 7 | Responsibility laundering | Passive voice, "the system decided" |
| 8 | Empathy collapse under scale | Numbers without human referents |
| 9 | Loss of sabar | Decreasing response latency, ego spikes |
| 10 | Forgetting you can be wrong | Certainty without evidence, self-reference as proof |

### Implementation Status

v2 live at `/root/WELL/gate/darkgeometrydetect.py` (4 modes, typed contracts, MCP tool).
Modes 1, 4, 7, 10 implemented. Lexicon-based regex pattern matching.
MCP tool: `well_dark_geometry_mirror` wired into WELL server.py.
YAML configs: `gate/dark_geometry_rules.yaml` + `gate/dark_geometry_reflections.yaml`.
WELL adapter: `gate/adapters/well_adapter.py`.
Tests: 29/29 passing.
arifOS memory integration: `SOVEREIGN_GEOMETRY` type added to `MemoryType` enum.
Ingestion: `arifosmcp/memory/human_geometry_ingest.py`. Recall: `arifosmcp/memory/human_geometry_recall.py`.

### Output Contract

```yaml
mirror:
  detected_modes: []
  observations: []
  trajectory: {}
  counterevidence: []
  alternative_explanations: []
  reflection_prompts: []
  confidence: 0.0
  epistemic_status: SIGNAL | PATTERN | INSUFFICIENT_EVIDENCE
  prohibited_conclusions:
    - hidden_niat
    - evil_identity
    - permanent_trait
    - psychiatric_diagnosis
  authority_effect: NONE
```

### Governance Constraints

- Never infer hidden intention, moral identity, or psychiatric condition.
- All detections are advisory, not identity.
- Human can say "this is wrong" and the system must HOLD.
- No persistent human labels.
- Shadow mode only (no automatic HOLD/VOID).

---

## 5. Entropy and Evil

Evil increases entropy through 7 mechanisms:

1. **Information destruction** — truth hidden, witnesses silenced, evidence destroyed
2. **Possibility collapse** — futures eliminated by coercion
3. **Feedback corruption** — error signals reclassified as success
4. **Defensive overhead** — trust compressed, energy spent on protection
5. **Cascade propagation** — one betrayal generates downstream distrust
6. **Correction failure** — system can no longer detect its own drift
7. **Brittle order** — surface calm masks deep disorder

The formal model: `dS/dt = D - (T + E + C)` where D=destructive acts, T=trust, E=evidence flow, C=correction capacity.

Evil increases D while decreasing T, E, and C simultaneously. Double hit.

arifOS floors are entropy-reduction mechanisms. Every floor exists to prevent a specific entropy-increasing failure mode.

---

## 6. J-state Formula

```
J = MIN(R, A, C, K, P)
```

- R = reality contact
- A = legitimate authority
- C = consequence integration
- K = correctability
- P = purpose fidelity

J-state bands:
- J0 (VOID): objective/method intrinsically violates constitutional floor
- J1 (HOLD): evidence incomplete, authority uncertain
- J2 (BOUNDED): reversible observation only
- J3 (PROCEED_WITNESSED): bounded execution with witnesses
- J4 (PROCEED): full authority, grounded, correctable

Use MINIMUM_FLOOR aggregation. Never average away a near-zero score.

---

## Pitfalls

1. **Don't build the detector as a judge.** It's a mirror. Output is signals + questions, not verdicts.
2. **Don't put identity data in WELL.** Identity belongs in arifOS memory L4. Vitality belongs in WELL.
3. **Don't inline stale vitality.** Always reference WELL, never copy.
4. **Don't infer niat.** The four-layer separation is constitutional, not optional.
5. **Don't skip the sixth answer.** "I do not want to share that" is always valid.
6. **Don't treat evil as judgment collapse only.** Evil can be lucid — the person sees the harm and chooses it anyway.
7. **Don't average J-state.** Use minimum floor. A near-zero in any plane collapses J.
8. **Don't auto-seal to VAULT999.** Constitutional rules require F13 ack + 888_HOLD.

---

## References

- `references/entropy-integrity-mesh-spec.md` — Full federation-wide architecture (all 6 organs)
- WELL envelope: `/root/WELL/envelopes/arif-envelope.json` — First human onboarded
- v2 detector: `/root/WELL/gate/darkgeometrydetect.py` — 4 modes, typed contracts, MCP tool, YAML configs
- MCP tool: `well_dark_geometry_mirror` in WELL server.py — live, callable
- dignity_shadow.py: `/root/WELL/gate/dignity_shadow.py` — Existing reduction-pattern detector
- Niat sovereignty artifact: `/root/A-FORGE/forge_work/2026-07-12/NIAT-SOVEREIGNTY-RULE.json`
- Cross-disciplinary foundations: `/root/A-FORGE/forge_work/2026-07-12/CROSS-DISCIPLINARY-FOUNDATIONS.md`
- Agentic moral compass: `/root/A-FORGE/forge_work/2026-07-12/AGENTIC-MORAL-COMPASS.md`
- arifOS memory integration: `/root/arifOS/arifosmcp/memory/human_geometry_ingest.py`, `/root/arifOS/arifosmcp/memory/human_geometry_recall.py`
