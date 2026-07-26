# MCP SSE Session Lifecycle — Canonical Recipe

> Born from: GEOX deployment audit (2026-07-19)
> Problem: `tools/list` and `resources/list` return 0 results or HTTP 400 without proper session
> Root cause: SSE transport requires 3-step handshake before any query method works

## The 3-Step Handshake

MCP over SSE (Server-Sent Events) requires this exact sequence:

```
1. POST initialize     → capture Mcp-Session-Id from response header
2. POST notifications/initialized → 202 Accepted (EMPTY body, not JSON!)
3. POST tools/list     → NOW returns actual tools
```

Skipping step 2 causes all subsequent calls to return:
- `HTTP 400 Bad Request` (GEOX, arifOS)
- `MCP_LIFECYCLE: tools/call rejected until client sends notifications/initialized`
- Empty `tools: []` even though tools exist

## Working Python Recipe

```python
import json, http.client as hc

HOST = "localhost"
PORT = 8081
H = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
sess = None

def mcp_call(method, params=None, id=None):
    """Make an MCP call, tracking session across calls."""
    global sess
    body_dict = {"jsonrpc": "2.0", "method": method, "params": params or {}}
    if id is not None:
        body_dict["id"] = id
    body = json.dumps(body_dict).encode()

    conn = hc.HTTPConnection(HOST, PORT, timeout=15)
    hdrs = dict(H)
    if sess:
        hdrs["Mcp-Session-Id"] = sess
    conn.request("POST", "/mcp", body=body, headers=hdrs)
    resp = conn.getresponse()

    # Capture session from initialize response
    if not sess:
        sid = resp.getheader("Mcp-Session-Id")
        if sid:
            sess = sid
            print(f"Session: {sess}")

    raw = resp.read()
    conn.close()

    # notifications/initialized returns 202 with EMPTY body
    if not raw:
        return {"_empty": True, "_status": resp.status}
    return json.loads(raw)

# 1. INITIALIZE — captures Mcp-Session-Id from header
init = mcp_call("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "probe", "version": "1.0"}
}, id=1)
print(f"Protocol: {init['result']['protocolVersion']}")

# 2. INITIALIZED NOTIFICATION — 202, empty body
notif = mcp_call("notifications/initialized", {})  # NO id field!
assert notif["_status"] == 202, f"Expected 202, got {notif['_status']}"

# 3. NOW queries work
tools = mcp_call("tools/list", {}, id=2)
print(f"Tools: {len(tools['result']['tools'])}")

resources = mcp_call("resources/list", {}, id=3)
print(f"Resources: {len(resources['result']['resources'])}")

# 4. TOOL CALL
result = mcp_call("tools/call", {
    "name": "geox_falsify",
    "arguments": {"claim_text": "Test claim", "mode": "full"}
}, id=4)
content = result["result"]["content"][0]["text"]
```

## Critical Pitfalls

### 1. `notifications/initialized` returns EMPTY body
NOT JSON. HTTP 202 with zero-length body. `json.loads("")` crashes. Always check for empty response and handle as `{"_empty": True, "_status": 202}`.

### 2. Missing `id` on notification
`notifications/initialized` is an MCP notification — it MUST NOT have an `id` field. Including `id` makes it a request, and the server may reject it or treat it differently.

### 3. Session header name is `Mcp-Session-Id` (with hyphens)
NOT `Mcp_Session_Id` or `mcp-session-id` (lowercase form appears in response headers but sending uppercase is safer).

### 4. `x-mcp-lifecycle: awaiting-initialized` header
After initialize, the response includes this header. It means the server is waiting for the `notifications/initialized` call. Tools/call before this notification will return `MCP_LIFECYCLE` error.

### 5. Session expires
GEOX sessions expire after inactivity. If you get `SESSION_INVALID`, re-initialize. Don't retry with the old session ID.

## Symptom → Diagnosis

| Symptom | Diagnosis |
|---|---|
| `tools/list` returns 0 tools | Session not initialized. Run full handshake. |
| HTTP 400 on tools/list | Missing `Mcp-Session-Id` header or step 2 skipped |
| `MCP_LIFECYCLE: awaiting-initialized` | Called tool before sending notifications/initialized |
| `SESSION_INVALID` | Session expired. Re-initialize. |
| `json.decoder.JSONDecodeError` on step 2 | Empty body from 202 — handle gracefully |
| `LANE_ENFORCEMENT · session_id required` | Tool requires governed session. Use arif_init first. |

## GEOX-Specific Notes

- GEOX uses `x-earth-anchor: DITEMPA BUKAN DIBERI` and `x-geox-version: v2026.07.17` headers
- After handshake: 16 tools and 32 resources (11 ui:// MCP Apps)
- `geox_list_apps` may return empty body in some modes — handle gracefully
- Claims sub-server (~15 tools) gracefully skipped due to FastMCP 3.4.2 **kwargs rejection
- WEALTH bridge (`geox_to_wealth_bridge`) is NOT in the 16 public tools
