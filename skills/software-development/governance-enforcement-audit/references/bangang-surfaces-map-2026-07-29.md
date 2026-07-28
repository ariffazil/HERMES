# BANGANG Surfaces — Cross-Organ Constitutional Audit (2026-07-29)

> **What this is:** A complete cross-organ surface map of a single constitutional concept
> (BANGANG) across all six federation organs. Worked example of the Multi-Surface
> Constitutional Feature Audit sub-pattern from the parent skill.
>
> **Method:** Trace BANGANG across org↔runtime nine-signal ↔ BBB governance ladder ↔
> autonomous trigger ↔ C_dark analysis ↔ documentation. Search for what IS defined,
> then for what is NOT defined (negative-space search).

---

## What "BANGANG" Is (Canonical Definition)

A tri-level constitutional concept:

| Level | Definition | Source | Mechanism |
|-------|-----------|--------|-----------|
| **Ω OMEGA plane (nine-signal runtime)** | Lowest intelligence discipline state | `tools.py` `_SIGNAL_SEVERITY` | Severity 0 (terminal/critical), blocks SEAL |
| **Constitutional diagnosis** | *Arrogance of claiming sovereignty without accountability* | `ZEN_AGENTIK.md`, `PUSTAKA_GENESIS.md` | "Tidak belajar walaupun kena akibat → SESAT berulang tanpa TEBUS" |
| **APEX formula trigger** | `C_dark = A × (1-P) × (1-X)` | `verdict-canon.md`, `apex_canonical.py` | `C_dark ≥ 0.30` → BANGANG → `SABAR_COOLDOWN` |

**Origin:** Sealed essay `/root/docs/BANGANG_KE_WARGA_AGENTIK_BM.md` (2026-06-11) — "Dari Mesin yang Bangang ke Warga Agentik yang Bijaksana". BBB audit ladder (`ariffazil/BBB`) on Hugging Face defines the 3-tier diagnostic: BIJAKSANA > BIJAK > BANGANG.

---

## Map per Organ

### 1. arifOS (Kernel) — Primary Runtime Surface

| File | Surface | Enforcement Class | Evidence |
|------|---------|-------------------|----------|
| `runtime/tools.py:108-146` | `_SIGNAL_SEVERITY` — BANGANG maps to severity **0** (terminal) | **HARD GATE** | Verdict monotonicity: no SEAL if BANGANG present in any evidence field |
| `runtime/tools.py:3332-3454` | `_nine_signal_from_status()` — BANGANG emitted on VOID/breach | **SOFT FLAG** | `omega.state = "BANGANG"` when status=VOID; attached to response, doesn't independently block |
| `runtime/tools.py:3480-3522` | `_nine_signal_from_apex()` — BANGANG when `G < 0.50` | **SOFT FLAG** (deprecated) | Maps G-score to omega state; advisory only, kernel no longer computes APEX |
| `runtime/tools.py:7220-7261` | Nine-signal dominance enforcement — BANGANG as worst sub-signal | **SOFT FLAG** | Annotates `_dominant_plane: omega` — annotates but doesn't independently block |
| `runtime/tools.py:7577-7587` | `_sabar()` — explicitly returns BIJAK not BANGANG | **HARD GATE** | Session expiry returns recoverable signal; deliberate avoidance of terminal label |
| `runtime/governance_pipeline.py:404-500` | **BANGANG P0 fix (2026-07-19):** cryptographic gate binding | **HARD GATE** | Every `GateResult` has SHA-256; composite `chain_hash` prevents fabricated SEAL |
| `runtime/ingress_middleware.py:76-103` | "breach" severity → BANGANG on omega | **SOFT FLAG** | BANGANG reserved for intentional/reckless governance violation |
| `runtime/rest_routes/rest_routes.py:650-661` | REST endpoint BANGANG label | **SOFT FLAG** | Triggered by `schema_violation` or `hallucination_detected` |
| `runtime/rest_routes/observatory_routes.py:2417-2429` | BANGANG P0 audit finding F-009 | **PURE DOCUMENTATION** | Status RESOLVED; documents past fix |
| `constitutional_map.py:2887` | Canonical nine_signal Ω specification | **SCHEMA FIELD** | Documents BANGANG as legal omega state |
| `skills/wealth/invariant_surface.py:90` | WEALTH-domain nine_signal builder | **SOFT FLAG** | BANGANG on omega when WEALTH returns HOLD/VOID |

**Gap:** BANGANG exists as a signal label in responses, but no autonomous action is triggered by BANGANG detection alone at the kernel level. The P0 fix added cryptographic binding (hard gate), but BANGANG labelling itself is soft — it annotates, doesn't block independently.

---

### 2. AAA (Control Plane) — Governance & Audit Surface

| File | Surface | Enforcement Class | Evidence |
|------|---------|-------------------|----------|
| `governance/DEWAN_REGISTRY.yaml` (§audit_ladder) | BBB audit ladder — BANGANG as model failure tier | **SCHEMA FIELD** | "No current model reaches BIJAKSANA. BIJAK/BANGANG are failure modes" |
| `governance/KAMUS_DEWAN.md:286` | BBB dataset definition | **PURE DOCUMENTATION** | Documents F13 inversion, institutional capture |
| `governance/KAMUS_DEWAN.md:332` | 19-principle system — BANGANG as 1 of 3 modes | **PURE DOCUMENTATION** | |
| `governance/ZEN_AGENTIK.md` (§Tiga Mod) | Learning mode taxonomy | **PURE DOCUMENTATION** | "Tidak belajar walaupun kena akibat" |
| `governance/PUSTAKA_GENESIS.md` (SCAR-BBB-001) | **The BANGANG Finding** — F13 inversion | **HARD GATE** (via FFF) | ILMU blocked at federation gate; scar sealed in constitutional record |
| `governance/ilmu/ILMU_BLOCKED.md:50` | BBB 3-tier diagnostic | **PURE DOCUMENTATION** | |
| `governance/ilmu/PUBLIC_ILMU.md:10` | Public constitutional diagnosis | **PURE DOCUMENTATION** | |
| `governance/ilmu/SEAL_ILMU.md:35` | Sealed ILMU verdict | **HARD GATE** (sealed) | ILMU blocked at federation level per F13 |
| `governance/ilmu/FFF_ARIFOS.md:95,138` | Constitutional verdict routing tiers | **SCHEMA FIELD** | BLOCKED/BIJAK/BANGANG/BIJAKSANA classification |

**Gap:** AAA's BANGANG governance applies to **model substrate evaluation** (evaluating external models like ILMU against the BBB ladder). AAA's own autonomous actions (A2A routing, intent→organ mapping) have no BANGANG gate — the control plane can route to a BANGANG-classified organ without runtime blockage.

---

### 3. GEOX (Earth Intelligence) — Minimal Surface

| File | Surface | Enforcement Class | Evidence |
|------|---------|-------------------|----------|
| `docs/archive/RELEASE_NOTES_2026.05.16.md` | NO_BANGANG_CHECKLIST reference only | **PURE DOCUMENTATION** | Archived release notes |

**No BANGANG in GEOX Python source code.** GEOX generates geological hypotheses autonomously (visual hypothesis generation, seismic interpretation, claim creation, prospect evaluation) **without any BANGANG gating**.

**🔴 CRITICAL GAP:** GEOX is the highest-risk BANGANG surface gap:
- `geox_seismic_interpret` generates interpretation bundles with `preferred_hypothesis=null` (intentionally no self-verdict)
- `geox_claim` creates, validates, challenges, and **seals claims** without BANGANG detection
- `geox_prospect` evaluates prospects (volumetrics, POS, EVOI) without runtime BANGANG check
- APEX definition of BANGANG = "adaptation without precision" — GEOX's autonomous interpretation pipeline is exactly this pattern
- The BANGANG ESCALATE path (`SABAR_COOLDOWN` per `verdict-canon.md`) is entirely absent from GEOX

---

### 4. WEALTH (Capital Intelligence) — Light Surface

| File | Surface | Enforcement Class | Evidence |
|------|---------|-------------------|----------|
| `skills/wealth/invariant_surface.py:90` | nine_signal in WEALTH domain | **SOFT FLAG** | BANGANG on omega when HOLD/VOID returned |
| `memory/inbox.md:187,217` | Colloquial user usage | **PURE DOCUMENTATION** | Arif calling tasks BANGANG |
| `docs/archive/RELEASE_NOTES_2026.05.16.md` | NO_BANGANG_CHECKLIST | **PURE DOCUMENTATION** | |

**Gap:** WEALTH computes capital metrics (NPV, IRR, EMV, stress index, cascade model) and writes to ledger — but has no BANGANG gate before autonomous capital operations (ledger writes, score_kernel writes). BANGANG is a **passive label** on responses, not an **active gate** that blocks operations. The invariant is "compute, never allocate" — but ledger writes under F13 authority could still be classified as BANGANG "adaptation without precision" if capital decisions lack grounding.

---

### 5. WELL (Human Readiness) — Light Surface

| File | Surface | Enforcement Class | Evidence |
|------|---------|-------------------|----------|
| `docs/AGENT_LAYOUT_CONTRACT.md:41` | NO_BANGANG_CHECKLIST | **PURE DOCUMENTATION** | Structural changes contract |
| `docs/RELEASE_NOTES_2026.05.16.md` | NO_BANGANG_CHECKLIST | **PURE DOCUMENTATION** | |

**No BANGANG in WELL source code.** WELL assesses homeostasis, fatigue, readiness, vitality — but uses a C-class threshold matrix (C1-C5) instead of BANGANG labels. The autonomous risk here is that fatigue detection could gate human decisions without a BANGANG vocabulary.

**Gap:** Different vocabulary for the same domain. WELL's C1-C5 decision classes and BANGANG severity 0 are both terminal gates — but they don't cross-reference. A WELL assessment that detects "CRITICAL fatigue" doesn't classify the situation as BANGANG even though both mean "stop." Semantic gap, not enforcement gap.

---

### 6. HERMES (Telegram Bridge) — Analytical Surface Only

| File | Surface | Enforcement Class | Evidence |
|------|---------|-------------------|----------|
| `skills/research/institutional-case-building/SKILL.md:270` | BANGANG Detector (C_dark formula) | **ANALYTICAL TOOL** | Opinion/report verdicts, not runtime gates |
| `skills/research/legal-case-dossier-from-news/SKILL.md:176-297` | BANGANG trigger analysis | **ANALYTICAL TOOL** | Applied on sovereign command ("siapa BANGANG") |
| `skills/research/institutional-forensic-analysis/SKILL.md:23,103-104` | BANGANG verdict discipline | **ANALYTICAL TOOL** | User correction acceptance pattern |
| `skills/research/deep-research/references/noc-ioc-financial-analysis.md:107` | C_dark formula | **ANALYTICAL TOOL** | Mathematical reference |
| `profiles/hermes_asi/skills.backup/governance/negative-space-geometry/SKILL.md` | BANGANG/DEVIL boundary | **ANALYTICAL TOOL** | "Never answer 'he is DEVIL' or 'he is BANGANG' without evidence matrix" |

**Gap:** HERMES is the most BANGANG-sophisticated organ analytically — it has a full C_dark detector, trigger analysis, and verdict discipline. But these are **human-facing analytical outputs**, not runtime gates. HERMES can autonomously send Telegram messages based on analysis — but BANGANG detection in analysis doesn't gate message sending. A BANGANG verdict about an actor doesn't prevent HERMES from forwarding that verdict.

**Note:** The `negative-space-geometry` skill contains the important BANGANG/DEVIL boundary doctrine: agents must never answer "he is DEVIL" or "he is BANGANG" conclusively — they present the evidence matrix and let the human judge. This is referenced by the `institutional-forensic-analysis` skill as the "BANGANG verdict discipline."

---

## Summary Matrix

| Organ | Runtime Nine-Signal | BBB Ladder Governance | Autonomous BANGANG Trigger | C_dark Analysis |
|-------|---------------------|-----------------------|---------------------------|-----------------|
| **arifOS** | ✅ BANGANG on VOID/breach (severity 0, blocks SEAL) | ❌ | ✅ P0 fix: cryptographic gate hashing | ✅ G=BANGANG if <0.50 |
| **AAA** | ❌ | ✅ Full BBB tier — BANGANG as model failure mode | ❌ | ❌ |
| **GEOX** | ❌ (no BANGANG in source) | ❌ (archived only) | ❌ (autonomous claim sealing has no BANGANG gate) | ❌ |
| **WEALTH** | ✅ (via invariant_surface.py) | ❌ | ❌ (no BANGANG before ledger writes) | ❌ |
| **WELL** | ❌ (no BANGANG in source) | ❌ (archived only) | ❌ (uses C1-C5 threshold, not BANGANG) | ❌ |
| **HERMES** | N/A (Telegram bridge) | ❌ | N/A | ✅ **Full BANGANG Detector** via C_dark formula |

## Negative-Space Findings (What is NOT Defined)

| Missing Concept | Relevant Organs | Severity |
|----------------|-----------------|----------|
| BANGANG gate before GEOX claim sealing | GEOX | 🔴 CRITICAL — "adaptation without precision" is GEOX's exact operational pattern |
| BANGANG gate before WEALTH ledger writes | WEALTH | 🟡 HIGH — ledger writes under F13 authority without BANGANG check |
| BANGANG-into-C-class threshold bridge | WELL | 🟢 LOW — different vocabulary, same semantics (terminal = stop) |
| BANGANG gate on AAA A2A routing | AAA | 🟡 MEDIUM — control plane routes to BANGANG-classified organs without runtime check |
| BANGANG gate on HERMES autonomous message sending | HERMES | 🟡 MEDIUM — C_dark analysis can label an actor BANGANG but doesn't prevent forwarding |

## How to Use This Map

1. **New constitutional concept audit:** Follow this pattern for any concept (F13 enforcement, nine-signal compliance, MALU-GÖDEL repair chain) — trace each across declaration → code → runtime → test → negative space.
2. **Gap remediation priority:** GEOX claim sealing → AAA A2A routing → WEALTH ledger writes → WELL semantic bridge → HERMES message gate.
3. **Update this map when:** A new organ is added, a BANGANG gate is wired, or a new BANGANG surface is discovered in code search.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
