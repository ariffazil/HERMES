# GEOX GUI Debugging — Token Gate + Empty-Body Crash (2026-07-19)

## The Problem
Arif opened `https://geox.arif-fazil.com/gui/` — got "GEOX returned an invalid MCP envelope." Required an SCT token to proceed. He couldn't get in.

## Root Cause (two bugs)

### Bug 1: Mandatory token gate
`OperatorCockpit.tsx` required `bindSession(token)` before connecting. GEOX supports anonymous MCP sessions natively (18 tools, OBSERVE_ONLY), but the GUI code blocked access without an arifOS SCT.

### Bug 2: Empty-body parser crash
`geoxMcpClient.ts::parseEnvelope()` crashed on `notifications/initialized` response (HTTP 202, `content-length: 0`). Empty string → `JSON.parse("")` throws → "invalid MCP envelope."

```javascript
// BEFORE (broken):
function parseEnvelope(text, id) {
  const chunks = text.split('\n')...
  const candidates = chunks.length > 0 ? chunks : [text]; // [""] — empty string!
  for (const candidate of candidates) {
    JSON.parse(candidate); // throws on ""
  }
  throw new Error('GEOX returned an invalid MCP envelope.');
}

// AFTER (fixed):
function parseEnvelope(text, id) {
  if (!text.trim()) return {}; // <— handle 202 empty body
  // ... rest of parsing
}
```

## Fix Applied

### 1. Added anonymous `connect()` method to `GeoxMcpClient`
```typescript
async connect(): Promise<GeoxSurfaceStatus> {
  this.token = '';
  this.identity = null;
  this.mcpSessionId = '';
  this.initialized = false;
  await this.initialize();
  const result = await this.callTool({ tool: 'geox_surface_status', arguments: { mode: 'registry' } });
  return result as GeoxSurfaceStatus;
}
```

### 2. Auto-connect on mount in `SessionGate`
```typescript
useEffect(() => {
  if (token.trim()) return; // user has a token
  setState('connecting');
  geoxMcpClient.connect()
    .then((status) => onBound(null, status))
    .catch((caught) => setError(caught.message));
}, []);
```

## Verification
- GUI: `https://geox.arif-fazil.com/gui/` → HTTP 200, auto-connects anonymously
- Well-Desk: `https://geox.arif-fazil.com/apps/well-desk/` → HTTP 200 (separate surface)
- MCP: Anonymous `tools/list` returns 18 tools without any token

## Key Insight
GEOX MCP supports anonymous sessions. The auth gate was a UI decision, not a server requirement. Sovereign tools should default to zero-friction access — token binding is opt-in for elevated authority, not a gate.
