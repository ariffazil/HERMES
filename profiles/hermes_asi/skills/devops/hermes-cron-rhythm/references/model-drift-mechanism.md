# Model Drift Mechanism (Hermes Cron)

Reverse-engineered 2026-07-17 from live system behavior + source inspection.

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

## Fix Patterns

### Fix One Job (pin to current)
```python
cronjob(action='update', job_id='<id>',
        model={'model': 'deepseek-v4-pro', 'provider': 'deepseek'})
```
Pinning makes the job immune to future drift (but also prevents it from auto-following model changes).

### Fix One Job (rebased unpinned)
```python
cronjob(action='update', job_id='<id>', model={})
```
Clears snapshots to current global. Job will drift again on next model change.

### Fix All Jobs (Watchdog)
Model Drift Watchdog (`5a29d4fd77b8`): runs hourly, pinned to `deepseek/deepseek-chat`, detects drift across all jobs, updates affected ones to match current global config. Silent when clean.

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

# Find all drifted jobs
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
