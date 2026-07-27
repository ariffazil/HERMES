# arifos://tools/registry — Build Reference

> Forged: 2026-07-26
> Origin: Furi gap analysis → native kernel resource decision
> Session: Hermes + Arif

## Decision Chain

1. **Furi evaluated** — CLI for MCP server management (GitHub install, PM2, SSE aggregator)
2. **Gap analysis** (what Furi solves vs what we have):
   - Package mgmt? → We have zero external MCP servers. 6 native organs.
   - SSE aggregation? → Already have Caddy reverse proxy to /mcp/ endpoints.
   - Unified discovery? → **Real gap.** No single place to ask "what tools exist?"
3. **Decision:** Skip Furi (BSL license, PM2 overlap, marginal value). Build native.
4. **Built:** `arifos://tools/registry` as kernel MCP resource — 200 lines, zero deps, zero new services.

## Resource Probe Architecture

```
async def _build_registry():
    ┌─────────────────────┐     ┌──────────────────────┐
    │ arifOS    :8088     │────▶│ MCP tools/list → 8   │
    │ A-FORGE   :7072     │────▶│ MCP tools/list → 120 │
    │ GEOX      :8081     │─┬──▶│ MCP → 0 (session)    │
    │ WEALTH    :18082    │─┤   │ health → 33 tools     │
    │ WELL      :18083    │─┤   │ MCP → 0 (session)    │
    │                     │ │   │ health → 12 tools     │
    │                     │ │   │ MCP → 0 (session)    │
    │                     │ │   │ health → 8 tools      │
    │ arifFLOW  :7073     │─┘   │ data service, no MCP  │
    └─────────────────────┘     └──────────────────────┘
          └── asyncio.gather + 5s timeout per organ
```

## Verification Transcript

```
curl -X POST .../mcp -d '{"method":"resources/read","params":{"uri":"arifos://tools/registry"}}'

Summary:   6/6 sihat, 128 MCP tools
  arifOS    :8088  🟢  tools: MCP=8
  A-FORGE   :7072  🟢  tools: MCP=120
  GEOX      :8081  🟢  tools: MCP=0 health=33  (session-gated)
  WEALTH    :18082 🟢  tools: MCP=0 health=12  (session-gated)
  WELL      :18083 🟢  tools: MCP=0 health=8   (session-gated)
  arifFLOW  :7073  🟢  tools: MCP=0           (data service)
Tools: 128 entries
```

## Pitfalls Hit

| Issue | Fix |
|-------|-----|
| `PermissionError` on new .py file | `chmod 644 + chown ariffazil:arifos` |
| `Extended resource registration failed: URI template must contain at least one parameter` | Removed `name=`/`description=` kwargs from `@mcp.resource()` — FastMCP 3.4.4 only accepts positional URI string |
| `restart counter too quick` | `systemctl reset-failed arifos` before restart |
| Session-gated organs return 0 tools | Fall back to health endpoint `tools_loaded` field |

## Files

- `/root/arifOS/arifosmcp/resources/tools_registry.py` — main resource file
- `/root/arifOS/arifosmcp/resources/__init__.py` — import + provenance + registration
