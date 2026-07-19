# MoA + OpenCode Provider Matrix — Verified 2026-07-04

## The Critical Distinction

`opencode-zen` and `opencode-go` are registered as SEPARATE Hermes providers with DIFFERENT endpoints:

| Provider | Base URL | Models | Billing |
|---|---|---|---|
| `opencode-zen` | `https://opencode.ai/zen/v1` | 50 (full catalog) | Zen tier |
| `opencode-go` | `https://opencode.ai/zen/go/v1` | 20 (subset) | Go tier |

Source: `plugins/model-providers/opencode-zen/__init__.py` lines 113 + 121.

**Critical:** The `/go/` in the opencode-go URL is NOT a typo — it's the plugin-registered base_url. The same physical API key works on both endpoints, but billing tier is determined server-side.

## Models by Provider

### opencode-zen ONLY (not on /go/)

- claude-fable-5, claude-opus-4-8, claude-opus-4-7, claude-opus-4-6, claude-opus-4-5, claude-opus-4-1
- claude-sonnet-5, claude-sonnet-4-6, claude-sonnet-4-5, claude-sonnet-4, claude-haiku-4-5
- gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.4-pro, gpt-5.4-mini, gpt-5.4-nano
- gpt-5.3-codex-spark, gpt-5.3-codex, gpt-5.2, gpt-5.2-codex, gpt-5.1, gpt-5.1-codex-max, gpt-5.1-codex, gpt-5.1-codex-mini, gpt-5, gpt-5-codex, gpt-5-nano
- gemini-3.5-flash, gemini-3.1-pro, gemini-3-flash
- grok-build-0.1
- big-pickle, nemotron-3-ultra-free, north-mini-code-free

### opencode-go ONLY (not on /zen/v1)

- mimo-v2-pro, mimo-v2-omni, mimo-v2.5-pro, mimo-v2.5
- hy3-preview
- qwen3.7-max, qwen3.7-plus

### Both providers

- deepseek-v4-pro, deepseek-v4-flash
- minimax-m3, minimax-m2.7, minimax-m2.5
- kimi-k2.7-code, kimi-k2.6, kimi-k2.5
- glm-5.2, glm-5.1, glm-5
- qwen3.6-plus, qwen3.5-plus
- deepseek-v4-flash-free, mimo-v2.5-free

## Auth

Same physical API key from `https://opencode.ai/auth` works on both endpoints. But Hermes treats them as separate credential namespaces:

- `OPENCODE_ZEN_API_KEY` → opencode-zen provider
- `OPENCODE_GO_API_KEY` → opencode-go provider

Set BOTH to the same value in `~/.hermes/.env` if you use both.

## api_mode per model (opencode-go)

| Model prefix | api_mode | Notes |
|---|---|---|
| minimax-* | anthropic_messages | Uses Anthropic SDK path |
| qwen3.7-max | anthropic_messages | Uses Anthropic SDK path |
| Everything else | chat_completions | Standard OpenAI-compatible |

Source: `hermes_cli/models.py::opencode_model_api_mode` lines 3343-3348.

**MoA aggregator implication:** Use a `chat_completions` model as aggregator (DeepSeek, Kimi, GLM) to avoid mode conflicts. MiniMax as aggregator works but routes through Anthropic Messages path.

## MoA Provider Selection Rules

| Model family | Correct provider | Wrong provider (will 401) |
|---|---|---|
| Claude (any) | opencode-zen | opencode-go |
| GPT (any) | opencode-zen | opencode-go |
| Gemini (any) | opencode-zen | opencode-go |
| DeepSeek | either (prefer zen) | — |
| MiniMax | either (prefer zen) | — |
| MiMo | opencode-go (canonical) | opencode-zen (has free tier only) |
| Qwen3.7-max | opencode-go | opencode-zen |

## Recommended MoA Presets — Zen tier (tested 2026-07-03)

```yaml
moa:
  presets:
    default:  # hard reasoning
      reference_models:
      - provider: opencode-zen
        model: gpt-5.5
      - provider: opencode-zen
        model: deepseek-v4-pro
      aggregator:
        provider: opencode-zen
        model: claude-opus-4-8
      reference_max_tokens: 600
      max_tokens: 4096
      enabled: true
    code:  # code review
      reference_models:
      - provider: opencode-zen
        model: gpt-5.3-codex
      - provider: opencode-zen
        model: kimi-k2.7-code
      aggregator:
        provider: opencode-zen
        model: claude-sonnet-5
      reference_max_tokens: 600
      max_tokens: 4096
      enabled: true
    fast:  # quick queries
      reference_models:
      - provider: opencode-zen
        model: gemini-3.5-flash
      - provider: opencode-zen
        model: deepseek-v4-flash
      aggregator:
        provider: opencode-zen
        model: claude-haiku-4-5
      reference_max_tokens: 400
      max_tokens: 4096
      enabled: true
```

## Recommended MoA Presets — Go tier only (validated 2026-07-04)

When the user has Go subscription only (not Zen), use `opencode-go` with Go-tier models. No Claude/GPT/Gemini available.

```yaml
moa:
  presets:
    default:  # strongest reasoning on Go
      reference_models:
      - provider: opencode-go
        model: kimi-k2.7-code
      - provider: opencode-go
        model: qwen3.7-plus
      aggregator:
        provider: opencode-go
        model: deepseek-v4-pro
      reference_temperature: 0.6
      aggregator_temperature: 0.4
      reference_max_tokens: 600
      max_tokens: 4096
      enabled: true
    code:  # coding specialists
      reference_models:
      - provider: opencode-go
        model: deepseek-v4-pro
      - provider: opencode-go
        model: qwen3.6-plus
      aggregator:
        provider: opencode-go
        model: kimi-k2.7-code
      reference_temperature: 0.5
      aggregator_temperature: 0.3
      reference_max_tokens: 600
      max_tokens: 4096
      enabled: true
    fast:  # speed-optimized
      reference_models:
      - provider: opencode-go
        model: glm-5.2
      - provider: opencode-go
        model: minimax-m3
      aggregator:
        provider: opencode-go
        model: deepseek-v4-flash
      reference_temperature: 0.5
      aggregator_temperature: 0.3
      reference_max_tokens: 400
      max_tokens: 4096
      enabled: true
```

## Verifying MoA Actually Runs

Without verbose mode, MoA failures are invisible — Hermes silently falls back to the main model.

```bash
# Test with verbose — look for MoA-specific log lines
hermes chat -q "hello" --provider moa -m default -v -Q 2>&1 | \
  grep -iE "moa_reference|moa_aggregator|failed|CreditsError|401"

# Expected (working):
#   agent.auxiliary_client - INFO - Auxiliary moa_reference: using custom (kimi-k2.7-code) at https://opencode.ai/zen/go/v1/
#   agent.auxiliary_client - INFO - Auxiliary moa_reference: using custom (qwen3.7-plus) at https://opencode.ai/zen/go/v1/
#   agent.auxiliary_client - INFO - Auxiliary moa_aggregator: using custom (deepseek-v4-pro) at https://opencode.ai/zen/go/v1/

# Expected (broken — credits or auth):
#   agent.moa_loop - WARNING - MoA reference model opencode-go:kimi-k2.7-code failed: Error code: 401 - CreditsError
```

## CreditsError vs AuthError

| Error message | Meaning | Fix |
|---|---|---|
| `"Invalid API key"` (AuthError) | Key not set or wrong provider | Set OPENCODE_GO_API_KEY in .env |
| `"Insufficient balance"` (CreditsError) | Key valid, subscription out of credits | Top up at billing URL in error |
| `"Model not supported"` (ModelError) | Model not on this endpoint | Wrong provider (e.g. GPT on opencode-go) → switch to opencode-zen |

## Pitfall: silent fallback hides MoA failures

When reference models fail, MoA includes the failure notes in context and continues with the aggregator. If the aggregator also fails, Hermes falls back to the main model. The output looks normal but it's single-model, not multi-perspective synthesis. ALWAYS verify with `-v` flag after configuring presets.
