# arifOS Provider Architecture — Sealed 2026-07-06

## Provider Stack (5 providers, all armed)

| Provider | Endpoint | Key Env | Role |
|---|---|---|---|
| xiaomi-mimo | token-plan-sgp.xiaomimimo.com/v1 | XIAOMI_API_KEY | Primary (mimo-v2.5-pro text + mimo-v2.5 vision) |
| bailian-token-plan | ap-southeast-1.maas.aliyuncs.com | QWEN_API_KEY | Fallback 1 + MoA reference/aggregator |
| minimax | api.minimax.io/v1 | MINIMAX_API_KEY | Fallback 2 (multimodal: image/speech/music/video) |
| opencode-go | opencode.ai/zen/v1 | OPENCODE_GO_API_KEY | MoA presets (22 open-source models, $10/mo) |
| bailian-payg | ws-wlab8klalfojzq7i | BAILIAN_PAYG_API_KEY | Emergency backup |

## Fallback Chain

```
1. mimo-v2.5-pro    (xiaomi-mimo, Token Plan SGP)
2. qwen3.7-plus     (bailian-token-plan)
3. minimax-m3       (minimax direct, Monthly Max)
```

## Model Assignments

| Slot | Model | Provider | Purpose |
|---|---|---|---|
| PRIMARY | mimo-v2.5-pro | xiaomi-mimo | Main reasoning, 1M ctx, tool_call |
| VISION | mimo-v2.5 | xiaomi-mimo | Image/audio/video understanding |
| FALLBACK 1 | qwen3.7-plus | bailian-token-plan | Quota-exhausted rotation |
| FALLBACK 2 | minimax-m3 | minimax | Multimodal fallback |

## MoA Presets (via opencode-go)

| Preset | Reference Models | Aggregator |
|---|---|---|
| quality (default) | kimi-k2.7-code + qwen3.7-plus | deepseek-v4-pro |
| code | deepseek-v4-pro + qwen3.6-plus | kimi-k2.7-code |
| fast | glm-5.2 + minimax-m3 | deepseek-v4-flash |

## Auxiliary

| Function | Provider | Model |
|---|---|---|
| Vision | xiaomi-mimo | mimo-v2.5 |
| TTS | edge (free) | en-US-AriaNeural |
| STT | local | faster-whisper base |
| OCR | local | tesseract 5.5.0 + opencv 4.13.0 |

## Excluded (by sovereign directive)

- Claude (removed from fallback — no ANTHROPIC_API_KEY)
- Gemini (removed from fallback)
- GPT (removed from fallback)
- Grok (only for x_search, not main/fallback)

## Key Design Decisions

1. **Single-provider vision**: mimo-v2.5 handles vision on the same provider as the main model. No cross-provider billing complexity.
2. **Open-source only**: Zero Claude/Gemini/GPT in fallback. All providers use open-source or open-weight models.
3. **Three-tier multimodal fallback**: Every tier supports image/audio/video — fallback never degrades to text-only.
4. **MoA via proxy**: OpenCode Go provides access to 22 open-source models for MoA reference/aggregation at $10/month.
5. **mmx-cli for media**: MiniMax TTS/video/music/image generation via CLI, not MCP. Skill at minimax-cli.

## Config Hashes (sealed 2026-07-06T05:13:18Z)

```
config.yaml: 80058ea7b3696a85385b4921865c57d8c4a3af237b58ef976b1000bad084115c
.env: 063a5d3b82cb4d7bff76b616ca6f162e089212c60f7d9d23f46e19bc5875fe03
```

## Seal Receipt

Full receipt at: `/var/arifos/artifacts/outbox/2026-07-06/hermes-agent-zen-seal.md`
