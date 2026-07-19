# arifOS Health Snapshot — 2026-07-04

Captured via `curl http://127.0.0.1:8088/health` mid-session. Use as reference for
"is arifOS in a known state" checks.

## Build vs Runtime

| Field | Value |
|-------|-------|
| release_name | v2026.07.04-MARHIN |
| version | kanon-c6fa7a5 |
| git_commit (build) | c6fa7a5 |
| git_commit (live) | **82f9146** |
| branch | main |
| runtime_path | /opt/arifos/app |
| transport | streamable-http |
| mcp_protocol_version | 2025-11-25 |
| deployment_marker | /opt/arifos/app/.git_commit (exists) |

## Tool Surface (2026-07-04)

| Metric | Value |
|--------|-------|
| tools_loaded | 17 |
| canonical_tools_loaded | 17 |
| tools_exposed_via_mcp | 45 |
| canonical_tools | 9 |
| diagnostic_tools | 41 |
| total_declared_tools | 58 |
| operational_tools | 28 |

Internal (hidden from public facade, F13-ratified): arif_act, arif_bridge_connect,
arif_fetch, arif_judge_deliberate, arif_kernel_intercept, arif_measure, arif_memory,
arif_triage.

## Surface Consistency

canonical_hash: ea7fc3a794a5d363
canonical_count: 9
divergences: []
verdict: CONSISTENT (between vantages)

## Floors Active

13 floors total.
F1: 0.5 · F2: 0.99 · F3: 0.75 · F4: -0.0 · F5: 1.0 · F6: 0.7 · F7: 0.04 ·
F8: 0.8 · F9: 0.0 · L10: 1.0 · L11: 1.0 · L12: 0.425 · L13: 1.0

Hard active: L01, L02, L04, L07, L09, L10, L11, L12, L13
Soft doctrinal: L03, L05, L06, L08

## Known Gaps (this snapshot)

| id | severity | detail | floors |
|----|----------|--------|--------|
| `runtime_drift` | warning | live_commit != build_commit (82f9146 vs c6fa7a5). Rebuild container to sync. | L10 |

Owner summary: YELLOW (vault healthy, runtime drift).

## Capability Map (config providers)

Configured: anthropic, deepseek, sea_lion (primary), minimax, brave, jina, perplexity,
firecrawl, tavily, exa, browserless, ddgs_local, ollama_local.

Not configured: openai, anthropic (in hermes view), google, openrouter, venice.

⚠ Hermes `config.yaml` shows fewer providers (4: xiaomi-mimo, bailian-token-plan,
bailian-payg, opencode-go) than arifOS capability map declares. **Split-brain source
of truth.** Deferred to a future forge — not in scope of session-2026-07-04.

## ML Floors

enabled, ml_method=sbert, model=sentence-transformers/all-MiniLM-L6-v2,
ml_runtime_ready=true, ml_hold_state=ready.

## Langfuse Tracing

ACTIVE, host=https://jp.cloud.langfuse.com, traced_tools_count=13.

## Token Pressure

Phase 1.A (telemetry only). autonomous_compaction_enabled=false. global=0 tokens,
0 active sessions. Phase 2 auto-compaction DISABLED by default — F8+F13 sovereign
to enable.

## Federation Epistemology

status=enabled, witness_oracle=active, belief_query=active, ledger_events=0,
bootstrap_events=0.

## Vault / Seal Readiness

vault999_health=healthy, ack_irreversible_gate=passable, hold_reasons_schema OK,
runtime_drift=true (see above), graphiti_read=healthy, semantic_floor=enabled.

## Thermodynamic (this moment)

entropy_delta: -0.0 · peace_squared: 0.5 · vitality_index: 0.5946 · shadow: 0.0 ·
confidence: 0.99 · verdict: SEAL · metabolic_stage: 333
witness: human=0.42, ai=0.32, earth=0.26

## Probe Command

```bash
curl -sf http://127.0.0.1:8088/health | python3 -m json.tool | head -50
```

(Health endpoint is open and returns full envelope. No auth required.)