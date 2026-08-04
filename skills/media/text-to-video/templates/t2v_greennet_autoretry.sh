#!/usr/bin/env bash
# Token Plan happyhorse-1.1-t2v with seat fallback + Green Net auto-retry.
# Pattern proven 2026-08-04. Edit P_PRIMARY / P_SOFT / OUT, then: bash thisfile.sh
set -e
source /root/.secrets/kunci-mas.env
BASE="https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1"
OUT="/tmp/output_v1.mp4"

P_PRIMARY='<full prompt — try this first>'
P_SOFT='<softened fallback — keep ALL cinematic staging (angle, lighting, setting, cast), swap only the risky framing (shirtless→tight singlet, seduction→friendly-respectful)>'

submit() {
  local PROMPT="$1"
  for K in QWEN_TEAM_OWNER_API_KEY QWEN_API_KEY QWEN_INDIVIDUAL_API_KEY; do
    AK="${!K}"
    [ -z "$AK" ] && continue
    RESP=$(curl -s -X POST "$BASE/services/aigc/video-generation/video-synthesis" \
      -H "X-DashScope-Async: enable" \
      -H "Authorization: Bearer $AK" \
      -H "Content-Type: application/json" \
      -d "$(jq -n --arg p "$PROMPT" '{model:"happyhorse-1.1-t2v",input:{prompt:$p},parameters:{resolution:"720P",ratio:"16:9",duration:5}}')")
    TASK_ID=$(echo "$RESP" | grep -o '"task_id":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ -n "$TASK_ID" ]; then echo "SUBMITTED with $K: $TASK_ID"; return 0; fi
    echo "$K rejected: $RESP"
  done
  return 1
}

# Sentinel returns: 0=SUCCEEDED (video downloaded) | 1=fatal/timeout | 2=GREEN NET (retryable)
poll() {
  for i in $(seq 1 40); do
    sleep 15
    SR=$(curl -s "$BASE/tasks/$TASK_ID" -H "Authorization: Bearer $AK")
    STATUS=$(echo "$SR" | grep -o '"task_status":"[^"]*"' | cut -d'"' -f4)
    echo "poll $i: $STATUS"
    if [ "$STATUS" = "SUCCEEDED" ]; then
      VIDEO_URL=$(echo "$SR" | grep -o '"video_url":"[^"]*"' | cut -d'"' -f4)
      curl -sL -o "$OUT" "$VIDEO_URL"
      echo "DOWNLOADED:"; ls -lh "$OUT"
      return 0
    elif [ "$STATUS" = "FAILED" ]; then
      if echo "$SR" | grep -q "DataInspectionFailed"; then
        echo "GREEN_NET_BLOCKED"; return 2
      fi
      echo "TASK_FAILED: $SR"; return 1
    fi
  done
  echo "TIMEOUT after 40 polls"; return 1
}

submit "$P_PRIMARY" || { echo "ALL KEYS FAILED"; exit 1; }
# poll returns non-zero sentinels on purpose — bracket under set +e so the
# retry branch below runs (bare call under set -e dies at the call line).
set +e
poll
RC=$?
set -e
if [ $RC -eq 2 ]; then
  echo "RETRY with softened prompt..."
  submit "$P_SOFT" || exit 1
  poll || exit 1
elif [ $RC -ne 0 ]; then
  exit 1
fi
