# MCP Transport Debugging Patterns

> Forged 2026-07-11 from GEOX P1-P3 investigation session.
> Load when: `tools/list` returns unexpected count, federation health reports session issues, or MCP calls fail with "session_unavailable".

## Pattern 1: `stateless_http=True` Kills Session IDs

**Root cause:** FastMCP `stateless_http=True` (used by arifOS) means the server never returns `mcp-session-id` header on initialize. Each request is independent — no session tracking.

**Symptom:** Federation health reports `"arifOS did not return mcp-session-id"` and `federation_geometry: null`.

**How to detect:**
```bash
# Check if server returns mcp-session-id
curl -D- -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' 2>&1 | grep -i "mcp-session-id"

# Check server config
grep -rn "stateless_http" /opt/arifos/app/arifosmcp/ 2>/dev/null | grep -v __pycache__
```

**Fix pattern:** Don't require session IDs from stateless servers. Generate a local session ID for correlation and proceed with tool calls:

```python
# WRONG — blocks on session availability
sid = resp.headers.get("mcp-session-id")
if not sid:
    return {"error": "session_unavailable"}  # ← This is the bug

# RIGHT — proceed without server session
sid = resp.headers.get("mcp-session-id") or f"local-{uuid.uuid4().hex[:16]}"
# Tool calls work without session header on stateless servers
```

**Why not change server to stateful:** arifOS intentionally runs `stateless_http=True` (PHOENIX-73C). Changing to stateful has implications for all MCP clients. Fix the client, not the server.

**Multiple code paths:** Check ALL places that call the stateless server. In GEOX, both `federation_memory.py` (`_ensure_session()`) AND `server.py` (health check federation geometry) had the same assumption. Both needed fixing.

## Pattern 2: Middleware Filtering `tools/list`

**Root cause:** `GeoxGovernanceMiddleware.on_list_tools()` filters the tool list to only `CANONICAL_PUBLIC_TOOLS`. Domain server tools (from `mcp.mount()`) are registered but hidden from discovery.

**Symptom:** `mcp.list_tools()` returns 40 tools (in-process), but HTTP `tools/list` returns only 17.

**How to detect:**
```bash
# Check what HTTP clients see
INIT=$(curl -s -D/dev/stderr -X POST http://localhost:8081/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' 2>&1)
SESSION=$(echo "$INIT" | grep -i "mcp-session-id" | awk '{print $2}' | tr -d '\r')
curl -sf -X POST http://localhost:8081/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('result',{}).get('tools',[])))"

# Check what the server thinks it has
grep "CANONICAL_PUBLIC_TOOLS" /root/geox/src/geox_mcp/registry.py
grep "_PUBLIC_SURFACE" /root/geox/src/geox_mcp/geox_middleware.py
```

**This is usually BY DESIGN, not a bug.** The middleware intentionally limits the discovery surface. Domain server tools (witness, paleoscan, claims, vision) are internal — callable but not discoverable.

**Three-layer truth:**
1. `CANONICAL_PUBLIC_TOOLS` (17) — what MCP clients discover
2. `CANONICAL_RUNTIME_TOOLS` (78) — what the server can execute
3. `mcp.list_tools()` (40) — in-process view (includes mounted servers)

## Pattern 3: Dead Tool References in Health Checks

**Root cause:** Health check code references tools that were renamed or removed from the server.

**Symptom:** Health check returns `"arifOS responded but no geometry telemetry found"` — the tool call succeeds but returns `KERNEL_DENY: Capability not registered in graph`.

**How to detect:**
```bash
# Test the tool directly
curl -sf -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"<tool_name>","arguments":{...}}}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('content',[{}])[0].get('text','')[:200])"
```

**Fix:** Health checks should gracefully degrade when tools don't exist. Report the failure in the health note, don't crash.

## Cross-Reference

- arifOS PHOENIX-73C: stateless_http design decision (server.py:1773)
- GEOX GeoxGovernanceMiddleware: on_list_tools filtering (geox_middleware.py:230)
- GEOX federation_memory.py: session ID requirement (federation_memory.py:31)
- GEOX server.py health check: federation geometry probe (server.py:2200)
