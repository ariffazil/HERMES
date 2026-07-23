# SearxNG — Self-Hosted Meta-Search

**Deployed:** 2026-07-08 | **Patched:** 2026-07-21 (engine multiplexing + caching)  \n**Container:** `searxng` (image: `searxng/searxng:latest`)  \n**Port:** `127.0.0.1:8080` (localhost only)  \n**Compose:** `/root/searxng/docker-compose.yml`  \n**Settings:** `/root/searxng/settings.yml` (bind-mounted to `/etc/searxng/settings.yml:ro`)  \n**Repo:** `ariffazil/searxng` (canonical — GitHub, public)  \n**Cache:** Redis-backed, 600s TTL, 1000 entry max  \n**Restart:** `unless-stopped`  \n**RAM:** ~200MB

## What It Provides

**What It Provides**\n\nSelf-hosted meta-search aggregating DuckDuckGo, Google, Wikipedia, and arXiv. JSON API at `/search?q=<query>&format=json`. Zero API key, zero per-query cost, zero rate limits beyond your own infra. **No MCP wrapper needed** — any agent or process on localhost can `curl` directly. The older `ask-search` MCP (`/opt/ask-search/mcp/server.py`) has been replaced by direct HTTP access + Hermes backend config.\n\n**For warga AAA:** clone `github.com/ariffazil/searxng`, run `docker compose up -d`, point agent at `http://localhost:8080/search?q=...&format=json`.

## Configuration

- **Compose:** `/root/searxng/docker-compose.yml`
- **Settings:** `/root/searxng/settings.yml` — bind-mounted to `/etc/searxng/settings.yml:ro` in container. **Edit on host, not in container.**
- **Secret:** inline in compose `SEARXNG_SECRET` env var

### Multi-Engine Sovereign Config (patched 2026-07-21)

```yaml
use_default_settings: true
engines:
  - name: duckduckgo        # Primary: free, no API key, always on
    engine: duckduckgo
  - name: google            # Fallback: Google via CSE
    engine: google
  - name: brave             # Backup: different exit IP than DDG
    engine: brave
    disabled: false
    api_key: "${BRAVE_API_KEY}"    # From vault.env
  - name: wikipedia
    engine: wikipedia
  - name: arxiv
    engine: arxiv
```

**Why multiplexing matters:** If DuckDuckGo blocks your homelab IP (rate limiting), SearXNG silently rotates to Google. The agent never sees the failure. Each engine exits through different IPs/ASNs.\n\n**⚠️ Engine hang pitfall (2026-07-21):** Brave engine without an API key hangs indefinitely in web scrape mode → all SearXNG requests timeout. **Fix:** `disabled: true` for non-functional engines. Test each engine individually: `curl --max-time 5 "http://127.0.0.1:8080/search?q=test&format=json&engines=<name>"`. If it doesn't return in under 3 seconds, disable it.

### Redis Caching (patched 2026-07-21)

```yaml
redis:
  url: unix:///run/redis-searxng/redis.sock?db=0
cache:
  search_cache: true
  search_cache_ttl: 600     # 10 min — identical queries served from cache
  search_cache_max_size: 1000
```

Zero redundant upstream requests for repeated queries. Same query from 5 agents within 10 minutes = 1 upstream request, 4 cache hits.

### Hermes Integration

```bash
# Route ALL Hermes web search through local SearXNG
hermes config set web.search_backend searxng
hermes config set web.backend searxng
hermes config set web.extract_backend searxng
```

**⚠️ Split-brain pitfall:** Hermes config has TWO search sections — `web:` (used by `web_search` tool) and `search:` (used by search-only toolset). Both must point to the same backend. Verify with:
```bash
grep "search_backend\|backend:" /root/.hermes/config.yaml | grep -v "^#" | grep -v "^$"
```

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
# Health + engine coverage
curl -s "http://127.0.0.1:8080/search?q=test&format=json" | python3 -c "
import sys,json; d=json.load(sys.stdin)
engines=set(r.get('engine','?') for r in d.get('results',[]))
print(f'{len(d.get(\"results\",[]))} results from engines: {engines}')
"
# Expected: results from duckduckgo + google cse (brave may appear later)

# Isolated engine test
curl -s "http://localhost:8080/search?q=test&format=json&engines=duckduckgo" | python3 -c "
import sys,json; d=json.load(sys.stdin); print(f'DDG only: {len(d.get(\"results\",[]))} results')
"
```

## Federation Integration

**Hermes:** Routed via `web.search_backend: searxng` (config change 2026-07-21). See Hermes Integration section above.

**OpenCode/OpenClaw:** Inherit through federation routing — OpenCode calls A-FORGE proxy tools or curl `:8080` direct, OpenClaw delegates to Hermes which uses SearXNG. No per-agent config needed.

**WM trajectory log:** SearXNG itself is not instrumented, but any `forge_*` call that uses search results logs the full action→observation pair to `/root/.local/share/arifos/world-model/trajectories.jsonl`.
**forge_fetch search mode** (already live): `forge_fetch(query="...", mode="search", num_results=5)` routes through SearxNG `localhost:8080`. Code at `A-FORGE/src/interfaces/mcp/proxyTools.ts:994-1031`. No separate tool needed — one primitive, two faces.
