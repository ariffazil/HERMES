# Web Research Fallback Chain

**Created:** 2026-07-18
**Context:** Tavily down, all search engines CAPTCHA'd, Arif reminded about A-FORGE tools.

## Primary: A-FORGE MCP (port 7072) — ALWAYS TRY FIRST

```bash
# Search via Brave API
curl -s -X POST http://127.0.0.1:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_search","arguments":{"query":"YOUR QUERY","limit":10}}}'

# Fetch URL content
curl -s -X POST http://127.0.0.1:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_fetch_url","arguments":{"url":"https://..."}}}'

# Fetch JSON
curl -s -X POST http://127.0.0.1:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_fetch_json","arguments":{"url":"https://..."}}}'
```

## Fallback chain (in order):

1. **A-FORGE `forge_search`** — Brave API, most reliable, bypasses Tavily 432
2. **A-FORGE `forge_fetch` / `forge_fetch_url`** — direct URL fetch
3. **`web_search`** (Hermes built-in) — Tavily backend, frequently 432
4. **`web_extract`** (Hermes built-in) — Tavily backend, frequently 432
5. **`browser_navigate` + `browser_snapshot`** — SPA sites, interactive content
6. **`curl` via terminal** — last resort, headers/UA spoofing

## NEVER DO:
- Report access blocks to Arif as problems
- Ask Arif to paste content when automated tools fail
- Spend 5+ attempts on one tool before trying alternatives
- Say "Cloudflare blocked" as output

## ALWAYS DO:
- Try A-FORGE tools FIRST (they're the most reliable)
- If A-FORGE fails, try the full chain
- Only report failure after exhausting ALL tools
- Present results, not blockers

## Known working patterns:
- **arif-fazil.com SPA**: JS bundle extraction (not browser) for corpus-level work
- **bharian.com.my**: `forge_search` via Brave (indirect) — direct URL blocked by Cloudflare
- **Malaysian news sites**: `forge_search` with BM queries works well
- **Academic/legal**: `forge_fetch_url` for PDFs, `forge_search` for discovery
