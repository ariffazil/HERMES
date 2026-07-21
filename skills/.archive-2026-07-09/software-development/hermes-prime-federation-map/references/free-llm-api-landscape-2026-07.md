# Free LLM API Landscape — July 2026

> Forged 2026-07-20 by Hermes (deepseek-v4-pro). Sources: klymentiev.com (June 2026), tokenmix.ai (July 13 2026), `mnfst/awesome-free-llm-apis` GitHub (canonical list), Grizzly Peak Software (April 2026).

## Federation Miskin Stack (What We Have)

| Tier | Provider | Models | Quota | Card? | Status |
|------|----------|--------|-------|-------|--------|
| 1 | TokenRouter | Smart routing (DeepSeek→MiniMax→GLM→Ollama) | — | No | ✅ LIVE |
| 2 | Groq | 5 models (llama-3.3-70b, qwen3-32b, etc.) | 1,000 RPD, 100K TPD | No | ✅ LIVE |
| 3 | Gemini | 3 models (2.5 Flash, 2.0 Flash/Lite) | 1,500 RPD, 10-30 RPM | No | ✅ LIVE |
| 4 | Cerebras | 3 models (gpt-oss-120b, zai-glm-4.7, gemma-4-31b) | 14.4K RPD, 1M TPD | No | ⚠️ PREPAID $5, expires Aug 20 |
| 5 | SEA-LION | 3 models (qwen-v4-32b, llama-v3.5-70b, gemma-v4-27b) | 10 RPM | No | ✅ LIVE |
| 6 | GLM Free | glm-5.2 (via TokenRouter) | — | No | ⚠️ FREE until Jul 25 2026 |
| 7 | Ollama | qwen2.5-coder:3b | Unlimited local | No | ✅ LIVE |
| 8 | OpenCode Go Free | 5 models (deepseek-v4-flash-free, glm-5.2, etc.) | ~200 req/hr | No | ✅ LIVE |

**Total: 8 free tiers, ~24 free models, RM0/day.**

## What We're MISSING (Ranked by Value)

| # | Provider | Why Worth It | Free Quota | Card? | Models |
|---|----------|-------------|-----------|-------|--------|
| 1 | **Mistral AI** | ~1B tokens/month — most generous by volume | 500K TPM, ~1 RPS | No | Medium 3.5, Small 4, Large 3, Codestral, Pixtral Large |
| 2 | **NVIDIA NIM** | DeepSeek-R1 on free tier, 100+ models | ~40 RPM, no daily cap | No (dev acct) | DeepSeek-R1, Nemotron 120B, Llama 3.1 405B, 90+ more |
| 3 | **SambaNova** | DeepSeek V3.1 on RDU, ultra-fast | 20 RPM, 200K TPD (permanent) | No | DeepSeek-V3.1/3.2, gpt-oss-120b, MiniMax-M2.7 |
| 4 | **Cloudflare AI** | 50+ models, edge inference | 10K neurons/day | No | llama-3.3-70b, gpt-oss-120b, kimi-k2.7-code, 42+ more |
| 5 | **GitHub Models** | GPT-5, GPT-4.1, o4-mini on free | 50-150 RPD | No (GH user) | GPT-5, gpt-4.1, o4-mini, DeepSeek-R1, 35+ more |
| 6 | **Kilo Code** | MiniMax M2.5 free + auto-router | ~200 req/hr | No | grok-code-fast, minimax-m2.5, nemotron-3-super, trinity |
| 7 | **OVHcloud** | Anonymous — no key or signup | 2 RPM per IP | No | Qwen3.5-397B, gpt-oss-120b, Mistral-Small, Qwen3-Coder |

## NOT Worth Adding

| Provider | Why Skip |
|----------|---------|
| OpenAI API | No permanent free tier. Trial credits expire. Card required. |
| Anthropic Claude | $5 trial only. Card required. OSS program (6mo, application). |
| Together AI | No free trial anymore — min $5 purchase. |
| Fireworks AI | One-time $1 credit. Trivial. |
| Aion Labs | 15 RPM, 20K tok/day. Roleplay-only. Tiny. |
| AI21 Labs | $10 one-time, expires 3 months. |
| Cohere | 1,000 calls/month trial key. Non-commercial only. |
| Hugging Face | $0.10/month credit. Trivial. |
| DeepSeek direct | Pay-as-you-go. No permanent free tier. |
| xAI Grok | Trial credits only. Card required. |

## Complete Free Tier Landscape (All Permanent, No Credit Card)

| Provider | Models | Best Model | RPD | TPD | RPM | Context |
|----------|--------|-----------|-----|-----|-----|---------|
| **Google Gemini** | 4 | Gemini 3.5 Flash | 1,500 | — | 15-30 | 1M |
| **Cerebras** | 2-3 | gpt-oss-120b | 14,400 | 1M | 30 | 8K (free cap) |
| **Groq** | 5 | llama-3.3-70b | 1,000 | 100K | 30 | 131K |
| **Mistral** | 6 | Medium 3.5 (128B) | — | 500K TPM | ~1 RPS | 256K |
| **NVIDIA NIM** | 100+ | Nemotron 120B | — | — | ~40 | 262K |
| **SambaNova** | 6 | DeepSeek-V3.1 | 20 | 200K | 20 | 128K |
| **SEA-LION** | 3 | qwen-v4-32b | — | — | 10 | 32K |
| **Cloudflare** | 50+ | llama-3.3-70b | — | 10K neurons | — | 131K |
| **GitHub Models** | 45+ | GPT-5 | 50-150 | — | 10-15 | 200K |
| **OpenRouter** | 22 | qwen3-coder:free | 200 | — | 20 | 1M |
| **Kilo Code** | 6 | minimax-m2.5:free | ~4,800/day | — | ~200/hr | 196K |
| **OVHcloud** | 13+ | Qwen3.5-397B | — | — | 2 | 131K |
| **SiliconFlow** | 2 | Qwen3-8B | — | 60K TPM | 30 | 131K |
| **Ollama Cloud** | 30+ | kimi-k2:1t-cloud | session-based | session | — | 128K |
| **Ollama Local** | unlimited | qwen2.5-coder:3b | ∞ | ∞ | ∞ | hardware |

## RM0 Cascade (Canonical)

```
TokenRouter → MiniMax → MiMo → Groq → Gemini → Cerebras → SEA-LION → Ollama → HOLD
    0            1        2       3       4         5          6         7       99
```

Encoded in AGENTMODELMAP.json as `rm0-general-reasoning`, strategy: sequential.

## Monitoring Sources (for monthly cron)

1. **GitHub `mnfst/awesome-free-llm-apis`** — canonical list, actively maintained. Diff for new entries monthly.
2. **Google AI Studio pricing** — `ai.google.dev` — Gemini free tier quotas change without notice.
3. **Groq console limits** — `console.groq.com/settings/limits` — rate limits per model.
4. **Cerebras dashboard** — `cloud.cerebras.ai` — model roster and credit balance.
5. **Mistral La Plateforme** — `console.mistral.ai` — Experiment plan status.

**Cadence:** Monthly is right. Weekly overkill — real changes happen every 4-8 weeks.

## Key Rate Limit Gotchas

- **Groq:** Token/day (100K) binds 10× before requests/day (1K). 100 calls/day realistic, not 1,000.
- **Cerebras:** 8K context cap on free tier (128K on paid). Long-context tasks fail silently.
- **OpenRouter:** 50 RPD on free models unless $10+ credits purchased → then 1,000 RPD.
- **Gemini:** Exact limits vary by project — check AI Studio, not blog posts.
- **Mistral:** Limits are workspace-specific, not one public number. Check dashboard.
