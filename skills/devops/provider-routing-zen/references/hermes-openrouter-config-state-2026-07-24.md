# Hermes OpenRouter Config State — 2026-07-24

> **Forged:** After full OpenRouter integration session.
> **Purpose:** Snapshot of actual live config after patching. Not a SOT — verify before re-applying.

## Live Fallback Chain (10 tiers)

Applied to `/root/.hermes/config.yaml`. Backup at `config.yaml.bak.pre-openrouter`.

| Tier | Provider | Model | Role |
|------|----------|-------|------|
| T1 | tokenrouter | deepseek/deepseek-v4-pro | Primary reasoning |
| T2 | openrouter | openrouter/auto-beta | Smart failover (70+ providers, auto-failover) |
| T3 | groq | llama-3.1-8b-instant | Direct Groq fallback |
| T4 | sea-lion | aisingapore/Qwen-SEA-LION-v4-32B-IT | BM native |
| T5 | gemini | gemini-2.5-flash | Google fallback |
| T6 | cerebras | gemma-4-31b | Cerebras |
| T7 | tokenrouter | MiniMax-M3 | Note: SHADOW-MM-001 — never route MY governance |
| T8 | tokenrouter | z-ai/glm-5.2 | GLM |
| T9 | openrouter | openrouter/free | RM0 survival (50 models, 20 req/min) |
| T10 | ollama | qwen2.5-coder:3b | Local last resort |

## OpenRouter Config Section

```yaml
openrouter:
  enabled: true
  auto_fallback: true
  response_cache: true
  response_cache_ttl: 300
  min_coding_score: 0.65
  cost_quality_tradeoff: 5
  base_url: https://openrouter.ai/api/v1
```

## OpenRouter MCP Server

Registered in `mcp_servers`:
```yaml
openrouter:
  description: OpenRouter MCP — model discovery, credit monitoring, benchmarks
  transport: streamable-http
  url: https://mcp.openrouter.ai/mcp
  auth: oauth
  enabled: true
  headers: {}
  timeout: 30
```

⚠️ Needs OAuth on first connect — browser flow, approve with `OPENROUTER_MANAGEMENT_KEY`.

## Key Learnings

- **Session stickiness:** PATCHED at source level (`/usr/local/lib/hermes-agent/agent/agent_init.py` lines 952-956) — every outgoing OpenRouter call now carries `x-session-id: aaa-hermes-{agent.session_id}`. Pins model+provider for 5min inactivity. Requires gateway restart to take effect. **Was previously "requires source change" — now applied.**
- **MiniMax MUST be excluded** from auto-beta routing via `allowed_models: ["-minimax/*"]` or route sensitive topics direct to DeepSeek.
- **OpenRouter auto-beta vs auto:** `auto` was NotDiamond (deprecated, default CQT=7). `auto-beta` is OpenRouter's own router (default CQT=9). 5-step pipeline: classify → rank by task spend-share → dial filter → fallback route → graceful degrade.
- **Pricing:** DeepSeek V4 Flash $0.14/$0.28. V4 Pro $1.74/$3.48. Auto-beta adds $0 extra. $28.08 remaining, ~$0.50-1.00/session burn.
- **Reasoning control:** Available via `reasoning: {effort: "high|medium|low|minimal"}` on DeepSeek V4 Pro, Claude Sonnet, Kimi K3. Kimi K2.5 safest for reasoning with tool use.
- **Policy enforcement:** `fallback_providers[]` ignores `extra_body` / `plugins`. Must enforce OR policy (ZDR, model allowlist, budget caps) via OpenRouter Management API guardrails. Script: `/root/AAA/scripts/provision-openrouter-guardrail.py`.

## Additional Changes (2026-07-24 Final Phase)

- **`aaa_measure` ghost tool removed from `opencode_toolbench.yaml` line 67.** Declared as a plugin tool with no MCP endpoint at `:3001/mcp`. Caused OpenRouter Auto Exacto to error "No endpoints found that support tool use" — the unresolvable tool in the registration list confused the provider routing layer. Fix: `plugin_tools: []`. Audit ref: `forge_work/2026-07-24/agent5-audit/ALIAS_DEPRECATION_PLAN.md`.
- **Gateway restart NOT required.** Systemd probe confirmed `hermes-asi-gateway` active, functional. Session continued without restart.
- **Org workspace migration complete.** Single `arifOS-federation-20260724` key active. Old management key (`sk-or-v1-346...066`) still live — must disable at openrouter.ai/keys UI.
- **MCP OAuth pending.** `hermes mcp login openrouter` requires interactive browser. In headless environments, the SDK prints an authorization URL; paste the full redirect URL (including `?code=...&state=...`) back into the waiting stdin.
