# Free LLM API Landscape — July 2026

> Deep research on permanent-free and trial-credit LLM inference providers.
> Sources: klymentiev.com, tokenmix.ai, cheahjs/free-llm-api-resources, costbench.com.
> Research date: 2026-07-20.

## Permanent Free Tiers (no credit card)

| Provider | Models | Free Quota | Card? | Best Use |
|----------|--------|-----------|-------|----------|
| **Google Gemini** | Gemini 2.5/3 Flash, Flash-Lite | 1,500 RPD, 10-15 RPM, 250K TPM | No | General baseline, multimodal |
| **Groq** | Llama 3.1 8B/70B, Mixtral, Gemma 2 | 30 RPM, 14.4K RPD (8B), 100K TPD (70B) | No | Speed (560+ t/s) |
| **Cerebras** | gpt-oss-120b, GLM-4.7, Gemma-4-31b | 30 RPM, 14.4K RPD, 1M TPD | No | Volume, long context |
| **SEA-LION** | Qwen v4 32B, Llama v3 70B, Gemma v4 27B | 10 RPM (trial key) | No* | BM/Malay native, SG jurisdiction |
| **Cloudflare Workers AI** | 25+ models (Kimi, Nemotron, GLM, Qwen) | 10K neurons/day | No | Edge/serverless |
| **OpenRouter** | 28+ free models via aggregator | 20 RPM, 50 RPD (1K after $10 topup) | No | Single key, many models |

*SEA-LION: trial key, no stated expiry, 10 RPM.

## Trial Credits / Evaluation

| Provider | Credit | Expiry | Card? | Models |
|----------|--------|--------|-------|--------|
| SambaNova | $5 | 30 days | No | Fast open-model eval |
| AI21 Labs | $10 | 3 months | No | Jamba family |
| Cohere | Trial key | 1K calls/mo | No | Chat, Embed, Rerank (strong RAG) |
| Mistral | Free mode | Workspace limits | No | EU-hosted, Codestral |
| HuggingFace | $0.10/mo | Monthly | No | Open model sampling |
| Vercel AI Gateway | $5/mo | Monthly (recurring) | No | Gateway credit |
| Fireworks | $1 | One-time | No | Serverless eval |
| DeepSeek | 5M tokens (unconfirmed) | Account-dependent | Yes | Cheap reasoning |

## Not Free (production only)

- **OpenAI** — No permanent free tier. Old $5 trial inconsistent.
- **Anthropic Claude** — ~$5 starter credit. OSS program: $1200 for 6mo (10K spots).
- **Together AI** — No free trial. Min $5 purchase.

## Rate Limit Reality

Headline request limits rarely bind first. Tokens/day is the real cap:

| Model | Requests/Day | Tokens/Day | Real Calls/Day (1K tok) | Binding Limit |
|-------|-------------|------------|------------------------|---------------|
| Groq Llama 70B | 1,000 | 100K | ~100 | TPD |
| Groq Llama 8B | 14,400 | 500K | ~500 | TPD for long prompts |
| Cerebras gpt-oss-120b | 14,400 | 1M | ~1,000 | TPD |
| Gemini Flash | 1,500 | 250K TPM | ~1,500 | RPD (generous) |

## Stacking Strategy (RM0)

1. **Google Gemini** — Default route, most generous, multimodal
2. **Groq** — Real-time/latency-sensitive
3. **Cerebras** — Volume/long-context overflow
4. **SEA-LION** — BM/Malay-native tasks, ASEAN data
5. **Ollama** — Blind survival knife (local)

90% of production agent calls can route through free tiers. Only top 10% of high-stakes calls need paid models.

## Sources

- klymentiev.com/blog/free-llm-api (June 2026)
- tokenmix.ai/blog/free-llm-api (July 13, 2026)
- github.com/cheahjs/free-llm-api-resources
- costbench.com/best/best-llm-api-with-free-tier/
- freellm.net/models/ (353+ model directory)
