# Model Drift Watcher – Quick Reference

## Detect drift
1. Read global config (`~/.hermes/config.yaml`) → output provider and model.
2. Parse `~/.hermes/cron/jobs.json` (ignore numeric prefixes).
3. For each job with `model` or `provider`:
   - Compare against global values.
   - Report mismatches.

## Fix drift
Use `hermes cronjob update job_id=<ID> model=<model> provider=<provider>`.

## Script
`scripts/check_drift.py` performs detection and prints mismatches.

## Notes
- Ignore `no_agent` jobs.
- Keep model/provider values exactly as shown in the global config.