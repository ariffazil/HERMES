# SOT → OpenCode Provider & Model Mapping

Canonical SOT: `/root/AAA/registries/models/AGENT_MODEL_MAP.json` (symlinked as `/root/.config/federation-models.json`)
Renderer: `/root/AAA/src/resolvers/opencode_render.py`
OpenCode config: `/root/.config/opencode/opencode.json`

**Directionality:** Strictly one-directional (SOT → OpenCode). The xlat table is never consulted in reverse. Identity mappings (SOT name == OpenCode name) are passthroughs, not ambiguity.

## Provider ID Translation

| SOT provider_id | OpenCode provider key | API Key | Status |
|---|---|---|---|
| `deepseek` | `deepseek` | `DEEPSEEK_API_KEY` | ACTIVE ($7.06) |
| `opencode-go` | `opencode-go` | `OPENCODE_GO_API_KEY` | ACTIVE |
| `opencode-zen` | `opencode-zen` | `OPENCODE_GO_API_KEY` | ACTIVE (same key) |
| `openrouter` | `openrouter` | `OPENROUTER_API_KEY` | ACTIVE |
| `kimi` / `kimi-moonshot` | `kimi` | `KIMI_API_KEY` | ACTIVE (REST API) |
| `tokenrouter-arifos` | `tokenrouter-arifos` | `TOKENROUTER_API_KEY` | ACTIVE |
| `minimax` | `minimax` | `MINIMAX_API_KEY` | RATE_LIMITED |
| `ollama` | `ollama` | (none — local) | ACTIVE |
| `groq` | `groq` | `GROQ_API_KEY` | ACTIVE (FREE) |
| `gemini` | `gemini` | `GEMINI_API_KEY` | ACTIVE (FREE) |
| `cerebras` | `cerebras` | `CEREBRAS_API_KEY` | ACTIVE ($5 credit) |
| `sea-lion` | `sea-lion` | `SEA_LION_API_KEY` | ACTIVE (FREE) |
| `azure-openai` | `azure-openai` | `AZURE_OPENAI_KEY` | ACTIVE (retiring Oct 2026) |
| `bailian-token-plan` | (no direct OpenCode provider) | `QWEN_API_KEY` | Falls back to `kimi` for kimi models |
| `mimo-platform` | (no direct OpenCode provider) | `MIMO_API_KEY` | Falls back to `opencode-go` for mimo models |
| `glm` | `tokenrouter-arifos` | (via TokenRouter) | GLM models via TokenRouter |
| `openai` | `openrouter` | (via OpenRouter) | OpenAI models via OpenRouter |
| `xai` | `openrouter` | (via OpenRouter) | xAI models via OpenRouter |
| `flame` | (no OpenCode provider) | (none) | Free-loop engine, not routed through OpenCode |

## SOT model_key → OpenCode model reference

SOT`s model_key includes provider prefix (e.g., `deepseek/deepseek-v4-pro`).
The OpenCode reference uses the OpenCode provider key + model ID.

| SOT model_key | OpenCode reference | Notes |
|---|---|---|
| `deepseek/deepseek-v4-pro` | `deepseek/deepseek-v4-pro` | Direct match ✅ |
| `deepseek/deepseek-v4-flash` | `deepseek/deepseek-v4-flash` | Direct match ✅ |
| `kimi/k3` | `kimi/k3` | Direct match ✅ |
| `kimi/kimi-k2.7-code` | `kimi/kimi-for-coding` | ⚠️ Kimi API calls it `kimi-for-coding` |
| `kimi/kimi-for-coding` | `kimi/kimi-for-coding` | Direct match ✅ |
| `minimax/MiniMax-M3` | `minimax/MiniMax-M3` | Direct match ✅ |
| `minimax/MiniMax-M2.7` | `minimax/MiniMax-M2.7` | Direct match ✅ |
| `ollama/qwen2.5-coder:3b` | `ollama/qwen2.5-coder:3b` | Direct match ✅ |
| `glm/glm-5.2` | `tokenrouter-arifos/z-ai/glm-5.2` | Via TokenRouter |
| `mimo/mimo-v2.5-pro` | `opencode-go/mimo-v2.5-pro` | Via opencode-go |
| `groq/llama-3.1-8b-instant` | `groq/llama-3.1-8b-instant` | Direct match ✅ |
| `groq/llama-3.3-70b-versatile` | `groq/llama-3.3-70b-versatile` | Direct match ✅ |
| `sea-lion/Qwen-SEA-LION-v4-32B-IT` | `sea-lion/aisingapore/Qwen-SEA-LION-v4-32B-IT` | Full path needed |
| `sea-lion/Llama-SEA-LION-v3-70B-IT` | `sea-lion/aisingapore/Llama-SEA-LION-v3-70B-IT` | Full path needed |
| `sea-lion/Gemma-SEA-LION-v4-27B-IT` | `sea-lion/aisingapore/Gemma-SEA-LION-v4-27B-IT` | Full path needed |
| `gemini/gemini-2.5-flash` | `gemini/gemini-2.5-flash` | Direct match ✅ |
| `cerebras/gemma-4-31b` | `cerebras/gemma-4-31b` | Direct match ✅ |

## Agent Model Assignments (SOT → OpenCode)

| OpenCode Agent | SOT Source | Model | Provider |
|---|---|---|---|
| forge | forge | deepseek/deepseek-v4-pro | deepseek |
| auditor | auditor | deepseek/deepseek-v4-pro | deepseek |
| ops | ops | deepseek/deepseek-v4-flash | deepseek |
| planner | planner | kimi/kimi-for-coding | kimi (via model key) |
| recovery | recovery | ollama/qwen2.5-coder:3b | ollama |
| image-prompt-architect | (special) | kimi/k3 | kimi (vision) |

## Fallback Chains per Agent (from SOT)

| Agent | Fallback 1 | Fallback 2 | Fallback 3 |
|---|---|---|---|
| forge | tokenrouter/z-ai/glm-5.2 | minimax/MiniMax-M3 | — |
| auditor | opencode-go/mimo-v2.5-pro | minimax/MiniMax-M3 | — |
| ops | minimax/MiniMax-M2.5 | minimax/MiniMax-M3 | — |
| planner | deepseek/deepseek-v4-pro | opencode-go/mimo-v2.5-pro | — |
| recovery | (none) | — | — |
| opencode (default) | tokenrouter/z-ai/glm-5.2 | minimax/MiniMax-M3 | ollama/qwen2.5-coder:3b |
