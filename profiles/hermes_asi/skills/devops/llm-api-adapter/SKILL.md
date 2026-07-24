---
name: llm-api-adapter
description: "Build thin translation proxies between incompatible LLM API formats (Chat Completions ↔ Responses API, etc.). For custom providers, external routing gateways, and protocol bridges."
version: 1.1.0
author: Hermes Agent
tags: [llm, api, adapter, proxy, gateway, protocol, translation, routing]
triggers:
  - "integrate [gateway/router] with Hermes"
  - "connect [provider] to Hermes"
  - "build adapter for [API format]"
  - "Chat Completions to Responses API"
  - "protocol translation proxy"
  - "custom provider adapter"
  - "TokenRouter integration"
---

# LLM API Adapter

Build thin, reversible (ΔS ≤ 0) translation proxies between incompatible LLM API formats. The adapter sits between Hermes (which speaks OpenAI Chat Completions) and any provider/gateway that uses a different format.

## When to Use

- Integrating an external LLM routing gateway (TokenRouter, custom router) that uses non-standard formats
- Bridging Chat Completions API ↔ OpenAI Responses API
- Injecting BYOK provider keys that Hermes can't natively pass as headers
- Any situation where the provider and Hermes speak different API dialects

## When NOT to Use

- Provider already has native Chat Completions support → use Hermes `custom` provider directly
- Provider is on Hermes's built-in provider list (OpenRouter, Anthropic, DeepSeek, etc.) → use native config
- Simple API key change → just update config.yaml

## Architecture Pattern

```
Hermes Agent → localhost:9999/v1/chat/completions → Adapter → Target API
   (OpenAI format)         (translate)              (inject BYOK)   (native format)
```

Key properties:
- **Stateless** — no database, no sessions, no persistent state
- **Reversible (F1)** — kill the process, point Hermes back to native provider, zero cleanup
- **Low entropy (ΔS ≤ 0)** — one file, ~50 lines, standard libraries
- **BYOK sovereignty** — provider keys pulled from environment, never stored in Hermes config or logs

## Procedure

### 1. Identify the Format Gap

| Hermes sends | Target expects | Translation needed |
|---|---|---|
| `messages: [{role, content}]` | `input: "string"` | Flatten messages array |
| `model: "gpt-4o"` | `model: "auto:balance"` or `router_provider: "openai"` | Map model names |
| `stream: true` | `stream: true` (usually same) | Pass through |
| `tools: [...]` | `tools: [...]` (varies) | May need reshaping |

### 2. Build the Adapter — with required headers

Use FastAPI + httpx. **CRITICAL (2026-07-20):** Some gateways (TokenRouter) require `Accept: application/json` + `User-Agent: Tokenrouter/Python 1.2.1` headers. Without them, the request crashes before auth — returning 500 (HTML) instead of 401/403. Always include both. The full template is at `templates/tokenrouter_adapter.py`.

### 3. Wire into Hermes

```bash
# Start adapter with provider keys
TOKENROUTER_URL=https://api.tokenrouter.io/v1/responses \
TOKENROUTER_API_KEY=sk-... \
DEEPSEEK_API_KEY=sk-... \
ANTHROPIC_API_KEY=sk-ant-... \
python3 tokenrouter_adapter.py &

# Configure Hermes custom provider
hermes config set model.provider "custom:adapter"
hermes config set model.base_url "http://127.0.0.1:9999/v1"
hermes config set model.api_key "none"
hermes config set model.default "auto:balance"
```

### 4. Verify

```bash
curl -s http://127.0.0.1:9999/health
curl -s http://127.0.0.1:9999/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"auto:balance","messages":[{"role":"user","content":"Say OK"}]}'
```

## Pitfalls

- **⚠️ ADAPTER DELETED — unnecessary once `.com` Chat Completions discovered (2026-07-20):** TokenRouter operates TWO API domains: `api.tokenrouter.com` (Chat Completions, Hermes-compatible) and `api.tokenrouter.io` (Responses API only). We built a fully working adapter, debugged auth for 3+ hours, then discovered `.com` had native `/v1/chat/completions` returning 200 the whole time. The adapter was deleted — maximum entropy reduction. **Before building ANY adapter, probe ALL known provider domains for `/v1/chat/completions`.** The adapter is the backup path, not the first choice. Two minutes of probing saves hours of building.

- **500 from curl but 401 from SDK = header problem (2026-07-20):** TokenRouter crashes before auth if `Accept` and `User-Agent` headers are missing. The SDK sends these automatically; raw curl/httpx does NOT. Always include `Accept: application/json` + `User-Agent: Tokenrouter/Python 1.2.1` in the adapter's forwarded request.
- **Response format assumption:** Always print raw response once to confirm the output field name (`output` vs `response` vs `text` vs `choices[0].message.content`). Different gateways use different schemas.
- **Multimodal content:** When messages contain image URLs, extract only the text parts. Image URLs need special handling if the target supports vision.
- **Streaming:** SSE streaming requires chunk-by-chunk translation — more complex. Start with non-streaming.
- **Tool calls:** Tool/function definitions may need reshaping to match the target's tool format.
- **500 ≠ auth error:** If target returns 500 with CORRECT headers, issue is upstream (missing provider keys, server bug).
- **401 vs 500 on same endpoint:** Management key → 401. Model key + no providers → 500. Different server layers intercept.
- **No programmatic provider management:** TokenRouter and similar gateways often have console-only provider setup. BYOK headers are the workaround. Personal Management Keys (sk-FU... prefix) are web console only — not model-request keys.
- **Automated browser login blocked:** Google and GitHub OAuth block headless browsers. User must add provider keys via web console manually (2 clicks) or provide email+password for native login.
- **Key disabled/inactive (401 from .com):** `api.tokenrouter.com` returns Chinese `"该令牌状态不可用"` when key exists but is inactive. Go to Console → API Keys → toggle Enabled ON → Save. The `.io` domain only says "Unauthenticated" — less useful for diagnosis.
- **`.com` better for debugging:** `api.tokenrouter.com` has Chinese-language error messages that are more descriptive than `.io`'s generic English errors. Use `.com` during integration, switch to `.io` for production.
- **Adapter must NOT add `auto:` prefix to `provider/model` format:** Models with `/` (like `anthropic/claude-sonnet-4`) already have a routing prefix. Only add `auto:` when model has no `:` AND no `/`.
- **TokenRouter `output` is a nested array, not a string:** Response format is `{"output":[{"type":"message","content":[{"type":"output_text","text":"..."}]}]}`. Parse by walking `output[] → type=message → content[] → type=output_text → text`. Don't use `.get("output")` directly as a string.
- **113 models listed, only ~4 have channels (2026-07-20):** `/v1/models` returns full catalog. But only models with an active provider channel return 200 — all others return 500 or 503. Test models before advertising them as available.
- **Working models (2026-07-20):** `anthropic/claude-sonnet-4`, `google/gemini-3-flash-preview`, `qwen/qwen3.7-max`, `x-ai/grok-4.20-beta`.
- **403 \"no access\" → key model restriction:** API key has Allowed Models set to something restrictive. Fix: Console → API Keys → [key] → Allowed Models → leave BLANK (empty = allow all).
- **503 \"no channel for model X under group default (distributor)\":** TokenRouter's distributor platform doesn't have upstream provider connections for this model. NOT fixable from user console — TokenRouter service issue.

## Support Files

- `references/tokenrouter-specifics.md` — TokenRouter quirks: SDK internals, auth formats, endpoints, provider config, leaderboard, 500 dual-cause diagnosis
- `templates/tokenrouter_adapter.py` — Fully working adapter script with BYOK header injection and correct TokenRouter headers
