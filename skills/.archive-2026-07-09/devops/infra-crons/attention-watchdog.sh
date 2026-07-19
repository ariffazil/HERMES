#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  attention-watchdog — Silent Hermes session monitor         ║
# ║  Every 30 min. Wakes Hermes only on threshold breach.    ║
# ║  Logs to /var/log/attention-watchdog.log                  ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/var/log/attention-watchdog.log"
STATEFILE="/root/.openclaw/state/attention-watchdog.json"
OUTPUTFILE="/root/.hermes/cron/output/attention-watchdog.md"
REDIS_KEY="federation:hermes:session_telemetry"
BREACH_LOG="/root/.openclaw/logs/attention-breaches.log"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$STATEFILE")"

log "=== attention-watchdog start ==="

# Read telemetry from Redis
if command -v redis-cli &>/dev/null && redis-cli ping > /dev/null 2>&1; then
    data=$(redis-cli get "$REDIS_KEY" 2>/dev/null)
    if [ -n "$data" ] && [ "$data" != "ERR" ]; then
        active_sessions=$(echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('active_sessions', 0))" 2>/dev/null || echo "0")
        error_rate=$(echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error_rate_24h', 0))" 2>/dev/null || echo "0")
        tool_calls=$(echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_calls_24h', 0))" 2>/dev/null || echo "0")
        log "Sessions: $active_sessions, Error rate: $error_rate, Tool calls 24h: $tool_calls"
    else
        log "No telemetry in Redis — skipping"
        exit 0
    fi
else
    log "Redis unavailable — skipping"
    exit 0
fi

# Check thresholds
ERROR_THRESHOLD=0.05    # 5%
SESSION_THRESHOLD=50    # 50 concurrent sessions

breached=0
report=""

if (( $(echo "$error_rate > $ERROR_THRESHOLD" | python3 -c "print(1 if float(input()) > float('$ERROR_THRESHOLD'))" 2>/dev/null || echo "0") )); then
    log "BREACH: error_rate $error_rate > $ERROR_THRESHOLD"
    report="${report}error_rate=${error_rate} "
    breached=$((breached + 1))
fi

if [ "$active_sessions" -gt "$SESSION_THRESHOLD" ] 2>/dev/null; then
    log "BREACH: active_sessions $active_sessions > $SESSION_THRESHOLD"
    report="${report}active_sessions=${active_sessions} "
    breached=$((breached + 1))
fi

if [ "$breached" -gt 0 ]; then
    # Log breach
    echo "[$(TS)] BREACH: $report" >> "$BREACH_LOG"
    # Write output for Hermes to pick up
    cat > "$OUTPUTFILE" << EOF
# Attention Watchdog Breach
$(date -Iseconds)

Active sessions: $active_sessions (threshold: $SESSION_THRESHOLD)
Error rate: $error_rate (threshold: $ERROR_THRESHOLD)
Tool calls 24h: $tool_calls

Breach count: $breached
Condition: $report

WAKING HERMES for interpretation.
EOF
    log "Threshold breached — Hermes will be notified via cron wake"
else
    log "All metrics normal — no action needed"
    echo "status=ok" > "$STATEFILE"
fi

log "=== attention-watchdog done ==="
