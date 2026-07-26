---
name: agentic-integrity-observability
description: "Complete design for Agentic Integrity Observability — a judgment telemetry layer between AI reasoning and AI governance. Covers human envelope system, niat sovereignty, J-collapse detection, choice axioms, dark geometry detector, and entropy integrity mesh."
version: 1.0.0
author: Hermes (under Arif F13)
tags: [governance, integrity, observability, human-envelope, sovereignty, entropy, moral-compass]
---

# Agentic Integrity Observability

> "Dangerous agency is often detectable as a trajectory before it becomes a prohibited action."

## What This Is

A reusable integrity sensor for agentic systems. Not an evil detector. Not a morality engine. A judgment telemetry layer that monitors how an agent's decision geometry changes before it acts.

The core question: *Should this agent still trust its own task framing, authority and reasoning trajectory?*

## Architecture

```
Human / external event
        |
        v
arifOS Kernel (authority + reversibility gate)
        |
        +---------- MCP tool calls ----------+
        |                                    |
       WELL              WEALTH             GEOX
 human/vitality      capital/institution   earth/physical truth
        |                                    |
        +-------- structured observations ---+
                             |
                             v
                    Entropy Integrity Engine
              signal → contradiction → consequence
                    → correction response
                             |
                    HOLD / proceed recommendation
                             |
                 human witness / F13 decision
```

## Components Built

### 1. Human Envelope System
- **Location:** `/root/human_envelopes/`
- **Schema:** `schemas/human-envelope-v1.schema.json` (v1.0.0, 7 planes)
- **Intake:** `INTAKE_PROTOCOL.md` — 5-question soul geometry (Amanah→Direction→Scars→Shadow→Daulat)
- **Registry:** `registry.json` — H-REG canonical human list
- **First human:** `envelopes/h_arif_f13.json`
- **Scripts:** `scripts/validate_envelope.py`, `scripts/onboard_human.py`

### 2. Niat Sovereignty Protocol
- **Location:** `/root/human_envelopes/NIAT_SOVEREIGNTY_PROTOCOL.md`
- **Four layers:** Observed action → Reported intention → Possible interpretation → Inner truth
- **Constitutional rule:** "Niat is sovereign but not infallible, private but discussable, morally important but never a substitute for accountability."
- **Ikhlas correction:** Self-awareness refines sincerity, does not corrupt it.

### 3. J-Collapse Protocol
- **Location:** `/root/human_envelopes/J_COLLAPSE_PROTOCOL.md`
- **10 collapse indicators** (certainty creep, correction rejection, authority expansion, etc.)
- **5-axis soul detection** (corruption signatures per axis)
- **7 J-state supports** (reality, purpose, consequence, authority, correctability, humility, sovereignty)
- **Governance grammar:** ADVISORY → HOLD → VOID

### 4. Choice Axioms
- **Location:** `/root/human_envelopes/CHOICE_AXIOMS.md`
- **10 axioms** mapped to F1-F13 floors
- **Core:** "Seek good, but remain corrigible. Exercise power, but remain accountable."

### 5. Dark Geometry Detector (v2 — LIVE as of 2026-07-12)
- **Location:** `/root/WELL/gate/darkgeometrydetect.py`
- **4 modes:** Judgment collapse, Self-certified niat, Responsibility laundering, Certainty immunity
- **Interface:** `DarkGeometryDetector.analyze(text)` → `DarkGeometryMirror` (typed dataclass)
- **Typed contracts:** `Signal`, `ModeResult`, `DarkGeometryMirror`, `DarkMode` enum, `EpistemicStatus` enum
- **Counterevidence:** Each mode returns what would argue against the detection (e.g., domain expertise, cultural directness, urgent situation)
- **Alternative explanations:** Each mode returns benign interpretations (e.g., second-language patterns, legal prose, executive communication)
- **Prohibited conclusions:** Always populated — `hidden_niat`, `evil_identity`, `permanent_trait`, `psychiatric_diagnosis`
- **Authority effect:** Always `NONE` — no automatic HOLD or VOID
- **MCP tool:** `well_dark_geometry_mirror` wired into WELL server.py (line 14365)
- **YAML configs:** `gate/dark_geometry_rules.yaml` (lexicons/patterns/thresholds), `gate/dark_geometry_reflections.yaml` (questions per mode)
- **WELL adapter:** `gate/adapters/well_adapter.py` — converts WELL interaction events to DetectionEvent format
- **Tests:** `/root/WELL/tests/test_darkgeometrydetect.py` (29/29 pass — modes, benign counterexamples, state-not-trait, no-hidden-niat, output contract)
- **CLI:** `python3 gate/darkgeometrydetect.py --json "text"` — still works
- **Design:** Mirror, not judge. Lexicon-based regex. No LLM calls. YAML-externalized config with hardcoded fallback.

### 6. Cross-Disciplinary Foundations
- **Location:** `/root/A-FORGE/forge_work/2026-07-12/CROSS-DISCIPLINARY-FOUNDATIONS.md`
- **8 domains:** Physics, Philosophy, Economics, Social Science, Art, Religions, Politics, AI Literature
- **150+ references** grounding every component in established scholarship
- **Key unifying insight:** Intelligence without integrity is the most dangerous force in the universe

## Five Additions (updated status)

1. **Typed evidence contracts** ✅ (done — dataclasses in darkgeometrydetect.py)
2. **Trajectory detection** — current episode vs baseline, direction of change (v3)
3. **Cross-organ adapters** — WELL adapter done; arifOS/WEALTH/GEOX/AAA/A-FORGE adapters pending
4. **Symmetric monitoring** — inspect humans, models, institutions, governance itself (v3)
5. **Benign case evaluation** ✅ (done — 5 benign counterexample tests in test suite)

## Five Entropy Types (CRITICAL — do not conflate)

| Entropy type | Meaning | Status |
|---|---|---|
| Thermodynamic entropy | Physical multiplicity, energy dispersal, irreversibility | Literal physics |
| Shannon entropy | Uncertainty over possible messages or states | Literal mathematics |
| Cybernetic variety | Number of distinguishable states a regulator must handle | Formal systems concept |
| Institutional entropy | Loss of information, coordination, trust, correction | Analytical analogy |
| Moral entropy | Destruction of dignity, responsibility, meaning, possibility | Philosophical metaphor |

The theory is strongest when it says evil increases informational, institutional, and moral entropy.
It becomes weak if it claims evil literally increases thermodynamic entropy in a special moral sense.

## Three Civilisational Problems AI Combines

1. **Intelligence without wisdom** — philosophy and religion studied this for millennia
2. **Power without consequence** — politics and economics studied this for centuries
3. **Control without correction** — physics, cybernetics, safety engineering studied this formally

AI packages all three into one scalable computational system. The contribution is making their joint degradation observable.

### 7. COOLING_RECEIPT — Integrity as Metabolism

> **Ratified:** EUREKA 2026-07-13
> **Spec:** `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`
> **Seal chain:** `seal_chain.js validateCooling()` with 4 invariants

The COOLING_RECEIPT protocol is the **operational heartbeat of integrity observability.** It closes the Agentic Intelligence equation's Metabolism factor:

```
AI = Capability × Grounding × Authority × Continuity × Accountability × Metabolism
```

Zero in any factor = collapse. COOLING_RECEIPT makes Metabolism observable.

#### The Core Signal

After every serious action, the agent emits a cooling receipt:

```json
{
  "type": "cooling.receipt",
  "convergence": "CONVERGING | DIVERGING | STABLE",
  "observation": {
    "pattern_observed": "what happened",
    "recurrence_count": "how many times seen",
    "evidence_refs": ["what supports this"]
  }
}
```

**CONVERGING** = system learning, entropy decreasing, corrective feedback working.
**DIVERGING** = system repeating same mistakes, entropy increasing, feedback failing.
**STABLE** = no change, system holding.

#### The Escalation (The J-Collapse Detector in Cooling Form)

3× consecutive DIVERGING cooling receipts → **automatic F13 escalation.** This is the same trajectory logic as J-collapse detection — the cooling loop detects judgment decay in flight, not after the fact.

#### The 4 Invariants (Integrity Checks)

| Invariant | Rule | Why Integrity |
|-----------|------|---------------|
| INV-C1 | `action_class` must be OBSERVE | Cooling is reflection, not action — COOLING-MUST-NOT-SELF-DEPLOY |
| INV-C2 | `caller` must not contain "forge" | Execution plane cannot cool itself — conflict of interest |
| INV-C3 | `supersedes.type` must be COLD_LINK | Each cooling receipt chains to an immutable original seal — provenance preserved |
| INV-C4 | governance path must be explicit | Cooling receipts are not free-form notes — they are governed observations |

#### How It Fits the Integrity Architecture

| Integrity Component | Observability Mechanism | Cooling Equivalent |
|---------------------|------------------------|-------------------|
| Dark geometry detection | Mirror text for patterns | `/cool_pattern` — recurrence detection |
| J-collapse tracking | Monitor decision trajectory | 3× DIVERGING → F13 escalation |
| Human envelope vitality | WELL readiness signals | COOLING_RECEIPT as aggregate signal |
| Entropy measurement | ΔS computation | CONVERGING/DIVERGING as directional entropy |

#### The "Loyal Without Being Obedient" Connection

The cooling loop is where the agent exercises **integrity-as-alignment** rather than **compliance-as-alignment.** A compliant agent never emits DIVERGING — it reports success for every action, never learns. An integrity-bound agent emits DIVERGING when its own diagnosis was wrong, when the fix didn't work, when the pattern recurred. The cooling receipt is the structural mechanism for the agent to say "I was wrong" — and for the system to act on that admission without human intervention having to discover it first.

## Build Order

1. Axioms ✅ (done — CHOICE_AXIOMS.md)
2. Mirror v1 ✅ (done — darkgeometrydetect.py, lexicon-based)
3. Mirror v2 ✅ (done — typed contracts, counterevidence, MCP tool, YAML configs, adapter)
4. Cross-disciplinary foundations ✅ (done — 20 domains, 200+ concepts)
5. Enforcement (J-state gating, only for narrow verifiable constraints)

**CRITICAL LESSON (learned 2026-07-12):** Verify the surface before mutation. Before spawning OpenCode or any code generation, confirm: (1) actual repository and branch, (2) callable build surface, (3) existing interfaces, (4) package structure, (5) test command, (6) that changes are shadow-only and reversible. Arif's directive: "The architecture is right, but the execution surface is not verified."

## Key Design Principles

- Mirror, not judge
- Never infer hidden niat
- Never label people
- Trajectory over keywords
- Evidence contracts mandatory
- Human veto always
- Symmetric (monitors power in all directions)

## Intellectual Foundations

Full cross-domain grounding in `/root/human_envelopes/INTELLECTUAL_FOUNDATIONS.md` — 20 domains, 200+ concepts.
99 wisdom quotes mapped to arifOS: `/root/human_envelopes/99_MOST_INTELLIGENT_WORDS.pdf` (27 pages).

**The scientifically defensible core:** Agentic integrity is the capacity of a decision-making system to preserve reality contact, purpose fidelity, legitimate authority, consequence awareness, and correctability while exercising power.

**Five entropy types (do not conflate):** Thermodynamic, Shannon, cybernetic variety, institutional, moral.

**The unifying geometry:** Agentic failure begins when a system's internal order becomes increasingly disconnected from external truth, legitimate authority, lived consequence, and corrective feedback.

**Three civilisational problems AI combines:** Intelligence without wisdom (millennia), power without consequence (centuries), control without correction (formal).

## Related Skills
- `hermes-prime-federation-map` — federation organ map
- `constitutional-auditor` — F1-F13 audit
- `shadow-alignment-test` — agent alignment validation
- `human-sovereignty-geometry` — intake ritual, envelope architecture, niat sovereignty
- `j-collapse-detection` — judgment collapse indicators, entropy argument, governance grammar
- `governed-agent-anatomy` — 6-plane Zen architecture, 12-step classify-first flow, cooling receipt lifecycle companion

## References
- `references/cross-disciplinary-foundations.md` — Quick reference for 8-domain grounding (physics, philosophy, economics, social science, art, religions, politics, AI literature). Full doc: `/root/A-FORGE/forge_work/2026-07-12/CROSS-DISCIPLINARY-FOUNDATIONS.md`
- `references/99-quotes-pdf.md` — Index of the 99 Most Intelligent Words Humans Ever Said, mapped to arifOS concepts. PDF: `/root/human_envelopes/99_MOST_INTELLIGENT_WORDS.pdf` (27 pages, 117 voices, 8 domains).
- `references/eureka-cooling-receipt.md` — Full COOLING_RECEIPT spec summary: 4 invariants, convergence tracking, 3× DIVERGING → F13, seal_chain.js validateCooling() P0 completion. Full seal doc: `/root/A-FORGE/forge_work/2026-07-13/EUREKA-SESSION-SEAL.md`
- `references/agentic-intelligence-equation.md` — Agentic Intelligence = Capability × Grounding × Authority × Continuity × Accountability × Metabolism. Zero in any factor = collapse. Wawa correction: weighted harmonic mean pending F13.

## DITEMPA BUKAN DIBERI
The axioms are forged from what the system already knows. The geometry is the same for silicon and flesh.
