# Streamable HTTP Lifecycle Gate & Vertical Slice Conformance

Discovered 2026-07-19 during GEOX MCP conformance testing on branch `forge/geox-mcp-apps-chatgpt-conformance`.

## Lifecycle Gate Discovery

**`tools/list` passes without `notifications/initialized`, but `tools/call` is rejected.**

When `McpLifecycleMiddleware` is active (GEOX Phase A1 lifecycle gate), the server enforces:
```
initialize → notifications/initialized → tools/call
```

- `tools/list` and `resources/list` work BEFORE the notification
- `tools/call` returns `MCP_LIFECYCLE: tools/call rejected until client sends notifications/initialized`
- `notifications/initialized` must be sent as a JSON-RPC **notification** (no `id` field) — returns 202 Accepted
- Sending `notifications/initialized` with an `id` field returns error -32602

Full lifecycle test pattern:

```python
# 1. Initialize
resp = _jsonrpc("initialize", {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "conformance-test", "version": "1.0.0"},
})
session_id = resp["session_id"]  # from mcp-session-id response header

# 2. Send initialized notification (no id field)
_jsonrpc_notify("notifications/initialized", {}, session_id)

# 3. Now tools/call works
resp = _jsonrpc("tools/call", {"name": "geox_surface_status", "arguments": {"mode": "health"}}, session_id=session_id)
```

## Vertical Slice Conformance Pattern

To prove ONE complete app slice from initialize through render:

```
GATE A: Tool in tools/list
  → GATE B: Tool has _meta.ui.resourceUri in tools/list entry
    → GATE C: Resource URI in resources/list
      → GATE D: resources/read returns valid HTML (>=100 chars, doctype or <html>)
        → GATE E: MIME type is text/html;profile=mcp-app (both list AND read)
        → GATE F: No tokens/API keys in HTML content
          → GATE G: tools/call on the tool succeeds
```

Each gate is an independent assertion. If any gate fails, the subsequent gates may still pass or fail independently — the test suite should report each gate separately, not skip on first failure.

Reference implementation: `tests/mcp_conformance/test_one_app_vertical_slice.py` in GEOX.

## Python urllib Test Client Pattern

For testing Streamable HTTP MCP servers without any MCP SDK dependency:

```python
import json, urllib.request, urllib.error

def _jsonrpc_full(method, params=None, id_val=1, session_id=None):
    """Send JSON-RPC, return body + session_id from headers."""
    body = {"jsonrpc": "2.0", "id": id_val, "method": method, "params": params or {}}
    req = urllib.request.Request(
        "http://localhost:8081/mcp/",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    if session_id:
        req.add_header("mcp-session-id", session_id)
    with urllib.request.urlopen(req, timeout=10) as resp:
        sid = resp.headers.get("mcp-session-id", "")
        result = json.loads(resp.read().decode("utf-8"))
        result["_session_id"] = sid
        return result

def _jsonrpc_notify(method, params, session_id):
    """Send JSON-RPC notification (no id)."""
    body = {"jsonrpc": "2.0", "method": method, "params": params}
    req = urllib.request.Request(
        "http://localhost:8081/mcp/",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "mcp-session-id": session_id,
        },
        method="POST",
    )
    urllib.request.urlopen(req, timeout=10)  # fire-and-forget
```

**Key detail:** The `Accept` header MUST be `application/json, text/event-stream`. FastMCP 3.x returns 406 without `application/json`. The `text/event-stream` is for SSE compatibility — Streamable HTTP servers accept it harmlessly.

## Server Dependency

These tests hit the live server. They require the server to be running. When the server crashes (e.g., due to import errors like xarray/packaging conflicts), all tests fail with `ConnectionRefusedError`. The systemd service auto-restarts, but tool registration may differ between instances. Always verify tool count with `tools/list` after a restart.

## Test File Structure

```
tests/mcp_conformance/
  __init__.py
  test_initialize_streamable_http.py   # 8 tests: lifecycle, accept header, session ID
  test_tool_visibility.py              # 8 tests: tools/list content, ghost tools, internal visibility
  test_resources_list.py               # 9 tests: resources/list, resources/read, URI resolution
  test_appconfig_links.py              # 8 tests: tool→resource URI linking, geox_list_apps
  test_one_app_vertical_slice.py       # 9 tests: full vertical slice proof
```

All test files share helpers via `from .test_tool_visibility import _jsonrpc_full, _jsonrpc_notify, _get_session`.
