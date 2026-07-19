# MCP Apps Framework — Core Knowledge for Federation Agents

> **Source:** MCP Apps documentation (Anthropic). Compressed for agent use.
> **Date:** 2026-07-10
> **Status:** ACTIVE — embedded in `arif-mcp-governor` skill.

---

## The One-Line Definition

**MCP Apps = interactive HTML interfaces rendered inside the chat host (Claude Desktop, VS Code Copilot, etc.) via sandboxed iframe — not web pages, not dashboards.**

---

## Key Facts

### MCP Apps vs GUI
| | MCP App | GUI |
|---|---|---|
| Renders in | Chat (iframe) | Browser tab |
| Discoverable by agents | ✅ Yes (via apps.json) | ❌ No |
| Communication | JSON-RPC over postMessage | HTTP/WebSocket |
| Security | Sandboxed iframe, zero parent access | Standard web security |
| Access to parent page cookies | None | None |
| Examples | well-desk, seismic-viewer | geox.arif-fazil.com dashboard |

**Rule:** GUI is the human console. MCP App is the agent-discoverable UI surface.

---

## MCP Apps Protocol Requirements

### 1. Tool Must Declare `_meta.ui.resourceUri`
Any tool that opens a UI **must** include in its description:
```json
{
  "name": "geox_well_desk",
  "description": "Open the Well Desk app",
  "_meta": {
    "ui": {
      "resourceUri": "ui://geox/well-desk/index.html"
    }
  }
}
```
**Rule:** No `_meta.ui.resourceUri` = the tool cannot open a UI in MCP Apps spec.

### 2. Server Must Serve `ui://` Resources
The `ui://` scheme is served by FastMCP. Maps to:
- `ui://geox/well-desk/index.html` → `/srv/mcp/apps/well-desk/index.html`

### 3. JSON-RPC Messages (ui/*)
Core messages apps and hosts exchange:
- `ui/initialize` — app bootstraps with host
- `ui/update-model-context` — app pushes context to model
- `tools/call` — app requests a tool call through the host
- `ui/notifications/initialized` — app signals ready

### 4. apps.json Manifest (Discovery Layer)
```json
{
  "apps": [
    {
      "id": "well-desk",
      "name": "Well Desk",
      "description": "Interactive well planning and evaluation interface",
      "url": "ui://geox/well-desk/index.html",
      "protocol": "mcp-ui-v1"
    }
  ]
}
```
- `apps.json` is what makes GEOX discoverable as an app host
- `.well-known/agent.json` must reference `apps_manifest: "https://geox.arif-fazil.com/apps.json"`

### 5. Sandbox Security
> "MCP Apps run in a sandboxed iframe… cannot access the parent page, steal cookies, or escape."

GEOX apps are safe to expose. All are static bundles over HTTPS with no shared cookies or parent DOM access.

---

## GEOX Current State (as of 2026-07-10)

### Already Deployed (7 apps, all HTTP 200)
| App | URL | Status |
|---|---|---|
| well-desk | `/apps/well-desk/` | LIVE |
| seismic-review | `/apps/seismic-review/` | LIVE |
| prospect-ui | `/apps/prospect-ui/` | LIVE |
| ac-risk | `/apps/ac-risk/` | LIVE |
| attribute-audit | `/apps/attribute-audit/` | LIVE |
| georeference | `/apps/georeference/` | LIVE |
| analog-digitizer | `/apps/analog-digitizer/` | LIVE |

### Existing apps.json (GEOX-native format, 2026-04-15)
- Location: `https://geox.arif-fazil.com/apps.json`
- Format: GEOX-internal (uses `route` not `ui://` URL scheme)
- **Gap for MCP spec compliance:** Missing `resourceUri`, `protocol` fields
- Not referenced in `.well-known/agent.json`

### What GEOX Needs for Full MCP Compliance
1. **apps.json MCP overlay** — add `url` with `ui://` scheme + `protocol` field per app
2. **agent.json update** — create `/.well-known/agent.json` referencing both `tools.json` and `apps.json`
3. **tools.json** — serve canonical tool list at `/tools.json`
4. **ui:// resource handler** — FastMCP must serve `ui://` resources (not yet confirmed wired)

---

## Agent Enforcement Rules

- ❌ No tool without `_meta.ui.resourceUri` can open a UI in MCP Apps
- ❌ No app without `apps.json` is agent-discoverable
- ❌ No GUI without manifest can be agent-visible
- ❌ No MCP surface without `tools.json` is enterprise-valid
- ✅ Before proposing to create `apps.json`, probe `https://geox.arif-fazil.com/apps.json` first
