# Federation MCP Server Wiring — The Hound Pattern

> **Pattern class:** Adding a new MCP server to all federation agents
> **Forged:** 2026-07-19 — Hound v10.2.1 deployment
> **Archetype:** dondai1234/master-fetch (MIT, $0, keyless web research)

## The 5-Step Wiring Pattern

When adding a new MCP server that ALL agents should access:

### Step 1 — Install + Verify

```bash
pip install --break-system-packages <package>[all]
# Test MCP init handshake
echo '{"jsonrpc":"2.0","id":0,"method":"initialize",...}' | <command>
# Verify tool listing
```

### Step 2 — Create Launcher Script

Single-line launcher for each agent home:
```bash
# /root/.arifos/agents/<agent>/mcp-launchers/<server>.sh
#!/usr/bin/env bash
exec <command>
```
Create for ALL agent homes: kimi, claude, opencode, gemini, cursor

### Step 3 — Register in Agent MCP Configs

#### Kimi Code (`/root/.kimi/mcp.json`):
```json
"hound": {
  "command": "/root/.arifos/agents/kimi/mcp-launchers/hound.sh",
  "description": "..."
}
```

#### OpenClaw (`/root/.openclaw/workspace/openclaw/exports/mcp-catalog-v1.json`):
```json
{
  "server_id": "hound-mcp",
  "enabled": true,
  "transport": "stdio",
  "command": "hound",
  ...
}
```

### Step 4 — Update Agent Docs

Each agent's AGENTS.md gets the new server in its MCP list:
```markdown
- **MCP servers:** arifos, aforge, geox, wealth, well, minimax, hound, ...
```

### Step 5 — End-to-End Test

```python
# MCP init → tools/list → tools/call test
proc = subprocess.Popen([command], stdin=PIPE, stdout=PIPE)
# ... full MCP handshake + tool call verification
```

## Hound-Specific Notes

- **Package:** `hound-mcp[all]` (v10.2.1, MIT)
- **Tools:** `mcp_smart_fetch`, `mcp_smart_search`, `mcp_smart_crawl`, `mcp_screenshot`, `cache_clear`, `version`
- **Tools use `mcp_` prefix** — discovered during testing, not documented in README
- **Prerequisite:** `playwright install chromium` (already installed on af-forge)
- **Zero cost:** No API keys, 10 keyless search backends, runs locally
- **Caveat:** A-FLOW/WawaBot unreachable (SSH port 22 closed, Tailscale off) — requires node provisioning before wiring

## Pitfalls

1. **MCP tool prefix discovery:** Always run `tools/list` after install — tool names may differ from README documentation (e.g., `mcp_smart_fetch` vs `smart_fetch`)
2. **shell escaping:** Testing MCP stdio from bash is fragile. Use Python `subprocess.Popen` with explicit stdin/stdout.
3. **Agent catalog format:** OpenClaw uses its own catalog format (`mcp-catalog-v1.json`), not the standard `mcp.json`. Check each agent's config format.
4. **Launcher perms:** Always `chmod +x` launcher scripts — silent failure otherwise.
