# GEOX Probe Gotchas — Live Session Evidence

## The Lane-Enforcement Gate Response

When probing `geox_surface_status(mode=health)` **without** a governed session, the actual response is:

```json
{
  "error": "LANE_ENFORCEMENT · verdict=HOLD · trace=gov-24e912688dca · lane=discovery · Tool 'geox_surface_status' is in discovery lane — session_id required · fix: Call arif_init(mode=init) first to establish governed session."
}
```

**Critical interpretation:** This is NOT "connector dead." This is "connector reachable, but you need to initialize a governed session first." The two are fundamentally different:

| Probe response | What it means | Agent action |
|---|---|---|
| `LANE_ENFORCEMENT · verdict=HOLD` | Server is UP, gated by auth | Call `arif_init(mode=init)` then re-probe |
| Connection refused / timeout | Server is DOWN | Declare UNAVAILABLE |
| 401/403 | Auth failure (wrong token, expired) | Declare UNAVAILABLE for this session |
| 429 | Rate-limited | Back off, retry after cooldown |
| Valid JSON with data | Server healthy | Proceed with CONNECTOR claims |

## The Correct Probe Sequence for GEOX

```
Step 1: arif_init(mode=init, intent="spatial query", ...)
  → returns session_id + session_token + lease_id + actor_id

Step 2: geox_surface_status(mode=health, session_id=..., actor_id=..., lease_id=..., session_token=..., sct=...)
  → returns registry of all GEOX tools + health status

Step 3: geox_h3_spatial_index(mode=latlng_to_cell, lat=0.0, lng=0.0, resolution=0, session_id=..., ...)
  → smoke query — if this returns a cell ID, the full spatial pipeline is live
```

## A-FORGE Probe Alternative

If using A-FORGE as the execution engine instead of direct GEOX MCP:

```
forge_probe(organs="geox", include_latency="true", session_id=..., actor_id=..., lease_id=..., session_token=..., sct=...)
```

This wraps the probe in governed lease context automatically. Returns organ liveness + latency.

## Lessons from Live Session (2026-08-04)

- First probe attempt without `arif_init` returns the gate response. This is expected, not an error.
- The GEOX MCP server definition being present in the config does NOT mean the server is reachable — it only means the routing is configured.
- Rate: after `arif_init`, the smoke query typically completes in <1s. If it takes >5s, suspect server load or partial failure.
