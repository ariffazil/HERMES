#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  model-fallback-monitor probe — Model chain health + billing    ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/root/.openclaw/logs/model-fallback-monitor.log"
ALERT_LOG="/root/.openclaw/logs/model-fallback-monitor-alerts.log"
mkdir -p "$(dirname "$LOGFILE")"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

ISSUES=0
log "=== model-fallback-monitor probe start ==="

# ─── 1. MiniMax (primary) ─────────────────────────────────────────
mm_start=$(date +%s%N)
mm_resp=$(curl -s -X POST https://api.minimaxi.chat/v1/text/chatcompletion_v2 \
  -H "Authorization: Bearer sk-cp-5_ouSBpUY5oVq2BuokHSQe1-5vsesbHPmIlB3IU1FbwHpfBDaphSgJxchFgiU7qzbnr--4WNgtYMrsqHHr85qWlzIc9essD6Ch9cjhgiog_E8DTC2eJUgO4" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.7-highspeed","messages":[{"role":"user","content":"ping"}],"max_tokens":5}' \
  --max-time 15 2>/dev/null || true)
mm_ms=$(( ($(date +%s%N) - mm_start) / 1000000 ))
if echo "$mm_resp" | grep -q '"choices"'; then
    log "OK: MiniMax primary responds (${mm_ms}ms)"
else
    err=$(echo "$mm_resp" | grep -o '"message":"[^"]*"' | head -1 || echo "unknown")
    alert "CRITICAL: MiniMax primary DOWN (${mm_ms}ms) — $err"
    ISSUES=$((ISSUES + 1))
fi

# ─── 2. DeepSeek (hot-swap, expect 402) ──────────────────────────
ds_start=$(date +%s%N)
ds_resp=$(curl -s -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY:-}" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"ping"}],"max_tokens":5}' \
  --max-time 15 2>/dev/null || true)
ds_ms=$(( ($(date +%s%N) - ds_start) / 1000000 ))
if echo "$ds_resp" | grep -q '"Insufficient Balance"'; then
    log "WARN: DeepSeek 402 Insufficient Balance (${ds_ms}ms) — still dead"
    ISSUES=$((ISSUES + 1))
elif echo "$ds_resp" | grep -q '"choices"'; then
    log "OK: DeepSeek RECOVERED (${ds_ms}ms) — re-add to fallbacks!"
else
    alert "WARNING: DeepSeek unexpected response (${ds_ms}ms)"
    ISSUES=$((ISSUES + 1))
fi

# ─── 3. Ollama local (cold-start check) ───────────────────────────
# DISABLED: Ollama is now purely an embedding backbone (bge-m3). Generation fallback is deprecated.

# ─── 4. Ollama inference test ─────────────────────────────────────
# DISABLED: Generation fallback is deprecated.

# ─── 5. Kimi (moonshot) — light ping ──────────────────────────────
km_resp=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer ${KIMI_API_KEY:-}" \
  --max-time 10 "https://api.moonshot.cn/v1/models" 2>/dev/null || echo "000")
if [ "$km_resp" = "200" ]; then
    log "OK: Kimi (Moonshot) API reachable"
else
    log "WARNING: Kimi API HTTP $km_resp"
fi

log "Probe complete. issues=$ISSUES"
