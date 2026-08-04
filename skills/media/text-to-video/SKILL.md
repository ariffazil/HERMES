---
name: token-plan-video
description: "Generate videos via QwenCloud Token Plan. Activates when user asks to create videos, animations, or moving visual content."
---

# Token Plan Video Generation

Call the Token Plan video API to generate videos from text or images.

## Supported models

| Model | Function |
|-------|----------|
| `happyhorse-1.1-t2v` | Text-to-video |
| `happyhorse-1.1-i2v` | Image-to-video (first frame) |
| `happyhorse-1.1-r2v` | Reference-to-video |

## ⚠️ Multi-seat quota fallback (important)

Token Plan quota is **per seat/key**, not global. If one key is exhausted, the same endpoint works with another seat's key. Error signature:

```json
{"code":"Throttling.AllocationQuota","message":"Your token-plan quota has been exhausted."}
```

On that error, fall through the seat ladder (same URL, swap the Bearer):

1. `QWEN_TEAM_OWNER_API_KEY` (Token Plan lane — matches Pitfalls below)
2. `QWEN_API_KEY`
3. `QWEN_INDIVIDUAL_API_KEY`

Source keys from `/root/.secrets/kunci-mas.env` (`source` it first). The key that returned a `task_id` is the one to use for polling too — keep it consistent across submit + poll.

**Routing:** call the Token Plan endpoint **directly with curl** (pattern below). Do not route Token Plan video through the `mmx` CLI — its video route map goes through older providers and returns HTTP 404 when stale. Direct curl is the reliable path; only reconsider mmx if it's verified working for this endpoint.

## Usage (async task pattern)

Set `QWEN_VIDEO_KEY` to whichever seat has quota (see fallback ladder above).

```bash
#!/bin/bash
set -e
QWEN_VIDEO_KEY="${QWEN_VIDEO_KEY:-$QWEN_API_KEY}"
TASK_RESPONSE=$(curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
  -H "X-DashScope-Async: enable" \
  -H "Authorization: Bearer ${QWEN_VIDEO_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "happyhorse-1.1-t2v",
    "input": {"prompt": "<prompt>"},
    "parameters": {"resolution": "720P", "ratio": "16:9", "duration": 5}
  }')
TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"task_id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -z "$TASK_ID" ]; then echo "Submission failed: $TASK_RESPONSE"; exit 1; fi
echo "Task submitted: $TASK_ID"
# Bounded polling: 30 x 15s = 7.5 min cap. Never use `while true` — a task
# stuck in PENDING would hang the loop forever.
for i in $(seq 1 30); do
  sleep 15
  STATUS_RESPONSE=$(curl -s "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer ${QWEN_VIDEO_KEY}")
  STATUS=$(echo "$STATUS_RESPONSE" | grep -o '"task_status":"[^"]*"' | cut -d'"' -f4)
  if [ "$STATUS" = "SUCCEEDED" ]; then
    VIDEO_URL=$(echo "$STATUS_RESPONSE" | grep -o '"video_url":"[^"]*"' | cut -d'"' -f4)
    OUTPUT="generated_$(date +%Y%m%d_%H%M%S).mp4"
    curl -s -o "$OUTPUT" "$VIDEO_URL"
    echo "Video: $(pwd)/$OUTPUT"
    exit 0
  elif [ "$STATUS" = "FAILED" ]; then
    echo "Failed: $STATUS_RESPONSE"; exit 1
  fi
  echo "Generating... ($STATUS)"
done
echo "TIMEOUT: task $TASK_ID still $STATUS after 30 polls — re-check manually"
exit 1
```

Build the JSON payload with `python3 -c 'import json; ...'` when the prompt comes from a file or contains quotes — never hand-interpolate prompts into JSON.

## Parameters

- **resolution**: 480P, 720P, 1080P
- **ratio**: 16:9, 9:16, 1:1
- **duration**: 3-10 seconds (default 5)

## Content moderation (Green Net)

Aliyun runs a strict provider-side input filter ("Green Net"). A rejected task submits fine but fails fast on the first poll (~15s) with:

    "code": "DataInspectionFailed",
    "message": "Green net check failed for text (input): Input data may contain inappropriate content."

This is Aliyun policy, not a key/Hermes problem — resubmitting unchanged fails again, and F13 overrides do not reach provider-side filters. Fix pattern (verified 2026-08-04): soften the prompt and retry — replace shirtless/explicit-body framing with clothed-but-fit (e.g., tight singlet), replace flirt/seduction beats (wink, blush, "pickup") with friendly-respectful interaction (smile, nod). Keep all cinematic staging (low angle, rim lighting, setting, supporting cast). One retry usually passes; if it fails twice, drop the romantic framing entirely.

**Automate the retry in the job script.** Instead of manual resubmission, encode it: `submit()` walks the seat ladder, `poll()` returns sentinel codes (0=SUCCEEDED+downloaded, 1=fatal/timeout, 2=`DataInspectionFailed`), and the main flow resubmits with a pre-written softened prompt when RC=2. Critical detail: the poll call MUST be bracketed (`set +e` / `RC=$?` / `set -e`) — under `set -e`, a bare call returning 2 kills the script before the retry branch runs. Full proven pattern: `templates/t2v_greennet_autoretry.sh` (seat-ladder submit + sentinel poll + auto-retry; also uses `jq -n --arg` for safe JSON building).

## Pitfalls

- **Key resolution**: kunci-mas holds many Qwen keys (QWEN_API_KEY, QWEN_TEAM_OWNER_API_KEY, QWEN_HERMES_API_KEY, QWEN_INDIVIDUAL_API_KEY, ...). Token Plan lane = `QWEN_TEAM_OWNER_API_KEY` first, fall back to `QWEN_API_KEY`.
- **Redaction corruption**: scripts written via heredoc/inline python that spell out secret var names in certain contexts get corrupted (`***` injected → SyntaxError). Use the bash + `source kunci-mas.env` pattern in this skill instead; if a written file shows `***` corruption, rewrite it as a `.sh`.

## ⚠️ Credits Warning

Video generation consumes significantly more Credits than text. A single call can use a large portion of your 5-hour or 7-day quota. Start with short duration + low resolution.

## Notes

- Billed in Credits from Token Plan quota
- Async — task typically completes in 1-3 minutes
- Credits settle after task completes, not at submission
- Multiple concurrent tasks settle together — may trigger quota limit
