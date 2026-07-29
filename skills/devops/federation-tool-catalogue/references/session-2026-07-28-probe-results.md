# Session Probe Results — 2026-07-28

Detailed probe commands and responses for building the inaugural federation tool catalogue.

## Endpoint Discovery

### arifOS Kernel (port 8088)

**MCP tools/list** — requires `Accept: application/json` header.

```bash
curl -s -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Result: 8 tools — `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`. Full input schemas returned.

### A-FORGE (port 7072)

**MCP tools/list** — open, no special headers needed.

```bash
curl -s -X POST http://127.0.0.1:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Result: 120 tools. Full input schemas returned. Also available in registry at `/root/A-FORGE/forge_work/2026-07-28/mcp-registry/aforge.json` (has `tools_count: 120`, `tools` array with `name`, `description`, `risk_tier`).

### GEOX (port 8081)

**MCP tools/list** — fails without session ID.
```
{"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Bad Request: Missing session ID"}}
```
(Also needs Accept header — returns "Not Acceptable" without it.)

**HTTP /tools** — works without auth.

```bash
curl -s http://127.0.0.1:8081/tools
```

Result: 33 tools with full descriptions. Includes `use_when` hints per tool.

**Health endpoint:**
```
GET http://127.0.0.1:8081/
{"service":"geox-unified","version":"v2026.07.24","domain_law":"NATURAL_LAW","authority":"REFLECT_ONLY","endpoints":{"health":"/health","tools":"/tools","mcp":"/mcp"}}
```

### WEALTH (port 18082)

**MCP tools/list** — requires `Mcp-Session-Id` header.
```
{"jsonrpc":"2.0","error":{"code":-32000,"message":"SESSION_MISSING: Mcp-Session-Id header required"}}
```

**HTTP /tools** — returns names only (no descriptions).

```bash
curl -s http://127.0.0.1:18082/tools
# Returns: [{"name":"wealth_institutional_stress_index"},{"name":"wealth_cascade_model"},...]
```

Result: 14 tools (names only). Descriptions must be sourced from MCP tool definitions or registry.

**Tools:**
- `wealth_institutional_stress_index`
- `wealth_cascade_model`
- `wealth_governance_capacity`
- `wealth_external_exploitation_detect`
- `wealth_bid_surface`
- `capital_primitive`
- `capital_health`
- `capital_diagnose`
- `capital_wisdom`
- `capital_market`
- `capital_ledger`
- `capital_registry`
- `capital_entropy`
- `wealth_judge_handoff`

### WELL (port 18083)

**MCP tools/list** — requires `Mcp-Session-Id` header (same as WEALTH).

**HTTP /tools** — full detail with danger level taxonomy.

```bash
curl -s http://127.0.0.1:18083/tools
```

Result: 8 tools with full descriptions, inputSchema, outputSchema, danger_level (L1-L3), fail_posture.

**Tool categories by danger level:**
- L1 (fail-open): `well_classify_substrate`, `well_trace_lineage`
- L2-L3: `well_assess_homeostasis`, `well_check_repair`, `well_validate_vitality`, `well_assess_reliability`, `well_guard_dignity`, `well_registry_status`

**Health endpoint:**
```
GET http://127.0.0.1:18083/
{"status":"degraded","role":"Body / Human Intelligence","authority":"REFLECT_ONLY"}
```

## Registry Files

All organs have registry data at:
```
/root/A-FORGE/forge_work/2026-07-28/mcp-registry/
```

| File | Tools | Fields |
|------|-------|--------|
| aforge.json | 120 | description, risk_tier, transport |
| arifos.json | 8 | description, risk_tier, transport |
| geox.json | 0 | Schema-only (no tools array populated) |
| wealth.json | 0 | Schema-only (no tools array populated) |
| well.json | 0 | Schema-only (no tools array populated) |

## Auth Scheme Summary

| Organ | MCP Auth | Accept Header | Session ID | HTTP /tools |
|-------|----------|--------------|------------|-------------|
| arifOS (8088) | None | Required | No | N/A |
| A-FORGE (7072) | None | No | No | N/A |
| GEOX (8081) | Session | Required | Required | Open (33 tools) |
| WEALTH (18082) | Session | No | Required | Open (14 names only) |
| WELL (18083) | Session | No | Required | Open (8 full detail) |

## SEAL

Session-specific probe results captured for reproducibility. Not a live diagnostic — actual organ state may differ on subsequent calls.
