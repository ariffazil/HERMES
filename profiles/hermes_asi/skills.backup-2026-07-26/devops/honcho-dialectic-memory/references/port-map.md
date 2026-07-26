# arifOS Federation Port Map (2026-07-24)

Active ports on the federation VPS. Check before deploying new services.

## Core Federation Organs

| Port | Service | Container/Process |
|------|---------|-------------------|
| 8088 | arifOS kernel | arifos MCP server |
| 8081 | GEOX | geox MCP server |
| 18082 | WEALTH | wealth MCP server |
| 18083 | WELL | well MCP server |
| 7071 | A-FORGE | forge execution |
| 7072 | A-FORGE MCP | forge MCP gateway |
| 3001 | AAA control plane | a2a-server |

## Infrastructure

| Port | Service | Container |
|------|---------|-----------|
| 5432 | PostgreSQL (vault999) | postgres:16-alpine |
| 6379 | Redis | redis:7-alpine |
| 6380 | FalkorDB | 826f22f7321c |
| 6333-6334 | Qdrant | qdrant/qdrant |
| 9000-9001 | MinIO | minio/minio |
| 8080 | SearXNG | searxng/searxng |

## Hermes + Gateway

| Port | Service | Container/Process |
|------|---------|-------------------|
| 18086 | Hermes Gateway MCP | hermes-asi-gateway |
| 18001 | A2A service | hermes-a2a |
| 18080 | ntfy | binwiederhier/ntfy |

## Memory + Tools

| Port | Service | Container/Process |
|------|---------|-------------------|
| 8000 | graphiti-mcp | zepai/knowledge-graph-mcp |
| 8001 | arifOS L5 search | arifosmcp.runtime.l5_search_api |
| 6274, 6277 | mcpjam-federation | mcpjam/mcp-inspector |

## Deployed in This Session (2026-07-24)

| Port | Service | Container |
|------|---------|-----------|
| 8002 | Honcho API | af-forge-api-1 (internal 8000) |
| 5433 | Honcho PostgreSQL | af-forge-database-1 (internal 5432) |
| 6381 | Honcho Redis | af-forge-redis-1 (internal 6379) |
| 9377 | Camofox Browser | camofox.service (systemd) |

## Port Conflict Resolution Pattern

When deploying a new service:
1. Check target port: `ss -tlnp | grep :<port>`
2. If occupied, find next free: `for p in $(seq <start> <end>); do ss -tlnp | grep -q ":$p " || echo $p; done | head -1`
3. For Docker: remap external port, keep internal port unchanged
4. For systemd: pass port via Environment= or env var
5. Update all config files pointing to the new port