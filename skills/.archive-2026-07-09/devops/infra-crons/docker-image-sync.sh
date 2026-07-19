#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  docker-image-sync — Pull + SHA256 verify Hermes image       ║
# ║  Every 6 hours. Logs to /var/log/docker-image-sync.log      ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

IMAGE="nikolaik/python-nodejs:python3.11-nodejs20"
LOGFILE="/var/log/docker-image-sync.log"
ALERT_LOG="/root/.openclaw/logs/docker-image-sync-alerts.log"
STATEFILE="/root/.openclaw/state/docker-image-sync.json"
EXPECTED_DIGEST_FILE="/root/.openclaw/state/docker-image-expected-digest"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")" "$(dirname "$STATEFILE")"

log "=== docker-image-sync start ==="

# Pull latest
log "Pulling $IMAGE..."
if ! docker pull "$IMAGE" >> "$LOGFILE" 2>&1; then
    alert "FAIL: docker pull $IMAGE failed"
    echo "status=fail" >> "$STATEFILE"
    exit 1
fi

# Verify SHA256 digest
ACTUAL_DIGEST=$(docker inspect "$IMAGE" --format='{{index .RepoDigests 0}}' 2>/dev/null | cut -d'@' -f2)
if [ -z "$ACTUAL_DIGEST" ]; then
    alert "FAIL: could not get digest for $IMAGE"
    echo "status=error" >> "$STATEFILE"
    exit 1
fi

log "Digest: $ACTUAL_DIGEST"

# First run — save expected digest
if [ ! -f "$EXPECTED_DIGEST_FILE" ]; then
    echo "$ACTUAL_DIGEST" > "$EXPECTED_DIGEST_FILE"
    log "First run — saved expected digest: $ACTUAL_DIGEST"
    echo "status=first_run" >> "$STATEFILE"
    exit 0
fi

EXPECTED_DIGEST=$(cat "$EXPECTED_DIGEST_FILE")
if [ "$ACTUAL_DIGEST" != "$EXPECTED_DIGEST" ]; then
    alert "DIGEST CHANGED: $EXPECTED_DIGEST → $ACTUAL_DIGEST"
    # Restart hermes if running to pick up new image
    if systemctl is-active --quiet hermes-asi-gateway; then
        log "Digest changed — restarting hermes-asi-gateway..."
        systemctl restart hermes-asi-gateway
        sleep 5
        if systemctl is-active --quiet hermes-asi-gateway; then
            log "OK: hermes-asi-gateway restarted successfully"
        else
            alert "FAIL: hermes-asi-gateway did not come back up"
        fi
    fi
    echo "$ACTUAL_DIGEST" > "$EXPECTED_DIGEST_FILE"
    echo "status=digest_changed_restarted" >> "$STATEFILE"
else
    log "Digest unchanged: $ACTUAL_DIGEST — no action needed"
    echo "status=ok" >> "$STATEFILE"
fi

# Prune dangling images
PRUNED=$(docker image prune -f 2>&1 | grep "Total reclaimed" || echo "0 bytes")
log "Pruned dangling images: $PRUNED"

log "=== docker-image-sync done ==="
echo ""
