# arif-fazil.com Full Site Architecture — reference map (2026-08-01)

Source: architecture diagram Arif shared 2026-08-01 ("Full Site Architecture" HTML/SVG).
Use this as the mental map when diagnosing routing, deploy, or design issues. Probe live
state before trusting any single line — this is a snapshot, not a live registry.

## Topology at a glance

- 1 apex domain: `arif-fazil.com` (Ψ SOUL, human surface)
- 22 subdomains · 7 backend organs · React 19 SPA + 140+ static pages
- Edge: Cloudflare CDN (SIN) → Caddy reverse proxy (`/etc/caddy/Caddyfile`, ~1970 lines, 22 vhosts)

## Layer 2 — Domain surfaces (Caddy routes)

| Surface | Role | Webroot / backend |
|---|---|---|
| `arif-fazil.com` | MAIN SPA (React 19 + Vite) | `/var/www/html/arif/` (dist, ~51MB) |
| `arifos.arif-fazil.com` | Observatory + MCP proxy | static `/var/www/html/arifos/` + `/mcp*` → :8088 |
| `mcp.arif-fazil.com` | Canonical MCP gateway | `/.well-known/oauth-*`, `/mcp*` |
| `geox.arif-fazil.com` | Earth intelligence | `/mcp*` → :8081 · ChatGPT registered |
| `wealth.arif-fazil.com` | Capital intelligence | `/mcp*` → :18082 · ChatGPT registered |
| `well.arif-fazil.com` | Readiness mirror | `/mcp*` → :18083 |
| `aaa.arif-fazil.com` | A2A cockpit | :3001 |
| `forge.arif-fazil.com` | A-FORGE webhook | :7071 |
| `syedos.arif-fazil.com` | SyedOS | `/var/www/html/syedos/` |
| `deploy.arif-fazil.com` | Webhook | :18000 |
| INFRA (LAN/internal) | ollama·prometheus·grafana·temporal·nats·monitor·vault999·headscale·openclaw·claw·wiki·apex | :11434 :9090 :3000 :8233 :8222 :8100 :8083 :18789 |

## Layer 3 — Backend organs (localhost MCP)

| Organ | Port | Role | Notes |
|---|---|---|---|
| arifOS | 8088 | Constitutional kernel | Judge · Seal · 8 tools · forward_auth gate |
| GEOX | 8081 | Earth intelligence | Wells · Seismic · Basins · ChatGPT reg |
| WEALTH | 18082 | Capital intelligence | NPV · Risk · Wisdom · ChatGPT reg |
| WELL | 18083 | Readiness mirror | Homeostasis · Vitality · REFLECT_ONLY |
| AAA | 3001 | A2A control plane | Agent cards · WARGAA allowlist |
| A-FORGE | 7071/7072 | Execution | Build · Deploy · never self-seals |
| OpenClaw | 18789 | Multi-surface gateway | Reversible ops |
| Commodity APIs | 3456 gold · 3457 oil · 3458 gas | WEALTH commodity feeds | |

## Layer 4 — Source + build + cron

- Source: `/root/arif-fazil.com` (git main) — src/pages/ (22 .tsx), src/data/essays/ (22 .ts),
  src/data/makcikgpt/ (22+ articles), public/ (140+ static .html), scripts/web-zen/
- Build: `npm run build` (Vite → dist/ ~51MB) → `rsync dist/ → /var/www/html/arif/`
- MakcikGPT dual-path (CRITICAL — see skill pitfalls #38, #15, #17):
  - Browser: `/world/makcikgpt/:slug` → React SPA (App.tsx → MakcikGptArticle / MakcikGPT)
  - Bot: `/world/makcikgpt/:slug.html` → static HTML (`makcikgpt-md/` · 81 files)
  - Gap (known): named slugs lack `.html` → fall back to listing page
- Cron immune system (3 jobs max, F13):
  - 🜂 Sense (15m) — web_zen doctor + curl probes, silent on GREEN
  - 🜂 Verify (6h) — Caddy↔App.tsx drift · dist staleness · bot dual-path · MCP surface audit
  - 🜂 Heal (6h) — auto-sync static files; gated git clean; never `--delete` / Caddy reload / npm build
- Plus: NS telemetry (15m), wealth watchdog (30m)

## Layer 5 — F13 sovereign gates

- Caddyfile mutation → 888 + explicit reload go
- `npm run build` + dist deploy → 888
- Irreversible mutations → 888_HOLD → F13 veto
- Heal: reversible-only (rsync public/ files)
- Sense + Verify: read-only · OBSERVE_ONLY

## Known drift (FI-008 era, resolve/verify before trusting)

- F1: `/institution*` + `/compliance*` were missing from Caddy `@spa_routes` → 404 (since patched)
- F2: `/world/{oil,gas,gold}` in stale dist bundle → wrong shell (since rebuilt)
- MakcikGPT named slugs lack `.html` static → bot fallback to listing

## How to probe (fast orientation)

```bash
# Route health
curl -s -o /dev/null -w '%{http_code}' https://arif-fazil.com/<path>
# Which bundle is live
curl -s https://arif-fazil.com/ | grep -oP 'index-[A-Za-z0-9]+\.js'
# Canon JSON served as JSON (not SPA shell)
curl -sI https://arif-fazil.com/canon/navigation.json | grep -i content-type
# Bot vs browser split (makcikgpt)
curl -s -A 'GPTBot/1.0' https://arif-fazil.com/world/makcikgpt/ | grep -o '<title>[^<]*</title>'
curl -s -A 'Mozilla/5.0'  https://arif-fazil.com/world/makcikgpt/ | grep -o '<title>[^<]*</title>'
```
