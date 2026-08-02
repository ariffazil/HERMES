# Qwen Fallback Chain — Live Test Results 2026-08-02

**Session:** Arif audit + zen of Hermes fallback routing
**Profile:** `default` (main Hermes config)
**Date:** 2026-08-02 ~07:00 UTC

## Live Probe Results (curl, 1-token test)

| Position | Model | Provider | Key | Result | Latency |
|---|---|---|---|---|---|
| PRIMARY | deepseek-v4-pro | qwen-token-plan | QWEN_OPENCODE_API_KEY (Pro 100K) | ✅ (reasoning) | 1.0s |
| [0] | qwen3.6-flash | qwen-token-plan-standard | QWEN_HERMES_API_KEY (Standard 25K) | ✅ OK | 1.2s |
| [1] | minimax-m3 | minimax | MINIMAX_API_KEY | ✅ (thinking spill) | 1.0s |
| [2] | llama-3.1-8b-instant | groq | GROQ_API_KEY | ✅ OK | 0.2s |
| [3] | qwen2.5:3b | ollama | ollama (local) | ✅ OK | 0.7s |

**5/5 PASS — all entries verified live.**

## Dead Providers Detected (removed from chain)

| Provider | Issue | Evidence |
|---|---|---|
| MuleRouter | Negative balance (-0.75 credits) | `Available balance: -0.7476 credits, Minimum required: 0.1 credits` |
| OpenRouter | $0 credits | `Insufficient credits. Add more using https://openrouter.ai/settings/credits` |
| Gemini | Removed by user | "gemini dah x dak la" |

## Ollama Model Name Correction

- **Expected:** `qwen2.5-coder:3b`
- **Actual:** `qwen2.5:3b` (no `-coder` suffix)
- **Available models:** `bge-m3:latest`, `qwen2.5:3b`

## Key Inventory (Actual — 2 keys under 6 env var names)

| Env Var | Key Prefix | Seat | Monthly |
|---|---|---|---|
| QWEN_OPENCODE_API_KEY | sk-sp-H.DIEXP | Pro | 100K |
| QWEN_API_KEY (legacy) | sk-sp-H.DIEXP | Pro | 100K — SAME KEY |
| QWEN_HERMES_API_KEY | sk-sp-D.IPRH | Standard | 25K |
| QWEN_BAILIAN_KEY (legacy) | sk-sp-D.IPRH | Standard | 25K — SAME KEY |
| QWEN_INDIVIDUAL_API_KEY | sk-sp-H.DIIYD | Individual Pro | 5h+7d windows |
| QWEN_OPENCLAW_API_KEY | sk-sp-D.IEHM | Standard (Seat 2) | ❌ DEAD — key purged |

## Pro Quota Exhaustion Pattern

- 06:43-06:45 UTC: Pro key (100K) exhausted — `HTTP 429: Allocated quota exceeded`
- 07:15 UTC: Pro key recovered — quota window reset
- Individual Pro also exhausted its 5h window at the same time

## Final Config (deployed)

```yaml
model:
  provider: qwen-token-plan
  default: deepseek-v4-pro
  context_length: 262144  # 256K
  max_tokens: 32768

fallback_providers:
  - model: qwen3.6-flash
    provider: qwen-token-plan-standard
    timeout: 30
  - model: minimax-m3
    provider: minimax
    timeout: 30
  - model: llama-3.1-8b-instant
    provider: groq
    timeout: 20
  - model: qwen2.5:3b
    provider: ollama
    timeout: 20

auxiliary:
  compression:
    provider: minimax
    model: minimax-m3
    timeout: 120

compression:
  threshold: 0.25
  target_ratio: 0.1

fallback_silent_failover: true
```

**Key diversity:** 4 independent keys (Pro, Standard, MiniMax, Groq) + Ollama local = 5 independent failure domains.