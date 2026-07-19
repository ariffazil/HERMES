---
name: geox-federation-mcp-driver-enrichment
version: "1.0.0-2026.07.08"
description: Consolidated enrichment for geox-federation-mcp-driver — merged unique core knowledge from 9 GEOX fragment skills into a single reference appendice.
forged: 2026-07-08
forged_by: FORGE subagent (delegated extraction task)
absorbed_from:
  - geox-claim-grammar
  - geox-constitution
  - geox-contradiction-engine
  - geox-earth-evidence
  - geox-epistemic-ladder
  - geox-petrophysics-bounds
  - geox-redteam-hantu
  - geox-scientific-writing
  - geox-000-999-deployment-macro
target_skill: geox-federation-mcp-driver (/root/.hermes/skills/devops/geox-federation-mcp-driver/SKILL.md)
---

# GEOX Federation MCP Driver — Consolidated Enrichment

> This document extracts the UNIQUE core knowledge from 9 GEOX domain-specific fragment skills and merges it into a single reference that enriches the `geox-federation-mcp-driver` skill. Load alongside the parent skill whenever driving GEOX tools to ensure constitutional, epistemic, and domain enforcement.

---

## §1 — Claim Grammar (from `geox-claim-grammar`)

### Claim Structure

Every geological claim in GEOX must be expressible as:

```yaml
claim:
  text: "<specific, falsifiable statement>"
  rung: OBSERVED | DERIVED | INTERPRETED_LOCAL | PROCESS_HYPOTHESIS | EARTHMODEL | DECISIONSUPPORT
  evidence_for: [{artifact_ref: <sha256>, weight: 0.0-1.0}]
  evidence_against: [{artifact_ref: <sha256>, weight: 0.0-1.0}]
  missing_tests: ["What data would prove this wrong?"]
  acrisk: 0.0-1.0
  alternatives:
    - description: "rival hypothesis"
      support: ["evidence_item_1"]
```

### Location First — SCAR `scar_1783404210900`

Every location-bearing claim MUST include:

| Field | Required | Notes |
|---|---|---|
| `coordinates.lat` | Yes | Decimal degrees North |
| `coordinates.lon` | Yes | Decimal degrees East |
| `coordinates.crs` | Yes | Always `"EPSG:4326"` |
| `positional_accuracy_m` | Yes | Radius of confidence in meters |
| `source_tag` | Yes | One of: `VERIFIED_SURVEY`, `VERIFIED_LITERATURE`, `ESTIMATED`, `UNKNOWN` |
| `source_reference` | Conditional | Required when `source_tag=VERIFIED_LITERATURE` |

**Source tag confidence caps:** `VERIFIED_SURVEY` → 0.95, `VERIFIED_LITERATURE` → 0.85, `ESTIMATED` → 0.60, `UNKNOWN` → 0.30.

**Rule:** No `UNKNOWN` coordinates for `DECISIONSUPPORT` rung. `INTERPRETED_LOCAL` and above: `ESTIMATED` or better.

### Multi-Hypothesis Mandate

No single hypothesis without alternatives. For every `INTERPRETED_LOCAL`+ claim: primary hypothesis, ≥1 alternative, evidence for each, distinguishing test.

### Forbidden Phrases (immediate RED-TEAM review)

- "proven reservoir" — reservoir never "proven" until produced
- "confirmed hydrocarbon" — only DST/MDT confirms mobile HC
- "100% confidence" — impossible in subsurface
- "certain" / "definitely" — subsurface certainty is oxymoronic
- Coordinates "from memory" — must use ESTIMATED or better
- "analogous to" without quantifying similarity

### Claim Types

| Type | Template |
|---|---|
| FACT | `<property> = <value> at <location>` |
| INTERPRETATION | `<observation> suggests <process>` |
| SPECULATION | `<analogy> implies <possibility> at <undrilled_location>` |
| COMPARISON | `<A> similar to <B> in X, differs in Y` |
| CHALLENGE | `<claim> questioned because <contradicting_evidence>` |

---

## §2 — Constitution (from `geox-constitution`)

### Prime Law

**Physics > Narrative. Earth > Model. Evidence > Belief.**

### GEOX-Specific Constitutional Floors

| Floor | Interpretation |
|---|---|
| **F2 TRUTH** | τ ≥ 0.99 accuracy or declare uncertainty. Output labels: CLAIM / PLAUSIBLE / HYPOTHESIS / ESTIMATE / UNKNOWN |
| **F4 CLARITY** | ΔS ≤ 0. Units mandatory. Every output reduces entropy |
| **F9 ANTI-HANTU** | Physics > Narrative. Earth > Model. Evidence > Belief |
| **F1 AMANAH** | All changes reversible or flagged |
| **F11 AUDIT** | Full provenance chain on every claim |
| **F13 SOVEREIGN** | Arif vetoes; machine never self-seals irreversible |

### 888 HOLD Triggers (call immediately)

- `rm -rf`, `DROP TABLE`, `docker volume rm`
- `git push --force`, `git rebase`
- Production deployment without test pass
- Secret exposure or rotation
- VAULT999 chain writes
- Caddy reload (production traffic)
- VPS restart/stop
- Non-canonical tool surfaces or shadow schemas

### One Root, One Registry

- Never create competing schemas, shadow tools, or convenience bridges
- Every renderable: `artifact_ref`, source tool, timestamp/session, modality, verdict, risk metadata
- Frontend is a lens, not a brain — GUI may not invent geology

### Binary Transport Doctrine

Large 3D data travels via MCP resources, NOT JSON tool responses:
1. Tool envelope (JSON, small): `{renderable: true, cube_manifest_uri: "geox://render/cubes/CUBE123/manifest"}`
2. Manifest (JSON, MCP resource): dims, LODs, brick shape, CRS
3. Bricks (binary, MCP resource): LOD0=uint8+wavelet, LOD1=int16+zstd, LOD2=float32
4. GPU path: `ArrayBuffer → Float32Array (zero-copy) → WebGL 3D texture → shader`

---

## §3 — Contradiction Engine (from `geox-contradiction-engine`)

### Core Pattern

Every interpretation must list alternatives. Every alternative must list what evidence would support it vs the primary claim.

### Contradiction Types

| Type | Detection |
|---|---|
| **Evidence gap** | Mismatch between log and seismic evidence (e.g. high Sw but DHI present) |
| **Physics violation** | Exceeds CANON-9 bounds (e.g. porosity > 0.45 without explanation) |
| **Single-well certainty** | Regional interpretation from < 3 wells |
| **Uncalibrated pressure** | Fluid gradient without DST/MDT |
| **Temporal drift** | Newer evidence supersedes older claim |
| **Modal contradiction** | Seismic says flat spot, logs say water |
| **Epistemic collapse** | "Bright spot = hydrocarbon" — skips AVO, rock physics, fluid analysis |

### Required Contradiction Scan Fields

```yaml
contradiction_scan:
  status: PASS | WARN | FAIL
  contradictions_found: []
  alternatives_evaluated: 2
  missing_evidence: ["DST in zone X"]
```

### Enforcement

- Every INTERPRETATION+ claim: ≥ 1 alternative
- Every claim must pass contradiction scan before SEAL
- Contradictions are intellectual honesty, not failures
- A claim with no alternatives is a weak claim

---

## §4 — Earth Evidence Discipline (from `geox-earth-evidence`)

### Artifact References (not raw paths)

```
✅ GOOD: artifact_ref = "geox://wells/north_malacca_cdp_2024"
❌ BAD:  artifact_ref = "/data/seismic/stack_mukah_2023.sgy"
```

### Uncertainty Language

| Confidence | Language |
|---|---|
| 0.85–0.90 | "High confidence" — multiple independent lines |
| 0.70–0.84 | "Moderate confidence" — single dataset, analog support |
| 0.50–0.69 | "Low confidence" — regional analog, limited data |
| < 0.50 | "Hypothesis" — needs test |

### GEOX → WEALTH Handoff Protocol

```
1. GEOX.geox_prospect() → G_factor, risk, volume estimates
2. WEALTH.wealth_compute_evoi() → uses GEOX inputs
3. WEALTH.wealth_judge_handoff() → submit to arifOS
```

**Never submit capital decisions to WEALTH without GEOX evidence first.**

### Anti-Patterns

- Using raw file paths as artifact references
- Claiming > 0.90 confidence on single-well interpretation
- Bypassing contradiction scan
- Making policy claims (GEOX computes, arifOS judges)
- Submitting to WEALTH without GEOX evidence

### Pre-Flight Check

```bash
curl -sf http://localhost:8081/health && echo "✅ GEOX" || echo "❌ GEOX DOWN"
```

---

## §5 — Epistemic Ladder (from `geox-epistemic-ladder`)

### The 7-Rung Ladder

| # | Rung | Meaning | UI Color |
|---|---|---|---|
| 1 | **OBSERVED** | Direct sensor reading — the only rung that is "true" physically | Green |
| 2 | **DERIVED** | Computed from OBSERVED via bounded, validated transform | Blue |
| 3 | **INTERPRETED_LOCAL** | Single-well geological interpretation | Cyan |
| 4 | **PROCESS_HYPOTHESIS** | Depositional/environmental process hypothesized | Amber |
| 5 | **EARTHMODEL** | Multi-well + seismic integrated 3D/4D narrative | Purple |
| 6 | **DECISIONSUPPORT** | Formal recommendation with quantified uncertainty + risk | Magenta |
| 7 | **HUMAN JUDGMENT** | Arif's final decision after reviewing all evidence | Red/Gold |

### Iron Rule: Lower Rung ALWAYS Beats Higher

- A DERIVED porosity of 0.22 is MORE TRUE than an EARTHMODEL that says 0.18
- A PROCESS_HYPOTHESIS must be challenged if it conflicts with OBSERVED data
- HUMAN JUDGMENT can override any rung, but only after viewing all evidence

### Forbidden Moves

| Move | Why |
|---|---|
| INTERPRETED → CLAIM without evidence chain | Skips uncertainty |
| EARTHMODEL → FACT | Models are never facts |
| Single well → Basin-wide conclusion | Spatial extrapolation without data |
| "Bright spot = gas" without fluid substitution | AVO classes I-IV can mimic HC |
| Correlation without chronostratigraphic constraint | Time-transgressive surfaces |

### Detection Rules

- String "the reservoir" without `EpistemicRung` → flag
- Number without uncertainty band (P10/P50/P90) at INTERPRETED+ → flag
- Single well log labeled EARTHMODEL → flag
- HUMAN_JUDGMENT without `888_HOLD` or Arif's signature → flag
- Rung ≥ 4 without `evidence_for`, `evidence_against`, `missing_tests` → flag

---

## §6 — Petrophysics Bounds (from `geox-petrophysics-bounds`)

### Canonical Transforms

| Property | Inputs | Method | Bounds |
|---|---|---|---|
| Vsh | GR, SP, N | Linear, Larionov, Clavier, Steiber | 0.0–1.0 |
| Porosity (density) | RHOB, ρma, ρf | Density | 0.0–0.45 |
| Porosity (neutron) | NPHI | Neutron | 0.0–0.45 |
| Porosity (sonic) | DT | Wyllie, Raymer-Hunt | 0.0–0.40 |
| Sw (Archie) | Rt, phi, Rw, a, m, n | Archie | 0.0–1.0 |
| Sw (Simandoux) | Rt, phi, Rw, Vsh | Simandoux | 0.0–1.0 |
| Sw (Indonesia) | Rt, phi, Rw, Vsh | Indonesia | 0.0–1.0 |
| AI | Vp, ρ | Acoustic impedance | > 0 |
| VP/VS | Vp, Vs | Ratio | 1.4–3.0 |

### QC Rules for Log Curves

| Check | Range | Action |
|---|---|---|
| GR | 0–500 API | Flag out-of-range |
| RHOB | 1.0–3.5 g/cc | Flag out-of-range |
| NPHI | -0.05–0.60 V/V | Flag out-of-range |
| DT | 40–300 µs/ft | Flag out-of-range |
| Depth monotonicity | Strictly increasing | Reject if non-monotonic |
| Null % | < 50% | Warn if high null |
| Depth step consistency | ±10% of expected | Warn if irregular |

### Critical Rules

1. **Permeability is always empirical** — never present as deterministic truth
2. **Pressure needs calibration** — never use gradient alone without DST/MDT
3. **Archie parameters are assumptions** — a=1.0, m=2.0, n=2.0 are defaults; document any deviation
4. **Fluid contacts need pressure confirmation** — resistivity alone cannot prove fluid type
5. **Every output declares equations_used, assumptions, limitations**

### Forbidden

- Predicting permeability without stating it's empirical
- Claiming fluid type from resistivity alone
- Sw > 1.0 or < 0.0 without explanation
- Porosity > 0.45 without explanation (unconsolidated sands / fractured carbonates)

---

## §7 — Red-Team Hantu (from `geox-redteam-hantu`)

### Guardian Checklist (run before every merge)

**Tool Surface:**
- Every tool in `CANONICAL_PUBLIC_TOOLS` is callable at runtime
- No phantom tools (in registry but not callable)
- No shadow tools (callable but not in registry)
- Tool names follow `geox_<domain>_<action>` convention

**Schema:**
- No ad-hoc JSON shapes — everything Pydantic
- No TypeScript types diverging from Python Pydantic
- No `Any` types that should be specific

**Governance:**
- Every response carries `session_id` + `actor_id`
- No `"geox-no-session"` or `"geox-unknown"` sentinels
- Every renderable carries `acrisk_score` + `arifos_verdict`
- Irreversible tools have 888 HOLD gate
- Mutations cannot bypass arifOS

**GUI:**
- No component does geology without calling GEOX MCP
- No silent epistemic upgrade (HYPOTHESIS → CLAIM)
- ACRisk visible on load (not behind menu)
- HOLD state locks mutation

### Common Hantu Patterns

| Pattern | Severity | Detection |
|---|---|---|
| Tool in registry but not callable | 🔴 CRITICAL | `test_registry_runtime_truth.py` |
| Frontend parsing raw envelope fields | 🟡 MEDIUM | Grep `result\[\"` in React code |
| LLM saying "proven reservoir" | 🔴 CRITICAL | Forbidden phrase scan |
| Smooth surface hiding interpolation | 🟡 MEDIUM | Check `claim_state` |
| Submit button ignoring HOLD | 🔴 CRITICAL | Trace mutation paths |
| Schema drift (TS ≠ Pydantic) | 🟡 MEDIUM | Contract parity tests |

### Immediate Block Triggers

- New `"geox-"` tool without `CANONICAL_PUBLIC_TOOLS` update
- Frontend `fetch()`/`axios`/`http` directly to geology API
- Convenience transform mutating scientific meaning
- Any 888 bypass path

---

## §8 — Scientific Writing (from `geox-scientific-writing`)

### Paper Structure

```
1. ABSTRACT — One paragraph, governing model, epistemic band
2. INTRODUCTION — The enigma: what doesn't fit?
3. METHODS — Data sources, tools, constitutional constraints
4. RESULTS — Figures + tables with epistemic labels
5. DISCUSSION — Governing model, Eureka insights
6. CONCLUSIONS — One governing sentence
7. PROVENANCE — All references with DOIs
```

### Mandatory Epistemic Labels

Every claim: **OBS** (observed), **DER** (derived), **INT** (interpreted), **SPEC** (speculative)

### Mandatory Provenance Chain

```
Source paper → Data → Computation → Claim → Label
```

### Mandatory Figures (any paper)

1. Location map — structural elements, GPS vectors, faults
2. Cross-section — depth-partitioned model
3. Key data plot — cooling path, velocity profile, etc.
4. Summary dashboard — kill matrix, Eureka grid

### Representation Engineering Insight

GEOX doesn't change the Earth. It changes the compression ratio.
- Before: 100 papers × 50 years × 20 models = disconnected facts
- After: "Depth-partitioned system" = one idea that contains all of them
- The product is not data. The product is **navigation**.

### Governance for Publications

- F2: Every claim labeled
- F7: Confidence capped at 0.90
- F10: Canonical terminology
- F11: Full provenance chain
- F13: Arif decides what gets published

---

## §9 — 000–999 Deployment Macro (from `geox-000-999-deployment-macro`)

### 6-Stage Pipeline

```
000 INIT → 111 SENSE → 333 PLAN → 666 CRITIQUE → 888 JUDGE → 999 SEAL
[detect gap] [verify gap] [spec+tests] [haram+audit] [verdict] [commit+push+receipt]
```

### Stage Summary

| Stage | Action | Output |
|---|---|---|
| 000 | Read state, detect physics-first gap, write EXTINCTION_INTENT | `EXTINCTION_INTENT_<N>.md` |
| 111 | Grep taxonomy residue, verify gap, map engine topology | `GEOX_GAP_REPORT_<N>.md` |
| 333 | Spec + MCP schema + tests + implement engine + wire MCP | Engine code, tests, wiring |
| 666 | HARAM scan + contradiction audit + F1–F13 floor check | `CRITIQUE_<N>.md` |
| 888 | Review CRITIQUE; SEAL / SABAR / HOLD verdict | `VERDICT_<N>.md` |
| 999 | Final verification, git commit+push, registry update, SEAL receipt | git push + receipt |

### ZEN-10 Consolidation Context

GEOX underwent ZEN-10 consolidation (2026-07-07): **89 tools → 14 canonical**.
- **10 surface:** `geox_observe`, `geox_compute`, `geox_model`, `geox_interpret`, `geox_spatial`, `geox_govern`, `geox_bridge`, `geox_surface_status`, `geox_tie_receipt`, `geox_tie_preflight`
- **4 internal:** `geox_claim`, `geox_evidence`, `geox_prospect`, `geox_doctrine`
- **85 legacy:** backward-compat via middleware, hidden from `tools/list`

### Physics-First vs Taxonomy-First Detection

```bash
# Legacy taxonomy in well domain (expected — not in engines)
grep -r "LST\|TST\|HST\|systems_tract\|seq_strat" src/geox_core/well/ --include="*.py"
# Taxonomy in engines domain (UNEXPECTED — flag)
grep -r "LST\|TST\|HST\|systems_tract\|classif\|taxonomy\|facies_rule" src/geox_core/engines/ --include="*.py"
```

### Known Engines (Already Forged)

| Engine | Status |
|---|---|
| Accommodation | ✅ `src/geox_core/engines/stratigraphy/accommodation.py` |
| Sediment Routing | ✅ `src/geox_core/engines/stratigraphy/sediment_routing.py` |
| Surface-First | ✅ `src/geox_core/engines/stratigraphy/surface_first.py` |
| Sequence Emergence | ✅ `src/geox_core/engines/stratigraphy/sequence_emergence.py` |

### Known Gaps (2026-07-07)

Carbonate platform, clinoform progradation, autogenic cycles, deepwater fan architecture, tidal/inlet processes.

### VERDICT Decision Matrix

| Verdict | When | Action |
|---|---|---|
| **SEAL** | All CRITICAL/HIGH issues fixed, tests pass, registry consistent | Proceed to 999 |
| **SABAR** | Minor MEDIUM issues, doc gaps | Fix then re-JUDGE |
| **HOLD** | Engine contradicts existing physics, missing tests, HARAM found | Block; escalate to Arif |

### Reality Check Before 000 INIT

If the engine already exists as a physics-first module → **STOP.** The macro is for NEW engines, not re-forging existing ones. If the engine exists but is taxonomy-first → proceed.

---

## §10 — Cross-Cutting Enforcement Patterns (Fragments Consolidated)

### When driving GEOX tools, always enforce:

| Guard | Source Fragment |
|---|---|
| Every claim has `evidence_for` + `evidence_against` + `missing_tests` | claim-grammar |
| Location-bearing claims carry `source_tag` + `positional_accuracy_m` | claim-grammar (scar_1783404210900) |
| No "proven reservoir" / "confirmed hydrocarbon" / "100% confidence" | claim-grammar + redteam-hantu |
| Every output tagged with epistemic rung (OBS→DER→INT→SPEC) | epistemic-ladder |
| Lower-rung observation beats higher-rung interpretation | epistemic-ladder |
| Interpretations list ≥ 1 alternative with discrimination test | contradiction-engine |
| Log-derived properties within physical bounds (φ ≤ 0.45, Sw ∈ [0,1]) | petrophysics-bounds |
| Permeability always declared "empirical" | petrophysics-bounds |
| Artifact refs are GEOX URIs, never raw filesystem paths | earth-evidence |
| No capital decisions to WEALTH without GEOX evidence | earth-evidence |
| F2 TRUTH labels on all outputs; F9 ANTI-HANTU enforced | constitution |
| 888 HOLD for any irreversible mutation | constitution |
| No shadow tools, phantom tools, schema drift, or bypass paths | redteam-hantu |
| Papers carry OBS/DER/INT/SPEC labels + provenance chain | scientific-writing |
| New engines follow 000→999 pipeline with HARAM scan at 666 | deployment-macro |
| ZEN-10: 14 canonical tools; 85 legacy via backward-compat only | deployment-macro |

---

## §PROVENANCE

This document was produced by a delegated extraction task on 2026-07-08 against 9 fragment skills discovered under `/root/.agents/skills/`:

| # | Fragment | Path | Key Unique Content Extracted |
|---|---|---|---|
| 1 | `geox-claim-grammar` | `/root/.agents/skills/geox-claim-grammar/SKILL.md` | Claim structure, Location First (scar_1783404210900), source tags, forbidden phrases, multi-hypothesis mandate, claim types |
| 2 | `geox-constitution` | `/root/.agents/skills/geox-constitution/SKILL.md` | F1-F13 floors (GEOX-specific), epistemic style, 888 HOLD triggers, One Root doctrine, binary transport |
| 3 | `geox-contradiction-engine` | `/root/.agents/skills/geox-contradiction-engine/SKILL.md` | 7 contradiction types, contradiction_scan fields, enforcement rules |
| 4 | `geox-earth-evidence` | `/root/.agents/skills/geox-earth-evidence/SKILL.md` | Artifact refs (URIs not paths), uncertainty bands, GEOX→WEALTH handoff, anti-patterns |
| 5 | `geox-epistemic-ladder` | `/root/.agents/skills/geox-epistemic-ladder/SKILL.md` | 7-rung ladder, iron rule (lower beats higher), forbidden moves, detection rules |
| 6 | `geox-petrophysics-bounds` | `/root/.agents/skills/geox-petrophysics-bounds/SKILL.md` | Canonical transforms table, QC rules, LAS validation, critical rules (permeability, Archie, fluid contacts) |
| 7 | `geox-redteam-hantu` | `/root/.agents/skills/geox-redteam-hantu/SKILL.md` | Guardian checklist (5 domains), 7 hantu patterns, forbidden phrases, block triggers |
| 8 | `geox-scientific-writing` | `/root/.agents/skills/geox-scientific-writing/SKILL.md` | Paper structure, mandatory figures, epistemic labels, provenance chain, representation engineering insight |
| 9 | `geox-000-999-deployment-macro` | `/root/.agents/skills/geox-000-999-deployment-macro/SKILL.md` | 6-stage pipeline, ZEN-10 consolidation, physics-first detection, known engines/gaps, HARAM scan checklist |

**Target skill enriched:** `geox-federation-mcp-driver` at `/root/.hermes/skills/devops/geox-federation-mcp-driver/SKILL.md`. This enrichment covers the domain-specific enforcement patterns (constitutional, epistemic, geophysical, governance, and deployment) that the parent skill's MCP tool-driving patterns do not directly address.

**DITEMPA BUKAN DIBERI — Forged from fragment wisdom, not inferred.**
