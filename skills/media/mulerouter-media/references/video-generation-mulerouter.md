# MuleRouter Video Generation

Discovered endpoints and working patterns — tested 2026-07-30.

## Available Video Endpoints

| Model | Vendor | Endpoint | Status | Tested |
|-------|--------|----------|--------|--------|
| **Veo 3.1 Fast** | Google | `/vendors/google/v1/veo/generation` | ✅ Working | 2026-07-30 |
| **Wan 2.6 T2V** | Alibaba | `/vendors/alibaba/v1/wan2.6-t2v/generation` | ✅ Working | 2026-07-30 |
| **MiniMax Hailuo-2.3** | MiniMax | `mmx video generate` (Token Plan) | ✅ Working | 2026-07-30 |

## Endpoint Details

### Veo 3.1 Fast

```
POST https://api.mulerouter.ai/vendors/google/v1/veo/generation
Authorization: Bearer $MULEROUTER_API_KEY
Content-Type: application/json

{
  "model": "veo-3.1-fast",
  "prompt": "Your video description",
  "duration": 6,
  "resolution": "720p"
}
```

**Parameters:** `model` (required: "veo-3.1-fast"), `duration` (4, 6, or 8), `resolution` ("720p" or "1080p")
**Response:** Returns `task_info` with `id` and `status: "pending"`.
**Polling:** `GET /vendors/google/v1/veo/generation/{task_id}`
**On completion:** Response includes `videos: ["https://...mp4"]` array.
**Typical time:** ~45s for 6s clip | **File size:** ~2.6MB | **Resolution:** 720p

### Wan 2.6 T2V

```
POST https://api.mulerouter.ai/vendors/alibaba/v1/wan2.6-t2v/generation
Authorization: Bearer $MULEROUTER_API_KEY
Content-Type: application/json

{
  "prompt": "Your video description",
  "duration": 5
}
```

**Note:** Model is inferred from the endpoint path — DO NOT include a `model` field.
**Polling:** `GET /vendors/alibaba/v1/wan2.6-t2v/generation/{task_id}`
**On completion:** Response includes `videos: ["https://...mp4"]` array.
**Typical time:** ~46s | **File size:** ~5.5MB | **Resolution:** 720p

### MiniMax Hailuo-2.3 (via mmx-cli)

```
cd /tmp && source /root/.secrets/kunci-mas.env
mmx video generate --prompt "..." --download /tmp/output.mp4 --poll-interval 10 --non-interactive
```

**Modes:** T2V (default), I2V (with `--first-frame`), SEF (with `--first-frame` + `--last-frame`), S2V (with `--subject-image`)
**Typical time:** ~1-2min | **File size:** ~743KB | **Quota:** 3/day, 21/week

## Multi-Engine Video Comparison (2026-07-30)

Same prompt: *"Southeast Asian Malay muscular man, chiseled chest, flexing biceps in gym"*

| Dimension | MiniMax Hailuo-2.3 | Veo 3.1 Fast | Wan 2.6 T2V |
|-----------|:------------------:|:------------:|:------------:|
| File size | 743KB | 2.6MB | **5.5MB** |
| Duration | ~6s | **6s** | 5s |
| Cost | Token Plan quota | MuleRouter API key | MuleRouter API key |
| Speed | ~2min | **~45s** | ~46s |
| Resolution | 720p | 720p | 720p |
| Route | mmx-cli | MuleRouter | MuleRouter |

## Pitfalls

1. **No dedicated video script** — `mulerouter-video.py` does not exist. Use direct curl or mmx-cli.
2. **Async polling required** — all endpoints return `pending`; poll via `GET /generation/{task_id}`.
3. **Veo duration validation** — `duration` must be exactly 4, 6, or 8.
4. **Wan model field** — Do NOT include `model` in Wan T2V body. Inferred from path.
5. **Polling endpoint mismatch** — Poll the SAME endpoint path used for creation. Cross-polling returns "Task type mismatch" error.
6. **MiniMax daily quota** — 3 videos/day, 21/week. Separate from MuleRouter key.
7. **MuleRouter video cost** — Charged to MuleRouter API key balance. No free tier.