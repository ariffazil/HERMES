# OpenRouter Live Probe — 2026-07-24

> **Forged:** 2026-07-24 during deep research session.
> **Source:** `curl -s https://openrouter.ai/api/v1/models` + docs + blog cross-reference.
> **Purpose:** Session-specific detail for the provider-routing-zen skill. Not a SOT — probe again before acting.

## Catalog Summary

| Dimension | Value |
|-----------|-------|
| Total models | 343 |
| Providers | 58 |
| Free models (RM0) | ~50 |
| Vision/multimodal | 181 |
| Reasoning (thinking) | 70+ |
| 1M+ context paid | 15+ |
| Prompt-cache supported | 182 |

## Provider Counts

| Provider | Models | Free | Notes |
|----------|--------|------|-------|
| openai | 67 | 1 | GPT-5.x series dominates |
| qwen | 47 | 12 | Qwen 3.5/3.6 series, strong free tier |
| google | 30 | 3 | Gemini 3.x, Gemma 4 free |
| mistralai | 19 | 1 | EU ZDR-safe |
| anthropic | 15 | 0 | Claude 4.x Opus/Sonnet/Haiku |
| z-ai | 12 | 1 | GLM-5.2, ZDR-safe |
| deepseek | 11 | 1 | V4 Pro + Flash, lowest-cost frontier |
| nvidia | 10 | 3 | Nemotron free models |
| meta-llama | 8 | 1 | Llama 4 Scout free, ZDR-safe |
| minimax | 8 | 0 | **SHADOW-MM-001** — silent MY governance censorship |
| moonshotai | 7 | 0 | Kimi K2/K3 series |
| xiaomi | 5 | 0 | MiMo V2.5, 1M context, ZDR-safe |
| x-ai | 5 | 0 | Grok-3/4, US ZDR |
| cohere | 5 | 0 | Command R |

## OpenRouter-Specific Primitives

| Primitive | What it does |
|-----------|-------------|
| `openrouter/auto-beta` | Task-classified routing across community-curated models. Uses spend-share weighting (not NotDiamond as of mid-2026). Default cqt=9. |
| `openrouter/free` | RM0 last-resort fallback. Routes to free-tier providers. |
| `cost_quality_tradeoff` (0-10) | Per-request cost/quality dial. 0=max quality, 10=cheapest. |
| `session_id` / `x-session-id` | 5-min session stickiness — pins model + provider, skips classifier on follow-ups. |
| `provider` object | Override: `order`, `allow_fallbacks`, `sort`, `only`, `ignore`, `quantizations`, `data_collection`, `zdr`, `max_price`, `preferred_min_throughput`, `preferred_max_latency`, `require_parameters` |
| `allowed_models` (wildcard) | Restrict pool to vetted set. Supports `anthropic/*`, `deepseek/*`, etc. |
| `cache_control: {type:"ephemeral"}` | Prompt caching support (Anthropic models). |
| Guardrails (Management API) | Budget caps, ZDR, model allowlist, prompt-injection detection, PII redaction, DLP. |
| `zdr: true` parameter | Per-request Zero Data Retention. |
| MCP server | `mcp.openrouter.ai/mcp` — live model discovery + credit balance. Needs OAuth approval. |

## Auto-Router Behaviour (2026-07-24 Verified)

- The auto-router (`openrouter/auto-beta`) uses **community spend share** to rank models per task class — NOT NotDiamond as earlier docs stated. Free models with low spend share get deprioritised even if they can handle the task.
- Default `cost_quality_tradeoff` = 9 (strongly RM-leaning).
- Response `model` field reveals which model actually served — trust this for auditing, not assumptions.
- Session stickiness: pass `x-session-id` header; pins for 5min inactivity.

**Important caveat:** The auto-router can route MY governance topics through MiniMax M3 if it has dominant community spend share in that task class (SHADOW-MM-001). Always exclude `minimax/*` from `allowed_models` and route sovereign topics direct to DeepSeek.

## Key Free Models for FLAME

| Model | Context | Provider | Speed |
|-------|---------|----------|-------|
| `qwen/qwen-3.6-plus-preview` | 128K | qwen | Good |
| `deepseek/deepseek-chat:free` | 128K | deepseek | Good |
| `google/gemma-4-31b-it:free` | 256K | google | Fast |
| `nvidia/nemotron-3-super-120b-a12b:free` | 1M | nvidia | Medium |
| `meta-llama/llama-4-scout:free` | 1.3M | meta-llama | Medium |
| `openai/gpt-oss-120b` | 131K | openai | Fast (suppressed content safety) |
| `poolside/laguna-s-2.1:free` | 262K | poolside | Medium |

## Reasoning Models (mandatory/default-enabled)

70+ models with mandatory or default-enabled reasoning. Cheapest with reasoning:
- `poolside/laguna-s-2.1:free` — RM0
- `deepseek/deepseek-r1:free` — RM0
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — RM0
- `openai/o3-mini` — $1.10/$4.40
- `deepseek/deepseek-r1` — $2.19/$2.19

## Observation: Reasoning Token Transparency

Per Feb 2026 community audit of 5 LLMs via OpenRouter:
- Some models silently drop reasoning tokens when used with structured output or tool calling
- Kimi K2.5: safest for universal reasoning visibility
- Claude Sonnet 4.x: opt-in reasoning, reliable when enabled
- GPT-5.x: reasoning transparency varies
- **Audit your specific model+structured+tool combo before relying on reasoning_details**

## Provider Slug Quirks

- Base slug (`"anthropic"`) matches every variant. Full slug (`"deepinfra/turbo"`) pins a single endpoint.
- Provider routing default: cheapest reliable, inverse-square of price weighted. 30-second outage window.
- `:nitro` suffix = route for speed (`provider.sort: "throughput"`)
- `:floor` suffix = route for cost (`provider.sort: "price"`)
- Requests with **tools** route through Auto Exacto (quality-first tool-call routing), not price weighting. Force `:floor` or `provider.sort: "price"` to override.
