# OpenCode Zen and Go — verified endpoints, models, config

Last verified: 2026-07-24 (live source code + opencode.ai/docs)

## Two providers, two endpoints

OpenCode has TWO **built-in** providers in Hermes's `PROVIDER_REGISTRY`
(`hermes_cli/auth.py` lines 368-388). They use DIFFERENT endpoints:

| Provider slug | Endpoint | API surface routing |
|---|---|---|
| `opencode-zen` | `https://opencode.ai/zen/v1` | responses / messages / chat/completions per model |
| `opencode-go` | `https://opencode.ai/zen/go/v1` | messages / chat/completions per model |

**Previous sessions claimed Go was consolidated to `/zen/v1`. This was wrong.**
The live `auth.py` has `inference_base_url="https://opencode.ai/zen/go/v1"`
for opencode-go. Server-side tier routing also plays a role, but the
endpoints themselves are distinct paths.

## Built-in shortcut (no custom providers: block needed)

Because opencode-zen and opencode-go are in `PROVIDER_REGISTRY`, you do NOT
need a custom `providers:` block. Three steps:

```bash
# 1. Key in .env
echo 'OPENCODE_GO_API_KEY=sk-***' >> ~/.hermes/.env

# 2. Switch
hermes config set model.provider opencode-go
hermes config set model.default deepseek-v4-pro

# 3. Done. Hermes auto-routes api_mode per model via opencode_model_api_mode().
```

The `opencode_model_api_mode()` function in `hermes_cli/models.py` handles
per-model routing:
- Go: ALL models → `chat_completions` (MiniMax/Qwen were incorrectly routed
  to anthropic_messages per upstream docs — patched 2026-07-23 after live probe)
- Zen: Claude → `anthropic_messages`, GPT → `codex_responses`, Qwen →
  `anthropic_messages`, everything else → `chat_completions`

## OpenCode Go — model list (verified 2026-07-24 from opencode.ai/docs/go/)

16 models, **$5 first month**, then **$10/month**, usage caps: $12/5hr, $30/week, $60/month.

| Model | Requests/week | Pricing (per MTok in/out) |
|---|---|---|
| Grok 4.5 | 300 | $2.00 / $6.00 |
| GLM-5.2 | 2,150 | $1.40 / $4.40 |
| GLM-5.1 | 2,150 | $1.40 / $4.40 |
| Kimi K3 | 250 | $3.00 / $15.00 |
| Kimi K2.7 Code | 3,380 | $0.95 / $4.00 |
| Kimi K2.6 | 2,880 | $0.95 / $4.00 |
| MiMo-V2.5 | 75,200 | $0.14 / $0.28 |
| MiMo-V2.5-Pro | 8,150 | $0.435 / $0.87 |
| MiniMax M3 | 8,000 | $0.30 / $1.20 |
| MiniMax M2.7 | 8,500 | $0.30 / $1.20 |
| Qwen3.7 Max | 2,390 | $2.50 / $7.50 |
| Qwen3.7 Plus | 10,800 | $0.40 / $1.60 |
| Qwen3.6 Plus | 8,200 | $0.50 / $3.00 |
| DeepSeek V4 Pro | 8,550 | $0.435 / $0.87 |
| DeepSeek V4 Flash | 79,050 | $0.14 / $0.28 |
| Hy3 | 10,750 | $0.14 / $0.58 |

**API surface by model on Go (LIVE-PROBED 2026-07-23 — docs were WRONG):**
- `/v1/chat/completions` (OpenAI SDK): **ALL models** — DeepSeek, Kimi, GLM,
  MiMo, Grok, Hy3, MiniMax M3/M2.7/M2.5, Qwen3.7 Max/Plus, Qwen3.6 Plus
- MiniMax and Qwen were documented as `/v1/messages` but live probe showed
  401 on that endpoint — only chat_completions works. Hermes source code
  (`hermes_cli/models.py` `opencode_model_api_mode()`) had this bug routing
  Go MiniMax/Qwen through anthropic_messages. Patched 2026-07-23 to return
  chat_completions for ALL Go models.

**NOT on Go (Zen-only):** Claude, GPT, Gemini, Grok Build 0.1, Big Pickle,
Laguna, North Mini Code, Nemotron 3 Ultra.

## OpenCode Zen — model surface (verified 2026-07-24 from opencode.ai/docs/zen/)

Pay-per-token. 50+ models including all frontier models.

**API surface by model on Zen:**
- `/v1/responses` (OpenAI Responses): all GPT models (5.6 Sol/Terra/Luna,
  5.5, 5.4, 5.3 Codex, 5.2, 5.1, 5, Nano)
- `/v1/messages` (Anthropic SDK): Claude (Fable 5, Opus, Sonnet, Haiku),
  Qwen3.7 Max/Plus, Qwen3.6 Plus, Qwen3.5 Plus
- `/v1/chat/completions`: everything else (Gemini, Grok, DeepSeek, MiniMax,
  GLM, Kimi, MiMo free, Laguna, North Mini Code, Nemotron 3 Ultra, BigPickle)

**Free models on Zen**: DeepSeek V4 Flash Free, MiMo-V2.5 Free, Laguna S 2.1
Free, North Mini Code Free, Nemotron 3 Ultra Free, Big Pickle.

**Deprecated as of 2026-07-23**: GPT 5.2 Codex, GPT 5.1 Codex, GPT 5.1 Codex
Max, GPT 5.1 Codex Mini, GPT 5 Codex.

## Model IDs

Bare format always: `deepseek-v4-pro`, NOT `opencode/deepseek-v4-pro`.
The `opencode/<id>` prefix is internal to OpenCode's own config format
(`opencode.json`), not the API.

## Auth

Same physical API key from `https://opencode.ai/auth` can work on both
endpoints (tier determines what you can access). Hermes treats them as
separate credential namespaces:

- `OPENCODE_ZEN_API_KEY` → opencode-zen provider
- `OPENCODE_GO_API_KEY` → opencode-go provider

Set both if using both providers. Auth header: `Authorization: Bearer <key>`.

**Key management pattern (2026-07-24):** OpenCode's dashboard lets you create
multiple named API keys under one account. A single Zen subscription can have
separate keys labeled "AAA", "Hermes agent", "Openclaw", etc. — each with the
same access tier but different names for tracking. The key named "AAA" might be
used for `OPENCODE_GO_API_KEY` while "Hermes agent" is used for
`OPENCODE_ZEN_API_KEY`. Go's subscription (`$10/mo`) is an add-on to the Zen
account; the API determines tier from the key at request time, not from the env
var name. Both keys should be synced to BOTH `~/.hermes/.env` and
`/root/.secrets/vault.env` for consistency across Hermes and the federation.

## Verification

```bash
# Zen models
curl -sS https://opencode.ai/zen/v1/models \
  -H "Authorization: Bearer $OPENCODE_ZEN_API_KEY" | jq '.data[].id'

# Go models (different endpoint)
curl -sS https://opencode.ai/zen/go/v1/models \
  -H "Authorization: Bearer $OPENCODE_GO_API_KEY" | jq '.data[].id'
```

## Cross-reference

- `hermes-provider-setup/SKILL.md` — main skill (built-in shortcut, picker zen, MoA)
- `references/moa-opencode-provider-matrix.md` — MoA-specific provider rules
