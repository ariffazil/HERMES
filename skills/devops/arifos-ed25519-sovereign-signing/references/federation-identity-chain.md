# Federation Identity Chain — Telegram → A2A → OpenClaw → arifOS

## The Problem

Every hop in the chain strips the original sender's identity:

```
Telegram sender (267378578)
  → A2A server (port 3001) — drops identity, only forwards message text
  → OpenClaw gateway (ws://127.0.0.1:18789) — no actor_id → coerces to "openclaw-anon"
  → arifOS kernel (port 8088) — envelope rejects: "actor_id is mandatory"
```

## Fixes Applied (2026-07-12)

### 1. federation_gateway.js — mcpCall identity param

```javascript
// Before: headers only had Content-Type, Accept, Content-Length
// After: accepts optional identity param
async function mcpCall(organKey, method, params = {}, timeoutMs = 10000, identity = {}) {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Content-Length': Buffer.byteLength(payload),
  };
  if (identity.actor_id) headers['X-Actor-Id'] = identity.actor_id;
  if (identity.session_id) headers['X-Session-Id'] = identity.session_id;
  // ...
}
```

### 2. openclaw.json — X-Actor-Id header in arifOS MCP config

```json
{
  "arifos": {
    "url": "http://127.0.0.1:8088/mcp",
    "headers": {
      "Accept": "application/json",
      "X-Actor-Id": "openclaw"
    }
  }
}
```

## Remaining Gap

The arifOS ingress middleware (`ingress_middleware.py:1505-1539`) reads `actor_id` from:
1. MCP tool call arguments (`arguments.actor_id`) — preferred
2. FederationEnvelope (`envelope.actor_id`) — fallback

It does NOT read `X-Actor-Id` from HTTP headers. To pass dynamic per-sender identity, the middleware must be patched to extract `X-Actor-Id` from the incoming request and inject it into the MCP context.

## Files Touched

- `/root/AAA/a2a-server/federation_gateway.js` — mcpCall function
- `/root/.openclaw/openclaw.json` — arifos MCP server headers
- `/opt/arifos/app/arifosmcp/runtime/ingress_middleware.py` — **needs patch** to read X-Actor-Id header
