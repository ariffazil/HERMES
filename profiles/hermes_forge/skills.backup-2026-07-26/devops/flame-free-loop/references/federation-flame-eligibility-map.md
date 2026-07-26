# Federation FLAME Eligibility Map — Full 94-Tool Audit

> Forged 2026-07-20. Cross-referenced against all 6 organs.

## Per-Organ Breakdown

| Organ | Total | ALLOWED | FALLBACK | FORBIDDEN | Rule |
|-------|-------|---------|----------|-----------|------|
| A-FORGE | 111 | 35 | 0 | 76 | Only OBSERVE-class. MUTATE/governance/vault blocked |
| arifOS | 8 | 0 | 0 | 8 | Kernel IS governance. Never FLAME |
| GEOX | 24 | 0 | 0 | 24 | Evidence-only domain organ |
| WEALTH | 12 | 0 | 0 | 12 | Compute-only. Capital primitives |
| WELL | 8 | 0 | 0 | 8 | REFLECT_ONLY. Dignity protection |
| Hermes | 7 | 0 | 5 | 2 | Health ok. Cross-verify/plan-review forbidden |
| **TOTAL** | **170** | **35** | **5** | **135** | |

## 22 Call Sites Mapped

| Category | Count | Examples |
|----------|-------|----------|
| ALLOWED | 8 | Daily briefing, title gen, skill extract, classify |
| FALLBACK | 6 | arif_think non-constitutional, shadow eval, terminal chat |
| FORBIDDEN | 8 | Judge, seal, constitutional, PII, PETRONAS, sovereign |

## arifOS Kernel (8 tools — ALL FORBIDDEN)

These ARE the governance layer. Never route through FLAME.

- `arif_init` — Session ignition
- `arif_observe` — Sense reality into evidence
- `arif_think` — Structured reasoning (constitutional when mode=reason/atlas)
- `arif_route` — Intent→organ router
- `arif_memory` — Memory governor L1-L6
- `arif_judge` — Constitutional verdict (SEAL/HOLD/SABAR/VOID)
- `arif_forge` — Execution gate via A-FORGE
- `arif_seal` — VAULT999 immutable append

## GEOX (24 tools — ALL FORBIDDEN)

Domain organ. Evidence only. Computation uses domain-specific physics, not LLM inference.

## WEALTH (12 tools — ALL FORBIDDEN)

Capital primitives are deterministic math. No LLM inference path.

## WELL (8 tools — ALL FORBIDDEN)

REFLECT_ONLY. Human readiness. Never touched by free-loop.

## Hermes (7 tools)

- 🟡 `hermes_health` — Observational
- 🟡 `hermes_system_status` — Observational
- 🟡 `hermes_epistemic_check` — Advisory verification (FALLBACK only)
- 🟡 `hermes_fact_check` — Advisory verification (FALLBACK only)
- 🟡 `hermes_memory_steward` — Classification (FALLBACK only)
- 🔴 `hermes_cross_verify` — Governance-adjacent (FORBIDDEN)
- 🔴 `hermes_plan_review` — Governance-adjacent (FORBIDDEN)

## A-FORGE ALLOWED Tools (35 OBSERVE-class)

### Health & Probe (6)
forge_health_check, forge_probe, forge_security_drift_scan, forge_runtime_verify, forge_isomorphism_check, forge_verify_timeline

### VPS & System (7)
forge_vps_ports, forge_vps_services, forge_vps_cron, forge_netdata_alarms, forge_netdata_metrics, forge_worktree, forge_entropy_sweep

### Surface & Audit (5)
forge_surface_guard, forge_surface_audit, forge_scar_scan, forge_registry_status, forge_fingerprint_check, forge_status

### Research (5)
forge_fetch_url, forge_fetch_json, forge_fetch_metadata, forge_fetch_links, forge_search, forge_docs_lookup, forge_research, forge_minimax_search

### Documents (1)
forge_document_ingest

### Filesystem Read-Only (4)
forge_filesystem_read, forge_filesystem_tree, forge_filesystem_search, forge_filesystem_stat

### Cooling (2)
forge_cool_drift, forge_cool_pattern

### Journal (1)
forge_journalctl

## A-FORGE FORBIDDEN (76 — MUTATE, governance, vault, registry, shell, git, docker, browser, skill, confirm, job)

Any tool with: MUTATE class, governance, vault/registry mutation, shell execution, git mutation, docker, browser interaction, skill generation, job submission, lease management.

## Control Gate Reference

1. **CLI-only** — `free-llm` or Python API, never agent MCP
2. **No governance chain** — output never feeds `arif_judge`/`arif_seal` without human
3. **RM0 hard gate** — paid models blocked at config level
4. **Hitrate log** — all calls to `flame_hitrate.jsonl`
5. **No agent access** — Hermes/OpenCode/OpenClaw never route FLAME
6. **Seal boundary** — FLAME output = evidence only, never seals

## Classification Rule

```
ALLOWED if:   OBSERVE-class AND non-governance AND non-domain-organ
FALLBACK if:  advisory/observational but agent-adjacent (Hermes health, epistemic)
FORBIDDEN if: MUTATE OR governance OR domain_organ OR touches VAULT999 OR requires lease
```
