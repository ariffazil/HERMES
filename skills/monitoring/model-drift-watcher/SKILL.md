---
name: model-drift-watcher
description: Detect and fix model/provider drift for pinned Hermes cron jobs.
category: monitoring
---
# Model Drift Watcher

**Purpose**: Detect and fix model/provider drift for pinned Hermes cron jobs.

## Trigger
Any time you need to verify that job‑level model/provider pins match the current global configuration.

## Steps

1. **Read global config**  
   ```bash
   python3 -c "
   import yaml, os
   with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
       cfg = yaml.safe_load(f) or {}
   m = cfg.get('model', {})
   if isinstance(m, dict):
       print(f'provider:{m.get(\"provider\",\"\")}')
       print(f'model:{m.get(\"default\",\"\") or m.get(\"model\",\"\")}')
   elif isinstance(m, str):
       print(f'model:{m}')
   "
   ```

2. **List cron jobs**  
   ```bash
   hermes cron list
   ```  
   Or parse `~/.hermes/cron/jobs.json` directly.

3. **Identify pinned jobs** – jobs where `model` or `provider` is non‑null.

4. **Compare** each pinned job against the values printed in step 1.  
   - If a mismatch is found, note the job ID, name, current `model`, current `provider`, and the expected values.

5. **Update** the mismatched job:  
   ```bash
   hermes cronjob update job_id=<ID> model=<new_model> provider=<new_provider>
   ```

6. **Verify** by re‑running the detection step.

## Common Pitfalls
- Do **not** update `no_agent` jobs (they have no model/provider).
- The JSON format in `jobs.json` is line‑delimited with a numeric prefix; use `grep` or a small parser.
- Preserve quoting and exact spelling of model/provider values.

## Script (optional)
A ready‑made Python helper `scripts/check_drift.py` (see `scripts/check_drift.py` in this skill) automates steps 1‑4.

## License
Public domain – feel free to copy, modify, and reuse.