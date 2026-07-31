# Direct MiniMax Vision Fallback — Worked Example

## ⚠️ SUPERSEDED (2026-07-30)

This is a HISTORICAL reference. The working vision config is now **Qwen-VL via OpenRouter**
(see `references/openrouter-qwen-vl-config.md`). MiniMax-M3 was replaced because its
`MINIMAX_BASE_URL` env var carried sops ciphertext → `urlparse` crash. The OpenRouter path
uses `OPENROUTER_API_KEY` which was correctly stored as raw key.

Keep this file only if you need to debug the MiniMax path for some reason. Otherwise
always prefer the OpenRouter path.

## Context

Date: 2026-07-30
Primary model: DeepSeek V4 Flash (text-only, no native vision)
Trigger: User sent image via Telegram, `vision_analyze()` failed with:
```
Error code: 400 - {'error': {'message': 'unknown variant `image_url`, expected `text`'}}
```

Root cause: DeepSeek V4 Flash API does not accept `image_url` content parts. The `vision_analyze` tool tries to attach the image to the primary model's API call as an `image_url` block, but the model rejects it.

## Solution

Call MiniMax M3 directly using `execute_code` (Python `requests`). The MiniMax API is OpenAI-compatible and accepts standard `image_url` content parts.

## Step-by-step

### 1. Check env vars
```bash
source /root/.secrets/kunci-mas.env
echo "MINIMAX_API_KEY set: $([ -n \"$MINIMAX_API_KEY\" ] && echo 'YES' || echo 'NO')"
echo "MINIMAX_BASE_URL: ${MINIMAX_BASE_URL:-(not set)}"
```
Expected: `MINIMAX_API_KEY set: YES`, `MINIMAX_BASE_URL: https://api.minimax.io`

### 2. Write Python script in execute_code
```python
import base64, subprocess, requests

# Read image
with open('/path/to/image.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

# Source env vars from kunci-mas
result = subprocess.run(
    ['bash', '-c', 'source /root/.secrets/kunci-mas.env && echo "$MINIMAX_API_KEY"'],
    capture_output=True, text=True, timeout=10
)
api_key = result.stdout.strip()

# Call MiniMax M3
resp = requests.post(
    "https://api.minimax.io/v1/chat/completions",
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    json={
        "model": "minimax-m3",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]
        }],
        "max_tokens": 1024
    },
    timeout=60
)
print(resp.json()['choices'][0]['message']['content'])
```

### 3. Process the result
MiniMax M3 returns a JSON with `choices[0].message.content`. The model outputs in the language requested — request in Malay if the user is Malay-speaking.

## Key observations from this session

- Image: 1280×960 JPEG, 119KB → base64 ~159KB
- Python `requests` handled it fine; `curl` failed with "Argument list too long"
- Model `minimax-m3` worked; no `minimax-m3-vl` was needed
- MiniMax M3 appends `<think>...</think>` reasoning blocks before the answer — strip if needed
- Response time: ~17s (MiniMax API was responsive)
- The result text can be shared immediately with the user — no need to route through any organ
