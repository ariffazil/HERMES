#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  vault999-reader probe — Bridge to arifOS MCP vault tools       ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/root/.openclaw/logs/vault999-reader.log"
ALERT_LOG="/root/.openclaw/logs/vault999-reader-alerts.log"
mkdir -p "$(dirname "$LOGFILE")"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

ISSUES=0
log "=== vault999-reader probe start ==="

VAULT_DIR="/root/arifOS/VAULT999"
VAULT_FILES="/root/.agent-workbench/vault999.jsonl"

if [ -d "$VAULT_DIR" ]; then
    count=$(find "$VAULT_DIR" -type f | wc -l)
    log "OK: VAULT999 dir has $count entries"
else
    alert "CRITICAL: VAULT999 directory missing at $VAULT_DIR"
    ISSUES=$((ISSUES + 1))
fi

if [ -f "$VAULT_FILES" ]; then
    lines=$(wc -l < "$VAULT_FILES" 2>/dev/null | tr -d ' ' || echo 0)
    log "OK: vault999.jsonl has $lines lines"
    if [ "$lines" -gt 0 ]; then
        bad_lines=$(grep -v '^[[:space:]]*{' "$VAULT_FILES" 2>/dev/null | wc -l | tr -d ' ' || true)
        if [ "$bad_lines" -eq 0 ]; then
            log "OK: All vault entries are valid JSON objects"
        else
            alert "WARNING: $bad_lines vault entries are not valid JSON"
            ISSUES=$((ISSUES + 1))
        fi
    fi
else
    log "INFO: vault999.jsonl not found at $VAULT_FILES"
fi

judge_resp=$(curl -s -X POST "http://localhost:8088/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
    --max-time 5 2>/dev/null || true)
if echo "$judge_resp" | grep -q 'arif_judge_deliberate'; then
    log "OK: arif_judge_deliberate tool available"
else
    alert "WARNING: arif_judge_deliberate not in tool list"
    ISSUES=$((ISSUES + 1))
fi

if echo "$judge_resp" | grep -q 'arif_vault_seal'; then
    log "OK: arif_vault_seal tool available"
else
    alert "WARNING: arif_vault_seal not in tool list"
    ISSUES=$((ISSUES + 1))
fi

log "Probe complete. issues=$ISSUES"
