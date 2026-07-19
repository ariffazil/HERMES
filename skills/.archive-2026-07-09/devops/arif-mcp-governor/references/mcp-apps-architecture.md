# MCP Apps Architecture — Deployment Model (2026-07-19)

> **Context:** Discovered during GEOX GUI hardening — the six MCP Apps were deployed as standalone public websites then wrapped inside another React SPA. This file documents the correct architecture.

## The Core Distinction

**MCP Apps are NOT public web pages.** They are `ui://` HTML resources rendered inside an MCP host (ChatGPT, Claude Desktop, VS Code Copilot) via sandboxed iframe. Tool calls go through the HOST bridge (postMessage), NOT direct browser→`/mcp/`.

## The Four Surfaces

| Surface | Purpose | Should Be Public? | Technology |
|---------|---------|-------------------|------------|
| **MCP App (`ui://`)** | Small HTML/JS rendered inside MCP host iframe | No — served via FastMCP `ui://` resource | Lightweight HTML, no heavy runtime |
| **Operator Cockpit (`/gui/`)** | Full human workspace in browser | Yes, but authenticated | Purpose-built adapter → GEOX tools, not raw MCP |
| **Landing Page (`/`)** | Explain GEOX to outsiders | Optional, separate | Lightweight static HTML, no Cesium/MapLibre |
| **MCP Endpoint (`/mcp`)** | Tool transport | Public ingress only if secured | Protocol transport |

## What Went Wrong (GEOX Case)

The six MCP Apps were deployed as standalone public websites + wrapped inside a React SPA. This caused:

- **Duplicated navigation** and UI layers
- **Source/deployment drift** between `/var/www/html/geox/gui/` and `/root/GEOX/` source
- **Direct browser→MCP calls** producing HTTP 406 (protocol mismatch — browser vs MCP)
- **Fake "connected" states** — MCP bridge would "call" tools but the transport wasn't wired
- **Larger attack surface** — 20MB Cesium.js loaded on a marketing page
- **Conceptual confusion** — mixing MCP App, Operator Cockpit, and Product Brochure

## Correct Architecture

```
MCP hosts (ChatGPT, Claude Desktop)
  └── ui://geox/well-desk/index.html
        └── Tool calls through HOST bridge (postMessage)

Human operator
  └── /gui/ (authenticated)
        └── Purpose-built API/session adapter
              └── GEOX canonical tools

Public visitor
  └── / (lightweight static page)
        └── No Cesium/MapLibre/MCP runtime
```

## Migration Rules

1. **MCP Apps → `ui://` resources** — Convert standalone HTML apps to FastMCP `ui://` resource handlers. Remove direct `/mcp/` fetch calls; use host bridge.
2. **`/apps/` → internal previews** — Keep `/apps/` as dev previews and documentation only, not primary public destinations.
3. **`/gui/` → single authenticated cockpit** — One operator workspace with purpose-built adapter. Session-gated.
4. **`/` → lightweight** — No heavy 3D libraries, no MCP runtime. Just facts + links.
5. **Source control** — ALL GUI files must live in the GEOX source repo (`/root/GEOX/static/`), not just in `/var/www/html/geox/`. Pre-compressed `.gz` assets belong with source.

## Verification

After migration:
- `curl https://geox.arif-fazil.com/` → < 100KB, no Cesium/MapLibre JS
- `curl https://geox.arif-fazil.com/gui/` → loads cockpit, 200 OK
- `curl -X POST https://geox.arif-fazil.com/mcp` → MCP JSON-RPC works (not HTTP 406)
- `ls /root/GEOX/static/gui/` → mirrors `/var/www/html/geox/gui/`
