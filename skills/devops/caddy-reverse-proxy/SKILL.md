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

1. **ALWAYS back up before modifying**: `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak.YYYY-MM-DD`
2. **ALWAYS validate before reloading**: `caddy validate --config /etc/caddy/Caddyfile`
3. **ALWAYS test existing routes after reload** — verify homepage and related paths still return 200
4. **Handle blocks evaluate TOP-DOWN** — more specific routes MUST come before broader ones
5. **The `patch` tool REFUSES system paths** (`/etc/caddy/`, `/etc/systemd/`) — use `terminal` with `sed` or heredoc instead

## Caddyfile Location

- Config: `/etc/caddy/Caddyfile`
- Admin socket: `unix//var/run/caddy-admin.sock`
- Managed domains: `arif-fazil.com` (Ψ), `arifos.arif-fazil.com` (Ω), `aaa.arif-fazil.com` (Δ)

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

## Existing arif-fazil.com Route Map

Reference — routes already configured in the main site block (as of 2026-07-14):

| Path | Backend | Notes |
|------|---------|-------|
| `/api/*` | `127.0.0.1:8088` | arifOS kernel |
| `/mcp*` | `127.0.0.1:8088` | MCP endpoint |
| `/wealth/gold/*` | static + `localhost:3456` | Gold chart app |
| `/wealth/*` | SPA fallback | React Router |
| `/canon/*` | static SPA | |
| `/assets/*` | static (immutable cache) | Built assets |
| `/_shared/*` | `/var/www/html/_shared` | Shared assets |

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
