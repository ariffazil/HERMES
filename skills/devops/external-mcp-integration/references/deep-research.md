# Deep Research (u14app/deep-research)

Third-party MCP server providing multi-stage research report synthesis with separated thinking/task models and configurable web search.

- **Repo**: https://github.com/u14app/deep-research
- **License**: MIT
- **Image**: `xiangfa/deep-research:latest`
- **Deployed**: Port 3333, container name `deep-research`
- **MCP**: Streamable HTTP at `http://localhost:3333/api/mcp` with Bearer auth
- **Current LLM**: OpenRouter auto-beta (via OpenAI-compatible endpoint)
- **Current search**: SearXNG self-hosted (`:8080`, same Docker network)

## Deployment

```bash
# Recommended: OpenRouter + SearXNG on same Docker network
docker run -d --name deep-research --restart unless-stopped \
  -p 3333:3000 \
  --network af-forge_default \
  -e ACCESS_PASSWORD="<generated-password>" \
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

**Key deployment lessons:**
- `host.docker.internal` is NOT reliable on Linux — use Docker network (`--network af-forge_default`) and DNS name (`http://searxng:8080`)
- `OPENAI_API_BASE_URL` NOT `OPENAI_BASE_URL` (env.tpl naming)
- Both `SEARXNG_BASE_URL` AND `SEARXNG_API_BASE_URL` are needed
- `openrouter/auto-beta` as both thinking AND task model = task-aware routing, no fixed split needed
- Timeout must be ≥600s for full research pipelines

## MCP Tools Exposed (5 tools)

| Tool | Description | Key Params |
|------|-------------|------------|
| `deep-research` | One-shot: plan → search → synthesise → full report | query (req), language, maxResult, enableCitationImage, enableReferences |
| `write-research-plan` | Generate research plan from query | query (req), language |
| `generate-SERP-query` | Generate search queries from plan | plan (req), language |
| `search-task` | Execute search and collect results | tasks[] (req), language, maxResult |
| `write-final-report` | Write final report from plan + task results | plan (req), tasks[] (req), language, maxResult |

## Hermes Config

```yaml
mcp_servers:
  deep-research:
    description: "Deep Research Engine — multi-LLM iterative research, SearXNG-backed, report synthesis"
    transport: streamable-http
    url: http://127.0.0.1:3333/api/mcp
    headers:
      Authorization: "Bearer <password>"
    timeout: 600
```

## Architecture Zen

```
Hound (10-engine search + fetch)  ← complementary →  deep-research (report synthesis)
                                                       ↕
                                                    SearXNG (self-hosted, :8080, af-forge_default)
                                                       ↕
                                                 OpenRouter auto-beta (task-aware routing)
```

Hound = sensor layer (low latency). deep-research = metabolizer layer (high latency, stateful). They compose, not overlap.

## Environment Variables

| Env Var | Purpose | Example |
|---------|---------|---------|
| `ACCESS_PASSWORD` | Bearer token for MCP auth | random hex string |
| `OPENAI_API_KEY` | OpenRouter API key (or any OpenAI-compatible LLM key) | `${OPENROUTER_API_KEY}` |
| `OPENAI_API_BASE_URL` | Base URL for OpenAI-compatible API | `https://openrouter.ai/api/v1` |
| `SEARXNG_BASE_URL` | Self-hosted search backend (via Docker DNS) | `http://searxng:8080` |
| `SEARXNG_API_BASE_URL` | Same as SEARXNG_BASE_URL (both needed) | `http://searxng:8080` |
| `MCP_AI_PROVIDER` | LLM provider for MCP mode | `openai`, `google`, `anthropic`, `deepseek`, `openrouter` |
| `MCP_SEARCH_PROVIDER` | Search backend for MCP mode | `searxng`, `model`, `tavily`, `brave` |
| `MCP_THINKING_MODEL` | Reasoning model (auto-beta = task-aware) | `openrouter/auto-beta` |
| `MCP_TASK_MODEL` | Writing model (auto-beta = task-aware) | `openrouter/auto-beta` |
| `NEXT_PUBLIC_ENABLE_LOCAL_KB` | Upload PDF/Office files as research sources | `true` |

## Notes

- Timeout must be ≥600s — deep research involves multiple LLM calls + search rounds
- SearXNG on same Docker network (`af-forge_default`) at `http://searxng:8080`
- No external search API key needed — SearXNG covers it at $0
- Web UI at `http://localhost:3333` for manual research sessions
- MCP endpoint requires Bearer auth header (ACCESS_PASSWORD)
- Container version may lag 1-2 days behind latest release — update notice is normal
- Workspace is free tier (0 credits) — verify key credits with `curl /api/v1/auth/key`
