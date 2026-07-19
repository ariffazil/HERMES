# MCP Tool Discovery — Protocol Differences Across Organs

**Proven:** 2026-07-16 during federation tool surface audit.

## The Problem

Not all MCP servers respond to `tools/list` the same way. A naive JSON-RPC POST may return empty for servers that use SSE transport or expose tools through different endpoints.

## Discovery Methods (try in order)

### Method 1: Direct JSON-RPC POST (works for arifOS, A-FORGE, WEALTH, WELL)

```bash
curl -sf -X POST "http://127.0.0.1:<PORT>/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1,"params":{}}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); tools=d.get('result',{}).get('tools',[]); print(f'{len(tools)} tools'); [print(f'  {t[\"name\"]}') for t in tools]"
```

**Works for:** arifOS (:8088), A-FORGE (:7072), WEALTH (:18082), WELL (:18083)
**Fails for:** GEOX (:8081), MIND (:51001)

### Method 2: SSE Transport with Initialize (for SSE servers)

Some servers require a proper MCP session initialization before responding to tools/list:

```bash
# Step 1: Initialize
curl -sf -X POST "http://127.0.0.1:<PORT>/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":0,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}'

# Step 2: Then tools/list (may need session token from step 1)
```

**Works for:** MIND (:51001) — confirms server is alive even if tools/list doesn't return in plain HTTP

### Method 3: Organ-Specific Surface Status (for GEOX)

GEOX exposes a `geox_surface_status` tool that returns the full registry:

```
geox_surface_status(mode="registry")
```

Returns: canonical_callable (15 public), internal_tools (54), phantom_tools, registry truth verdict.

**Why GEOX is different:** GEOX uses FastMCP with a custom registry that separates public vs internal tools. The standard `tools/list` endpoint may not return all tools.

### Method 4: Health Endpoint (fallback — confirms liveness only)

```bash
curl -sf http://127.0.0.1:<PORT>/health | python3 -m json.tool
```

Confirms the server is alive but doesn't enumerate tools. Use when Methods 1-3 fail.

## Per-Organ Discovery Map

| Organ | Port | Method 1 (JSON-RPC) | Method 2 (SSE) | Method 3 (Custom) | Tool Count |
|---|---|---|---|---|---|
| arifOS | 8088 | ✅ works | — | — | 8 |
| A-FORGE | 7072 | ✅ works | — | — | 109 |
| GEOX | 8081 | ❌ empty | — | ✅ `geox_surface_status` | 15 public + 54 internal |
| WEALTH | 18082 | ✅ works | — | — | 12 |
| WELL | 18083 | ✅ works | — | — | 27 |
| MIND | 51001 | ❌ empty | ✅ confirms alive | — | 5 (from source code) |
| VAULT999 | 8100 | — | — | — | No MCP (REST API only) |
| AAA | 3001 | — | — | — | A2A protocol (not MCP) |
| OpenClaw | 18789 | — | — | — | Gateway (bridges to organs) |

## MIND Tools (from source — not discoverable via MCP probe)

MIND runs at :51001 with SSE transport. Tools defined in `/root/A-FORGE/services/sequential-thinking/server.py`:

- `mind_sequentialthinking` — structured, revisable, branchable reasoning
- `mind_recall_context` — recall past reasoning context
- `mind_list_sessions` — list active thinking sessions
- `mind_clear_session` — clear a thinking session
- `mind_health` — MIND organ health check

## Pitfall

**Don't declare a tool count from a single failed probe.** If Method 1 returns empty, try Methods 2-4 before concluding "0 tools." MIND was incorrectly reported as "0 tools" because the initial probe used plain HTTP POST without SSE initialization. The server has 5 tools — they're just not discoverable via the standard JSON-RPC path.
