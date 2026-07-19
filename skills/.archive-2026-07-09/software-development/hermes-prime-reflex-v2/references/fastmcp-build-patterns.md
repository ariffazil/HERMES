# FastMCP 3.4.2 — Build & Verify Patterns

> Session: 2026-07-04. Building stealth-browser MCP server from scratch.

## Constructor

```python
# WRONG — FastMCP 3.4.2 removed description kwarg
mcp = FastMCP("my-server", description="...")  # TypeError

# CORRECT
mcp = FastMCP("my-server")
```

## Tool Registration

```python
from fastmcp import FastMCP
mcp = FastMCP("my-server")

@mcp.tool()
async def my_tool(param: str) -> str:
    """Docstring becomes tool description."""
    return json.dumps({"result": param})
```

Tools auto-discovered from `@mcp.tool()` decorators. No manual registration needed.

## MCP Handshake (Critical)

The MCP protocol requires `initialize` before `tools/list`. Sending `tools/list` alone returns 0 tools.

```
# WRONG — 0 tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python server.py

# CORRECT — initialize first, then tools/list
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n' | python server.py
```

## Verify Script

```bash
cd /path/to/server
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n' | timeout 5 ./venv/bin/python src/server.py 2>/dev/null | python3 -c "
import sys,json
for line in sys.stdin:
    d=json.loads(line.strip())
    if d.get('id')==2:
        tools=d.get('result',{}).get('tools',[])
        print(f'Tools: {len(tools)}')
        for t in tools: print(f'  - {t[\"name\"]}')
"
```

## Venv Pattern

Always use a dedicated venv per MCP server. Never install MCP deps globally.

```bash
mkdir -p /root/<server-name>/src
cd /root/<server-name>
python3 -m venv venv
./venv/bin/pip install fastmcp <other-deps>
```

## OpenClaw Config

```json
{
  "mcp": {
    "servers": {
      "<server-name>": {
        "command": "/root/<server-name>/venv/bin/python",
        "args": ["/root/<server-name>/src/server.py"],
        "env": {},
        "enabled": true
      }
    }
  }
}
```

## Pitfalls

- `FastMCP("name", description="...")` FAILS in 3.4.2. Use positional arg only.
- `tools/list` without `initialize` returns 0 tools. Always send initialize first.
- `--help` on stdio MCP servers doesn't work (they read stdin). Use the JSON handshake to verify.
- Pyright/LSP will report "Import X could not be resolved" for venv packages. This is expected — the server runs with its own venv Python, not system Python.
