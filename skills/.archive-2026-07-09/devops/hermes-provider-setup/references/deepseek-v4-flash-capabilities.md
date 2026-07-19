# DeepSeek V4 Flash — Verified Capability Reference

> Source: DeepSeek official API docs (api-docs.deepseek.com), live API probes, HN community reports.
> Verified: 2026-07-19

## Model Identity

| Field | Value |
|---|---|
| API model name | `deepseek-v4-flash` |
| Sibling | `deepseek-v4-pro` (bigger, stronger, 500 concurrency) |
| Deprecated aliases | `deepseek-chat` → non-thinking mode of v4-flash. `deepseek-reasoner` → thinking mode of v4-flash. Both deprecated 2026-07-24 15:59 UTC. |
| Base URL (OpenAI) | `https://api.deepseek.com` |
| Base URL (Anthropic) | `https://api.deepseek.com/anthropic` |
| Model version | DeepSeek-V4-Flash |

## Specs (verified from DeepSeek's Models & Pricing page)

| Spec | Value |
|---|---|
| **Context window** | **1,000,000 tokens (1M)** |
| **Max output** | **384,000 tokens** |
| Thinking mode | Default: enabled. Switch via `thinking: {"type": "enabled"}` or `thinking: {"type": "disabled"}`. See Thinking Mode docs. |
| JSON Output | ✓ |
| **Tool Calls** | ✓ |
| Chat Prefix Completion (Beta) | ✓ |
| FIM Completion (Beta) | ✓ (non-thinking mode only) |
| **Vision / Multimodal** | **NOT supported** |
| Concurrency limit | **2,500** requests |

## Multimodality: Confirmed Text-Only

**DeepSeek V4 Flash does not accept any image/vision input.** Proven via live API probe: sending `image_url` content blocks returns `400: unknown variant 'image_url', expected 'text'`.

The features table on DeepSeek's official Models & Pricing page lists JSON Output, Tool Calls, Chat Prefix, FIM — zero mention of vision or multimodal support. The Anthropic API example code only uses `"type": "text"` content blocks, never `"type": "image"`.

## Hermes Agent — Vision Fallback

When DeepSeek V4 Flash is the primary model in Hermes Agent, vision tasks still work through **auxiliary fallback**:

1. Hermes detects primary model has no native vision (set `model.supports_vision: false` in config)
2. `vision_analyze_tool()` routes image to `auxiliary.vision` provider
3. Auxiliary vision model returns a text description
4. DeepSeek receives and reasons on the text description — never touches raw pixels

**Config pattern for DeepSeek primary + auxiliary vision:**
```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
  supports_vision: false           # CRITICAL — forces image routing via auxiliary

auxiliary:
  vision:
    provider: <vision-capable-provider>
    model: <vision-capable-model>

agent:
  image_input_mode: auto            # or text to force all images through auxiliary
```

Without `supports_vision: false`, Hermes attempts native image attachment, hits the API's `'unknown variant image_url'` rejection, and the user sees "model doesn't support images."

## Pricing (per 1M tokens)

| Scenario | deepseek-v4-flash | deepseek-v4-pro |
|---|---|---|
| Input (cache hit) | **$0.0028** | $0.0036 |
| Input (cache miss) | **$0.14** | $0.435 |
| Output | **$0.28** | $0.87 |
| Concurrency | 2,500 | 500 |

~350× cheaper than Claude Sonnet on output tokens.

## Agentic Coding Performance

From HN community reports (2026-05-16, seangoedecke.com):
> "A local model good enough to compete with at least the low end of frontier model agentic coding"

Can run locally via:
- **llama.cpp** / DwarfStar 4 (antirez's stripped-down build) — fully local, no API needed
- AMD MI300X (fergusfinn.com, 2026-06-02)

## Strengths

- **Massive 1M context** — can hold entire codebases in a single turn
- **384K max output** — can produce very long artifacts
- **Thinking mode** — chain-of-thought reasoning built in by default
- **Insanely cheap** — $0.28/M output tokens
- **2,500 concurrency** — high throughput
- **Runs locally** — can drop into llama.cpp for offline coding tasks

## Limitations

- **No vision / multimodal** — cannot see images, screenshots, or video
- **No native audio** — no TTS/STT
- **No file upload endpoint** — cannot accept PDF/DOCX context natively (text-only API)
- DeepSeek-chat / deepseek-reasoner aliases being deprecated 2026-07-24 — update any configs using these

## Config for Hermes Agent

```yaml
providers:
  deepseek:
    name: DeepSeek (BYOK)
    api: https://api.deepseek.com
    key_env: DEEPSEEK_API_KEY
    transport: openai_chat
    models:
      - { id: deepseek-v4-flash, name: "DeepSeek V4 Flash (text, 1M ctx) — DEFAULT" }
      - { id: deepseek-v4-pro, name: "DeepSeek V4 Pro (text, stronger)" }
```

For Anthropic-compatible endpoint (`https://api.deepseek.com/anthropic`):
- Use `transport: anthropic_messages`
- Model mapping: Claude Opus → deepseek-v4-pro, Claude Haiku/Sonnet → deepseek-v4-flash
- Only supports `"type": "text"` content blocks — no image blocks
