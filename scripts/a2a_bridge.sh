#!/bin/bash
# a2a_bridge.sh — Cross-Agent A2A Task Bridge v2.0
# Hermes/OpenClaw/OpenCode → AAA A2A Gateway → target agent
#
# Usage: ./a2a_bridge.sh hermes opencode "Deploy the fix" task
#        ./a2a_bridge.sh opencode hermes "Done." notify
#
# Forged: 2026-08-06 by 333-AGI — "the mesh must breathe"
# DITEMPA BUKAN DIBERI

set -euo pipefail

AAA_URL="${AAA_A2A_URL:-http://127.0.0.1:3001/tasks}"
SOURCE="${1:-hermes}"
TARGET="${2:-opencode}"
MESSAGE="${3:-ping}"
MODE="${4:-task}"

echo "A2A: ${SOURCE} → ${TARGET} | mode=${MODE}"

# ── Step 1: Get session binding ────────────────────────────────
BINDING=$(curl -sf -X POST http://127.0.0.1:8088/mcp \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"arif_init\",\"arguments\":{\"actor_id\":\"${SOURCE}\",\"intent\":\"A2A ${SOURCE}→${TARGET}\",\"mode\":\"light\"}}}" 2>/dev/null | \
    python3 -c "
import json,sys
try:
    d=json.loads(json.loads(sys.stdin.read())['result']['content'][0]['text'])
    print(d.get('session_token','NO_SCT'))
    print(d.get('session_id','') or d.get('result',{}).get('session_id','NO_SID'))
except:
    print('NO_SCT')
    print('NO_SID')
" 2>/dev/null)

SCT=$(echo "$BINDING" | head -1)
SESSION_ID=$(echo "$BINDING" | tail -1)

TASK_ID="${SOURCE}-$(date +%s%N)"
MSG_ID="${SOURCE}-msg-$(date +%s%N)"

# ── Step 2: Build payload ──────────────────────────────────────
SCT_PART=""
SID_PART=""
[ "$SCT" != "NO_SCT" ] && [ -n "$SCT" ] && SCT_PART=",\"sessionToken\":\"${SCT}\""
[ "$SESSION_ID" != "NO_SID" ] && [ -n "$SESSION_ID" ] && SID_PART=",\"session_id\":\"${SESSION_ID}\""

PAYLOAD=$(cat <<END
{
  "jsonrpc": "2.0",
  "id": "${TASK_ID}",
  "method": "tasks/send",
  "params": {
    "id": "${TASK_ID}"
    ${SID_PART},
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "${MESSAGE}"}],
      "messageId": "${MSG_ID}"
    },
    "metadata": {
      "targetAgent": "${TARGET}",
      "sourceAgent": "${SOURCE}",
      "source": "${SOURCE}-bridge",
      "notification": $([ "$MODE" = "notify" ] && echo "true" || echo "false")
      ${SCT_PART}
    }
  }
}
END
)

# ── Step 3: Dispatch ───────────────────────────────────────────
RESPONSE=$(curl -sf -X POST "${AAA_URL}" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -H 'A2A-Version: 1.0' \
    -d "${PAYLOAD}" 2>&1) || {
    echo "A2A: FALLBACK — queued to /root/forge_work/a2a_queue/"
    mkdir -p /root/forge_work/a2a_queue/
    echo "${PAYLOAD}" > "/root/forge_work/a2a_queue/${TASK_ID}.json"
    exit 0
}

echo "${RESPONSE}" | python3 -c "
import json,sys
d=json.load(sys.stdin)
res=d.get('result',{})
err=d.get('error',{})
if res:
    print(f'A2A: OK id={res.get(\"id\",\"?\")} status={res.get(\"status\",\"?\")}')
elif err:
    print(f'A2A: ERR {err.get(\"message\",\"?\")[:150]}')
else:
    print('A2A: UNKNOWN')
" 2>/dev/null || echo "A2A: PARSE_FAILED"

# ── Step 4: Flow ingest ────────────────────────────────────────
python3 /root/HERMES/scripts/arifflow_ingest.py \
    --actor "${SOURCE}" --session "a2a-${TASK_ID}" \
    --step_type "Route" --epistemic "Observation" \
    --floor_verdict "Pass" --quiet 2>/dev/null || true

echo "A2A: bridge closed | ${SOURCE}→${TARGET} | task=${TASK_ID}"
