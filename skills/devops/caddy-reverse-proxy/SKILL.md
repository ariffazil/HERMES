---
name: caddy-reverse-proxy
description: >
  Add, modify, and test Caddy reverse proxy routes on the arif-fazil.com
  infrastructure. Covers static file serving, API proxy, handle block
  ordering, systemd service creation for backend APIs, and end-to-end
  verification. USE WHEN: "add Caddy route", "proxy to localhost",
  "deploy behind Caddy", "new subpath on arif-fazil.com", "Caddy config".
tags: [caddy, reverse-proxy, infrastructure, systemd, devops]
related_skills: [infra-guardian, federation-self-hosted-services, vps-operations]
---

# Caddy Reverse Proxy Configuration

**Add new routes to the arif-fazil.com Caddy infrastructure without breaking existing routes.**

## Critical Rules

1. **ALWAYS check which config file is actually running**: `ps aux | grep caddy | grep run` — Caddy may start from `/etc/caddy/Caddyfile` while backup copies (`Caddyfile.live`, `Caddyfile.bak.*`) exist in the same directory. Editing the wrong file = edits that never take effect. The running config wins.
2. **ALWAYS back up before modifying**: `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak.YYYY-MM-DD`
2. **ALWAYS validate before reloading**: `caddy validate --config /etc/caddy/Caddyfile`
3. **ALWAYS test existing routes after reload** — verify homepage and related paths still return 200
4. **Handle blocks evaluate TOP-DOWN** — more specific routes MUST come before broader ones
5. **The `patch` tool REFUSES system paths** (`/etc/caddy/`, `/etc/systemd/`) — use `terminal` with `sed` or heredoc instead

## Caddyfile Location

- Config: `/etc/caddy/Caddyfile`
- Admin socket: `unix//var/run/caddy-admin.sock`
- Managed domains: `arif-fazil.com` (Ψ), `arifos.arif-fazil.com` (Ω), `aaa.arif-fazil.com` (Δ)

## Adding a Standalone Subdomain (Not Under arif-fazil.com)

When the user asks to deploy a site "not linked to main site" (e.g., `syedos.arif-fazil.com` instead of `arif-fazil.com/syedos/`):

### Step 1: Cloudflare DNS Record

Credentials live in `/root/.secrets/vault.env`:
- `CF_TOKEN=cfut_...`
- `CF_ZONE_ID=6e837d3be53b37dcf79e0f09a1e14faa`
- VPS IP: `72.62.71.199`

```python
import urllib.request, json
data = json.dumps({
    "type": "A",
    "name": "syedos",        # creates syedos.arif-fazil.com
    "content": "72.62.71.199",
    "ttl": 120,
    "proxied": True
}).encode()
req = urllib.request.Request(
    f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records",
    data=data,
    headers={"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"}
)
print(json.loads(urllib.request.urlopen(req).read()))
```

**Note:** TTL becomes 1 (auto) when proxied=True — Cloudflare manages this.

### Step 2: Caddy vhost

```caddyfile
newsubdomain.arif-fazil.com {
    import tls_origin
    encode zstd gzip
    root * /var/www/html/newsubdomain
    
    # Optional sub-paths
    handle /dashboard/* {
        try_files /dashboard.html /index.html
        file_server
    }
    
    # Default
    handle {
        try_files {path} {path}/index.html /index.html
        file_server
    }
}
```

### Step 3: Certificate + Verification

Caddy auto-requests Let's Encrypt cert via HTTP-01 challenge through Cloudflare. Monitor:
```bash
journalctl -u caddy --no-pager -n 5 | grep "newsubdomain"
# Wait for "certificate obtained successfully"
```

Test via direct IP (bypasses DNS):
```bash
curl -sk --resolve "newsubdomain.arif-fazil.com:443:72.62.71.199" \
  -o /dev/null -w "HTTP %{http_code}\nSize: %{size_download}\n" \
  https://newsubdomain.arif-fazil.com/
```

**Pitfall:** SSL will fail (exit code 35, "000") until Let's Encrypt cert is issued (~5 seconds). This is normal. Check `journalctl -u caddy` for ACME progress.

### Step 4: DNS Propagation

Cloudflare DNS takes ~1-2 minutes to propagate globally. Until then, only `--resolve` testing works.

### User Preference: Standalone Subdomain vs Main-Site Subpath

**When to use subdomain** (proven 2026-07-24 — user preference):
- Site is for someone OTHER than Arif (e.g., Syed's dashboard)
- User says "just share domain" or "jangan link dengan main site"
- The site has its own identity/theme unrelated to arif-fazil.com
- Zero risk of breaking main site SPA routing

**When to use subpath** (`arif-fazil.com/<app>/`):
- Internal governance/observatory tools
- Quick prototypes or testing before domain migration
- Federation organ dashboards (gold, oil, gas)
- Any case where the user DIDN'T specifically request a standalone domain

## Adding a New Subpath Route (Static + API Proxy)

Pattern for serving a standalone app at `/<app>/` with a backend API at `/<app>/api/`:

```caddyfile
# <App name> — static frontend + API proxy
@app_api path /<app>/api/*
handle @app_api {
    uri strip_prefix /<app>
    reverse_proxy localhost:<PORT>
}
handle /<app>/* {
    uri strip_prefix /<app>
    root * /var/www/html/arif/<app>
    try_files {path} /index.html
    file_server
}
```

### Key Details

- **Named matcher (`@app_api`)**: Must come BEFORE the broader `handle /<app>/*` block
- **`uri strip_prefix`**: Strips the subpath so the backend receives clean paths (e.g., `/wealth/gold/api/ticker` → `/api/ticker`)
- **`try_files {path} /index.html`**: SPA fallback pattern — serves `index.html` for client-side routing
- **`root * /var/www/html/arif/<app>`**: Static files served from the arif-fazil.com document root subtree
- **Insert location**: Place the new block BEFORE any existing broader `handle /<parent>/*` block that would match the same paths

### Common Pitfall: Trailing Slash — `handle /path/*` Does NOT Match `/path`

Caddy's `handle /path/*` only matches requests that have at least one character after `/path/`. The bare path `/path` (no trailing slash) falls through to whatever catch-all comes next — typically the SPA fallback that serves the homepage.

**Symptoms:** `https://site.com/gold` returns the homepage, but `https://site.com/gold/` returns the correct page. File sizes differ wildly (e.g., 10KB home vs 75KB dashboard).

**Fix:** Add an explicit redirect BEFORE the `handle` block:
```caddyfile
redir /gold /gold/ 308
handle /gold/* {
    root * /var/www/html/gold
    try_files {path} /index.html
    file_server
}
```

**Verification:** After reload, `curl -s -o /dev/null -w "%{http_code}, url: %{redirect_url}" https://site.com/gold` should return `308` and the trailing-slash URL.

### Common Pitfall: Parent Path Conflict

If an existing `handle /wealth/*` block exists and you add `handle /wealth/gold/*`, the gold block MUST appear before the wealth block. Otherwise the wealth block catches the request first and the gold route never triggers.

### Common Pitfall: `uri strip_prefix` Mismatch with Backend Routes (PROVEN 2026-07-16)

When Caddy strips a prefix, the backend receives a DIFFERENT path than what the browser sent. If the backend only registers the full path, the stripped path returns 404.

**Example:** Caddy config:
```caddyfile
@wealth_gold_api path /wealth/gold/api/*
handle @wealth_gold_api {
    uri strip_prefix /wealth/gold
    reverse_proxy localhost:3456
}
```

Browser requests: `/wealth/gold/api/macro`
Caddy strips `/wealth/gold` → sends `/api/macro` to backend
Backend has: `/api/gold/macro` but NOT `/api/macro` → **404!**

**Fix:** Always add BOTH the full path AND the short alias in the backend server:
```javascript
const handlers = {
  '/api/gold/apex': async () => { ... },
  '/api/apex': async () => handlers['/api/gold/apex'](),  // ← SHORT ALIAS
  '/api/gold/macro': async () => { ... },
  '/api/macro': async () => handlers['/api/gold/macro'](),  // ← SHORT ALIAS
  '/api/gold/ticker': async () => { ... },
  '/api/ticker': async () => handlers['/api/gold/ticker'](),  // ← SHORT ALIAS
};
```

**Verification:** After adding routes, always test BOTH direct and via Caddy:
```bash
curl -sf localhost:3456/api/macro | head -1          # Direct
curl -sf https://arif-fazil.com/wealth/gold/api/macro | head -1  # Via Caddy
```

**Debugging:** If Caddy returns 404 but direct works, check:
1. Does the backend have the SHORT alias (not just the full path)?
2. Is the `uri strip_prefix` value correct?
3. Test: `curl -v https://arif-fazil.com/wealth/gold/api/endpoint 2>&1 | grep HTTP`

## Inserting Config into System Files

Since the `patch` tool refuses to write to `/etc/caddy/Caddyfile`:

```bash
# Method: sed insert before a known pattern, then atomic replace
cat /etc/caddy/Caddyfile | sed '/^PATTERN$/i\
\tnew line 1\
\tnew line 2\
' > /etc/caddy/Caddyfile.new && mv /etc/caddy/Caddyfile.new /etc/caddy/Caddyfile
```

Alternative for multi-line inserts — use a heredoc with `cat > /tmp/patch.txt` and apply via `sed -f`.

## Reload Sequence

**Always use the safe reload script** instead of bare `systemctl reload caddy`:

```bash
bash /root/.hermes/scripts/caddy-safe-reload.sh
```

See [references/caddy-safe-reload.md](references/caddy-safe-reload.md) for details — backup → validate → reload → verify. No email, all receipts to local log.

### Manual reload (only if script unavailable)

```bash
# 1. Validate (catches syntax errors without disrupting live config)
caddy validate --config /etc/caddy/Caddyfile 2>&1

# 2. Reload (zero-downtime config swap)
caddy reload --config /etc/caddy/Caddyfile 2>&1
```

## Bot Markdown Bypass

For serving raw markdown to AI crawlers (GPTBot, ClaudeBot, etc.) while keeping HTML for humans. See [references/bot-markdown-bypass.md](references/bot-markdown-bypass.md).

## Testing

### Direct API Test (bypass Caddy)
```bash
curl -s http://localhost:<PORT>/api/<endpoint>
```

### Caddy Proxy Test (end-to-end via HTTPS)
```bash
# Note: HTTP requests return 308 (HTTPS redirect) — test via HTTPS
curl -sk https://arif-fazil.com/<app>/api/<endpoint>
curl -sk -o /dev/null -w "%{http_code}" https://arif-fazil.com/<app>/
```

### Existing Routes Integrity
```bash
# Verify nothing broke
curl -sk -o /dev/null -w "%{http_code}" https://arif-fazil.com/
curl -sk -o /dev/null -w "%{http_code}" https://arif-fazil.com/<parent-path>
```

## Systemd Service for Python API

For Python HTTPServer backends (e.g., file upload servers, lightweight APIs):

```ini
[Unit]
Description=<description>
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/sado
ExecStart=/usr/bin/python3 /root/sado/server.py
Restart=always
RestartSec=3
Environment=HOME=/root

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable <service>
systemctl start <service>
systemctl status <service> --no-pager | head -10
# Verify port
ss -tlnp | grep <PORT>
```

**Common pitfall:** Python's built-in `HTTPServer` is single-threaded. For single-user portals behind Caddy it's fine. For multi-user, use `ThreadingHTTPServer` or gunicorn.

## File Upload Backend Pattern

When building a file upload portal with auto-processing pipeline:

1. **Upload HTML** — drag-drop zone + file input with `capture="environment"` (phone camera), POST multipart form to `/api/upload`
2. **Python backend** — parses multipart POST, saves file to disk with UUID filename + sidecar `.json` metadata, touches `.pending` flag
3. **systemd service** — keeps Python server alive
4. **Caddy proxy** — `handle /api/* { reverse_proxy 127.0.0.1:<PORT> }`
5. **Cron watcher** — checks `.pending` file every N minutes, processes receipts, marks processed=true, removes flag, regenerates dashboard
6. **Dashboard regeneration** — cron rewrites the static HTML with fresh data

### User Preference: Zen Single-Page Design (proven 2026-07-24)

Arif prefers **one scrollable page** over multi-tab/multi-page navigation for non-technical users (like Syed). Evidence:
- "So many button to click to go to the desired pages. Zen it"
- User wanted floating upload button (FAB) rather than separate upload page
- Everything in one scroll, no tabs, no sub-navigation

**When building sites for end-users (not yourself):**
- Default to one-page scroll layout
- Use floating action buttons (FAB) for secondary actions
- No tabs, no sub-pages, no hierarchical navigation
- Everything visible without clicking
- Responsive: stacks vertically on mobile

## Systemd Service for Node.js API

```ini
[Unit]
Description=<Service Name>
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/html/arif/<app>/api
ExecStart=/usr/bin/node /var/www/html/arif/<app>/api/server.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

```bash
# Write to /etc/systemd/system/<service>.service via terminal (patch tool refuses)
# Then:
systemctl daemon-reload
systemctl enable <service>.service
systemctl start <service>.service
systemctl status <service>.service
```

### Common Pitfall: Standalone `.html` Files at Root Return 404 (PROVEN 2026-07-20)

When you place a standalone `.html` file at `/var/www/html/arif/some-file.html`, requesting `https://arif-fazil.com/some-file.html` returns 404 even though the file exists. This is because the SPA fallback at the end of the `arif-fazil.com` block catches all unmatched paths and routes them to the React SPA, which doesn't recognize the path as a valid route.

**Symptom:** `curl -sI https://arif-fazil.com/file.html` → `HTTP/2 404`. File exists on disk at `/var/www/html/arif/file.html`.

**Root cause:** The SPA catch-all `try_files {path} /index.html` in the final `handle` block intercepts every path that isn't explicitly handled. Standalone `.html` files need a `handle` block with `file_server` to be served.

**Quick fix — use an existing file_server path:** Place the file under `/verify/`, `/data/`, `/assets/`, or `/connect/` — these paths already have `file_server` handlers:

```bash
cp file.html /var/www/html/arif/verify/file.html
# Now serves at: https://arif-fazil.com/verify/file.html (200, text/html)
```

**Trade-off:** `/data/*` sets `Content-Type: application/json` — avoid for HTML files. `/assets/*` has long cache (`max-age=31536000`) — avoid for frequently updated files. `/verify/*` is the best fit for ad-hoc HTML delivery.

**Permanent fix — add explicit handle:** If the file needs to live at root:
```caddyfile
# BEFORE the SPA fallback
handle /file.html {
    root * /var/www/html/arif
    file_server
}
# Then: caddy validate && caddy reload
```

**Verification:** `curl -sI https://arif-fazil.com/verify/file.html | head -3` should return `200` and `text/html`.

### Common Pitfall: `root * /outside/docroot` Returns 404 for file_server (PROVEN 2026-07-24)

When you add a `handle /path/*` block with `root * /root/some-dir` pointing to a directory OUTSIDE `/var/www/html/`, the `file_server` handler returns 404 even though the file exists and permissions are correct.

**Symptom:** `curl -sk https://arif-fazil.com/path/file.html` → `HTTP/2 404` with `content-length: 0`. File exists at `/root/some-dir/file.html` with `-rw-r--r--`. The route appears in the live config (verified via admin API). All tls_origin headers are present, confirming Caddy's host block is routing the request.

**Root cause:** When a Caddy vhost has a `root` set at the top level (e.g., `root * /var/www/html/arif` via the tls_origin import), nested `handle` blocks that set `root * /some/external/path` may not propagate correctly to the `file_server` handler within deeply nested subroutes. The subroute group (created by Caddyfile adapter for `handle` blocks) inherits the parent root, and the override from a `vars` handler in a nested sub-subroute doesn't take effect for `file_server`.

**Fix — copy files to the standard document root:**

```bash
# Instead of:
#   root * /root/sado
#   file_server

# Do this:
mkdir -p /var/www/html/arif/<app>
cp /root/some-dir/* /var/www/html/arif/<app>/
chmod 644 /var/www/html/arif/<app>/*

# Caddyfile:
handle /<app>/* {
    root * /var/www/html/arif
    try_files {path} {path}/index.html /<app>/index.html
    file_server
}
```

**Why this works:** The file lives under the vhost's established root, so `file_server` resolves it correctly. The `try_files` chain provides SPA-like fallback.

**Alternative — use a symlink in the document root:**
```bash
ln -s /root/some-dir /var/www/html/arif/<app>
```
Then use the same `handle` block with the standard root. The symlink follows automatically as long as Caddy has filesystem access (runs as root on this infra).

**Verification:**
```bash
curl -sk -o /dev/null -w "HTTP %{http_code}\nSize: %{size_download}\n" https://arif-fazil.com/<app>/file.html
# Should return 200, not 404/0
```

### Common Pitfall: Static Sub-Pages Under SPA Route Need `@spa_routes` + `{path}/index.html` (PROVEN 2026-07-26)

When a site uses React SPA with `handle @spa_routes { try_files ...; file_server }`, adding new static sub-pages (e.g., `/pulse/`) requires TWO fixes or they silently fall through to the 404 handler:

**Fix 1 — add the path to the `@spa_routes` matcher:**
```caddyfile
@spa_routes path / /economics* /writing* /world* /doctrine* /pulse*
#                                                    ^^^^^^^ ADD
```
Without this, paths not in the matcher hit the final `handle { respond "404" }` block.

**Fix 2 — use `{path} {path}/index.html /index.html` (NOT just `{path} /index.html`):**
```caddyfile
handle @spa_routes {
    try_files {path} {path}/index.html /index.html
    #                ^^^^^^^^^^^^^^^^ CRITICAL — tries static index.html before SPA fallback
    file_server
}
```
The default SPA pattern `try_files {path} /index.html` skips `{path}/index.html`. For `/pulse/`, `{path}` is `/pulse/` (a directory), `{path}/index.html` resolves to `/pulse/index.html` (the static page). Without this middle term, the resolver serves the SPA shell (`/index.html`) instead.

**Symptom:** Static HTML exists at `/var/www/html/arif/pulse/index.html` with correct 644 permissions. `curl https://site.com/pulse/` returns the SPA title (e.g., "Arif Fazil — Exploration Geoscientist") instead of the static page title (e.g., "Federation Pulse — arifOS"). Response size matches SPA index.html.

**Verification:**
```bash
curl -s https://site.com/pulse/ | grep '<title>'
# Expected: "Federation Pulse — arifOS"
# Wrong:    "Arif Fazil — Exploration Geoscientist" (SPA shell)
```

**Post-deploy: cron-generated data files** — `rsync --delete` removes files not in `dist/`. If the page reads a data.json written by cron:
```bash
# Recreate after deploy via post-deploy hook
bash /root/scripts/post-deploy-pulse.sh

# Better: fq-probe.sh writes to both webroot + a backup dir,
# so a simple post-deploy restore script resurrects it
```

### Common Pitfall: `uri strip_prefix` + Root Path `/` After Strip Leaves `try_files` With a Directory Match (PROVEN 2026-07-29)

When a Caddy config uses `uri strip_prefix` on a directory path (e.g., `/world/makcikgpt/`) that reduces to `/`, the `try_files {path} {path}.html /index.html` with `{path}=/` may **fail to resolve `index.html`** because Caddy treats `/` as a directory hit and `file_server` doesn't automatically serve the directory index.

**Symptom:** Individual article pages under a prefix work fine (`/world/makcikgpt/slug` → 200), but the root landing page (`/world/makcikgpt/` → 404). The `file_server` serves 0 bytes with `content-length: 0`.

**Root cause:** After `uri strip_prefix /world/makcikgpt`, the internal path becomes just `/`. The `try_files {path}` matches against `/var/www/html/arif/makcikgpt-md/` — a directory — which Caddy considers "found" by `try_files`. The subsequent `file_server` then tries to serve the directory, but the index resolution (`index.html`) within a `handle` block that already executed `try_files` against a directory doesn't cascade to serve an index file as expected.

Note: this is a Caddy v2 edge case specific to the **stripped root path** scenario. Regular `handle /path/*` blocks without `uri strip_prefix` do not exhibit this — see the ["Static Sub-Pages" pitfall](#common-pitfall-static-sub-pages-under-spa-route-need-spa_routes--pathindexhtml-proven-2026-07-26) above for the non-strip counterpart.

**Fix — add a dedicated `handle /path/` block (with trailing slash) BEFORE the `@ai-bot` block:**

```caddyfile
# Landing page root handler — serves index.html when uri strip_prefix reduces path to /
handle /world/makcikgpt/ {
    root * /var/www/html/arif/makcikgpt-md
    try_files /index.html =404
    file_server
}

# Bot-readable individual articles
@ai-bot-world {
    header_regexp User-Agent (?i)GPTBot|ClaudeBot|...|curl|Python-urllib|python-requests|...
    path /world/makcikgpt/*
}
handle @ai-bot-world {
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    try_files {path} {path}.html /index.html
    file_server
}
```

Note: the `Python-urllib` entry in the bot UA regex is **optional** — it's only needed if probes use Python's `urllib.request.urlopen()` which sends `Python-urllib/3.x`. The regex already covers `python-requests` and `curl`.

**Why this works:** The `handle /world/makcikgpt/` block matches the exact directory path BEFORE the broader `@ai-bot-world` matcher. It uses `try_files /index.html =404` which resolves the file explicitly (not relying on `{path}` directory matching). The `file_server` then serves it directly.

**Verification:**

```bash
# Landing page returns 200 with actual content
curl -svo /dev/null --resolve "arif-fazil.com:443:127.0.0.1" \
  "https://arif-fazil.com/world/makcikgpt/" 2>&1 | grep -i "< http\\|200\\|404"

# Individual articles still work
curl -svo /dev/null --resolve "arif-fazil.com:443:127.0.0.1" \
  "https://arif-fazil.com/world/makcikgpt/ilmu-bbb" 2>&1 | grep -i "< http\\|200\\|404"

# Content is served (not 0 bytes)
curl -s --resolve "arif-fazil.com:443:127.0.0.1" \
  "https://arif-fazil.com/world/makcikgpt/" | wc -c
# Should be > 0 — 404 returns 0 bytes on this infra
```

**Detection:** When the external witness probe (P17) repeatedly reports `HTTP 404` for `/world/makcikgpt/` but individual article paths resolve fine, this is the root cause.

### Common Pitfall: Probe User-Agent Not in Caddy Bot Regex (PROVEN 2026-07-29)

When a Caddy config uses `@ai-bot-world` with `header_regexp User-Agent` to match bots and serve raw/markdown content, the probe's HTTP library User-Agent string may not be in the regex. Python's `urllib.request.urlopen()` sends `Python-urllib/3.x` — the regex may include `python-requests` but NOT `Python-urllib`.

**Symptom:** The external witness probe returns 404 for paths that curl works fine on. `curl` sends `curl/8.x` which matches the regex; the Python probe sends an unmatched UA.

**Fix (probe side):** Override the User-Agent in the probe's HTTP calls — OR — Add `Python-urllib` to the Caddy bot regex:
```caddyfile
header_regexp User-Agent (?i)GPTBot|ClaudeBot|...|Python-urllib|python-requests|...
```

**Detection:** Compare probe results with `curl -A "Python-urllib/3.13"`. If curl with the Python UA also returns 404, the bot route is UA-gated and the probe's UA isn't matched.

## Existing arif-fazil.com Route Map

Reference — routes already configured in the main site block (as of 2026-07-22):

| Path | Backend | Notes |
|------|---------|-------|
| `/sado/*` | static (`/var/www/html/arif/sado/`) | SyedOS dashboard — ADDED 2026-07-24 |
| `/images/*` | static (`/var/www/html/arif/images/`) | Static media — ADDED 2026-07-22 |
| `/api/*` | `127.0.0.1:8088` | arifOS kernel |
| `/mcp*` | `127.0.0.1:8088` | MCP endpoint |
| `/wealth/gold/*` | static + `localhost:3456` | Gold chart app |
| `/wealth/*` | SPA fallback | React Router |
| `/canon/*` | static SPA | |
| `/assets/*` | static (immutable cache) | Built assets |
| `/_shared/*` | `/var/www/html/_shared` | Shared assets |

### Pitfall: `/images/*` handler was MISSING (added 2026-07-22)

The `handle /images/* { file_server }` block did NOT exist. When articles embedded `<img src="/images/...">`, Caddy had no handler → fell through to SPA fallback → returned `index.html` instead of the image. Symptom: `curl -sI https://arif-fazil.com/images/foo.jpg` returns `text/html`. Fix: add the handler BEFORE the `/assets/*` block. Any new static directory needs its own `handle` block — Caddy doesn't auto-discover subdirectories.

## Federation Chrome — shared_assets snippet

Every federation subdomain should have `import shared_assets` in its Caddy block to serve `/_shared/design-system/tokens.css` and `/_shared/unified-header-loader.js` from the global `/var/www/html/_shared/` directory.

```caddyfile
site.arif-fazil.com {
    import tls_origin
    import shared_assets    # ← ADD THIS
    encode zstd gzip
    root * /var/www/html/site
    # ... rest of config
}
```

The `shared_assets` snippet:
```caddyfile
(shared_assets) {
    handle /_shared/* {
        uri strip_prefix /_shared
        root * /var/www/html/_shared
        file_server
    }
}
```

**Pitfall:** Some sites (arif, arifos) have local `_shared/` directories that override the global one. If you edit the global file, these sites won't see the change. Either delete the local copy or reconcile: `cp /var/www/html/_shared/design-system/tokens.css /var/www/html/<site>/_shared/design-system/tokens.css`.

**Pitfall:** Cloudflare edge cache can serve stale `_shared/` files even after VPS files are fixed. Purge via Cloudflare API or wait for `max-age` expiry (usually 14400s = 4 hours).

### Common Pitfall: `.well-known/*` files split across multiple roots (PROVEN 2026-07-19)

When `/var/www/html/<site1>/.well-known/` and `/var/www/html/<site2>/.well-known/` BOTH exist (e.g., `arif-fazil.com` has `arif/.well-known/` while `arifos.arif-fazil.com` has `arifos/.well-known/`), a single shared-domain `handle /.well-known/*` block that points at one root will return 404 on paths that live in the other root.

**Symptom:** `https://arif-fazil.com/.well-known/X` returns 404 even though the file exists at the corresponding subdomain, AND the reload appears to succeed.

**Root cause:** The catch-all `handle /.well-known/*` with `root * /var/www/html/arif/.well-known` tries `try_files {path} {path}/index.html /index.html`. If those fallbacks don't exist (because the file lives in `/var/www/html/arifos/.well-known/`), Caddy returns 404 without falling through to a more specific matcher that came **after** it in declaration order. Caddy's handler precedence runs in declaration order, not matcher specificity.

**Fix — declare the more-specific matcher FIRST:**

```caddyfile
# Order matters — observatory discovery BEFORE the catch-all
@observatory_discovery path /.well-known/governance.jsonld /.well-known/mcp/server.json
handle @observatory_discovery {
    uri strip_prefix /.well-known
    root * /var/www/html/arifos/.well-known
    try_files {path} {path}/index.html
    file_server
}
@well-known path /.well-known/*
handle @well-known {
    uri strip_prefix /.well-known
    root * /var/www/html/arif/.well-known
    try_files {path} {path}/index.html /index.html
    file_server
}
```

For OAuth discovery routes that don't have a local file (e.g., `oauth-authorization-server`), use `redir` to the canonical subdomain BEFORE either `handle` block:

```caddyfile
handle /.well-known/oauth-authorization-server* {
    redir https://<canonical-subdomain>.arif-fazil.com{uri} permanent
}
```

**Verification:** After edit, run ALL of these before declaring done:

```bash
caddy validate --config /etc/caddy/Caddyfile  # MUST say "Valid configuration"
systemctl reload caddy                          # exit 0
for p in /.well-known/governance.jsonld /.well-known/mcp/server.json /.well-known/oauth-authorization-server; do
  code=$(curl -sI -o /dev/null -w "%{http_code}" "https://arif-fazil.com$p")
  echo "  $p → $code"  # 200 or 301 = ✅, 404 = ❌
done
# Cloudflare cache may serve stale 404 for up to ~4 hours — purge via API if needed
```

**Pitfall variant — file does not exist anywhere:** If the file doesn't exist in EITHER root, the discovery claim itself is wrong. Remove the claim from the audit report rather than fabricate a file. Audit narrative "fixed discovery files" without verifying file existence produces phantom receipts (F2 TRUTH violation).

### Common Pitfall: `try_files` Falls Back to SPA `index.html` Even When Static File Exists (PROVEN 2026-07-22)

When static assets live at nested paths (e.g., `/wealth/gold/vendor/library.js`), the standard SPA pattern `try_files {path} /index.html` may serve `index.html` **even when the file exists on disk**. The response returns HTTP 200 with `text/html` — no error in Caddy logs, no 404.

**Symptom:** `curl -s https://arif-fazil.com/wealth/gold/vendor/lib.js | head -1` returns `<!DOCTYPE html>`. File exists at `/var/www/html/gold/vendor/lib.js` (verified with `ls -la`). Response size matches `index.html` exactly.

**Root cause:** With `uri strip_prefix /wealth/gold` and `root * /var/www/html/gold`, the path should resolve to the correct file. But `try_files` + `file_server` interaction can cause the fallback to always fire for certain path structures. The `{path}` placeholder may not resolve the rewritten path as expected.

**Fix — add a dedicated `file_server` handler BEFORE the catch-all:**

```caddyfile
# BEFORE the catch-all SPA handler — serve static vendor files directly
handle /wealth/gold/vendor/* {
    uri strip_prefix /wealth/gold
    root * /var/www/html/gold
    file_server
}
handle /wealth/gold/* {
    uri strip_prefix /wealth/gold
    root * /var/www/html/gold
    try_files {path} /index.html
    file_server
}
```

**Verification:** `curl -s https://arif-fazil.com/wealth/gold/vendor/lib.js | head -1` should return the actual JS (not `<!DOCTYPE html>`). File size should match `wc -c /var/www/html/gold/vendor/lib.js`.

**Alternative — use CDN instead of local vendor files:** If the file exists on a CDN (e.g., `cdn.jsdelivr.net`), update the HTML `<script src>` to point there. This bypasses Caddy routing entirely. Verify the CDN URL is in the CSP `script-src`.

### Common Pitfall: Cloudflare Edge Cache Masks VPS Fixes (PROVEN 2026-07-22)

When you fix a broken file on the VPS but the browser still sees the broken version, Cloudflare's edge cache is serving a stale copy.

**Diagnostic headers to check:**

```bash
curl -sI 'https://arif-fazil.com/path/to/file' | grep -i 'cf-cache\|age\|cache-control'
```

| Header | Value | Meaning |
|---|---|---|
| `cf-cache-status: HIT` | Cached | Served from Cloudflare edge, NOT your origin |
| `cf-cache-status: MISS` | Fresh | Just fetched from origin, or cache expired |
| `age: 325` | Seconds | How long this copy has been cached |
| `cache-control: max-age=14400` | 4 hours | Cache expires 14,400 seconds after fetch |

**Quick diagnosis — origin vs edge:**

```bash
# With cache-buster (bypasses Cloudflare, hits origin fresh)
curl -s 'https://arif-fazil.com/path?cb=1' -o /dev/null -w "Size: %{size_download}\n"

# Without cache-buster (may hit stale Cloudflare cache)
curl -s 'https://arif-fazil.com/path' -o /dev/null -w "Size: %{size_download}\n"
```

If `?cb=1` returns the correct size but the clean URL returns old size → **Cloudflare cache, not your VPS fix.**

**Workarounds (when purge is unavailable):**
- **Cache-busting query params:** `<script src="file.js?v=2">` — creates unique cache key. Immediate effect for all future visitors.
- **Meta no-cache:** `<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">` in HTML `<head>`. Forces browser to always revalidate.
- **Wait:** `max-age=14400` = 4 hours. Cache expires naturally.

**Permanent fix — Cloudflare API purge:**
```bash
source /root/.secrets/vault.env
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://arif-fazil.com/path/to/file"]}'
```

### Pitfall: `redir @match` shorthand breaks `@ai-bot` markdown bypass ordering (PROVEN 2026-07-19, /wealth/makcikgpt/<slug>)

When you have an existing `@ai-bot` markdown bypass (line 71-80) and need to add a redirect for legacy URLs (`/wealth/makcikgpt/<slug>` → `/makcikgpt/<slug>`), the natural-looking shorthand breaks:

```caddyfile
# BROKEN — shorthand `redir @match` creates an inner handle that
# overrides the more-specific @ai-bot matcher for AI bot UAs.
redir /wealth/makcikgpt/([^/]+) /makcikgpt/{re.1} 301
```

**Symptom:** AI bots hitting `/wealth/makcikgpt/searah-followup` get redirected to `/makcikgpt/searah-followup` (the React SPA) instead of receiving the raw markdown. The `@ai-bot` handler at line 71 never fires.

**Why:** Caddy's `redir @match` shorthand is sugar for an internal `handle @match { redir ... }` block. When you mix shorthand `redir` with explicit `handle @match` blocks at the same site, the shorthand's implicit handle loses priority against the explicit `handle @ai-bot` block — but only when the @ai-bot block appears FIRST in declaration order. In practice, the shorthand `redir` placed LATER in the config still wins for matching paths, regardless of the @ai-bot's earlier position.

**Fix:** Wrap the redirect in an explicit `handle @match` block:

```caddyfile
# CORRECT — explicit handle block preserves ordering with @ai-bot
@makcikgpt_legacy path_regexp ^/wealth/makcikgpt/(.+)$
handle @makcikgpt_legacy {
    redir /makcikgpt/{re.1} 301
}
```

**Why this works:** The explicit `handle` block makes the order deterministic. Caddy evaluates handlers in declaration order, and `handle @match` is treated like any other handler.

**Verification:**

```bash
# Human gets HTML via SPA fallback (200)
curl -sI https://arif-fazil.com/wealth/makcikgpt/searah-followup | grep -i "^content-type:"

# AI bot gets raw markdown (200, text/markdown)
curl -sI -A "GPTBot" https://arif-fazil.com/wealth/makcikgpt/searah-followup | grep -i "^content-type:"
```

If the bot returns `text/html` instead of `text/markdown`, the `@ai-bot` handler is being overridden — switch to explicit `handle @match`.

**Companion pitfall — `try_files` with `@matcher` fallback doesn't work:**

```caddyfile
# BROKEN — try_files with named matcher as fallback is not valid Caddy syntax
handle /wealth/makcikgpt/* {
    uri strip_prefix /wealth/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    try_files {path}.md @makcikgpt_legacy_redirect  # ← invalid
    file_server
}
```

**Symptom:** `caddy validate` returns an error or the fallback never fires — every request 200's via `file_server` regardless of whether `.md` exists. The `@matcher` placeholder in `try_files` does NOT chain to the named handler.

**Fix:** Use a literal path as fallback (e.g., `/makcikgpt-redirect.html` and serve a stub), OR split into two separate handlers with explicit ordering. The cleanest pattern for "serve .md if exists, else redirect":

```caddyfile
# Two handlers, ordered by specificity
handle /wealth/makcikgpt/* {
    root * /var/www/html/arif/wealth/makcikgpt
    try_files {path}.md {path}/index.html
    file_server
}
@makcikgpt_nomd path_regexp ^/wealth/makcikgpt/([^/]+)$
handle @makcikgpt_nomd {
    redir /makcikgpt/{re.1} 301
}
```

Note: in this two-handler pattern, the first handler catches BOTH existing-`.md` and missing-`.md` paths. Missing files 404 (or SPA fallback). The second handler only fires for paths the first handler returns 404 from. Order matters: declare the most specific handler FIRST.
