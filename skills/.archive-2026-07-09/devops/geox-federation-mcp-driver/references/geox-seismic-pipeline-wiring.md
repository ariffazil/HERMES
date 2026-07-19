# GEOX Seismic Pipeline Wiring Pattern — Phase 3.1 (2026-07-06)

## Problem
Standalone seismic interpretation scripts (4,393 lines across 8 modules) needed to be wired as proper MCP tools in the GEOX server. Modules were independently written by OpenCode — each had different input/output formats.

## Solution Architecture

### Files Created
| File | Lines | Function |
|---|---|---|
| `src/geox_core/seismic_pipeline/__init__.py` | — | Package init |
| `src/geox_core/seismic_pipeline/geox_physical_reality.py` | 895 | Full RSI pipeline |
| `src/geox_core/seismic_pipeline/geox_geological_cognition.py` | 988 | Pixel→hypothesis |
| `src/geox_core/seismic_pipeline/geox_panel_d.py` | 501 | Cognitive panel |
| `src/geox_core/seismic_pipeline/geox_segy_trace_reality.py` | 880 | SEG-Y audit |
| `src/geox_core/seismic_pipeline/geox_well_tie_bruges.py` | 253 | Well-tie |
| `src/geox_core/seismic_pipeline/geox_3d_modeling_gempy.py` | 296 | 3D model |
| `src/geox_core/seismic_pipeline/geox_wealth_bridge.py` | 282 | Capital bridge |
| `src/geox_core/seismic_pipeline/geox_seismic_vision_ai.py` | 298 | Orchestrator |
| `src/geox_core/seismic_cognition.py` | — | 7-layer engine |

### MCP Wiring Steps (4 files must change)
1. **`src/geox_mcp/registry.py`** — Add to `SURFACE_TOOLS` list + `GEOX_TOOL_MANIFEST` + update counts
2. **`src/geox_mcp/server.py`** — Add `@mcp.tool()` wrapper + timeout + `_EXPECTED_CANONICAL` + version
3. **`src/geox_core/seismic_pipeline/`** — Implementation modules
4. **`geox/AGENTS.md`** — Update tool counts (drift-prone, see pitfall 14)

### Registry Pattern
```python
# In SURFACE_TOOLS list:
"geox_physical_reality_interpret",  # Phase 3.0: Full RSI pipeline

# In GEOX_TOOL_MANIFEST:
{
    "name": "geox_physical_reality_interpret",
    "domain": "earth.seismic",
    "axis": "reason",
    "lane": "reasoning",
    "expose": True,
    "face": "surface",
},
```

### Server Wrapper Pattern
```python
@mcp.tool(name="geox_physical_reality_interpret", annotations=_geox_annotations("geox_physical_reality_interpret"))
async def _geox_physical_reality_interpret(
    image_path: str,
    output_dir: str | None = None,
) -> dict[str, Any]:
    """Docstring becomes tool description."""
    try:
        from geox_mcp.federation_safety import classify_error
        from geox_core.seismic_pipeline.geox_physical_reality import GeoxPhysicalReality

        engine = GeoxPhysicalReality()
        result = engine.interpret(image_path, output_dir=output_dir)
        return {"status": "success", "tool": "geox_physical_reality_interpret", **result}
    except Exception as e:
        return classify_error(e, source_tool="geox_physical_reality_interpret", source_organ="geox")
```

### Timeout Pattern
```python
# In TOOL_TIMEOUTS dict:
"geox_physical_reality_interpret": 120.0,  # CPU-intensive
"geox_geological_cognition_run": 60.0,     # Hypothesis generation
"geox_panel_d_render_mcp": 60.0,           # Panel rendering
"geox_segy_trace_audit": 120.0,            # File I/O intensive
"geox_well_tie_compute": 60.0,             # bruges computation
"geox_3d_model_build": 120.0,              # GemPy model building
"geox_wealth_bridge_run": 60.0,            # Economic evaluation
```

## Critical Pitfall: Inter-Module Data Format Mismatch

When agents build pipeline modules independently, each module's input/output format won't match the next module's expectations. The physical reality engine returns a structured summary dict, but the geological cognition engine expects raw numpy arrays (agc, phase, coherence, etc.).

**Fix:** Store raw arrays as instance attributes on the engine:
```python
# In GeoxPhysicalReality.interpret():
self._last_attrs = attrs    # dict with 'agc', 'phase', 'coherence', etc.
self._last_fp = fp           # fault probability array
self._last_faults = faults   # fault polylines
self._last_horizons = horizons  # horizon picks
self._last_raw_arr = raw_arr    # cropped image array
self._last_crop_bbox = crop_bbox  # crop coordinates
```

Then in the MCP wrapper, access stored arrays:
```python
attrs = engine._last_attrs
fp = engine._last_fp
```

**Never assume** `phys.get("attributes")` contains raw arrays — it usually contains a summary dict.

## Verification Checklist
- [ ] `python3 -c "from geox_mcp.registry import CANONICAL_PUBLIC_TOOLS; print(len(CANONICAL_PUBLIC_TOOLS))"` matches `_EXPECTED_CANONICAL`
- [ ] `python3 -c "from geox_core.seismic_pipeline.geox_physical_reality import GeoxPhysicalReality"` imports clean
- [ ] `curl -sf http://localhost:8081/health` shows new version string
- [ ] `pytest tests/ -q` passes (no regressions)
- [ ] `systemctl restart geox-mcp` + re-probe confirms tools are live

## Seismic Cognition Doctrine (Deployed)

| Layer | Label | Can Do | Cannot Do |
|---|---|---|---|
| OBS_IMAGE | `OBS_IMAGE` | Pixels, contrast, geometry | Explain geology |
| CV_DETECTION | `DER_ATTRIBUTE` | Edges, coherence, phase, dip | Choose interpretation |
| LLM_COGNITION | `INT_SEISMIC` | Hypotheses with alternatives | Prove geology |
| GEN_MODEL | `DER_SYNTHETIC` | Imagine continuations | Judge geology |
| PHYSICS | `DER_ATTRIBUTE` | SEG-Y, wavelet, AVO | Interpret meaning |
| GEOLOGIST | `INT_GEOLOGY` | Judge plausibility | Govern |
| GOVERNANCE | `GOVERNANCE` | HOLD/advance/reject/seal | Observe |

**Constitutional rule:** "Code can detect evidence. Code cannot manufacture earth truth."
