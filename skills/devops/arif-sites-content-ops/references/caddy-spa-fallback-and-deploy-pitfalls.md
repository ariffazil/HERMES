# Caddy SPA Fallback & Deploy Pitfalls (2026-08-03 shadow-board deploy)

Session: deployed `/politics/shadow/derita/` (RASA DERITA) + `/politics/shadow/board/` (Shadow Board) on arif-fazil.com. Two non-trivial traps found, plus a reusable Caddy 404 debug path.

## Pitfall 1 — deploy-vps.sh `npm ci` fails with ERESOLVE

`npm ci` dies with `ERESOLVE could not resolve: vite-plugin-ssg@0.1.0` — the plugin's peer requires `@vitejs/plugin-react@^4.0.0` while package.json declares `^5.1.1`. The script's `npm ci || npm install` both fail → deploy aborts at the build step.

**Do NOT touch dependencies during a deploy** (out of scope, "Never batch"). The working pattern:
1. `node_modules` already exists and is proven — run `npm run build` directly (no ci/install).
2. Sync `dist/` manually following the script's atomic pattern:
   ```bash
   SHA=$(git rev-parse --short HEAD)
   TEMP="${WEBROOT}.tmp.$SHA" && mkdir -p "$TEMP" && cp -a sites/arif-fazil.com/dist/* "$TEMP/"
   [ -d "$WEBROOT" ] && mv "$WEBROOT" "${WEBROOT}.bak.$SHA"
   mv "$TEMP" "$WEBROOT" && chown -R www-data:www-data "$WEBROOT"
   ```
3. Snapshot Caddyfile, `caddy reload --config /etc/caddy/Caddyfile --force`, verify live.

The lockfile/peer drift is a separate maintenance item — settle it on its own pass, not mid-deploy.

## Pitfall 2 — Caddy handle-block matcher specificity swallows SPA sub-routes

Root cause of `/politics/shadow/derita/` + `/politics/shadow/board/` returning 404 while `/politics/shadow/` was 200:

A pre-existing `handle /politics/shadow/* { root * /var/www/html/arif; file_server }` (no try_files) — added 2026-07-31 for static Shadow Decoder dossiers — **wins over** the broader `handle /politics/* { try_files {path} {path}/index.html /index.html; file_server }`. In a Caddy route group, the **more specific path matcher executes first and terminates the group**. So any SPA client-side route under `/politics/shadow/` (no static file on disk) hit `file_server` → 404, never reaching the fallback.

**Rule:** every `handle <path>/* { file_server }` block that serves a folder containing SPA routes MUST carry a try_files fallback:
```
handle /politics/shadow/* {
    root * /var/www/html/arif
    try_files {path} {path}/index.html /index.html
    file_server
}
```
When adding a new SPA route under a path that already has a Caddy handle block, **check the existing handle block first** — do not assume the broader SPA fallback will catch it.

## Reusable Caddy 404 debug path

When a live route 404s and the cause is not obvious:

1. **Identify who serves the 404.** `curl -sI` — `server: cloudflare` means traffic proxies through Cloudflare. `cf-cache-status: DYNAMIC` = pass-through (origin's response). Empty 404 body ≠ Caddy's standard text body — suspicious of a non-file_server handler.
2. **Probe origin directly with correct SNI.** `curl -sk -H "Host: ..." https://127.0.0.1/...` fails with `000` because curl sends SNI=`127.0.0.1` → Caddy resets the TLS handshake. Use:
   ```bash
   curl -sk --resolve arif-fazil.com:443:127.0.0.1 "https://arif-fazil.com/path/"
   ```
3. **Isolate semantics with a mini server.** Reproduce the config shape in `/tmp/mini.conf` (`caddy run --config /tmp/mini.conf`). Mini 200 vs prod 404 = config semantics are fine; the runtime config/route order is the problem. Mini 404 = you misunderstand the semantics.
4. **Inspect the adapted route tree.** `caddy adapt --config /etc/caddy/Caddyfile --adapter caddyfile | python3 -c ...` — dump routes in order, look for overlapping path matchers and route groups. A path matcher that appears earlier (or more specific within a group) than the fallback explains the 404.
5. **`caddy validate --config` before reload; `caddy reload --config ... --force` after patching.** Snapshot `/etc/caddy/Caddyfile` to a `.bak.<ts>` first (F1).

## Surfaces SOT notes

- Canonical catalog: `/root/arif-fazil.com/surfaces.json` (doctrine: "If it is not in surfaces.json, it does not get served to a machine."). `site-architecture-surfaces-2026-08-03.md` points at `sites/arif-fazil.com/surfaces.json` — treat as the same catalog (mirrored).
- `/politics/*` was **never** declared in surfaces.json (ns-election pre-existing, un-declared). For shadow surfaces, follow the `/forge/` pattern: declare-but-hidden — status `live`, no navCanon entry.
- `/index.html` returning 404 at origin is **pre-existing** (`@spa_routes` matches `/` exactly, not `/index.html`) — not a regression; don't chase it mid-deploy.
