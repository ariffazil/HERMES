# MiniMax Direct Provider — Hermes Configuration Reference (2026-07-06)

## Provider registration

MiniMax Token Plan uses `https://api.minimax.io/v1` (OpenAI-compatible). The subscription key prefix is `sk-cp-` (distinct from pay-as-you-go API keys).

```yaml
providers:
  minimax:
    name: MiniMax (Token Plan Max)
    api: https://api.minimax.io/v1
    key_env: MINIMAX_API_KEY
    transport: openai_chat
    models:
      - id: MiniMax-M1
        name: MiniMax M1
      - id: minimax-m3
        name: MiniMax M3
```

`~/.hermes/.env`:
```
MINIMAX_API_KEY=sk-cp-...
```

## Token Plan tiers

| Tier | Price | Concurrent agents | Context | Key capability |
|------|-------|-------------------|---------|----------------|
| Plus | $20/mo | 3-4 | 1M | All models |
| Max | $50/mo | 4-5 | 1M | Full multimodal (image, speech, music, video gen: 3/day) |
| Ultra | $120/mo | 6-7 | 1M | Heavy agent workflows |

All tiers share one quota across text, image, speech, and music.

## Key format

- Subscription key: `sk-cp-<random>` — for Token Plan / credits calls
- Pay-as-you-go key: different prefix — for per-token billing
- They are NOT interchangeable. `sk-cp-` keys cannot be used for pay-as-you-go and vice versa.

## Multimodal capabilities (Monthly Max)

- **Language**: MiniMax-M1 (flagship), minimax-m3
- **Image understanding**: native multimodal input
- **Video understanding**: native input
- **Speech**: TTS and ASR built-in
- **Music**: generation supported
- **Video generation**: 3 clips/day on Max tier
- **~5.1B tokens/month** of M3 usage included

## Probe command

```bash
curl -sS -H "Authorization: Bearer $MINIMAX_API_KEY" \
  https://api.minimax.io/v1/models | python3 -c "
import sys,json
d=json.load(sys.stdin)
for m in d.get('data',[]): print(m['id'])
"
```

## Pitfall: MINIMAX_API_HOST exists but MINIMAX_API_KEY may not

Some setups have `MINIMAX_API_HOST=https://api.minimax.io` in env (from MiniMax CLI or SDK) but no `MINIMAX_API_KEY`. The host env var alone doesn't authenticate — you need the subscription key from https://platform.minimax.io/user-center/payment/token-plan.

## Pitfall: MiniMax MCP ≠ MiniMax provider

The `minimax-coding-plan-mcp` MCP server (stdio) was quarantined due to structural memory leak. It's a separate concern from the provider registration. MiniMax models are accessible via:
1. Direct provider (this config) — full multimodal
2. OpenCode Go proxy — text only, as `minimax-m3` / `minimax-m2.7` / `minimax-m2.5`

For multimodal (image, audio, video), use the direct provider. For text-only fallback through OpenCode, the proxy works.

## When to use MiniMax as fallback vs primary

MiniMax M3 is strong but not the strongest reasoning model. Best use:
- **Third-tier fallback** after mimo-v2.5-pro and qwen3.7-plus
- **Multimodal fallback** — when mimo and qwen are both unavailable, MiniMax handles image/speech/music
- **NOT recommended as primary** for code/reasoning — mimo-v2.5-pro and qwen3.7-plus are stronger

## Cross-reference

- `references/mmx-cli-minimax-multimodal-2026-07.md` — mmx-cli for TTS, video, music, image, vision, search (CLI multimodal)
- Main SKILL.md — MiniMax in fallback chain, MoA presets


```yaml
fallback_providers:
  - provider: custom
    model: mimo-v2.5-pro          # Tier 1: strongest reasoning
    base_url: https://token-plan-sgp.xiaomimimo.com/v1
    key_env: XIAOMI_API_KEY
  - provider: bailian-token-plan  # Tier 2: strong multimodal
    model: qwen3.7-plus
  - provider: minimax             # Tier 3: multimodal + music/speech
    model: minimax-m3
```

All three tiers support multimodal input. If tier 1 fails, tier 2 handles vision natively. If tier 2 fails, tier 3 covers image/speech/music. No dead entries. No providers without keys. Zen.
