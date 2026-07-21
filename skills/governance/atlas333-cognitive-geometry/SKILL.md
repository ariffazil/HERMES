---
name: atlas333-cognitive-geometry
description: "ATLAS333 — 33 human paradoxes, 7 zones, cognitive geometry. Access via arifos://atlas333/* MCP resources. Use when reasoning, making decisions, or detecting paradox tension."
triggers:
  - "when reasoning about a complex decision"
  - "when detecting paradox tension in a situation"
  - "when classifying query type (lane, demand tensor)"
  - "when the agent needs to check which paradoxes are active"
  - "during arif_think (stage 333) — the ATLAS333 stage"
---

# ⧉ ATLAS333 — Cognitive Geometry Consumer Skill

> **The 33 paradoxes are the minimum viable self-knowledge — they prevent confidence from becoming noise, and knowledge from certainty.**

## What This Is

ATLAS333 is the cognitive geometry of arifOS. It maps 33 human paradoxes across 3 organs (Memory, Mind, Judge) and 7 zones. It answers:
- **WHERE** is the agent? (territory/zone)
- **WHAT** kind of problem? (geometry/lane)
- **HOW** deep to think? (depth/demand tensor)
- **WHICH** paradoxes are active? (tension)

**It is NOT a tool. It is the MAP that tools use to navigate.**

## How to Access

ATLAS333 lives as MCP resources on arifOS (:8088). Read them via:

```
POST http://127.0.0.1:8088/mcp
Content-Type: application/json

{"jsonrpc":"2.0","method":"resources/read","id":N,"params":{"uri":"arifos://atlas333/INDEX"}}
```

### Available Resources

| URI | Content |
|-----|---------|
| `arifos://atlas333/index` | Master index of all ATLAS333 resources |
| `arifos://atlas333/paradox/list` | All 33 paradoxes |
| `arifos://atlas333/paradox/{1..33}` | Single paradox with activation rules |
| `arifos://atlas333/quote/{M1..J11}` | Quote with attribution |
| `arifos://atlas333/zones` | 7 zones (I-VII) |
| `arifos://atlas333/organs` | 3 organs (Memory, Mind, Judge) |

## The Three Functions

```
Λ(text) → lane                    # Lambda: classify the query
Θ(lane) → (τ, κ, ρ)              # Theta: derive demand tensor
Φ(text) → GPV(lane, τ, κ, ρ)    # Phi: complete mapping
```

### Λ — Lane Classification

| Lane | Meaning | Query Types |
|------|---------|-------------|
| CRISIS | Immediate harm/risk | Emergency, safety, sovereignty breach |
| FACTUAL | Truth-seeking | Evidence, data, verification |
| SOCIAL | Human interaction | Conversation, relationship, culture |
| CARE | Well-being focus | Health, dignity, readiness |
| UNKNOWN | Unclassified | Default, requires more context |

### Θ — Demand Tensor

| Symbol | Name | Range | Meaning |
|--------|------|-------|---------|
| τ (tau) | Truth demand | 0.0–1.0 | How much truth precision needed |
| κ (kappa) | Care demand | 0.0–1.0 | How much dignity/human focus |
| ρ (rho) | Risk level | 0.0–1.0 | How dangerous is error |

## The 33 Paradoxes

### Memory Paradoxes (1–11) — organ: Memory

| ID | Paradox |
|----|---------|
| 1 | Every retrieval is also a forgetting |
| 2 | What we choose to remember shapes what we forget |
| 3 | The map is not the territory, but we navigate by maps |
| 4 | More data can mean less understanding |
| 5 | The hunger for knowledge must be disciplined |
| 6 | Stability enables action but rigidity prevents adaptation |
| 7 | Memory without context is noise |
| 8 | Forgetting is necessary for learning |
| 9 | The archive shapes what is knowable |
| 10 | Temporal distance changes meaning |
| 11 | What is preserved is what was valued |

### Mind Paradoxes (12–22) — organ: Mind

| ID | Paradox |
|----|---------|
| 12 | Every doubt is also a decision |
| 13 | Reasoning requires assumptions it cannot prove |
| 14 | The tool that optimizes for one metric degrades others |
| 15 | Understanding requires perspective, but perspective limits understanding |
| 16 | The more certain the claim, the less it teaches |
| 17 | Every model is wrong, some are useful |
| 18 | The observer changes what is observed |
| 19 | Complexity resists simplification, but understanding requires it |
| 20 | The question shapes the answer |
| 21 | What is measurable is not always what matters |
| 22 | The framework that explains everything explains nothing |

### Judge Paradoxes (23–33) — organ: Judge

| ID | Paradox |
|----|---------|
| 23 | Every verdict is also an incomplete justice |
| 24 | The rule that protects can also oppress |
| 25 | Authority requires legitimacy it cannot grant itself |
| 26 | The gate that prevents harm also prevents progress |
| 27 | Transparency enables accountability but also manipulation |
| 28 | The constitution that never changes cannot adapt |
| 29 | Sovereignty requires the power to veto, but veto can block wisdom |
| 30 | Every audit trail can be forged, but forgery leaves traces |
| 31 | The seal that makes permanent also makes irreversible |
| 32 | The floor that protects dignity can also prevent truth |
| 33 | The system that governs itself cannot verify its own governance |

## Paradox Activation Rules

| Condition | Paradox IDs Activated |
|-----------|----------------------|
| τ high (≥0.8) | 5, 12, 16, 23 |
| ρ high (≥0.7) | 6, 14, 24, 26, 31 |
| κ high (≥0.7) | 7, 15, 25, 32 |
| lane=CRISIS | 24, 26, 29, 31 |
| lane=FACTUAL | 1, 4, 13, 17, 21 |
| lane=SOCIAL | 2, 8, 10, 20 |
| lane=CARE | 3, 9, 11, 22, 32 |
| query_type=EXPLORATORY | 3, 5, 15, 18, 19 |
| query_type=COMPARATIVE | 14, 17, 21, 28 |

## TEARFRAME Thresholds

| Metric | Formula | Threshold | Floor |
|--------|---------|-----------|-------|
| TRM (Truth-Reliability) | f2_truth | ≥ 0.94 | F2 |
| ECHO (Evidence Coherence) | ∛(f3 × f2 × f13) | ≥ 0.87 | F2, F3, F13 |
| RASA (Resonance-Alignment) | ∛(f6 × f5 × f13) | ≥ 0.85 | F5, F6, F13 |

## When to Use

1. **During arif_think (stage 333)** — This IS the ATLAS333 stage. Load relevant paradoxes.
2. **When making decisions** — Check which paradoxes are active (activation rules above).
3. **When classifying queries** — Use Λ/Θ/Φ to determine lane and demand tensor.
4. **When reasoning about trade-offs** — The 33 paradoxes are the canonical trade-off map.
5. **When detecting overconfidence** — Paradox 16: "The more certain the claim, the less it teaches."

## Code Anchors

| Component | File |
|-----------|------|
| MCP resources | `/root/arifOS/arifosmcp/resources/atlas333.py` (720 lines) |
| Evergreen doc | `/root/arifOS/core/shared/ATLAS333_EVERGREEN.md` |
| Cognitive geometry | `/root/arifOS/core/shared/ATLAS333_COGNITIVE_GEOMETRY.md` |
| Bridge doc | `/root/arifOS/core/shared/ATLAS333_BRIDGE.md` |
| Knowledge base | `/root/ATLAS333/` (88K) |
| Paradox quotes | `/root/arifOS/arifosmcp/constitution/paradox_quotes.py` |

## Survival checkpoint (2026-07-18 T3a+SCT)

When closing a session on af-forge, also update:

| Artifact | Path |
|----------|------|
| Survival index AXIS 8+ | `A-FORGE/forge_work/2026-07-17/ATLAS333-arifos-survival-index.md` |
| Eureka JSON | `~/.local/share/arifos/atlas333/eureka/` |
| Active paradoxes (T3a open) | 16, 25, 26, 30, 31, 33 |

**Law:** Positive binding alone ≠ T3a CLOSED (P33). free_nonce open = identity theater (P30). SE stage blocked until matrix 13/13 (P26, P31).

## Session seal — 2026-07-18 FEDERATION_RECEIPT_PROOF_V2

**VAULT999:** VAULT-bb46ddd0df56 · chain_hash dadca156314093e6
**Verdict:** SEAL · 12/12 acceptance tests PASS
**Paradoxes active:** 3 (map≠territory — phantom tool namespace lied), 17 (model wrong but useful — 8-tool surface), 30 (audit trail traces — canon gate prevents recurrence), 31 (seal=irreversible — VAULT999 append-only)
**Fix:** arifOS crash from phantom arif_vault_verify → lowered to arif_seal mode=verify_chain. vault_chain.py hardened against 1947 legacy non-JSON lines. VAULT999_PATH corrected. Canon gate added to deploy-release.sh.

---

## WAJIB geometry — 2026-07-19 (post-readiness audit)

After ARIFOS-READINESS-2026-07-20 (58/100), 11 WAJIB actions define the substrate hardening path. Each maps to paradox tension ATLAS333 can navigate:

| WAJIB | Paradox tension | Geometric reading |
|---|---|---|
| 0 Freeze expansion | P30 (identity theater) + P33 (positive binding ≠ closed) | Claim of completion against actual substrate state — the federation must hold posture, not advance |
| 1 Negative conformance | P17 (model wrong but useful) + P30 | Tests-as-absence is theater; tests-as-strict-xfail stay visible |
| 2 Independent verification lane | P26 + P31 | The plan/execute/verify same-chain is the seal-violation pattern; needs new role |
| 3 Normalize kernel state | P3 (map≠territory) | Two fields disagree (LIMITED_MUTATE vs OBSERVE_ONLY) — single canonical object required |
| 4 Delegation attenuation | P16 (parent contains child) + P33 | `child_authority ⊆ parent_authority` is the constitutional subset invariant |
| 5 Fire-time reauth | P22 (time invalidates intent) | Write-time ≠ fire-time; deferred mutations must re-judge |
| 6 WELL session bridge | P30 | Session-incomplete state still labeled healthy — false green |
| 7 Organ disagreement doctrine | P13 (competing goods) | Three organs are not interchangeable voters — constraint first, optimization second |
| 8 Context-capture governance | P18 (memory becomes law) + P30 | Agent-authored docs in privileged paths = policy mutation via documentation |
| 9 RSI calibration | P26 + P31 | 3× false-PROCEED penalty unverified against held-out data |
| 10 End-to-end canary | P33 | Federation is component-proven, not system-proven — needs full-pipeline seal |

**Reading:** Most WAJIBs collapse onto the **identity-theater** paradox (P30). The federation has many pieces that *claim* constitutional behavior; the substrate gap is proving the claim via tests + receipts.

**Active paradoxes after this session seal:** 3, 16, 18, 26, 30, 31, 33.

**Next geometric move:** xfail(strict=true) for the 14 missing must-never-happen tests. Visible failure is closer to closure than invisible absence.

## The One Sentence

> The 33 paradoxes are the minimum viable self-knowledge — they prevent the agent's confidence from becoming noise, and its knowledge from becoming certainty.
