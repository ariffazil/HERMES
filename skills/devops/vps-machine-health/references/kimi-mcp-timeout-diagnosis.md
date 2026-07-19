# Kimi Code MCP Timeout Diagnosis (2026-07-16)

## Problem
Kimi Code CLI (v1.47.0, installed via binary at `/root/.kimi-code/bin/kimi`) reports:
```
MCP server "arifos" failed: Timed out after 30000ms
```

Other MCP servers (capability-index, serena, brave-search) connect fine.

## Root Cause (confirmed 2026-07-16)

The stdio loop in `__main__.py` (lines 398-724) is **correct** — it handles initialize, tools/list, tools/call with proper select()-based non-blocking I/O. The server does NOT exit after initialize.

**Real cause: startup latency.** Python import takes 7-8s (huggingface_hub, MemoryEngine, federation bridge discovery). Under heavy load (30GB RAM, load 118+), startup can take 15-20s+. The Kimi CLI default `startupTimeoutMs: 30000` is too tight — by the time initialize responds, there's barely enough time for tools/list before the 30s deadline.

**Proof:** subprocess test with `time.sleep(2)` after spawn → initialize responds in 4s, tools/list responds in 0.00s with 33 tools. Without the sleep (server still bootstrapping), initialize takes 8s and tools/list times out.

## Launcher Script
`/root/.arifos/agents/kimi/mcp-launchers/arifos.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
export AAA_MCP_TRANSPORT=stdio
export ARIFOS_MINIMAL_STDIO=1
export PYTHONNOUSERSITE=1
cd /opt/arifos
exec /opt/arifos/venv/bin/python -m arifosmcp.runtime
```

## Config Location
`/root/.kimi-code/mcp.json` — user-level MCP config for Kimi Code CLI.

## Kimi Code MCP Config Format (official docs)
Per https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "/path/to/script.sh",    // stdio
      "url": "http://127.0.0.1:PORT/mcp", // HTTP
      "transport": "sse",                  // SSE (legacy)
      "env": {"KEY": "value"},            // optional
      "cwd": "/path",                      // optional
      "startupTimeoutMs": 60000,           // optional, default 30000
      "toolTimeoutMs": 120000,             // optional
      "enabled": true,                     // optional
      "enabledTools": ["tool1"],           // optional allowlist
      "disabledTools": ["tool2"]           // optional blocklist
    }
  }
}
```

## Fix Applied (2026-07-16)

Added `"startupTimeoutMs": 60000` to ALL MCP servers in `/root/.kimi-code/mcp.json`:

```json
"arifos": {
  "command": "/root/.arifos/agents/kimi/mcp-launchers/arifos.sh",
  "startupTimeoutMs": 60000,
  "description": "..."
}
```

## Alternative: HTTP Transport

Instead of stdio (which requires full Python startup per session), point Kimi at the already-running arifOS HTTP server on port 8088:
```json
"arifos": {
  "url": "http://127.0.0.1:8088/mcp",
  "description": "..."
}
```
This avoids the 7.5s+ Python cold start entirely. Requires session handshake (Accept header + Mcp-Session-Id).

## MCP Stdio Debugging Technique

When an MCP stdio server times out, test with subprocess + select():

```python
import subprocess, time, json, select, os

proc = subprocess.Popen(
    ['/path/to/launcher.sh'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env={**os.environ, 'AAA_MCP_TRANSPORT': 'stdio'},
)

# MUST wait for server to finish bootstrapping
time.sleep(2)

# Send initialize
proc.stdin.write((json.dumps({
    "jsonrpc": "2.0", "id": 0, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
               "clientInfo": {"name": "debug", "version": "1.0"}}
}) + '\n').encode())
proc.stdin.flush()

# Read with timeout
r, _, _ = select.select([proc.stdout], [], [], 30)
if r:
    resp = json.loads(proc.stdout.readline())
    # Now send tools/list and measure response time
```

Key insight: if initialize responds but tools/list doesn't, the issue is startup latency (not the message loop). Increase `startupTimeoutMs`.

## Status
**RESOLVED** — `startupTimeoutMs: 60000` applied. Verified tools/list responds correctly after warm startup.
