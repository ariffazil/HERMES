# FORGE Weekly Governance Roll-up — Allowlist Fix (2026-08-01)

## Incident

AGI surfaced: `FORGE ⟁ Weekly Governance Roll-up (Sun 03:00 MYT)` failed.

```
cron payload.model 'deepseek-v4-flash' rejected by agents.defaults.models
allowlist: minimax/deepseek-v4-flash is not in [bailian-token-plan/deepseek-v4-flash,
bailian-token-plan/deepseek-v4-flash-0731, bailian-token-plan/deepseek-v4-pro,
bailian-token-plan/glm-5.2, bailian-token-plan/kimi-k2.7-code,
bailian-token-plan/qwen3.6-flash, bailian-token-plan/qwen3.7-max,
bailian-token-plan/qwen3.8-max-preview, deepseek/deepseek-v4-flash,
deepseek/deepseek-v4-pro, groq/gpt-oss-120b, groq/llama-3.1-8b-instant,
groq/llama-3.3-70b-versatile, kimi-coding/k3, kimi-coding/kimi-for-coding,
minimax/MiniMax-M2.7-highspeed, minimax/MiniMax-M3,
openrouter/ai21/jamba-large-1.7, openrouter/moonshotai/kimi-k3]
```

## Job

- job_id: `a4301644-2f6a-4365-965a-a6c908953a8f`
- Schedule: Sun 03:00 MYT (`0 3 * * 0`, tz Asia/Kuala_Lumpur)
- Runs `/root/.openclaw/cron/forge-2026-06-29/forge-weekly.sh`, receipts-only policy
- Delivery: none (silent) per HEARTBEAT.md

## Root Cause

The job's `payload.model` was `deepseek-v4-flash` (bare). The allowlist in
`/root/.openclaw/openclaw.json` → `agents.defaults.models` only contains
provider-prefixed IDs. Bare names are rejected at preflight.

Note: this job failed BEFORE (2026-07-25) with a broken fallback chain
(dead `deepseek-chat` + unconfigured ollama). Each fix must check the pinned
model AND the fallback list.

## Fix Applied

Dual write into `/root/.openclaw/state/openclaw.sqlite`:

1. `payload_model` → `deepseek/deepseek-v4-flash`
2. `job_json.payload.model` → `deepseek/deepseek-v4-flash` (via Python json rewrite, preserving all other fields)

## Open Items

- Gateway was NOT restarted at fix time (started 07:50 UTC, edit ~11:00 UTC).
  If the job fails again on the next Sunday run, restart `openclaw-gateway`
  so the scheduler re-reads the DB. Check:
  `systemctl show openclaw-gateway --property=ActiveEnterTimestamp`
- `openclaw cron list` CLI was broken by `models.providers.bailian-token-plan-responses: Invalid input`
  — gateway ran anyway; sqlite3 is the reliable path.
- Gateway startup failures seen at
  `/root/.openclaw/logs/stability/*-gateway.startup_failed.json` referencing
  `xiaomi-coding` and `mimo-token-plan` providers — these were NOT present in
  the current openclaw.json, suggesting config churn; re-validate before
  relying on the CLI.

## Recurrence (2026-08-05)

Same job `a4301644` failed AGAIN on 2026-08-05 — but the live diagnosis differed:
`payload_model` was **EMPTY** (not `minimax/deepseek-v4-flash` as the old error string
claimed). The allowlist rejection error text is STALE — it quotes the allowlist state
at last failure time, not current.

Fix applied (dual write, same as before):
1. `payload_model` → `deepseek/deepseek-v4-flash`
2. `job_json.payload.model` → same (python json rewrite, preserve all fields)
3. DB backup first: `cp openclaw.sqlite openclaw.sqlite.bak-weekly-gov-<ts>`

**Why `deepseek/deepseek-v4-flash`, NOT `minimax/…`:** the `minimax` provider catalog
only has MiniMax-M2.7/M2.7-highspeed/M3 — it does NOT define `deepseek-v4-flash`.
The allowlist entry `minimax/deepseek-v4-flash` exists (added 08-01) but a runtime call
would fail "model not found". Check the provider catalog, not just the allowlist.

Also verified: `deepseek` provider has `deepseek-v4-flash`; next run 2026-08-08 11:00 UTC.
If it fails again on Sunday, restart `openclaw-gateway` so the scheduler re-reads the DB.

## Reference Data

- Cron store schema: `cron_jobs` table — key columns: store_key, job_id, name,
  enabled, schedule_kind/expr/tz, session_target, wake_mode, payload_kind,
  payload_message, payload_model, payload_fallbacks_json, job_json,
  state_json, last_run_status, last_error, next_run_at_ms.
- Run log: `cron_run_logs` — job_id, ts, status, error, summary, run_id.
