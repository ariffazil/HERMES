---
name: deep-research-deployment
description: Deploy and maintain the u14app/deep-research MCP server as a federated research organ
trigger: When deploying deep research or reconfiguring its MCP/LLM/Search providers
---

# deep-research Deployment & Operations

Deploy `u14app/deep-research` as an MCP research organ alongside Hound, SearXNG, and OpenRouter.

**Related:** OpenRouter provider routing governed by `skill:provider-routing-zen` — see that skill for CQT dial, ZDR enforcement, session stickiness, binding constraints, and the 3-loop key rotation procedure. deep-research injects the OpenRouter API key via `OPENAI_API_KEY` env var — when rotating keys, Loop 3 must include redeploying this container.

## Reference Files

- `references/openrouter-integration-state-2026-07-24.md` — verified deployment state snapshot with credit balance, key assets, Hermes config wiring, and key rotation notes after OpenRouter zen consolidation. Load this before re-deploying or auditing.

## Architecture

```
Hermes/Hound (sensor)     ← quick search, fetch, crawl
deep-research (pipeline)  ← plan → search → collect → synthesize → report
SearXNG (self-hosted)     ← private search backend (port 8080)
OpenRouter (routing)      ← auto-beta model selection (cost/quality dial)
```

## Deployment

```bash
# Core deployment — OpenRouter + SearXNG bridge
docker run -d --name deep-research --restart unless-stopped \
  -p 3333:3000 \
  --network af-forge_default \
  -e ACCESS_PASSWORD="<from vault.env:DEEP_RESEARCH_PASSWORD>" \
  -e OPENAI_API_KEY="${OPENROUTER_API_KEY}" \
  -e OPENAI_API_BASE_URL="https://openrouter.ai/api/v1" \
  -e SEARXNG_BASE_URL="http://searxng:8080" \
  -e SEARXNG_API_BASE_URL="http://searxng:8080" \
  -e NEXT_PUBLIC_ENABLE_LOCAL_KB="true" \
  -e MCP_AI_PROVIDER="openai" \
  -e MCP_SEARCH_PROVIDER="searxng" \
  -e MCP_THINKING_MODEL="openrouter/auto-beta" \
  -e MCP_TASK_MODEL="openrouter/auto-beta" \
  xiangfa/deep-research:latest
```

**Alternative: Host bridge mode** (SearXNG on host, not in Docker network):

```bash
docker run -d --name deep-research --restart unless-stopped \
  -p 3333:3000 \
  -e ACCESS_PASSWORD="<from vault.env:DEEP_RESEARCH_PASSWORD>" \
  -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
  -e SEARXNG_API_BASE_URL="http://host.docker.internal:8080" \
  -e MCP_AI_PROVIDER="deepseek" \
  -e MCP_SEARCH_PROVIDER="searxng" \
  -e MCP_THINKING_MODEL="deepseek-reasoner" \
  -e MCP_TASK_MODEL="deepseek-chat" \
  -e NEXT_PUBLIC_ENABLE_LOCAL_KB="true" \
  xiangfa/deep-research:latest
```

Use host bridge when SearXNG runs on the host (port 8080) not in Docker. `host.docker.internal` resolves to Docker host on this VPS — test with `docker run --rm alpine curl -s -I http://host.docker.internal:8080` before deploying. No `--network` flag needed — default bridge mode gives host access.
```

## MCP Server Config (Hermes ~/.hermes/config.yaml)

```yaml
mcp_servers:
  deep-research:
    description: Deep Research Engine — multi-LLM iterative research, SearXNG-backed, report synthesis
    transport: streamable-http
    url: http://127.0.0.1:3333/api/mcp
    headers:
      Authorization: Bearer <ACCESS_PASSWORD>
    timeout: 600
```

## Provider Options

| Provider | Env Vars | Notes |
|----------|----------|-------|
| **OpenRouter via OpenAI (recommended)** | `OPENAI_API_KEY`, `OPENAI_API_BASE_URL=https://openrouter.ai/api/v1` | Auto-beta routing, zero extra router fee. Use `openrouter/auto-beta` as both thinking AND task model — auto-beta classifies per prompt. **⚠️ Credit status:** Verify key has credits with `curl /api/v1/auth/key` before assuming paid models work. This workspace was consolidated to org arifOS 2026-07-24 with $30 topup — `is_free_tier: false`. See `skill:provider-routing-zen` for key rotation and credit management. |
| **Groq (free)** | `OPENAI_API_KEY`, `OPENAI_API_BASE_URL=https://api.groq.com/openai/v1` | RM0, ~15 models |
| **DeepSeek direct** | `DEEPSEEK_API_KEY`, `DEEPSEEK_API_BASE_URL` | Direct API |
| **Anthropic BYOK** | `ANTHROPIC_API_KEY`, `ANTHROPIC_API_BASE_URL` | Via DeepSeek proxy |

## Search Provider Options

| Provider | Env Vars | Notes |
|----------|----------|-------|
| **SearXNG** | `SEARXNG_BASE_URL=http://searxng:8080` | Self-hosted, $0, same network |
| **Tavily** | `TAVILY_API_KEY` | Paid, more structured results |

## MCP Tools (5)

- `deep-research` — Full pipeline: plan → search → synthesize → report
- `write-research-plan` — Generate structured research plan
- `generate-SERP-query` — Generate search task list from plan
- `search-task` — Execute search + collect results
- `write-final-report` — Synthesize collected data into report

## Key Env Var Differences from README

- Uses `OPENAI_API_BASE_URL` not `OPENAI_BASE_URL` (env.tpl naming)
- `SEARXNG_API_BASE_URL` also needed alongside `SEARXNG_BASE_URL`
- Must be on same Docker network as SearXNG for DNS resolution

## Network

**Docker network mode:** Container runs on `af-forge_default` network for SearXNG DNS access (`http://searxng:8080`). Port `3333` exposed to host for Hermes MCP.

**Host bridge mode:** No `--network` flag — default bridge. SearXNG accessed via `http://host.docker.internal:8080`. Test connectivity before deploying with `docker run --rm alpine curl -s -I http://host.docker.internal:8080` (expect HTTP 200). `host.docker.internal` IS reliable on this VPS — Docker routes it to the host.

## Troubleshooting

- **"Insufficient credits" / 402**: API key is valid but workspace has 0 credits. Check with `curl /api/v1/credits -H "Authorization: Bearer $KEY"`. As of 2026-07-24, this workspace was consolidated to org arifOS with $30 topup — workspaces merged, key has credits. If 402 persists, the API key and topup may be on different workspaces — verify at openrouter.ai/settings/credits.
- **Docker env vars captured at launch**: Updating vault.env alone does NOT update the deep-research container — it captured the API key at `docker run`. Must `docker rm -f deep-research` + re-run with new key. Verify with `docker exec deep-research env | grep OPENAI` after re-deploy.
- **searxng/.env is a symlink → vault.env**: `/root/searxng/.env → /root/.secrets/vault.env`. Writing to vault.env auto-updates searxng. Symlinks always show permissions 777 (Linux kernel default) — the target file's real permissions (600 root:root) are what matters.
- **"Not Found"**: OpenRouter model name mismatch — use exact IDs from /v1/models
- **"searxng: fetch failed"**: Container not on same Docker network as SearXNG
- **ECONNRESET**: Transient network error on long-running tasks — retry
- **Empty plan**: Model returned empty — check API credits/quota
- **Timeout >180s**: Expected for complex deep-research — set timeout ≥600s
