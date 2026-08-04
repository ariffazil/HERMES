# MiMo (Xiaomi) Capability Matrix — 2026-08-04

**Source:** mimo.mi.com docs + live API probes
**Verified by:** Hermes (docs) + Kimi K3 (live probes)

## Model Variants

| Model | Type | Context | Multimodal | Deep Thinking |
|---|---|---|---|---|
| `mimo-v2.5` | Base | 1M | ✅ image/audio/video | ✅ ON by default |
| `mimo-v2.5-pro` | Deep-thinking | 1M | ❌ text-only | ✅ ON by default (forced temp=1.0, top_p=0.95) |

**Critical:** `-pro` variant is TEXT-ONLY. Docs describe `mimo-v2.5` (base) for multimodal. Same vendor, different alias → different capability.

## Endpoints

| Endpoint | Use Case |
|---|---|
| `https://api.xiaomimimo.com/v1` | Pay-as-you-go (docs default) |
| `https://token-plan-sgp.xiaomimimo.com/v1` | Token Plan SGP (our billing) |
| `https://api.xiaomimimo.com/anthropic` | Anthropic-compatible protocol |

Both endpoints reach same models. Different billing gateway.

## Capabilities

### Text Chat
```python
messages=[{"role": "user", "content": "Hello"}]
# No extra flags needed
```

### Image Understanding (mimo-v2.5 ONLY)
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "text", "text": "describe this image"},
        {"type": "image_url", "image_url": {"url": "<URL or base64>"}}
    ]
}]
# Formats: JPEG, PNG, GIF, WebP, BMP
# Max size: 50MB per image
# Verify: usage.image_tokens > 0 in response
```

### Audio Understanding (mimo-v2.5)
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "input_audio", "input_audio": {"data": "<URL or base64>"}},
        {"type": "text", "text": "describe this audio"}
    ]
}]
# Max size: 100MB URL, 50MB base64
# Token calc: duration_seconds × 6.25
```

### Video Understanding (mimo-v2.5)
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "video_url", "video_url": {"url": "<URL>"}, "fps": 2, "media_resolution": "default"},
        {"type": "text", "text": "describe this video"}
    ]
}]
# Max size: 300MB URL, 50MB base64
# fps: frames per second (2-5 typical)
# media_resolution: "default" or "max"
# Max frames: 2048
```

### Deep Thinking (mimo-v2.5-pro)
```python
extra_body={"thinking": {"type": "enabled"}}  # ON by default
extra_body={"thinking": {"type": "disabled"}}  # Force OFF
# Returns reasoning_content field
# NOTE: temp/top_p forced to 1.0/0.95 when thinking ON
# Multi-turn: MUST pass back reasoning_content field (400 error if missing)
```

### Web Search (mimo-v2.5-pro)
```python
tools=[{
    "type": "web_search",
    "max_keyword": 3,
    "force_search": True,
    "limit": 1,
    "user_location": {"type": "approximate", "country": "China"}
}]
# Requires plugin activation in MiMo Console (separate billing)
# Returns annotations: [{url, title, summary, site_name}]
```

### Structured Output (JSON mode)
```python
response_format={"type": "json_object"}
# Guarantee: syntactically valid JSON
# NOT guarantee: correct fields/schema — validate with jsonschema
```

## Pricing Notes
- Image tokens calculated via patch_size=16, spatial_merge_size=2
- Audio tokens: duration_seconds × 6.25
- Video tokens: complex (frames × pixels_per_frame)
- Web Search: separate billing per invocation
- Deep Thinking: reasoning_tokens included in completion_tokens

## Common Pitfalls
1. **`mimo-v2.5-pro` ≠ multimodal** — use `mimo-v2.5` (base) for image/audio/video
2. **Deep Thinking forces temp=1.0** — can't customize temperature when thinking ON
3. **Multi-turn reasoning_content** — MUST echo back `reasoning_content` field or 400 error
4. **Web Search not free** — requires Console plugin activation + separate billing
5. **Cold start** — first hit per modality may take 30-60s on Token Plan SGP
6. **V2 deprecated** — MiMo-V2 series deprecated 2026-06-30, migrate to V2.5
