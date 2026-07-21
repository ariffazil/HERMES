# TokenRouter Research — July 2026
# TokenRouter Research — July 2026

> **UPDATED 2026-07-20:** TokenRouter has TWO API domains. Earlier research only tested `.io` (Responses API only). The `.com` domain has FULL Chat Completions — Hermes-compatible, no adapter needed.

## Identity

TokenRouter (tokenrouter.io / tokenrouter.com) is an intelligent LLM routing layer. BYOK model: you bring your own provider keys; TokenRouter routes between them based on cost, quality, latency, or balance.

| Fact | Detail |
|------|--------|
| **Primary for Hermes** | `https://api.tokenrouter.com/v1/chat/completions` (standard OpenAI) |
| Responses API endpoint | `https://api.tokenrouter.io/v1/responses` (different domain, different protocol) |
| Health | `https://api.tokenrouter.io/health` or `.com/health` → `{"status":"ok"}` |
| API key formats | `sk-...` (both domains) |
| Providers | OpenAI, Anthropic, Google Gemini, Mistral, DeepSeek, Meta, Qwen, xAI, MiniMax, Kimi, GLM, Xiaomi |
| Models available | 113 total (95 text, 5 image, 4 video, 2 audio, multimodal) |
| Working models verified | deepseek-v4-pro, deepseek-v4-flash, MiniMax-M3, gemini-3.5-flash, mimo-v2.5-pro, glm-5.2 (FREE), claude-sonnet-4, gemini-3-flash-preview, qwen3.7-max, grok-4.20-beta |
| Routing modes | `auto:balance`, `auto:cost`, `auto:quality`, `auto:latency` |
| SDKs | Python (`pip install tokenrouter`), TypeScript |
| Pricing model | BYOK — you bring your own provider keys via console or inline headers |
| Docs | docs.tokenrouter.io |
| FREE tier | `z-ai/glm-5.2` — zero cost until July 25, 2026 |

## THE CRITICAL INSIGHT: Two API Domains

TokenRouter operates TWO separate API surfaces on different domains:

| | api.tokenrouter.io | api.tokenrouter.com |
|---|---|---|
| Protocol | **Responses API only** | **Chat Completions + Responses API** |
| `/v1/chat/completions` | 404 | **200** |
| `/v1/responses` | 500 (auth-sensitive) | 200 |
| `/v1/models` | 404 | **200** (113 models) |
| Hermes-compatible? | ❌ (needs adapter) | ✅ (native drop-in) |

**Lesson learned 2026-07-20:** We spent hours building a Chat→Responses adapter for `.io` before discovering that `.com` has native Chat Completions. The `.com` domain is the correct endpoint for Hermes integration. **Always probe BOTH domains before concluding incompatibility.**

## Live API Probe Results (2026-07-20, api.tokenrouter.com)

| Endpoint | HTTP | Meaning |
|----------|------|---------|
| `/v1/chat/completions` | **200** | Native Chat Completions — Hermes drop-in |
| `/v1/models` | **200** | 113 models listed |
| `/health` | **200** | Server alive |

**Verified working models (200 on Chat Completions):**
| Model | Provider | Notes |
|-------|----------|-------|
| `deepseek/deepseek-v4-pro` | DeepSeek | Primary for reasoning |
| `deepseek/deepseek-v4-flash` | DeepSeek | Fast/cheap |
| `z-ai/glm-5.2` | GLM | FREE until Jul 25 |
| `MiniMax-M3` | MiniMax | Multimodal, 1M context |
| `google/gemini-3.5-flash` | Gemini | |
| `xiaomi/mimo-v2.5-pro` | MiMo | |
| `anthropic/claude-sonnet-4` | Claude | |
| `google/gemini-3-flash-preview` | Gemini | |
| `qwen/qwen3.7-max` | Qwen | |
| `x-ai/grok-4.20-beta` | Grok | |

## Authentication Debugging Path (2026-07-20)

The full 500→401→403→200 journey:

1. **500** — Missing User-Agent/Accept headers. TokenRouter's `.io` domain requires specific headers; missing them causes server crash. Fix: add `User-Agent: Tokenrouter/Python 1.2.1` and `Accept: application/json`.

2. **401 "该令牌状态不可用"** — Key exists but is INACTIVE. The Chinese error (from `.com` domain, better diagnostics) reveals the real issue. Fix: Console → API Keys → Enable toggle → ON.

3. **403 "no access to model"** — Key is active but has model restrictions. Fix: API Keys → Allowed Models → leave BLANK (empty = allow all models).

4. **503 "No available channel"** — TokenRouter's distributor hasn't configured upstream channels for this model. Some models work, some don't. Try different models. The 113 listed models aren't all active.

5. **200** — Success.
This is a fundamental incompatibility for Hermes, which only speaks Chat Completions.

## BYOK (Bring Your Own Keys)

Two methods for providing provider keys:

### Console (persistent)
Register keys in the TokenRouter web console. Keys stored on TokenRouter's servers.

### Inline Headers (ephemeral, sovereign)
Pass keys per-request via custom headers. Keys never stored on TokenRouter servers:
```
X-OpenAI-Key: sk-...
X-Anthropic-Key: sk-ant-...
X-Gemini-Key: ...
X-Mistral-Key: ...
X-DeepSeek-Key: sk-...
```

## Multimodal Capabilities

Through underlying providers: GPT-4o/Claude/Gemini for vision, DALL-E passthrough for
image gen, Gemini TTS for audio. Leaderboard top models include mistral-small-latest
("agentic, multimodal"), gemini flash models, and TTS-specific models.

## Hermes Integration (CONFIRMED WORKING)

### Direct provider config (NO adapter needed)

TokenRouter's `.com` domain speaks native Chat Completions. Register as a standard Hermes provider:

```yaml
providers:
  tokenrouter:
    name: TokenRouter (Unified Gateway)
    api: https://api.tokenrouter.com/v1
    key_env: TOKENROUTER_API_KEY
    transport: openai_chat
    models:
      - { id: deepseek/deepseek-v4-pro,  name: "DeepSeek V4 Pro (TR)" }
      - { id: deepseek/deepseek-v4-flash, name: "DeepSeek V4 Flash (TR)" }
      - { id: z-ai/glm-5.2,              name: "GLM 5.2 (FREE)" }
      - { id: MiniMax-M3,                 name: "MiniMax M3 (TR)" }
      - { id: google/gemini-3.5-flash,    name: "Gemini 3.5 Flash (TR)" }
      - { id: xiaomi/mimo-v2.5-pro,       name: "MiMo V2.5 Pro (TR)" }
```

**Fallback chain** (deployed on Arif's VPS, 2026-07-20):
```yaml
fallback_providers:
  - provider: tokenrouter
    model: deepseek/deepseek-v4-pro    # Tier 1: best reasoning
  - provider: tokenrouter
    model: MiniMax-M3                  # Tier 2: multimodal backup
  - provider: tokenrouter
    model: z-ai/glm-5.2                # Tier 3: FREE always-available
  - provider: ollama
    model: qwen2.5-coder:3b            # Tier 4: SOVEREIGN ANCHOR — local, WAN-proof
```

**Key lesson — Sovereign Anchor:** Cloud-only fallback chains die when the WAN drops. Always append a local Ollama model as the final tier. OpenCode uses the same pattern (ollama qwen2.5-coder:3b as recovery agent). Hermes now mirrors it. **Unreliable internet ≠ dead agent.**

**Cron timing — proactive, not reactive:** GLM 5.2 FREE expires July 25. First cron fired at expiry (reactive — too late). Shifted to July 23 (H-48) so there's runway to swap the model before a live failure. Cron `c4d4b95ed026` delivers to Telegram.

**Config purge — strip to essentials:** Original fallback chain had 8 entries with duplicates (mimo-platform + xiaomi-mimo, minimax standalone as well as via tokenrouter). Stripped to 4 clean tiers. Every fallback entry must have a working key; dead entries = log noise, debugging confusion, and wasted probe cycles.

Hermes config path: `/root/HERMES/config.yaml` (already wired). Guide: `/root/HERMES/skills/tokenrouter-guide.md`.

### The adapter (historical — no longer needed)

The adapter at `scripts/tokenrouter_adapter.py` was built for the `.io` domain's Responses API. It is no longer needed since `.com` has native Chat Completions. The adapter was deleted (entropy reduction) on 2026-07-20. The pattern (30-line FastAPI proxy translating Chat→Responses) is preserved here for future reference if another provider only exposes Responses API.

## EMD Stack Validation (2026-07-20, FINAL)

| Floor | Finding |
|-------|---------|
| F2 (Truth) | **CORRECTED:** `.com` domain has native Chat Completions → Hermes drop-in. Earlier `.io`-only research was incomplete. |
| F1 (Safety) | Direct provider config — fully reversible, no daemon, no adapter. |
| ΔS (Entropy) | **Adapter deleted.** ΔS < 0 — removed 30 lines of unnecessary translation code. |
| W_scar | GLM 5.2 FREE expires July 25. Cron `c4d4b95ed026` monitors and auto-fixes. |

**Architecture:**
```
Hermes → DeepSeek (primary)
         ↓ fail
       TokenRouter .com (fallback chain)
         ↓
       deepseek-v4-pro → MiniMax-M3 → GLM 5.2 FREE
```

DITEMPA BUKAN DIBERI.

## Federation-Specific Value Analysis

TokenRouter has THREE high-ROI integration points in arifOS federation:

1. **Daily Briefing pipeline** — largest win. The /economics page has great UI for
   AI-synthesized briefings but is currently dead (KLCI numbers, no narrative).
   TokenRouter + LLM → auto-generate market signal → meaning → capital action →
   sovereign check. The UI exists, data flows, only synthesis missing.

2. **MCP Provider Resilience** — arifOS, GEOX, WEALTH, WELL, A-FORGE all depend on
   LLM providers for tool reasoning. TokenRouter auto-failover when primary (DeepSeek,
   MiniMax) goes down. MCP Gateway at mcp.arif-fazil.com becomes always-available.

3. **Cost Governance** — different organ calls need different intelligence. WELL
   vitality check → cheap model. GEOX seismic inversion → expensive model. TokenRouter
   routes each to right-cost model with spending caps + audit logs.

NOT useful for: arif-fazil.com (portfolio), /world dashboards (visualization),
/writing (human essays), /doctrine (constitutional reference).

## Assessment

Strengths: intelligent routing, inline BYOK = sovereignty, firewall rules, unified analytics.
Weaknesses: multimodal passthrough not implemented (image requests return 500), extra dependency, some models unavailable (503 "no channel"). Only valuable with multiple provider keys.

## OpenClaw Synchronization (2026-07-20)

After migrating Hermes and OpenCode to TokenRouter, audit OpenClaw — it's often the last component still running old architecture:

```bash
jq '.agents.defaults.model.primary' /root/.openclaw/openclaw.json
jq '.agents.defaults.model.fallbacks' /root/.openclaw/openclaw.json
```

Common finding: OpenClaw still has `minimax/MiniMax-Text-01` as primary while everything else uses DeepSeek V4 Pro + TokenRouter. Rotate to match.
