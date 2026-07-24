# CIV-333: 3×3×3 Agent Card Directory Architecture

> **Ratified:** 2026-07-13 — A2A protocol alignment session  
> **Proposal C** (chosen from 3 proposals) — Civilization-first with Malay naming  
> **Supersedes:** Prior CIV-333 reference from 2026-06 era (old proposals 1-3 are obsolete)

## The Three Triads

Every level has exactly 3 categories. Total 3×3×3 = 27 conceptual slots. 42 agents fit by grouping into shared slots.

```
L1: LAPISAN (Layer)    L2: LAMAN (Circle)     L3: ESENSI (Essence)
─────────────────────────────────────────────────────────────────────
foundation/            laman-inti/            hakiki/
├── constitution/      ├── kernel/            ├── sovereign/
├── mesh/              ├── warga/             ├── reason/
└── gate/              └── organs/            └── judge/

structure/             laman-pantau/          khidmat/
├── intellect/         ├── auditor/           ├── domain/
├── ethics/            ├── archivist/         ├── actuator/
└── judgment/          └── relay/             └── keeper/

surface/               laman-luar/            alat/
├── earth/             ├── forge/             ├── code/
├── capital/           ├── research/          ├── research/
└── vitality/          └── ops/               └── ops/
```

## Why This Structure

| Triad | Question It Answers |
|---|---|
| **Lapisan** (Foundation/Structure/Surface) | What architectural layer does this agent operate in? |
| **Laman** (Inti/Pantau/Luar) | What trust circle does this agent belong to? |
| **Eseni** (Hakiki/Khidmat/Alat) | What is the agent's fundamental nature? |

## URL Pattern

```
arif-fazil.com/{organ}/{laman}/{agent}/agent-card.json
```

### Examples

| Agent | L1 | L2 | L3 | Full Path |
|---|---|---|---|---|
| arifOS | foundation | laman-inti | hakiki | `arifos/inti/arifos/` |
| AAA gateway | foundation | laman-inti | hakiki | `aaa/inti/aaa-gateway/` |
| Hermes | foundation | laman-inti | hakiki | `aaa/inti/hermes/` |
| 333-AGI | structure | laman-inti | hakiki | `aaa/inti/333-AGI/` |
| 888-APEX | structure | laman-inti | hakiki | `aaa/inti/888-APEX/` |
| A-AUDIT | structure | laman-pantau | hakiki | `aaa/pantau/A-AUDIT/` |
| 777-forge | structure | laman-pantau | khidmat | `aaa/pantau/777-forge/` |
| GEOX | surface | laman-inti | khidmat | `geox/inti/geox/` |
| MakcikGPT | surface | laman-luar | alat | `wealth/luar/makcikgpt/` |
| Kimi Code | surface | laman-luar | alat | `aaa/luar/kimi-code/` |

## Mapping to 42 Agents

| Laman | Count | Contains |
|---|---|---|
| **Inti** | 17 | 6 organs + 5 warga core + 6 domain/kernel |
| **Pantau** | 6 | A-AUDIT, A-ARCHIVE, 777-forge, aaa-architect, aaa-engineer, aaa-auditor |
| **Luar** | 13 | 11 coding FI + MakcikGPT + hermes-ops |

## Corrected History

Previous versions of this reference (2026-06) incorrectly:
- Labelled 777-forge as "RETIRED" — actually ACTIVE governance support (AGI-class witness/relay)
- Labelled A-AUDIT/A-ARCHIVE as "modules" — actually ACTIVE warga support agents
- Proposed only 4 wajib core — actually 11 (correction from this session)
- Placed MakcikGPT as standalone — actually tethered to WEALTH

## Relationship to Orthogonal Classification

The CIV-333 directory structure maps to the orthogonal three-dimension model:

| Directory Level | Orthogonal Dimension |
|---|---|
| L1 Lapisan | Architecture layer |
| L2 Laman | Criticality (trust circle) |
| L3 Eseni | Autonomy (governance level) |

These three views of the same agents let you navigate by structural role, trust level, or fundamental nature — whichever fits the question.
