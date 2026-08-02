# Deploy Path Pitfall (2026-08-03)

## The Caddy root is `/var/www/html/arif/` — not `sites/`

The Caddy root for arif-fazil.com's main domain is `/var/www/html/arif/` — **NOT** `/var/www/html/sites/arif-fazil.com/`.

| Path | Purpose |
|---|---|
| `/root/arif-fazil.com/sites/arif-fazil.com/` | Project source (React + Vite + `public/`) |
| `/root/arif-fazil.com/sites/arif-fazil.com/dist/` | Build output (`npm run build`) |
| `/var/www/html/arif/` | **Caddy live webroot** — files here are served |
| `/var/www/html/sites/arif-fazil.com/` | Staging/backup mirror (NOT live) |

## Deploy workflow

```bash
# Build
cd /root/arif-fazil.com/sites/arif-fazil.com
npm run build

# Deploy to live
rsync -av dist/ /var/www/html/arif/

# For static HTML pages in public/ subdirectories, also copy manually:
cp public/politics/shadow/index.html /var/www/html/arif/politics/shadow/index.html
```

## Verify

```bash
curl -sI https://arif-fazil.com/politics/shadow/ | head -3
# Must return HTTP/2 200
```

## Symptom of wrong path

Deploying to `/var/www/html/sites/arif-fazil.com/` silently fails — `curl` to the live URL returns 404 or stale content because Caddy never serves from that path. The `sites/` tree is for development mirroring, not serving.
