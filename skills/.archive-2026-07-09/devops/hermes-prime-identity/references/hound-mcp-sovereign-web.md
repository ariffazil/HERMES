# Hound MCP — Sovereign Keyless Web Research

> Wired 2026-07-19. v10.2.1. 6 tools, 705 tests, MIT license.

## What It Replaces

| Before | After | Why |
|--------|-------|-----|
| Brave Search (single backend, API key) | Hound smart_search (10 backends, keyless, neural rerank) | Sovereign, no rate limits |
| Jina Reader (rate-limited cloud) | Hound smart_fetch (local, anti-bot, PDF+OCR) | Zero API dependency |
| Firecrawl (paid cloud crawl) | Hound smart_crawl (local, best-first, sitemap, budget) | Same-domain deep crawl |

## Install

```bash
pip install --break-system-packages hound-mcp[all]
# Playwright already installed on af-forge (v1.60.0)
hound --version  # v10.2.1
```

## Federation Wiring

**MCP launcher (all agents):** `/root/.arifos/agents/{kimi,claude,opencode,gemini,cursor}/mcp-launchers/hound.sh`
```bash
#!/usr/bin/env bash
exec hound
```

**Kimi config:** Added to `/root/.kimi/mcp.json` with brave-search retained as fallback.

**OpenClaw catalog:** Added to `/root/.openclaw/workspace/openclaw/exports/mcp-catalog-v1.json`.

## 6 Tools

| Tool | Use |
|------|-----|
| `smart_fetch` | Fetch any URL. HTTP first, auto-escalates to anti-detect browser. Bulk, PDFs+OCR, CSS selectors. |
| `smart_crawl` | Best-first same-domain crawl. Each page as markdown with `content_ok` + `page_type`. |
| `smart_search` | 10 keyless backends in parallel, neural rerank, cross-backend consensus. |
| `screenshot` | Page capture for multimodal agents. |
| `cache_clear` | Clear fetch cache. |
| `version` | Installed version + update status. |

## Self-Update

```bash
hound -u          # brick-proof self-update
hound --doctor    # health check
hound --rollback  # undo last update
```

## Why Sovereign

- Zero API keys, zero accounts, zero per-request billing
- All search backends run locally (DuckDuckGo, Brave, Mojeek, Yahoo, Yandex, Startpage, Google, Qwant, Wikipedia, Grokipedia)
- Neural rerank runs locally via ONNX (ms-marco-MiniLM-L-6-v2)
- Internet Archive auto-recovery when live sites block
- Anti-detect browser (Patchright) for Cloudflare bypass
- NEVER calls a third-party scraper service
