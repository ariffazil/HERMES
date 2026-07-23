# OpenCode Live Probe — 2026-07-23 18:30Z

80 models tested (57 Zen + 23 Go). 39 alive, 41 dead.
API keys: OPENCODE_ZEN_API_KEY + OPENCODE_GO_API_KEY both present.

## Probe results

| | Zen | Go | Total |
|---|---|---|---|
| Total listed | 57 | 23 | 80 |
| Alive (200) | 19 | 20 | 39 |
| Dead (401/400/429) | 38 | 3 | 41 |

## Zen Alive (19)

All via chat_completions endpoint:
grok-build-0.1, grok-4.5, deepseek-v4-pro, deepseek-v4-flash, glm-5.2, glm-5.1,
glm-5, minimax-m3, minimax-m2.7, minimax-m2.5, kimi-k2.6, kimi-k2.5,
qwen3.6-plus, qwen3.5-plus, big-pickle (free), deepseek-v4-flash-free,
mimo-v2.5-free, nemotron-3-ultra-free, north-mini-code-free

## Zen Dead (38)

- Claude (11): all 401 — premium billing required
- GPT (20): all 400 — premium billing + responses endpoint
- Gemini (5): all 400 — premium billing
- kimi-k2.7-code (429 rate limited), laguna-s-2.1-free (timeout)

## Go Alive (20) — all via chat_completions

kimi-k3, kimi-k2.7-code, kimi-k2.6, kimi-k2.5, glm-5.2, glm-5.1, glm-5,
deepseek-v4-pro, deepseek-v4-flash, mimo-v2.5-pro, mimo-v2.5, hy3, grok-4.5,
minimax-m3, minimax-m2.7, minimax-m2.5, qwen3.7-max, qwen3.7-plus,
qwen3.6-plus, qwen3.5-plus

## Go Dead (3)

mimo-v2-pro (400), mimo-v2-omni (400), hy3-preview (400)

## Routing Bug

Go MiniMax/Qwen routed through anthropic_messages (per docs) → 401.
Live probe confirms ALL Go models work via chat_completions.
Fix in `hermes_cli/models.py` `opencode_model_api_mode()`.

## 4-Tier Assignment

| Tier | Provider | Model | Cost |
|------|----------|-------|------|
| bulk (cron) | opencode-go | deepseek-v4-flash | flat $10/mo |
| default | opencode-zen | deepseek-v4-flash | $0.14/M in |
| heavy | opencode-zen | deepseek-v4-pro | $1.74/M in (fallback: minimax-m3 $0.30) |
| apex | opencode-zen | grok-4.5 | $2.00/M in (fallback: glm-5.2 $1.40) |

Anti-mahal: gateway switched from pro ($1.74/M) to flash ($0.14/M) — 12x cheaper.
