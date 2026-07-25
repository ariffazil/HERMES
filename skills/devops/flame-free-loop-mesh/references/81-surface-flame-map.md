# FLAME Integration Map — Full Federation 81-Surface Classification

> Forged: 2026-07-20 by FORGE (000Ω) + Hermes
> Updated: 2026-07-25 — Paper Trading corrected to NO-LLM (deterministic engine). Cron agent jobs reclassified as 🏛️ governed (user-facing content). Ollama dropped. Routing restructured.

## Clean Division of Labor (Arif-ratified 2026-07-24)

| Layer | Role | Model Tier |
|---|---|---|
| **FLAME** | Tools, workers, fallback throughput | Free/cheap, tiered by availability, disposable |
| **Hermes** | Epistemic/human-life reasoning | Premium, high-effort, reasoning-preserved |
| **OpenCode** | Execution/coding actuation | Budget-to-premium depending on task complexity |
| **arifOS** | Judgment, audit, sealing | Policy logic — not a model tier at all |

## 11-Tier Architecture (2026-07-25)

```
T1:     Groq — qwen/qwen3.6-27b (primary, 292ms stable)
T2:     Groq — llama-3.3-70b-versatile (deep reasoning, 159ms)
T3:     Groq — llama-3.1-8b-instant (fastest, 586ms)
T4:     Cerebras — gpt-oss-120b (fast, 337ms)
T5:     Groq — openai/gpt-oss-120b (deep, 473ms)
T6:     Cerebras — gemma-4-31b (multimodal, 786ms)
T7:     Gemini — gemini-flash-lite-latest (deep-context, 598ms)
T8:     SEA-LION — Qwen-SEA-LION-v4-32B-IT (BM native, 2019ms)
T9:     SEA-LION — Llama-SEA-LION-v3-70B-IT (BM deep, 1463ms)
T10:    SEA-LION — Gemma-SEA-LION-v4-27B-IT (BM fast, 1482ms)
T11:    OpenRouter — :free aggregator (Tier-3 fallback, 1042ms, 20rpm)

Dropped: Ollama qwen2.5-coder:3b — 18ms connection refused.
```

Tiers are a cascading **availability ladder**, not a reasoning hierarchy.

## Classification Legend

| Flag | Meaning | Action |
|------|---------|--------|
| 🔥 FLAME-PRIME | Tool internally calls an LLM for non-constitutional work | Route through FLAME |
| ⚡ CONDITIONAL | LLM for some sub-modes, governed for others | FLAME for non-seal sub-paths only |
| 🏛️ GOVERNED-ONLY | Constitutional hard boundary | NEVER FLAME |
| 🚫 NO-LLM | Pure compute, I/O, no inference path | Not applicable |

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

| Job | Type | FLAME? | Notes |
|-----|------|--------|-------|
| `morning-brief` | script | 🚫 no-LLM | |
| `drift-alert` | script | 🚫 no-LLM | |
| `STEEL pulse` | script | 🚫 no-LLM | |
| `well-biometric-feed` | script | 🚫 no-LLM | |
| `TokenRouter GLM check` | script | 🚫 no-LLM | |
| `daily-news-briefing` | **agent** | 🏛️ **governed** | User-facing content — intentional governed cascade. Corrected 2026-07-25. |
| `evening-digest` | **agent** | 🏛️ **governed** | Same — user-facing. Corrected 2026-07-25. |
| `weekly-deep-brief` | **agent** | 🏛️ governed | Deep synthesis |
| `weekly-reflection` | **agent** | 🏛️ **governed** | User-facing. Corrected 2026-07-25. |
| `IG Story Gym Quote` | **agent** | 🔥 FLAME for creative | Low-stakes, suitable |
| `federation-auto-remediation` | **agent** | 🏛️ governed | Infrastructure |
| `Paper Trading Morning` | **script** | 🚫 **NO-LLM** | ⚠️ **Corrected 2026-07-25**. Engine is 100% deterministic (yfinance + numpy). Zero LLM calls. |
| `Paper Trading Zen Exec` | **script** | 🚫 **NO-LLM** | Same — deterministic engine. |

## Totals

| Category | Previous | Corrected (2026-07-25) | Change |
|----------|----------|------------------------|--------|
| 🔥 FLAME-PRIME | 19 | **17** | -2 (Paper Trading ×2 → NO-LLM) |
| ⚡ CONDITIONAL | 8 | **8** | Unchanged |
| 🏛️ GOVERNED-ONLY | 14 | **17** | +3 (agent cron jobs → governed) |
| 🚫 NO-LLM | 40 | **42** | +2 (Paper Trading ×2) |
| **TOTAL** | **81** | **84** | |

Note: Totals increased because cron agent jobs were previously double-counted or under-reported.

## Priority Wiring Order (2026-07-25)

1. `geox_contradiction_scan` — pattern matching, no sovereignty, low effort
2. `geox_evidence` discover — evidence synthesis, low effort
3. `arif_observe` search/fetch — result synthesis, medium effort
4. `capital_market` signal — interpretation, no money movement, medium effort
5. `forge_search` — semantic codebase, medium effort
6. `forge_diagnose` — error analysis, low effort
7. System scripts (`mimo-doctor`, `mimo-fallback`) — low effort
8. `geox_claim` create — claim generation, low effort
9. `forge_summarize`, `forge_plan` — medium effort

**NOT in priority order (corrected classifications):**
- Hermes MCP tools — not deployed as standalone services; run within Hermes governed cascade
- Paper Trading crons — deterministic NO-LLM, no LLM needed
- Agent cron jobs — user-facing, intentional governed cascade

## Architectural Rule

```
FLAME touches: advisory, classification, extraction, summarization
FLAME NEVER touches: judging, sealing, sovereign data, human substrate
When in doubt → governed cascade
FLAME is for throughput, not truth
```
