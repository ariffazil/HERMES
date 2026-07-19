#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  constitutional-floor-watch — Scan for F1-F13 violations    ║
# ║  Every 6 hours. Wakes Hermes only on anomaly detected.      ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/var/log/constitutional-floor-watch.log"
ALERT_LOG="/root/.openclaw/logs/constitutional-alerts.log"
OUTPUTFILE="/root/.hermes/cron/output/constitutional-floor-watch.md"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")"

log "=== constitutional-floor-watch start ==="

anomalies=0

# Check for unauthorized VAULT999 writes (any non-root process writing to vault)
if [ -d "/root/arifOS/VAULT999" ]; then
    recent_writes=$(find /root/arifOS/VAULT999 -mmin -360 -name "*.jsonl" 2>/dev/null | head -5)
    if [ -n "$recent_writes" ]; then
        log "Recent VAULT999 activity detected (last 6h): $(echo "$recent_writes" | wc -l) files"
    fi
fi

# Check for 888_HOLD attempts by non-APEX agents
# Look at recent hermes logs for hold-related activity
if [ -f "/root/.openclaw/logs/mcp-lifeguard-alerts.log" ]; then
    holds=$(grep -c "888_HOLD\|HOLD\|irreversible" /root/.openclaw/logs/mcp-lifeguard-alerts.log 2>/dev/null || echo "0")
    if [ "$holds" -gt 0 ]; then
        log "Found $holds HOLD-related entries in probe log"
    fi
fi

# Check for VAULT999 seal events in recent logs
if [ -f "/var/log/vault999.log" ]; then
    recent_seals=$(tail -100 /var/log/vault999.log 2>/dev/null | grep -c "seal\|SEAL" || echo "0")
    log "Recent vault seals in log: $recent_seals"
fi

# If anomaly detected → write for Hermes interpretation
if [ "$anomalies" -gt 0 ]; then
    alert "Constitutional anomaly detected — waking Hermes"
    cat > "$OUTPUTFILE" << EOF
# Constitutional Floor Watch — Anomaly Detected
$(date -Iseconds)

Anomalies: $anomalies

Details:
- VAULT999 recent writes: check manually
- HOLD attempts: $holds
- Recent seals: $recent_seals

WAKING HERMES for constitutional interpretation.
EOF
else
    log "No constitutional anomalies detected"
fi

log "=== constitutional-floor-watch done ==="
