# Provider Quick Reference — verified 2026-07-06

Verbatim findings from probing the actual APIs. **Re-verify before pasting — vendors rotate models and rename endpoints without notice.** Always run `scripts/probe_provider.py` to regenerate the live block.

## Xiaomi MiMo (Token Plan SGP)

- **Endpoint:** `https://token-plan-sgp.xiaomimimo.com/v1`
- **Anthropic alt endpoint:** `https://token-plan-sgp.xiaomimimo.com/anthropic`
- **Auth header:** `api-key:*** KEY` (NOT `Authorization: Bearer ...` — this is the difference from most OpenAI-compat providers)
- **Env vars (set BOTH for safety):** `MIMO_API_KEY` and `XIAOMI_API_KEY` (same value)
- **Live model list** (as of 2026-07-04):
  - `mimo-v2.5`
  - `mimo-v2.5-asr` (speech/audio)
  - `mimo-v2.5-pro`
- **Probing command:**
  ```bash
  curl -sS -H "api-key: $MIMO_API_KEY" https://token-plan-sgp.xiaomimimo.com/v1/models
  ```
- **Health check:** 200 OK with `{"object":"list","data":[...]}`. 401 = wrong key.
- **Pitfall:** The Anthropic alt endpoint accepts Anthropic body shape, but the `/v1` endpoint is OpenAI-compat — use `transport: openai_chat` unless you have proof the Anthropic shape works.

## MiniMax (Token Plan)

- **Endpoint:** `https://api.minimax.io/v1`
- **Auth header:** `Authorization: Bearer *** KEY (standard OpenAI-compat)
- **Key prefix:** `sk-cp-` (subscription key, distinct from pay-as-you-go)
- **Env var:** `MINIMAX_API_KEY`
- **Models:** `MiniMax-M1` (flagship), `minimax-m3`
- **Capabilities:** text, image understanding, video understanding, speech (TTS/ASR), music generation, video generation (3/day on Max tier)
- **Tiers:** Plus ($20/mo), Max ($50/mo), Ultra ($120/mo) — all share one multimodal quota
- **Probing command:**
  ```bash
  curl -sS -H "Authorization: Bearer $MINIMAX_API_KEY" \
    https://api.minimax.io/v1/models
  ```
- **Health check:** 200 OK with model list. 401 = wrong key or expired subscription.
- **Pitfall:** `MINIMAX_API_HOST=https://api.minimax.io` may exist in env from MiniMax CLI, but `MINIMAX_API_KEY` must be set separately from https://platform.minimax.io/user-center/payment/token-plan

## OpenCode Zen / Go

- **Endpoint:** `https://opencode.ai/zen/v1` (Go traffic routes here too)
- **Alias:** `https://api.opencode.ai/go/v1/{chat/completions,messages,responses}` (same models, same key — only the `/chat/completions`, `/messages`, `/responses` paths work; `/models` returns 404 on the Go alias)
- **Auth header:** `Authorization: Bearer *** key>
- **Env var:** `OPENCODE_API_KEY` (the same key works for Free, Pro, and Go tiers — the tier is server-determined by your subscription at opencode.ai/auth)
- **Model IDs in API:** BARE — e.g. `gpt-5.5`, `claude-opus-4-8`, `mimo-v2.5-pro`. NOT prefixed with `opencode/` despite what the OpenCode docs say.
- **Live model count:** 50 (as of 2026-07-04)
- **Tier differences (no API impact, only billing/quota):**
  - **Go** = $5 first month / $10/mo sub, high per-model RPH limits (MiMo-V2.5-Pro 3,250/5hr, MiMo-V2.5 30,100/5hr, DeepSeek V4 Pro 4,300/5hr)
  - **Zen** = pay-per-token, lower RPH limits, no monthly cap
- **Probing command (no auth needed for /v1/models):**
  ```bash
  curl -sS https://opencode.ai/zen/v1/models
  ```
- **Health check:** HTTP 200 from your server IP. From other IPs (e.g. clean datacenters), Cloudflare returns 403 error 1010 — that's a fingerprint check, not an auth failure. Your VPS should be clean.
- **Picker label convention:** If user said "OpenCode Go", use slug `opencode-go` and label `"OpenCode Go (Zen subscription)"`. If user said "Zen", use slug `opencode-zen` and label `"OpenCode Zen"`. The endpoint and key_env are identical either way.

## Alibaba Bailian (Token Plan SG / PAYG)

- **Token Plan endpoint:** `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **PAYG endpoint:** `https://ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **Auth header:** `Authorization: Bearer *** KEY
- **Env vars:** `QWEN_API_KEY` (token plan), `BAILIAN_PAYG_API_KEY` (PAYG)
- **Models:** qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.6-flash, deepseek-v4-pro, deepseek-v4-flash, kimi-k2.7-code, glm-5.2, and more
- **Vision models:** qwen3.7-plus (strongest, 1M context, 16M pixels, 2h video), qwen3.6-flash (near-flagship, cheaper), qwen-vl-ocr (dedicated OCR)

## When MiMo and OpenCode both register `mimo-v2.5-pro` in your picker

This is intentional. They are the same model served by different providers at different prices. Arif usually wants OpenCode Go (subscription, generous quota) for coding work and MiMo direct (token-plan SGP) for federation fallback. The picker shows both with distinct labels; pick by use case:
- **`/model mimo-v2.5-pro` on MiMo** → goes to token-plan-sgp endpoint, charged against token-plan credits
- **`/model opencode-go` (with model mimo-v2.5-pro under that provider)** → goes through Zen endpoint, charged against Go subscription

This means you don't need a single "canonical" MiMo provider — keep both registered. They're complementary billing paths, not duplicates.

## Quick env-var cheat sheet for this machine

| Variable | Value source | Used by |
|---|---|---|
| `MIMO_API_KEY` | `/root/.secrets/mimo.env` or `/root/.secrets/vault.flat.env` (sourced by `/etc/profile.d/mimo-tokenplan.sh`) | Xiaomi MiMo direct |
| `XIAOMI_API_KEY` | (alias) same value as `MIMO_API_KEY`, written to `/root/.hermes/.env` for Hermes canonical name | Xiaomi MiMo direct (Hermes-canonical lookup) |
| `OPENCODE_API_KEY` | https://opencode.ai/auth (after subscribing to Go) | OpenCode Zen/Go |
| `OPENCODE_GO_API_KEY` | (alias for users who call it Go) same value as `OPENCODE_API_KEY` | OpenCode Go (Hermes-canonical name) |
| `MINIMAX_API_KEY` | https://platform.minimax.io/user-center/payment/token-plan (sk-cp- prefix) | MiniMax direct |
| `QWEN_API_KEY` | Alibaba Bailian token plan | Bailian Token Plan SG |
| `BAILIAN_PAYG_API_KEY` | Alibaba Bailian PAYG workspace | Bailian PAYG |

Always write to `/root/.hermes/.env` (chmod 600) so the gateway picks it up at restart. The shell export via `mimo-tokenplan.sh` only covers CLI sessions, not the long-running gateway service.
