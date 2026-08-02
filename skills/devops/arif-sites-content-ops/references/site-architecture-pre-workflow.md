# Site Architecture Pre-Workflow

**When Arif asks to add/relocate/restructure content on arif-fazil.com, never just propose a path.**
The site is instrument-driven architecture, not a blog. Study first, propose second.

## Required study steps

1. **Fetch `surfaces.json` live** — `https://arif-fazil.com/surfaces.json`
   - This is the SINGLE canonical surface catalog
   - Doctrine: "If it is not in surfaces.json, it does not get served to a machine."
   - All machine catalogs (sitemap, llms.txt, missions.json) are generated views of this file

2. **Read `page-instruments.json`** — `/root/web-canon/canon/page-instruments.json`
   - Every page is an instrument, not a poster
   - Each instrument declares: territory, palette, instrument type, motion, data source, status
   - Hard invariant: "A page cannot choose its own hero. The route registry chooses the hero."

3. **Crawl the live site** — understand actual URL structure, namespace conventions, what's live vs proposed vs gone vs redirect

4. **Propose integration, not placement** — Ask: "What territory? What instrument? What palette?"

## Key architecture decisions (as of 2026-08-02)

| Page | Instrument | Status | Notes |
|------|-----------|--------|-------|
| `/politics/` | shadow-board | proposed | "The Shadow Board — dark institutional blue, shadow cabinet as org-chart instrument, each seat a dossier link." |
| `/politics/ns-election/` | GIS-engine | live | PRN16 — already deployed |
| `/forge/` | execution-shell | live | A-FORGE execution, NOT content hosting. Shadow/Shadow Decoder content should NOT go here. |
| `/world/oil/`, `/world/gas/`, `/world/gold/` | commodity-chart | live/proposed | Commodity dashboards |
| `/wealth/*` | institutional-pulse | live (subdomain) | On wealth.arif-fazil.com — VITALS, Malaysia pulse |

## Namespace conventions

- `/politics/` — institutional/political intelligence (Shadow Board, election GIS, shadow PM/CEO dossiers)
- `/world/` — civic journalism + commodity intelligence (MakcikGPT, oil/gas/gold)
- `/economics/` — WEALTH capital intelligence (redirects to wealth.arif-fazil.com)
- `/earth/` — GEOX geoscience
- `/doctrine/` — constitution, federation topology
- `/writing/` — narrative essays
- `/000/`, `/999/` — genesis archive, proof chamber
- `/forge/` — EXECUTION ONLY. Not for content pages. Not for shadow.

## Arif's direct instruction (2026-08-03)

> "Hang pi tengok site live and bagitau macam mana nak selit benda shadow ni. Aku x mau hang just tepek macam tu ja. The site is architecture system design system. Jangan nak buat bangang. Watch ur own shadow."

Translation: Study the architecture. Understand the design system. Integrate, don't paste. The site is not a blog — it's an instrument system.

## Shadow content canonical home

All Shadow content (PM profiles, CEO dossiers, institutional analysis, DERITA map, cascade events) belongs under `/politics/`:

```
/politics/                    → Shadow Board (org-chart instrument)
/politics/shadow/             → Shadow Decoder landing
/politics/shadow/pm/{slug}/   → Individual PM profiles
/politics/shadow/ceo/         → Shadow CEO index
/politics/shadow/ceo/petronas/ → PETRONAS CEO B-score
/politics/shadow/institution/ → Institutional shadow dimensions
/politics/shadow/derita/      → DERITA map (33+33+33)
/politics/shadow/cascade/     → Cascade events timeline
/politics/shadow/seal/        → VAULT999 seal
```

This was DESIGNED by Arif in `page-instruments.json` — the `/politics` instrument IS the Shadow Board. We're implementing the design, not inventing it.
