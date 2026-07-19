# SearxNG — Self-Hosted Meta-Search

**Deployed:** 2026-07-08  
**Container:** `searxng` (image: `searxng/searxng:latest`)  
**Port:** `127.0.0.1:8080` (localhost only)  
**Compose:** `/root/searxng/docker-compose.yml`  
**Settings:** `/root/searxng/settings.yml`  
**Repo:** `ythx-101/ask-search` (cloned to `/opt/ask-search`)  
**CLI:** `/usr/local/bin/ask-search`  
**MCP:** `/opt/ask-search/mcp/server.py` (FastMCP, 3 tools)  
**Restart:** `unless-stopped`  
**RAM:** ~200MB

## What It Provides

Self-hosted meta-search aggregating Google, DuckDuckGo, Brave, and 70+ other engines. JSON API at `/search?q=<query>&format=json`. Zero API key, zero per-query cost, zero rate limits beyond your own infra.

## Configuration

- **Compose:** `/root/searxng/docker-compose.yml`
- **Settings:** `/root/searxng/settings.yml` — bound to `/etc/searxng/settings.yml:ro` in container
- **Secret:** inline in compose `SEARXNG_SECRET` env var

### Key settings (from settings.yml)

```yaml
use_default_settings: true  # pulls ~70 engines from SearxNG defaults
server:
  limiter: false            # no rate limiting (VPS is private)
search:
  formats: [html, json]     # JSON is required for agent/API consumption
```

Engine set is SearxNG defaults — Google, DuckDuckGo, Brave, Wikipedia, and 70+ others. No manual engine whitelist needed.

## CLI Usage

```bash
# Basic search
ask-search "query" --num 5

# JSON output
ask-search "query" --json

# News search
ask-search "query" --news

# Language filter
ask-search "query" --lang en --num 10
```

## Verification

```bash
# Health
curl -sf "http://127.0.0.1:8080/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['results']), 'results')"

# Full test
ask-search "Claude Code agent mode" --num 3
```

## Deep-Dive Limitations

SearxNG returns snippets from search indexes. When your agent needs full page content:

| Site | Search | Deep-dive | Fix |
|---|---|---|---|
| Most sites | ✅ | ✅ | — |
| Reddit | ✅ | ❌ VPS IP blocked | SSH SOCKS proxy + `.json` API |
| Zhihu | ✅ | ❌ Login wall | Delegate to local agent |
| Medium | ✅ | ⚠️ Paywall | Partial content only |

The VPS→local multi-node pattern: search on VPS, deep-dive fetch from local machine with residential IP.

## Recovery

```bash
# Restart if down (from /root/searxng/)
cd /root/searxng && docker compose restart

# Full rebuild
cd /root/searxng && docker compose down && docker compose up -d

# Check logs
docker logs searxng --tail 50
```

## Federation Integration

**forge_fetch search mode** (already live): `forge_fetch(query="...", mode="search", num_results=5)` routes through SearxNG `localhost:8080`. Code at `A-FORGE/src/interfaces/mcp/proxyTools.ts:994-1031`. No separate tool needed — one primitive, two faces.
