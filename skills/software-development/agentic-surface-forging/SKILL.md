---
name: agentic-surface-forging
title: Agentic Dual-Surface Site Forging
description: Build websites with BOTH human-facing visual surfaces AND machine-readable agent surfaces (llms.txt, JSON-LD, MCP endpoints) so AI agents can ingest and act on the data. One system, two surfaces.
trigger: user wants a website that AI agents (ChatGPT, Claude, Gemini) can read and make recommendations from — medical tourism, e-commerce, directory, or any data-driven domain with referral/decision logic.
domain: web-development, agentic-architecture, MCP
---

# Agentic Dual-Surface Site Forging

> **Satu sistem, dua permukaan** — human nampak cantik, agent baca structured.

## 1. The Principle

Modern AI agents browse the web and read pages. But JS-heavy SPAs return zero content to agents. Marketing prose with no structured data is useless for agent decision-making.

**Solution:** Build every data-driven page with two surfaces:
1. **Human Surface** — beautiful, narrative, outcome-oriented. Mobile-first.
2. **Agent Surface** — machine-readable, structured, discoverable via llms.txt + MCP endpoints

## 2. Architecture

```
STATIC LAYER (domain invariants):
  Registry ──┬── identity/name/location
              ├── accreditations/verification
              ├── pricing (transparent ranges)
              ├── outcomes/success rates
              ├── practitioner profiles  
              └── domain-specific metadata

DYNAMIC LAYER (per-session computed):
  Matching engine → condition/solution
  Comparison engine → side-by-side
  Cost estimator → package total
  Ethics/dignity check → F6 MARUAH (if health)
```

## 3. Agent Surface Checklist

Every agentic site MUST expose:

- `llms.txt` → `/llms.txt` — AI orientation one-pager
- `agent.json` → `/.well-known/agent.json` — capabilities & governance
- `database.json` → structured domain data in JSON
- `AI_CONTEXT.md` → `/.well-known/AI_CONTEXT.md` — recommendation format & ethics
- MCP endpoint → `/mcp` (streamable-http) — live query tools
- Schema.org JSON-LD → in HTML `<script>` — search engine + agent structured data

## 4. Red Team Methodology

Before building, probe 3 competitors:

1. `curl` each → if <500 chars → JS-heavy SPA = agents blind
2. Check for `llms.txt`, `agent.json`, JSON-LD, pricing transparency
3. Rate each 0-100 on agent-readability
4. Extract what they do RIGHT (branding, journey) → keep
5. Extract what they do WRONG (hidden pricing, JS-only, no agent surface) → avoid

## 5. Caddy Deployment Pattern

```caddy
handle /subpath/* {
    uri strip_prefix /subpath      # CRITICAL — without this paths break
    root * /var/www/html/organ/subpath
    try_files {path} {path}/index.html /index.html
    file_server
}
handle /subpath { redir /subpath/ 308 }
```

**PITFALLS:**
- Never `caddy fmt --overwrite` (wipes file silently). Use `caddy validate --config` only.
- Caddy admin on Unix socket: `systemctl restart caddy` to reload (NOT `caddy reload`).
- `uri strip_prefix` REQUIRED for subpath static serving — without it, `try_files {path}` looks for `/subpath/file` inside root.
- **Route ordering with subpath + MCP conflict:** `handle /subpath/*` catches `/subpath/mcp` before the MCP proxy handler. Solution: put MCP on separate `/api/subpath/mcp` path, or ensure MCP handler is defined FIRST and uses a non-overlapping match.
- Always backup Caddyfile before editing: `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak.$(date +%Y%m%d_%H%M%S)`.
- Cloudflare proxied domains: 502 errors from Caddy may be Cloudflare retry loops, not config errors.

## 6. Live MCP Backend (The Real Agentic Surface)

Static files alone are NOT "truly agentic." A live MCP server lets AI agents query data programmatically.

### Architecture

```
Caddy proxy (/api/<domain>/mcp*) → FastMCP server (:port) → database.json
```

### FastMCP Server Pattern

```python
from fastmcp import FastMCP
mcp = FastMCP("kpj-server")
DATA_PATH = "/var/www/html/well/kpj/data/hospitals.json"

def _load_data() -> dict:
    if not os.path.exists(DATA_PATH):
        return {"hospitals": []}
    with open(DATA_PATH) as f:
        return json.load(f)

@mcp.tool()
def kpj_search_hospitals(specialty: str = None, location: str = None) -> list:
    data = _load_data()
    results = data["hospitals"]
    if specialty:
        results = [h for h in results if specialty.lower() in 
                   str(h.get("doctors", [])).lower() or 
                   specialty.lower() in str(h.get("procedures", {})).lower()]
    return results[:10]

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=18085)
```

### Tools to Expose
- `search_hospitals(specialty, location, procedure)` — filter by criteria
- `get_doctor(specialty, name, language, hospital)` — find practitioners
- `estimate_cost(treatment, hospital_id)` — price with MYR+USD conversion
- `compare(treatment, [hospital_ids])` — side-by-side table
- `visa_check(country)` — medical visa requirements
- `savings_estimate(treatment, country, hospital_id)` — % vs home country

### Caddy Proxy Pattern (subpath MCP)

```caddy
# IMPORTANT: MUST be BEFORE the static file handler for same subpath
handle /api/kpj/mcp* {
    import cors_public
    uri strip_prefix /api/kpj          # so backend sees /mcp
    reverse_proxy 127.0.0.1:18085 {
        header_up Accept "application/json, text/event-stream, */*"
    }
}
```

### Streamable-HTTP Session Handling
- FastMCP streamable-http requires `initialize` → gets `Mcp-Session-Id` → subsequent calls use it
- Real MCP clients (ChatGPT, Claude Code, OpenCode) handle this automatically
- For curl testing: send initialize first, then pass `Mcp-Session-Id` header
- `curl -H "Accept: application/json, text/event-stream, */*"` is required

## 7. Dual-Species Navigation Pattern (Route Alias + Discovery)

Every agentic surface needs THREE discovery layers:

| Layer | Format | Purpose |
|-------|--------|---------|
| **Human** | Browser nav + breadcrumb | Clickable paths for non-technical users |
| **Agent** | `llms.txt` + `sitemap.xml` | Standard crawler discovery (ChatGPT, Claude, Perplexity) |
| **Machine** | Live JSON feed | Programmatic data for scripts and dashboards |

### Route Alias Pattern

Create alias routes for common terms so agents AND humans navigate by intent:

```caddy
@vitals_path path /vitals /vitals/*
redir @vitals_path https://wealth.arif-fazil.com{uri} 301
@malaysia_path path /malaysia /malaysia/*
redir @malaysia_path https://wealth.arif-fazil.com{uri} 301
```

**Rules:**
- Use 301 redirect (not 302) — search engines propagate link equity
- Create static HTML fallback for bare paths (e.g., `/politics` without trailing slash):
  `<meta http-equiv="refresh" content="0; url=/politics/ns-election/">`
- After adding routes, ALWAYS update sitemap.xml + llms.txt + rebuild + commit

### Sitemap + llms.txt Auto-Update

After adding routes, update BOTH discovery files:

```bash
# 1. Edit sitemap.xml with new <url> block (priority 0.9-0.95 for primary)
# 2. Edit llms.txt with new section (title + description + canonical URL)
# 3. Rebuild: cd /root/arif-sites && npm run build
# 4. Commit + push
```

**Pitfall:** llms.txt and sitemap.xml are generated DURING `npm run build` from site config, not static files. Always rebuild after editing.

**Worked example:** `references/prn16-political-surface-2026-07-28.md` — PRN16 Negeri Sembilan surface with GIS map, 8 swing seat playbook, 3 WhatsApp variant templates, live telemetry JSON stream, full sitemap/llms.txt wiring.

## 8. Quality Gates

- [ ] Human page renders in browser with full JS execution
- [ ] `curl` returns ≥5KB meaningful content (no JS execution needed)
- [ ] llms.txt accessible and agent-readable (check with `curl`)
- [ ] agent.json has correct MCP endpoint URL
- [ ] database.json is valid JSON with all entities
- [ ] Schema.org JSON-LD in HTML `<script>` validates
- [ ] **REAL doctors with real names, qualifications, sub-specialties** — not placeholders
- [ ] **Focused on ONE real brand/chain** — not mixed hospital groups
- [ ] MCP server starts and responds to `tools/list` (check via initialize handshake)
- [ ] No fake/synthetic data — only verified claims
- [ ] F6 MARUAH (health domain): risk context with every recommendation

## 9. Domain Research: Finding Real Data

### Hospital Research Sources
1. **Official hospital websites** — but often JS-heavy SPA, hard to extract
2. **Health tourism aggregators**: health-tourism.com, clinicsoncall.com, medisata.com
3. **Insurance panel lists**: Prudential/BSN panel doctor PDFs
4. **Search pattern**: `"KPJ [Hospital Name] doctors [specialty]"` with year
5. **Wikipedia**: chain overview with hospital list
6. **Listed company filings**: annual/integrated reports (e.g. kpj.listedcompany.com)

### Real Doctor Name Sources
- health-tourism.com/medical-centers/ — per-hospital doctor pages
- healtha.io — doctor directories
- clinicsoncall.com — pricing + doctor lists
- myhospitalnow.com — hospital profiles
- YouTube (hospital channels) — doctor introductions

### Critical: Always Use REAL Names
- The user will reject synthetic data. "I give 15/100" was triggered by mixed random hospitals.
- Real names with qualifications (FRCS, MRCP, MRCOG, FRCR, etc.) build credibility.
- Include sub-specialty (e.g. "Interventional Cardiology" not just "Cardiology").
- Include languages spoken — critical for international patient matching.

### Domain Reference Files
- `references/medical-tourism-domain.md` — MHTC red team findings, competitor analysis, AI recommendation format, generic 5-hospital data
- `references/kpj-chain-research.md` — KPJ Healthcare chain research: 6 hospitals, 22 real doctors with qualifications, pricing benchmarks, awards
