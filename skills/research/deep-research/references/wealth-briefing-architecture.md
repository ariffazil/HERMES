# WEALTH Briefing — Architecture Reference

**Date:** 2026-07-11 | **Source:** Session probe of `https://arif-fazil.com/wealth/`

---

## Data Flow

```
WEALTH engine (:18082)
    ↓ cron 06:00 UTC (root cron)
    ↓ /root/scripts/wealth-briefing-cron.sh
    ↓ Step 1: Python generates JSON → /var/www/html/arif/data/wealth/latest.json
    ↓ Step 2: rsync to /var/www/html/arif/data/wealth/
    ↓ Step 3: static render → /var/www/html/arif/static/wealth.html
```

## React App Data Fetching (Two-Step Fallback)

The main React app at `https://arif-fazil.com/wealth/` (served by Caddy from `/var/www/html/arif/`):

```javascript
// Step 1: Try live engine
fetch("https://mcp.arif-fazil.com/briefing")
  .then(r => r.json())

// Step 2: Fallback to static JSON (if live engine fails)
fetch("/data/wealth/latest.json")
```

**Key:** Both URLs return `meta.date` — the React app reads this for the briefing date banner.

## Caddy Routing

```
https://arif-fazil.com/wealth/
    → React SPA route (try_files {path} /index.html)
    → served from /var/www/html/arif/ (Caddy root)
    → /data/wealth/latest.json → /var/www/html/arif/data/wealth/latest.json ✅
    → /data/wealth/archive_index.json → /var/www/html/arif/data/wealth/archive_index.json ✅

OLD: https://arif-fazil.com/wealth-static/
    → /static/wealth.html (orphaned static render, not updated)
```

## Stale Data Diagnosis

| Tool | What it shows | Why |
|---|---|---|
| `curl https://arif-fazil.com/wealth/` | Old HTML comment block | Caddy cached the React `index.html` shell |
| `web_extract` | Old cached HTML (June 16) | web_extract doesn't execute JS — gets static shell |
| `browser_navigate` | **Live 2026-07-10** | Real Chromium renders the React app + JS data fetch |
| `curl /data/wealth/latest.json` | **Live 2026-07-10** | Static JSON file — definitive data source |

**Rule:** For SPAs (React/Next.js/Vue), `browser_navigate` + `browser_snapshot` is the **only** way to see what a real user sees. `web_extract` and plain `curl` get the server-rendered shell or cached HTML.

## Cron Status

- **Last run:** 2026-07-11 06:00 UTC ✅ (log confirmed `[DONE]`)
- **Live engine (`mcp.arif-fazil.com/briefing`):** Unreachable — React app falls back to static JSON
- **Static JSON:** Has 2026-07-11 data ✅ — no data loss, only live-API gap
- **Archives:** 44 entries in `archive_index.json`

## Archive Structure

```
/var/www/html/arif/data/wealth/
    latest.json          ← current briefing
    archive_index.json    ← array of {date, url} entries
    archive/
        2026-07-10.json ← individual dated files
        2026-07-09.json
        ...
```

The `latest.json` has no top-level `date` field — date is in `meta.date`. The React app reads `i.meta.date` for the banner.
