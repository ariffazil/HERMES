# FastMCP Server Patterns — Worked Example: KPJ MCP

Full worked example of building a data-driven FastMCP MCP server from scratch.
Reference for the patterns documented in §7 of the parent skill.

## Directory Layout

```
/opt/kpj-mcp/
├── kpj_server.py         # FastMCP server: 6 tools, lazy-loads data
├── start.sh              # exec python3 kpj_server.py
├── requirements.txt      # fastmcp>=3.0.0, uvicorn>=0.30.0
```

Data (could live inside `/opt/kpj-mcp/data/` or at a well-known path):
```
/var/www/html/well/kpj/data/hospitals.json
```

## FastMCP API Checklist

| Need | API |
|------|-----|
| Create server | `FastMCP(name, instructions=...)` |
| Register tool | `@mcp.tool()` decorator on a function |
| Tool params | Function type hints → auto JSON schema |
| Tool docstring | Becomes tool description in `tools/list` |
| Return JSON | Return dict/list — auto-serialized |
| Run HTTP | `mcp.run(transport="streamable-http", host="0.0.0.0", port=N)` |
| Run stdio | `mcp.run(transport="stdio")` |

## Tool Patterns Used in KPJ

### Pattern: Filter-and-return (kpj_search_hospitals)
Accept optional filters, iterate data, apply each filter if present, return filtered list.

### Pattern: Cross-reference with context (kpj_get_doctor)
Search doctors nested inside hospitals, attach hospital name to each result before returning.

### Pattern: Compute with breakdown (kpj_estimate_cost)
Look up a procedure's base cost, apply a regional factor (hospital-specific), optionally add consultation fee, return a detailed breakdown dict with `estimated_total_rm`.

### Pattern: Side-by-side compare (kpj_compare)
Accept a list of IDs, look up each, return a simplified projection for comparison. The list-of-dicts return naturally renders as a comparison table for the agent.

### Pattern: Rule-lookup with ternary outcome (kpj_visa_check)
Check nationality against two lists (required/exempt) and return three possible outcome shapes: `{"visa_required": false}`, `{"visa_required": true, "fee_rm": ..., "processing_days": ...}`, or `{"visa_required": "unknown"}`.

### Pattern: Discount calculator (kpj_savings_estimate)
Look up procedure cost, apply a discount tier (percentage), return breakdown with `base_cost_rm`, `discount_pct`, `discount_amount_rm`, `estimated_final_cost_rm`.

## Data File Structure

The JSON data is organized into domain-specific top-level keys — each tool reads only the section it needs:

```json
{
  "hospitals": [{ "id": "kpj-kl-01", "name": "KPJ Kuala Lumpur", ... }],
  "procedures": { "cardiac_bypass": {"base_cost_rm": 45000, ...} },
  "visa_info": { "medical_visa_required_countries": [...], ... },
  "savings_tiers": { "corporate": {"discount_pct": 20, ...} }
}
```

Each tool reloads the file on every call (`_load_data()`), making the data hot-reloadable without server restart.

## Transport & Testing

The KPJ server runs on `streamable-http` transport at port 18085 (18084 was taken by WELL WITNESS).
The endpoint is `http://localhost:18085/mcp`.

**Test via FastMCP Client (preferred):**
```python
from fastmcp.client import Client
async with Client("http://localhost:18085/mcp") as client:
    tools = await client.list_tools()
    result = await client.call_tool("kpj_search_hospitals", {"specialty": "cardiology"})
```

**Test via curl:**
```bash
curl -s -X POST http://localhost:18085/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## Pitfalls from This Build

- **Port conflicts:** Port 18084 was already occupied by the WELL WITNESS service. Always check with `ss -tlnp | grep <port>` before claiming a port is available. Step to the next port (18085) rather than fighting the existing binding.
- **Transport mismatch:** The default `"http"` transport requires SSE (`text/event-stream` Accept header) and rejects JSON-only POSTs with 406. For development and curl testing, use `"streamable-http"` instead. Only switch to `"http"` (SSE) when the target consumer requires it.
- **FastMCP 3.4.4 quirks:** `@mcp.resource()` accepts positional URI only (no kwargs). `@mcp.tool()` auto-derives schema from type hints — ensure proper type hints (not `Any`) for good agent-facing schema. Return types must be JSON-serializable (no custom objects).
