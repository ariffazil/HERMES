---
name: hermes-tokenrouter-guide
description: "How Hermes uses TokenRouter — model selection, auto-routing, cost strategy, FREE tier. Load when Hermes needs to choose an LLM model or when asked about TokenRouter usage."
---

# 🪙 TokenRouter Guide for Hermes

> **Your config is already wired.** TokenRouter is provider `tokenrouter` in `/root/HERMES/config.yaml`.
> **SOT:** 2026-07-20 | **Balance:** $59.96 + $25.61 vouchers | **GLM 5.2:** FREE until July 25

---

## ⚡ 5-DAY PULUN WINDOW (July 20–25, 2026)

**GLM 5.2 FREE tier is active NOW. Expires July 25. 120 hours remaining.**

### Containment Paradox (F2)

US Entity List + chip restrictions forced Zhipu AI onto Huawei Ascend silicon → architectural independence from Nvidia → fully open MIT weights with no regional restrictions → uncontrollable open-source release → now operating inside the sovereign federation it was meant to exclude. **The containment strategy inverted itself.** The geopolitical wall created the asset.

### Tactical: Pulun Habis

| Window | Strategy |
|---|---|
| **Now → Jul 25** | `z-ai/glm-5.2-free` as PRIMARY for background/volume tasks. Exploit 1M context, zero cost. |
| **Jul 25 → onward** | Falls back to `z-ai/glm-5.2` (paid, $1.20/$4.10 MTok) or `MiniMax-M3` |

**Context saturation:** Push entire repos, sync logs, dense documentation into single 1M-token prompts.
**Token discipline:** GLM 5.2 generates long execution traces. Structure prompts for CONCISE output to maximize throughput before route closure.

### Operational Fallback Chain (5-day window)

```yaml
# PULUN MODE — July 20-25
fallback_providers:
  - provider: tokenrouter
    model: z-ai/glm-5.2-free         # Tier 1 — FREE, pulun habis
  - provider: tokenrouter
    model: MiniMax-M3                 # Tier 2
  - provider: ollama
    model: qwen2.5-coder:3b           # Tier 3 — local sovereign
```

Cron `c4d4b95ed026` fires 8am July 25 — detects 402/403, swaps chain back to paid mode.

---

## Quick Start — already configured

Standard fallback chain in `config.yaml`:
```yaml
fallback_providers:
  - provider: tokenrouter
    model: deepseek/deepseek-v4-pro   # Tier 1
  - provider: tokenrouter
    model: MiniMax-M3                 # Tier 2
  - provider: tokenrouter
    model: z-ai/glm-5.2               # Tier 3 — FREE
```

TokenRouter is called automatically when your primary (deepseek) fails or rate-limits. No manual action needed.

---

## How to call TokenRouter directly (when you want a specific model)

TokenRouter is OpenAI-compatible. From any code or curl:

```bash
source /root/.secrets/vault.env

curl -s https://api.tokenrouter.com/v1/chat/completions \
  -H "Authorization: Bearer $TOKENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek/deepseek-v4-pro",
    "messages": [{"role": "user", "content": "Your task here"}],
    "max_tokens": 1000
  }'
```

---

## Model Selection — which model for which task

| Task | Best Model | Why | Cost |
|------|-----------|-----|------|
| **Geology dossiers** | `deepseek/deepseek-v4-pro` | High reasoning, 1M context | $$ |
| **Prospect evaluation** | `deepseek/deepseek-v4-pro` | Needs deep domain knowledge | $$ |
| **Code review/PR** | `MiniMax-M3` or `deepseek/deepseek-v4-flash` | Fast, good code understanding | $ |
| **Daily briefing** | `z-ai/glm-5.2` | **FREE until July 25** | FREE |
| **Memory compression** | `z-ai/glm-5.2` | Simple summarization, cheap | FREE |
| **Health summary** | `z-ai/glm-5.2` | 4-sentence output, no need for heavy model | FREE |
| **Quick Q&A** | `deepseek/deepseek-v4-flash` | Fastest, cheapest paid option | $ |
| **Multimodal (images)** | `MiniMax-M3` or `xiaomi/mimo-v2.5` | Vision-capable | $$ |
| **Sovereign decisions** | `deepseek/deepseek-v4-pro` | Never cheap out on governance | $$ |

---

## Auto-Routing (let TokenRouter pick)

Instead of specifying a model, use auto-routing:

```json
{"model": "auto:balance"}   // Best overall (default)
{"model": "auto:cost"}      // Cheapest that can handle the task
{"model": "auto:quality"}   // Best available model
{"model": "auto:latency"}   // Fastest response
```

For background tasks (memory bridge, health checks): `auto:cost`
For Arif-facing responses: `auto:quality` or explicit `deepseek/deepseek-v4-pro`

---

## GLM 5.2 FREE Tier (until July 25, 2026)

- Model ID: `z-ai/glm-5.2`
- Cost: ZERO on shared gateway
- Best for: summarization, simple Q&A, memory compression, health narratives
- Limitations: shared capacity, variable latency, no guaranteed availability
- Full 1M context also available at 40% list price on Full Context Tier

**Strategy:** Route ALL background synthesis pipelines through GLM 5.2 FREE. Save the paid balance for Arif-facing responses and high-cognitive geological work.

---

## 95 Text Models Available

Key ones to know:
- `deepseek/deepseek-v4-pro` — your primary (best reasoning)
- `deepseek/deepseek-v4-flash` — fast/cheap DeepSeek
- `MiniMax-M3` — multimodal, 1M context
- `z-ai/glm-5.2` — FREE tier ⭐
- `xiaomi/mimo-v2.5-pro` — strong coding specialist
- `openai/gpt-5.6-sol` — Codex's primary, available as backup
- `moonshotai/kimi-k3` — latest Kimi
- `anthropic/claude-opus-4.8` — Claude family (premium)
- `google/gemini-3.5-flash` — Gemini for Antigravity-style tasks

---

## Cost Strategy

```
FREE (GLM 5.2)     → background tasks, memory, health checks
CHEAP (v4-flash)    → quick Q&A, code review, simple tasks
PREMIUM (v4-pro)    → geology, sovereign decisions, Arif-facing output
```

Your config already does this via the 3-tier fallback chain. TokenRouter auto-bills to one account — no per-provider tracking needed.
