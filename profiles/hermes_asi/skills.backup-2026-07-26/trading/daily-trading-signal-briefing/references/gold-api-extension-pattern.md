# Gold API Extension Pattern

How to add new endpoints to the gold-api (port 3456). This is the ONLY way to add trading features — Arif forbids new servers.

## Architecture

```
Browser → Caddy → gold-api (port 3456) → fetch_gold.py → Python trading modules
```

Caddy strips `/wealth/gold` prefix, so `/wealth/gold/api/apex` → `/api/apex` on the backend.

## Steps

### 1. Add Python command to fetch_gold.py

```python
# /var/www/html/gold/api/fetch_gold.py
def cmd_XXX(args):
    """Description of what this does."""
    cache = _cache_key("xxx")
    cached = _read_cache(cache)
    if cached:
        return cached

    # ... your logic here ...
    result = { ... }
    _write_cache(cache, result)
    return result
```

### 2. Register in CLI choices + handlers

```python
parser.add_argument("command", choices=[..., "xxx"])
handlers = { ..., "xxx": cmd_xxx }
```

### 3. Add endpoint to server.js

```javascript
// /var/www/html/gold/api/server.js
'/api/gold/xxx': async () => {
  const c = getCache('xxx'); if (c) return c;
  const d = await runPython('xxx'); setCache('xxx', d); return d;
},
'/api/xxx': async () => handlers['/api/gold/xxx'](),  // Caddy alias
```

### 4. Restart and test

```bash
systemctl restart gold-api
curl -sf localhost:3456/api/gold/xxx | python3 -m json.tool
curl -sf https://arif-fazil.com/wealth/gold/api/xxx | python3 -m json.tool
```

## Caching

- Default TTL: 300 seconds (5 minutes)
- Python side: `_cache_key()` + `_read_cache()` + `_write_cache()` (file-based in `/tmp/gold_cache/`)
- Node.js side: `getCache()` + `setCache()` (in-memory Map)
- Both layers cache independently — that's fine, double-cache is intentional

## Pitfalls

- **Caddy strip_prefix:** If you add `/api/gold/xxx` to server.js, you MUST also add `/api/xxx` alias. Otherwise the Caddy-routed path won't match.
- **Python imports:** Use `sys.path.insert(0, "/root")` then `from trading.xxx import yyy`. Not `sys.path.insert(0, "/root/trading")` — relative imports need the parent package.
- **TradingConfig missing attributes:** If `cfg.contract_multiplier` fails, add it to `/root/trading/core/config.py` as a field with default.
- **yfinance timeouts:** Direct yfinance calls timeout on this VPS. Use gold-api cache as primary data source. If you need OHLCV data, fetch from gold-api's `/api/gold/history` endpoint first, fall back to yfinance only if cache misses.
- **numpy JSON serialization:** Always use a custom JSON encoder for numpy types. See `fetch_gold.py` for the pattern.
- **ForexFactory JSON API (proven 2026-07-16):** Use `https://nfs.faireconomy.media/ff_calendar_thisweek.json` — returns clean JSON array. Filter by `country` and `impact` fields. Timezone is EST (-04:00/-05:00), convert to MYT (+08:00) for display. Cache for 30 minutes. NEVER scrape the HTML page — regex parsing fails on merged cells.
- **DO NOT register gold-api as arifOS organ (reverted 2026-07-16):** Arif explicitly forbade creating bridge modules, organ registrations, or new MCP tools on arifOS. The gold-api is just a REST endpoint on port 3456. Any agent calls `curl localhost:3456/api/gold/signal_v2` directly. No bridge needed. No organ registration needed. No new tools on arifOS. This was built and reverted in the same session — do not rebuild.
- **Gold site navigation (proven 2026-07-16):** The gold site at `/var/www/html/gold/index.html` includes `/_shared/unified-header-loader.js` which injects the federation nav bar. To add new links to ALL sites, edit `/_shared/unified-header.html`. The nav bar has sections: HOME, WELLS, SYSTEMS (OBSERVATORY, GEOX, WEALTH, WELL, MAKCIKGPT), MARKETS (GOLD, OIL), GOVERN (AAA, MCP, A-FORGE), /000, /999, CANON, CONSTELLATION, WRITING, CONTACT.
