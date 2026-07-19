# Coordinate Verification Protocol

> Learned 2026-07-07. Three coordinates wrong by 0.34–0.67°. Block name unverified. Arif: "Location location location!!!"

## Rule

**Every coordinate plotted on a map MUST have a source.** No exceptions.

## Epistemic Tags

| Tag | Meaning | Example |
|---|---|---|
| `OBSERVED` | GPS measurement or published coordinates with exact lat/lon | Wikipedia city coords, well surface location from log header |
| `ESTIMATE` | Read from published map figure (digitized, not exact) | Fault trace from Morley 2023 Figure 2, MV caldera from ResearchGate inset |
| `SPECULATED` | From memory, mental model, or "roughly where I think it is" | **NEVER PLOT THIS** — search first, plot second |
| `UNVERIFIED` | User-provided name, not independently confirmed | "Block P" — search PSC lists before building analysis |

## Verification Workflow

### Step 1: City/landmark coordinates
```
Source priority: Wikipedia > geonames.info > latlong.info > countrycoordinate.com
Example: Ranau → Wikipedia/geonames → 5.954°N, 116.664°E
```

### Step 2: Geological feature coordinates
```
Source priority: Published paper with GPS > Paper figure (digitize) > Gazetteer > UNVERIFIED
Example: Lipad MV → Published GPS: 5°11'15"N 118°30'8"E (ewenhooi blog + Tabin papers)
Example: Maliau Basin → Wikipedia: 4.830°N, 116.900°E
```

### Step 3: PSC block names and boundaries
```
Source priority: PETRONAS MPM bid round > OE Digital/Offshore Energy > OnePetro papers > UNVERIFIED
Known Sabah blocks: G, J, H, K, N, R, X, 2K, 2V, 2W, 2X
"Block P" = NOT confirmed as PSC designation — "P" in "L-B-P" is structural trend name
```

### Step 4: Offshore structural features
```
Source: Published map figures only — digitize with caution
NSPW extent, Sabah Trough axis, FTB boundary = all SCHEMATIC unless tied to well/seismic data
Label as "approx from [paper name] Figure [N]"
```

## Verification Commands

```bash
# Search Wikipedia for coordinates
web_search(query="FeatureName GPS coordinates latitude longitude")

# Search published papers for geological feature locations
web_search(query="feature name" Sabah coordinates site:researchgate.net)
web_search(query="feature name" offshore Sabah latitude longitude site:onepetro.org)

# Search PSC block names
web_search(query="PETRONAS PSC Block X Sabah deepwater" site:oedigital.com)
web_search(query="PETRONAS Malaysia Bid Round PSC Sabah blocks awarded")
```

## What Happened (2026-07-07)

| Feature | Plotted | Actual | Error | Source of actual |
|---|---|---|---|---|
| Lipad MV (Tabin) | 5.3°N, 118.0°E | 5.188°N, 118.502°E | **0.5° lon** | GPS: 5°11'15"N 118°30'8"E |
| Maliau Basin | 5.5°N, 117.5°E | 4.830°N, 116.900°E | **0.67° lat** | Wikipedia verified |
| Ranau | 5.85°N, 117.0°E | 5.954°N, 116.664°E | **0.34° lon** | latlong.info |
| "Block P" | 5.5°N, 116.2°E | **UNKNOWN** | Block may not exist | Khamis 2018: "L-B-P Ridge" = structural trend, not block |

**Impact:** 0.5° longitude error ≈ 55 km at equator. In exploration terms: wrong basin, wrong prospect, dry hole.

## The Arif Rule

> "Location location location!!! That's the foundation for Geox. Can you imagine u ai give wrong drill location!!!"

In geoscience, coordinate accuracy is non-negotiable. A map with wrong coordinates is worse than no map — it gives false confidence.
