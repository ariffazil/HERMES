# PROTOCOL_CONFORMANCE.md — HERMES (L3 DOMAIN)

```yaml
organ: HERMES
layer: L3 DOMAIN
role: Multi-Modal Bridge
internal_port: 8644
last_verified: 2026-07-19T17:30Z
```

## Protocol Status

| Protocol | Status | Notes |
|----------|--------|-------|
| **Telegram Bot API** | ✅ OPERATIONAL | Operator edge |
| **MCP** | N/A | Does not host MCP tools (bridge only) |
| **FastMCP** | N/A | Not applicable |
| **JSON-RPC 2.0** | N/A | Not applicable |
| **SSE** | N/A | Not applicable |
| **SEP-2127** | ⚠️ GAP | Missing `llms.txt` |
| **A2A** | ⚠️ GAP | No A2A agent card |
| **CloudEvents** | ⚠️ GAP | No event emission |

## Bridge Protocol

HERMES is a MULTI-MODAL BRIDGE — it routes external signals into the federation.
It does NOT host MCP tools or compute evidence.
Its protocol is the Telegram Bot API + internal routing to MCP organs.

## Routing Table

| Signal Type | Routes To | Protocol |
|-------------|-----------|----------|
| Seismic image | GEOX | MCP (geox_seismic_interpret) |
| Well log (LAS) | GEOX | MCP (geox_well_ingest) |
| Market alert | WEALTH | MCP (capital_market) |
| Fatigue check | WELL | MCP (well_assess_homeostasis) |
| PDF/Report | A-FORGE | MCP (forge_document_ingest) |

## Gaps to Close

1. **SEP-2127**: Create `llms.txt` for bridge discovery
2. **A2A**: Register A2A agent card as bridge agent
3. **CloudEvents**: Emit CloudEvents on signal routing
