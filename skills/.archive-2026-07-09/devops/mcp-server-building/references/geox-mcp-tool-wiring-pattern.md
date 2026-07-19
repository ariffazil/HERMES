# GEOX MCP Tool Wiring Pattern — Adding New Tools to an Existing FastMCP Server

## Overview
Pattern for wiring standalone Python modules as proper MCP tools in the GEOX server. Validated 2026-07-06 with 7 RSI pipeline tools.

## Files That Must Change (4-step pattern)

### 1. `src/geox_mcp/registry.py`
- Add to `SURFACE_TOOLS` list (with comment)
- Add to `GEOX_TOOL_MANIFEST` list (with domain/axis/lane/expose/face)
- Update count comments

### 2. `src/geox_mcp/server.py`
- Add `@mcp.tool()` wrapper function
- Add timeout in `TOOL_TIMEOUTS` dict
- Update `_EXPECTED_CANONICAL` constant
- Update `GEOX_VERSION` and `GEOX_CONTRACT_EPOCH`

### 3. `src/geox_core/<module>/` (or `src/geox_mcp/tools/`)
- Implementation code

### 4. Service restart
- `sudo systemctl restart geox-mcp`
- Verify with `curl -sf http://localhost:8081/health`

## Server Wrapper Template

```python
@mcp.tool(name="geox_new_tool", annotations=_geox_annotations("geox_new_tool"))
async def _geox_new_tool(
    required_param: str,
    optional_param: str | None = None,
) -> dict[str, Any]:
    """Tool description — becomes the MCP tool description.
    
    Args:
        required_param: Description
        optional_param: Description
    """
    try:
        from geox_mcp.federation_safety import classify_error
        from geox_core.new_module import implementation_func

        result = implementation_func(required_param, optional_param)
        return {
            "status": "success",
            "tool": "geox_new_tool",
            **result,
        }
    except Exception as e:
        return classify_error(e, source_tool="geox_new_tool", source_organ="geox")
```

## Key Pitfalls

1. **`classify_error` must be imported INSIDE the try block** — it's not available at module level
2. **`_EXPECTED_CANONICAL` must match `len(CANONICAL_PUBLIC_TOOLS)`** — server won't start if they disagree
3. **Timeouts must be added** — default timeout is 30s, most tools need 60-120s
4. **Data format mismatch** — if chaining modules, store raw arrays on instance attributes, not in return dict
5. **Agent-spawned scripts go to repo root** — explicitly forbid in prompt, or move them after

## Verification

```python
# Quick check
from geox_mcp.registry import CANONICAL_PUBLIC_TOOLS
print(f"Canonical: {len(CANONICAL_PUBLIC_TOOLS)}")

# Import check
from geox_core.new_module import implementation_func
print("Import OK")

# Server start check
from geox_mcp.server import compose_geox_servers
print("Server OK")

# Live check
# curl -sf http://localhost:8081/health | python3 -m json.tool
```
