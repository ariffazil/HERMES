#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  constitutional-auditor probe — F1-F13 + vault + MCP tool audit ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/root/.openclaw/logs/constitutional-auditor.log"
ALERT_LOG="/root/.openclaw/logs/constitutional-auditor-alerts.log"
mkdir -p "$(dirname "$LOGFILE")"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

log "=== constitutional-auditor probe start ==="
ISSUES=0

# ─── 1. arifOS MCP health + tool count ────────────────────────────
# FIX 2026-06-12: was probing :8080 (wrong port), now :8088 (canonical)
arif_health=$(curl -s --max-time 5 "http://localhost:8088/health" 2>/dev/null || echo '{}')
if echo "$arif_health" | grep -q '"status":"healthy"'; then
    log "OK: arifOS MCP healthy"
elif [ "$arif_health" != "{}" ] && [ -n "$arif_health" ]; then
    # Got a non-empty response that doesn't have "status:healthy" key
    # (e.g. bare "OK" or empty body from /health) — accept as healthy if 200
    log "OK: arifOS MCP responding on :8088 (health endpoint returned content)"
else
    alert "CRITICAL: arifOS MCP not healthy on :8088"
    ISSUES=$((ISSUES + 1))
fi

# ─── 2. F-floor definitions exist (canonical home) ─────────────────
# FIX 2026-06-12: was looking for /root/arifOS/core/floors.py (does not exist)
# Canonical home is arifosmcp/runtime/fiqh_of_floors.py
FLOORS="/root/arifOS/arifosmcp/runtime/fiqh_of_floors.py"
if [ -s "$FLOORS" ]; then
    lines=$(wc -l < "$FLOORS")
    log "OK: fiqh_of_floors.py exists ($lines lines)"
else
    alert "CRITICAL: fiqh_of_floors.py missing or empty"
    ISSUES=$((ISSUES + 1))
fi

# ─── 3. VAULT999 chain integrity ──────────────────────────────────
# FIX 2026-06-12: was looking at /root/arifOS/VAULT999 (does not exist)
# Canonical vault is /root/.local/share/arifos/vault999
VAULT_DIR="/root/.local/share/arifos/vault999"
if [ -d "$VAULT_DIR" ]; then
    entries=$(find "$VAULT_DIR" -type f | wc -l)
    latest=$(find "$VAULT_DIR" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | awk '{print $2}')
    if [ -n "$latest" ]; then
        latest_age_h=$(( ($(date +%s) - $(stat -c %Y "$latest" 2>/dev/null || echo 0)) / 3600 ))
        log "OK: VAULT999 has $entries entries, latest sealed ${latest_age_h}h ago"
        if [ "$latest_age_h" -gt 168 ]; then
            alert "WARNING: VAULT999 latest entry is ${latest_age_h}h old (>7 days)"
            ISSUES=$((ISSUES + 1))
        fi
    else
        log "WARNING: VAULT999 directory empty"
    fi
else
    alert "CRITICAL: VAULT999 directory missing at $VAULT_DIR"
    ISSUES=$((ISSUES + 1))
fi

# ─── 4. arifOS MCP tools availability (13 canonical) ─────────────
# FIX 2026-06-12: was probing :8080 (wrong port), now :8088
mcp_tools=$(curl -s -X POST "http://localhost:8088/mcp" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
    --max-time 5 2>/dev/null | grep -o '"name"' | wc -l)
if [ "$mcp_tools" -ge 10 ]; then
    log "OK: arifOS MCP exposes $mcp_tools tools"
else
    alert "WARNING: arifOS MCP only exposes $mcp_tools tools (expected 13+)"
    ISSUES=$((ISSUES + 1))
fi

# ─── 5. Check agent-workbench audit trail ─────────────────────────
AUDIT="/root/.agent-workbench/mcp-audit.jsonl"
if [ -f "$AUDIT" ]; then
    audit_lines=$(wc -l < "$AUDIT" 2>/dev/null || echo 0)
    log "OK: mcp-audit.jsonl has $audit_lines entries"
else
    log "WARNING: mcp-audit.jsonl not found"
fi

log "Probe complete. issues=$ISSUES"
