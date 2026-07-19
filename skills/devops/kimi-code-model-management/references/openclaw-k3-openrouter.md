# OpenClaw + OpenRouter K3 Configuration

How to add Kimi K3 to OpenClaw via OpenRouter — bypasses Kimi Code quota limits.

## Why OpenRouter instead of direct Kimi API

- Kimi Code `managed:kimi-code` provider uses OAuth (device-code flow) — hard to wire into OpenClaw
- Kimi Code burns quota on cheap plans fast
- OpenRouter uses simple API key auth — `OPENROUTER_API_KEY`
- OpenRouter pricing: $3/M input, $15/M output, $0.30/M cache read

## Steps

### 1. Add OpenRouter provider

In `/root/.openclaw/openclaw.json`, under `models.providers`:

```json
"openrouter": {
  "baseUrl": "https://openrouter.ai/api/v1",
  "api": "openai-completions",
  "apiKey": "${OPENROUTER_API_KEY}",
  "models": [
    {
      "id": "moonshotai/kimi-k3",
      "name": "Kimi K3 (OpenRouter) — 2.8T MoE reasoning, 1M ctx, coding+vision",
      "contextWindow": 1000000,
      "maxTokens": 131072,
      "input": ["text", "image"],
      "cost": {"input": 3, "output": 15, "cacheRead": 0.3, "cacheWrite": 0}
    }
  ]
}
```

### 2. Add model alias

Under `agents.defaults.models`:

```json
"openrouter/moonshotai/kimi-k3": {
  "alias": "Kimi K3"
}
```

### 3. Use as worker

For the opencode agent (coding worker):

```json
"default_model": "openrouter/moonshotai/kimi-k3"
```

Or in main fallbacks:

```json
"fallbacks": [
  "deepseek/deepseek-v4-pro",
  "openrouter/moonshotai/kimi-k3",
  "minimax/MiniMax-M2.7-highspeed"
]
```

### 4. Restart

```bash
systemctl restart openclaw-gateway
sleep 3 && curl -sf http://localhost:18789/health
```

Check logs for: `openrouter/moonshotai/kimi-k3 model configured, enabled automatically.`

## K3 Specs (OpenRouter)

| Property | Value |
|---|---|
| Parameters | 2.8T (open-weight) |
| Context | 1M tokens |
| Modalities | text + image |
| Pricing | $3/$15 per 1M tokens |
| Latency | ~7s p50 |
| Throughput | 21 tps |
| Cache hit | 94% → effective input ~$0.46/M |

## Caveats

- Released Jul 16 2026 — upstream capacity limited, may 429
- Structured output error rate ~12% — JSON mode unreliable
- Reasoning: only `max` level supported currently
- Via OpenRouter, quota is separate from Kimi Code plan — no moderato/allegretto tiering
