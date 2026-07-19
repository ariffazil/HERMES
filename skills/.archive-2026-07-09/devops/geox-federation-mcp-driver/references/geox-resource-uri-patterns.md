# GEOX Resource URI Patterns — Complete Catalog

Discovered by probing `client.list_resources()` and `resources/templates/list` on 2026-07-03. URI templates that work vs. don't work, with verified return shapes.

## Verified Working URIs (as of GEOX v2026.07.01-phase2.3-earthmap)

### Ontology / Playbooks / Schemas
```
geox://resources/ontology/<name>.yaml
geox://resources/playbooks/<name>.yaml
geox://resources/schemas/<name>.json
geox://resources/examples/<name>.<ext>
```

Verified examples:
- `geox://resources/ontology/sabah_basin_strat.yaml` → 24,117 chars
- `geox://resources/ontology/biostrat_reference_stack.yaml`
- `geox://resources/playbooks/prospect_evaluation.yaml`
- `geox://resources/playbooks/seismic_well_tie.yaml`

### Layer Packages (Earth Layer Registry v1)
```
geox://layers/<layer_id>/package
```

Verified:
- `geox://layers/sabah.basin_outline.v3/package` → full envelope, INTERPRETATION class
- Format: `GEOX-LAYER-PKG-v1`, includes governance gates F1/F2/F6/F11

Common pitfalls:
- Wrong layer_id format → `{"error": "layer_not_found: <x>", "hint": "fetch geox://layers/index for available layer_ids"}`
- Hint resource `geox://layers/index` exists but `EarthLayer` schema has bug — `AttributeError: 'EarthLayer' object has no attribute 'title'` on raw curl. Try Python client.

### Identity / Capabilities / Status
```
geox://identity
geox://capabilities
geox://surface/truth
geox://layers/index           # ⚠️  EarthLayer schema bug — see above
geox://resources/index        # ✅ returns categories list
geox://resources/prompts/index  # ✅ prompt file list
geox://resources/playbooks/index
geox://resources/ontology/index
geox://resources/schemas/index
geox://registry/apps          # list of MCP apps
geox://profile/status
geox://reality/context
tree777://index               # TREE777 root
```

### Literature (sparse — only 1 seeded paper)
```
geox://literature/index
geox://literature/GSM-MADON-2021-MALAY-BASIN
```

⚠️ Only the GSM-MADON-2021 paper is currently seeded. Other literature URIs (e.g. `geox://literature/KREBS-2011-CHRONOSEQ`) are placeholders referenced by evidence attachments but return 404.

### Claims Graph
```
geox://claims/index
geox://claims/graph           # knowledge graph with nodes + edges
```

Returns JSON arrays of claim metadata + graph structure with claim/evidence node types.

### Basins
```
geox://basins/index           # list of basin names + URIs
geox://basins/malay-basin/profile   # ✅ works
geox://basins/sabah-basin/profile   # ⚠️ REGISTERED in index but read_resource returns "Unknown resource"
```

The basin index advertises Sabah but the profile resource is not yet exposed. Workaround: query Sabah data via `geox_basin` tool with `basin_name="Sabah"` (also returns "Basin data not found" — the basin is referenced but data not seeded). Use `geox_deep_time_state` or `geox_atlas` for Sabah-specific queries.

### TREE777 Wiki
```
tree777://index
tree777://skills/geox/<name>          # GEOX skill pages
tree777://geo/concepts/<name>         # GEOX concepts
tree777://geo/scars/<name>            # GEOX scar/incident records
```

Currently only `skill-spatial-grounding` and ~20 concept pages are seeded. Kinabalu-specific entries (e.g. `tree777://geo/concepts/Kinabalu`) return 404 — would need to be added via the TREE777 ingestion pipeline.

## URIs That Return "Resource Not Found"

Common mistakes — DO NOT use:
```
geox://basins/sabah-basin/profile         # indexed but not exposed
geox://ontology/sabah_basin_strat.yaml    # missing /resources/ prefix
geox://layers/kinabalu.velocity/package   # not seeded (only sabah.basin_outline.v3 is)
geox://literature/KREBS-2011-CHRONOSEQ   # placeholder, not seeded
tree777://geo/concepts/Kinabalu           # not seeded
```

## Patterns for Discovery

If you don't know the right URI:

```python
# 1. List all registered resources
resources = await client.list_resources()
for r in resources:
    print(f"{r.name}: {r.uri}")

# 2. List URI templates (for parameterized resources)
templates = await client.list_resource_templates()
for t in templates:
    print(f"{t.name}: {t.uriTemplate}")
    print(f"  {t.description}")
```

Or via raw JSON-RPC:
```bash
curl ... -d '{"jsonrpc":"2.0","id":X,"method":"resources/list","params":{}}'
curl ... -d '{"jsonrpc":"2.0","id":X,"method":"resources/templates/list","params":{}}'
```

## Pre-Seeded Layer IDs (from templates/list description)

The seed description in `geox_layer_package` template mentions: "Seeds include Sabah basin_outline, faults, plates, **Kinabalu velocity**."

But `geox://layers/kinabalu.velocity/package` returns `layer_not_found`. Either:
- The seed description is forward-looking (not yet loaded)
- The actual layer_id differs from the human-readable name

Workaround: parse `geox://layers/index` via Python client to avoid the `EarthLayer.title` schema bug.

## Cross-References

- `/root/AAA/docs/MCP-RESOURCES-MAP.md` — canonical resource URI catalog (may be more current)
- `/root/AAA/docs/TOOLREGISTRY.json` — capability-tag-based tool discovery
- `/root/AAA/agents/AAA_ZEN_INIT.md` — agent onboarding (resources zen placement)