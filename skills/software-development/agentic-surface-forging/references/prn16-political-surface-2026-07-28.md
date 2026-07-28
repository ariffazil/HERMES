# PRN16 Political Surface — Dual-Species Navigation Worked Example

**Date:** 2026-07-28
**Domain:** Negeri Sembilan PRN 2026
**Surface URL:** https://arif-fazil.com/politics/ns-election/

## The Three-Layer Surface

| Layer | What | URL |
|-------|------|-----|
| **Human** | Leaflet GIS map + 9 invariants + playbook | `/politics/ns-election/` |
| **Agent** | llms.txt section + sitemap entry | `llms.txt` + `sitemap.xml` |
| **Machine** | Live sensory telemetry JSON | `/data/politics/ns_live_telemetry.json` |

## Route Aliases Created

| Alias | Target | Type |
|-------|--------|------|
| `/politics` | `/politics/ns-election/` | Static HTML redirect |
| `/politics/` | `/politics/ns-election/` | Caddy SPA handler |
| `/malaysia` | `https://wealth.arif-fazil.com/malaysia` | Caddy 301 redirect |
| `/vitals` | `https://wealth.arif-fazil.com/vitals` | Caddy 301 redirect |

## WhatsApp Field Templates

3 variants at `wa.html`:
- **Varian Makcik** — BN nostalgia + anti-DAP sentiment + daily life language
- **Varian Anak Muda** — Economy/cost-of-living focus + anti-establishment
- **Varian FELDA** — Water quality + infrastructure + local issues

## Agentic Playbook Content

8 swing seats identified:
- **N32 Linggi** (MB fight — HOT) — PH vs BN vs Bersatu
- **N14 Ampangan** (329 majority — ULTRA_MARGINAL) — PH vs BN vs Bebas
- **N9 Lenggeng** (Aliff's area) — BN hold, Bersatu split risk
- **N25 Paroi** — PAS stronghold, Bersatu contest risk
- Plus 4 more marginal seats

Live seat projection: PH 18 + BN 16 + PN 3 = HUNG (deadlock)
Bersatu holds kingmaker leverage. Palace intervention possible.

## Telemetry Stream Shape

```json
{
  "total_signals_ingested": 1645,
  "sentiment_index": { "ph_positive": 39.8, "bn_positive": 39.2, "pn_positive": 21 },
  "voter_turnout_projection": 74.1,
  "highest_volatility_seat": "N32 Linggi",
  "ground_telemetry_seats": [{...per-seat data...}]
}
```

## Deployment Sequence

1. Build React SPA with politics routes
2. Deploy to Caddy with `handle /politics/*` block
3. Add static HTML fallback for bare `/politics` path
4. Add Caddy redirect rules for `/malaysia`, `/vitals`
5. Update sitemap.xml + llms.txt
6. `npm run build` (generates sitemap from site config)
7. Commit + push
