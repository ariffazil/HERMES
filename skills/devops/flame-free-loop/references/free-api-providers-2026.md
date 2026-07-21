# Free LLM API Providers — July 2026 Landscape

Research compiled 2026-07-20 from klymentiev.com, tokenmix.ai, GitHub `mnfst/awesome-free-llm-apis`, and Grizzly Peak Software.

## Current Federation Stack (all RM0)

| Tier | Provider | Models | Limit | Card? | Status |
|------|----------|--------|-------|-------|--------|
| 1 | TokenRouter | deepseek-v4-pro, deepseek-v4-flash, glm-5.2, minimax-m3, mimo | Smart routing | No | ✅ Live |
| 2 | Groq | llama-3.1-8b-instant, llama-3.3-70b-versatile, openai/gpt-oss-120b | 1,000 RPD, 30 RPM | No | ✅ Live |
| 3 | SEA-LION | Qwen v4 32B, Llama v3 70B, Gemma v4 27B | 10 req/min | No | ✅ Live |
| 4 | Gemini | gemini-2.5-flash | 1,500 req/day | No | ✅ Live |
| 5 | Cerebras | gpt-oss-120b, gemma-4-31b, zai-glm-4.7 | 14,400 RPD, 1M TPD | No | ✅ Live ($5 credit, expires Aug 20) |
| 6 | OpenCode Go | deepseek-v4-flash-free, north-mini-code-free, glm-5.2, nemotron-3-ultra-free | 200 req/hr | No | ✅ Live |
| 7 | Ollama | qwen2.5-coder:3b | Local only | No | ✅ Live |

## Providers NOT Yet Wired (Ranked by Value)

### 1. Google Gemini (Additional Models)
- **Status**: Gemini 2.5 Flash already wired. Missing: Gemini 3.5 Flash, 2.5 Pro, Flash-Lite.
- **Value**: HIGH. Multimodal (text+image+audio+video). 1M context. Free tier: 1,500 req/day, 10-30 RPM.
- **Effort**: Low — same key, just add model entries.
- **Note**: Gemini Flash Lite degraded in testing (SHADOW-GEM-002, 12s timeout). Likely rate-limited or removed.

### 2. Mistral AI — MOST GENEROUS BY VOLUME
- **Free tier**: "Experiment" plan, ~1B tokens/month, 500K TPM. No credit card.
- **Models**: Mistral Medium 3.5 (128B), Small 4, Large 3, Codestral, Pixtral Large, Nemo (12B).
- **Value**: HIGH. Most generous free tier in existence by token volume. Codestral for code.
- **Effort**: Medium — sign up at console.mistral.ai, get key, add provider config.

### 3. NVIDIA NIM
- **Free tier**: ~40 RPM, 100+ models. Free with NVIDIA Developer Program. No daily token cap.
- **Models**: DeepSeek-R1, Nemotron Super 120B, Llama 3.1 405B, Qwen 2.5 72B, Gemma 4 31B, Mistral Large 2, MiniMax M2.7.
- **Value**: MEDIUM-HIGH. DeepSeek-R1 on free tier is compelling. 100+ model variety.
- **Effort**: Low — dev account at build.nvidia.com, get key.

### 4. SambaNova
- **Free tier**: Permanent: 20 RPM, 200K TPD per model. No credit card.
- **Models**: DeepSeek-V3.1, DeepSeek-V3.2 (Preview), Llama 3.3 70B, gpt-oss-120b, MiniMax-M2.7, Gemma 4 31B.
- **Value**: MEDIUM. DeepSeek V3.1/3.2 available on RDU hardware. Ultra-fast.
- **Effort**: Low — sign up at cloud.sambanova.ai.

### 5. Cloudflare Workers AI
- **Free tier**: 10,000 neurons/day. 50+ models. Edge inference.
- **Value**: LOW-MEDIUM. Neuron accounting is opaque. Good for edge tasks only.
- **Effort**: Medium — requires Cloudflare account + Workers setup.

### 6. OVHcloud AI Endpoints
- **Free tier**: Anonymous (no key, no signup!). 2 RPM per IP per model. 20+ open-weight models. EU-hosted.
- **Models**: Qwen3.5-397B-A17B, gpt-oss-120b/20b, Llama 3.3 70B, Qwen3.6-27B, Mistral Small 3.2, etc.
- **Value**: LOW. 2 RPM is tiny. But zero friction — no signup at all.
- **Effort**: Zero. Just use the endpoint.

## NOT Worth Adding

| Provider | Why |
|----------|-----|
| OpenAI API | No permanent free tier. Trial credits expire. Card required. |
| Anthropic Claude | $5 trial only. Card required. OSS program needs application + 6mo cap. |
| Together AI | No free trial anymore. Min $5 purchase. |
| Fireworks AI | One-time $1 credit. |
| AI21 Labs | $10 credit, expires 3 months. |
| Aion Labs | 15 RPM, 20K tok/day. Roleplay-only. |
| Hugging Face | $0.10/month. Trivial. |

## Monitoring Strategy

- **Cron**: Monthly check of `mnfst/awesome-free-llm-apis` GitHub repo + Google AI Studio pricing + Groq rate limits page.
- **Trigger**: New free tier appears, existing tier changes limits, or tier expires.
- **Action**: Evaluate, add to fleet if valuable, update this reference.

## Sources

- [klymentiev.com — Free LLM APIs 2026](https://klymentiev.com/blog/free-llm-api) (updated June 2026)
- [tokenmix.ai — 15 Best Free LLM APIs](https://tokenmix.ai/blog/free-llm-api) (updated July 13 2026)
- [GitHub mnfst/awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis) (canonical list)
- [Grizzly Peak — Every AI API Free Tier 2026](https://www.grizzlypeaksoftware.com/articles/p/every-ai-api-with-a-free-tier-in-2026-the-developers-cheat-sheet-jl33ach0)
