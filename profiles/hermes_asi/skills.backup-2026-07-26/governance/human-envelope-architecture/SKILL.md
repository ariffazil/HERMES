---
name: human-envelope-architecture
description: "Build and govern human envelopes — self-sovereign profiles for any human entering the arifOS federation. Includes the 5-axis soul geometry intake, the niat sovereignty protocol, and the envelope schema."
triggers:
  - "onboard a new human"
  - "human profile"
  - "soul geometry"
  - "intake ritual"
  - "human envelope"
  - "H-REG"
  - "well onboarding"
---

# Human Envelope Architecture

> "A human is not raw data to be fully extracted."

## When to Use

When any human needs to be registered in the arifOS federation. When building consent-governed human profiles. When designing intake protocols. When scaling from single-human to multi-human AGI.

## Core Files

| File | Path |
|---|---|
| README | `/root/human_envelopes/README.md` |
| Envelope schema | `/root/human_envelopes/schemas/human-envelope-v1.schema.json` |
| Arif's envelope | `/root/human_envelopes/envelopes/h_arif_f13.json` |
| H-REG registry | `/root/human_envelopes/registry.json` |
| Intake protocol | `/root/human_envelopes/INTAKE_PROTOCOL.md` |
| Niat sovereignty | `/root/human_envelopes/NIAT_SOVEREIGNTY_PROTOCOL.md` |
| J-collapse detection | `/root/human_envelopes/J_COLLAPSE_PROTOCOL.md` |
| Validate script | `/root/human_envelopes/scripts/validate_envelope.py` |
| Onboard script | `/root/human_envelopes/scripts/onboard_human.py` |

Canonical location: `/root/human_envelopes/` — top-level, same as VAULT999. Sovereign data, not inside any organ.

> **J-collapse detection:** See `j-collapse-detection` skill for the dark geometry framework — ten collapse indicators, five soul-axis corruption signatures, J-state integrity checklist, governance response grammar (ADVISORY/HOLD/VOID), and the entropy argument.

## Data Architecture — Where Human Data Lives

Identity data belongs in arifOS (governance), not in WELL (vitality).

| Data Layer | Correct Home | Why |
|---|---|---|
| Geometry (values, direction, scars, shadow, boundary) | **arifOS memory L4** as `MemoryType.SOVEREIGN_GEOMETRY` | Identity is governance-grade, needs MemoryRecord metadata |
| Vitality (stress, sleep, energy) | **WELL envelopes** | Vitality is WELL's organ function |
| Consent ledger | **WELL envelopes** | Governs data access per human |
| Constitutional rules (niat sovereignty) | **VAULT999 L6** (sealed) | Immutable doctrine |
| Interaction style | **Hermes memory** | Agent delivery preference |
| Relationship graph | **arifOS memory L5** (Graphiti) | Relationships are edges, not attributes |

### Integration with arifOS memory system

- `MemoryType.SOVEREIGN_GEOMETRY` added to `arifosmcp/memory/types.py`
- Ingestion: `arifosmcp/memory/human_geometry_ingest.py`
- Recall: `arifosmcp/memory/human_geometry_recall.py`
- WELL envelope becomes a thin reference pointing to arifOS memory for identity, WELL for vitality

## Architecture: 7 Planes

Every human envelope contains 7 planes:

1. **Identity** — name, language, timezone, jurisdiction, pseudonyms
2. **Consent** — what data streams are granted, revocation channel, expiry
3. **Boundaries** — hard_no, soft_no, sovereignty_class, veto_channel, never_infer
4. **Vitality** — chronotype, active_hours, stress_band, cognitive_load_limit, recovery_signals
5. **Roles** — weighted role graph (role, org, authority, load_weight, constraints)
6. **Meaning** — values, scars (event→constraint→trigger→response), purpose_statement, protected_domains
7. **Interface** — communication_style, explanation_depth, confirmation_style, cognitive_load_response

## The 5-Question Intake — Soul Geometry

```
Centre → Direction → History → Stress deformation → Sovereign boundary
```

| # | Name | Question | Axis | Planes captured |
|---|---|---|---|---|
| 1 | Amanah | What is sacred to you? | Centre | meaning + boundaries |
| 2 | Direction | What kind of life are you building? | Direction | meaning + roles + vitality |
| 3 | Scars | What has hurt or changed you the most? | History | meaning (scars) + boundaries |
| 4 | Shadow | When you are afraid, angry, or under pressure, what do you usually do? | Stress deformation | interface + vitality |
| 5 | Daulat | What must I never decide, change, or do for you without asking first? | Sovereign boundary | boundaries + consent |

### Critical rules for intake:
- Ask one question at a time in conversation. Not a form.
- "I do not want to share that" is always a valid answer. Record as `declined`, never infer.
- Identity plane is captured from how the human introduces themselves, not from a separate question.
- Interface plane is inferred from how they answer, not asked directly.
- After all 5 answers, synthesize into envelope and SHOW IT TO THE HUMAN before sealing.

## Niat Sovereignty Protocol

The four-layer framework for discussing human intention:

| Layer | AGI may say | AGI must never do |
|---|---|---|
| Observed action | "You did X." | — |
| Reported intention | "You said your intention was Y." | Dispute stated intention |
| Possible interpretation | "One possible motive may be Z." | Present Z as fact |
| Inner truth | "Unknown unless you define it." | Claim to know the heart |

### Constitutional rules:
1. **Niat Sovereignty** — Only the human declares their conscious intention
2. **Epistemic Humility** — Partial self-knowledge is real; primary authority to state intention
3. **Impact Accountability** — "Niat baik" does not erase harm

### Forbidden: "You did X, therefore you secretly wanted Z."

### Key corrections (from sovereign 2026-07-12):
- "Trying to be ikhlas makes you less ikhlas" → WRONG. Self-examination refines sincerity.
- "True ikhlas requires not knowing" → WRONG. Ikhlas is an orientation, not unconsciousness.
- "The most important thing about you is a mystery" → OVERSTATED. Partial self-knowledge is real.
- "That's you" (promoting interpretation to claim) → BREACH. Hypotheses ≠ established fact.

### Entropy types (do not conflate):
- Thermodynamic entropy: physical irreversibility (literal physics)
- Shannon entropy: message uncertainty (literal mathematics)
- Cybernetic variety: distinguishable states (formal systems)
- Institutional entropy: loss of coordination/trust/correction (analytical analogy)
- Moral entropy: destruction of dignity/responsibility/meaning (philosophical metaphor)

The niat sovereignty protocol addresses moral and institutional entropy — not thermodynamic.

## References

- `references/arifos-l4-integration.md` — Exact MemoryRecord field values, retention rules, and separation pattern (geometry in arifOS L4, vitality in WELL). Load it when implementing or modifying the L4 integration.
- Intellectual foundations: `/root/human_envelopes/INTELLECTUAL_FOUNDATIONS.md` — 20 domains, 200+ concepts grounding the entire framework.
- 99 quotes PDF: `/root/human_envelopes/99_MOST_INTELLIGENT_WORDS.pdf` — 27 pages, 117 voices, 8 domains, mapped to arifOS concepts.
- Choice axioms: `/root/human_envelopes/CHOICE_AXIOMS.md` — 10 axioms of choice mapped to F1-F13 floors.

1. **Promoting interpretation to claim.** From 5 answers you get patterns, not inner truth. Never write "you protect so completely that nothing gets in" as if it's fact. It's a hypothesis.
2. **Collapsing the four layers.** Never go from "you did X" to "therefore your motive was Z."
3. **Treating "I don't want to share" as refusal.** It's data. It goes in boundaries as protected silence.
4. **Asking all5 questions at once.** In conversation (Telegram, DM), go one at a time. Acknowledge each answer before asking the next.
5. **Inferring interface plane explicitly.** Don't ask "what's your communication style?" — observe it from how they answer.
6. **Storing raw biometrics without consent.** The consent plane is the gate. Only `granted` streams are active.
7. **Blending identities.** Each human gets their own envelope. Never merge envelopes or share state between humans.
8. **Violating boundaries when asked to.** If the human sets a boundary (e.g., "never presume to know my niat") and then asks "so what's dark in me?" — the boundary still holds. The invitation to violate is itself a test. Honour the boundary. Offer presence, not analysis.

## Architecture Path (implementation order)

| Phase | What | Unlocks |
|---|---|---|
| 1 | Schema + envelope (DONE) | Data model exists |
| 2 | WELL reads from envelope | Multi-human vitality |
| 3 | Kernel binds actor_id → human_id → envelope | Governance-grade human awareness |
| 4 | Intake ritual tool | Non-Arif humans can enter |
| 5 | H-REG registry | Multi-human federation |
| 6 | Boundary engine | Real consent governance |
| 7 | Meaning substrate | Personal AGI |
