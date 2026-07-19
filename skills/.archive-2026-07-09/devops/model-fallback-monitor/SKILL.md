---
name: model-fallback-monitor
description: >
  Monitor the model fallback chain: MiniMax (primary), DeepSeek (hot-swap),
  Kimi, Ollama qwen2.5:7b (local). Track latency, billing failures (402),
  cold-start failures, and auto-pause dead models. USE WHEN: "model health",
  "check fallback chain", "DeepSeek balance", "model latency", "billing alert".
---

# Model Fallback Monitor

**Tracks Arif's model federation health. Prevents the DeepSeek 402 scenario from going unnoticed.**

## Current Fallback Chain

```
Primary:    minimax/MiniMax-M2.7  (hot)
Fallback 1: deepseek/deepseek-chat
Fallback 2: kimi/kimi-for-coding
Fallback 3: ollama/qwen2.5:7b     (cold/local)
```

## Monitor Checks

### 1. DeepSeek Balance
```bash
# Check DeepSeek balance (will 402 if empty)
curl -s -X POST https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_KEY" \
  --max-time 10 | jq '.error.code' 2>/dev/null
```

### 2. MiniMax Availability
```bash
# Quick MiniMax ping (adjust endpoint as needed)
curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
  https://api.minimax.chat/v1/models 2>/dev/null
```

### 3. Ollama Cold Start
```bash
# Check Ollama is responsive
curl -s --max-time 5 localhost:11434/api/tags | jq '.models[].name'
```

### 4. Fallback Chain Latency Test
```bash
# Time each model in chain
for model in "mini-mini" "deepseek" "kimi" "ollama"; do
  start=$(date +%s%N)
  # lightweight ping for each
  echo "$model: $(($(date +%s%N) - $start))ns"
done
```

## Known Failure Modes

| Model | Failure Mode | Detection |
|---|---|---|
| deepseek-v4-pro | 402 Insufficient Balance | HTTP 402 |
| deepseek-chat | Rate limit | HTTP 429 |
| kimi | Unknown model key | Config mismatch |
| ollama/qwen2.5:7b | Cold start slow | > 30s response |

## Log Output

```
MODEL FALLBACK MONITOR — $(date -u)
────────────────────────────────────
MiniMax:   ✅ OK (latency: Xms)
DeepSeek:  ⚠️ LOW BALANCE (estimated $Y remaining)
Kimi:      ✅ OK / ❌ UNCONFIGURED
Ollama:    ✅ OK (qwen2.5:7b loaded)
────────────────────────────────────
Active model: minimax/MiniMax-M2.7
Fallback chain: healthy / degraded / critical
```

## Cron

```bash
# Run every 30 min
*/30 * * * * /root/.openclaw/workspace/skills/model-fallback-monitor/check.sh >> /var/log/model-monitor.log 2>&1
```
