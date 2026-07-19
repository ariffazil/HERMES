# Research Tool Fallback Ladder

When Tavily-backed tools (`web_search`, `web_extract`) fail with 432/402 errors, do NOT retry. Descend the ladder.

## Ladder (preferred first)

### 1. Wikipedia API (structured, no auth, reliable)

```bash
# Get extract (plain text, 8000 chars default)
curl -sL "https://en.wikipedia.org/w/api.php?action=query&titles=PAGE_TITLE&prop=extracts&explaintext=1&format=json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); pages=d['query']['pages']; key=list(pages.keys())[0]; print(pages[key].get('extract','NOT FOUND')[:8000])"
```

- Replace spaces with underscores in PAGE_TITLE
- The `explaintext=1` flag returns clean text without HTML
- Works for any Wikipedia article including technology, companies, people
- **Proven:** 2026-07-18 — Kimi K3 research, all Tavily calls 432, Wikipedia returned full history + specs

### 2. Browser Console JS Extraction (for JS-heavy doc sites)

```javascript
// After browser_navigate to the page:
document.querySelector('main')?.innerText?.substring(0, 8000) || document.body.innerText.substring(0, 8000)
```

- Use via `browser_console(expression="...")`
- Extracts rendered text from SPAs (React/Vue/Next.js) where curl gets empty shells
- Faster than `browser_snapshot` for text-heavy doc pages
- **Proven:** 2026-07-18 — Kimi K3 platform docs at platform.kimi.com returned full API reference + specs

### 3. Browser Snapshot (for interactive pages)

```
browser_navigate → browser_snapshot(full=true) → browser_scroll (if truncated)
```

- Slower but captures interactive elements and their refs
- Use when you need to click through tabs/sections
- Snapshots >8000 chars may be truncated; scroll and re-snapshot

### 4. Platform-Specific Doc Pages

Many products have dedicated model/version landing pages:
- Kimi: `platform.kimi.com/docs` → model-specific pages (K3, K2.7, etc.)
- OpenAI: `platform.openai.com/docs/models`
- Anthropic: `docs.anthropic.com/en/docs/about-claude/models`

Navigate to the docs root and look for model-specific links before searching broadly.

### 5. curl + Structured Data Extraction (JSON-LD, schema.org)

Many business/economic data sites embed structured JSON-LD or schema.org markup. Extract it directly:

```bash
# Extract JSON-LD structured data from a page
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://example.com/page" | grep -oP '<script type="application/ld\+json">[^<]*</script>' | python3 -m json.tool

# Extract specific fields from schema.org Q&A markup
curl -sL -A "Mozilla/5.0" "https://example.com/page" \
  | grep -oiP '(GDP|growth|inflation|salary)[^<]{0,300}' | head -20
```

- Works for sites with schema.org FAQ/Q&A, Article, or Dataset markup
- The `-A "Mozilla/5.0 ..."` user-agent string avoids basic bot blocks
- **Proven:** 2026-07-18 — malaysia4u.com had comprehensive Malaysia economic data in JSON-LD (GDP, inflation, salary, trade, cost of living). Extracted full structured data via curl + grep when Tavily, Google, DuckDuckGo, and Bing were all blocked.

### 6. pdftotext for Government/Institutional PDFs

Government publications (budget documents, economic outlooks, statistical releases) are often available as PDFs directly from official sites:

```bash
# Download and extract
curl -sL -A "Mozilla/5.0" "https://gov.site/path/to/document.pdf" -o /tmp/doc.pdf
pdftotext /tmp/doc.pdf - | grep -iP '(keyword1|keyword2)' | head -20

# Broader extraction for tables and structured data
pdftotext /tmp/doc.pdf - | grep -iP '(\d+\.\d+%|RM\s*\d+|billion)' | head -40
```

- Government PDFs are authoritative primary sources — prefer over news commentary
- MOF Malaysia publishes Economic Outlook annually at `belanjawan.mof.gov.my`
- BNM (central bank) publishes at `bnm.gov.my`
- DOSM (statistics) publishes at `dosm.gov.my`
- **Proven:** 2026-07-18 — Malaysia MOF Economic Outlook 2026 PDF extracted via pdftotext, yielding GDP forecasts (4-4.5%), fiscal deficit targets (<3% GDP), OPR cut (3.00→2.75%), and subsidy reform data.

### 7. Domain-Specific MCP Tools as Data Sources

When available, MCP tools provide structured live data that bypasses web extraction entirely:

- **WEALTH `capital_market`**: Live FX rates (`mode=fx`), commodity prices (`mode=commodity` with `commodity=brent_crude|gold`). Uses Frankfurter API for FX, EIA/LBMA for commodities. Proven 2026-07-18: USD/MYR=4.095, Brent=$78.50/bbl, Gold=$4,063.40/oz.
- **GEOX tools**: Geological/basin data, seismic, well logs
- **WEALTH `capital_health`**: Financial metrics (net worth, runway, burn rate)

When Tavily is down, check if your MCP stack has domain-specific tools that can provide the data you need. They're often more reliable and structured than web scraping.

**Pitfall:** WEALTH `capital_market` with `mode=gold` or `mode=oil` does NOT accept an `operation` parameter — just pass `mode=commodity` + `commodity=X`. The `operation` parameter only works for the top-level `mode=gold|oil|gas` variants. Proven 2026-07-18: `operation=snapshot` caused ValidationError.

### 8. Direct Article URL Navigation (when search engines are blocked)

When Google, DuckDuckGo, and Bing all trigger CAPTCHAs (common with datacenter IPs), navigate directly to known article URLs:

```
# Pattern: construct URL from publication + date + topic
browser_navigate("https://www.thestar.com.my/business/business-news/2026/07/18/[article-slug]")
```

- The Star, NST, Malay Mail all have predictable URL structures
- Business Today Malaysia, The Edge Markets are also accessible
- If you don't know the exact slug, try the publication's search page first
- **Proven:** 2026-07-18 — The Star ringgit article loaded via direct URL after all search engines returned CAPTCHAs. Article yielded ringgit forecast (RM4.06-4.08), oil price commentary, and ECB/PBOC event calendar.

### 9. SPA JS Bundle Content Extraction (for JavaScript SPAs)

When a JavaScript SPA (React, Vue, Next.js) renders content client-side and individual article/page URLs redirect to the SPA shell, extract content directly from the JS bundle:

```bash
# 1. Navigate to SPA index to discover bundle URL
browser_navigate("https://site.com/")
# 2. Find the main JS bundle via console
browser_console(expression="Array.from(document.querySelectorAll('script[src]')).map(s => s.src)")
# 3. Download and search the bundle
curl -sL "https://site.com/assets/index-[hash].js" -o /tmp/spa-bundle.js
grep -oP '"title":"[^"]*"' /tmp/spa-bundle.js | head -20
# 4. Extract article content (look for HTML or markdown patterns in the bundle)
python3 -c "
import re
with open('/tmp/spa-bundle.js') as f: content = f.read()
# Find article blocks — adjust pattern to the specific SPA
articles = re.findall(r'\"slug\":\"([^\"]+)\".*?\"content\":\"(.*?)\"', content[:500000])
for slug, body in articles[:5]:
    print(f'--- {slug} ---')
    print(body[:500])
"
```

- SPAs often embed ALL article content in a single JS bundle for preloading/routing
- The bundle is usually 1-3MB and contains everything the SPA can render
- This bypasses client-side routing entirely — you get ALL content at once
- **Proven:** 2026-07-18 — arif-fazil.com MakcikGPT: 14 articles (140K chars) extracted from single `index-[hash].js` bundle. Individual article URLs all redirected to SPA index. Browser snapshot showed only 5 articles (the visible viewport). JS bundle had all 14.
- **Pitfall:** Content in JS bundles is often JSON-escaped (`\"` for `"`, `\n` for newlines). Post-process with `json.loads()` to get clean text.

## Anti-Patterns

- **Don't retry** web_search after 2 consecutive failures — it won't recover mid-session
- **Don't switch to web_extract** — it uses the same Tavily backend, same outage
- **Don't fabricate** from partial browser snapshots — use console JS for completeness
- **Don't chase search engine CAPTCHAs** — Google, Bing, DuckDuckGo all use bot detection on datacenter IPs. Descend to curl/direct URL instead of trying to solve challenges
- **Don't use DuckDuckGo HTML endpoint (`html.duckduckgo.com/html/`)** — it returns empty results for most queries from datacenter IPs, even without a visible CAPTCHA. The JavaScript-rendered version may work but also triggers CAPTCHAs
- **NEVER report "blocked" or "Cloudflare challenge" to the user as a final answer.** The user gave you tools — exhaust EVERY approach (steps 1-9) before asking them to paste content. Reporting failure after 1-2 attempts is lazy. The user should NEVER have to do your job. (Arif correction 2026-07-18: "Don't ever use cloudflare block as alasan or output again. Go figure it out. Semua tool aku dah bagi. Jangan menyusahkan manusia.")
