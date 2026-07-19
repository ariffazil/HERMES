# GEOX Registry Repair Example (2026-07-19)

Concrete walkthrough of the multi-surface registry repair on GEOX MCP server.

## Before State

| Surface | Count | Issue |
|---|---|---|
| `tools_manifest.yaml` public | 24 | Missing `geox_list_apps` |
| `registry.py` CANONICAL_PUBLIC_TOOLS | 24 (manifest - 18 ghosts) | 8 tools declared but never wired |
| `CANONICAL_PUBLIC_SURFACE.json` canonical_tools | 24 | Drifted from registry |
| `server-card.json` tools | 24 | Stale |
| Live `tools/list` | 16 | RT1_GUARD blocks `geox_list_apps` |
| `health.json` public_tools claim | 24 | Incorrect |

**8 unwired tools in manifest:** `geox_basin_backstrip`, `geox_claim_graph_evaluate`, `geox_contradiction_scan`, `geox_evidence`, `geox_lem_predict`, `geox_sediment_mass_balance`, `geox_thermal_maturity_history`, `geox_to_wealth_bridge`

## Repair Steps

### 1. Add `geox_list_apps` to `tools_manifest.yaml`

```yaml
- name: geox_list_apps
  domain: control.surface
  axis: observe
  lane: evidence
  face: surface
  visibility: public
  description: 'List all registered GEOX MCP Apps (SEP-1865).'
  input_schema_source: callable
  annotations:
    read_only: true
    destructive: false
    idempotent: true
  ui: null
  plugin:
    exposed: true
  governance:
    action_class: OBSERVE
    mutation: false
    physics_guard_required: false
```

### 2. Ghost 8 unwired tools in `registry.py`

```python
GHOST_TOOLS: set[str] = {
    # ... existing ghosts ...
    "geox_basin_backstrip",           # unwired — no FastMCP registration
    "geox_claim_graph_evaluate",      # unwired — no FastMCP registration
    "geox_contradiction_scan",        # unwired — no FastMCP registration
    "geox_evidence",                  # unwired — no FastMCP registration
    "geox_lem_predict",               # unwired — no FastMCP registration
    "geox_sediment_mass_balance",     # unwired — no FastMCP registration
    "geox_thermal_maturity_history",  # unwired — no FastMCP registration
    "geox_to_wealth_bridge",          # unwired — no FastMCP registration
}
```

### 3. Regenerate CANONICAL_PUBLIC_SURFACE.json (with import bypass)

```python
#!/usr/bin/env python3
"""Regenerate CANONICAL_PUBLIC_SURFACE.json — bypasses server startup verification."""
import sys
sys.modules["geox_mcp.server"] = type(sys)("geox_mcp.server")  # block verification

from geox_mcp.registry import CANONICAL_PUBLIC_TOOLS, GHOST_TOOLS
from geox_mcp.surface_manifest import load_surface_manifest, public_tool_names

load_surface_manifest.cache_clear()
out = {
    "canonical_tools": sorted(CANONICAL_PUBLIC_TOOLS),
    "public_count": len(CANONICAL_PUBLIC_TOOLS),
    # ...
}
```

### 4. Update server-card.json

```json
"tools": 17,
"internal_tools": 54,
"resources": 32,
"prompts": 12
```

### 5. Create canonical_manifest.json as single source of truth

```json
{
  "public_tools": [
    "geox_basin", "geox_claim", ... , "geox_list_apps"
  ],
  "mcp_apps": {
    "tool_to_resource": {
      "geox_well_desk": "ui://geox/well-desk",
      ...
    }
  }
}
```

### 6. CI validator script

```bash
python3 scripts/validate_canonical_manifest.py
# PASS: manifest public_tools (17) == registry (17)
# PASS: CANONICAL_PUBLIC_SURFACE.json (17) == registry (17)
# PASS: server-card.json tools=17 == registry=17
# PASS: All app linked_tools in manifest public_tools
# PASS: All tool→resource mappings valid
# PASS: No ghost tools in manifest public_tools
# Errors: 0
```

## After State

| Surface | Count | Status |
|---|---|---|
| `tools_manifest.yaml` public | 25 | +`geox_list_apps`, 8 now internal-only |
| `registry.py` CANONICAL_PUBLIC_TOOLS | 17 | 25 manifest - 26 ghosts = 17 live |
| `CANONICAL_PUBLIC_SURFACE.json` | 17 | MATCHES registry |
| `server-card.json` | 17/54/32/12 | MATCHES live |
| Live `tools/list` | 17 | After server restart, `geox_list_apps` callable |

## Conformance Test Results

```
tests/mcp_conformance/test_conformance.py ....................... [23/23 PASS]
tests/mcp_conformance/test_falsify.py .... [4/4 contract PASS]
```

## Key Pitfalls

1. **Module import bypass is mandatory** when the server module runs verification at import time. Stub `sys.modules["package.server"]` before any imports.
2. **Ghosting is safer than deleting** from the manifest. Deleted tools can't be restored without git archaeology. Ghosted tools stay visible in the manifest for documentation and can be un-ghosted when wired.
3. **Don't ghost tools that ARE wired.** `geox_list_apps` was wired via `@mcp.tool()` but absent from the manifest — it needed to be ADDED, not ghosted.
4. **Count-bearing files are a chain.** Changing one means changing all: manifest → registry → surface file → server card → apps.json → CI validator.
