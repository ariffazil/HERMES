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

## Usage (async task pattern)

```bash
#!/bin/bash
set -e
TASK_RESPONSE=$(curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
  -H "X-DashScope-Async: enable" \
  -H "Authorization: Bearer ${QWEN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "happyhorse-1.1-t2v",
    "input": {"prompt": "<prompt>"},
    "parameters": {"resolution": "720P", "ratio": "16:9", "duration": 5}
  }')
TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"task_id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -z "$TASK_ID" ]; then echo "Submission failed: $TASK_RESPONSE"; exit 1; fi
echo "Task submitted: $TASK_ID"
while true; do
  sleep 15
  STATUS_RESPONSE=$(curl -s "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer ${QWEN_API_KEY}")
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
  echo "Generating..."
done
```

## Parameters

- **resolution**: 480P, 720P, 1080P
- **ratio**: 16:9, 9:16, 1:1
- **duration**: 3-10 seconds (default 5)

## ⚠️ Credits Warning

Video generation consumes significantly more Credits than text. A single call can use a large portion of your 5-hour or 7-day quota. Start with short duration + low resolution.

## Notes

- Billed in Credits from Token Plan quota
- Async — task typically completes in 1-3 minutes
- Credits settle after task completes, not at submission
- Multiple concurrent tasks settle together — may trigger quota limit
