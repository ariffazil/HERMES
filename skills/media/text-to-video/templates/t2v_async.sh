#!/bin/bash
# Token Plan t2v — proven async pattern (verified 2026-08-04).
# Usage: PROMPT='your prompt' bash t2v_async.sh
# Knobs: MODEL, RES (480P|720P|1080P), RATIO, DUR (3-10), OUTDIR
set -e
source /root/.secrets/kunci-mas.env
AK="${QWEN_TEAM_OWNER_API_KEY:-$QWEN_API_KEY}"
[ -z "$AK" ] && { echo "NO KEY"; exit 1; }

BASE="https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1"
MODEL="${MODEL:-happyhorse-1.1-t2v}"
RES="${RES:-720P}"; RATIO="${RATIO:-16:9}"; DUR="${DUR:-5}"
OUTDIR="${OUTDIR:-/root/generated}"
: "${PROMPT:?Set PROMPT env var or edit this line}"

TASK_RESPONSE=$(curl -s -X POST "$BASE/services/aigc/video-generation/video-synthesis" \
  -H "X-DashScope-Async: enable" \
  -H "Authorization: Bearer $AK" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg p "$PROMPT" --arg m "$MODEL" --arg r "$RES" --arg rt "$RATIO" --argjson d "$DUR" \
        '{model:$m, input:{prompt:$p}, parameters:{resolution:$r, ratio:$rt, duration:$d}}')")
echo "SUBMIT: $TASK_RESPONSE"
TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"task_id":"[^"]*"' | head -1 | cut -d'"' -f4)
[ -z "$TASK_ID" ] && { echo "Submission failed"; exit 1; }

for i in $(seq 1 40); do
  sleep 15
  SR=$(curl -s "$BASE/tasks/$TASK_ID" -H "Authorization: Bearer $AK")
  STATUS=$(echo "$SR" | grep -o '"task_status":"[^"]*"' | cut -d'"' -f4)
  echo "poll $i: $STATUS"
  case "$STATUS" in
    SUCCEEDED)
      VIDEO_URL=$(echo "$SR" | grep -o '"video_url":"[^"]*"' | cut -d'"' -f4)
      mkdir -p "$OUTDIR"
      OUTPUT="$OUTDIR/t2v_$(date +%Y%m%d_%H%M%S).mp4"
      curl -s -o "$OUTPUT" "$VIDEO_URL"
      echo "DONE: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
      exit 0 ;;
    FAILED|UNKNOWN)
      # code=DataInspectionFailed -> Green Net filter; soften prompt and rerun (see SKILL.md)
      echo "Failed: $SR"; exit 1 ;;
  esac
done
echo "TIMEOUT"; exit 1
