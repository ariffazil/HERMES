# FastMCP Session-Validation Middleware Pattern

**Forged 2026-07-18** from GEOX/WELL/WEALTH multi-organ session enforcement work.

## Pattern

Add a `Middleware` subclass to any FastMCP server that intercepts `on_call_tool` and validates session presence/quality before the tool executes. This is a **defense-in-depth** layer — tools may also validate session_id individually, but the middleware ensures no anonymous call slips through.

## Three-Way Error Taxonomy

Session validation errors MUST be differentiated by HTTP status:

| Status | Meaning | Error Codes | Logging Level |
|--------|---------|-------------|---------------|
| **400** | No token provided (client error, routine) | `SESSION_MISSING`, `ACTOR_MISSING` | WARNING |
| **401** | Token present but invalid/forged (security event) | `SESSION_INVALID`, `SCT_INVALID`, `ACTOR_MISMATCH`, `TRANSPORT_DEGRADED` | WARNING |
| **403** | Valid token, insufficient authority (policy event) | `INSUFFICIENT_AUTHORITY` | WARNING |

**Why this matters:** Security teams route on HTTP status. If "no token" and "forged token" both return 400, the forged-token events drown in routine noise. Differentiating lets SIEM/SOC tools triage correctly.

## Implementation Template

```python
import json
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware


class SessionValidationMiddleware(Middleware):
    """Reject tool calls that lack a session_id."""

    # Tools exempt from session validation (health checks, diagnostics)
    _EXEMPT_TOOLS: frozenset[str] = frozenset({"health_check"})

    async def on_call_tool(self, context, call_next):
        tool_name = getattr(context.message, "name", "")
        raw_arguments = getattr(context.message, "arguments", {}) or {}

        # Defensive parse: some MCP transports serialize args as JSON string
        if isinstance(raw_arguments, str):
            try:
                arguments = json.loads(raw_arguments)
            except (json.JSONDecodeError, TypeError):
                arguments = {}
        else:
            arguments = raw_arguments

        # Check session_id (skip exempt tools)
        if tool_name not in self._EXEMPT_TOOLS:
            session_id = (arguments.get("session_id")
                          if isinstance(arguments, dict) else None)
            if not session_id or (isinstance(session_id, str)
                                  and not session_id.strip()):
                raise ToolError(
                    f"SESSION_MISSING: tool '{tool_name}' requires a session_id. "
                    f"Provide a valid session token. http_status=400"
                )

        # Strip session_id from arguments before tool dispatch
        # (tools don't declare it; it's middleware-only metadata)
        if isinstance(arguments, dict) and "session_id" in arguments:
            cleaned = {k: v for k, v in arguments.items() if k != "session_id"}
            context.message.arguments = cleaned

        return await call_next(context)


# Register after FastMCP init
try:
    mcp.add_middleware(SessionValidationMiddleware())
except Exception:
    logger.warning("SessionValidationMiddleware failed to load")
```

## Integration with HTTP Middleware

For dual-layer defense (HTTP + FastMCP), also check session tokens at the ASGI/Starlette layer. This catches requests before they reach FastMCP at all:

```python
class OriginAndSessionMiddleware:
    """Validate Origin header AND session token on MCP endpoints."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("path", "").startswith("/mcp"):
            headers = dict(scope.get("headers", []))
            method = scope.get("method", "GET").upper()

            if method == "POST":
                # Check X-Session-Token or Authorization: Bearer
                token = headers.get(b"x-session-token", b"")
                if isinstance(token, bytes):
                    token = token.decode()
                if not token:
                    auth = headers.get(b"authorization", b"")
                    if isinstance(auth, bytes):
                        auth = auth.decode()
                    if auth.startswith("Bearer "):
                        token = auth[7:]

                if not token or token.strip() in (
                    "", "anonymous", "null", "None", "_default"
                ):
                    await send({
                        "type": "http.response.start",
                        "status": 400,
                        "headers": [[b"content-type", b"application/json"]],
                    })
                    await send({
                        "type": "http.response.body",
                        "body": b'{"error":"SESSION_MISSING","http_status":400}',
                    })
                    return

        await self.app(scope, receive, send)
```

## Pitfalls

### 1. Tests that call tools without session_id will fail after adding middleware
Existing test files often call `mcp.call_tool("tool_name")` without `session_id`. After middleware is armed, these all fail with `SESSION_MISSING`. This is **correct behavior** — update tests to pass `session_id="SEAL-test-session"` in arguments.

**Pattern for test updates:**
```python
# Before (anonymous)
res = await mcp.call_tool("well_state")

# After (session-bound)
res = await mcp.call_tool("well_state", arguments={"session_id": "SEAL-test-session"})
```

**Bulk update pattern (100+ call sites):** Write a Python script to transform call_tool invocations. Watch for three patterns:
1. **Single-line with arguments:** `call_tool("name", arguments={...})` — add `"session_id": "SEAL-test-session"` to existing dict
2. **Single-line without arguments:** `call_tool("name")` — add `arguments={"session_id": "SEAL-test-session"}`
3. **Variable-based calls:** `call_tool(name, arguments=args)` — use `{**args, "session_id": "SEAL-test-session"}`

**Common script pitfall:** The no-args pattern `call_tool("name")` requires inserting the comma INSIDE the call parens. A naive regex can produce `call_tool("name"), arguments={...}` (outside the paren) instead of `call_tool("name", arguments={...})`. Always validate with `python -m py_compile` after bulk transforms.

### 2. Don't forget JSON string argument parsing
Some MCP transports serialize tool arguments as a JSON string rather than a dict. The middleware MUST handle both:
```python
if isinstance(raw_arguments, str):
    try:
        arguments = json.loads(raw_arguments)
    except (json.JSONDecodeError, TypeError):
        arguments = {}
```
Without this, the `arguments.get("session_id")` call raises `AttributeError` on string arguments.

### 3. Orphaned code when patching conditional blocks
When replacing a multi-line `if/else/return` block with a simpler version, the patch may leave orphaned lines from the old block (e.g., old `return` dict entries). Always verify with `lint` or `read_file` after the patch. This happened in WEALTH's `_validate_direct_session_binding` — the old OBSERVE_UNBOUND return dict had leftover lines after the patch.

### 4. HTTP middleware and FastMCP middleware are different layers
- **ASGI/Starlette middleware** (e.g., `OriginValidationMiddleware`): runs on raw HTTP, sees headers, can reject before FastMCP processes the request
- **FastMCP middleware** (`Middleware` subclass): runs inside FastMCP, sees parsed MCP messages and tool arguments

Both are needed for full coverage. ASGI catches header-level issues; FastMCP catches argument-level issues.

### 5. Middleware MUST strip session_id from arguments before dispatching to tools
After validating `session_id`, the middleware must remove it from `context.message.arguments` before calling `call_next(context)`. Tools that don't declare `session_id` in their Pydantic model will reject it with `ValidationError: Unexpected keyword argument`.

**Symptom:** Tests pass session_id correctly, middleware validates it, but tool execution fails with:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for call[tool_name]
session_id
  Unexpected keyword argument [type=unexpected_keyword_argument, input_value='SEAL-test-session', input_type=str]
```

**Fix — add stripping after validation (already included in template above):**
```python
# Strip session_id from arguments before tool dispatch
# (tools don't declare it; it's middleware-only metadata)
if isinstance(arguments, dict) and "session_id" in arguments:
    cleaned = {k: v for k, v in arguments.items() if k != "session_id"}
    context.message.arguments = cleaned
```

**Why this happens:** FastMCP generates tool input schemas from function signatures. If the function has `param: str` but not `session_id: str`, Pydantic rejects `session_id` as unknown. The middleware validates it, but the tool's Pydantic model also sees it and rejects it.

**Exception:** If tools DO declare `session_id: str | None = None` in their signature (as WEALTH tools do), stripping is optional but still recommended — it keeps the tool's Pydantic model clean and the session concern in the middleware layer only.

## Files Modified in Multi-Organ Rollout (2026-07-18)

| Organ | File | Change |
|-------|------|--------|
| GEOX | `src/geox_mcp/session_enforcement.py` | Added `_error_code_to_http_status()`, `http_status` field |
| WELL | `server.py` | Added `WellSessionValidationMiddleware` (FastMCP) |
| WEALTH | `wealth_mcp/server.py` | Closed `OBSERVE_UNBOUND` pass-through in `_validate_direct_session_binding` |
| WEALTH | `internal/monolith.py` | Added session token validation to `OriginValidationMiddleware` (ASGI) |
