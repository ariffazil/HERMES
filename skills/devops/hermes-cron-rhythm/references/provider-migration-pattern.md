# Provider Migration Pattern — Cron Jobs

Forged 2026-08-03. When a provider dies and cron jobs need mass migration.

## Scenario

Provider `qwen-token-plan` died. All 15+ cron jobs using it failed with 401/404.
Canonical live provider: `bailian-token-plan`.

## Fix Pattern

```bash
# 1. Backup
cp /root/HERMES/cron/jobs.json /root/HERMES/cron/jobs.json.bak-$(date +%Y%m%d-%H%M%S)

# 2. Bulk rename all instances
python3 -c "
import json
with open('/root/HERMES/cron/jobs.json') as f:
    data = json.load(f)
fixed = 0
for j in data['jobs']:
    if j.get('provider') == 'qwen-token-plan':
        j['provider'] = 'bailian-token-plan'
        fixed += 1
        print(f'Fixed: {j[\"name\"]}')
with open('/root/HERMES/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Total: {fixed}')
"

# 3. Verify
python3 -c "
import json
with open('/root/HERMES/cron/jobs.json') as f:
    data = json.load(f)
dead = [j['name'] for j in data['jobs'] if j.get('provider') == 'qwen-token-plan']
print(f'Still on qwen-token-plan: {len(dead)}')
"
```

## Live Models (bailian-token-plan)

- ✅ `qwen3.6-flash` — confirmed live
- ✅ `deepseek-v4-pro` — confirmed live  
- ❌ `deepseek-v4-flash` — 403 access denied
- ❌ `deepseek-v4-flash-0731` — unknown, likely 403

For light cron tasks, prefer `qwen3.6-flash`. For heavy reasoning, use `deepseek-v4-pro`.

## Pitfall

The fix may not persist across daemon restarts or scheduler rewrites. Verify after any gateway restart or config change. The previous fix (2026-08-02, `qwen-token-plan`→`bailian-token-plan`) was silently reverted and 15 jobs reverted to dead provider within 24h. Unknown root cause — suspect `jobs.json` rewrite race from scheduler.
