# Model Drift Mechanism (Hermes Cron)

Reverse-engineered 2026-07-17 from live system behavior + source inspection.

## Structural Property: Model Pinning Vacuum

**Confirmed 2026-07-27 by Model Drift Watchdog live run.** Cron jobs in Hermes have NO per-job model/provider pinning mechanism at the CLI level. This is not a transient state — it is a structural property of the system:

- `hermes cron create` has NO `--model` or `--provider` flags
- `hermes cron edit` has NO `--model` or `--provider` flags
- The `cron:` section in `config.yaml` has NO per-job sub-objects — only a top-level `provider: ''` field (for global fallback)
- ALL jobs inherit model/provider from the global `model:` section in `config.yaml`
- The sanctioned way to pin/change a job's model/provider is the **`update_job()` library function** in `cron/jobs.py` (L1286) — the `cronjob(action='update')` MCP tool wraps it. Callable directly with the hermes venv python when the MCP tool isn't exposed (see Fix Patterns). Direct `~/.hermes/cron/jobs.json` editing works but races with the scheduler's post-run writes and is only a fallback.

**Correction (2026-07-31):** The earlier claim "the only way to pin is direct jobs.json editing" was wrong — `update_job()` has always been the canonical path; the CLI simply doesn't expose it.

**Consequence:** The Model Drift Watchdog's "zero drift" finding is the expected steady state. Any drift can only be introduced by direct `jobs.json` edits (which the watchdog then detects and fixes). The CLI cannot create or maintain drift — only remediate it.

**Watchdog detection procedure (confirmed 2026-07-27):**
1. Read global config from `~/.hermes/config.yaml` → `model.provider`, `model.default`/`model.model`
2. List jobs via `hermes cron list` — this shows all jobs but OMITS model/provider fields (CLI blind spot)
3. Verify `hermes cron create --help` and `hermes cron edit --help` have no `--model`/`--provider` flags — confirms pinning is structurally impossible via CLI
4. Only then inspect `~/.hermes/cron/jobs.json` directly for any explicit `model`/`provider` fields per job
5. Jobs with `no_agent: true` are structurally immune (snapshots always null)
6. Jobs with null/empty model and provider inherit from global — no drift possible
7. Only jobs with non-null model/provider that differ from global are drifted — and those can only exist via direct JSON edit

## Source Locations

| What | File | Lines |
|------|------|-------|
| Snapshot creation | `cron/jobs.py` | `_compute_provider_model_snapshots()` at L978-1020 |
| no_agent immunity | `cron/jobs.py` | L998: `if bool(no_agent): return None, None` |
| Drift guard check | `cron/scheduler.py` | L3011-3058 in `run_job()` |
| Drift guard gating | `cron/scheduler.py` | L3032: `if _provider_snapshot and not (job.get("provider") or "").strip()` |
| Job storage | `cron/jobs.py` | L71: `JOBS_FILE = CRON_DIR / "jobs.json"` |
| Default model resolution | `cron/jobs.py` | `_resolve_default_model_snapshot()` at L930-965 |

## Snapshot Lifecycle

```
create_job()
  └─ for each UNPINNED axis:
       snapshot = current_global_config
       store as provider_snapshot / model_snapshot

run_job()
  └─ for each axis with non-null snapshot AND no explicit pin:
       if current_global != snapshot → SKIP + drift error
       else → proceed
```

## Immunity Rules

1. **`no_agent: true`** → snapshots always `null` → drift guard never fires
2. **Explicit `provider` + `model` pin** → snapshots stay `null` → drift guard skipped (has explicit pin)
3. **Unpinned (null)** → snapshots captured at creation → compared at every fire
4. **Partial pin** (e.g., only `model` pinned, `provider` null) → only the unpinned axis checked

## Sync Pin vs Immunity Pin — Discrimination Procedure (2026-07-31)

**Do NOT treat every explicit pin as an intentional immunity marker.** Pins are usually auto-stamped from the global config at job creation (all 8 jobs created Jul 5–26 carried `deepseek/deepseek-v4-flash`, matching the global of that era). When global moves, those pins are STALE and the operator's watchdog prompt explicitly instructs updating them ("if the pinned model/provider DIFFERS from current, update it to match current").

**Evidence-based procedure:**

1. **Read the watchdog's own run history** — `/root/.hermes/cron/output/5a29d4fd77b8/*.md` (one file per run, `## Response` section):
   - Past runs saying "in sync with global config" or actively fixing a pin to match global (e.g. 2026-07-30: nightly-seal `deepseek/deepseek-v4-flash` → `deepseek-v4-flash`, "in sync with global config") prove the pins are **watchdog-maintained sync points** → update them.
   - A prior run's "intentional immunity pins" claim is a self-report, not evidence — check whether it cited any operator intent.
2. **Cross-check pins against creation-time global**: `created_at` in jobs.json vs `~/.hermes` git history of config.yaml `model:` section. Pin == creation-time global ⇒ auto-stamp.
3. **Positive evidence of intent** (only this justifies leaving a pin): explicit operator note, stable divergence across multiple global switches, or prompt text naming the provider as deliberate.

**Provider-resolution check:** a pinned provider absent from config.yaml `providers:` keys is NOT proof of breakage — providers can still resolve via `auth.json` `credential_pool` (e.g. `deepseek` was absent from `providers:` but present in the pool; all pinned jobs ran `last_status: ok`). Check both files before declaring a pin dead.

**Proven 2026-07-31:** 8 pinned jobs (`deepseek/deepseek-v4-flash`) updated to `mulerouter/deepseek-v4-flash` after the history check proved they tracked global. The 2026-07-28 "7 immunity pins" case is hereby demoted: it only demonstrated the watchdog skipping pins, never operator intent.

## Field Schema

Model/provider are stored as **simple string fields** directly on each job dict in `jobs.json`:

```json
{
  "id": "abc123...",
  "name": "my-job",
  "model": "deepseek-v4-flash",
  "provider": "deepseek",
  "provider_snapshot": null,
  "model_snapshot": null,
  "base_url": null,
  "context_from": null,
  "skills": [],
  "skill": null,
  ...
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `model` | string\|null | Explicit model pin. `null` = inherit from global config. |
| `provider` | string\|null | Explicit provider pin. `null` = inherit from global config. |
| `model_snapshot` | string\|null | Global model at job creation (for unpinned jobs). `null` for pinned or no_agent jobs. |
| `provider_snapshot` | string\|null | Global provider at job creation (for unpinned jobs). `null` for pinned or no_agent jobs. |
| `base_url` | string\|null | Custom API base URL override. `null` = use global default for the provider. |
| `context_from` | string\|null | References context from another session. `null` = no inheritance. |
| `skills` | string[] | LLM skills loaded for agent-driven jobs. Empty for no_agent or skill-less jobs. |
| `skill` | string\|null | Legacy single-skill field. Usually `null` in modern jobs (use `skills[]`). |
| `no_agent` | boolean | When `true`, the job runs a script without LLM inference. Immune to model drift. |

- Pinned jobs: `model`/`provider` have non-empty string values; snapshots are `null`
- Unpinned jobs: `model`/`provider` are `null`; snapshots capture global config at creation
- `no_agent: true` jobs: all model/provider fields are always ignored

## Fix Patterns

### CLI Limitation

**`hermes cron edit` has NO `--model` or `--provider` flags.** You cannot fix model drift via the Hermes CLI. Use the `update_job()` library function (canonical — the cronjob MCP tool wraps it) or direct `jobs.json` editing as fallback.

### Fix One Job (canonical — `update_job()` library, PREFERRED)

```bash
# Backup first (bak-drift-<timestamp> convention)
cp ~/.hermes/cron/jobs.json ~/.hermes/cron/jobs.json.bak-drift-$(date +%Y%m%d%H%M%S)

# Run with the HERMES VENV python so cron.jobs imports resolve
/usr/local/lib/hermes-agent/venv/bin/python3 - <<'PY'
from cron.jobs import update_job, load_jobs
jid = "<JOB_ID>"
before = next(j for j in load_jobs() if j["id"] == jid)
res = update_job(jid, {"provider": "mulerouter", "model": "deepseek-v4-flash"})
print(f"{before['name']}: {before.get('provider')}/{before.get('model')} -> "
      f"{res.get('provider')}/{res.get('model')}")
PY
```

`update_job` re-runs `_compute_provider_model_snapshots()` when inference fields change: pinned axes → snapshots recomputed to `null`; unpinned axes → fresh snapshot captured from current global. Takes the jobs lock and saves atomically — safe against the scheduler's concurrent writes (jobs.json is rewritten after every job run, so raw file edits can race). Bulk version: `scripts/sync-pinned-jobs.py` in the skill.

### Fix One Job (fallback — direct JSON edit)
```bash
cp ~/.hermes/cron/jobs.json ~/.hermes/cron/jobs.json.bak-$(date +%Y%m%d%H%M%S)
python3 -c "
import json
with open('/root/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    if j['id'] == '<JOB_ID>':
        j['model'] = 'deepseek-v4-flash'
        j['provider'] = 'deepseek'
        print(f'Fixed: {j.get(\"name\")}')
with open('/root/.hermes/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
"
```
Pinning makes the job immune to future drift (but also prevents it from auto-following model changes).

### Fix One Job (rebased unpinned — direct JSON edit)
Set both `model` and `provider` to empty string in jobs.json. The cron system will capture fresh snapshots from global config on next run. Job will drift again on next model change.

### Fix All Jobs (Watchdog)
Model Drift Watchdog (`5a29d4fd77b8`): runs hourly, detects drift across all jobs, updates affected ones to match current global config. Silent when clean.

**Watchdog workflow:**
1. Read global config from `~/.hermes/config.yaml`
2. List jobs via `hermes cron list`
3. Parse `~/.hermes/cron/jobs.json` — inspect each job's `model` and `provider` fields
4. Skip `no_agent: true` jobs
5. For jobs where pinned model/provider differs from global: edit the JSON fields directly
6. Backup before edit; verify after

**Proven 2026-07-25:** 4 paused jobs pinned to `flame/free`/`custom:flame` found drifted against global `deepseek-v4-flash`/`deepseek`. Fixed via direct JSON edit.

## Diagnostic Commands

```bash
# Read current global model
python3 -c "
import yaml, os
with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    cfg = yaml.safe_load(f) or {}
m = cfg.get('model', {})
print(f'provider: {m.get(\"provider\",\"\")}')
print(f'model: {m.get(\"default\",\"\") or m.get(\"model\",\"\")}')
"

# Inspect a job's snapshots
python3 -c "
import json
with open(os.path.expanduser('~/.hermes/cron/jobs.json')) as f:
    data = json.load(f)
for j in data['jobs']:
    if j['id'] == '<job_id>':
        for k in ['provider','model','provider_snapshot','model_snapshot','no_agent']:
            print(f'{k}: {j.get(k)}')
"

# Full inventory sweep — categorize ALL jobs by drift status in one view
python3 << 'PYEOF'
import json, yaml, os

home = os.path.expanduser('~/.hermes')
with open(f'{home}/config.yaml') as f:
    cfg = yaml.safe_load(f) or {}
m = cfg.get('model', {})
if isinstance(m, dict):
    cur_prov = (m.get('provider','') or '').strip().lower()
    cur_model = (m.get('default','') or m.get('model','') or '').strip().lower()
else:
    cur_prov, cur_model = '', ''

print(f'Global: {cur_prov}/{cur_model}')
print()

with open(f'{home}/cron/jobs.json') as f:
    data = json.load(f)

no_agent_count = 0
pinned_match = 0
pinned_drift = []
inherited_null = 0
snapshot_drift = []

for j in data['jobs']:
    name = j.get('name', j['id'])
    no_agent = j.get('no_agent', False)
    model = (j.get('model') or '').strip()
    provider = (j.get('provider') or '').strip()
    ms = (j.get('model_snapshot') or '').strip().lower()
    ps = (j.get('provider_snapshot') or '').strip().lower()

    if no_agent:
        no_agent_count += 1
        continue

    if model and provider:
        if model.lower() == cur_model and provider.lower() == cur_prov:
            pinned_match += 1
        else:
            pinned_drift.append((name, model, provider))
    else:
        inherited_null += 1
        if ps and cur_prov and ps != cur_prov:
            snapshot_drift.append((name, 'provider', ps, cur_prov))
        if ms and cur_model and ms != cur_model:
            snapshot_drift.append((name, 'model', ms, cur_model))

print(f'Total jobs: {len(data["jobs"])}')
print(f'  no_agent (skipped):           {no_agent_count}')
print(f'  Pinned + matching:            {pinned_match}')
print(f'  Pinned + DRIFTED:             {len(pinned_drift)}')
print(f'  Inheriting global (no pin):   {inherited_null}')
print(f'  Snapshot DRIFTED:             {len(snapshot_drift)}')
print()

if pinned_drift:
    print('=== PINNED DRIFT ===')
    for n, m, p in pinned_drift:
        print(f'  {n}: pinned {p}/{m} != global {cur_prov}/{cur_model}')
    print()
if snapshot_drift:
    print('=== SNAPSHOT DRIFT ===')
    for n, axis, old, cur in snapshot_drift:
        print(f'  {n}: {axis} snapshot {old} != global {cur}')
    print()
if not pinned_drift and not snapshot_drift:
    print('All clear — no drift detected.')
PYEOF

# Legacy drift finder (checks snapshots only — the sweep above is more comprehensive)
python3 -c "
import json, yaml, os
home = os.path.expanduser('~/.hermes')
with open(f'{home}/config.yaml') as f:
    cfg = yaml.safe_load(f) or {}
m = cfg.get('model', {})
cur_prov = (m.get('provider','') if isinstance(m,dict) else '').strip().lower()
cur_model = (m.get('default','') or m.get('model','') if isinstance(m,dict) else (m if isinstance(m,str) else '')).strip().lower()
with open(f'{home}/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    ps = (j.get('provider_snapshot') or '').strip().lower()
    ms = (j.get('model_snapshot') or '').strip().lower()
    has_pin = bool((j.get('provider') or '').strip()) and bool((j.get('model') or '').strip())
    if j.get('no_agent'): continue
    drifted = []
    if ps and not (j.get('provider') or '').strip() and cur_prov and ps != cur_prov:
        drifted.append(f'provider {ps}->{cur_prov}')
    if ms and not (j.get('model') or '').strip() and cur_model and ms != cur_model:
        drifted.append(f'model {ms}->{cur_model}')
    if drifted:
        print(f\"DRIFTED: {j.get('name', j['id'])} — {'; '.join(drifted)}\")
"
```

## Proven Cases

| Date | Trigger | Jobs Affected | Fix |
|------|---------|---------------|-----|
| 2026-07-17 | mimo-v2.5-pro -> deepseek-v4-pro | Trading Position Monitor | Pinned to deepseek, then watchdog built |
| 2026-07-31 | deepseek -> mulerouter (global) | 8 pinned jobs (evening-digest, weekly-deep-brief, daily-news-briefing, weekly-reflection, ASI World Sensorium, Model Drift Watchdog, SyedOS Ringkasan Harian, nightly-seal) | Stale sync pins updated to mulerouter/deepseek-v4-flash via `update_job()`; history check proved pins tracked global |
