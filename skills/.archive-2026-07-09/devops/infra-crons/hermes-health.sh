#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  hermes-health — Federation-wide health probe (machine task)     ║
# ║  Replaces Hermes cron job 'Hermes Health Probe' (deepseek/402)   ║
# ║  Pure shell, no LLM. Runs hourly. Logs to /var/log/hermes-health ║
# ╚══════════════════════════════════════════════════════════════════╝
set -uo pipefail

LOGFILE="/var/log/hermes-health.log"
ALERT_LOG="/root/.openclaw/logs/hermes-health-alerts.log"
STATEFILE="/root/.openclaw/state/hermes-health.json"
OUTPUTFILE="/root/.hermes/cron/output/hermes-health.md"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")" "$(dirname "$STATEFILE")" "$(dirname "$OUTPUTFILE")"

log "=== hermes-health start ==="

FAILED=0
> "$STATEFILE"

probe() {
    local name="$1"; local url="$2"; local method="${3:-GET}"; local timeout="${4:-5}"
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" -X "$method" "$url" 2>/dev/null || echo "000")
    if [ "$code" = "200" ] || [ "$code" = "204" ]; then
        log "OK: $name HTTP $code"
        printf '%s=ok\n' "$name" >> "$STATEFILE"
    else
        alert "FAIL: $name HTTP $code"
        printf '%s=fail_http_%s\n' "$name" "$code" >> "$STATEFILE"
        FAILED=$((FAILED + 1))
    fi
}

# Core federation organs
probe "arifos-mcp"    "http://localhost:8088/health"
probe "arifosd"       "http://localhost:18081/health"
probe "geox-mcp"      "http://localhost:8081/health"
probe "wealth"        "http://localhost:18082/health"
probe "well"          "http://localhost:18083/health"
probe "aforge"        "http://localhost:7071/health"
probe "aforge-mcp"    "http://localhost:7072/health"
probe "aaa-a2a"       "http://localhost:3001/health"
probe "openclaw"      "http://localhost:18789/health"
probe "ollama"        "http://localhost:11434/api/tags"

# Qdrant: probe root path (200 OK on empty path; 404 also means alive)
QD_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://localhost:6333/" 2>/dev/null || echo "000")
if [ "$QD_CODE" = "200" ] || [ "$QD_CODE" = "404" ]; then
    log "OK: qdrant HTTP $QD_CODE (alive)"
    printf 'qdrant=ok\n' >> "$STATEFILE"
else
    alert "FAIL: qdrant unreachable (HTTP $QD_CODE)"
    printf 'qdrant=fail_http_%s\n' "$QD_CODE" >> "$STATEFILE"
    FAILED=$((FAILED + 1))
fi

# Redis: TCP socket probe (binary protocol refuses HTTP). PING via raw RESP is overkill,
# a successful TCP connect proves the daemon is up. Use /dev/tcp which bash supports.
if (echo > /dev/tcp/127.0.0.1/6379) >/dev/null 2>&1; then
    log "OK: redis port 6379 accepting TCP"
    printf 'redis=ok\n' >> "$STATEFILE"
else
    alert "FAIL: redis port 6379 unreachable"
    printf 'redis=fail\n' >> "$STATEFILE"
    FAILED=$((FAILED + 1))
fi

# Postgres: probe via pg_isready
if command -v pg_isready > /dev/null 2>&1; then
    if pg_isready -h 127.0.0.1 -p 5432 -q; then
        log "OK: postgres"
        printf 'postgres=ok\n' >> "$STATEFILE"
    else
        alert "WARN: postgres not accepting"
        printf 'postgres=fail\n' >> "$STATEFILE"
        FAILED=$((FAILED + 1))
    fi
fi

# Disk usage sanity (root partition)
DISK_PCT=$(df / --output=pcent 2>/dev/null | tail -1 | tr -dc '0-9')
if [ -n "$DISK_PCT" ] && [ "$DISK_PCT" -lt 90 ]; then
    log "OK: disk ${DISK_PCT}%"
    printf 'disk=ok_pct_%s\n' "$DISK_PCT" >> "$STATEFILE"
else
    alert "WARN: disk ${DISK_PCT}%"
    printf 'disk=fail_pct_%s\n' "${DISK_PCT:-?}" >> "$STATEFILE"
    FAILED=$((FAILED + 1))
fi

# Vault writer alive?
if systemctl is-active --quiet vault999-writer; then
    printf 'vault999-writer=ok\n' >> "$STATEFILE"
    log "OK: vault999-writer"
else
    alert "FAIL: vault999-writer not active"
    printf 'vault999-writer=fail\n' >> "$STATEFILE"
    FAILED=$((FAILED + 1))
fi

# Write markdown report
cat > "$OUTPUTFILE" << EOF
# Hermes Health Probe
Generated: $(date -Iseconds)

| Service | Status |
|---------|--------|
$(grep '=ok' "$STATEFILE" | sed 's/=/ | OK |/; s/^/| /; s/$/ |/')
$(grep -v '=ok' "$STATEFILE" | grep -v '^$' | sed 's/=/ | FAIL |/; s/^/| /; s/$/ |/')

Failed: $FAILED
EOF

log "hermes-health: $FAILED failed"
log "=== hermes-health done ==="

if [ "$FAILED" -gt 0 ]; then
    printf 'status=fail\n' >> "$STATEFILE"
    exit 1
fi
printf 'status=ok\n' >> "$STATEFILE"
exit 0
