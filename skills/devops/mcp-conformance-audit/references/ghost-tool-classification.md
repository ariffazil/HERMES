# Ghost Tool Classification Template

Compare live `tools/list` against canonical registry. Every tool in the registry but NOT live gets classified into one of these categories.

## Classification taxonomy

| Class | Meaning | Action |
|-------|---------|--------|
| `PUBLIC_CANONICAL` | Declared public, needs wiring | Wire with `@mcp.tool()` |
| `INTERNAL_CALLABLE` | Internal dispatch only | Keep hidden from tools/list |
| `COMPATIBILITY_ALIAS` | Mode alias for consolidated tool | Map via compat layer, don't expose |
| `CROSS_ORGAN_ROUTE` | Bridges to another organ (WEALTH, WELL) | Keep internal, route through federation |
| `DEAD_OR_DUPLICATE` | Genuinely defunct | Remove from manifest, add to GHOST_TOOLS |

## Key rules

1. **Do NOT blindly `@mcp.tool()` all phantom tools.** Classify first.
2. **Cross-organ tools** (`_bridge_run`, `_consequence`, `_to_wealth_*`) MUST remain internal. GEOX is evidence-only.
3. **Compat aliases** like `geox_well_tie` → `geox_seismic_compute mode=well_tie` should be handled via a compat layer, not registered as separate tools.
4. **Consolidated tools** (`geox_3d_model`, `geox_3d_model_build`) dispatch to the unified tool (`geox_subsurface_model`) — don't create separate surface entries.
5. **Live-but-missing-from-canonical** tools (registered in code but not in manifest) are DRIFT — update the manifest.

## Output format

```json
{
  "artifact": "P0.2 — Ghost/Recovered Tool Classification",
  "live_tool_count": 17,
  "registry_surface_tool_count": 24,
  "drift_tools": 8,
  "phantom_canonical_tools": [
    {
      "tool_name": "geox_basin_backstrip",
      "domain": "earth.basin",
      "classification": "PUBLIC_CANONICAL",
      "reason": "Declared as public in manifest; backstrip computation mode of geox_basin.",
      "action": "WIRE — dispatch to geox_basin with mode='backstrip'",
      "priority": "HIGH"
    }
  ],
  "internal_tools_of_interest": [
    {
      "tool_name": "geox_wealth_bridge_run",
      "classification": "CROSS_ORGAN_ROUTE",
      "reason": "Bridges to WEALTH organ. GEOX is evidence-only.",
      "action": "INTERNAL_CALLABLE only. Do NOT @mcp.tool()."
    }
  ]
}
```

## GEOX-specific notes

- `geox_wealth_bridge_run`, `geox_wealth_consequence`, `geox_to_wealth_bridge` → CROSS_ORGAN, do not expose
- `geox_well_tie`, `geox_well_tie_compute` → COMPATIBILITY_ALIAS for `geox_seismic_compute mode=well_tie`
- `geox_3d_model`, `geox_3d_model_build` → COMPATIBILITY_ALIAS, dispatch to `geox_subsurface_model`
- `geox_list_apps` was live but missing from canonical manifest → DRIFT to fix
