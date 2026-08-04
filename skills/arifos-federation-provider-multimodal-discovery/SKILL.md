---
name: aifos-federation-provider-multimodal-discovery
description: Probe and document a model provider's true multimodal capability before claiming it from docs alone. Prevents the recurring failure where docs claim multimodal on a base model but the configured alias routes to a text-only variant or a dead key. Covers live dual-layer probing, provider-specific key facts for MiniMax and MiMo, MCP wiring checklist, and the doc-vs-reality verification protocol.
category: governance
---

# Federation Provider Multimodal Discovery

The failure this skill prevents: docs claim `mimo-v2.5` supports image/audio/video. The configured alias `hermes-asi` routes to `mimo-v2.5-pro`. `-pro` is text-only deep thinking. Base is multimodal. LiteLLM hard-rejects image input with `NotFoundError: No endpoints found that support image input. Received Model Group=hermes-asi` before any backend call lands. The user observes "model says it can do X but it can't."

## When to use

When claiming any of:

- "is provider X multimodal" / "wire up image/audio/video understanding"
- "audit federation multimodal surface" / "verify mimo/minimax multimodal"
- A claim that a federation model name supports image/audio/video
- LiteLLM `NotFoundError: No endpoints found that support image input`

## Two-layer probe (always run both)

### Layer 1 — Backend truth (substrate, not proxy)

```
source /root/.secrets/kunci-mas.env
curl -sS -X POST $PROVIDER_URL/v1/chat/completions \
  -H "Authorization: Bearer $PROVIDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<base-model-id>","messages":[{"role":"user","content":[
    {"type":"text","text":"describe"},
    {"type":"image_url","image_url":{"url":"https://..."}}
  ]}],"max_tokens":256}'
```

If this returns usage with non-zero image_tokens → base model IS multimodal.
If it returns 404/NotFoundError → model is text-only OR key is dead. Both possible. Check status code.

Repeat for audio (`input_audio`) and video (`video_url`) if claimed.

### Layer 2 — Proxy/litellm truth (the actual wire)

```
curl -sS -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<alias>","messages":[<image_payload>]}'
```

If this returns `NotFoundError: No endpoints found that support image input` → alias is wired to text-only backend OR capability flag missing in litellm-config.yaml.

## What the failure modes actually mean

| Symptom | Layer | Real cause |
|---|---|---|
| `NotFoundError: No endpoints support image input` | proxy | Alias bound to text-only backend variant (`-pro` vs base) |
| Image returns but `img_tokens=0` or partial content | backend | Key expired or wrong model id (key authenticates but model name rejected) |
| Backend 401 Unauthorized | backend | Key expired — not config, not model — **the keys** |
| LiteLLM returns 404 on `/health` | proxy | Expected if FED serves MCP only. Use MCP tools to probe live |
| FED balance reads $0 but API works | registry | Cached balance drifted; test live with curl before trusting state |
| Auxiliary vision works despite chat alias text-only | orchestrator | Hermes routes image → vision provider (e.g. MiniMax-M3) → text description → chat LLM. Two-step, not native |

## The probe script (use this, don't hand-type)

```bash
#!/usr/bin/env bash
# probe-multimodal.sh — verify true capability of a model alias
# Usage: ./probe-multimodal.sh <model-alias>
ALIAS="${1:?usage: $0 alias}"
source /root/.secrets/kunci-mas.env

echo "=== Layer 1: Backend truth ==="
for mod in "image" "audio" "video"; do
  case "$mod" in
    image)
      content='[{"type":"text","text":"describe in 1 word"},{"type":"image_url","image_url":{"url":"https://example-files.cnbj1.mi-fds.com/example-files/image/image_example.png"}}]'
      ;;
    audio)
      content='[{"type":"text","text":"describe"},{"type":"input_audio","input_audio":{"data":"https://example.com/audio.wav"}}]'
      ;;
    video)
      content='[{"type":"text","text":"describe"},{"type":"video_url","video_url":{"url":"https://example.com/video.mp4","fps":2,"media_resolution":"default"}}]'
      ;;
  esac
  body=$(printf '{"model":"%s","messages":[{"role":"user","content":%s}],"max_tokens":64}' "$ALIAS" "$(echo "$content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')")
  echo "--- $mod ---"
  curl -sS --max-time 30 -X POST "${PROVIDER_URL:-https://api.minimax.io/v1}/chat/completions" \
    -H "Authorization: Bearer $PROVIDER_KEY" \
    -H "Content-Type: application/json" \
    -d "$body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps({k:v for k,v in d.items() if k in ('error','choices','usage')}, indent=2)[:500])"
done

echo ""
echo "=== Layer 2: LiteLLM proxy ==="
curl -sS --max-time 15 -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d "$body" | head -c 500
```

## Provider key facts (verified 2026-08-04)

### MiMo (Xiaomi, Token Plan SGP)

- Endpoint: `https://token-plan-sgp.xiaomimimo.com/v1` (production) or `https://api.xiaomimimo.com/v1` (docs example)
- Key env: `MIMO_API_KEY`
- Models: `mimo-v2.5` (multimodal, supports image_url/input_audio/video_url), `mimo-v2.5-pro` (text-only, deep thinking), `mimo-v2.5-tts-voicedesign` (TTS)
- Deep thinking: default ON for both. Force via `extra_body={"thinking":{"type":"enabled"}}`. When ON, temp/top_p forced to 1.0/0.95.
- Multi-turn: MUST pass back `reasoning_content` or 400 on some plans.
- Web Search: separate plugin, activate in Xiaomi Console. $5/1K requests overseas.
- Structured output: `response_format={"type":"json_object"}`
- Cold start: 30-60s first hit per modality. 180s+ for video.

### MiniMax (MiniMax pay-as-you-go)

- Endpoint: `https://api.minimax.io/v1` (OpenAI compatible) or `https://api.minimax.io/anthropic` (Anthropic compatible)
- Key env: `MINIMAX_API_KEY` (NOT `MINIMAX_PLUGIN_API_KEY` — that's for the MCP server)
- Models: `MiniMax-M3` (multimodal flagship, 1M ctx), `MiniMax-M2.7` (200K, agentic), `MiniMax-M2.5`/`M2.1`/`M2` (legacy)
- MiniMax-M3 input: `image_url` supported per docs. Verify with probe before claiming.
- Pricing (50% off until further notice): M3 ≤512k $0.30/$1.20 per M tokens, >512k $0.60/$2.40.
- Token Plan tiers: Plus $20, Max $50, Ultra $120/month. One key, one bill — separated from pay-as-you-go API key.
- Subscription Key ≠ Pay-as-you-go API Key. Don't confuse.
- H3 video generation NOT in Token Plan. Video packages separate ($1,000+ Standard).
- Voice clone $1.50, voice design $3 — each NOT in Token Plan.

## MCP wiring checklist (for ANY provider)

When wiring a provider MCP into the federation, register in **all** of these:

1. `~/.hermes/config.yaml` — `mcp_servers:` block (for Hermes)
2. `~/.claude/mcp.json` — `mcpServers` (for Claude Code)
3. `~/.grok/mcp.json` — `mcpServers` (for Grok Build)
4. `~/.config/opencode/opencode.json` — `mcpServers` (for OpenCode, often empty)

Detect missing registration: grep each path for the provider name. If absent, add the stdio entry pointing to the binary and pass the env var from `kunci-mas.env`. Restart session.

## The doc-vs-reality checklist

Before claiming a federation model is multimodal, **all four boxes must be ticked**:

1. Layer 1 probe accepted the multimodal request, returned non-zero image_tokens
2. Layer 2 probe accepted it (or no proxy in production path — verify which)
3. MCP wiring: every tool config has the provider registered
4. Key alive: separate curl to `/v1/models` returns expected model list

If any box unticked, the agent may not need to be fixed — but the doc-claim is wrong until proven otherwise.

## Anti-pattern: capability flag override

It is tempting to add `supports_vision: true` to a litellm-config entry to make it accept image input. **Don't**, unless the backend genuinely supports it. Litellm's capability gate exists because misrouted multimodal requests silently degrade to text-and-lose-the-image. T1 reversible config edits that override real capability metadata turn detectable failures into silent data loss.

## Pitfalls learned in real sessions

- **2026-08-04:** I claimed hermes-asi was multimodal by reading MiMo docs. Kimi's live T0 probe showed it wasn't. Doc-claim without substrate probe is fabrication (violates F2). Always probe both layers.
- **2026-08-04:** MiniMax pay-as-you-go key had expired. All MiniMax-M3 requests returned partial data or 401. Symptoms looked like config errors. Probe the keys, not the routing.
- **2026-08-04:** User gave API key in chat; handling per F1 AMANAH — never echo, never paste in chat, write to kunci-mas.env directly. Same handling for any sovereign-provided secret.
- **2026-08-04:** LiteLLM `/health` 404 on FED port 7074 — expected, FED serves MCP only. Don't confuse "endpoint not found" with "service down". Use MCP tools for live probe.
- **2026-08-04:** Archived providers drift in FED token_bank after they're removed from litellm-config. ~$110 stranded (mulerouter $49.93, tokenrouter $59.94, openrouter $0.50). Tombstone in DB with audit receipt (F11) before deleting or withdraw funds + drop the row. Don't leave orphan balances.
- **2026-08-04:** User asked for MiniMax MCP wiring across 3 tools (Hermes, Claude, Grok, OpenCode). The right answer was 3 commands of `python3 -c "..."`, not a 100-line explanation. Match response shape to user signal.
