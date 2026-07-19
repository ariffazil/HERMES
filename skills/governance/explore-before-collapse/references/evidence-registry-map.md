# Evidence Registry — 2026-07-13

> **Canonical mapping of every evidence surface in the arifOS federation.**
> Source: `/root/AAA/docs/evidence-registry.json` (generated from JSON schema)
> Principle: EXPLORE_BEFORE_COLLAPSE — know where to look before you look.

## Source Map

| Source ID | Type | Owner | Freshness | Reliability | Questions Answered |
|-----------|------|-------|-----------|-------------|-------------------|
| runtime_import_probe | live_system | Intelligence | live | high | Which module executes, which env, import path |
| service_health_endpoint | live_system | arifOS/A-FORGE/AAA | live | high | Organ responding, status, tools intact |
| git_source_truth | version_control | Intelligence | live | high | Which commit, diff, tree state |
| runtime_verify_tool | composite | Intelligence | live | high | Git/wheel/import agreement, drift |
| vault999_seal_chain | immutable_ledger | Truth | at seal | very high | Actions sealed, chain intact, cooling receipts |
| cooling_receipt_log | derived_ledger | Truth | at cooling | high | Convergence patterns, 3x DIVERGING |
| memory_canonical_store | governed_memory | Governance | KSR <1h | medium | Previously known, provenance |
| session_state_current | governed_session | Governance | live | high | Active session, authority, capabilities |
| filesystem_probe | live_system | Intelligence | live | high | Files at path, content, hash |
| log_stream | telemetry | Truth | at event | high | Service logs, errors, sequence |
| web_external_search | external_internet | Intelligence | at crawl | low-medium | Internet facts, current events |
| geox_subsurface | domain_organ | GEOX | at-ingest | medium-high | Geological context, basin, well interp |
| wealth_capital | domain_organ | WEALTH | on-demand | high deductive | Financial health, NPV, market |
| well_human | domain_organ | WELL | at-injection | low-medium | Human readiness, vitality, stress |
| sovereign_identity | cryptographic | Governance + Sovereign | at-session | very high | Authentication, Ed25519 key |
| postgresql_database | database | Continuity | live | high | Persisted state, current records |
| tool_registry_surface | live_configuration | A-FORGE + arifOS MCP | live | high | Available tools, schemas |
| config_settings | configuration_file | All planes | at-write | high | Configured behaviour, denied tools |
| systemd_service_manifest | live_configuration | A-FORGE | at-deploy | high | Service config, env vars |
| telemetry_metrics | time_series | Truth | scrape 15-60s | medium | Load, latency, error rates |
| a2a_agent_registry | federation_state | AAA | at-register | medium | Registered agents, capabilities |
| runtime_pid_probe | live_system | Intelligence | live | high | Process running, start time |

## Exploration Modes → Source Mapping

| Mode | Purpose | Primary Sources | Cost |
|------|---------|----------------|------|
| **scout** | Fast broad discovery | filesystem_probe, tool_registry, web_search | low |
| **mapper** | Map dependencies | config_settings, git_source, a2a_registry | low-moderate |
| **driller** | Deep inspect one path | filesystem_probe, import_probe, log_stream | moderate |
| **surveyor** | Measure counts/drift | telemetry, vault999, runtime_verify | low-moderate |
| **contrarian** | Find counterevidence | log_stream, vault999, memory, web_search | moderate |
| **verifier** | Reproduce claim | runtime_verify, health, import_probe | moderate |

## Source Reliability Guide

| Reliability | Meaning | Example Sources |
|-------------|---------|----------------|
| **very high** | Append-only, cryptographically verified | vault999_seal_chain, sovereign_identity |
| **high** | Direct observation, live system | filesystem_probe, health_endpoint, git_source |
| **medium** | Depends on provenance or sampling | memory, telemetry, a2a_registry |
| **low-medium** | Web provenance varies, voluntary input | web_search, well_human |
| **high deductive** / **medium diagnostic** | Math vs model output distinction | wealth_capital |

## Key Limitation Patterns

1. **Source intent ≠ running state** — git_source, config_settings, systemd manifest all show intended state, not necessarily current execution
2. **Live ≠ complete** — health endpoint says green but backend degraded, PID exists but process hung
3. **Sealed ≠ current** — vault999 captures past actions, not current session state
4. **Memory ≠ truth** — memory is what was recorded, not what is currently true
5. **Tool registry ≠ service availability** — tool listed doesn't mean upstream backend responds
6. **At-ingest ≠ up-to-date** — GEOX profiles compiled at ingest time may not reflect latest data
