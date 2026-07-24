# OpenRouter Canonical Docs — 2026-07-24 Session State

Three docs now sit under `/root/AAA/docs/`:

| Doc | Audience | Lines | Focus |
|-----|----------|-------|-------|
| `OPENROUTER_ZEN_OPTIMIZATION.md` | F13 / strategic | 525 | Constitutional doctrine — when OR is allowed, when forbidden |
| `OPENROUTER_AGENT_GUIDE.md` | Any AAA agent | 593 | Operational mechanics — how to call OR, CQT, ZDR, models |
| `OPENROUTER_HERMES_OPS.md` | Hermes session | 429 | Hermes-specific — profiles, Telegram patterns, MY override, failure modes |

## OpenRouter MCP Server

- **Endpoint:** `https://mcp.openrouter.ai/mcp` (streamable-http)
- **Tools:** model discovery, credit monitoring, benchmark tools
- **Auth:** OAuth — one-time approval via `codex mcp login openrouter` or `claude mcp login openrouter`
- **Status (2026-07-24):** Registered in `mcp_servers.openrouter` in config.yaml but NOT yet OAuth-approved
- **Blocker:** Requires management key rotation first (key was briefly exposed in chat)
- **Registration in config.yaml:**
  ```yaml
  mcp_servers:
    openrouter:
      description: OpenRouter MCP — model discovery, credit monitoring, benchmark tools
      transport: streamable-http
      url: https://mcp.openrouter.ai/mcp
      auth: oauth
      enabled: true
      headers: {}
      timeout: 30
  ```

## FLAME vs OpenRouter — The Two-Lane Architecture

| Lane | Domain | Controls | Route | Status |
|------|--------|----------|-------|--------|
| **FLAME** | Tool model inference | `flame_config.json`, 35 eligible tools | Groq→SEA-LION→Gemini→Cerebras→OR/free→Ollama | Active |
| **OpenRouter** | Agent intelligence | `fallback_providers[]`, CQT | Direct→auto-beta cqt=5→OR/free→Ollama | Patched, waiting restart |
| **DeepSeek direct** | Identity + constitutional | Hardcoded in agent_init | 000_INIT, 666_JUDGE, 999_SEAL, MY gov | Active (unchanged) |

**Key principle:** Tool output must never enter the governed cascade. Agent output must never route through FLAME. Separate lanes, separate concerns.

## Deep-Research as OpenRouter Consumer

Deep-research (`:3333`) now routes through the same OpenRouter credit pool:
- **Provider:** `openai` (OpenRouter-compatible endpoint)
- **Thinking model:** `openrouter/auto-beta` (task-aware routing)
- **Task model:** `openrouter/auto-beta`
- **Search:** SearXNG (`:8080`, same Docker network)
- **Cost:** Shares the $28.08 OpenRouter credit with Hermes agent
- **MCP:** 5 tools registered at `http://localhost:3333/api/mcp` with Bearer auth

## Pricing Summary

| Route | Cost/M Input | Cost/M Output | Annual |
|-------|-------------|--------------|--------|
| deepseek-v4-flash (direct) | $0.14 | $0.28 | ~$63.60 at current burn |
| openrouter/auto-beta (cqt=5) | Same as selected model | Same | $0 extra |
| openrouter/free | $0 | $0 | $0 |
| ollama/qwen2.5-coder:3b | $0 | $0 | $0 |
| Projected Hermes monthly | ~$5.30 | — | ~$63.60 |
| Remaining OR credit | $28.08 | — | ~5.3 months at current burn |

## Binding Constraints (Hard Rules)

These NEVER route through OpenRouter — confirmed and operationalized this session:

1. **000_INIT** — Identity binding needs sovereign direct connection
2. **666_JUDGE** — Constitutional verdict; OR has `identity_verified: false`
3. **999_SEAL** — Irreversible commitment; F13 trust required
4. **MY Governance** — Najib, 1MDB, PETRONAS, Jho Low, myKad — hard route DeepSeek V4 Pro direct
5. **MiniMax** — SHADOW-MM-001 silent MY censorship — must NEVER pass through auto-beta routing
6. **apex persona** (`hermes_apex` profile) — Constitutional review; F1 AMANAH requires escalation to arifOS kernel, not community spend-share voting

## Remaining Blockers (888_HOLD)

1. ~~**Rotate management key**~~ ✅ **DONE 2026-07-24** — Single zen org key `arifOS-federation-20260724`, vault.env updated, old keys purged
2. ~~**Gateway restart**~~ ✅ **DONE 2026-07-24** — hermes-asi-gateway restarted, fallback chain active
3. **OAuth approve OpenRouter MCP** — needs interactive browser flow (`hermes mcp login openrouter`)

## Zen Org Key State (2026-07-24)

| Field | Value |
|-------|-------|
| Key name | `arifOS-federation-20260724` |
| Workspace | `f5be0c4e-caee-591f-ba95-41a1bd6cba72` |
| vault.env var | `OPENROUTER_API_KEY` (line 68) |
| Sub-keys active | 1 (zen single-key architecture) |
| Old keys deleted | 3 (`arifOS ` trailing-space, `arifOS-org`, `arifOS-hermes` — unrecoverable) |
| Credit tested | ✅ Live — routed to `deepseek/deepseek-v4-flash` |
| Snapshot | `/root/.secrets/vault.env.bak.zen-openrouter-20260724-060510` |
