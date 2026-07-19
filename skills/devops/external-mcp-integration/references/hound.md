# Hound — External MCP Reference

> Source: https://github.com/dondai1234/master-fetch
> Package: `hound-mcp` v10.2.1
> Author: Bishesh Bhandari (dondai1234)
> License: MIT
> Installed: 2026-07-19 on af-forge + A-FLOW
> Status: Wired to Hermes + Kimi Code + OpenClaw + Claude Code + OpenCode + Gemini + Cursor

## What It Is

Hound is an MCP server that gives AI agents full web research capability — fetch, crawl, search, PDF+OCR, screenshots — from a single local process. **$0, no API keys, nothing leaves the machine.**

## 6 Tools (mcp_ prefix internally)

| Tool | What | Key Features |
|------|------|-------------|
| `mcp_smart_fetch` | Fetch any URL | HTTP first → auto-escalates to Patchright anti-detect browser. Cloudflare bypass. PDF extraction + OCR for scanned PDFs. Internet Archive auto-recovery. `focus` parameter for BM25 extraction. `actions` for page interaction. |
| `mcp_smart_crawl` | Best-first domain crawl | BFS with relevance scoring. Sitemap mode. Budget caps. Content-adaptive extraction. |
| `mcp_smart_search` | Keyless local web search | 10 backends in parallel. Neural rerank (ONNX). Cross-engine consensus. Filters: site, location, freshness. `find_similar` mode. |
| `mcp_screenshot` | Page capture | Auto-managed stealthy browser session. |
| `cache_clear` | Cache management | `all=true` wipes everything. |
| `version` | Version + update | Self-update check. |

## Why It Matters for arifOS

| Current | Hound Replaces/Augments |
|---------|------------------------|
| Brave Search MCP (single backend, API key) | 10 keyless backends, neural rerank, $0 |
| Jina Reader (rate-limited cloud) | Local fetch, no rate limits, PDF+OCR |
| Firecrawl (paid limits) | Free local crawl with archive fallback |
| No anti-bot/crawl capability | Built-in Cloudflare bypass |

## Install Commands

**Primary (pipx — isolated venv):**
```bash
pipx install hound-mcp[all]
playwright install chromium
```
Binary lands at `/root/.local/bin/hound` (pipx-managed).

**Fallback (system pip — when pipx unavailable):**
```bash
pip install --break-system-packages hound-mcp[all]
```
Binary lands at `/usr/local/bin/hound`.

## Wiring: Federation-Wide (not just Hermes)

Hound wires to multiple agent config systems simultaneously:

### 1. Create launcher script (one per agent home, shared template)
```bash
# /root/.arifos/agents/<agent>/mcp-launchers/hound.sh
#!/usr/bin/env bash
exec hound
```

### 2. Kimi Code MCP (`/root/.kimi/mcp.json`)
```json
"hound": {
  "command": "/root/.arifos/agents/kimi/mcp-launchers/hound.sh",
  "description": "Hound — sovereign keyless web research: smart_fetch, smart_search (10 backends), smart_crawl, PDF+OCR, Internet Archive recovery. $0 MIT, local."
}
```

### 3. OpenClaw MCP catalog (both af-forge + A-FLOW)
File: `/root/.openclaw/workspace/openclaw/exports/mcp-catalog-v1.json`
```json
{
  "server_id": "hound-mcp",
  "enabled": true,
  "auto_start": true,
  "display_name": "Hound — Sovereign Web Research",
  "transport": "stdio",
  "command": "hound",
  "tool_count": 6,
  "categories": ["web", "search", "fetch", "research"]
}
```

### 4. Agent AGENTS.md update
Add `hound` to the MCP servers list in each platform wrapper:
- Kimi Code AGENTS.md
- Claude Code AGENTS.md
- OpenCode AGENTS.md  
- Gemini CLI AGENTS.md
- Cursor AGENTS.md

### 5. Verify end-to-end
```python
import subprocess, json
proc = subprocess.Popen(["hound"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, ...)
# Init sequence → tools/list → call mcp_smart_fetch/mcp_smart_search
```

**Important:** Tools use `mcp_` prefix internally (e.g., `mcp_smart_fetch` not `smart_fetch`). Always probe `tools/list` to get actual names.

## Cross-VPS Deployment

1. SSH to remote: `ssh root@<REMOTE_IP>`
2. Check Python: `python3 --version` (requires >=3.11)
3. Install: `pip install --break-system-packages hound-mcp[all]`
4. Install Chromium: `playwright install chromium`
5. Verify: `hound --version`
6. Wire per-agent configs (same pattern as local)
7. Test: MCP init → `tools/list` → `mcp_smart_search`

## Self-Update
```bash
hound -u          # brick-proof update
hound --doctor    # health check
hound --rollback  # undo last update
```

## Notes
- The `[all]` extra includes `pdfplumber`, `pypdfium2`, `rapidocr`, `onnxruntime` (~500MB). Essential for PDF/OCR and neural rerank.
- Neural rerank model (`ms-marco-MiniLM-L-6-v2`, ~80MB) downloads on first use.
- Browser warms at startup, closes after 5 min idle.
- Search is 100% HTTP (no browser needed). Browser is `smart_fetch`'s alone.
- Internet Archive auto-recovery: live hard-block → Wayback Machine (`source=archive.org`).
- Tools return `mcp_` prefixed names — always probe with `tools/list` before calling.
