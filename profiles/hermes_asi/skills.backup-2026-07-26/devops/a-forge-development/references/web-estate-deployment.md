# Web Estate Deployment — arif-fazil.com arifOS Observatory aaa.arif-fazil.com

## Three-Site Federation Map

| Site | Domain | Type | Stack | Deploy Path |
|------|--------|------|-------|-------------|
| Observatory Hub | arif-fazil.com | React SPA + static | React 19 + Vite + Tailwind | `/var/www/html/arif/` |
| Kernel SOT | arifos.arif-fazil.com | Static HTML | Vanilla JS + SVG | `/var/www/html/arifos/` |
| Agent Control Plane | aaa.arif-fazil.com | Static HTML | Vanilla JS | `/var/www/aaa.arif-fazil.com/` |

## arif-fazil.com Deployment

**Source:** `/root/arif-sites/sites/arif-fazil.com/`
**Build output:** `/root/arif-sites/sites/arif-fazil.com/dist/`
**Web root:** `/var/www/html/arif/`

```bash
# 1. Build
cd /root/arif-sites/sites/arif-fazil.com && npm run build

# 2. Deploy
sudo cp -r /root/arif-sites/sites/arif-fazil.com/dist/* /var/www/html/arif/

# 3. Verify
for path in "/" "/wealth/" "/wealth/makcikgpt/" "/constellation/" "/canon/" "/000/" "/999/"; do
  status=$(curl -sf -o /dev/null -w "%{http_code}" "https://arif-fazil.com$path")
  echo "$status $path"
done
```

**SPA routes return `index.html`** — the server returns the same HTML shell for all routes. The `<title>` is set by React client-side, so `curl` will return HTTP 200 with the root `index.html` title. Use browser or JS fetch to verify the actual rendered page.

## Caddy SPA Routing — The Critical Rule

**Location:** `/etc/caddy/Caddyfile`

**SPA routing for React apps:**
```
handle /<route>/* {
    try_files {path} /index.html   # serve React app, let router handle route
    file_server
}
```

**What breaks it:**
```
handle /wealth/* {
    try_files /static/wealth.html /index.html  # STATIC FALLS FIRST — SPA never loads
    file_server
}
```

When a static `.html` file exists AND a React route exists at the same path, `try_files` serves the static file. The React SPA never loads. Fix: remove the static fallback, keep only `try_files {path} /index.html`.

**Reload after change:**
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
# If valid:
sudo caddy reload --config /etc/caddy/Caddyfile
```

## arifos.arif-fazil.com Deployment

Static HTML — no build step. Edit the files directly in `/var/www/html/arifos/` and they go live immediately.

**Key pages:**
- `index.html` — Observatory home
- `federation.html` — Federation map (organ cards, live health probe)

## aaa.arif-fazil.com Deployment

Static HTML — no build step. Edit directly in `/var/www/aaa.arif-fazil.com/`

**Key files:**
- `index.html` — Cockpit landing
- `agent.json` — Agent capability declaration
- `llms.txt` — LLM-readable site overview

## Known Issues (2026-07-10)

### Fixed
- `/wealth` was serving `/static/wealth.html` (static HTML) instead of React SPA. Fixed by removing static fallback from Caddyfile.

### Outstanding
- `arifOS Observatory index.html` still references APEX port 3002 (decommissioned 2026-06-27)
- `AAA` still shows old APEX references in nav/metadata
- `WELL` landing page needs updating to reflect current 3-phase system

## Broken Link Diagnosis

When a URL returns unexpected content:
1. Check if the path exists in Caddyfile — Caddy routes take priority over `file_server`
2. Check if a static file exists at that path — `try_files static.html` wins over SPA
3. For SPA routes: verify the route exists in `App.tsx` `<Route path="...">` entries
4. `curl -sf "https://site.com/path/" | grep '<title>'` — gets server-returned title

## MCP Endpoint URLs (verified 2026-07-10)

| File | Field | Correct URL | Was |
|------|-------|------------|-----|
| `aaa.arif-fazil.com/agent.json` | `tools_list` | `https://aaa.arif-fazil.com/.mcp-tools.json` | `https://mcp.arif-fazil.com/tools` (404) |
| `aaa.arif-fazil.com/llms.json` | `mcp_endpoint` | `https://mcp.arif-fazil.com` | `https://arifosmcp.arif-fazil.com/mcp` (404) |
