# FastMCP HTTP Transport — Session & Header Requirements

> **Discovered:** 2026-07-11, arifOS federation GEOX P1 bug
> **Symptom:** Organ health green, `tools/list` returns 0
> **Root cause:** Registry crawler sends raw HTTP without session handshake

## The Problem

FastMCP's HTTP transport (StreamableHTTP) requires a stateful session for all requests after `initialize`. Code that sends raw JSON-RPC POSTs to `/mcp` without:

1. `Accept: application/json` header → HTTP 406 "Not Acceptable: Client must accept application/json"
2. Prior `initialize` call → `"Session not found"` error
3. `Mcp-Session-Id` header → session expired

...will get empty tool lists or errors, even though the organ is healthy.

## Proven Pattern: `geox_bridge.py` (arifOS kernel)

The arifOS kernel's `geox_bridge.py` at `/root/arifOS/arifosmcp/runtime/geox_bridge.py` is the reference implementation:

```python
# Session cache with TTL
_geox_session_id: str | None = None
_geox_session_established_at: float = 0.0
_GEOX_SESSION_TTL_SECONDS = 600

async def _ensure_session(client: httpx.AsyncClient) -> str | None:
    """Ensure valid GEOX MCP session. Returns session ID or None."""
    global _geox_session_id, _geox_session_established_at
    
    if _geox_session_id and (time.time() - _geox_session_established_at) < _GEOX_SESSION_TTL_SECONDS:
        return _geox_session_id
    
    resp = await client.post(
        f"{GEOX_BASE}/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "arifos-geox-bridge", "version": "1.0"},
        }},
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )
    if resp.status_code == 200:
        session_id = resp.headers.get("mcp-session-id")
        if session_id:
            _geox_session_id = session_id.strip()
            _geox_session_established_at = time.time()
            return _geox_session_id
    return None
```

Key details:
- **TTL:** 10 minutes (conservative; server may expire sooner)
- **Headers:** Always sends `Accept: application/json, text/event-stream`
- **Re-init on 400:** If response has "session" in error message, force re-init
- **Session ID from headers:** `mcp-session-id` response header, NOT from JSON body

## Broken Pattern: `federation_registry.py:_crawl_organ()`

The arifOS kernel's `federation_registry.py` at `/root/arifOS/arifosmcp/runtime/federation_registry.py` has a `_crawl_organ()` method that does raw HTTP without session management:

```python
# BROKEN: no Accept header, no session handshake
url = f"http://127.0.0.1:{port}/mcp"
payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
resp = await self._http.post(url, json=payload)  # FAILS silently
tools = data.get("result", {}).get("tools", [])  # always []
```

The fix: use `geox_bridge.list_geox_tools()` for GEOX, or add session management to the generic crawler.

## Diagnostic Script

```bash
#!/bin/bash
# probe_mcp_session.sh — Verify MCP session handshake works for a given organ URL
# Usage: bash probe_mcp_session.sh http://localhost:8081/mcp

URL="${1:-http://localhost:8081/mcp}"

echo "=== Step 1: Initialize ==="
HEADERS=$(curl -s -D - -o /dev/null -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}')

SESSION=$(echo "$HEADERS" | grep -i "mcp-session-id" | awk '{print $2}' | tr -d '\r')
echo "Session ID: ${SESSION:-NONE}"

if [ -z "$SESSION" ]; then
  echo "FAIL: No session ID returned"
  exit 1
fi

echo ""
echo "=== Step 2: tools/list ==="
RESULT=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}')

TOOL_COUNT=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('result',{}).get('tools',[])))" 2>/dev/null)
echo "Tools returned: ${TOOL_COUNT:-PARSE_ERROR}"

if [ "${TOOL_COUNT:-0}" -gt 0 ]; then
  echo "SUCCESS: $TOOL_COUNT tools discovered"
else
  echo "FAIL: 0 tools returned (check session + headers)"
fi
```

## Key Takeaways

1. **FastMCP HTTP is stateful** — always `initialize` before `tools/list`
2. **`Accept: application/json` is mandatory** — FastMCP rejects without it
3. **Session ID comes from response headers** — `mcp-session-id` header, not JSON body
4. **Use bridge modules** — `geox_bridge.py`, `federation_bridge.py` handle sessions; raw HTTP doesn't
5. **Health endpoint ≠ tool discovery** — `/health` works without sessions; `/mcp` doesn't
