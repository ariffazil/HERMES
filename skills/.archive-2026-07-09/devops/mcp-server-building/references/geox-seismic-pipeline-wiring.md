# GEOX Seismic Pipeline Wiring — Reference

> Forged 2026-07-06. Wiring standalone seismic cognition scripts into GEOX MCP server.

## Context

Arif's GEOX seismic cognition pipeline was built as 8 standalone Python scripts (~4,400 lines) by OpenCode. The scripts lived in repo root, not wired into the GEOX MCP surface. This reference captures the integration pattern.

## Architecture

```
src/geox_core/seismic_pipeline/   ← pipeline modules (implementations)
src/geox_mcp/tools/seismic_rsi.py ← RSI tool (earlier integration)
src/geox_mcp/server.py            ← MCP tool wrappers (@mcp.tool decorators)
src/geox_mcp/registry.py          ← canonical tool list + manifest
```

**Key insight:** Pipeline modules go in `src/geox_core/seismic_pipeline/`, NOT in `src/geox_mcp/tools/`. The tools directory holds thin wrappers; the core directory holds real implementations.

## Wiring Steps

### 1. Move scripts to package location
```python
# Copy (not move — preserve originals until verified)
src_dir = "/root/GEOX"  # repo root
dst_dir = "/root/GEOX/src/geox_core/seismic_pipeline"
os.makedirs(dst_dir, exist_ok=True)
# Copy each .py file, create __init__.py
```

### 2. Fix inter-module data flow
When pipeline modules need to chain data (module A → module B), store raw arrays as instance attributes:
```python
class GeoxPhysicalReality:
    def interpret(self, image_path, ...):
        # ... compute attrs, fp, faults, horizons ...
        # Store for downstream use
        self._last_attrs = attrs    # raw numpy arrays
        self._last_fp = fp
        self._last_faults = faults
        self._last_horizons = horizons
        self._last_raw_arr = raw_arr
        self._last_crop_bbox = crop_bbox
        return report  # summary dict (JSON-safe, no raw arrays)
```

Then in MCP wrapper:
```python
engine = GeoxPhysicalReality()
phys = engine.interpret(image_path)
# Access stored raw arrays for downstream cognition
attrs = engine._last_attrs
fp = engine._last_fp
cogn = run_geological_cognition(attrs, fp, horizons, faults, output_dir)
```

**Pitfall:** Don't expect raw numpy arrays in the JSON return dict — they get serialized to lists and lose shape/dtype. Store on instance, access directly.

### 3. Register in registry.py
Add to `SURFACE_TOOLS` list + `GEOX_TOOL_MANIFEST` list. Update count comments.

### 4. Wire in server.py
```python
@mcp.tool(name="geox_physical_reality_interpret", annotations=_geox_annotations("..."))
async def _geox_physical_reality_interpret(image_path: str, ...) -> dict:
    try:
        from geox_mcp.federation_safety import classify_error  # MUST import
        from geox_core.seismic_pipeline.geox_physical_reality import GeoxPhysicalReality
        engine = GeoxPhysicalReality()
        result = engine.interpret(image_path, ...)
        return {"status": "success", "tool": "...", **result}
    except Exception as e:
        return classify_error(e, source_tool="...", source_organ="geox")
```

**Pitfall:** Every wrapper MUST import `classify_error` from `geox_mcp.federation_safety` inside the try block. Forgetting this causes `NameError` at runtime.

### 5. Add timeouts
```python
TOOL_TIMEOUTS = {
    "geox_physical_reality_interpret": 120.0,  # CPU-intensive
    "geox_panel_d_render_mcp": 60.0,           # rendering
    ...
}
```

### 6. Update _EXPECTED_CANONICAL
```python
_EXPECTED_CANONICAL = (
    56  # Phase 3.1: +7 seismic pipeline tools
)
```

### 7. Restart + verify
```bash
sudo systemctl restart geox-mcp
curl -sf http://localhost:8081/health | python3 -m json.tool
# Verify canonical_tools count matches _EXPECTED_CANONICAL
```

## Epistemic Grammar (GEOX-specific)

Every seismic output MUST carry epistemic labels:
- `OBS_IMAGE_PIXEL` — directly observed pixel values
- `DER_IMAGE_CONTRAST` — derived from pixel arithmetic
- `INT_SEISMIC_HORIZON` — interpreted (needs alternatives)
- `INT_SEISMIC_FAULT` — interpreted (needs alternatives)
- `HOLD` — claims not supportable from image alone

**Hard law:** OBS_IMAGE ≠ OBS_GEOLOGY. Pixels are observed. Geology requires calibration.

## Libraries Used
- `segyio` — SEG-Y I/O
- `bruges` — rock physics, AVO, synthetic seismograms
- `gempy` — 3D implicit geological modeling
- `scipy` — Hilbert transform, signal processing
- `numpy`, `PIL`, `matplotlib` — core array/image/plotting
