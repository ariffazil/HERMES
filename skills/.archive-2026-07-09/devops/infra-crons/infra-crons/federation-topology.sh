#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  federation-topology — Ping all federation organs              ║
# ║  Every 24 hours. Logs to /var/log/federation-topology.log  ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/var/log/federation-topology.log"
ALERT_LOG="/root/.openclaw/logs/federation-topology-alerts.log"
STATEFILE="/root/.openclaw/state/federation-topology.json"
OUTPUTFILE="/root/.hermes/cron/output/federation-topology.md"
REDIS_KEY="federation:topology:status"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")" "$(dirname "$STATEFILE")"

log "=== federation-topology start ==="

> "$STATEFILE"
ALIVE=0
DEAD=0

# hermes-a2a (port 18001)
check_http() {
    local url=$1
    curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000"
}

# arifOS MCP
code=$(check_http "http://localhost:8088/health")
if [ "$code" = "200" ]; then
    log "OK: arifOS MCP (:8088) → HTTP $code"
    echo "arifOS MCP=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: arifOS MCP (:8088) → HTTP $code"
    echo "arifOS MCP=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# arifosd
code=$(check_http "http://localhost:18081/health")
if [ "$code" = "200" ]; then
    log "OK: arifosd (:18081) → HTTP $code"
    echo "arifosd=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: arifosd (:18081) → HTTP $code"
    echo "arifosd=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# WEALTH
code=$(check_http "http://localhost:18082/health")
if [ "$code" = "200" ]; then
    log "OK: WEALTH (:18082) → HTTP $code"
    echo "WEALTH=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: WEALTH (:18082) → HTTP $code"
    echo "WEALTH=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# WELL
code=$(check_http "http://localhost:18083/health")
if [ "$code" = "200" ]; then
    log "OK: WELL (:18083) → HTTP $code"
    echo "WELL=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: WELL (:18083) → HTTP $code"
    echo "WELL=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# OpenClaw Gateway
code=$(check_http "http://localhost:18789/health")
if [ "$code" = "200" ]; then
    log "OK: OpenClaw GW (:18789) → HTTP $code"
    echo "OpenClaw GW=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: OpenClaw GW (:18789) → HTTP $code"
    echo "OpenClaw GW=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# Hermes A2A bridge (port 18001)
code=$(check_http "http://localhost:18001/.well-known/agent-card.json")
if [ "$code" = "200" ]; then
    log "OK: Hermes A2A (:18001) → HTTP $code"
    echo "hermes-a2a=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: Hermes A2A (:18001) → HTTP $code"
    echo "hermes-a2a=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# Ollama (no /health — use /api/tags)
code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:11434/api/tags" 2>/dev/null || echo "000")
if [ "$code" = "200" ]; then
    log "OK: Ollama (:11434 /api/tags) → HTTP $code"
    echo "Ollama=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    alert "DOWN: Ollama (:11434) → HTTP $code"
    echo "Ollama=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
fi

# APEX (port 3002 — Express app)
code=$(check_http "http://localhost:3002/health")
if [ "$code" = "200" ]; then
    log "OK: APEX (:3002) → HTTP $code"
    echo "APEX=200" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
else
    # APEX may not have /health — try root
    code2=$(check_http "http://localhost:3002/")
    if [ "$code2" = "200" ] || [ "$code2" = "404" ]; then
        log "OK: APEX (:3002) → HTTP $code2 (alive but no /health)"
        echo "APEX=$code2" >> "$STATEFILE"; ALIVE=$((ALIVE+1))
    else
        alert "DOWN: APEX (:3002) → HTTP $code"
        echo "APEX=DOWN" >> "$STATEFILE"; DEAD=$((DEAD+1))
    fi
fi

# Write Redis key if available
if command -v redis-cli &>/dev/null && redis-cli ping > /dev/null 2>&1; then
    JSON=$(python3 -c "
import json, time
state = {}
with open('$STATEFILE') as f:
    for line in f:
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            state[k] = v
state['timestamp'] = time.time()
state['alive'] = $ALIVE
state['dead'] = $DEAD
print(json.dumps(state))
" 2>/dev/null || echo "{}")
    redis-cli set "$REDIS_KEY" "$JSON" ex=172800 >> "$LOGFILE" 2>&1
    log "Written to Redis: $REDIS_KEY"
fi

# Write report
cat > "$OUTPUTFILE" << EOF
# Federation Topology
Generated: $(date -Iseconds)

| Organ | Status |
|-------|--------|
$(while IFS='=' read -r k v; do echo "| $k | $v |"; done < "$STATEFILE")

Alive: $ALIVE | Dead: $DEAD
EOF

log "Topology: $ALIVE alive, $DEAD down"
log "=== federation-topology done ==="
echo ""
