# Federation Mapping Stack — Source File Map

Exact file paths and technology references discovered 2026-08-04.

## GEOX Cesium 3D Globe

- **Cesium HTML shell**: `/root/GEOX/geox-gui/public/cesium/index.html`
  - Title: "GEOX X-3D Globe — Subsurface Volumetric Intelligence"
  - Base imagery: `Cesium.ArcGisMapServerImageryProvider.fromUrl('https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer')`
  - Token: `Cesium.Ion.defaultAccessToken = undefined` (local Cesium, no Ion)
  - Terrain: `terrain: undefined` (flat ellipsoid)
  - Default view: Malay Basin at `(110.5, 4.5)` → 500km altitude, -45° pitch
  - Subsurface layers: gravity (red), magnetic (blue), seismic (yellow), all semi-transparent
  - Wired to: `geox_subsurface_model`, `geox_simulate_accommodation`, `geox_simulate_sequences`
- **Cesium manifest**: `/root/GEOX/geox-gui/public/cesium/manifest.json`
  - Display name: "X3D Cesium Subsurface Viewer"
  - External URL: `https://geox.arif-fazil.com/cesium/?session={session_id}`
- **Caddy serving**: `/root/compose/Caddyfile` line 863 — `@gui_assets path /cesium/* /assets/* /geox-icon.svg`

## GEOX STAC / Satellite Imagery

- **EarthVisionPanel.tsx**: `/root/GEOX/geox-gui/src/components/EarthVision/EarthVisionPanel.tsx`
  - Collections: `sentinel-2-l2a`, `sentinel-1-grd`, `landsat-c2-l2`
  - Default: `sentinel-2-l2a` with 20% max cloud
  - Uses STAC search → COG/tile URL → overlay as imagery layer
- **Python STAC fetcher**: `geox_core.io.landsat_stac_fetcher.LandsatSTACFetcher` (tested in `tests/test_earth_surface_2.py`)
- **MCP tool**: `geox_stac_discover` — queries Earth Search, Planetary Computer, Copernicus, USGS

## GEOX 2D Map Toolchain (earth_map domain)

- **Tool definitions**: `/root/GEOX/resources/smithery.yaml` lines 321-344
- **Capabilities**: `/root/GEOX/resources/capabilities/geox_capabilities.json`
- **MCP App registry**: `/root/GEOX/resources/apps/registry.json` — see `geox://registry/apps` resource
- **Earth Map app**: `ui://geox/earth-map` (backed by `apps/workbench-v1.html`)
- **Tools**:
  1. `geox_map_layers_list` — list available map layers + bbox + metadata
  2. `geox_map_scene_plan` — plan composition: layer ordering, zoom, annotations
  3. `geox_map_render_preview` — render PNG preview with style profile
  4. `geox_map_export_package` — package layers into portable format
- **Style profile**: `geox_regional_clean_v1`
- **DEPRECATED**: `georeference-map` app (2026-07-16 ZEN-15) — replaced by `basin + deep_time_state`

## Hermes `maps` Skill (OSM-based)

- **Skill**: `/root/.hermes/skills/productivity/maps/SKILL.md`
- **Script**: `/root/.hermes/skills/productivity/maps/scripts/maps_client.py`
- **Data sources**: Nominatim, Overpass API, OSRM, TimeAPI.io — **no API key**
- **8 commands**: search, reverse, nearby, distance, directions, timezone, area, bbox
- **46 POI categories** (restaurant, hospital, pharmacy, etc.)
- **Telegram location pin compatible** — extract lat/lon from message, pass to `nearby`
- **Google Maps deep-links**: `maps_url` and `directions_url` are **tap-to-open** convenience links, NOT API calls

## What Does NOT Exist (verified)

- **Google Maps API key**: `grep -ri "GOOGLE_MAPS\|googleapis.com/maps\|places.googleapis"` across `/root/.env*`, `/root/.hermes/`, `/root/scripts/` = **0 hits**
- **Google Earth Engine**: no `ee` import, no GEE Python client anywhere
- **Google Maps JS API**: no `maps.google.com/maps/api/js` loader, no `google.maps.*` in any frontend
- **Google Places API**: no places.googleapis.com references
- **Google Static Maps API**: no `maps.googleapis.com/maps/api/staticmap` calls
- **Google Earth 3D Tiles**: Cesium uses ArcGIS World Imagery, not Google photorealistic 3D

## Cross-References

- Vendor sovereignty doctrine: `dependency-sovereignty` skill
- Caddy reverse proxy config: `caddy-reverse-proxy` skill
- GEOX tool registry: `geox://capabilities` MCP resource
- GEOX apps catalog: `geox://registry/apps` MCP resource
