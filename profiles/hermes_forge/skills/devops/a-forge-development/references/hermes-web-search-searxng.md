# Hermes Web Search — SearXNG Local Backend

**Configured:** 2026-07-21
**Why:** Tavily free-tier quota exhausted (432/401). Brave split-routing was a
temporary fix. Local SearXNG eliminates all external API key + quota dependencies.

## Config

```bash
hermes config set web.search_backend searxng
hermes config set web.backend searxng
hermes config set web.extract_backend searxng
```

SearXNG instance: `http://127.0.0.1:8080` (systemd: `searxng.service`)
JSON endpoint: `http://127.0.0.1:8080/search?q=QUERY&format=json`

Config lives in `~/.hermes/config.yaml`:
```yaml
web:
  backend: searxng
  extract_backend: searxng
  search_backend: searxng
```

## Verification

```bash
curl -sf "http://127.0.0.1:8080/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['results']), 'results')"
```

## Important: Session Restart Required

`web.search_backend` is read at session start. After config change, `/reset` or
start a new session for the built-in `web_search` tool to pick up the new backend.

## Fallback

Hound MCP (`mcp__hound__mcp_smart_search`) is always available as keyless
10-engine parallel search. Never gated by quota or API key.

## Previous State

| Backend | Status | Issue |
|---------|--------|-------|
| Tavily (default) | Dead | Free key `tvly-dev-...` quota exhausted → 432 |
| Brave | Working | 2,000/month, but split-routing + external dependency |
| SearXNG (current) | Working | Local, zero keys, zero quotas, DuckDuckGo + Google CSE proxied |
