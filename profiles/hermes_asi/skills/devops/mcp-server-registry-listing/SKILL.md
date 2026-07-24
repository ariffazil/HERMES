---
name: mcp-server-registry-listing
description: "List an MCP server on public registries — Glama, awesome-mcp-servers, MCP Registry. Covers server.json authoring, well-known deployment, Caddy routing, submission templates, and discovery verification. Use when Arif says 'list GEOX on registries', 'publish MCP server', 'submit to Glama', 'MCP registry', or 'public listing'."
version: 1.0.0
author: Hermes-PRIME
created: 2026-07-19
tags: [mcp, registry, listing, server.json, glama, deployment, public-surface]
---

# MCP Server Registry Listing

## What This Is

The workflow for listing an arifOS federation MCP server (GEOX, WEALTH, etc.) on public MCP registries so AI clients and developers can discover it.

## Registries

| Registry | Type | Submission | Auto-Discovery |
|---|---|---|---|
| **Glama** (glama.ai/mcp/servers) | Directory | Form (needs account) | Crawls GitHub + server.json |
| **Smithery** | Directory | Form | Crawls npm + server.json |
| **PulseMCP** | Directory | Form | Crawls server.json |
| **MCP Registry** (registry.modelcontextprotocol.io) | Official | server.json at well-known | Auto-discovers |
| **awesome-mcp-servers** (GitHub) | Curated list | Pull Request | Manual review |

## The server.json Standard

All registries auto-discover via `server.json` at a well-known path.

**Deploy to:** `https://<subdomain>.arif-fazil.com/.well-known/mcp/server.json`

### Minimal server.json

```json
{
  "name": "ORGAN — Tagline",
  "version": "v2026.MM.DD",
  "description": "One-line capability summary.",
  "repository": "https://github.com/ariffazil/REPO",
  "endpoint": "https://organ.arif-fazil.com/mcp",
  "transport": ["streamable-http"],
  "protocolVersion": "2025-06-18",
  "capabilities": {"tools": true, "resources": true, "prompts": true}
}
```

### Rich server.json (recommended for listing)

Add these fields for maximum discoverability:

| Field | Purpose | Example |
|---|---|---|
| `tools.totalRegistered` | Total tool count | 78 |
| `tools.publicCount` | Public-facing tools | 24 |
| `tools.categories` | Tool grouping | `{"basin": [...], "seismic": [...]}` |
| `mcpApps.count` | Interactive UI apps | 9 |
| `mcpApps.apps` | App listing | `[{"id": "well-desk", "name": "Well Witness"}]` |
| `governance` | Constitutional framework | `{"framework": "arifOS F1-F13", "authority": "EVIDENCE_ONLY"}` |
| `federation` | Organ mesh details | `{"organs": ["arifOS :8088", ...]}` |
| `tags` / `keywords` | Search/discovery terms | `["geoscience", "mcp-server", ...]` |
| `highlight` | One-line pitch | "World's first geoscience MCP server..." |

### Epistemic discipline for server.json

- `publicCount` must match live `tools/list` — never stale
- `capabilities` must reflect what the MCP server actually declares
- `transport` must match the MCP handshake response

## Deployment Flow

### 1. Check Current State

```bash
# Does a server.json already exist?
curl -sf https://<organ>.arif-fazil.com/.well-known/mcp/server.json | jq

# What does the MCP initialize response say?
curl -sf -X POST https://<organ>.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}' | jq
```

### 2. Write server.json

Place at two locations:
- **Source:** `/root/<ORGAN>/.well-known/mcp/server.json` (committed to git)
- **Static fallback:** `/var/www/html/<organ>/.well-known/mcp/server.json`

### 3. Check Caddy Routing

GEOX (and similar subdomain configs) may explicitly proxy `/.well-known/mcp/server.json` to the MCP server:

```caddy
handle /.well-known/mcp/server.json {
    reverse_proxy 127.0.0.1:8081
}
```

**Important:** If Caddy proxies well-known to the MCP server, the Python `discovery_handler` controls the response — not the static file. Two fixes:

| Fix | Method | Risk |
|---|---|---|
| **A** | Update discovery_handler in server.py → restart service | Service restart (T3) |
| **B** | Change Caddy to serve static file → reload Caddy | Caddy reload (T3) |

Both are T3 (888_HOLD). For GEOX, the handler is at `server.py:2711` (`discovery_handler`).

### 4. Verify Public Access

```bash
curl -sf https://<organ>.arif-fazil.com/.well-known/mcp/server.json | jq '{name, version, tools: .tools.publicCount, apps: .mcpApps.count}'
```

Expected: HTTP 200, content-type application/json, all fields present.

## Registry Submission Templates

### Glama (glama.ai/mcp/servers)

**URL:** https://glama.ai/mcp/servers → "Add Server" button
**Requires:** Glama account (GitHub OAuth)

| Field | Value |
|---|---|
| Server Name | ORGAN — Tagline |
| Description | 2-3 sentence summary with tools count, categories, unique features |
| Repository URL | https://github.com/ariffazil/REPO |
| Installation | "Remote — no install needed. Connect via `https://organ.arif-fazil.com/mcp`" |
| Transport | streamable-http, sse |
| Tool Count | N public (M registered) |
| Capability Summary | One-line hook |
| Categories | Match the domain (e.g., Geoscience, Research & Data) |
| Tags | 5-7 narrow terms |

### awesome-mcp-servers (GitHub PR)

**Repo:** https://github.com/punkpeye/awesome-mcp-servers
**File:** `README.md`
**Method:** Pull Request

**Entry format:**
```markdown
### 🌍 Category Name (create if new)

- [ORGAN](https://github.com/ariffazil/REPO) — Description. Key features. Transport. N public tools.
```

**Tips:**
- Create a new category section if the domain doesn't exist (e.g., 🌍 Geoscience)
- Keep description to 1-2 lines
- Include transport and tool count
- Link directly to the repo

## Known Pitfalls

1. **Caddy proxies well-known to MCP server** — static file ignored. Must update handler or Caddy config. See Deployment Flow §3.
2. **server.json says 24 tools but handler returns 241 bytes** — check Caddy routing. The handler may be returning a hardcoded minimal response.
3. **Glama search doesn't find the server** — Glama updates periodically. May take hours/days after submission.
4. **Stale data in server.json** — `tools/list` is the runtime truth. Re-verify before submitting.

## GEOX Case Study (2026-07-19)

GEOX had a minimal 241-byte server.json from June 2026. Updated to rich 3.8KB version with:
- 24 public tools across 12 categories
- 9 MCP Apps with ui:// resource URIs
- arifOS F1-F13 governance framework
- Federation organ mesh details
- Highlight: "World's first geoscience MCP server with interactive MCP Apps"

**Unique positioning:** First geoscience MCP server in 57,000+ Glama listings. First with MCP Apps. First under constitutional governance. Zero competitors.

See `references/geox-server-json-example.md` for the full rich server.json.
