---
name: sovereign-search
description: "Self-host web search for Hermes Agent — SearXNG deployment, Tavily/Brave migration, config unification, and zero-API-key architecture. Use when web_search fails with quota errors (432/401/429), when adding self-hosted search, or when Arif says 'hak asasi warga AAA' for search."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, search, searxng, self-hosted, sovereign]
---

# Sovereign Search

Self-host web search backend for Hermes Agent. Eliminates external API key dependency, monthly quotas, and vendor lock-in. The principle: **own the metal, don't rent the API.**

## When to Use

- `web_search` returns 432 (quota exhausted), 401 (key invalid), or 429 (rate limited)
- Arif says "hak asasi warga AAA" for search
- You want zero-cost, zero-quota web search
- Tavily/Brave API keys are dead or about to expire

## Architecture

```
Agent → web_search → Hermes config (search_backend: searxng) → SearXNG :8080 → DuckDuckGo/Google/etc
```

SearXNG is a privacy-respecting metasearch engine. It proxies queries to upstream engines (DuckDuckGo, Google, Wikipedia, etc.) with zero API keys required for most engines.

## Quick Fix: Switch Existing Hermes to Local SearXNG

If SearXNG is already running locally (check: `curl -sI http://localhost:8080 | head -1`):

```bash
# Unify all backends to SearXNG
hermes config set web.search_backend searxng
hermes config set web.backend searxng
hermes config set web.extract_backend searxng
hermes config set search.search_backend searxng
hermes config set search.backend searxng
```

Verify no split-brain:
```bash
grep -A4 "^web:" ~/.hermes/config.yaml
grep -A3 "^search:" ~/.hermes/config.yaml
```

**Both sections must point to `searxng`.** If they differ, `web_search` may still route through the old dead backend.

Set the URL:
```bash
export SEARXNG_URL="http://127.0.0.1:8080"  # in ~/.hermes/.env or vault.env
```

**Restart required**: `/reset` the session or restart Hermes for config to take effect.

## Deploying SearXNG (if not running)

```bash
# Docker — quickest
docker run -d --name searxng \
  -p 127.0.0.1:8080:8080 \
  -v searxng-config:/etc/searxng \
  searxng/searxng:latest

# Verify
curl -s "http://127.0.0.1:8080/search?q=test&format=json" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['results']), 'results')"
```

Default config uses DuckDuckGo + Google CSE. DuckDuckGo is zero-API-key. Google CSE needs a key — disable it in settings.yml if you don't have one.

## Diagnosing Dead Backend

When `web_search` fails:

1. **Check the error**: 432 = Tavily quota, 401 = invalid key, 429 = rate limit
2. **Check current config**: `grep search_backend ~/.hermes/config.yaml`
3. **Check for split-brain**: Both `web:` and `search:` sections must agree
4. **Check SearXNG alive**: `curl -sI http://localhost:8080 | head -1` → should be 200
5. **Test SearXNG directly**: `curl -s "http://127.0.0.1:8080/search?q=test&format=json"`

If SearXNG returns results but Hermes doesn't → config or restart issue. If SearXNG itself is down → Docker restart.

## Pitfalls

- **Split-brain config**: `web.search_backend` and `search.search_backend` are DIFFERENT config keys. The `web_search` tool uses `web.*` section. Unify both.
- **Restart required**: Config changes don't take effect mid-session. Need `/reset` or Hermes restart.
- **SearXNG engine failures**: Individual upstream engines (Brave, Startpage) may rate-limit. DuckDuckGo is most reliable free engine.
- **`use_default_settings: true` pitfall**: If Brave engine is enabled in settings.yml but API key doesn't propagate, check if `use_default_settings: true` is overriding custom engine configs. Add `disabled: false` and `api_key` explicitly, then `docker restart searxng`.
- **Docker bind-mount**: If settings.yml is bind-mounted (check: `docker inspect searxng --format '{{json .Mounts}}'`), edit the HOST file (e.g. `/root/searxng/settings.yml`) then `docker restart searxng`. Do NOT edit inside the container — bind mounts are read-only.
- **DuckDuckGo IP block risk**: If 5+ agents hammer SearXNG concurrently, DuckDuckGo may block the homelab IP. Enable MULTIPLE engines for resilience — SearXNG silently rotates to the next engine if one fails.

## Verification

```bash
# 1. SearXNG alive
curl -sI http://localhost:8080 | head -1  # HTTP/1.1 200 OK

# 2. Config unified
grep -A4 "^web:" ~/.hermes/config.yaml | grep backend  # all "searxng"

# 3. Multi-engine health check (count + which engines responded)
curl -s "http://localhost:8080/search?q=test&format=json" | python3 -c "
import sys,json
d=json.load(sys.stdin)
engines=set(r.get('engine','?') for r in d.get('results',[]))
print(f'{len(d.get(\"results\",[]))} results from engines: {engines}')
"
# Expected: >5 results from {duckduckgo, google cse} or similar
# If only 0-2 results or one engine → investigate Docker logs

# 4. Live test (after /reset)
# Use web_search in-session — should return results without quota errors
```

### Full sovereign bootstrap (SearXNG + WM + A-FORGE)

For a complete autonomous deployment mission — 5 phases: clone, build, test, Docker SearXNG, Hermes config, WM verification, report — see the reusable prompt template at:
- `references/autonomous-bootstrap-template.md`

## References

- `references/settings-multi-engine.yml` — production SearXNG config with DuckDuckGo + Brave + Google + Redis caching
