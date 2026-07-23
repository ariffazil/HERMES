# Web Search Backend Configuration

## The silent failure mode

When `web.search_backend`, `web.backend`, and `web.extract_backend` are all empty strings (`''`), Hermes silently falls back to **Tavily** using a bundled/shared free-tier API key. This key has a quota that exhausts quickly, producing:

- **432** — credits exhausted (most common)
- **401** — key expired/revoked
- **402** — payment required

The user sees: "Web search backend down." The reality: no backend was ever configured.

## The 5-second fix

```bash
hermes config set web.search_backend brave
hermes config set web.backend brave
hermes config set web.extract_backend brave
```

Requires `BRAVE_API_KEY` in `~/.hermes/.env` (or sourced from `/root/.secrets/vault.env`). Brave Search: **2,000 free queries/month**, 20 queries/minute, zero credit card required. No quota-hell cycle like Tavily.

## Verification

```bash
# 1. Config is set
grep -A3 "^web:" ~/.hermes/config.yaml
# web:
#   backend: brave
#   extract_backend: brave
#   search_backend: brave

# 2. Brave API key resolves
curl -sf "https://api.search.brave.com/res/v1/web/search?q=test" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | head -c 200

# 3. After /reset, web_search tool works
```

## Why Tavily keeps breaking

The `TAVILY_API_KEY` commonly found in vault.env files is a `tvly-dev-...` free developer tier key. These keys have:
- A hard credit cap that doesn't auto-refresh
- No billing path to add more credits
- Expiry tied to the developer account, not the project

When the key dies, `web_search` silently fails. There is no in-session indication that the backend is unconfigured — Hermes just returns empty or errors.

## Alternative: SearXNG (self-hosted)

If `/root/.secrets/vault.env` has `SEARXNG_URL=http://127.0.0.1:8080`:

```bash
hermes config set web.search_backend searxng
```

But verify it's alive first: `curl -s http://127.0.0.1:8080/search?q=test&format=json`. If it returns HTML instead of JSON, the instance needs `format=json` support enabled in `settings.yml`.

## Alternative: Hound MCP (keyless, always works)

The Hound MCP server (`mcp__hound__mcp_smart_search`) uses 10 independent search engines in parallel with zero API keys required. It is immune to single-provider quota issues. For Hermes sessions where `web_search` fails, Hound is the reliable fallback — no configuration needed.

## Root cause pattern

This is the same class of problem as provider fallback chains with dead entries: an **unconfigured default** that silently uses a **shared resource with a quota**. The fix is the same pattern: **explicitly configure a backend you own the key for**, rather than relying on the default.
