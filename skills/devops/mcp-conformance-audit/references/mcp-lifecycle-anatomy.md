# MCP Initialize Capture — Real Response Anatomy

Captured from a live GEOX MCP server (FastMCP + Uvicorn, port 8081, HTTP transport).

## Step 0: Health check (optional but recommended)
```
GET /health → 200
{
  "status": "healthy",
  "version": "v2026.07.19",
  "build_identity": { "git_commit": "...", "registry_hash": "..." }
}
```

## Step 1: Initialize (JSON)
```
POST /mcp
Headers: Content-Type: application/json, Accept: application/json
Body: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}

→ 200 OK
Response headers:
  content-type: application/json
  mcp-session-id: ce3304b5051d463c8b7b3077a2e4092a    ← LOWERCASE
  x-earth-anchor: DITEMPA BUKAN DIBERI
  x-geox-version: v2026.07.19
  x-mcp-lifecycle: awaiting-initialized                   ← must send initialized notification next

Response body:
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",           ← verify this
    "serverInfo": {"name": "GEOX", "version": "v2026.07.19"},
    "capabilities": {
      "experimental": {},
      "logging": {},
      "prompts": {"listChanged": true},
      "resources": {"subscribe": false, "listChanged": true},
      "tools": {"listChanged": true},
      "tasks": {"list": {}, "cancel": {}, "requests": {"tools": {"call": {}}, "prompts": {"get": {}}, "resources": {"read": {}}}},
      "extensions": {"io.modelcontextprotocol/ui": {}}    ← MCP Apps support
    },
    "instructions": "..."
  }
}
```

## Step 2: notifications/initialized
```
POST /mcp
Headers: Content-Type: application/json, mcp-session-id: <from step 1>
Body: {"jsonrpc":"2.0","method":"notifications/initialized"}

→ 202 Accepted (empty body)
```

**Pitfall**: If session ID header is wrong case (e.g. `Mcp-Session-Id` instead of `mcp-session-id`), the server returns 400 "Missing session ID". Always use lowercase.

## Step 3: tools/list
```
POST /mcp
Headers: Content-Type: application/json, mcp-session-id: <same session>
Body: {"jsonrpc":"2.0","id":2,"method":"tools/list"}

→ 200, tools array. Check for _meta.ui.resourceUri on AppConfig-wired tools.
```

## Step 4: resources/list
```
POST /mcp
Headers: same session
Body: {"jsonrpc":"2.0","id":3,"method":"resources/list"}

→ 200, resources array. ui:// URIs should have mimeType: text/html;profile=mcp-app
```

## Step 5: prompts/list
```
POST /mcp
Headers: same session
Body: {"jsonrpc":"2.0","id":4,"method":"prompts/list"}

→ 200, prompts array.
```

## Step 6: tools/call (requires initialized notification first)

If `notifications/initialized` is NOT sent after `initialize`, `tools/call` returns:
```json
{
  "result": {
    "content": [{"type": "text", "text": "MCP_LIFECYCLE: tools/call rejected until client sends notifications/initialized..."}],
    "isError": true
  }
}
```
**Pitfall**: This looks like a successful call (HTTP 200, valid JSON-RPC) but `isError: true`. Always check `isError` before trusting `content[0].text`.

## SSE rejection
```
POST /mcp
Headers: Content-Type: application/json, Accept: text/event-stream
→ 406 Not Acceptable: "Client must accept application/json"
```
FastMCP streamable HTTP is JSON-only by default. SSE support requires explicit configuration.

## Key lessons
1. Session header is **lowercase** `mcp-session-id` in FastMCP
2. Initialize returns `x-mcp-lifecycle: awaiting-initialized` — must send `notifications/initialized` before any other call
3. `notifications/initialized` returns HTTP 202 with **empty body** — handle `json.loads("")` gracefully (catch JSONDecodeError or check raw body length before parsing)
4. Skipping `notifications/initialized` causes `isError: true` with lifecycle gate message — not a server error, a protocol sequencing error. The lifecycle is: `initialize → notifications/initialized → tools/call`
5. All subsequent calls reuse the same session ID
6. Content-Type response header may appear lowercase — normalize keys when parsing
