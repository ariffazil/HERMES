# FED Provider Gap Audit — 2026-08-04

## Context

FED (arifOS federation router, port 7074, DB: `/root/.local/share/arifos/token_bank.db`) was probed via 3 MCP calls: `fed_health`, `fed_status`, `fed_probe`. This is **not** the same as the af-forge:4000 wire audit (see `fed-wire-gap-audit-20260804.md` for wire topology). This audit covers the **provider balance + health + latency** layer inside FED itself.

## FED Core State

| Field | Value |
|---|---|
| Port | 7074 (NOT 4000 — that's LiteLLM) |
| Version | 3.1.0-zen |
| DB | `/root/.local/share/arifos/token_bank.db` |
| Tables | providers, route_health, route_latency, shadow_ledger, sqlite_sequence, token_bank_spend |

## Provider Registry

| Provider | Track | Balance | Confidence | Status | Probe Source | Notes |
|---|---|---|---|---|---|---|
| deepseek | A | $19.08 (fresh probe) / $13.19 (DB stale from 2026-08-02) | 1.0 | LIVE | api_probe | Only provider with real API-based balance check |
| qwen-token-plan-team | B | **$0.00** | 0.95 | LIVE | manual | **0 seats remaining** — all 3 occupied. 21 models accessible. |
| minimax | B | **$0.00** | 0.95 | LIVE | manual | Reactivated 2026-08-03. Endpoint corrected. |
| mimo-platform | B | $10.00 | 1.0 | — | manual | Stale: last update 2026-07-30 |
| bailian-token-plan | B | $25.00 | 1.0 | — | manual | Stale: last update 2026-07-30 |
| mulerouter | B | $49.93 | 0.99 | **ARCHIVED** | — | Not in litellm-config.yaml. Orphaned. |
| tokenrouter | B | $59.94 | 0.98 | **ARCHIVED** | — | Not in litellm-config.yaml. Orphaned. |
| openrouter | B | $0.50 | 0.60 | **ARCHIVED** | — | **BLIND**: $29.99 spent unknown, no balance API. |

## Gaps

### GAP-1 (HIGH): Track A probe only checks deepseek
`fed_probe` exit=0, probed=1 — only deepseek returns API balance. MiniMax, mimo, bailian are all "Manual top-up" (not API-probed). If they spend money, FED won't know.

**Fix:** Implement Track A probe for minimax and mimo-platform (both have API endpoints). Bailian is likely dead or manual-only.

### GAP-2 (HIGH): qwen-token-plan 0 seats remaining
All 3 team seats occupied (arifOS Pro, ariffazil Standard, aliyun Standard). No fallback if arifOS seat is revoked. Balance=$0 with active models — either pre-paid or will hard-fail on next call.

**Fix:** Confirm whether qwen team has pre-paid quota or is about to 403. If 403 imminent: need alternative for `deepseek-v4-pro` which routes through qwen-token-plan.

### GAP-3 (HIGH): minimax balance = $0 but status = LIVE
MiniMax-M3 is the current default model. Balance is $0 (as of 2026-08-03). Either:
- Token Plan model (not pay-per-call) → balance tracking is misleading
- Pre-paid exhausted → next call will 403

**Fix:** Verify MiniMax Token Plan billing model. If Token Plan = unlimited, mark balance as N/A not $0.

### GAP-4 (HIGH): OpenRouter BLIND
$29.99 spent, $0.50 remaining, no credit balance API. "needs_manual_reconciliation" in notes.

**Fix:** Either reconcile manually or mark openrouter as dead.

### GAP-5 (MEDIUM): 3 ARCHIVED providers still in DB
mulerouter, tokenrouter, openrouter — not in litellm-config.yaml. Phantom entries inflating provider count from 5 live to 8 total.

**Fix:** Clean `ARCHIVED` entries or add `status=archived` filter to `fed_status` output.

### GAP-6 (MEDIUM): Latency telemetry sparse
Only 5 latency samples total across 4 models. Most recent: 2026-08-03 (MiniMax). DeepSeek sample from 2026-08-02. No continuous benchmarking.

**Fix:** Add `fed_report_latency` to cron heartbeat or federation-health watchdog.

## Architecture Note

FED port 7074 = arifOS federation router (Python, token-bank.db).
af-forge port 4000 = LiteLLM proxy (hermes-asi model routing).
`fed_probe` runs `balance_probe.py` which only has API probes for deepseek — all other providers are manual estimates. The probe is a **partial blind** — it says "✅ Probed: 1" but most providers are just read from DB.
