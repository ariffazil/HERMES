# MCP Client Ecosystem — GEOX Connectivity Research Pattern

> Discovered: 2026-07-19 | Method: Tavily 432 → GitHub API + awesome-mcp-clients

## The Problem

When researching which MCP GUI clients can connect to GEOX (`:8081/mcp` SSE), Tavily search (web_search + web_extract) returned HTTP 432 errors on all calls. Need an alternative research pipeline.

## The Pipeline (3 data sources, 0 LLM summarization)

### Source 1: awesome-mcp-clients README (canonical)

```
curl -sL "https://raw.githubusercontent.com/punkpeye/awesome-mcp-clients/main/README.md"
```

This is the most comprehensive curated list of MCP clients — 70+ entries, each with:
- GitHub link, website, license, type (Desktop/Web/CLI), platforms, pricing, language

**Why it's canonical:** Maintained by the MCP community (6,521⭐), updated regularly, each entry vetted.

### Source 2: GitHub API search (star-ranked)

```bash
curl -sL "https://api.github.com/search/repositories?q=mcp+client+OR+mcp+desktop+topic:model-context-protocol&sort=stars&per_page=40"
```

Filters for repos tagged `model-context-protocol` with client/desktop in description. Sorted by stars for priority ranking.

### Source 3: Per-repo GitHub API (individual star counts)

```bash
for repo in continuedev/continue cline/cline nanbingxyz/5ire ...; do
  curl -sL "https://api.github.com/repos/$repo" | jq '{stars: .stargazers_count, desc: .description}'
done
```

### The Critical Filter: Transport Type

GEOX uses **SSE (Server-Sent Events)** on `:8081/mcp`. Most IDE clients are **stdio-only**. The filter:

| Transport | Can connect to GEOX? |
|-----------|---------------------|
| **SSE / Streamable HTTP** | ✅ Direct URL config |
| **stdio only** | ❌ Needs proxy bridge |

### Top SSE-Native GUI Clients (2026-07-19)

| # | Client | Stars | Type | Connection |
|---|--------|-------|------|------------|
| 1 | Cherry Studio | 48,753⭐ | Desktop | Settings → MCP → Add SSE URL |
| 2 | 5ire | 5,282⭐ | Desktop | Settings → MCP Servers → SSE |
| 3 | AnythingLLM | 63,546⭐ | Desktop/Docker | Settings → Agents → MCP → Remote |
| 4 | Open WebUI | 145,935⭐ | Web self-hosted | Pipelines → MCP |
| 5 | ChatMCP | 242⭐ | Desktop | Add MCP Server → HTTP/SSE |
| 6 | EEChat | ~500⭐ | Desktop | Remote SSE connection |
| 7 | LibreChat | ~20k⭐ | Web self-hosted | librechat.yml SSE config |
| 8 | Chainlit | 12,319⭐ | Web app builder | MCP ClientSession SSE |
| 9 | LobeChat | 80,509⭐ | Web/Desktop | Plugins → MCP Server URL |
| 10 | MCPHub Desktop | 150⭐ | Desktop | Remote server discovery |

### For stdio-only clients (Claude Desktop, Cursor, Cline, Continue, Zed):

Use `mcp-stdio-proxy` — spawns as local stdio process, forwards to `http://localhost:8081/mcp`.

## GEOX Connection Templates (Top 10)

### #1 ChatGPT
Settings → Connected Apps → MCP → Add: `https://geox.arif-fazil.com/mcp`

### #2 Claude Desktop
```json
{ "mcpServers": { "geox": { "command": "npx", "args": ["-y", "@anthropic/mcp-server-sse", "--url", "https://geox.arif-fazil.com/mcp"] } } }
```

### #3 Goose
```bash
goose mcp add geox --url https://geox.arif-fazil.com/mcp
```

### #4 Cursor
```json
// .cursor/mcp.json
{ "mcpServers": { "geox": { "url": "https://geox.arif-fazil.com/mcp" } } }
```

### #5 Windsurf
Settings → MCP Servers → Add: Name=`geox`, Transport=`SSE`, URL=`https://geox.arif-fazil.com/mcp`

### #6 VS Code Copilot
```json
// .vscode/mcp.json
{ "servers": { "geox": { "type": "url", "url": "https://geox.arif-fazil.com/mcp" } } }
```

### #7 Cline
Cline → MCP Servers → Add: Name=`geox`, Type=`SSE`, URL=`https://geox.arif-fazil.com/mcp`

### #8 LibreChat
```yaml
# librechat.yaml
mcpServers:
  geox:
    url: https://geox.arif-fazil.com/mcp
    transport: sse
```

### #9 Open WebUI
Admin → MCP Connections → Add: Name=`GEOX`, URL=`https://geox.arif-fazil.com/mcp`

### #10 5ire
Settings → MCP → Add Custom: Name=`GEOX`, Type=`SSE`, URL=`https://geox.arif-fazil.com/mcp`

## GEOX MCP Apps — Killer Feature

GEOX has **ui:// MCP App resources** (interactive HTML widgets rendered INSIDE chat):

| App | Resource | Description |
|---|---|---|
| Well Desk | `ui://geox/well-desk` | Interactive well log panel |
| Basin Explorer | `ui://geox/basin-atlas` | Basin intelligence dashboard |
| Seismic Viewer | `ui://geox/seismic-viewer` | Seismic section browser |
| Map Workbench | `ui://geox/map-workbench` | MapLibre geological map |

**Only ChatGPT and Claude Desktop support MCP Apps rendering as of July 2026.** This is GEOX's unique advantage — when connected, well panels, basin maps, and seismic sections render directly inside the chat with zero external URLs.

## Testing Sequence After GEOX Fix

```
Phase 1 — Quick test: MCP Inspector or 5ire (5 min)
Phase 2 — Core test: Claude Desktop + ChatGPT MCP Apps rendering (30 min)
Phase 3 — Agentic test: Goose federation chain (GEOX→WEALTH→arifOS)
Phase 4 — Self-hosted: LibreChat + Open WebUI on af-forge VPS
Phase 5 — Production: List GEOX on glama.ai MCP registry
```

## Pitfalls

1. **GEOX currently DOWN** (2026-07-19): FastMCP v2 `**kwargs` crash. See SKILL.md pitfall 34.
2. **Tavily 432**: Don't retry — switch to GitHub API + raw README immediately.
3. **Star counts ≠ SSE support**: Many high-star clients (Cline 64k⭐, Continue 34k⭐) are stdio-only.
4. **`awesome-mcp-clients` may be stale**: Cross-reference with live GitHub API for current star counts.
