# deep-research + OpenRouter Integration — Verified State (2026-07-24)

**Snapshot taken after 3-loop audit + chaos test.** For rollback or next audit.

## Deployment State

| Parameter | Value |
|-----------|-------|
| Container | `xiangfa/deep-research:latest` |
| Port | `:3333` → `3000` |
| Network | `af-forge_default` (SearXNG DNS: `http://searxng:8080`) |
| MCP endpoint | `http://127.0.0.1:3333/api/mcp` |
| Auth | Bearer from `${DEEP_RESEARCH_PASSWORD}` in the process environment |
| Tools | 5 — `deep-research`, `write-research-plan`, `generate-SERP-query`, `search-task`, `write-final-report` |
| Timeout | 600s (Hermes config) |

## Provider Config

| Env Var | Value |
|---------|-------|
| `OPENAI_API_KEY` | `${OPENROUTER_API_KEY}` (from vault.env, 97-char ORG key `arifOS-federation-20260724`) |
| `OPENAI_API_BASE_URL` | `https://openrouter.ai/api/v1` |
| `MCP_AI_PROVIDER` | `openai` |
| `MCP_THINKING_MODEL` | `openrouter/auto-beta` |
| `MCP_TASK_MODEL` | `openrouter/auto-beta` |

## Search Config

| Env Var | Value |
|---------|-------|
| `MCP_SEARCH_PROVIDER` | `searxng` |
| `SEARXNG_BASE_URL` | `http://searxng:8080` |
| `SEARXNG_API_BASE_URL` | `http://searxng:8080` |

## Key Assets

| File | Purpose |
|------|---------|
| `/root/.secrets/vault.env` | API + management keys (97-char ORG keys, line 68, 70) |
| `/root/searxng/.env` | Symlink → vault.env (mode 600) |
| `/root/.hermes/config.yaml.ba.k.pre-openrouter` | Pre-OpenRouter config |
| `/root/.secrets/vault.env.bak.zen-openrouter-20260724-060510` | Pre-zen key snapshot |

## Credit Status

- Workspace: org arifOS (f5be0c4e)
- Balance: **$30.00** (topped up 2026-07-24)
- `is_free_tier: false`
- Inference: ✅ auto-beta → `deepseek/deepseek-v4-flash`
- MCP: ✅ 5 tools responding
- Verify: `curl /api/v1/credits -H "Authorization: Bearer $KEY"`

## Hermes Config Wiring

```yaml
# In /root/.hermes/config.yaml:
mcp_servers:
  deep-research:
    description: Deep Research Engine — multi-LLM iterative research, SearXNG-backed
    transport: streamable-http
    url: http://127.0.0.1:3333/api/mcp
    headers:
      Authorization: "Bearer ${DEEP_RESEARCH_PASSWORD}"
    timeout: 600
```

## Key Rotation Note (2026-07-24)

Original workspace had 3 messy keys and 0 credits. Zen process:
1. Consolidated to single org key `arifOS-federation-20260724`
2. Topped up $30 → workspace now has spend authority
3. Old leaked management key disabled via UI
4. vault.env written with full 97-char key
5. Do NOT rotate again unless key is compromised — "bodoh x payah la rotate buat semak kacau bilau"
