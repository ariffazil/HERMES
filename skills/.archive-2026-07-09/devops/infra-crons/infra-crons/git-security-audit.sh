#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  git-security-audit — Check Hermes upstream for new commits  ║
# ║  Every 12 hours. Logs to /var/log/git-security-audit.log    ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

HERMES_DIR="/usr/local/lib/hermes-agent"
LOGFILE="/var/log/git-security-audit.log"
ALERT_LOG="/root/.openclaw/logs/git-security-audit-alerts.log"
STATEFILE="/root/.openclaw/state/git-security-audit.json"
OUTPUTFILE="/root/.hermes/cron/output/git-audit.md"
BRANCH="deploy/af-forge"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")" "$(dirname "$STATEFILE")" "$(dirname "$OUTPUTFILE")"

log "=== git-security-audit start ==="

cd "$HERMES_DIR" || exit 1

# Fetch latest
git fetch origin >> "$LOGFILE" 2>&1

# Count commits behind/ahead origin/main
MAIN_COMMITS=$(git log --oneline origin/main ^origin/main 2>/dev/null | wc -l)
DEPLOY_COMMITS=$(git log --oneline origin/main ^deploy/af-forge 2>/dev/null | wc -l)

log "origin/main ahead of deploy/af-forge: $MAIN_COMMITS commits"
log "deploy/af-forge ahead of origin/main: $DEPLOY_COMMITS commits"

if [ "$MAIN_COMMITS" -gt 0 ]; then
    # Get the actual commits
    COMMITS=$(git log --oneline origin/main ^deploy/af-forge 2>/dev/null | head -20)
    log "New upstream commits: $MAIN_COMMITS"
    echo "$COMMITS" >> "$LOGFILE"

    # Write output file
    cat > "$OUTPUTFILE" << EOF
# Git Security Patch Audit
Generated: $(date -Iseconds)
Branch: $BRANCH

Upstream commits not in $BRANCH: $MAIN_COMMITS

## Commits
$(git log --oneline origin/main ^deploy/af-forge 2>/dev/null | head -20)

## Recommendation
EOF

    if [ "$MAIN_COMMITS" -gt 10 ]; then
        alert "LARGE_GAP: $MAIN_COMMITS new upstream commits — Hermes should review"
        echo "recommendation=review_required" >> "$STATEFILE"
        echo "ALERT: $MAIN_COMMITS commits behind upstream — Hermes should review" >> "$OUTPUTFILE"
    else
        log "Small gap — no Hermes wake needed"
        echo "recommendation=minor_gap_monitor" >> "$STATEFILE"
        echo "recommendation=minor_gap_monitor" >> "$OUTPUTFILE"
    fi
else
    log "deploy/af-forge is up to date with origin/main"
    echo "status=up_to_date" >> "$STATEFILE"
    echo "up_to_date=true" > "$OUTPUTFILE"
fi

log "=== git-security-audit done ==="
echo ""
