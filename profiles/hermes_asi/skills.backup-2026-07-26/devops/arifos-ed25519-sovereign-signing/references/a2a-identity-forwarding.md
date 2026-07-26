# A2A Identity Forwarding Gap (2026-07-12)

## Problem

The A2A server (port 3001) proxies Telegram → OpenClaw → arifOS but STRIPS identity at each hop:

```
Telegram sender (267378578)
  → A2A server (drops identity in dispatchOpenClawTask)
  → OpenClaw (null actor_id → coerced to "openclaw-anon")
  → arifOS ingress middleware (rejects MUTATE/ATOMIC actions)
```

**Kernel log evidence:**
```
WARNING: wrap_legacy_call: null actor_id coerced to 'openclaw-anon'
WARNING: KERNEL INTERCEPTOR: DENY for arif_ops_measure: capability not registered
```

## Fixes Applied

### 1. federation_gateway.js — mcpCall identity forwarding

**File:** `/root/AAA/a2a-server/federation_gateway.js`

Added optional `identity` parameter to `mcpCall()`:

```javascript
async function mcpCall(organKey, method, params = {}, timeoutMs = 10000, identity = {}) {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Content-Length': Buffer.byteLength(payload),
  };
  if (identity.actor_id) headers['X-Actor-Id'] = identity.actor_id;
  if (identity.session_id) headers['X-Session-Id'] = identity.session_id;
  // ... rest of request
}
```

### 2. OpenClaw MCP server config — static header

**File:** `/root/.openclaw/openclaw.json`

Added `X-Actor-Id: openclaw` header to arifOS MCP server config:
```json
"arifos": {
  "url": "http://127.0.0.1:8088/mcp",
  "headers": {
    "Accept": "application/json",
    "X-Actor-Id": "openclaw"
  }
}
```

## Remaining Gap

The kernel's ingress middleware (`ingress_middleware.py`) reads `actor_id` from:
1. MCP tool arguments (line 1511: `_args.get("actor_id")`)
2. FederationEnvelope (line 1514: `envelope.actor_id`)

It does NOT read `X-Actor-Id` from HTTP headers. To pass dynamic per-Telegram-sender identity, the middleware needs a patch to extract `X-Actor-Id` from incoming request headers and inject it into the tool's argument context before the tool executes.

## Clean Architecture (MCP/A2A Split)

Per Arif's constitutional verdict (2026-07-12), MCP and A2A are two separate planes:

- **MCP** = capability execution (tools, resources, prompts, schemas, sessions)
- **A2A** = agent federation (discovery, delegation, artifacts, long-running tasks)

The split is documented at `/root/A-FORGE/forge_work/2026-07-12/MCP-A2A-PROTOCOL-SPLIT.md`.
