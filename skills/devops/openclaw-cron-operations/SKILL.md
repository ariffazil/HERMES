---
name: openclaw-cron-operations
description: >-
  Diagnose and fix OpenClaw (AGI) cron jobs AND the autonomous health probe
  system — locate the SQLite job store, decode model allowlist rejections,
  apply dual-write model fixes, work around a broken `openclaw` CLI, and
  diagnose probe RED/YELLOW alerts. Separate from Hermes' own cron system.
category: devops
forged: 2026-08-01
---

# OpenClaw Cron Operations

OpenClaw's cron system is entirely separate from Hermes' cron. When AGI
surfaces a cron failure ("FORGE Weekly Governance Roll-up", "repo-watch",
any OpenClaw scheduled agent turn), the store, validation rules, and fix
paths are all different from `hermes cron` / `cronjob` tooling. Do not
search Hermes config for these jobs — they live in OpenClaw's own store.

## When to Use

- AGI reports an OpenClaw cron job failed (allowlist rejection, FallbackSummaryError, model errors)
- Error text mentions `agents.defaults.models allowlist` or `cron payload.model`
- `openclaw cron list` / `openclaw cron update` fails with `InvalidConfigError`
- Need to change an OpenClaw cron job's model, schedule, or delivery target
- User reports `🫀 openclaw probe RED (N): <items>` — probe health alert diagnosis

## Key Facts

| Item | Location |
|------|----------|
| Live cron store | SQLite `/root/.openclaw/state/openclaw.sqlite`, table `cron_jobs` |
| Run history | table `cron_run_logs` (same DB) |
| Model allowlist | `agents.defaults.models` in `/root/.openclaw/openclaw.json` |
| Stale trap | `/root/.openclaw/cron/jobs.json.migrated` and `jobs-state.json.migrated` are OLD migration artifacts — do not edit them |
| Gateway unit | `openclaw-gateway.service` |

The `cron_run_logs.store_key` column shows `/root/.openclaw/cron/jobs.json`
— misleading legacy namespace. The SQLite DB is the source of truth.

## The Model Allowlist Trap (most common failure)

Cron jobs pin `payload.model` with a BARE name (e.g. `deepseek-v4-flash`).
Preflight rejects bare names — the allowlist requires provider-prefixed
IDs (e.g. `deepseek/deepseek-v4-flash`, `bailian-token-plan/deepseek-v4-flash`).

Error signature:
```
cron payload.model 'deepseek-v4-flash' rejected by agents.defaults.models
allowlist: minimax/deepseek-v4-flash is not in [bailian-token-plan/deepseek-v4-flash, ...]
```

### Fix — DUAL WRITE, then RESTART

1. **Column:** `UPDATE cron_jobs SET payload_model = 'deepseek/deepseek-v4-flash' WHERE job_id='...';`
2. **job_json:** rewrite `job_json.payload.model` to the same provider-prefixed value
   (job_json is what the runner actually loads — the column alone is not enough).
3. **Restart gateway:** `systemctl restart openclaw-gateway`
   Jobs are cached in memory at gateway startup. A DB edit alone looks fixed
   but the next run still fails until the gateway re-reads the store.

```python
# Dual-write example (keeps the rest of job_json intact)
import sqlite3, json
db = sqlite3.connect('/root/.openclaw/state/openclaw.sqlite')
cur = db.cursor()
cur.execute("SELECT job_json FROM cron_jobs WHERE job_id=?", (JOB_ID,))
d = json.loads(cur.fetchone()[0])
d['payload']['model'] = 'deepseek/deepseek-v4-flash'
cur.execute("UPDATE cron_jobs SET job_json=?, payload_model=? WHERE job_id=?",
            (json.dumps(d), 'deepseek/deepseek-v4-flash', JOB_ID))
db.commit()
```

## Broken CLI Workaround

`openclaw cron list` runs full config validation. If `openclaw.json` contains
a provider entry that fails validation (seen flagged: `bailian-token-plan-responses`,
`xiaomi-coding`, `mimo-token-plan` → `Invalid input`), the CLI refuses to run
even though the gateway keeps working. **Do fixes via direct sqlite3 — no CLI needed.**

`openclaw doctor --fix` may be suggested by error messages — it can rewrite
provider config broadly. Prefer targeted sqlite edits.

## sqlite3 Recipes

```bash
DB=/root/.openclaw/state/openclaw.sqlite

# List all jobs (name, enabled, pinned model)
sqlite3 $DB "SELECT job_id, name, enabled, payload_model FROM cron_jobs;"

# Inspect one job: payload, schedule, delivery, last error
sqlite3 $DB "SELECT job_json, last_error, next_run_at_ms FROM cron_jobs WHERE job_id='<id>';"

# Recent run history
sqlite3 $DB "SELECT status, error FROM cron_run_logs WHERE job_id='<id>' ORDER BY rowid DESC LIMIT 5;"

# Verify fix applied
sqlite3 $DB "SELECT payload_model, json_extract(job_json,'$.payload.model') FROM cron_jobs WHERE job_id='<id>';"
```

Note: `next_run_at_ms` is epoch milliseconds — convert before reporting
`date -d @$((ms/1000))`.

## Pitfalls

- **`.migrated` files are traps.** The live store is the SQLite DB; the JSON
  migration files under `/root/.openclaw/cron/` are stale.
- **Bare model names ALWAYS fail.** The allowlist is provider-prefixed only.
- **Column-only or job_json-only edits are insufficient.** Dual write both.
- **Gateway caches cron definitions at startup.** DB-only edits appear fixed
  until the next scheduled run fails again. Restart the gateway to apply —
  it IS disruptive (AGI's Telegram bridge), so coordinate or schedule it.
- **`openclaw cron list` failing ≠ cron broken.** Config validation failure
  blocks the CLI but not the scheduler. Verify the gateway is up and read the
  DB directly instead of trusting the CLI's error.
- Check `systemctl show openclaw-gateway --property=ActiveEnterTimestamp`
  vs. when you edited the DB — if the gateway started before your edit, the
  fix is NOT live yet.

## Related Skills

- `model-drift-watcher` — Hermes cron model drift (different system)
- `hermes-cron-rhythm` — Hermes cron design (different system)
- `federation-checkup` — federation-wide health protocol

Session-specific detail: `references/forge-weekly-allowlist-fix-2026-08-01.md`
Probe diagnosis: `references/openclaw-probe-diagnosis.md`
