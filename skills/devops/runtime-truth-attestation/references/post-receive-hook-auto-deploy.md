# Post-Receive Hook — Auto-Deploy Pattern

> **Proven 2026-08-02** — arifOS deployment session
> **Purpose:** Eliminate manual dual-tree updates. Push to source → mirror fires → deployed auto-syncs.

## The Problem

The arifOS deployment has two trees:
- **Source tree:** `~/arifOS` (git working copy, development)
- **Deploy tree:** `/opt/arifos/app` (production runtime, systemd WorkingDirectory)

Every deploy requires manual sync between them. The post-receive hook automates this: push to the git mirror, and the hook pulls the deployed tree, rebuilds, reinstalls, and restarts.

## Hook Location

```
/root/git-mirrors/arifOS.git/hooks/post-receive
```

The mirror receives pushes from both `~/arifOS` (local) and `origin/github` (remote). Either trigger fires the hook.

## Hook Template

```bash
#!/bin/bash
# /root/git-mirrors/arifOS.git/hooks/post-receive
# Auto-deploy: push to mirror → pull /opt/arifos/app → reinstall → restart → health-check

set -euo pipefail

DEPLOY_DIR="/opt/arifos/app"
VENV_DIR="/opt/arifos/venv"
SERVICE="arifos.service"
HEALTH_URL="http://localhost:8088/health"
LOG_FILE="/var/log/arifos-auto-deploy.log"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"; }

# Read the ref being updated
while read oldrev newrev refname; do
    if [ "$refname" != "refs/heads/main" ]; then
        log "SKIP: push to $refname (not main)"
        continue
    fi

    log "DEPLOY: $oldrev → $newrev"

    # 1. Pull into deploy tree
    cd "$DEPLOY_DIR"
    git fetch origin main 2>&1 | tee -a "$LOG_FILE"
    git reset --hard origin/main 2>&1 | tee -a "$LOG_FILE"

    # 2. Reinstall editable package
    "$VENV_DIR/bin/pip" install -e "$DEPLOY_DIR" 2>&1 | tee -a "$LOG_FILE"

    # 3. Restart service
    systemctl daemon-reload
    systemctl restart "$SERVICE" 2>&1 | tee -a "$LOG_FILE"

    # 4. Wait for startup
    sleep 5

    # 5. Health check
    if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
        log "HEALTH: OK"
    else
        log "HEALTH: FAIL — service may need manual intervention"
        # Optionally: trigger alert, rollback, or notify
        # curl -X POST https://hooks.slack.com/... -d '{"text":"arifOS deploy failed health check"}'
    fi

    # 6. Update git commit stamp
    git -C "$DEPLOY_DIR" rev-parse HEAD > "$DEPLOY_DIR/.git_commit"
    git -C "$DEPLOY_DIR" rev-parse HEAD > "$DEPLOY_DIR/arifosmcp/.git_commit"
done
```

## Verification

After setting up the hook:
```bash
# Test: push to mirror triggers deploy
cd /root/arifOS && git push vps-mirror main

# Monitor the log
tail -f /var/log/arifos-auto-deploy.log

# Verify health after deploy
curl -s http://localhost:8088/health | python3 -c "
import json, sys; d = json.load(sys.stdin)
print(f'status={d.get(\"status\")} substrate_gate={d.get(\"substrate_gate\")}')
"
```

## Why This Ends the Manual Deploy

**Before:** Push to source → SSH to VPS → pull /opt → reinstall → restart → health-check. Two separate actions, error-prone.

**After:** Push to source → hook fires → everything happens automatically. One action, one surface.

The two trees stay (correctly — dev ≠ prod), but your hands touch only one.

## Pitfalls

1. **Don't deploy on every push to every branch.** The hook should only fire on `refs/heads/main`. Feature branch pushes shouldn't trigger deploys.

2. **The hook runs as the git user.** Ensure the git user has `sudo` access to `systemctl restart arifos` or use a sudoers rule:
   ```
   git ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart arifos.service
   ```

3. **Editable install vs wheel.** The hook uses `pip install -e` (editable) which means the venv imports from the deploy tree. If you switch to wheel-based deploys, change the hook to use `pip install --no-deps --force-reinstall dist/arifos-*.whl`.

4. **Health check is synchronous.** If the health check takes >5s, increase the timeout. The hook blocks until health check completes.