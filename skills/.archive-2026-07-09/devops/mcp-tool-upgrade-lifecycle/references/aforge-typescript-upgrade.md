# A-FORGE TypeScript MCP Tool Upgrade

**Upgrade:** `forge_fetch` — added SearxNG search mode (2026-07-08)
**Repo:** `/root/A-FORGE`
**File modified:** `src/interfaces/mcp/proxyTools.ts` (`executeFetch` + `registerFetchTools`)
**Build:** `npm run build` (tsc), `systemctl restart a-forge-mcp.service`

## Pattern: Add Alternative Input Mode to Multi-Mode Tool

`forge_fetch` originally required `url` as a mandatory parameter — it fetched pages.
The upgrade adds `query` as an alternative — when provided, it routes through self-hosted SearxNG instead of fetching a URL directly.

### What Changed

**executeFetch function signature** — made `url` optional, added `query`, `searxng_url`, `num_results`:

```typescript
async function executeFetch(params: {
  url?: string;           // was: url: string (required)
  query?: string;         // NEW — search mode trigger
  searxng_url?: string;   // NEW — SearxNG base URL
  num_results?: number;   // NEW — result count
  mode: string;
  // ... rest unchanged
})
```

**Early return pattern** — search mode at top, before SSRF/robots.txt checks:

```typescript
// ── SearxNG Search Mode ──────────────────────
if (params.query) {
  const searxngBase = (params.searxng_url || "http://localhost:8080")...
  // fetch from SearxNG JSON API, parse results, return structured output
  return text({ status: "OK", backend: "searxng", results: [...] });
}
// ── Standard URL fetch mode continues below ──
const url = params.url!;
if (!url) return text({ status: "BLOCKED", reason: "Either url or query required" }...);
```

**Zod schema** — added `query`, `searxng_url`, `num_results`; made `url` optional; added `"search"` to mode enum:

```typescript
inputSchema: z.object({
  url: z.string().url().optional().describe("..."),
  query: z.string().optional().describe("Search query..."),
  searxng_url: z.string().optional().describe("SearxNG base URL..."),
  num_results: z.number().default(10).describe("..."),
  mode: z.enum(["html", ..., "search"]).default("readable"),
  // ... rest unchanged
})
```

### Key Differences from Python FastMCP

| Aspect | Python FastMCP | A-FORGE TypeScript |
|---|---|---|
| Schema definition | Pydantic in function signature | Zod `z.object()` inline |
| Build | No build step (interpreted) | `tsc -p tsconfig.json` |
| Restart | `systemctl restart` | `systemctl restart a-forge-mcp.service` |
| Tool registration | `@mcp.tool()` decorator | `server.registerTool("name", {...}, handler)` |
| Health check | `curl :PORT/health` | `curl :7072/health` |
| Two-file problem | monolith.py + server.py wrapper | One file — `executeFetch` + `registerFetchTools` in same module |

### Backward Compatibility Check

After any param tweak that makes a required field optional, test BOTH paths:
1. **Old path still works:** `forge_fetch(url="https://example.com", mode="metadata")` → returns metadata
2. **New path works:** `forge_fetch(query="test", mode="search")` → returns search results

### SSRF/Security Note

When routing to an internal service (SearxNG on `127.0.0.1:8080`), bypass SSRF checks. In the implementation, this is achieved by placing the search mode early-return BEFORE the SSRF check block — search never reaches it.

### Deployment Checklist (A-FORGE TypeScript)

1. Edit `proxyTools.ts` — update both `executeFetch` params AND `registerFetchTools` schema
2. `npm run build` — TypeScript compile
3. `systemctl restart a-forge-mcp.service` — restart
4. `curl -s http://localhost:7072/health` — verify alive
5. Test old path + new path via MCP tool call
6. `git add -A && git commit -m "forge_fetch: add SearxNG search mode"` in `/root/A-FORGE`
