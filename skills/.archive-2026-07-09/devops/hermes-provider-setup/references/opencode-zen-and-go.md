# OpenCode Zen and Go — full registration notes

## CORRECTION (2026-07-06): opencode-go model list MUST match Go subscription

The `opencode-go` provider config in Arif's Hermes had accumulated 40+ models including Claude, GPT, Gemini, and Grok — all from Zen tier. These are phantom entries on a Go subscription. Every call to these models returns "Model not supported" (401).

**Verified Go-tier models (from OpenCode Go pricing page, 2026-07-06):**

```
mimo-v2.5-pro      3,250 req/5h    flagship reasoning
mimo-v2.5          30,100 req/5h   multimodal
deepseek-v4-pro    3,450 req/5h
deepseek-v4-flash  31,650 req/5h
qwen3.7-plus       4,300 req/5h
qwen3.7-max        950 req/5h
kimi-k2.7-code     1,150 req/5h
minimax-m3         3,200 req/5h
glm-5.2            880 req/5h
big-pickle         200 req/5h      free tier
+ free models: deepseek-v4-flash-free, mimo-v2.5-free, nemotron-3-ultra-free, north-mini-code-free
+ qwen3.6-plus, qwen3.5-plus, kimi-k2.6, kimi-k2.5, minimax-m2.7, minimax-m2.5, glm-5.1, glm-5
```

**NOT on Go (remove from opencode-go config):**
- All Claude models (opus, sonnet, haiku, fable)
- All GPT models (5.5, 5.4, 5.3-codex, 5.2, 5.1, 5, nano)
- All Gemini models (3.5-flash, 3.1-pro, 3-flash)
- grok-build-0.1

**Rule**: when user says "fix your opencode context with reality" or provides a pricing page, strip the provider config to match the actual subscription. Don't leave phantom models — they pollute the picker and confuse fallback chains.

## CORRECTION (2026-07-06): opencode-go endpoint is /zen/v1, not /zen/go/v1

The actual Hermes config uses `https://opencode.ai/zen/v1` for opencode-go — the SAME endpoint as opencode-zen. Server-side tier routing determines which models are available based on subscription (Go vs Zen). The `/zen/go/v1` path documented in older source code may have been consolidated or was never the production path.

**Verified from live config (2026-07-06):**
```yaml
opencode-go:
    name: OpenCode Go ($10/mo, open-source models)
    api: https://opencode.ai/zen/v1
    key_env: OPENCODE_GO_API_KEY
```

The key differentiation is server-side: same endpoint, same auth header, different model availability based on subscription tier. Probe `/v1/models` to see what your tier actually serves.

## CORRECTION (2026-07-03): Go ≠ Zen — different model catalogs on same endpoint

The previous version of this file said "Go is a subscription tier on top of Zen. Same endpoint, same key, same model IDs." That was WRONG. The Hermes plugin registers TWO providers with DIFFERENT base URLs:

| Provider slug | Endpoint | Models |
|---|---|---|
| `opencode-zen` | `https://opencode.ai/zen/v1` | 50 models (full: Claude, GPT, Gemini, DeepSeek, MiniMax, Kimi, GLM, Qwen, MiMo, Grok) |
| `opencode-go` | `https://opencode.ai/zen/v1` (same endpoint, server-side tier routing) | 22 open-source models (NO Claude, GPT, Gemini, Grok) |

Source: verified from live Hermes config (2026-07-06). Both providers use `https://opencode.ai/zen/v1`. Server-side tier routing determines model availability. The `/zen/go/v1` path documented in older plugin source (`plugins/model-providers/opencode-zen/__init__.py`) may have been consolidated into the main endpoint.

## Auth

Same physical API key from `https://opencode.ai/auth` works on both endpoints. But Hermes treats them as separate credential namespaces:

- `OPENCODE_ZEN_API_KEY` → opencode-zen provider
- `OPENCODE_GO_API_KEY` → opencode-go provider

Set BOTH to the same value in `~/.hermes/.env` if you use both providers.

## Model availability by provider

### opencode-zen ONLY (not on /go/)
- All Claude models (opus-4-8, sonnet-5, haiku-4-5, fable-5, etc.)
- All GPT models (5.5, 5.4, 5.3-codex, 5.2, 5.1, 5, etc.)
- All Gemini models (3.5-flash, 3.1-pro, 3-flash)
- grok-build-0.1
- Free tier models (big-pickle, nemotron-3-ultra-free, north-mini-code-free)

### opencode-go ONLY (not on /zen/v1)
- mimo-v2-pro, mimo-v2-omni, mimo-v2.5-pro, mimo-v2.5
- hy3-preview
- qwen3.7-max, qwen3.7-plus

### Both providers
- deepseek-v4-pro, deepseek-v4-flash, deepseek-v4-flash-free
- minimax-m3, minimax-m2.7, minimax-m2.5
- kimi-k2.7-code, kimi-k2.6, kimi-k2.5
- glm-5.2, glm-5.1, glm-5
- qwen3.6-plus, qwen3.5-plus
- mimo-v2.5-free

## Model IDs

Bare format: `gpt-5.5`, NOT `opencode/gpt-5.5`. The `opencode/<id>` prefix is internal to OpenCode's config, not the API.

## Auth header

`Authorization: Bearer <key>` — NOT `api-key:` header (that's Xiaomi MiMo's format).

## Tier distinction (Go vs Zen vs Free)

All tiers share the same two endpoints. Tier is determined server-side from subscription:

| Tier | Cost | Quota model |
|---|---|---|
| **Free** | $0 | Per-model RPH limits |
| **Go** | $5 first month / $10/mo | Higher RPH limits |
| **Zen** | Pay-per-token | No RPH cap |
| **Enterprise** | Custom | SLA + dedicated capacity |

## Working registration

```yaml
providers:
  opencode-zen:
    name: "OpenCode Zen"
    api: "https://opencode.ai/zen/v1"
    key_env: OPENCODE_ZEN_API_KEY
    transport: openai_chat
    models:
      - { id: claude-opus-4-8, name: "Claude Opus 4.8" }
      - { id: gpt-5.5, name: "GPT 5.5" }
      - { id: deepseek-v4-pro, name: "DeepSeek V4 Pro" }
      # ... etc (50 models total — probe /v1/models for full list)
  opencode-go:
    name: "OpenCode Go"
    api: "https://opencode.ai/zen/v1"
    key_env: OPENCODE_GO_API_KEY
    transport: openai_chat
    models:
      - { id: mimo-v2.5-pro, name: "MiMo-V2.5-Pro" }
      - { id: qwen3.7-max, name: "Qwen3.7 Max" }
      # ... etc (20 models total — probe /zen/go/v1/models for full list)
```

## Verification

```bash
# Zen models (50)
curl -sS https://opencode.ai/zen/v1/models | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"

# Go models (same endpoint, server-side tier filtering)
curl -sS https://opencode.ai/zen/v1/models -H "Authorization: Bearer $OPENCODE_GO_API_KEY" | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"
```

## Cross-reference

- `hermes-provider-setup/SKILL.md` — main skill (covers MoA presets + provider matrix)
- `references/moa-opencode-provider-matrix.md` — MoA-specific provider selection rules
