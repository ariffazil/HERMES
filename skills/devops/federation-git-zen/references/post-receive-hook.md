# Post-Receive Hook — Auto-Deploy to VPS

> When a push arrives at the VPS git mirror, this hook auto-syncs the deployed directory so you never manually update two copies.

## The Problem

The arifOS federation has two copies of the code:
- `~/arifOS` — source/development (where you commit and push)
- `/opt/arifos/app` — deployed runtime (where systemd services run)

**Both are intentional.** The separation enables diagnostic: "repo says fixed, front door serves old build" is only detectable because they're two directories. Deleting `/opt/arifos/app` would blind the diagnostic.

**The pain is manual sync, not the two copies.** The fix is automation, not deletion.

## The Hook

Place this at `/root/git-mirrors/arifOS.git/hooks/post-receive`:

```bash
#!/bin/bash
# post-receive — auto-sync /opt/arifos/app on push to mirror
# Push to source → mirror fires → pulls /opt → reinstalls → restarts → health-checks

set -euo pipefail

DEPLOY_DIR="/opt/arifos/app"
SERVICE="arifos.service"
HEALTH_URL="http://localhost:8088/health"
LOG_FILE="/var/log/arifos-deploy.log"

log() { echo "[$(date -Iseconds)] $*" | tee -a "$LOG_FILE"; }

while read oldrev newrev refname; do
    if [[ "$refname" != "refs/heads/main" ]]; then
        log "SKIP: push to $refname (not main)"
        continue
    fi

    log "DEPLOY: $oldrev → $newrev on $refname"

    cd "$DEPLOY_DIR"
    git fetch origin main 2>&1 | tee -a "$LOG_FILE"
    git reset --hard origin/main 2>&1 | tee -a "$LOG_FILE"

    # Reinstall editable (fixes split-brain: import path = run path)
    /opt/arifos/venv/bin/pip install -e "$DEPLOY_DIR" --quiet 2>&1 | tee -a "$LOG_FILE"

    # Restart service
    systemctl daemon-reload
    systemctl restart "$SERVICE"
    sleep 8

    # Health check
    if curl -sf --max-time 10 "$HEALTH_URL" > /dev/null 2>&1; then
        log "✓ HEALTHY — deploy complete"
    else
        log "✗ HEALTH CHECK FAILED — manual investigation required"
        exit 1
    fi
done
```

## Installation

```bash
# Create the hook
cat > /root/git-mirrors/arifOS.git/hooks/post-receive << 'HOOK'
... (content above) ...
HOOK

chmod +x /root/git-mirrors/arifOS.git/hooks/post-receive
```

## Verification

```bash
# Push from source to trigger the hook
cd ~/arifOS
git push vps-mirror main

# Watch the deploy log
tail -f /var/log/arifos-deploy.log

# After deploy, verify the surface
curl -s http://localhost:8088/health | python3 -m json.tool | grep -E "substrate|owner_summary"
```

## Split-Brain Venv Fix

The hook includes `pip install -e "$DEPLOY_DIR"` to ensure Python's import path and systemd's WorkingDirectory agree. Without this, the editable venv may import from `~/arifOS` while the service runs from `/opt/arifos/app` — a split-brain where "which code is actually running" depends on Python's resolution order.

**The separation of secrets/mounts between dev and prod stays correct.** Only the code the process imports must come from one place.

## Pitfalls

- **Don't delete `/opt/arifos/app`.** The separation is correct infrastructure. The fix is automation, not deletion.
- **The hook runs on EVERY push to the mirror.** If you push from GitHub → mirror, the hook fires. If you push from local → mirror, the hook fires. Either way, deployed updates.
- **First deploy after hook install should be manual.** Run the hook commands by hand once to verify the pipeline works before relying on automation.