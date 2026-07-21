# Groq Free Tier — Cross-Agent Wiring (2026-07-20)

Groq offers a FREE tier with ultra-fast LPU inference — no credit card required. 560-1000 tokens/second, 131K context across all models.

## API Details

| Property | Value |
|---|---|
| Base URL | `https://api.groq.com/openai/v1` |
| Auth | `Bearer $GROQ_API_KEY` |
| Transport | `openai_chat` (OpenAI-compatible) |
| Rate limit | TPM-based, not daily request-based |

## Free Tier Models

| Model ID | Speed | Free Limit | Context | Best For |
|---|---|---|---|---|
| `llama-3.1-8b-instant` | 560 t/s | **14,400 req/day** | 131K | Workhorse — spam freely |
| `llama-3.3-70b-versatile` | 280 t/s | 1,000 req/day | 131K | Complex reasoning |
| `openai/gpt-oss-20b` | **1,000 t/s** | 1,000 req/day | 131K | Fastest available |
| `openai/gpt-oss-120b` | 500 t/s | 1,000 req/day | 131K | Heavy lifting |
| `qwen/qwen3.6-27b` | 500 t/s | 1,000 req/day | 131K | Qwen latest |

All models are **text-only** (no vision). `attachment: false` in OpenCode config.

## Arif's Miskin Strategy (RM0 Full Stack)

```
PRIMARY:   groq/llama-3.1-8b-instant  (14K/day FREE → spam freely)
COMPLEX:   groq/llama-3.3-70b-versatile (1K/day → save for hard tasks)
FASTEST:   groq/gpt-oss-20b (1000 t/s → when speed matters)
BACKUP:    opencode-go/deepseek-v4-flash-free (also FREE)
LOCAL:     ollama/qwen2.5-coder:3b (zero API cost)
```

**TPM is the real limit — not daily requests.** Llama-8B has 6K TPM, 70B has 12K. Spread across providers when throttled.

## Cross-Agent Wiring (OpenCode + OpenClaw + Hermes)

All three agents share the same `GROQ_API_KEY` from `/root/.secrets/vault.env`. Each config format differs:

### OpenCode (`/root/.config/opencode/opencode.json`)

```json
"provider": {
  "groq": {
    "npm": "@ai-sdk/openai-compatible",
    "name": "Groq (FREE — ultra-fast inference)",
    "options": {
      "baseURL": "https://api.groq.com/openai/v1",
      "apiKey": "{env:GROQ_API_KEY}"
    },
    "models": {
      "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B (560t/s, 14K/d)",
        "attachment": false,
        "tool_call": true,
        "reasoning": false,
        "limit": {"context": 131072, "output": 8192},
        "modalities": {"input": ["text"], "output": ["text"]}
      }
    }
  }
}
```

### OpenClaw (`/root/.openclaw/openclaw.json`)

```json
"providers": {
  "groq": {
    "api": "openai-completions",
    "name": "Groq (FREE — ultra-fast)",
    "url": "https://api.groq.com/openai/v1",
    "apiKeyEnv": "GROQ_API_KEY",
    "models": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", ...]
  }
}
```

### Hermes (`~/.hermes/config.yaml`)

```yaml
providers:
  groq:
    name: Groq (FREE — ultra-fast LPU inference)
    api: https://api.groq.com/openai/v1
    key_env: GROQ_API_KEY
    transport: openai_chat
    models:
      - id: llama-3.1-8b-instant
        name: Llama 3.1 8B (560t/s, 14K/d)
```

## Verification

```bash
set -a && source /root/.secrets/vault.env && set +a
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $GROQ_API_KEY"
# Returns 8+ free models including llama-3.1-8b-instant
```

Key lives in `/root/.secrets/vault.env` as `export GROQ_API_KEY="..."` and `export GROQ_BASE_URL="https://api.groq.com/openai/v1"`.
