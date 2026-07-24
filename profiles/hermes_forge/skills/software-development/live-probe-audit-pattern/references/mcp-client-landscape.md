# MCP Client Landscape for Federation Organs

> Born from: MCP GUI platform deep research + GEOX integration audit (2026-07-19)
> Context: When connecting federation organs (GEOX, WEALTH, A-FORGE) to external MCP GUI clients
> Key insight: Most "top" clients are stdio-only; SSE/HTTP clients are fewer but growing

## Transport Reality

| Transport | GEOX uses? | Client support |
|-----------|-----------|----------------|
| **stdio** (local process spawn) | ❌ | Universal |
| **SSE** (Server-Sent Events) | ✅ (legacy, :8081) | 10+ clients |
| **Streamable HTTP** (2025-06-18) | ✅ (current, :8081/mcp) | Growing |

GEOX runs as an always-on HTTP server. Most "top" MCP clients (Claude Desktop, Cursor, Cline, Continue, Zed) are **stdio-first** — they expect to spawn a process, not connect to a running server.

## Top GUI Clients by SSE/HTTP Support

### Direct Connect (SSE/HTTP native — no proxy needed)

| # | Client | Stars | Type | Setup |
|---|--------|-------|------|-------|
| 1 | **5ire** | 5,282⭐ | Desktop (Win/Mac/Linux) | Settings → MCP → Add → URL: `http://host:8081/mcp` |
| 2 | **Cherry Studio** | 48,753⭐ | Desktop | Settings → MCP → Add → Transport: SSE |
| 3 | **ChatMCP** | 242⭐ | Desktop | Settings → Add MCP → HTTP/SSE |
| 4 | **EEChat** | ~500⭐ | Desktop | New Connection → Remote (SSE) |
| 5 | **AnythingLLM** | 63,546⭐ | Desktop/Docker | Agents → MCP → Remote Server URL |
| 6 | **LibreChat** | ~20k⭐ | Web self-hosted | `mcpServers: { geox: { transport: sse, url: "..." } }` |
| 7 | **Open WebUI** | 145,935⭐ | Web self-hosted | Admin → Pipelines → MCP → Add URL |
| 8 | **Chainlit** | 12,319⭐ | Web app builder | `ClientSession` to MCP SSE endpoint |
| 9 | **MCPHub Desktop** | 150⭐ | Desktop | Discover → Add Remote |
| 10 | **LobeChat** | 80,509⭐ | Web/Desktop | Plugins → MCP → Add Server URL |

### Stdio-Only (need proxy bridge)

| Client | Stars | Bridge needed |
|--------|-------|---------------|
| Claude Desktop | — | `mcp-stdio-proxy` or custom wrapper |
| Cursor | 33k⭐ | Stdio proxy |
| Windsurf | — | Stdio proxy |
| Cline (VS Code) | 64,797⭐ | Stdio proxy |
| Continue | 34,967⭐ | Stdio proxy |
| Zed | 87,224⭐ | Stdio proxy |
| GitHub Copilot | — | Stdio proxy |

## GEOX Connection Template

```
MCP endpoint: http://localhost:8081/mcp (local) or https://geox.arif-fazil.com/mcp (public)
Transport: Streamable HTTP (MCP protocol v2025-06-18)
Auth: Most tools require MCP session initialization
      Low-binding tools (geox_deep_time_state) work without full session
```

### Quick probe to verify connectivity

```bash
# 1. Health check
curl -s http://localhost:8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status'))"

# 2. MCP initialize handshake
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('result',{}).get('serverInfo',{}).get('name','NO_RESPONSE'))"
# Expected: "GEOX"
```

## Known Issues

### 1. Session gating on most tools
Most GEOX tools return `Missing session ID` or `SESSION_INVALID` without proper MCP session initialization. The Streamable HTTP transport requires an `initialize` → `tools/call` flow with session awareness. Low-binding tools (`geox_deep_time_state`, `geox_basin` with mode=profile/macrostrat) are the exceptions.

### 2. Claims sub-server disabled
FastMCP 3.4.2 rejects `**kwargs` in tool signatures. GEOX gracefully skips the claims sub-server (~15 tools). The main 24-tool surface is unaffected. See `references/geox-organ-probe-patterns.md` for full crash diagnosis.

### 3. Public endpoint routing
`https://geox.arif-fazil.com/mcp` routes through Caddy → Cloudflare tunnel → localhost:8081. Verify both paths:
```bash
curl -s https://geox.arif-fazil.com/health  # public
curl -s http://localhost:8081/health          # local
```

## Reference
- Full research artifact: `/root/forge_work/2026-07-19/GEOX_MCP_CLIENTS_RESEARCH.md`
- GEOX audit artifact: `/root/forge_work/2026-07-19/GEOX_VS_TRADITIONAL_AUDIT.md`
- GEOX probe patterns: `references/geox-organ-probe-patterns.md`
