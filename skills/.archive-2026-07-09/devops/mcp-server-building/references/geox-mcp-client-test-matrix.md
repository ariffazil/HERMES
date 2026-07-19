# GEOX MCP Client Compatibility Matrix

> **Tested:** 2026-07-19 | **GEOX:** v2026.07.17 | **Transport:** Streamable HTTP (protocol 2025-06-18)
> **Environment:** Ubuntu 25.10 headless VPS, Node.js v22.23.1, npx 10.9.8

## Live Test Results

### GEOX Server (127.0.0.1:8081)

| Check | Result | Detail |
|-------|--------|--------|
| Health endpoint | ✅ | `/health` returns `{"status":"healthy","version":"v2026.07.17"}` |
| MCP Initialize | ✅ | 200 OK, returns `mcp-session-id` in response header, 7 capability groups |
| tools/list | ✅ | 16 tools (runtime surface; health declares 24, registry targets 77) |
| tools/call (with session) | ✅ | `geox_deep_time_state(period="Miocene")` returns full Earth State Vector |
| tools/call (no session) | ❌ | `400 Bad Request: Missing session ID` |
| Public endpoint | ✅ | `https://geox.arif-fazil.com/mcp` reachable via Caddy + Cloudflare |

### MCP Protocol Detail

```bash
# Canonical curl test sequence
# 1. Init — capture session from response header
curl -sS -X POST http://127.0.0.1:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'

# 2. Extract session ID from mcp-session-id response header
# 3. Send initialized notification (also needs Accept header!)
curl -sS -X POST http://127.0.0.1:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 4. tools/list with session
curl -sS -X POST http://127.0.0.1:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

## GUI Client Installability (Headless VPS)

| Client | Type | Installable? | Headless Testable? | Notes |
|--------|------|-------------|-------------------|-------|
| **MCP Inspector** | Web dev tool | ✅ via npx | ❌ | CLI mode rejects HTTP transport. Web UI needs desktop browser + port 6277. |
| **MCP Studio** (PragmaLabs) | Native Linux binary | ✅ `npm install -g` | ⚠️ | Has `--headless` flag but requires `--tests-dir` with test definitions. Not ad-hoc GUI. |
| **5ire** | Electron desktop | ❌ | ❌ | Download page 404. No snap/apt/npm. macOS/Windows/Linux desktop needed. |
| **Cherry Studio** | Electron desktop | ❌ | ❌ | Redirects to cherryai.com.cn. No snap/apt/npm. Desktop-only. |
| **ChatMCP** | Desktop | ❌ | ❌ | Website unreachable. May be defunct. |
| **Goose CLI** (Block) | CLI agent | ⚠️ via npm | ✅ | Not a GUI but CLI-based MCP agent. Installable and usable headlessly. |
| **LibreChat** | Web self-hosted | ⚠️ Docker | ✅ | Docker-deployable. Web UI accessible via reverse proxy. |
| **Open WebUI** | Web self-hosted | ⚠️ Docker | ✅ | Docker-deployable. Web UI accessible via reverse proxy. |

## Key Findings

1. **No desktop GUI MCP client is testable on a headless VPS.** 5ire, Cherry Studio, Claude Desktop, and ChatMCP all require a display server (X11/Wayland) and desktop browser.

2. **MCP Inspector is the official debugging tool** but its web UI requires a browser. CLI mode only supports stdio transport, not HTTP. For HTTP-mode servers like GEOX, you need the web UI.

3. **MCP Studio (PragmaLabs) is the closest to headless** — it has a `--headless` mode and a native Linux x64 binary. But it expects pre-written test definitions (`--tests-dir`), not ad-hoc MCP exploration.

4. **Self-hosted web UIs (LibreChat, Open WebUI) are the practical path** for headless VPS MCP GUI testing. Both support MCP SSE/HTTP connections and can be accessed via Caddy reverse proxy.

5. **Protocol-level testing via curl is fully viable** — the MCP JSON-RPC protocol is simple enough that init → tools/list → tools/call can be tested entirely from the command line. This is what we validated in this session.

## Tool Count Discrepancy

GEOX shows different tool counts at different surfaces:
- **`/health`:** declares 24 public tools
- **`tools/list` (JSON-RPC):** returns 16 tools
- **Registry (`CANONICAL_PUBLIC_TOOLS`):** targets 77

This is **by design**, not a bug. The `tools/list` response is filtered by middleware and represents the runtime surface. The registry is the full catalog including internal/Phase-3 tools. The AGENTS.md explicitly states: "Tool count is a runtime fact — verify with tools/list."
