# GEOX Rich server.json — Reference Example

> **Source:** 2026-07-19 Phase 4 registry listing
> **Deployed to:** `/var/www/html/geox/.well-known/mcp/server.json`
> **Accessible at:** `https://geox.arif-fazil.com/.well-known/mcp/server.json` *(when Caddy routing updated)*

```json
{
  "$schema": "https://raw.githubusercontent.com/modelcontextprotocol/specification/main/schema/mcp-server.json",
  "name": "GEOX — Earth Intelligence",
  "version": "v2026.07.19",
  "description": "Governed geoscience coprocessor under arifOS constitutional floors F1-F13. Evidence-only earth intelligence: basin analysis, seismic interpretation, petrophysics, prospect evaluation, deep-time paleogeography, and 9 interactive MCP Apps.",
  "repository": "https://github.com/ariffazil/GEOX",
  "license": "BSL-1.1",
  "author": {
    "name": "Muhammad Arif bin Fazil",
    "url": "https://arif-fazil.com"
  },
  "endpoint": "https://geox.arif-fazil.com/mcp",
  "transport": ["streamable-http", "sse"],
  "protocolVersion": "2025-06-18",
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": true,
    "tasks": true,
    "ui": true
  },
  "tools": {
    "totalRegistered": 78,
    "publicCount": 24,
    "categories": {
      "basin": ["geox_basin", "geox_basin_backstrip", "geox_sediment_mass_balance", "geox_thermal_maturity_history"],
      "seismic": ["geox_seismic_compute", "geox_seismic_ingest", "geox_seismic_interpret"],
      "petrophysics": ["geox_petrophysics"],
      "well": ["geox_well_desk", "geox_well_ingest"],
      "prospect": ["geox_prospect"],
      "geophysics": ["geox_gravmag_studio", "geox_geomechanics", "geox_subsurface_model"],
      "stratigraphy": ["geox_sequence"],
      "deep_time": ["geox_deep_time_state"],
      "governance": ["geox_claim", "geox_claim_graph_evaluate", "geox_contradiction_scan", "geox_evidence", "geox_falsify"],
      "bridge": ["geox_to_wealth_bridge"],
      "inference": ["geox_lem_predict"],
      "meta": ["geox_surface_status"]
    }
  },
  "mcpApps": {
    "count": 9,
    "apps": [
      "ui://geox/well-desk",
      "ui://geox/prospect-ui",
      "ui://geox/seismic-vision-review",
      "ui://geox/geox-mcp-visual",
      "ui://geox/judge-console",
      "ui://geox/earth-volume",
      "ui://geox/attribute-audit",
      "ui://geox/georeference-map",
      "ui://geox/analog-digitizer"
    ],
    "manifestUrl": "https://geox.arif-fazil.com/apps.json"
  },
  "governance": {
    "framework": "arifOS F1-F13",
    "authority": "EVIDENCE_ONLY",
    "sovereign": "ARIF (F13)",
    "seal": "DITEMPA BUKAN DIBERI"
  },
  "seal": "DITEMPA BUKAN DIBERI"
}
```

## Key Design Decisions

1. **No `tools.list` array** — Registries should use MCP `tools/list` at runtime. The `categories` object is for human browsing.
2. **`publicCount` = 24** — Matches live `tools/list` output. 54 internal tools excluded.
3. **`ui: true` capability** — Signals MCP Apps support. Only ChatGPT + Claude Desktop honor this today.
4. **No installation instructions** — Remote SSE/Streamable HTTP means zero install. Just paste the URL.
5. **`seal` field** — Constitutional marker. Every arifOS organ carries it.

## What Was Missing Before (June 2026 version)

The old 241-byte server.json only had: `name`, `version`, `protocol_version`, `capabilities`, and `seal`. Missing:
- Tool count and categories
- MCP Apps listing
- Governance framework
- Federation details
- Repository link
- Tags/keywords for discovery
- Highlight/pitch
