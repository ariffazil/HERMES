# Unified Routing Audit — 3-Layer Accretion (2026-08-03)

> **Session:** Hermes Telegram, 2026-08-03 21:55-22:01 MYT
> **F13 directive:** "Kenapa kita x unified ja tu semua?" — Arif
> **Status:** AUDIT COMPLETE. Migration pending F13 approval.

## The Finding: Three Layers, Not One

The arifOS federation's model routing grew by accretion across three eras:

### Layer 1: FLAME (:18901) — Era 1 (Free-tier aggregation)

```
flame.service          — Engine, active but useless
flame-api.service      — API server, DEAD (auto-restart loop, exit code 1)
```

FLAME wraps Groq free-tier models behind a local API. Built first, when the problem was "how to access free models." The API server has been dead since at least 2026-08-03 without any visible alert — the engine stays alive so systemd reports green, but the API endpoint times out.

**Live state (2026-08-03):**
- `flame.service`: active, 48MB RAM, 2min uptime (keeps restarting)
- `flame-api.service`: activating (auto-restart), exit code 1
- `:18901` listens but times out on all requests
- **Verdict: DEAD — no consumers would notice because none use it directly**

### Layer 2: LiteLLM (:4000) — Era 2 (Sovereign proxy)

```
litellm-proxy.service  — Active, 10h uptime, 320MB RAM
Config: /root/A-FORGE/litellm-config.yaml (198 lines)
```

Built when direct provider connections were too fragile. LiteLLM abstracts 6 model tiers (main, forge, auditor, planner, ops, small) with 3-entry fallback per tier plus a secondary fallback chain (`→ flame-free → last-resort`). The `flame-free` fallback points to FLAME — which is dead.

**Live state (2026-08-03):**
- Healthy, responding on :4000
- 5 of 6 model tiers depend on FLAME for Gemini/SEA-LION entries
- `last-resort` tier works (MiniMax + Groq aggregator via FLAME — but FLAME is dead, so only MiniMax survives)
- 320MB RAM for a layer that FED already supersedes

### Layer 3: FED Router (:7074) — Era 3 (Intelligence plane)

```
fed-router.service     — Active, 12h uptime, 46MB RAM
MCP tools: fed_route, fed_status, fed_contrast, fed_health, fed_probe
```

The newest and most capable layer. Has balance tracking, latency telemetry, constitutional tiering, and route scoring. But it's used as an **advisory tool** — Hermes doesn't actually route through FED for runtime decisions. The live fallback chain is defined in Hermes config.yaml independently.

**Live state (2026-08-03):**
- Healthy, full MCP toolset operational
- Balance tracking shows DeepSeek at $13.19 (stale — API rejects)
- NOT the runtime routing plane — purely advisory

## The Overlap Matrix

| Capability | FLAME | LiteLLM | FED |
|---|---|---|---|
| Model→backend mapping | ✅ | ✅ | ✅ |
| Fallback chain logic | ❌ | ✅ | ✅ |
| Health checking | ❌ | ❌ | ✅ |
| Balance/cost tracking | ❌ | ❌ | ✅ |
| Constitutional tier routing | ❌ | ❌ | ✅ |
| Circuit breaker | ❌ | ✅ | ❌ |
| Free-tier aggregation | ✅ | ❌ | ❌ |
| RAM usage | 48MB | 320MB | 46MB |

**Three config files, three fallback chains, three places to debug.** When a provider changes or a key rotates, all three must be updated.

## Dead Paths Found

| Path | Dead Because |
|---|---|
| LiteLLM → flame-free (all tiers) | FLAME API dead |
| LiteLLM → gemini-2.5-flash | Via FLAME, dead |
| LiteLLM → gemini-flash-lite-latest | Via FLAME, dead |
| LiteLLM → qwen2.5-coder:3b | Via FLAME, dead |
| LiteLLM → llama-3.3-70b-versatile | Via FLAME, dead |
| LiteLLM → free-aggregator | Via FLAME, dead |
| LiteLLM → SEA-LION | Via FLAME, dead |
| Hermes → flame custom_provider | DEPRECATED, marked "do not use" |

## Unified Architecture Proposal

```
HERMES config.yaml (single fallback chain)
  │
  ▼
FED ROUTER (:7074) — single intelligence plane
  ├── Balance tracking
  ├── Latency telemetry
  ├── Constitutional tiering
  ├── Route scoring
  └── Provider health
       │
       ├── Paid: Qwen Token Plan (multi-seat)
       ├── Paid: MiniMax (quota-based)
       ├── Paid: DeepSeek (direct)
       └── Free: Groq (direct, no wrapper)
```

### What Gets Removed

| Component | Reason | Savings |
|---|---|---|
| `flame-api.service` | Dead — auto-restart loop | 17MB peak |
| `flame.service` | Engine without API = useless | 48MB |
| `litellm-proxy.service` | Redundant — FED supersedes | 320MB |
| FLAME custom_provider (Hermes config) | Deprecated | Config entropy |
| LiteLLM config.yaml | No more consumers | 198 lines |

### What Stays

- **FED Router** — already has all the intelligence
- **Direct provider connections** — Qwen TP, MiniMax, DeepSeek, Groq
- **Single fallback chain** in Hermes config.yaml
- **kunci-mas.env** — single key surface (Arif's preference: "API key itself is stupid architecture")

## Migration Path (Canary Doctrine)

1. **F13 verdict** — Arif approves the unified architecture
2. **Wire Groq direct** — add as Hermes fallback provider, verify latency
3. **Canary test** — 24h with Groq direct in fallback chain
4. **Remove LiteLLM from fallback** — stop routing through :4000
5. **Stop dead services** — `systemctl stop flame-api flame litellm-proxy`
6. **Verify** — 48h observation, no regression
7. **Disable units** — `systemctl disable` all three
8. **Clean config** — remove deprecated entries from Hermes config.yaml
9. **Seal** — arif_seal the migration

## Constitutional Note

This audit is OBSERVE_ONLY. No mutation without F13 sovereign approval.
The proposal removes 368MB of RAM, 3 config files, and 7 dead code paths.
All three layers were built with good intent in their era — this is consolidation, not criticism.
