# Site Architecture — Surface Catalog & Routing Map (2026-08-03)

Discovered during shadow content integration session. Maps the key routing surfaces
and how they connect.

## Surface catalog (surfaces.json)

`/root/arif-fazil.com/sites/arif-fazil.com/surfaces.json` is the **machine SOT**.
Every page must be declared here (status: live/gone/redirect, type: page/dynamic_page/machine/api).
Any surface not in this file does not get served to machines (llms.txt, sitemap.xml, etc.).

## Routing structure — top-level sections

| Route | Section | Content |
|-------|---------|---------|
| `/` | Home | Sovereign identity, portfolio |
| `/earth/` | Earth | Discoveries, well portfolio (geoscience) |
| `/economics/` | Economics | WEALTH capital briefing |
| `/world/` | World | MakcikGPT (civic journalism) + Commodities (oil/gas/gold) |
| `/politics/` | Politics | NS Election (single page: /politics/ns-election/). Redirect from bare /politics/. |
| `/writing/` | Writing | Essays |
| `/doctrine/` | Doctrine | Constitution, federation topology, manifesto |
| `/institution/` | Institution | Three-audience surface (human/agent/institution) |
| `/forge/` | Forge | A-FORGE Shadow Decoder (hidden — not in navCanon) |
| `/000/` | Genesis | Wisdom canon, agent context |
| `/999/` | Verification | Proof chamber, vault verification |

## Dual commodity surfacing

Commodity pages have TWO surfaces:
1. **React SPA route:** `/world/oil`, `/world/gas`, `/world/gold` — SPA shell, CommodityPage component
2. **Static standalone:** `/oil/`, `/gas/`, `/gold/` — standalone HTML served from `/var/www/html/{oil,gas,gold}/`

The React SPA routes (`/world/oil` etc) redirect from the legacy static paths (`/oil/` → `/world/oil`).
The static pages are NOT React — they're standalone HTML with their own CSS and API fetch scripts.

## /politics/ section

Currently single-page: `/politics/ns-election/`. No sub-section landing page.
To add `/politics/shadow/` as a parallel surface:
- Add route in App.tsx
- Add surface declaration in surfaces.json
- Add Caddy handler
- Update navCanon (regenerated from canon) or add to civicLinks in footer

## Navigation (navCanon.ts)

`src/data/navCanon.ts` is **auto-generated** from `/root/web-canon/canon/navigation.json`
via `scripts/generate-nav-canon.cjs`. Never hand-edit. The header says: "AUTO-GENERATED ...
DERIVED — never hand-edit. Edit canon, regenerate."

Current primary nav (6 items): Start · Earth · Economics · World · Politics · Read.

## /forge/ surface

Declared in surfaces.json as `"title": "A-FORGE Shadow Decoder"` with mission `build`.
Served from `/var/www/html/forge/`. NOT in navigation — reachable by direct URL only.
This is a "hidden surface" — deliberate architectural pattern for sovereign-only content.

## Key files for architecture changes

| File | Role | Edit? |
|------|------|-------|
| `surfaces.json` | Machine catalog SOT | Yes, add new surfaces |
| `src/App.tsx` | React Router routes | Yes, add Route declarations |
| `src/data/navCanon.ts` | Navigation items | NO — auto-generated from canon |
| `/root/web-canon/canon/navigation.json` | Navigation CANON | Yes, then regenerate |
| `/etc/caddy/Caddyfile` | Caddy handlers | Yes, add handler blocks |
| `src/data/siteContent.ts` | Link arrays (civicLinks, etc.) | Yes, for footer/indirect links |
