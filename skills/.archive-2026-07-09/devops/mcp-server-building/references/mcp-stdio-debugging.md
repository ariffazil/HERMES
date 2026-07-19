# MCP Stdio Debugging Technique

When an MCP stdio server fails to connect (timeout, no response), use this subprocess + select() pattern to isolate exactly which MCP message hangs.

## The Pattern

```python
import subprocess, time, json, select, os

env = os.environ.copy()
env['AAA_MCP_TRANSPORT'] = 'stdio'  # or whatever the server needs
env['ARIFOS_MINIMAL_STDIO'] = '1'

proc = subprocess.Popen(
    ['/path/to/launcher.sh'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
)

# CRITICAL: wait for server to finish bootstrapping
# Python imports can take 7-10s for heavy servers
time.sleep(2)

def send_msg(msg):
    proc.stdin.write((json.dumps(msg) + '\n').encode())
    proc.stdin.flush()

def recv_msg(timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        r, _, _ = select.select([proc.stdout], [], [], min(1.0, timeout - (time.time() - t0)))
        if r:
            line = proc.stdout.readline()
            if line:
                return json.loads(line), time.time() - t0
    return None, time.time() - t0

# Step 1: Initialize
resp, dt = send_and_wait({
    "jsonrpc": "2.0", "id": 0, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
               "clientInfo": {"name": "debug", "version": "1.0"}}
}, timeout=30)
print(f"initialize: {dt:.2f}s")

# Step 2: Notification (required by MCP spec)
send_msg({"jsonrpc": "2.0", "method": "notifications/initialized"})

# Step 3: tools/list
resp, dt = recv_msg(timeout=15)
print(f"tools/list: {dt:.2f}s — {len(resp.get('result',{}).get('tools',[]))} tools")

proc.terminate()
```

## Diagnostic Matrix

| initialize | tools/list | Diagnosis |
|---|---|---|
| ✅ responds | ✅ responds | Server works. Problem is client-side config. |
| ✅ responds | ❌ timeout | Startup latency issue. Increase `startupTimeoutMs`. |
| ❌ timeout | ❌ timeout | Server won't start. Check launcher script, Python env, imports. |
| ✅ responds | ❌ error | Protocol mismatch. Check MCP version negotiation. |

## Common Causes

1. **Startup latency** (most common): Heavy Python imports (huggingface_hub, transformers) take 7-10s. Under load, 15-20s. Default `startupTimeoutMs: 30000` is too tight. Fix: `"startupTimeoutMs": 60000` in client config.

2. **Missing bootstrap wait**: If you send initialize immediately after spawning the process, the server hasn't finished importing yet. The `time.sleep(2)` is critical.

3. **stderr bleeding to stdout**: If the server prints warnings to stdout before the JSON-RPC response, the client can't parse the response. Fix: redirect stderr in the launcher script, or suppress warnings in the server code.

4. **Non-blocking stdin issues**: Some servers set `O_NONBLOCK` on stdin. This works fine with pipes but can cause issues with PTY-based clients. Test with pipes first.

## Kimi Code Config (startupTimeoutMs)

Per https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "/path/to/launcher.sh",
      "startupTimeoutMs": 60000,
      "toolTimeoutMs": 120000
    }
  }
}
```

Default `startupTimeoutMs` is 30000 (30s). For Python-heavy servers, 60000 (60s) is safer.

## OpenClaw/Hermes MCP Config

For OpenClaw (`~/.openclaw/openclaw.json`), the equivalent timeout is in the server entry:
```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "/path/to/launcher.sh",
        "startupTimeout": 60000
      }
    }
  }
}
```

For Hermes (`~/.hermes/config.yaml`), MCP server timeouts are under `mcp.servers.*.timeout`.
