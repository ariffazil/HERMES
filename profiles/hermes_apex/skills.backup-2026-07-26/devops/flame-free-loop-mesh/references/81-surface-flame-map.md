# FLAME Integration Map — Full Federation 81-Surface Classification

> Forged: 2026-07-20 by FORGE (000Ω) + Hermes
> Reference for: `flame-free-loop-mesh` skill
> Methodology: Every MCP tool + internal CLI + system script classified by FLAME eligibility

## Classification Legend

| Flag | Meaning | Action |
|------|---------|--------|
| 🔥 FLAME-PRIME | Tool internally calls an LLM for non-constitutional work | Route through FLAME |
| ⚡ CONDITIONAL | LLM for some sub-modes, governed for others | FLAME for non-seal sub-paths only |
| 🏛️ GOVERNED-ONLY | Constitutional hard boundary | NEVER FLAME |
| 🚫 NO-LLM | Pure compute, I/O, no inference path | Not applicable |

## Call Site Governance Categories

| Category | Count | Rule |
|----------|-------|------|
| ALLOWED | 8 | FLAME by default |
| FALLBACK | 6 | Governed primary, FLAME on exhaustion |
| FORBIDDEN | 8 | Constitutional hard gate — never FLAME |

## Full Map by Organ

### arifOS Kernel (port 8088) — 8 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| `arif_init` | Session bind | 🚫 |
| `arif_judge` | Constitutional verdict | 🏛️ NEVER |
| `arif_seal` | VAULT999 append | 🏛️ NEVER |
| `arif_think` | Core reasoning | 🏛️ Governed (mode=verify: ⚡) |
| `arif_observe` | Sense→evidence | 🔥 mode=search,fetch |
| `arif_route` | Intent→organ | 🚫 |
| `arif_memory` | Memory governor | ⚡ mode=remember only; promote=🏛️ (kernel-owned memory law) |
| `arif_forge` | Execution gate | 🚫 |

### A-FORGE (port 7071/7072) — 8 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| `forge_search` | Semantic codebase | 🔥 |
| `forge_diagnose` | Error analysis | 🔥 |
| `forge_summarize` | Code/log summary | 🔥 |
| `forge_plan` | Plan generation | 🔥 |
| `forge_execute` | Shell execution | 🚫 |
| `forge_browser` | Browser automation | 🚫 |
| `forge_deploy` | Deployment | 🚫 |
| `forge_health` | Health probe | 🚫 |

### GEOX (port 8081) — 21 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| `geox_basin` | Basin intelligence | ⚡ synthesis mode |
| `geox_claim` | Claim lifecycle | 🔥 mode=create (seal: 🏛️) |
| `geox_evidence` | Evidence synthesis | 🔥 |
| `geox_contradiction_scan` | Pattern matching | 🔥 |
| `geox_falsify` | Kill matrix | ⚡ edge analysis |
| `geox_petrophysics` | Vsh/porosity/Sw | 🚫 |
| `geox_seismic_compute` | Synthetic/inversion | 🚫 |
| `geox_seismic_ingest` | File I/O | 🚫 |
| `geox_seismic_interpret` | Horizon/fault | ⚡ vision mode |
| `geox_sequence` | Stratigraphy | 🔥 |
| `geox_geomechanics` | Moduli/stress | 🚫 |
| `geox_prospect` | Volumetrics | 🔥 |
| `geox_well_desk` | Rendering | 🚫 |
| `geox_well_ingest` | File I/O | 🚫 |
| `geox_subsurface_model` | Joint inversion | 🚫 |
| `geox_gravmag_studio` | Forward modeling | 🚫 |
| `geox_sediment_mass_balance` | Volume accounting | 🚫 |
| `geox_thermal_maturity_history` | Burial math | 🚫 |
| `geox_deep_time_state` | Database lookup | 🚫 |
| `geox_lem_predict` | ML inference | 🚫 |
| `geox_surface_status` | Registry probe | 🚫 |

### WEALTH (port 18082) — 12 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| `capital_primitive` | NPV/IRR/EMV | 🚫 |
| `capital_market` | FX/commodities | 🔥 mode=signal |
| `capital_health` | Cash flow/runway | 🚫 |
| `capital_wisdom` | Wisdom evaluation | 🏛️ NEVER |
| `capital_diagnose` | Institutional | 🏛️ NEVER |
| `capital_entropy` | Power/trust drift | ⚡ text analysis |
| `capital_ledger` | VAULT999 query | 🚫 |
| `capital_registry` | Meta/introspection | 🚫 |
| `wealth_cascade_model` | Math model | 🚫 |
| `wealth_external_exploitation_detect` | Text analysis | ⚡ |
| `wealth_governance_capacity` | Text analysis | ⚡ |
| `wealth_institutional_stress_index` | Math composite | 🚫 |

### WELL (port 18083) — 8 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| ALL TOOLS | Human substrate | 🏛️ REFLECT_ONLY, NEVER FLAME |

### Hermes MCP — 7 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| `hermes_fact_check` | Claim verification | 🔥 |
| `hermes_epistemic_check` | Confidence heuristic | 🔥 |
| `hermes_memory_steward` | Classification | 🔥 |
| `hermes_plan_review` | Plan safety | 🔥 |
| `hermes_cross_verify` | Cross-agent | ⚡ |
| `hermes_health` | Health probe | 🚫 |
| `hermes_system_status` | Status snapshot | 🚫 |

### Housekeeping (hound) — 6 tools

| Tool | Class | FLAME? |
|------|-------|--------|
| ALL TOOLS | Keyless search/fetch | 🚫 NO-LLM |

### Internal CLIs + Scripts

| Script | Purpose | FLAME? |
|--------|---------|--------|
| `mimo-doctor.sh` | Health probe→diagnosis | 🔥 |
| `mimo-fallback.sh` | Routing decision | 🔥 |
| `m3-weights-snooze.sh` | Weight management | 🔥 |
| `wealth-static-render.py` | Data→narrative | ⚡ |
| `vault-migrate-arifos` | Data migration | 🚫 |
| `mcp-publisher` | Publishing | 🚫 |
| `forge-vault-flat` | Config management | 🚫 |
| `litellm-proxy` | Proxy passthrough | 🚫 |

### Cron Jobs — FLAME Impact

| Job | Type | FLAME? |
|-----|------|--------|
| `morning-brief` | script | 🚫 no-LLM |
| `drift-alert` | script | 🚫 no-LLM |
| `STEEL pulse` | script | 🚫 no-LLM |
| `well-biometric-feed` | script | 🚫 no-LLM |
| `TokenRouter GLM check` | script | 🚫 no-LLM |
| `daily-news-briefing` | agent | 🔥 FLAME for summarization |
| `evening-digest` | agent | 🔥 FLAME for digest |
| `weekly-deep-brief` | agent | 🏛️ governed (deep synthesis) |
| `weekly-reflection` | agent | 🔥 FLAME for reflection |
| `IG Story Gym Quote` | agent | 🔥 FLAME for creative |
| `federation-auto-remediation` | agent | 🏛️ governed (infrastructure) |
| `Paper Trading Morning` | agent | 🔥 FLAME for analysis |
| `Paper Trading Zen Exec` | agent | 🔥 FLAME for analysis |

## Totals

| Category | Count |
|----------|-------|
| 🔥 FLAME-PRIME | 19 |
| ⚡ CONDITIONAL | 8 |
| 🏛️ GOVERNED-ONLY | 14 |
| 🚫 NO-LLM | 40 |
| **TOTAL** | **81** |

## Priority Wiring Order

1. `hermes_fact_check` + `hermes_epistemic_check` (highest call volume)
2. `hermes_memory_steward` (every session)
3. `geox_contradiction_scan` (pattern matching, no sovereignty)
4. `arif_observe` search/fetch (result synthesis)
5. `geox_evidence` discover (evidence synthesis)
6. `capital_market` signal (interpretation, no money movement)
7. `forge_search` (semantic codebase)
8. System scripts (`mimo-doctor`, `mimo-fallback`)

## Architectural Rule

```
FLAME touches: advisory, classification, extraction, summarization
FLAME NEVER touches: judging, sealing, sovereign data, human substrate
When in doubt → governed cascade
FLAME is for throughput, not truth
```
