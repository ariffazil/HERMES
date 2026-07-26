# Web Surface Fossil Patterns

> Surface fossils = live-rendered pages that show stale, misleading, or incorrect state despite the underlying data being correct. Diagnostic technique and findings from 2026-07-11 WEALTH surface audit.

## The Core Pattern: web_extract Caching vs Browser Reality

**Symptom:** `web_extract` returns `2026-06-16` for WEALTH briefing; actual browser shows `2026-07-10`.

**Root cause:** `web_extract` caches by URL. The cron ran correctly and wrote `latest.json` with today's date. The browser correctly reads and renders today's date. `web_extract` had cached an older response for the same URL.

**Rule:** For rendered HTML with live JS-driven content, always use the browser tool. Use `web_extract` only for:
- Text-only endpoints (APIs returning JSON)
- Static files (`.json`, `.txt`, `.md`)
- Raw HTML without JS-driven state mutations

## Two-Layer Web Surface Investigation

| Layer | Tool | What it sees |
|---|---|---|
| Static surface | `web_extract` | HTML source, JSON APIs, cached state |
| Rendered surface | `browser_navigate` + `browser_snapshot` | Live JS-rendered DOM |

**Always start with `web_extract` for APIs** (faster, JSON-parsable). Escalate to browser only when:
- `web_extract` shows stale data
- User reports different content than `web_extract` shows
- The page has React/Vue/Svelte SPA routing

## Case: WEALTH Briefing — Cron + SPA Architecture

### What happened

1. Cron at `06:00 MYT` ran `wealth_daily_briefing.py` → wrote JSON to `/var/www/html/arif/data/wealth/latest.json` (date: 2026-07-10)
2. React SPA at `arif-fazil.com/wealth/` fetches from two sources:
   - Primary: `https://mcp.arif-fazil.com/briefing` (live engine) → HTTP 404 (engine offline)
   - Fallback: `/data/wealth/latest.json` (static file written by cron) → HTTP 200, shows 2026-07-10 ✅
3. `web_extract` returned cached 2026-06-16 → misleading
4. Browser showed 2026-07-10 → correct

### The 404 on mcp.arif-fazil.com/briefing

`mcp.arif-fazil.com/briefing` returns HTTP 404. The React app tries it first, falls back to static JSON. **This is intentional design** — the app is built to work offline. The 404 is the live engine not being stood up; the static fallback correctly serves today's briefing.

The `⚠️ OFFLINE MODE` banner is correct behavior. It says: "I tried the live engine, it didn't answer, using cached data instead."

## Source Repo vs Web Root Divergence

For any deployed surface (tools.json, apps.json, agent.json):

```
/root/<organ>/          ← source repo (authoritative)
/var/www/html/<organ>/ ← web root (what agents discover via HTTP)
```

**Always compare both.** This session found:
- `/root/geox/apps.json`: 6 apps, `ui_resource` fields, MCP Apps protocol schema
- `/var/www/html/geox/apps.json`: 4 apps, no `ui_resource`, older schema

**Fix:** Deploy source → web root. Never iterate on the web root copy.

### Divergence detection command

```bash
for organ in geox arifOS wealth well; do
  SRC="/root/$organ/apps.json"
  DST="/var/www/html/$organ/apps.json"
  if [ -f "$SRC" ] && [ -f "$DST" ]; then
    echo "=== $organ ==="
    python3 -c "
import json
src = json.load(open('$SRC'))
dst = json.load(open('$DST'))
src_n = len(src.get('apps', src.get('tools',[])))
dst_n = len(dst.get('apps', dst.get('tools',[])))
print(f'Source: {src_n} | Web: {dst_n} | Match: {src_n == dst_n}')
"
  fi
done
```

## Caddy SPA Catch-All — What It Does and Doesn't Block

Caddyfile for `geox.arif-fazil.com`:
```
handle /mcp*  { reverse_proxy 127.0.0.1:8081 }
handle /health { reverse_proxy 127.0.0.1:8081 }
handle /tools  { reverse_proxy 127.0.0.1:8081 }
handle /.well-known/mcp/server.json { reverse_proxy 127.0.0.1:8081 }
handle /*      { try_files {path} /index.html; file_server }
```

**What works:** `/apps.json`, `/.well-known/agent.json`, `/.well-known/mcp/server.json`, `/tools.json`
**Why:** They are not caught by `handle /*` — they exist as real files in the web root and Caddy serves them directly before reaching the SPA fallback.

**Myth debunked:** The SPA catch-all `handle /*` does NOT block static files that exist. It only sends non-existent paths to `index.html`. Real files are served normally.

**Test with:**
```bash
curl -sf "https://geox.arif-fazil.com/apps.json" -o /dev/null -w "%{http_code}\n"
curl -sf "https://geox.arif-fazil.com/.well-known/agent.json" -o /dev/null -w "%{http_code}\n"
curl -sf "https://geox.arif-fazil.com/tools.json" -o /dev/null -w "%{http_code}\n"
```

## MCP Briefing Endpoint — 404 is Intentional Offline Mode

The live briefing API at `https://mcp.arif-fazil.com/briefing` returns 404. The WEALTH React app:
1. Fetches live engine first → 404
2. Falls back to static JSON at `/data/wealth/latest.json` → shows today's data

**This is correct offline behavior.** The banner says "⚠️ OFFLINE MODE — showing last cached briefing (DATE)." The cron writes fresh JSON daily; the app falls back to it when live engine is unreachable.

To silence the banner: stand up the live briefing engine at the `/briefing` endpoint. The static JSON path is already correct.

## Surface Fossil Audit Checklist

When Arif says "this is supposed to be like this??" about any web surface:

1. **Browser first** — `browser_navigate` + `browser_snapshot` to see actual rendered state
2. **Static file probe** — `curl` the JSON data file directly to confirm cron wrote correct data
3. **Source vs web root** — compare `/root/<organ>/` with `/var/www/html/<organ>/`
4. **Caddy routing** — confirm the URL returns 200 as a real file, not 200 via SPA fallback
5. **Cron status** — check log at `/var/log/wealth_briefing.log`, confirm last run timestamp
6. **Engine status** — `curl :<port>/health` to see if live engine is running
