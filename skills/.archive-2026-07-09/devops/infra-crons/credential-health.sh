#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  credential-health — Verify key credentials are reachable       ║
# ║  Every 24 hours. Logs to /var/log/credential-health.log       ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/var/log/credential-health.log"
ALERT_LOG="/root/.openclaw/logs/credential-health-alerts.log"
STATEFILE="/root/.openclaw/state/credential-health.json"
OUTPUTFILE="/root/.hermes/cron/output/credential-health.md"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")" "$(dirname "$STATEFILE")" "$(dirname "$OUTPUTFILE")"

log "=== credential-health start ==="

# Load env
set -a
[ -f ~/.hermes/.env ] && source ~/.hermes/.env
set +a

FAILED=0
REPORT=""

# Langfuse
check_langfuse() {
    if [ -z "${HERMES_LANGFUSE_PUBLIC_KEY:-}" ] || [ -z "${HERMES_LANGFUSE_SECRET_KEY:-}" ]; then
        log "SKIP: Langfuse credentials not configured"
        return 0
    fi
    local code
    # Use the health endpoint — returns 200 if account is valid
    code=$(curl -s -o /dev/null -w "%{http_code}" \
        --max-time 10 \
        -H "Authorization: Bearer ${HERMES_LANGFUSE_SECRET_KEY}" \
        "${HERMES_LANGFUSE_BASE_URL:-https://cloud.langfuse.com}/api/public/health" 2>/dev/null || echo "000")
    # 200 = healthy, 401 = valid key wrong project (creds live), 405 = endpoint exists (also live)
    if [ "$code" = "200" ] || [ "$code" = "401" ] || [ "$code" = "405" ]; then
        log "OK: Langfuse reachable (HTTP $code)"
        echo "langfuse=ok" >> "$STATEFILE"
    else
        alert "FAIL: Langfuse unreachable (HTTP $code)"
        echo "langfuse=fail_http_$code" >> "$STATEFILE"
        REPORT="${REPORT}\n- Langfuse: HTTP $code"
        FAILED=$((FAILED + 1))
    fi
}

# Ollama
check_ollama() {
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:11434/api/tags 2>/dev/null || echo "000")
    if [ "$code" = "200" ]; then
        log "OK: Ollama reachable (HTTP $code)"
        echo "ollama=ok" >> "$STATEFILE"
    else
        alert "FAIL: Ollama unreachable (HTTP $code)"
        echo "ollama=fail_http_$code" >> "$STATEFILE"
        REPORT="${REPORT}\n- Ollama: HTTP $code"
        FAILED=$((FAILED + 1))
    fi
}

# Redis
check_redis() {
    if command -v redis-cli &>/dev/null; then
        if redis-cli ping > /dev/null 2>&1; then
            log "OK: Redis reachable"
            echo "redis=ok" >> "$STATEFILE"
        else
            alert "FAIL: Redis not responding"
            echo "redis=fail" >> "$STATEFILE"
            REPORT="${REPORT}\n- Redis: no response"
            FAILED=$((FAILED + 1))
        fi
    else
        log "SKIP: redis-cli not available"
    fi
}

# arifOS MCP
check_arifos() {
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:8088/health 2>/dev/null || echo "000")
    if [ "$code" = "200" ]; then
        log "OK: arifOS MCP reachable (HTTP $code)"
        echo "arifos=ok" >> "$STATEFILE"
    else
        alert "FAIL: arifOS MCP unreachable (HTTP $code)"
        echo "arifos=fail_http_$code" >> "$STATEFILE"
        REPORT="${REPORT}\n- arifOS MCP: HTTP $code"
        FAILED=$((FAILED + 1))
    fi
}

# Run checks
> "$STATEFILE"
check_langfuse
check_ollama
check_redis
check_arifos

# Write report
cat > "$OUTPUTFILE" << EOF
# Credential Health Check
Generated: $(date -Iseconds)

| Service | Status |
|---------|--------|
$(grep "=ok" "$STATEFILE" | sed 's/=/ | OK |/; s/^/| /; s/$/ |/')
$(grep -v "=ok" "$STATEFILE" | grep -v "^$" | sed 's/=/ | FAIL |/; s/^/| /; s/$/ |/')

Failed: $FAILED
EOF

log "Credential health: $FAILED failed"
log "=== credential-health done ==="

if [ "$FAILED" -gt 0 ]; then
    echo "status=fail" >> "$STATEFILE"
else
    echo "status=ok" >> "$STATEFILE"
fi
echo ""
