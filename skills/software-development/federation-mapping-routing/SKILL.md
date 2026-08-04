---
name: federation-mapping-routing
description: "Route geospatial/map/satellite/geocoding requests to the right federation organ. The federation has a vendor-sovereign mapping stack (Cesium + ArcGIS + STAC + OSM) — no Google Maps or Google Earth APIs anywhere by design. Load when the user asks 'do we have Google Maps?', 'can you do geocoding?', 'show me this on a map', 'render satellite imagery of X', '3D globe', 'where is X located', or any map / imagery / geocoding / routing / directions request. Classifies intent and routes to GEOX map tools, GEOX STAC, GEOX Cesium earth-volume app, or the Hermes `maps` skill accordingly."
version: 1.0.0
author: hermes-prime
license: MIT
metadata:
  hermes:
    tags: [maps, geocoding, satellite, imagery, geospatial, routing, cesium, stac, osm, arcgis, federation, dispatch]
    category: software-development
    supersedes: []
---

# Federation Mapping Routing

The arifOS federation has a deliberately **vendor-sovereign** mapping
stack. Google Maps, Google Earth, Google Places, and Google Earth Engine
APIs are **NOT** used anywhere in the federation — by design. When a user
asks for "map" / "satellite" / "geocode" / "directions" / "where is X" /
"3D globe", the answer is *yes* — but the underlying technology is
**Cesium + Esri ArcGIS World Imagery + ESA/USGS STAC + OpenStreetMap**,
not Google.

This skill is the routing layer. It classifies intent and dispatches
to the correct federation organ's mapping surface.

## The 4-Layer Mapping Architecture

| Layer | Federation owner | Source | NOT |
|---|---|---|---|
| **3D globe** (subsurface / 3D viz) | GEOX `ui://geox/earth-volume`, served at `/cesium/*` | CesiumJS + **Esri ArcGIS World Imagery** (`services.arcgisonline.com/.../World_Imagery/MapServer`). `Cesium.Ion.defaultAccessToken = undefined` — local Cesium, no Ion | NOT Google Earth 3D Tiles |
| **Satellite imagery** (multi-spectral, time-series) | GEOX `geox_stac_discover` | ESA **Sentinel-2 L2A**, **Sentinel-1 SAR** + USGS **Landsat C2 L2** via STAC catalogs (Earth Search, Planetary Computer, Copernicus, USGS) | NOT Google satellite |
| **Geological 2D maps** (basin/play/layer composition) | GEOX `geox_map_layers_list` / `geox_map_scene_plan` / `geox_map_render_preview` / `geox_map_export_package` | Custom `geox_regional_clean_v1` style profile, layers from GEOX knowledge pack | NOT Google Maps tiles |
| **Street-level geocoding / POI / routing** | **Hermes `maps` skill** | OpenStreetMap / Nominatim / Overpass / OSRM / TimeAPI.io. Zero API keys | NOT Google Maps API |

**The Google touchpoint in the entire federation**: the `maps_url` and
`directions_url` fields returned by the `maps` skill are **Google Maps
deep-links** (`https://maps.google.com/?...`) — tap-to-open shortcuts for
the user's browser. They are a courtesy, not an integration. No Google
API key exists in `/root/.env*`, scripts, or `.hermes/` configs.

## Intent → Organ Routing

### "Do you have Google Maps / Google Earth?" (capability question)
Answer: **No, by design.** The federation uses Cesium + ArcGIS + STAC +
OSM (vendor-sovereignty doctrine — see `dependency-sovereignty` skill).
Then offer the right alternative:

- 3D globe with subsurface overlays → GEOX Earth Volume
- Satellite imagery → GEOX STAC
- Basin/play context map → GEOX `geox_map_*`
- Address/coordinates/POI → `maps` skill (OpenStreetMap)

### "Where is X located?" / "Coordinates of place name" / "Address lookup"
**Use the `maps` skill** — `search "place name"` returns lat/lon.

```bash
python3 ~/.hermes/skills/maps/scripts/maps_client.py search "Kuala Lumpur"
```

If the user wants the location rendered on a basin/play geological map,
chain: `maps search` → `geox_workspace set basin=X` → `geox_map_scene_plan` → `geox_map_render_preview`.

### "Show me satellite imagery of region X"
**Use `geox_stac_discover`** — query ESA/USGS catalogs.

```python
geox_stac_discover(mode="search", bbox=[lon_min, lat_min, lon_max, lat_max],
                   datetime_range="2025-01-01/2025-12-31",
                   collections=["sentinel-2-l2a"], max_items=10)
```

If the user wants the imagery **on the 3D globe**, route to GEOX Earth
Volume (Cesium) and overlay the result.

### "Show me a map of basin X with layer Y" / "Geological context map"
**Use the GEOX map toolchain** in the canonical 4-verb chain:
1. `geox_map_layers_list(bbox=..., theme=...)` — discover
2. `geox_map_scene_plan(bbox=..., layer_ids=[...], map_purpose=...)` — plan
3. `geox_map_render_preview(scene_id=..., bbox=..., layer_ids=...)` — preview
4. `geox_map_export_package(...)` — export

### "3D globe" / "subsurface visualization" / "fly to location"
**Use GEOX Earth Volume** (Cesium) — `ui://geox/earth-volume` or
`/cesium/*`. Backed by `geox_3d_model_build`, `geox_subsurface_model`,
`geox_simulate_accommodation`, `geox_simulate_sequences`. Cesium's base
imagery is **Esri ArcGIS World Imagery** (NOT Google).

### "Driving directions from A to B" / "Distance" / "Travel time"
**Use the `maps` skill** — OSRM-backed. Modes: driving / walking / cycling.

```bash
python3 ~/.hermes/skills/maps/scripts/maps_client.py distance "KLCC" --to "Penang" --mode driving
python3 ~/.hermes/skills/maps/scripts/maps_client.py directions "Hotel" --to "Airport" --mode walking
```

### "Nearby restaurants / hospitals / pharmacies / etc."
**Use the `maps` skill** — Overpass API, 46 POI categories, Telegram
location-pin compatible.

```bash
python3 ~/.hermes/skills/maps/scripts/maps_client.py nearby 3.1390 101.6869 restaurant --radius 1000
```

### "What's the timezone at coordinates?"
**Use the `maps` skill** — `timezone lat lon`.

### "Well collar location / basin polygon / prospect footprint"
**Use GEOX** — `geox_basin(mode="profile", basin_name=...)`,
`geox_workspace(set basin=X)`. These are federation-internal coordinates
from the EGS ontology, not street-level. The `maps` skill handles
street-level.

## Pitfalls

- **Don't promise Google Maps**: it's not in the federation by design.
  Offer the sovereign alternative.
- **Don't use the `maps` skill for basin/play/prospect locations** — those
  live in GEOX's EGS ontology, not on OpenStreetMap.
- **Don't use GEOX for street addresses** — GEOX has no geocoding surface.
  Use `maps` skill.
- **Cesium Earth Volume's imagery is Esri ArcGIS**, not Google. Don't
  claim otherwise.
- **`Cesium.Ion.defaultAccessToken = undefined`** — the federation runs
  local Cesium with no Ion access. Don't add tokens.
- **The standalone `georeference-map` GEOX app is DEPRECATED** (2026-07-16
  ZEN-15 cleanup). Use `geox_basin + geox_deep_time_state` for spatial
  context instead.

## Verification

To confirm the federation's mapping architecture matches this skill:

```bash
# Should return 0 hits anywhere
grep -ri "GOOGLE_MAPS_API_KEY\|googleapis.com/maps\|places.googleapis" /root/.env* /root/.hermes/ /root/scripts/ 2>/dev/null

# Should find Cesium + ArcGIS imagery
grep -l "ArcGisMapServerImageryProvider" /root/GEOX/geox-gui/public/cesium/index.html

# Should find STAC references
grep -l "sentinel-2-l2a" /root/GEOX/geox-gui/src/components/EarthVision/EarthVisionPanel.tsx

# Should find OSM/Nominatim in maps skill
grep -l "nominatim\|overpass" /root/.hermes/skills/productivity/maps/scripts/maps_client.py
```

## Reference Files

- `references/federation-mapping-filemap.md` — exact source file paths, technology references, and verification greps for the entire federation mapping surface.