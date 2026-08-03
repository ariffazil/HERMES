# LiteLLM Unified Proxy — FED FLAME FRAME

> **Doctrine: ONE key, ONE entry point.** Satu pintu, satu kunci.
> "Aku penat handle API key ikut cartel ai labs. Dah la API key itself is stupid architecture." — Arif, 2026-08-03

## Architecture

LiteLLM (`/root/A-FORGE/litellm-config.yaml`, port 4000, systemd service) is the federation's
unified model routing plane — a single OpenAI-compatible proxy that manages all provider
API keys internally. Clients (Hermes, tools, cron jobs) only need the LiteLLM master key.

```
Client (Hermes/tool/cron) → LiteLLM :4000 → Providers
  ↓ single master_key                           ↓ all API keys in litellm-config.yaml
  ↓ no per-provider keys needed                 ↓ kunci-mas.env → EnvironmentFile
```

## Role-Based Model Groups

| Group | Primary Model | Primary Route | Fallback | Purpose |
|-------|--------------|---------------|----------|---------|
| `main` | deepseek-v4-pro | Qwen Token Plan | flame-free → last-resort | Deep reasoning |
| `forge` | glm-5.2 | Qwen Token Plan | flame-free → last-resort | Engineering |
| `auditor` | deepseek-v4-pro | Qwen Token Plan | flame-free → last-resort | Cross-check |
| `planner` | kimi-k2.7-code | Qwen Token Plan | flame-free → last-resort | Code planning |
| `ops` | MiniMax-M2.5-highspeed | MiniMax direct | flame-free → last-resort | Fast monitoring |
| `small` | qwen3.6-flash | Qwen Token Plan | flame-free → last-resort | Lightweight |

## Fallback Chain Doctrine

```
K1/Qwen TP → FLAME free (:18901) → last-resort (MiniMax)
```

- **Circuit breaker**: 3 fails → 60s cooldown per endpoint
- **Retry**: 2x on transient failures
- **Routing**: simple-shuffle across healthy endpoints
- **Default fallback**: `[flame-free, last-resort]` for all groups

## Key Files & Service

| Item | Value |
|------|-------|
| Config | `/root/A-FORGE/litellm-config.yaml` |
| Service | systemd `litellm` (user root, port 4000, bound 127.0.0.1) |
| Master key | `LITELLM_MASTER_KEY` in `/root/.secrets/kunci-mas.env` |
| Version | 1.90.2 (BerriAI) |
| DB | null (stateless — no persistence) |

## Health Check

```bash
curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  http://127.0.0.1:4000/health | \
  python3 -c "
import json, sys
d = json.load(sys.stdin)
h = len(d.get('healthy_endpoints', []))
u = len(d.get('unhealthy_endpoints', []))
print(f'Healthy: {h} | Unhealthy: {u}')
for ep in d.get('healthy_endpoints', []):
    print(f'  ✅ {ep[\"model\"]}')
for ep in d.get('unhealthy_endpoints', []):
    print(f'  ❌ {ep[\"model\"]} — {ep.get(\"error\",\"\")[:60]}')
"
```

## Test Chat Completion Through LiteLLM

```bash
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"main","messages":[{"role":"user","content":"test"}],"max_tokens":10}'
```

## FLAME Dependency

FLAME (:18901) is LiteLLM's free-tier fallback for all model groups. If FLAME is down,
LiteLLM falls through to `last-resort` (MiniMax direct). The proxy survives, but the free
tier is unavailable until FLAME is revived.

**Symptom when FLAME is dead**: All `flame-free` endpoints show `InternalServerError:
Connection error` in health check. Only MiniMax endpoints remain healthy.

**Recovery**: See `flame-free-loop-mesh` skill — zombie process + port conflict recovery.

## Unification Status (2026-08-03)

**Two routing planes run independently:**

1. **Hermes direct** — Hermes has its own provider list (qwen-token-plan, minimax, deepseek, groq) with direct API keys
2. **LiteLLM proxy** — Runs on :4000 with 6 role groups, circuit breaker, retry logic

**They are NOT connected.** Hermes does not currently route through LiteLLM.

**Unification path**: Point Hermes to use LiteLLM as its sole provider:
- Remove all direct provider blocks from Hermes config
- Add a single `litellm` provider pointing to `http://127.0.0.1:4000/v1`
- One master key → all provider keys managed by LiteLLM internally
- Hermes benefits from LiteLLM's circuit breaker, retry, and role-based routing

**Pre-requisite**: FLAME must be healthy for LiteLLM's fallback chain to be complete.
