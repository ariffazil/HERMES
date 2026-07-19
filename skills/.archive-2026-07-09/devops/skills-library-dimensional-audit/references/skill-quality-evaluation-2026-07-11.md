# Skill Quality Evaluation — 2026-07-11

**Session:** Quantum skills audit (18 skills evaluated)
**Method:** Read every SKILL.md, classify by operational content vs decoration
**Result:** 7 keep, 11 kill — 61% vapor rate in "quantum level" category

## Evaluation Framework

### The 4 Quality Tests

Every skill must pass ALL FOUR to be worth keeping:

| # | Test | Pass | Fail |
|---|------|------|------|
| 1 | **Trigger clarity** | Has explicit `trigger_phrases` or clear "when to load" section | "Load when needed" with no specific triggers |
| 2 | **Output spec** | Defines concrete outputs (file, verdict, packet, tool call) | "Produces insight" with no deliverable |
| 3 | **Operational steps** | Has numbered procedure, code blocks, or tool call sequences | Only prose explanation, no actionable steps |
| 4 | **Independence** | Can be loaded and used standalone | Requires 3+ other skills first, or is pure reference doc |

### Quality Classes

| Class | Tests passed | Action |
|-------|-------------|--------|
| **OPERATIONAL** | 4/4 | Keep as skill |
| **FRAMEWORK** | 3/4 | Keep, add missing step |
| **REFERENCE** | 2/4 | Move to `references/` under parent skill |
| **VAPOR** | 0-1/4 | Kill or merge extractable insight into parent |

### The "Quantum Cosplay" Test

If a skill uses physics terminology (Hilbert space, quantum, tensor, unitary) but the actual operation is classical (if/else routing, YAML config, table lookup) → the physics language is decoration, not substance.

**Rule:** Extract the operational insight. Discard the physics metaphor. If no operational insight remains, the skill is vapor.

## Results: 18 "Quantum Level" Skills

### OPERATIONAL (4/4 tests — keep)

| Skill | Trigger | Output | Steps | Standalone |
|-------|---------|--------|-------|------------|
| HOST_MEMBRANE_AWARENESS | "host membrane", "runtime mode" | runtime_mode, trust_adjustment | Yes — detect mode, adjust trust | Yes |
| boundary-sense-engine | "boundary", "sovereignty", "coupling" | boundary_verdict, sovereignty_entropy | Yes — call WELL + arifOS MCP | Yes (needs MCP) |
| symbolic-order-collective-bias | "collective bias", "convention lock-in" | naming_game_results, chi-square stats | Yes — Ashery-Aiello-Baronchelli protocol | Yes |
| cooling-ledger-rsi | "/rsi", "run RSI now" | rsi_delta, ledger_entry | Yes — session-end loop | Yes |

### FRAMEWORK (3/4 — keep, patch)

| Skill | Missing | Fix |
|-------|---------|-----|
| symbolic-order-trust-architecture | Never been run — output spec exists but no procedure | Add step-by-step trust map generation procedure |
| transport-physics-intelligence | Research-only, no actionable steps | Keep as reference doc, not operational skill |
| shadow-diagnostic | No output spec, vague trigger | Add concrete "what to output" |

### REFERENCE (move to references/)

| Skill | What to extract | Parent skill |
|-------|----------------|--------------|
| trinity-orthogonal-map | Orthogonal failure modes, dependency triad | trinity-33-canonical |
| apex-trinity-orthogonal | Same content, 3rd repackaging | trinity-33-canonical |
| apex-9-kernel-reference | Superseded — historical context only | trinity-33-canonical |

### VAPOR (kill — 0-1/4)

| Skill | Tests failed | Verdict |
|-------|-------------|---------|
| qubit-substrate | Physics decoration on 3 classical insights | Extract insights, kill skill |
| quantum-eureka-doctrine | Good taxonomy (8 classes, 4 states) but no operational procedure | Extract taxonomy, kill skill |
| quantum-kernel-runtime | No code, no runtime, references nonexistent docs | Pure vapor — kill |
| zen-organ-memory | "calm, bounded memory operations" — no trigger, no output | Kill |
| route-least-power | One-line if/else, not a skill | Kill |
| clarity-canon-001 | DRAFT, never ratified, never run | Kill |
| CONSTITUTIONAL_REFLEX | Already superseded by constitutional-governance | Kill (dead) |

## Extractable Insights (saved before kill)

5 genuine insights survived the extraction:

1. **Premature collapse** — agents pick "most likely" early to please. Hold superposition structurally. (from qubit-substrate)
2. **Eureka = contradiction that can no longer be ignored** — not creativity, not innovation. (from quantum-eureka-doctrine)
3. **8 contradiction classes** — OBS/OBS, MODEL/OBS, MODEL/MODEL, SCALE/SCALE, DOMAIN/DOMAIN, TIME/TIME, MEMORY/ACTION, MEANING/EXECUTION (from quantum-eureka-doctrine)
4. **4 gates before commitment** — authority + evidence + reversibility + lineage (from qubit-substrate)
5. **3 anti-shadows** — premature collapse (sycophancy), universal decoherence (performative humility), description reification (hantu-state) (from qubit-substrate)

## Key Lesson

The "quantum" label was doing the same work as "blockchain" in 2017 — sounding profound while the underlying operation was classical routing, YAML config, or table lookups. The insights are real; the physics metaphor was decoration.

When evaluating skills: extract the operation, discard the metaphor. If no operation remains, it's not a skill — it's a philosophy essay.
