---
name: federation-model-routing
description: "Resolve model identity through proxy chains, diagnose context window gaps, and select the right model for each federation role. Use when the gateway reports wrong context limits, the model name doesn't match the real upstream, a proxy alias resolves to unexpected behavior, or model selection needs to match a role's requirements (SOUL=conversational, JUDGE=frontier reasoning, HANDS=coding)."
tags: [model, routing, litellm, proxy, context-window, model-selection]
---

# Federation Model Routing

The arifOS federation routes models through a LiteLLM proxy with custom aliases. Each gateway role (SOUL/JUDGE/HANDS) has different model needs, and the proxy chain adds layers where config can lie. Same doctrine as gateway identity: **config files lie; only live probes are truth.**

## The resolution chain

```
gateway config.yaml: model.default = "hermes-asi"
  → provider: openai-api (connects to LiteLLM proxy via socat tunnel)
    → LiteLLM proxy (100.64.0.2:4000, Tailscale)
      → alias "hermes-asi" → openai/mimo-v2.5
        → upstream: https://token-plan-sgp.xiaomimimo.com/v1 (Xiaomi token plan)
```

Every layer can diverge from what the layer above declares. The only truth is the upstream provider's actual response.

## Role-based model requirements

| Role | Function | Needs | Current | Ideal |
|---|---|---|---|---|
| **SOUL** (Hermes) | Human-language bridge, conversation, delegation | Fast response, strong tool calling, long context, conversational BM, cost-effective at volume | `hermes-asi` → MiMo V2.5 (1M real, 250k reported) | DeepSeek V4 Flash (1M, fast, strong reasoning) |
| **JUDGE** (arifOS 888) | Constitutional deliberation, 666_JUDGE, 999_SEAL | Frontier reasoning, zero censorship, longest context | Not probed | DeepSeek V4 Pro (1M, MIT, 384K output) |
| **HANDS** (A-FORGE) | Code execution, file mutation, builds | Coding accuracy, structured output, tool calling | Not probed | DeepSeek V4 Flash or MiMo V2.5 Pro |
| **GUTS** (OpenClaw) | System metabolism, routing, orchestration | Fast, reliable, low latency | Not probed | Qwen 3.6 Flash or MiMo V2.5 |

## Probe the model resolution chain

```bash
# 1. What does the config say?
grep -A2 "^model:" /usr/local/lib/hermes-agent/config.yaml

# 2. What models does the proxy expose? (needs auth)
source /root/.secrets/kunci-mas.env
curl -s http://127.0.0.1:4000/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY" | jq '.data[].id'

# 3. What does a custom alias ACTUALLY resolve to?
curl -s "http://127.0.0.1:4000/model/info" -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  | jq '.data[] | select(.model_name == "<alias>")'

# 4. Check the upstream model's REAL context limit from models_dev_cache
python3 -c "
import json
with open('/usr/local/lib/hermes-agent/models_dev_cache.json') as f:
    data = json.load(f)
for p in data.values():
    if isinstance(p, dict) and 'models' in p:
        for mid, m in p['models'].items():
            if isinstance(m, dict) and '<model-id>' in mid:
                print(f'{mid}: ctx={m.get(\"limit\",{}).get(\"context\",\"?\")} out={m.get(\"limit\",{}).get(\"output\",\"?\")}')
"

# 5. Verify the upstream is responding correctly
curl -s "https://token-plan-sgp.xiaomimimo.com/v1/models" \
  -H "Authorization: Bearer <upstream-key>" | jq '.data[] | select(.id | contains("mimo"))'
```

## The context window gap

When LiteLLM proxy custom aliases have `max_input_tokens: null` and `max_output_tokens: null` in their `model_info`, the gateway falls back to a default cap (typically 250k). The real model may support much more.

**Root cause:** LiteLLM doesn't auto-detect context limits for custom aliases pointing to non-standard endpoints. Major provider models (OpenAI, Anthropic) have auto-detected limits; custom aliases to token-plan endpoints do not.

**Verification:** Compare the proxy's reported limit vs the `models_dev_cache.json` entry for the same model via other providers. If the cache shows 1M but the proxy says null, the proxy is the bottleneck.

## Fix options (in priority order)

1. **Fix LiteLLM config on the remote** — add `max_input_tokens` / `max_output_tokens` to each model's `model_info`. This fixes all aliases at once and is the canonical fix.
2. **Override in Hermes config** — set `context_window` in the provider config to bypass the null.
3. **Change the alias** to a model whose limits the proxy already knows (major provider models auto-detect).

## MODEL_TIERS.json (canonical tier definitions)

The federation's model tier registry lives at `/root/AAA/registries/models/MODEL_TIERS.json`. It defines 4 tiers:

| Tier | Label | Use when | Models |
|---|---|---|---|
| T1 | Frontier Reasoning | Constitutional deliberation, 666_JUDGE, 999_SEAL, complex coding | deepseek-v4-pro, kimi-k3, glm-5.2, mimo-v2.5-pro |
| T2 | Fast Coding | Daily coding, agent workflows, high-volume tasks | deepseek-v4-flash, mimo-v2.5-pro-ultraspeed, gpt-5.6-sol, qwen3.7-plus |
| T3 | Recovery | Emergency fallback when T1/T2 are down | gemini-2.5-flash, qwen3.6-flash |
| T4 | Local | Offline/sandbox, no API dependency | ollama/qwen2.5-coder:3b |

**Iron Rule from MODEL_TIERS:** "Never route 666_JUDGE/999_SEAL through anything but DeepSeek V4 Pro direct."

## Pitfalls

- **Do not assume `model.default` in config.yaml is a real model name.** It's a LiteLLM alias. Always trace through `/model/info` to find the actual upstream.
- **Null `model_info` ≠ "no limit".** The proxy returning `max_tokens: null` means "I don't know", not "unlimited". The gateway then applies its own default cap.
- **Same model via different providers can have different context limits.** MiMo V2.5 via Xiaomi token plan = 1M; via HuggingFace = 262k. The provider matters.
- **Cost varies by provider too.** Check `models_dev_cache.json` cost fields — the same model can be 10x cheaper via a token plan vs API credits.
- **When `web_search`/`web_extract` are unconfigured, use browser fallback.** Navigate to the target URL with `browser_navigate`, then extract full article text via `browser_console` with `document.querySelector('article').innerText` (or `main`/`div.content` depending on site structure). This is slower but reliable for pulling research from Anthropic blog, Microsoft Research, LiteLLM docs, arXiv, etc. Do NOT get stuck in retry loops on missing tools — switch to browser immediately after one failure.

## Current resolution map (2026-08-05)

| Alias | Resolves to | Upstream | Real context | Gateway sees |
|---|---|---|---|---|
| `hermes-asi` | `openai/mimo-v2.5` | Xiaomi token plan SGP | 1,048,576 | 250k (default) |
| `codex` | `openai/deepseek-v4-flash` | (multiple) | 1,000,000 | 250k (default) |
| `opencode` | `openai/deepseek-v4-flash` / `mimo-v2.5-pro` / `MiniMax-M3` | (multiple) | varies | 250k (default) |
| `asi-555` | `openai/qwen3.6-flash` / `mimo-v2.5-pro` / `MiniMax-M3` | (multiple) | varies | 250k (default) |
| `agi-333` | `openai/deepseek-v4-pro` / `mimo-v2.5-pro` / `MiniMax-M3` | (multiple) | varies | 250k (default) |
| `apex-888` | `openai/MiniMax-M3` / `deepseek-v4-pro` | (multiple) | varies | 250k (default) |

All aliases have null limits → all hit the same default cap regardless of real capability.

## Broader federation coordination patterns

Beyond model routing, the federation needs coordination architecture. See `references/federation-orchestration-patterns.md` for the full 10-pattern framework (orchestrator-worker ledger, tiered memory, circuit breakers, structured handoffs, evaluator-optimizer loops, ReAct+Reflexion, etc.) with implementation schemas and priority ordering.

## Reference files

- `references/model-resolution-2026-08-05.md` — specific probe outputs, the resolution chain, and the full model info dump from the LiteLLM proxy.
- `references/federation-orchestration-patterns.md` — 10 orchestration patterns for Hermes×OpenClaw×OpenCode federation coordination, sourced from Anthropic, Magentic-One, and LiteLLM docs (2024-2025).
