# OpenCode Provider Config

## DeepSeek baseURL Fix

**Symptom:** `Error: Unauthorized: Authentication Fails (governor)` when using `deepseek/deepseek-v4-pro` or `deepseek/deepseek-v4-flash` in OpenCode.

**Root cause:** OpenCode config has `provider.deepseek.options.baseURL` set to `https://api.deepseek.com/v1` — but DeepSeek's endpoint is `https://api.deepseek.com` (NO `/v1`). The `/v1` breaks the OpenAI adapter.

**Fix:** Edit `/root/.config/opencode/opencode.json`: change `baseURL` from `https://api.deepseek.com/v1` to `https://api.deepseek.com`.

**Verification:** `opencode run 'Respond: OK' --model deepseek/deepseek-v4-flash`

## Fallback (when DeepSeek fails)

`opencode-go/deepseek-v4-flash-free` → `opencode-go/qwen3.7-max` → `opencode-go/kimi-k2.7-code`

## Check

`opencode auth list` — list registered providers
`opencode models deepseek` — list models
