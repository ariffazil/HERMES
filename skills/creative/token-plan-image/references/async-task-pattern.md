# Token Plan Image Gen — Async Task Pattern (Fallback)

**Status:** Proven 2026-08-04 (Sabah geological cross-section generation).

When the canonical OpenAI-compatible path (`/api/v1/services/aigc/multimodal-generation/generation` with messages-format input — see SKILL.md) is unreachable or returns errors, an alternative async task pattern works for **text-to-image** models (qwen-image-plus, qwen-image, wanx-v1, etc.).

This is **NOT** the preferred path. The SKILL.md primary path should work. This pattern is a fallback when:
- The OpenAI-compatible `/compatible-mode/v1/images/generations` returns 404 (gateway does not expose image-gen at that route)
- The messages-format endpoint returns errors specific to image payloads
- You need a simpler `{"input":{"prompt":"..."}}` shape rather than messages-format

## Working endpoint (DASHSCOPE-style async)

```
POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
Authorization: Bearer $DASHSCOPE_API_KEY   # token-plan ap-southeast-1 key works here too
Content-Type: application/json
X-Dashscope-Async: enable    # ← critical header, makes it async
```

**Body shape** (simpler than messages-format):

```json
{
  "model": "qwen-image-plus",
  "input": {"prompt": "..."},
  "parameters": {"size": "1536*1024", "n": 1, "seed": 42}
}
```

Size format: `WIDTH*HEIGHT` (asterisk, not "x"). Examples: `1024*768`, `1536*1024`, `1024*1024`.

## Submit + poll

```bash
# Submit
TASK_RESP=$(curl -s -m 30 -X POST \
  "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Dashscope-Async: enable" \
  -d '{"model":"qwen-image-plus","input":{"prompt":"..."},"parameters":{"size":"1536*1024","n":1,"seed":42}}')
TASK_ID=$(echo "$TASK_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['output']['task_id'])")

# Poll until SUCCEEDED (typically 5-10 seconds for qwen-image-plus)
for i in 1 2 3 4 5 6 7 8 9 10; do
  STATE=$(curl -s -m 10 "https://dashscope-intl.aliyuncs.com/api/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['output']['task_status'])")
  if [ "$STATE" = "SUCCEEDED" ] || [ "$STATE" = "FAILED" ]; then break; fi
  sleep 4
done

# Extract signed URL
URL=$(curl -s -m 10 "https://dashscope-intl.inc.aliyuncs.com/api/v1/tasks/$TASK_ID" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['output']['results'][0]['url'])")

# Download
curl -sL -o output.png "$URL"
```

## Status enum

- `PENDING` → queued, not started yet
- `RUNNING` → inference in progress (typical: 5-15s for qwen-image-plus)
- `SUCCEEDED` → ready, signed URL valid for ~48h
- `FAILED` → check `output.message` for reason (usually safety filter or quota)

## Model IDs that worked on this endpoint

- `qwen-image-plus` — best quality for technical/illustration content
- `qwen-image` — faster, lower quality
- `wanx-v1` — Wan 1.x baseline (older, more permissive safety)

## Why this exists (2026-08-04 evidence)

The token-plan gateway `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/images/generations` returned **404** for image-gen calls (it only exposes text/chat). The DASHSCOPE international URL (`dashscope-intl.aliyuncs.com`) accepts token-plan keys via the SGL-style async task API for image gen.

If you are scripting this from arifOS `/root/scripts/`, save the snippet as `/root/scripts/mage-call.py` pattern (proven template in the Sabah mission).

## Companion path: Modal-hosted mage endpoint

`https://arifbfazil--mage-flow-inference-api-generate.modal.run` accepts synchronous POST with `{"prompt":"...","width":1024,"height":768,"steps":...,"cfg":...}` and returns `{"image_b64":"..."}`. **Caveat:** as of 2026-08-04, the MCP wrapper `mcp__mage__mage_generate` returns `{"status":"error","error":"unknown"}` for all calls, but the underlying Modal service still works via direct curl. Try direct curl before assuming mage is fully broken.

## Pitfalls

- **404 on `/compatible-mode/v1/images/generations`** → switch to `/api/v1/services/aigc/text2image/image-synthesis` with async header
- **Sync call returns "current user api does not support synchronous calls"** → add `X-Dashscope-Async: enable` header
- **Model not exist (HTTP 400)** → try `qwen-image-plus` instead of `qwen-image-2.0` (different name spaces)
- **Quota errors** → token-plan credit exhausted; user must top up at qwencloud.com
- **Diffusion-typical garbled text in labels** → overlay PIL text boxes on top (see `image-text-editing` skill, references/diffusion-composite.md)
- **Image quality issues at low step counts** → mage endpoint ignores cfg/steps params in some versions; always verify output is real content (file size > 50KB indicates real content, ~4KB indicates stub/placeholder)
