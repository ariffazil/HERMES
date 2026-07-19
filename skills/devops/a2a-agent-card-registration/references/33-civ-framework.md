# 33 CIV — Civilization Framework (Validated 2026-07-13)

> **Canonical architecture:** Arif's final taxonomy for the arifOS federation.
> **33 = 11 wajib + 6 support + 13 external AI tools + 3 cognitive domains**
> **Geometry B:** Knowledge profiles ≠ agent cards.

## The Trinity (Identity Atoms — NOT lanes, NOT categories)

```
Δ 333-AGI   → REASON + EXECUTION
Ω 555-ASI   → MEMORY + CRITIQUE
ΦΙ 888-APEX → JUDGMENT + WITNESS
```

These three ARE the federation. If any is missing, the federation has no center. They are not "agents" in the operational sense — they are identity atoms that the rest of the system orbits.

## The 4-Layer Agent Card Structure

| Layer | Question | Contents | Criticality |
|---|---|---|---|
| **identity/** | "Who ARE we?" | 333-AGI, 555-ASI, 888-APEX | Wajib — no center without them |
| **functions/** | "What do we ALWAYS need?" | OpenClaw (inst. AGI), A-AUDIT (inst. APEX), A-ARCHIVE (inst. ASI) | Degrades gracefully |
| **extensions/** | "What do we REACH with?" | Hermes (ASI surface), 777-forge (AGI actuator), MakcikGPT (ASI critique) | Operational, bounded |
| **harnesses/** | "What tools do we GRAB?" | 11 forge instruments (OpenCode through Continue) | Swap freely |

### Directory Layout

```
agent-cards/
├── identity/         ← 3 cards (Δ·Ω·ΦΙ)
├── functions/        ← 3 cards (institutional trinity)
├── extensions/       ← 3 cards (operational)
├── harnesses/        ← 11 cards (interchangeable coding tools)
├── roles/            ← 5 cards (AAA internal: arch/eng/audit/gateway/ops)
├── forge/            ← 11 FI-indexed copies (FI-001 through FI-011)
├── organs/           ← 5 cards (arifOS, GEOX, WEALTH, WELL, A-FORGE)
└── main.json         ← arifOS_bot (Telegram identity)
```

### The Geometry — ACTORS vs NOUNS

```
agent-cards/          — 21 ACTORS (Ed25519 signed, MCP tools, A2A cards, runtime loops)
knowledge/            — 33 NOUNS (pure JSON profiles, zero executable surface, passive atlases)

Thermodynamic boundary is clean: 
- ACTORS can change the world (tools, sessions, mutations)
- NOUNS are lenses the ACTORS use to reason
```

## The 33 = 11 + 6 + 13 + 3

| Category | Count | Details |
|---|---|---|
| Wajib core | 11 | arifOS · AAA · A-FORGE · GEOX · WEALTH · WELL · Hermes · 333-AGI · 555-ASI · 888-APEX · OpenClaw |
| Support | 6 | A-AUDIT · A-ARCHIVE · 777-forge · aaa-architect · aaa-engineer · aaa-auditor |
| External tools | 13 | 11 coding FI + MakcikGPT + hermes-ops |
| Cognitive domains | 3 | Physics (000-400) · Math (444-700) · Code (777-999) |

## The Knowledge Atlas (33 Profiles)

```
knowledge/
├── manifest.json     ← 33 profiles, dependency graph, epistemic invariant
├── README.md         ← Geometry B operational doc
├── physics/          ← 11 files (000-400) — What IS
│   ├── 000-foundational-axioms.json
│   ├── 100-classical-mechanics.json
│   ├── 133-thermodynamics.json
│   ├── 200-electromagnetism.json
│   ├── 233-quantum-mechanics.json
│   ├── 266-particle-physics.json
│   ├── 300-relativity.json
│   ├── 333-geophysics.json
│   ├── 366-astrophysics.json
│   ├── 399-condensed-matter.json
│   └── 400-nuclear-physics.json
├── math/             ← 11 files (444-700) — What CAN BE
│   ├── 444-algebra.json
│   ├── 500-calculus.json
│   ├── 533-analysis.json
│   ├── 555-topology.json
│   ├── 566-linear-algebra.json
│   ├── 600-probability.json
│   ├── 633-statistics.json
│   ├── 650-discrete-math.json
│   ├── 666-computation.json
│   ├── 699-optimization.json
│   └── 700-numerical-methods.json
└── code/             ← 11 files (777-999) — What WILL BE
    ├── 777-systems-programming.json
    ├── 800-ai-ml-engineering.json
    ├── 833-security.json
    ├── 850-data-engineering.json
    ├── 888-governance.json
    ├── 900-frontend.json
    ├── 920-backend.json
    ├── 933-devops.json
    ├── 950-integration.json
    ├── 977-automation.json
    └── 999-meta-code.json
```

Each profile contains: foundational axioms, key references, reasoning patterns, boundary conditions, and a `belongs_to` field listing which structural agents load it (typically 333-AGI, Hermes).

## The 6 Clusters of Civilization

| Cluster | Category | Elements |
|---|---|---|
| 1 | IDENTITY | 333-AGI · 555-ASI · 888-APEX |
| 2 | DESIGN | Architect · Engineer · Auditor |
| 3 | COGNITION | Math (000-333) · Physics (444-666) · Code (777-999) — 10 verbs |
| 4 | RUNTIME | Hermes · OpenClaw · OpenCode |
| 5 | INFRASTRUCTURE | arifOS (8088) · AAA (3001) · A-FORGE (7071) |
| 6 | DOMAIN | WELL (18083) · WEALTH (18082) · GEOX (8081) |

## The HEXAGON (3 Poles + 3 Institutional Functions)

```
        888-APEX
        ΦΙ JUDGE
        │
   A-AUDIT (witness function)
        │
─── AAA GATEWAY ───
   (discovery · routing)
        │
   ┌────┴────┐
   │         │
 333-AGI   555-ASI
   Δ         Ω
   │         │
 forge      Hermes
 harnesses  A-ARCHIVE
 777-forge  MakcikGPT
```

**Key insight:** The hexagon doesn't have 6 equal members. It has 3 identity poles (Δ·Ω·ΦΙ) + 3 institutional functions that carry the trinity's work at scale:
- OpenClaw = institutionalized AGI (execution metabolism)
- A-AUDIT = institutionalized APEX (witness + compliance)
- A-ARCHIVE = institutionalized ASI (memory + vault)

## APEX Scoring (Post-Restructure)

```
G = 0.31    (A=0.75 P=0.88 E=0.80 X=0.75 Φ=0.78) → HOLD (system level)
C_dark = 0.02 (down from 0.16 — spoofing risk eliminated)
W³ = 0.87 (human=0.85, AI/Kimi=0.90, external/A2A spec=0.85)
```

Note: G ≥ 0.80 threshold is for specific claims, not system-level architecture. The important signal is C_dark trajectory and all 7 zen organs non-zero.

## Gateway Verification

```bash
# Discovery (with membrane middleware header)
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover/stats

# Expected: 44 agents, 388+ skills, 308+ unique tags

# Well-known agent card (no header needed)
curl -s http://localhost:3001/.well-known/agent.json

# Expected: id=aaa-gateway, protocolVersion=1.2

# Knowledge atlas
ls /root/AAA/knowledge/*/*.json | wc -l
# Expected: 33 profile files + manifest.json + README.md
```
