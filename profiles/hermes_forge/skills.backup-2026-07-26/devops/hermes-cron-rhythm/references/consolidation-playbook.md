# Cron Consolidation Playbook

When the cron job list has drifted (paused jobs, orphan scripts, redundant system cron entries), use this playbook to zen and seal.

## Step 1: Audit

```bash
# List all Hermes cron jobs
# Use cronjob action='list'

# List system cron entries
crontab -l

# List all scripts
ls -la /root/.hermes/scripts/*.sh

# Check for orphan scripts (not referenced by any active job)
for f in /root/.hermes/scripts/*.sh; do
  name=$(basename "$f" .sh)
  echo "$f"
done
```

## Step 2: Classify Each Job

| Status | Action |
|--------|--------|
| ACTIVE + delivering to right place | Keep |
| PAUSED + logic absorbed by active job | Remove from Hermes |
| PAUSED + logic NOT absorbed | Evaluate: absorb or reactivate |
| System cron + redundant with Hermes | Remove from system cron |
| Orphan script + no job references | Archive |

## Step 3: Extract Before Remove

Before removing a paused job, verify its logic is captured:
- **federation-health** → organ health check is in drift-alert.sh (every 4h) and morning-brief.sh (daily)
- **well-entropy-seal** → WELL pulse is in morning-brief.sh (daily)
- **midday-scan** → replaced by drift-alert.sh (alert-only)

## Step 4: Execute Cleanup

```bash
# 1. Back up system crontab
crontab -l > /root/.hermes/scripts/.system-crontab-backup-$(date +%Y%m%d).txt

# 2. Archive orphan scripts
mkdir -p /root/.hermes/scripts/.archive-$(date +%Y-%m-%d)
mv /root/.hermes/scripts/<orphan>.sh /root/.hermes/scripts/.archive-$(date +%Y-%m-%d)/

# 3. Remove redundant system cron entries
crontab -l | grep -v "<pattern>" | crontab -

# 4. Remove paused Hermes jobs (use cronjob action='remove')

# 5. Add constitutional scope headers to remaining scripts

# 6. Clean up state files
rm -f /root/.hermes/scripts/.drift-alert-state.json
```

## Step 5: Verify

```bash
# Only active jobs should remain
# cronjob action='list'

# System crontab should have no redundant entries
crontab -l

# Archive should contain removed scripts
ls /root/.hermes/scripts/.archive-*/
```

## Known Redundancies (2026-07-12)

| Hermes Job | System Cron Entry | Resolution |
|------------|-------------------|------------|
| federation-health (paused) | federation-health-cron.sh every 2h | Both removed; logic in drift-alert |
| well-entropy-seal (paused) | well-entropy-seal.sh every 6h | Both removed; logic in morning-brief WELL pulse |
