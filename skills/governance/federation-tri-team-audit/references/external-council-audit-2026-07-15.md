# External Council Audit — arifOS Federation (2026-07-15)

## Context

External LLM (ChatGPT) with preconfigured MCP connector to arifOS kernel exercised the full 000→999 audit path live.

## Result: 5.8/10 Deployment Readiness — HOLD

| Dimension | Score | Finding |
|---|---|---|
| Semantic architecture | 9.0/10 | Scope and output contract coherent |
| Evidence discipline | 8.5/10 | L1-L4 separation strong |
| Organ boundaries | 9.0/10 | Correctly prevents self-judging organs |
| Model independence | 8.0/10 | Replacement test structurally sound |
| Skill registration | 2.0/10 | Exact skill absent from tested machine surfaces |
| Authority continuity | 2.0/10 | SOVEREIGN at init became MEDIUM at judge/forge |
| Schema/runtime convergence | 3.0/10 | Published modes contradict runtime dispatch |
| Transport health | 3.0/10 | Selective 502 failures |
| Replay accuracy | 2.0/10 | No implemented post-audit validation |

## Kernel Path Test

| Stage | Result | Evidence |
|---|---|---|
| 000 arif_init | DEGRADED PASS | Session created; alignment/adversarial profiles absent |
| 111 arif_observe | MISMATCH | Schema rejects skill_discover; runtime advertises it |
| 333 arif_think | FAIL | 502 upstream error |
| 444 arif_route | PASS | Correctly routed audit to ARIFOS |
| 888 arif_judge | HOLD | Runtime saw ARIF as MEDIUM, not SOVEREIGN |
| 777 arif_forge dry_run | HOLD | Same authority downgrade |
| 999 receipt | NOT ATTEMPTED | No valid judge chain |

Functional availability: 2/6 = 33.3%. Failure-closed rate: 2/2 = 100% (broken safely).

## Conformance Coverage

- 2/9 checks passed, 7/9 skipped, 22.2% exercised
- substrate_gate: RED
- live_tool_count: 0 (conformance observer undercounts)
- yaml_tool_count: 19

## Key Insight

> "The system is broken safely rather than broken dangerously."

Authority-bound actions fail closed. The kernel correctly downgrades and blocks mutations when it can't verify sovereignty. This is exactly what F1-F13 is designed to do.

## P0 Drift Map

1. **AUTHORITY_DRIFT** — Init recognized ARIF as SOVEREIGN/FULL; judge/forge received MEDIUM. F13 cannot reliably exercise sovereign authority.
2. **SCHEMA_DRIFT** — Public arif_observe schema rejects skill_discover; runtime advertises it and rejects published hybrid_discovery.
3. **TRANSPORT_DRIFT** — arif_think, direct WEALTH registry, kernel→WEALTH bridge returned 502.

## Permanent Fixes Required

P0: Authority propagation (one identity flow), schema from single source, transport restoration.
P1: Explicit execution mode (live/hybrid/offline), post-audit validation, skill registration.
P2: openai.yaml metadata separation (not authority control plane).
