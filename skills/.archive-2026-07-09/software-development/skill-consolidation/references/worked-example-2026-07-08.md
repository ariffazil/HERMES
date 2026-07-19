# Worked Example — 15 Fragments → 2 Consolidated Skills (2026-07-08)

## Context

The user asked: "Extract core knowledge from 5 federation + 10 ZEN fragments and produce two consolidated skills."

Neither target skill existed — both were created from scratch.

## Source Fragments

### Federation (5 fragments)
| Fragment | Key Contents |
|----------|-------------|
| `a2a-federation-builder` | A2A protocol, Agent Cards, 10 invariants, AGENT_REGISTRY.json, HOLD/SEAL workflow, task lifecycle states, A2A vs MCP boundary |
| `aaa-cockpit` | AAA control-plane boundaries (what it is NOT), approval ticket format, anti-patterns, pre-flight checks |
| `federation-observability` | OpenTelemetry + Prometheus + Grafana (LGTM), Python/TS instrumentation, federation span attributes, custom metrics, MCP Apps + A2A telemetry |
| `federation-safety-wiring` | 10 error classes, 6 memory classes, 4 epistemic layers, structured success/failure return formats, tool handler wiring checklist |
| `federation-topology-map` | Complete dependency graph, critical-path order, organ ports table, live probe shell script, Telegram bot detection |

### ZEN (10 fragments)
| Fragment | Key Contents |
|----------|-------------|
| `zen-organ-reality` | Organ 1: OBS/DER/INT/SPEC, probe-before-claim, heartbeat HEARTBEAT_OK, T_1 probe |
| `zen-organ-governance` | Organ 2: F1-F13 floors, blast radius (None→IRREVERSIBLE), loop cap 3, MUBAH auto |
| `zen-organ-civilization` | Organ 3: A2A+MCP+warga boundary, TOOLREGISTRY duplicate check (≥2 tags HARAM), dual-citizenship |
| `zen-organ-execution` | Organ 4: receipt-first, 600s foreground, notify_on_complete mandatory, T_1 before irreversible |
| `zen-organ-memory` | Organ 5: VAULT999 append-only, seal-chain lineage, char budget 98%/2200, /root/ariffazil/ guard |
| `zen-organ-witness` | Organ 6: Gödel, proposer≠judge, dual-witness, advisory_only contract, verdict path 000→999 |
| `zen-organ-meaning` | Organ 7: Output Contract ≤3 sentences, sovereign signals → ACT, DNA class (open/closed) |
| `zen-diagnostic-probe` | 3-probe reality check, "organ is not probe" rule, eureka margin cases (WELL 62 days, GEOX session init) |
| `ZEN_MD` | ALLCAPS-2-term naming, BANGANG detection, exempt paths, 4 action modes, heptalogy stage 000-ZEN |
| `ZEN_ORGANS` | Master framework, 7 conservation laws, metrics layer (ΔR, ΔG, I_sys, W, ∂M/∂t, Ω, ∇F), dS_agent/dt ≤ 0 |

## Outputs

| File | Words | Key Structure |
|------|-------|---------------|
| `/root/.hermes/plans/consolidation-federation.md` | 1,700 | 7 sections: topology map, A2A protocol, AAA cockpit, safety wiring, observability, live probe, quick reference |
| `/root/.hermes/plans/consolidation-zen.md` | 2,687 | 17 sections: operational map, each of 7 organs, system summary, diagnostic probe, ZEN_MD, metrics, blindspots, session-init check, integration, anti-patterns |

## Key Decisions

1. **Used richest fragment as base:** `a2a-federation-builder` for federation, `ZEN_ORGANS` for ZEN
2. **Injected field-level detail** from each fragment (receipt formats, failure signals, exact commands) — didn't just summarize
3. **§PROVENANCE table** in each file maps every fragment to its unique contribution
4. **Both under 4,000 words** despite 15 source fragments totaling ~100K chars
5. **Targets were empty** — created from scratch with `write_file`, output to `/root/.hermes/plans/`

## What Made This Work

- Batch reading all 15 fragments in parallel (2 rounds of reads + 1 for remaining)
- The §PROVENANCE table forced discipline: if a fragment had no unique contribution, it was absorbed, not merged
- The ZEN_ORGANS master already had a consolidated structure — the other 9 fragments provided field-level detail to inject, not independent sections
- Keeping word counts tight meant dropping duplicated bodies and keeping only what was unique per fragment
