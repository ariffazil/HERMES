# Sabah Deepwater PSC Blocks — Verified Reference

> **CRITICAL:** This file exists because plotting blocks from memory caused coordinate errors (2026-07-07). Always verify against PETRONAS MPM maps before plotting block boundaries. Block coordinates below are approximate — PSC boundary polygons are NOT publicly available.

## Known Blocks (Deepwater Sabah)

| Block | Operator | Key Fields/Discoveries | Water Depth | Status | Notes |
|---|---|---|---|---|---|
| **Block K** | PTTEP Sabah Oil (was Murphy) | Kikeh (oil, 2002 discovery), Siakap North, Kakap | ~1,300m | Producing since 2007 | Malaysia's first deepwater oil. PTTEP acquired from Murphy. ~120 km NW of Labuan. |
| **Block H** | PTTEP Sabah Oil (was Murphy) | Rotan (gas), Buluh (gas), Alum, Bemban, Permai | >1,500m | First gas Feb 2021 | Rotan Sands = turbidite reservoirs deposited on NSPW mud canopy. PTTEP 56% interest in Rotan. |
| **Block P** | Murphy Sabah Oil | — | 3,000-9,000 ft (~900-2,700m) | Exploration | ~4,246 sq km. Adjacent to Block K. NOT part of PTTEP acquisition of Murphy's H/K assets. |
| **Block N** | BHP Billiton → various | Tepat-1 (oil, 2018) | Ultra-deepwater | Exploration | Proved Oligo-Miocene carbonate trend in ultra-deepwater Sabah. |
| **Block Q** | BHP Billiton | — | Ultra-deepwater | Exploration | |
| **Block R** | INPEX | — | Ultra-deepwater | Exploration | |
| **Block 2K** | TotalEnergies (35%) / PETRONAS Carigali (40%) / Shell (25.1%) | — | Up to 3,000m | PSC signed ~2022 | Ultra-deepwater. 1,952 sq km. Completes licensing of 5 ultra-deepwater blocks. |
| **Block G** | ConocoPhillips (35%) / PETRONAS (30%) / Shell | Malikai (oil), Gumusut | ~500m | Producing | Malikai Phase 2 first oil Feb 2021. |
| **Block J** | ConocoPhillips | SNP (oil) | — | Producing | Unitized field. SNP Phase 2 first oil Nov 2021. |
| **Block X** | JX Nippon | B-1 discovery | Deepwater | Exploration | |

## Key Structural Features (Verified Coordinates)

| Feature | Approximate Coordinates | Source | Notes |
|---|---|---|---|
| West Baram Line (WBL) | ~4.0-4.3°N, 113.5-118°E | Hall 2017, GSM | Runs E-W along Sarawak-Sabah border. NOT at 5.5°N. |
| Crocker Fault | ~115.65-116.20°E, 5.0-5.95°N | Literature | Runs NW-SE through western Sabah (KK to Beaufort area). |
| Tongod Fault | ~116.80-117.10°E, 5.0-5.70°N | Literature | Interior Sabah, runs NNE. |
| Sabah Trough | Offshore NW, ~5.5-6.3°N | Hall 2017 | Flexural/gravity-driven, NOT active trench. |
| NSPW Domain | Offshore NW Sabah, ~5.5-7.0°N, 114-117.5°E | Morley 2023 Geosphere | MOBILE SHALE domain, NOT onshore. Deepwater fold-thrust belt. |
| Mud Canopy | Offshore ~6.2-6.5°N, 116°E area | Morley 2023 | ~1,900 km². ~50 mud-volcano centres at ~10.5 Ma. OFFSHORE, not onshore. |

## Key Cities (GeoNames Verified)

| City | Lon (°E) | Lat (°N) |
|---|---|---|
| Kota Kinabalu | 116.07 | 5.98 |
| Ranau | 116.66 | 5.95 |
| Beaufort | 115.74 | 5.35 |
| Keningau | 116.16 | 5.34 |
| Sandakan | 118.12 | 5.84 |
| Lahad Datu | 118.34 | 5.03 |
| Tawau | 117.89 | 4.25 |
| Semporna | 118.62 | 4.48 |
| Telupid | 117.12 | 5.63 |
| Tongod | 117.00 | 5.27 |

## Onshore Mud Volcanoes/Seeps (Approximate)

| Feature | Approximate Lon (°E) | Approximate Lat (°N) | Notes |
|---|---|---|---|
| Lipad MV (Tabin) | ~118.30 | ~5.10 | Active, Lahad Datu district |
| Maliau Basin MVs | ~116.90 | ~4.80 | Conservation area |
| Labuk Valley Seeps | ~117.40 | ~5.60 | |
| Telupid Seeps | ~117.12 | ~5.63 | |
| Interior Seeps | ~116.50 | ~5.40 | General interior division |

## Offshore Mud Volcano Features (Morley 2023)

| Feature | Approximate Lon (°E) | Approximate Lat (°N) | Notes |
|---|---|---|---|
| Western MV Cluster | ~115.5 | ~6.3 | Offshore |
| NSPW Canopy Centre | ~116.2 | ~6.5 | Morley 2023 epicentre |
| Eastern MV Cluster | ~117.0 | ~6.4 | |
| Sabah MV Caldera | ~117.5 | ~6.2 | ~1,100m water depth |

## Lessons Learned (2026-07-07 Session)

1. **NSPW was plotted onshore** — it's OFFSHORE NW Sabah. Major error.
2. **WBL was placed at ~5.5°N** — it's at ~4.0-4.3°N (Sarawak-Sabah border).
3. **Ranau was shifted 0.8° east** — actual 116.66°E, was plotted at ~117.5°E.
4. **Block P was relabeled as Block K** — without verifying they're different blocks with different operators.
5. **Mud canopy was shown in southern interior** — it's OFFSHORE, in the NSPW domain.

**Root cause:** All errors came from plotting from memory instead of verified sources. The cardinal rule: if you can't verify a coordinate, don't plot it.
