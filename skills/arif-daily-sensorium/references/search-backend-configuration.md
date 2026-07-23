# Search Backend — Canonical Configuration (UPDATED 2026-07-21)

## Root Cause (Historical)

Both `web_search` and `web_extract` use the backend configured under the `web:` section
in `~/.hermes/config.yaml`. The default (empty `search_backend`) routes through Tavily.
When Tavily returns **432** (credits exhausted) or **401** (key expired), both tools fail.

The free-tier `TAVILY_API_KEY` (`tvly-dev-*`) has a monthly quota that exhausts quickly
under agent research workloads.

## Permanent Fix: Local SearXNG

The arifOS federation runs a **self-hosted SearXNG instance** on `http://127.0.0.1:8080`.
It uses DuckDuckGo + Google CSE backends — no API key, no monthly quota, no rate limit.

**Config changes (one-time, permanent):**

```bash
hermes config set web.backend searxng
hermes config set web.search_backend searxng
hermes config set web.extract_backend searxng
hermes config set search.backend searxng
hermes config set search.search_backend searxng
```

**Verification:**

```bash
# Check SearXNG is alive
curl -sfo /dev/null -w "%{http_code}" "http://127.0.0.1:8080/search?q=test&format=json"
# → 200

# Verify SEARXNG_URL is set
grep SEARXNG_URL /root/.secrets/vault.env
# → export SEARXNG_URL="http://127.0.0.1:8080"

# Verify config is unified (no split-brain between web: and search: sections)
grep -A4 "^web:" ~/.hermes/config.yaml
grep -A3 "^search:" ~/.hermes/config.yaml
```

**Session restart required:** Config changes take effect on next session (`/reset` or new
`hermes` invocation). Current session still uses old backend.

## Fallback: Hound MCP

If SearXNG is down, Hound MCP (`mcp__hound__mcp_smart_search`) is always available as
a keyless alternative with 10 parallel backends (DuckDuckGo, Brave, Yahoo, Yandex, etc.).
Use it directly when `web_search` fails — no config change needed.

## Fallback: Browser (last resort)

If both SearXNG and Hound are down, use `browser_navigate` with a search engine URL.
This is the slowest path — only use when the other two are confirmed dead.
