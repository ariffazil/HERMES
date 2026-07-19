---
name: mcp-tool-upgrade-lifecycle
description: "Protocol-correct lifecycle for upgrading MCP tools — adding params, new modes, preload guards, schema signaling, curl testing. Based on MCP spec 2025-06-18."
version: 1.0.0
author: Hermes-PRIME
created: 2026-07-06
tags: [mcp, fastmcp, upgrade, lifecycle, protocol, tools, schema]
---

# MCP Tool Upgrade Lifecycle

Protocol mechanics for modifying running FastMCP servers in production.

## When to Use
- Adding a new parameter to an existing @mcp.tool
- Adding a new mode to a multi-mode tool
- Exempting modes from preload guards
- Testing MCP tools via curl
- Deploying schema changes to production

## Prerequisites
- FastMCP 3.4.2+ server running behind reverse proxy
- MCP Protocol 2025-06-18 (streamable HTTP transport)
- systemd service management

---

## 1. Adding an Optional Parameter

The MCP boundary is `inputSchema` in the `tools/list` response.

**TWO files must change, not one.** The monolith function AND the `@mcp.tool()` wrapper in `server.py`. If only the monolith gets the param, Pydantic rejects it at the MCP boundary with `Unexpected keyword_argument`. This was demonstrated live in the WEALTH APEX Pillar IV upgrade (2026-07-06) — agents updated monolith but not server.py, causing `BAD_INPUT_VALUE` errors on all 3 tools.

### a) Update the monolith function
```python
# internal/monolith.py
async def my_tool(existing: str, new_param: bool = False) -> dict:
    ...
```

### b) Update the @mcp.tool() wrapper in server.py
```python
# wealth_mcp/server.py
@mcp.tool(name="my_tool")
async def my_tool(existing: str, new_param: bool = False) -> dict:
    """Docstring must mention new param."""
    return await monolith_impl(existing=existing, new_param=new_param)
```

### c) Client discovery
Clients cache `tools/list`. After restart, existing sessions won't see new schema until they re-run `tools/list`. Signal with `notifications/tools/list_changed`.

### d) inputSchema
FastMCP auto-generates `inputSchema` from the wrapper function signature. No manual JSON Schema editing needed. Verify with tools/list after restart.

---

## 2. Preload Guard — Exempting Modes

Optional params on existing tools are NOT new capabilities. Do NOT require new resource preloads for optional params.

Pattern for mode-aware preload exemption:
```python
async def _governance_call_tool(name, arguments=None, **kwargs):
    _mode = (arguments or {}).get("mode", "")
    required = (
        [] if _mode == "kelly" else _REQUIRED_PRELOADS.get(name, [])
    )
```

- Gate on mode, not tool name
- Modes that don't need external data should be exempt
- Handle None case gracefully — fetch lazily or return clear error

---

## 3. "Mode" Variants: Extend vs New Tool

| Condition | Action |
|---|---|
| New mode is backward-compatible (optional param, same return shape) | Extend in-place |
| Different outputSchema, different error semantics | New tool |

Tool names are the stable identifier — clients cache by name.

Mode param pattern:
```python
@mcp.tool()
def search(query: str, mode: Literal["fast", "deep"] = "fast") -> str: ...
```

---

## 4. Signaling Schema Changes

Protocol mechanism: `notifications/tools/list_changed`

Server must:
1. Declare `"listChanged": true` in tools capability during initialize
2. After schema changes are live, emit:
```json
{"jsonrpc": "2.0", "method": "notifications/tools/list_changed"}
```
3. Client MUST then re-issue `tools/list`

FastMCP + streamable-HTTP note: On server restart, existing sessions are dropped — clients reconnect and re-initialize automatically. The notification matters for **hot-reload** scenarios.

No schema versioning field in MCP spec — the inputSchema itself is the version signal.

---

## 5. End-to-End curl Testing (Streamable HTTP)

3-step sequence:

### Step 1: Initialize (get session ID)
```bash
curl -X POST https://your-server/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
      "protocolVersion": "2025-06-18",
      "capabilities": {},
      "clientInfo": {"name": "curl-test", "version": "0.1"}
    }
  }'
# Capture Mcp-Session-Id from response headers
```

### Step 2: Send initialized notification
```bash
curl -X POST https://your-server/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: <session-id>" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -d '{"jsonrpc": "2.0", "method": "notifications/initialized"}'
```

### Step 3: Call tools/list or tools/call
```bash
curl -X POST https://your-server/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: <session-id>" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -d '{
    "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
  }'
```

Verify new param appears in `inputSchema.properties` and is absent from `required`.

### Caddy note
Ensure Caddy passes `Mcp-Session-Id` and `MCP-Protocol-Version` headers through — add `header_up` directives if reverse proxy strips non-standard headers.

---

## 6. Deployment Checklist (Complete Closure)

Arif demands **no loose ends**. Every MCP upgrade must complete the full loop:

1. Edit `internal/monolith.py` (engine)
2. Edit `wealth_mcp/server.py` (wrapper) — **must mirror monolith params**
3. `python3 -c "import ast; ast.parse(open('file.py').read()); print('OK')"` — syntax check
4. `systemctl restart wealth.service` — restart
5. `curl -sf https://wealth.arif-fazil.com/health` — verify alive
6. `git add -A && git commit` in BOTH repos (WEALTH + arifOS if theory changed)
7. Update SOT manifest (AGENTS.md `last_verified`, tool counts)
8. `git push origin main` — push to GitHub
9. curl 3-step E2E test through `wealth.arif-fazil.com/mcp` — verify new params work
10. Audit README — update tool counts, add new capability docs

**Never commit server.py without monolith. Never commit monolith without server.py.** They are a pair.

## 7. Stale Bytecode

Python caches `.pyc` in `__pycache__/`. After edits:
```bash
# Force recompile
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
systemctl restart <service>
```

Or set `PYTHONDONTWRITEBYTECODE=1` in the service environment.

---

## Pitfalls

1. **Pyright false positives** — large monolith files confuse static analysis. Runtime works, Pyright complains. Ignore for params that exist in the monolith but not in the wrapper's import scope.
2. **Sibling subagents overwriting** — if multiple agents edit the same file, last write wins. Use file locks or coordinate.
3. **Preload guard blocks new modes** — always exempt modes that don't need external data.
4. **Client caches stale schema** — restart drops sessions, clients reconnect with fresh `tools/list`.
5. **Caddy strips headers** — `Mcp-Session-Id` and `MCP-Protocol-Version` are non-standard; verify proxy passes them.
6. **Missing notifications/initialized** — MUST send after `initialize` before `tools/call`. Skipping is a protocol violation. Some servers are lenient, others reject.
7. **Stateless servers** — some FastMCP deployments don't generate `Mcp-Session-Id`. Each request is independent. Preload guards that depend on session state won't work — handle gracefully.
8. **Wrapper must mirror monolith** (LESSON LEARNED 2026-07-06): Adding a param to the monolith function is NOT enough. The `@mcp.tool()` wrapper in server.py MUST also expose the param. Pydantic validates at the MCP boundary, not the monolith boundary. If wrapper lacks the param → `Unexpected keyword argument` error. Always update BOTH files: monolith + server.py wrapper.

## Spec References
- Tools spec: inputSchema, listChanged, notification
- Lifecycle spec: capability negotiation, session scope
- Transports spec: Mcp-Session-Id, streamable HTTP sequence

## A-FORGE TypeScript Upgrades

For TypeScript/Zod-based MCP tool modifications in A-FORGE (`proxyTools.ts`, `serve.ts`), see `references/aforge-typescript-upgrade.md` — covers the `forge_fetch` search-mode addition pattern (optional `query` param, Zod schema, tsc build cycle, backward compat testing).
