# Politics / Shadow Static Pages

The `/politics/shadow/` pages on arif-fazil.com are **STATIC HTML** — NOT React/TS components.

## Architecture

```
Source:  public/politics/shadow/index.html  (hand-authored HTML)
         public/politics/shadow/pm/*/       (JS-driven, fetch from shadow-decoder.json)
Data:    public/politics/shadow/data/shadow-decoder.json
TS ref:  src/data/shadowPms.ts              (dev reference, NOT build input)
Build:   npm run build → copy-static-html.js mirrors to dist/politics/shadow/
Deploy:  cp dist/politics/shadow/index.html → /var/www/html/arif/politics/shadow/
Caddy:   /politics/shadow/* → root /var/www/html/arif (file_server)
```

## Critical Pitfall

**`src/data/shadowPms.ts` is a DEV REFERENCE — changing TS alone does NOT update the live page.** The HTML is manually authored. When making changes:
1. Edit `public/politics/shadow/index.html` (the canonical HTML source)
2. Optionally sync `src/data/shadowPms.ts` for dev consistency
3. Run `npm run build` from `/root/arif-fazil.com/sites/arif-fazil.com/`
4. Deploy: `cp dist/politics/shadow/index.html /var/www/html/arif/politics/shadow/`

## Shadow Verdict System

- **TERSEDAR** (green) — Awakened/conscious. Only Hussein Onn and Razak (as of 2026-08-03).
- **SAMAR** (amber) — Separuh Gelap (half-dark). Tunku, Abdullah, Ismail Sabri.
- **TENGGELAM** (red) — Drowned. Mahathir, Najib, Muhyiddin, Anwar.

## Razak Special Case (F13 ruling)

Arif specifically ruled: Razak = TERSEDAR, not SAMAR. Rationale: "He is APEX — at the time when he die, he was building." He died before seeing DEB corrupted. The dying-man's-urgency made his governance crystal clear, not ambiguous.

## PM Profile Pages

The individual PM pages (`/politics/shadow/pm/{slug}/`) are JS-driven — they fetch `shadow-decoder.json` and render dynamically. These were deployed from the backup at `/root/backups/www-html-20260801T115957Z-pre-web-canon-reconcile/forge/shadow/`.

## Portraits

The SAMAR-themed index uses real Wikipedia portrait URLs. The AI-generated portraits (MiniMax image-01) were placed at `/politics/shadow/images/` but the SAMAR theme does not use them — it uses Wikipedia URLs directly in the HTML.

## Related

- Page Instruments: `/root/web-canon/canon/page-instruments.json` declares `/politics` as "Shadow Board" instrument
- Caddy config: `/etc/caddy/Caddyfile` — `/politics/shadow/*` routes to `/var/www/html/arif/`
- Legacy redirect: `/shadow/ → /politics/shadow/` (301)
