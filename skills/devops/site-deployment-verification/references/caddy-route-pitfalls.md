# Caddy Route Pitfalls (proven 2026-08-02)

## 1. `root` directive path doubling

When adding a handler for `/forge/*` with content at `/var/www/html/forge/`:

**WRONG:** `root * /var/www/html/forge` → request `/forge/index.html` resolves to `/var/www/html/forge/forge/index.html` → 404

**CORRECT:** `root * /var/www/html` (the parent). Caddy appends the URI path to root.

```
handle /forge/* {
    root * /var/www/html
    try_files {path} {path}/index.html /forge/index.html
    file_server
}
```

The 404 is silent and looks identical to "content missing." Always verify immediately after `systemctl reload caddy`.

## 2. Retired route cleanup — three-surface consistency

When a route has a Caddy handler but no content and no surfaces.json entry:

1. Remove the Caddy handler block
2. Remove from `@spa_routes` matcher if present (otherwise SPA fallback returns 200 for a dead route)
3. Add to surfaces.json as `status: "gone"`

Verify all three agree: Caddy 404 + no SPA fallback + surfaces.json gone.

A route that 404s from Caddy but 200s from SPA fallback is a phantom — bots see 200, content is empty.

## 3. `/ready` 503 may be TRUTHFUL

arifOS `/ready` runs `_runtime_selftest()` which probes as `actor='anonymous'`/`'selftest'`.
Constitutional floors L02/L03/L04/L07/L08 correctly HOLD for unverified actors.
The selftest interprets HOLD as FAIL → 503.
The heart_check probe deliberately sends an injection payload → correctly gets CRITICAL.

Before "fixing" a 503 /ready: read the failure reasons. If they say "Constitutional HOLD: L02, L03..." the kernel is working correctly — the test design is wrong, not the system. Fix requires sovereign ruling (change selftest to use verified session, or accept HOLD-as-PASS). Never force /ready green by suppressing floor checks.

## 4. Sitemap generator must read surfaces.json

`generate-discovery.cjs` originally hardcoded 6 static routes. surfaces.json has 16+ live pages. Fix: read static routes from surfaces.json, keep article URLs from makcik-source.cjs. Path: `path.join(SITE_ROOT, "..", "..", "surfaces.json")` (SITE_ROOT = sites/arif-fazil.com, surfaces.json = /var/www/html/surfaces.json).
