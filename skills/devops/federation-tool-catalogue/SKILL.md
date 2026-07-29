---
name: federation-tool-catalogue
description: >-
  Build human-readable MCP tool catalogues and discovery dashboards across
  the arifOS federation organs. Covers probing tools/list endpoints from
  all organs, handling auth-gated MCP endpoints with fallback sources,
  and forging a self-contained static dashboard with search and filter.
tags:
  - federation
  - mcp
  - discovery
  - catalogue
  - dashboard
  - tools
  - forge
triggers:
  - "tool catalogue"
  - "show all tools"
  - "unified tool list"
  - "tool dashboard"
  - "MCP tool inventory"
  - "what tools exist"
  - "federation tools"
  - "list all MCP tools"
  - "tool discovery"
  - "catalogue all organs"
---

# Federation Tool Catalogue — MCP Tool Discovery Dashboard

Pattern for discovering, cataloguing, and rendering all MCP tools across arifOS federation organs into a single human-readable dashboard. Covers endpoint probing, auth handling, fallback data sources, and static HTML generation.

## Architecture Overview

```
                    ┌─────────────────────────┐
                    │   Federation Organs     │
                    │  ┌───┐ ┌────┐ ┌──┐ ┌──┐ │
Discover ──────────▶│  │OS │ │FORGE│ │GX│ │WL│ │
                    │  └───┘ └────┘ └──┘ └──┘ │
                    │  ┌──┐ ┌────┐            │
                    │  │WH│ │WELL│            │
                    │  └──┘ └────┘            │
                    └─────────┬───────────────┘
                              │
                    ┌─────────▼───────────────┐
                    │    Data Collection       │
                    │  MCP tools/list (JRON-RPC) │
                    │  HTTP /tools endpoints   │
                    │  Registry JSON fallback  │
                    └─────────┬───────────────┘
                              │
                    ┌─────────▼───────────────┐
                    │   Static HTML Page       │
                    │  Embedded tool data      │
                    │  Dark theme + search     │
                    │  READ ONLY (F1/F13)      │
                    └─────────────────────────┘
```

## Federation Organ MCP Endpoints

| Organ | Port | MCP Path | HTTP /tools | Auth |
|-------|------|----------|-------------|------|
| **arifOS (Kernel)** | 8088 | /mcp | — | Open (needs Accept: application/json) |
| **A-FORGE** | 7072 | /mcp | — | Open |
| **GEOX** | 8081 | /mcp | /tools | Session-gated MCP |
| **WEALTH** | 18082 | /mcp | /tools | Session-gated MCP |
| **WELL** | 18083 | /mcp | /tools | Session-gated MCP |

## Step-by-Step Workflow

### Step 1: Probe Each Organ's Tools Endpoint

Each organ may have different MCP server configurations. Probe in order of reliability:

**A. MCP JSON-RPC (tools/list):** Standard MCP protocol. Post JSON-RPC body.

```bash
# Open MCP endpoint
curl -s -X POST http://127.0.0.1:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# With Accept header (arifOS kernel needs this)
curl -s -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

**B. HTTP /tools endpoint:** Some organs expose a simpler REST endpoint.

```bash
curl -s http://127.0.0.1:8081/tools
curl -s http://127.0.0.1:18082/tools
curl -s http://127.0.0.1:18083/tools
```

**C. Federation Registry Fallback:** If live endpoints are inaccessible, load from the registry.

```bash
# Registry files are at:
/root/A-FORGE/forge_work/2026-07-28/mcp-registry/{organ}.json
```

### Step 2: Handle Auth-Gated MCP Endpoints

Three auth patterns encountered:

| Pattern | Error | Organs | Fix |
|---------|-------|--------|-----|
| Missing Accept header | `Not Acceptable: Client must accept application/json` | arifOS (8088), GEOX (8081) | Add `-H "Accept: application/json"` |
| Missing session ID | `SESSION_MISSING: Mcp-Session-Id header required` | WEALTH (18082), WELL (18083) | Use HTTP /tools endpoint or obtain session first |
| Invalid session ID | `SESSION_INVALID: Unknown or expired session ID` | WEALTH, WELL | Session must be initiated via organ's init flow |

For session-gated organs, fall back to:
1. HTTP `/tools` endpoint (returns tool names + descriptions)
2. Registry JSON files in `/root/A-FORGE/forge_work/2026-07-28/mcp-registry/`
3. Tool definitions visible in Hermes agent's MCP tool list

### Step 3: Collect Tool Data

Extract for each tool:
- **name** — tool identifier (e.g., `arif_init`, `geox_basin`)
- **description** — human-readable purpose
- **inputSchema** — parameter definitions (if available from MCP tools/list)
- **risk tier** — constitutional tier (A-FORGE only, from registry)
- **domain** — grouping prefix (e.g., `geox_`, `forge_`, `well_`, `capital_`, `wealth_`, `arif_`)

```python
# Parse MCP tools/list response
tools = result.get('tools', [])
for t in tools:
    name = t['name']
    description = t.get('description', '')
    schema = t.get('inputSchema', {})
    params = list(schema.get('properties', {}).keys())
```

### Step 4: Build the Static HTML Page

**Architecture:** Single self-contained HTML file with embedded JavaScript data array. No frameworks, no build step, no server dependencies.

**Key features:**
- Dark theme (`--bg: #0d1117` etc.)
- Organ-coded colours:
  - arifOS: blue `#3b82f6`
  - A-FORGE: purple `#a371f7`
  - GEOX: green `#3fb950`
  - WEALTH: gold `#d29922`
  - WELL: red `#f85149`
- Search bar (filters by name, organ, description in real time)
- Collapsible organ sections (click header to expand/collapse)
- Badges per organ (tool count, auth status)
- Auth notice banner for session-gated organs
- Footer with READ ONLY and localhost bind declaration

**Data embedding pattern:**

```javascript
const ORGANS = {
  arifos: {
    label: 'arifOS (Kernel)',
    port: 8088,
    icon: 'arifos',
    mcpNeedsAuth: false,
    color: '#3b82f6',
    tools: [
      {name:'arif_init', desc:'KERNEL 000 · Session ignition...'},
      // ...
    ]
  },
  aforge: { /* 120 tools */ },
  geox: { name, ...tools: [...] },
  wealth: { name, ...tools: [...] },
  well: { name, ...tools: [...] },
};
```

### Step 5: Verify and Seal

1. Serve the page locally:
   ```bash
   cd /path/to/tool-catalogue/
   python3 -m http.server 8099 --bind 127.0.0.1
   ```

2. Verify in browser or via curl:
   ```bash
   # Check serving
   curl -s http://127.0.0.1:8099/ | wc -c
   
   # Verify all tools embedded
   grep -c "name:'" index.html
   ```

3. Write a SEAL_README.md documenting:
   - What was built and why
   - How to access
   - Organ inventory (counts, ports, auth status)
   - Data sources and probes performed
   - Known auth gaps
   - File listing

## Directory Structure

```
tool-catalogue/
├── index.html         # Main catalogue page (self-contained, ~35KB)
└── SEAL_README.md     # Documentation and seal
```

Forge under `/root/A-FORGE/forge_work/{YYYY-MM-DD}/tool-catalogue/`.

## Alternative: Live-Probing Dashboard (Python stdlib)

For a **live** dashboard that re-probes organs on every page load — instead of building a static snapshot — deploy the arifOS MCP Dashboard:

```bash
forge_mcp_ui_start          # Launches on 127.0.0.1:7777
# Or: systemctl start forge-mcp-ui.service
```

**Static vs Live comparison:**

| Dimension | Static Catalogue | Live Dashboard (mcp_dashboard.py) |
|-----------|----------------|-----------------------------------|
| Data freshness | Snapshot at build time | Probes organs on every request |
| Dependencies | None (HTML/JS) | Python stdlib (http.server, json, urllib) |
| Deployment | `python3 -m http.server` | systemd service or `forge_mcp_ui_start` |
| Update cycle | Rebuild manually | Always live |
| Tool count | As-of generation time | Current — auto-detects changes |
| Accept header handling | Manual | Auto-sends for all session-based organs |
| Session management | Not needed | Handles MCP initialize for auth-gated organs |

**When to use which:**
- **Static catalogue** — fixed inventory snapshot for distribution or sharing
- **Live dashboard** — daily tool discovery when surface changes frequently

The live dashboard at `/root/A-FORGE/scripts/mcp_dashboard.py` (496 lines, pure stdlib):
- Handles MCP session lifecycle (initialize + tools/list for WEALTH/WELL/GEOX)
- Auto `Accept: application/json` — critical fix for session-based MCP servers
- Organ-grouped grid with live status badges (F1/F2/F11 compliance)
- All POST requests return HTTP 405 — F1 AMANAH enforced at application level
- CSP headers, no-referrer, read-only filesystem protections

**Proven 2026-07-28:** Deployed as `forge-mcp-ui.service`, 7MB RAM, 5 organs, 181 tools, 0 drift, IPAddressAllow=127.0.0.1 enforced by systemd.

## Pitfalls

- **Auth-gated MCP ≠ unavailable**: WEALTH, WELL, and GEOX return errors on MCP tools/list but have working HTTP /tools endpoints. Check both before declaring an organ unreachable.
- **Accept header required**: arifOS kernel and GEOX reject JSON-RPC requests without `Accept: application/json`. Always include it for these organs.
- **WEALTH /tools returns names only**: The WEALTH HTTP /tools endpoint returns tool names with blank descriptions. Supplement descriptions from the MCP tool definitions visible in the agent's tool list or from the federation registry.
- **WELL /tools returns full detail**: The WELL HTTP /tools endpoint returns full tool descriptions with danger level taxonomy (L1-L3) and fail posture. Prefer this over MCP for WELL.
- **Registry files may be stale**: Registry JSON files in mcp-registry/ are snapshots from the last reconciliation. They may not reflect the latest tool additions/removals.
- **Tool count must match**: After embedding, verify the total tool count matches the sum of all organ tool counts. Mismatches indicate missing data.
- **READ ONLY (F1 compliance)**: The catalogue must NOT have execute buttons, tool invocation, or any write capability. Localhost bind only (F13 compliance).
