# MCP Organ Schema-vs-Runtime Alignment Audit

**Repeatable pattern for any arifOS federation organ.** Checks whether the published MCP tool schema matches what the runtime authentication gate actually enforces.

## Why This Matters

An MCP organ can declare session/actor fields in its runtime gate but omit them from the published `tools/list` schema. Schema-conforming clients (LLMs, typed SDKs) can't discover auth fields the server never advertises. The organ works at runtime but its contract is a lie.

## The 4-Step Protocol

### Step 1 — Query Live Published Schema

Get the actual `tools/list` response from the running server. Do NOT read source code alone — the published schema is what callers see.

```bash
# Initialize session
SESSION_ID=$(curl -si http://127.0.0.1:<PORT>/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
    "protocolVersion":"2024-11-05","capabilities":{},
    "clientInfo":{"name":"audit-probe","version":"1.0"}
  }}' | grep -i 'mcp-session-id' | awk '{print $2}' | tr -d '\r')

# Get tool list
curl -s http://127.0.0.1:<PORT>/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for t in d.get('result',{}).get('tools',[]):
    props = list(t.get('inputSchema',{}).get('properties',{}).keys())
    print(f\"{t['name']}: {props}\")
"
```

**Check:** Does each tool's `inputSchema.properties` include `session_id`, `actor_id`, or whatever auth fields the runtime gate requires?

### Step 2 — Read the Runtime Gate

Find the server's tool call wrapper/interceptor. Look for:
- `_governance_call_tool` or similar wrapper around `mcp.call_tool`
- Where it extracts `session_id` / `actor_id` (usually from `_meta`, `kwargs`, or tool args)
- What happens when validation fails

```bash
search_files(pattern='session_id.*actor_id|_governance|call_tool', path='REPO', file_glob='*.py')
```

Document the extraction path:
1. `kwargs.get("actor_id")` — transport-level system injection
2. `arguments.get("_meta", {}).get("actor_id")` — caller metadata
3. Hardcoded defaults (e.g., `"wealth-mcp"`, `"_default"`)

### Step 3 — Check for Dead Code

Search for validation functions that are defined but never called:

```bash
# Find all definitions
search_files(pattern='def validate_session|def check_auth|def verify_actor', path='REPO')

# Find all call sites
search_files(pattern='await validate_session|validate_session\(|check_auth\(', path='REPO')
```

A function that appears only at its `def` line and its `__all__` export is dead code.

### Step 4 — Check the OBSERVE Bypass

Many organs allow unbound sessions for compute-only tools. Check:
- What tools are in the OBSERVE/allowlist surface?
- Does the entire published canonical surface fall under OBSERVE?
- If yes, the session gate is effectively a no-op for the published surface

## Report Template

```
| Tool | session_id in schema? | actor_id in schema? |
|------|----------------------|---------------------|
| tool_1 | ✅/❌ | ✅/❌ |
...

Gaps:
- Schema omits auth fields (N/M tools)
- Dead code: <function> defined but never called
- OBSERVE bypass covers entire published surface
```

## Known Findings

### WEALTH (2026-07-18)
- **11/12 tools** omit `session_id`/`actor_id` from published schema
- `validate_session_at_arifos()` in `wealth_arifos_bridge/__init__.py` is dead code
- Runtime uses synchronous `_validate_session_via_http_bridge()` in `server.py`
- All 7 canonical `capital_*` tools accept unbound sessions via OBSERVE bypass

### Ports Reference
| Organ | MCP Port | URL |
|-------|----------|-----|
| WEALTH | 18082 | http://127.0.0.1:18082/mcp |
| GEOX | 18765 | http://127.0.0.1:18765/mcp |
| arifOS | 8088 | http://127.0.0.1:8088/mcp |
