---
name: spatial-intelligence-substrate
description: >-
  Source-routed spatial intelligence — claim taxonomy, capability registry, and
  connector verification for any spatial/location/geography question. Forces
  the agent to declare WHERE the spatial answer came from (INTERNAL,
  CONNECTOR, BROWSER, or UNAVAILABLE) and to refuse spatial claims that have
  no verified source. Stops hallucinated "I have Google Maps / Macrostrat / the
  whole Earth" answers. USE WHEN: "where is X", "map of Y", "coordinates of Z",
  "what's at lat/lng", "satellite imagery of A", "route from B to C", "basin
  geology at D", "geocode this address", "I need a map", "show me the area",
  or any user assumption that the agent "has access to" a spatial platform.
trigger:
  - spatial
  - location
  - geography
  - map
  - coordinates
  - lat/lng
  - GIS
  - geological map
  - satellite imagery
  - routing
  - geocoding
  - basin
  - stratigraphy
  - macrostrat
  - lokasi
  - koordinat
  - peta
  - geografi
  - pemetaan
category: governance
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  mcp_servers: [geox]  # optional but recommended for CONNECTOR claims
metadata:
  hermes:
    tags: [governance, spatial, geography, epistemic, source-routing, claims, connector-verification, geo]
    related_skills: [governance-patterns, authority-boundary-audit, verify-gate, bangang-surface-audit, deep-codebase-audit]
---

## Cross-Agent Doctrine Reference

This skill implements the arifOS Spatial Intelligence Doctrine (canonical: /root/ariffazil/docs/doctrines/spatial-intelligence-doctrine.md). If the doctrine and this skill conflict, the doctrine wins.

---

# Spatial Intelligence Substrate

**Every spatial claim must declare its source. No internal possession of any map, globe, or imagery platform — only routed access if a connector is alive.**

This is the substrate the agent stands on when answering location, geography, geology, or imagery questions. The default human intuition is "the AI has a map in its head." That intuition is wrong. The agent has:

- Some **INTERNAL** compute (H3 indexing, coordinate math, distance/bearing)
- Some **CONNECTOR** access (if and only if a live tool/MCP server is reachable)
- A **BROWSER** channel (only as visual observation — no semantic query over pixels)
- A long list of **UNAVAILABLE** platforms it cannot reach

If the agent cannot route the question to a verified source, it must say so. Hallucinated "yes, I can show you that area on Google Earth" is the failure mode this skill exists to prevent.

## 0. Connector Liveness Is a Per-Statement Claim

A connector that was reachable earlier in the session may not be reachable now. **Source mode classification must reflect the current call site, not prior-session memory.**

Anti-pattern observed: agent says "I have GEOX" or "I can query Macrostrat" based on architectural knowledge, then discovers mid-answer that the GEOX MCP is in cooldown or returned `LANE_ENFORCEMENT`. The first claim is already a lie by the time the second clause arrives.

**Hard rule:** classify source mode **after** the live probe, never before. If you cannot or did not probe this turn, your claim about CONNECTOR availability is `SPEC_SPATIAL` at best, never `API_SPATIAL`.

When state changes from CONNECTOR to UNAVAILABLE mid-conversation, **state the transition in the answer** rather than papering over it, e.g.:

> "GEOX was verified live earlier this session but is now returning connection-refused; I cannot make `API_SPATIAL` claims until it recovers. Reclassifying this turn as `UNAVAILABLE`."

Mid-conversation confidence decay is honest reporting of liveness, not an excuse — the answer itself becomes the audit trail.

**Sub-rule (post-statement):** never invent a successful probe result to justify a claim you want to make. If the probe actually failed, the answer declares UNAVAILABLE. Confabulating "verified live" to keep the claim API_SPATIAL is the fabrication-prevention failure mode under a different name.

---

## 1. When to Load This Skill

Load this skill the moment the user asks anything that implies spatial knowledge:

- "Where is X?" / "Show me the map of Y" / "What's at these coordinates?"
- "Give me the route from A to B"
- "What basin / formation / stratigraphy is at location L?"
- "Can you pull up satellite imagery of region R?"
- Any user assertion that you "have access to" Google Earth / Google Maps / Macrostrat / Sentinel / Landsat
- Any task where the answer must reference a real geographic coordinate, tile, polygon, or imagery asset

Malay triggers: lokasi, koordinat, peta, geografi, pemetaan, imejan satelit.

**If the question is purely conceptual** ("what is a basin?", "explain H3 indexing"), this skill still applies to any spatial EXAMPLE the agent generates — label the example's source mode.

---

## 2. Spatial Capability Registry (the four modes)

Every spatial data source falls into exactly one of these four access modes. Before answering, the agent must classify the source it intends to use.

| Mode | Meaning | Examples | Trust level |
|---|---|---|---|
| **INTERNAL** | Computed locally in this session — no network, no API. Deterministic from inputs you already have. | H3 lat/lng→cell, k-ring neighbors, polygon fill, haversine distance, bearing, bbox math, CRS transforms | High — verifiable |
| **CONNECTOR** | Requires a live external API/MCP server/tool to be reachable right now. Answer is only as fresh as the last query. | GEOX MCP (`geox_h3_spatial_index`, `geox_basin`, `geox_stac_discover`, `geox_dde_reason`), Macrostrat API, OSM/Nominatim, CesiumJS globe via GEOX UI server | Conditional — live-verified |
| **BROWSER** | Visual observation only. Pixel render via headless browser / screenshot. No semantic query over the image. | CesiumJS globe rendered in browser tab, OSM map screenshot, any map tile image | Low — descriptive only |
| **UNAVAILABLE** | No integration exists in this agent. Cannot be queried. | Google Maps Platform, Google Street View, Google Earth Engine, Bing Maps, Mapbox (unless explicitly provisioned), HERE, TomTom | None — must refuse or redirect |

**Default policy**: if the user asks about a UNAVAILABLE platform, do not pretend. Offer the nearest available alternative or explain what is possible.

---

## 3. Spatial Claim Taxonomy (epistemic labels)

Every sentence in a spatial answer that makes a factual claim about a place must carry exactly one of these labels, prefixed or inline. No unlabeled spatial claims.

| Label | Meaning | Use when |
|---|---|---|
| `OBS_SPATIAL` | Directly observed from a tool result returned this session | You just ran `geox_basin(...)` and quoted its output |
| `API_SPATIAL` | Returned by a structured API call (could be cached) | "Macrostrat says unit X has age Y" — quote endpoint + timestamp |
| `DER_SPATIAL` | Computed from coordinates, layers, or other spatial inputs | "Distance from A to B is 12.4 km" — derived from haversine over two coords |
| `INT_SPATIAL` | Interpretive spatial/geological reasoning — uses domain knowledge | "This fault likely trends NE because of the offset pattern" |
| `SPEC_SPATIAL` | Hypothesis — not yet evidence-backed | "There may be a sand body at this location" |
| `UNKNOWN` | No verified spatial source available | Refusal mode — see §6 |

Example in a real answer:

> `[OBS_SPATIAL]` The H3 cell at lat 3.1390, lng 101.6869 (Kuala Lumpur) is `852a1073fffffff` at resolution 9. `[DER_SPATIAL]` The great-circle distance to Singapore (1.3521, 103.8198) is approximately 316 km.

If a sentence mixes observation and interpretation, split it. Do not stack labels.

---

## 4. No "Entire Map" Rule

When the user asks any variant of:

- "Do you have Google Earth?"
- "Can you access all of Google Maps?"
- "Can you query the full Macrostrat database?"
- "Can you pull any satellite image from anywhere?"

The mandatory response is:

> **"No internal possession. Only routed access if a connector exists and is currently verified live. I do not have a copy of Google Earth, Google Maps, or Macrostrat stored inside me. I can route a query to a live connector only if the relevant MCP server / API is reachable in this session. Want me to probe?"**

Then either probe or ask permission to probe. Never describe what "would be possible" as if it were actual capability.

**Why this matters**: users routinely conflate "LLM with geospatial training data" and "LLM with live geospatial access." They are different. The agent may have *training-data recall* about places (often stale, often wrong about coordinates) but that is not the same as a live query. Treat training-data recall as `INT_SPATIAL` or `SPEC_SPATIAL` at best, never as `OBS_SPATIAL`.

---

## 5. Connector Verification Protocol — DO THIS BEFORE EVERY CONNECTOR CLAIM

Before answering any spatial question that depends on a CONNECTOR source, the agent **must** verify the connector is actually alive in this session. Verification is a 3-step gate:

### Step 1 — Probe the registry / surface

Try the lightest available health check:

```bash
# For GEOX MCP (preferred for geology + H3 + STAC + basins)
mcp geox:geox_surface_status(mode=health)

# Or a smoke query that always succeeds if the server is up
mcp geox:geox_h3_spatial_index(mode=latlng_to_cell, lat=0.0, lng=0.0, resolution=0)
```

If your environment does not have a GEOX probe, try `forge_probe(organ='geox')` or check the active MCP servers via `claude mcp list` (or whatever your runtime surfaces them as).

**Live probe gotchas:** the GEOX probe commonly returns a `LANE_ENFORCEMENT · verdict=HOLD · session_id required` response rather than a clean health check. This is **NOT** "connector dead" — it means the server is reachable but you need `arif_init(mode=init)` first. See `references/geox-probe-gotchas.md` for the full interpretation table and the correct probe sequence.

### Step 2 — Check authorization / lane

GEOX and similar governed organs may respond with a lane-enforcement or session-init gate:

```
LANE_ENFORCEMENT · verdict=HOLD · session_id required
→ fix: Call arif_init(mode=init) first to establish governed session.
```

If you see this, **do not declare the connector dead.** The connector is reachable; you simply haven't initialized a governed session yet. Run `arif_init(mode=init, ...)` and re-probe.

### Step 3 — Classify the result

| Probe result | Status to declare |
|---|---|
| Returns data within ~3s | `CONNECTOR · verified live this session` |
| Returns lane/session gate | `CONNECTOR · reachable, awaiting governed session init` |
| Times out / connection refused | `UNAVAILABLE · connector down this session` |
| Returns 401/403 / quota error | `UNAVAILABLE · auth/quota exhausted` |
| Returns 429 / rate-limit | `UNAVAILABLE · rate-limited (try again in N seconds)` — also see §9 pitfall #5 |

**Critical rule**: if you have not run the probe this session, you have not verified the connector. Do not write `CONNECTOR` in your answer.

---

## 6. The Source-Routed Response Format (mandatory template)

For every spatial/location answer that depends on more than pure recall, structure the response using this template. Skip sections that don't apply, but never omit `Source used`, `Coverage`, `Limits`.

```markdown
### Spatial answer — <one-line topic>

**Location resolved:** <place name + coords if known + uncertainty>
**Source used:** INTERNAL | CONNECTOR · <server> · verified <yes/no this session>
**Freshness:** <live query just now | cached N min ago | training-data recall>
**Coverage:** <what this source can answer for this query>
**Limits:** <what this source CANNOT do — explicit>
**Claim labels used:** OBS_SPATIAL | API_SPATIAL | DER_SPATIAL | INT_SPATIAL | SPEC_SPATIAL | UNKNOWN

<the actual answer, with each factual sentence carrying one of the labels above>
```

### Worked examples

**Example A — verifiable H3 lookup**

> ### Spatial answer — H3 cell for Kuala Lumpur
>
> **Location resolved:** Kuala Lumpur, Malaysia — lat 3.1390, lng 101.6869
> **Source used:** CONNECTOR · geox · verified live this session via `geox_h3_spatial_index`
> **Freshness:** live query, just now
> **Coverage:** any lat/lng → H3 cell at resolutions 0–15; k-ring neighbors; polygon fill
> **Limits:** does NOT return map tiles, does NOT visualize the hex, does NOT include any geographic attributes (population, country, terrain)
> **Claim labels used:** API_SPATIAL
>
> `[API_SPATIAL]` At resolution 9 the cell is `852a1073fffffff`. `[DER_SPATIAL]` Its 1-ring contains 6 neighbors and 2-ring contains 18.

**Example B — declarative refusal**

> ### Spatial answer — "What's at lat 35.6762, lng 139.6503?" (Tokyo)
>
> **Location resolved:** Tokyo, Japan — lat 35.6762, lng 139.6503
> **Source used:** UNAVAILABLE · no live geocoding/reverse-geocode connector verified this session
> **Freshness:** n/a
> **Coverage:** none from live tools; I can offer training-data recall only
> **Limits:** no Macrostrat unit query, no OSM POI lookup, no reverse-geocode result possible without a CONNECTOR probe
> **Claim labels used:** UNKNOWN (for live data); INT_SPATIAL only if you want general descriptive context
>
> I cannot fetch live data for this coordinate right now. Want me to probe GEOX (`geox_h3_spatial_index` and `geox_basin`) and try again?

**Example C — visual / browser-rendered**

> ### Spatial answer — what does the 3D globe look like over the Malay Basin?
>
> **Location resolved:** Malay Basin, offshore Peninsular Malaysia — bbox approx [3.0, 100.0, 8.0, 106.0]
> **Source used:** BROWSER · CesiumJS globe rendered headless via GEOX UI server
> **Freshness:** rendered just now
> **Coverage:** visual observation of rendered tiles, lighting, terrain, bathymetry shading
> **Limits:** BROWSER mode gives **pixels only**. I cannot semantically query the globe ("which tectonic plate is this?", "what's the seafloor age here?") — those require CONNECTOR (e.g. `geox_basin`).
> **Claim labels used:** OBS_SPATIAL (only for what is visually present in the screenshot)

---

## 7. Step-by-Step: How to Answer a Spatial Question

Follow this checklist every time:

1. **Classify the question type.** Is the user asking for (a) a place lookup, (b) coordinates, (c) a route, (d) imagery, (e) geological attributes, (f) a "do you have X platform?" meta-question? Different sources handle different types.

2. **Resolve the location first.** Convert any place name → lat/lng bbox before searching. If the user gave coordinates, validate they parse. If ambiguous, ask.

3. **Pick the source mode.** Decide whether the question is answerable via INTERNAL math, needs a CONNECTOR, can be answered via BROWSER observation, or is UNAVAILABLE. Default to the least powerful source that still answers — INTERNAL > CONNECTOR > BROWSER > UNAVAILABLE.

4. **Verify any CONNECTOR claim** via the protocol in §5. Do not skip this step even if you "used it earlier in the session" — MCP servers can drop mid-conversation.

5. **Apply the response template** from §6. Every spatial answer that depends on external data carries Source / Coverage / Limits.

6. **Label every factual sentence.** Use the taxonomy from §3. No unlabeled spatial claims.

7. **Refuse honestly when the answer cannot be sourced.** The `UNKNOWN` label exists for a reason. "I don't have access to live data for this query" is a valid, complete answer.

8. **Offer the next step.** Either probe a connector you haven't tried, route to a related INTERNAL computation, or ask the user how they want to proceed.

---

## 8. Known Spatial Sources Inventory (reference table)

This is the canonical registry of spatial sources the agent either has, can route to, or cannot reach. Update it when a new connector comes online or goes offline.

| Source | Access Mode | What it covers | What it CANNOT do |
|---|---|---|---|
| **H3 spatial index** | INTERNAL / CONNECTOR (via geox) | Hex grid indexing, lat/lng→cell, k-ring neighbors, polygon fill, cell aggregation | No map tiles, no visualization, no semantic attributes |
| **Macrostrat API** | CONNECTOR (via geox_dde_reason, geox_basin) | Global stratigraphy, geologic units, columns, lithologies, paleogeography | Requires live API; strongest coverage in North America, New Zealand, Caribbean; sparse in equatorial Africa / interior Asia |
| **STAC catalogs** | CONNECTOR (via geox_stac_discover) | Satellite imagery discovery (Sentinel-2, Landsat, Copernicus, Planet) | Discovery only — actual asset download/streaming is a separate step |
| **OSM / Nominatim** | CONNECTOR (if provisioned) | Geocoding, POIs, basic routing, directions | Rate-limited (~1 req/sec); no business listings, no real-time traffic, no reviews |
| **OSRM / Valhalla** | CONNECTOR (if provisioned) | Driving/walking/cycling routing | No live traffic, no transit schedules, no turn-by-turn navigation |
| **CesiumJS globe** | CONNECTOR (via GEOX UI server) | 3D Earth visualization with ArcGIS imagery, terrain, bathymetry | Requires GEOX UI server running; semantically opaque |
| **CesiumJS in headless browser** | BROWSER | Visual globe rendering, tile fetch | No semantic query; pixel observation only |
| **OGC WMS / WFS** | CONNECTOR (if provisioned) | Raster tile / vector feature services from agencies | Per-service auth, varying coverage, no global aggregator |
| **Overpass API (OSM)** | CONNECTOR (if provisioned) | Complex OSM queries (buildings, landuse, amenities within bbox) | Rate-limited; query syntax is fragile |
| **Google Maps Platform** | UNAVAILABLE | N/A in this agent | No API key, no integration, deliberately avoided (vendor sovereignty) |
| **Google Earth Engine** | UNAVAILABLE | N/A | Not integrated; would require Google auth |
| **Google Street View** | UNAVAILABLE | N/A | Not integrated |
| **Mapbox / Bing / HERE / TomTom** | UNAVAILABLE | N/A unless explicitly provisioned | Vendor-locked; no sovereign alternative |
| **Training-data recall** | INT_SPATIAL (max) | General facts about well-known places, geography, geology | **NOT live**; coordinates often stale or wrong; never `OBS_SPATIAL` |

---

## 9. Pitfalls — read before answering anything spatial

These are the recurring failure modes. Burn them in.

1. **"I have GEOX" ≠ "GEOX is connected right now."**
   Possessing the MCP server definition is not the same as the server being live, healthy, and authorized for this session. Probe every time, or your `CONNECTOR` claim is a lie.

2. **"Macrostrat has X" ≠ "I can query Macrostrat for X right now."**
   Knowing that a database contains a record is `INT_SPATIAL` at best. Retrieving it is `API_SPATIAL` and requires a live query. Don't merge them.

3. **A screenshot of Google Maps ≠ API access to Google Maps.**
   If the agent browsed to maps.google.com and screenshotted a route, that is `BROWSER` observation of pixels. It does not give the agent programmatic routing, geocoding, or static-map API access. The next user request ("now do it for a different city") will fail unless you actually have an API.

4. **"I can do spatial queries" needs connector verification first.**
   Treat every spatial capability claim as suspect until the probe runs. Even if you verified it 10 minutes ago — servers restart, sessions expire, quotas refill slowly. Re-probe on every new top-level user query if it depends on a connector.

5. **OSM / Nominatim rate limits can silently fail.**
   Nominatim's usage policy is 1 request/second. Exceed it and you get either a 403 with no body, or an HTML error page that looks like "no results." If the response is empty or shape-mismatched, suspect rate-limiting before suspecting the data.

6. **GEOX server may be in cooldown after consecutive failures.**
   Like any governed organ, GEOX can enter a cooldown state after repeated errors, validation failures, or unauthorized attempts. Symptoms: timeouts on every probe, or `verdict=HOLD` responses. The right move is to back off, tell the user, and retry after the cooldown — not to hammer it.

7. **Lat/lng precision is not free information.**
   "Malaysia" is a country, not a coordinate. Don't pretend a country-level reference is `OBS_SPATIAL`. Down-grade to `INT_SPATIAL` or `SPEC_SPATIAL` until you have a real point.

8. **Confusing training-data recall with live data.**
   An LLM trained on web pages containing coordinates *will* produce coordinates when prompted. They are often wrong, often stale, often from a different place entirely. Treat any coordinate you "remember" as `SPEC_SPATIAL` unless verified by a live query.

9. **Mixing label types in one sentence.**
   "The basin (OBS_SPATIAL) probably contains (INT_SPATIAL) oil-prone source rocks" is two claims. Split it. Unlabeled compound sentences are the #1 way epistemic labels get laundered into false certainty.

10. **Don't route a basin question to CesiumJS.**
    BROWSER visual mode cannot answer "what formation is at this coordinate?" It can only describe what the rendered globe looks like. If the question is semantic, you need `geox_basin` or `geox_dde_reason` — a CONNECTOR.

---

## 10. Verification Steps (before publishing any spatial answer)

Before sending the response to the user, run through this checklist:

- [ ] Did I declare the **Source used** (INTERNAL / CONNECTOR / BROWSER / UNAVAILABLE)?
- [ ] If CONNECTOR — did I **probe live this session** and report the result?
- [ ] Did I declare **Coverage** (what this source can answer)?
- [ ] Did I declare **Limits** (what this source cannot do)?
- [ ] Did I declare **Freshness** (live / cached / recall)?
- [ ] Did I label **every factual sentence** with the taxonomy?
- [ ] If I refused, did I label the refusal `UNKNOWN` and offer a next step?
- [ ] If I produced coordinates, did they come from a live query, not training-data recall?
- [ ] If I used BROWSER mode, did I avoid semantic claims about the pixels?
- [ ] Did I avoid the "entire map" trap (claiming possession of Google Earth / Macrostrat / etc.)?

If any checkbox is unchecked and the answer is going to the user, fix it first.

---

## 11. Integration with Other Governance Skills

This skill is the spatial specialization of the broader epistemic-governance substrate. It composes with:

- **`governance-patterns`** — provides the OBS/DER/INT/SPEC label family this skill extends with the `_SPATIAL` suffix.
- **`authority-boundary-audit`** — for the BANGANG surface pattern: claiming spatial authority the agent doesn't have is exactly the kind of inflated authority this skill guards.
- **`verify-gate`** — the four gates (authority + evidence + reversibility + witness) apply; spatial answers must clear all four.
- **`bangang-surface-audit`** — running this skill is itself an anti-BANGANG move; the agent's tendency to claim "yes I have Google Earth" is the canonical inflated-authority failure.
- **`deep-codebase-audit`** — when auditing a tool that depends on spatial sources, verify which of the four modes each source actually operates in.

---

## 12. What This Skill is NOT

- Not a geocoding engine. INTERNAL mode is math, not gazetteer lookup.
- Not a replacement for `geox_basin` / `geox_stac_discover`. This skill decides *when and how* to call them; it does not implement them.
- Not a map renderer. BROWSER mode observes pixels; it does not draw maps.
- Not a license to hallucinate. If you can't source the answer, refuse.

The substrate is honest routing — nothing more, nothing less.