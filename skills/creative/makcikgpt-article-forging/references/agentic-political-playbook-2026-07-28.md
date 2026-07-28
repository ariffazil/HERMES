# Agentic Political Playbook — NS PRN Workflow (2026-07-28)

> **Workflow:** Research election → map seats → build GIS page → write playbook → create WhatsApp templates
> **Source session:** 2026-07-28 — Negeri Sembilan PRN16 election analysis for BN-PN side
> **Linked from:** makcikgpt-article-forging SKILL.md — Political analysis + WhatsApp templates

---

## The Workflow

| Phase | Output | Tools |
|---|---|---|
| 1. Research | Seat-by-seat 2023 data, candidate lists, polls, swing analysis | web_search, smart_fetch, ElectionData.MY, The Sun, Sinar Daily, Straits Times |
| 2. Map | 36-seat breakdown: 2023 winner, majority %, demography, 2026 prediction | HTML table, color-coded by coalition |
| 3. GIS Page | Interactive Leaflet map with lat/lng coords per seat, OpenStreetMap dark tiles | public/politics/ns-election/index.html + Leaflet 1.9 + Caddy route |
| 4. React SPA | ElectionCartographyMap.tsx — cartogram grid + Leaflet toggle + filter bar + seat drawer | React component + App.tsx route |
| 5. Playbook | 8 hot seats deep-dive: message templates per DUN in BM, counter-narrative, GOTV checklist | Static HTML page + WhatsApp templates |
| 6. Deploy | Caddy route + rsync + verify 200 on all surfaces | deploy-site.sh, sudo sed for Caddy |

## Key Architecture Decisions

### Static path for new pages
New standalone pages go under public/<path>/index.html. Static HTML is faster to deploy and debug. React SPA for interactive components.

### Caddy route protocol
Every new static path needs:
1. A handle /<path>/\* block in /etc/caddy/Caddyfile with try_files {path} {path}/index.html /index.html
2. sudo caddy validate before reload
3. sudo caddy reload

### Leaflet integration
- npm install leaflet @types/leaflet (NOT react-leaflet)
- L.tileLayer with OpenStreetMap dark tiles
- lat/lng per seat from postcode.my
- Toggle between cartogram grid and real GIS map via React state

## Political Analysis Rules
1. Frame BN-PN gains as default story. DAP holds as thing to be proven.
2. Identify 6-8 swing seats that determine government.
3. Mark every seat where Bersatu could split opposition vote.
4. Majority < 1000 = marginal. > 5000 = safe.
5. Different seats need different messages (Felda vs urban vs semi-rural).
