# OpenCode Provider Config Patterns

Live-tested fixes for OpenCode models at `/root/.config/opencode/opencode.json`.

## DeepSeek baseURL Fix

**Symptom:** `Error: Unauthorized: Authentication Fails (governor)` when using `deepseek/deepseek-v4-pro` or `deepseek/deepseek-v4-flash`.

**Root cause:** OpenCode config has `provider.deepseek.options.baseURL` set to `https://api.deepseek.com/v1` — DeepSeek's endpoint is `https://api.deepseek.com` (NO `/v1`). The `/v1` breaks the OpenAI adapter.

**Fix:** Edit `/root/.config/opencode/opencode.json`: change `baseURL` to `https://api.deepseek.com`.

## Gemini via OpenAI-Compatible Endpoint (2026-07-20)

**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/openai`
**Auth:** `{env:GEMINI_API_KEY}` — standard Bearer header

### Pitfall: Gemini rejects non-standard fields

Gemini's OpenAI-compatible endpoint is **strict** — it rejects any field it doesn't recognize. When `tool_call: true`, OpenCode sends `skills` and `instructions` fields that Gemini's endpoint rejects with:

```
400: "Invalid JSON payload received. Unknown name 'skills': Cannot find field."
     "Unknown name 'instructions': Cannot find field."
```

**Fix:** Set `tool_call: false` on Gemini models. `reasoning: true` can stay.

```json
**Fix A (keep tool_call disabled):** Set `tool_call: false` on Gemini models. `reasoning: true` can stay.

```json
{
  "npm": "@ai-sdk/openai-compatible",
  ...
  "models": {
    "gemini-2.5-flash": {
      "tool_call": false,
      "reasoning": true,
      ...
    }
  }
}
```

**Fix B (native provider, tool_call works):** Switch to `@ai-sdk/google`. Install first: `cd /root/.npm-global && npm install @ai-sdk/google`. This sends correct Gemini-native format and accepts tool_call + reasoning natively.

```json
{
  "npm": "@ai-sdk/google",
  "options": {
    "baseURL": "https://generativelanguage.googleapis.com/v1beta",
    "apiKey": "{env:GEMINI_API_KEY}"
  },
  ...
}
```

**Trade-off:** Fix A — simpler, no install, but no tool calling. Fix B — native, tool_call works, but needs npm install.

## TokenRouter Model IDs Must Match Provider Names (2026-07-20)

**Endpoint:** `https://api.tokenrouter.com/v1` (`.com` for Chat Completions, NOT `.io`)

TokenRouter uses provider-prefixed model names. The key in OpenCode config must match what `/v1/models` returns:

| OpenCode key | TokenRouter model ID |
|---|---|
| `z-ai/glm-5.2` | `z-ai/glm-5.2` |
| `z-ai/glm-5.2-free` | `z-ai/glm-5.2-free` |

### Pitfall: model_id not set → API rejects bare model name

When `model_id` is null, OpenCode sends the model key as-is. `glm-5.2` is NOT a valid TokenRouter model — needs `z-ai/` prefix.

**Fix:** Always use `z-ai/glm-5.2` as the model key. Direct Z.AI API key (`ZAI_API_KEY`) is expired (2026-07-20: `401 令牌已过期`). TokenRouter is the only path for GLM.

```bash
curl -s https://api.tokenrouter.com/v1/models \
  -H "Authorization: Bearer $TOKENROUTER_API_KEY" \
  | jq '.data[].id' | grep glm
```

### Reasoning-model max_tokens

GLM-5.2 emits `reasoning_content` — can consume the entire `max_tokens` budget on thinking, leaving `content: ""`. OpenCode needs `max_tokens` ≥ 200 for these models.
