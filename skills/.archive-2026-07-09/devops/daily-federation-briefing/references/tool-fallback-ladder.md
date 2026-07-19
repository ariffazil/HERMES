# Tool Fallback Ladder for Sensorium / Briefing Tasks

**Verified: 2026-07-18** — from live sensorium session where Tavily was fully down (432 quota).

## Fallback Sequence (in order)

### 1. web_search / web_extract (Tavily backend)
Primary path. Fast. Structured. But subject to quota exhaustion.

### 2. Google News RSS via curl (when Tavily 432)

```bash
# Malaysia-focused query
curl -s --max-time 10 \
  "https://news.google.com/rss/search?q=<url-encoded-query>&hl=en-MY&gl=MY&ceid=MY:en" \
  | grep -o '<title>[^<]*</title>' \
  | sed 's/<[^>]*>//g' \
  | head -30

# For structured extraction (titles + pubDates):
curl -s --max-time 10 \
  "https://news.google.com/rss/search?q=<query>&hl=en-MY&gl=MY&ceid=MY:en" \
  | python3 -c "
import sys, re
data = sys.stdin.read()
items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
for i, item in enumerate(items[:15]):
    title = re.search(r'<title>(.*?)</title>', item)
    pub = re.search(r'<pubDate>(.*?)</pubDate>', item)
    title_text = title.group(1) if title else 'N/A'
    pub_text = pub.group(1) if pub else 'N/A'
    print(f'[{i}] {title_text[:120]}')
    print(f'    Date: {pub_text}')"
```

**Gotcha:** Some queries (geopolitics, AI-specific) may return empty RSS. Google News RSS filters by query specificity — broad queries like "Iran US conflict" may be blocked/empty while "Malaysia economy" works fine. If empty, try a different query formulation.

### 3. Browser (last resort)
`browser_navigate` to specific news portals. **Warning:** Major news sites (thestar.com.my, reuters.com) can time out at 10s+. Only use when RSS fails and the specific URL is known to be loadable.

## WEALTH MCP Data Quality Notes

### Oil Price Staleness
`capital_market(mode='commodity', commodity='brent_crude')` returns EIA estimates with source tag "EIA estimate." The EIA publishes weekly estimates that can lag live trading by days. **Always cross-verify** with news RSS headlines for the current direction. If news reports a materially different price (e.g., $86+ vs $78.50), flag as DER with explicit gap callout.

### Stress Index Silent Default
`capital_diagnose(mode='stress_index')` returns stress_index=0.0 (risk_level=GREEN) with warning "SILENT_DEFAULT_RISK" when the 16 input fields aren't populated. The 0.0 means "no data supplied," not "no stress observed." Report as UNK, never as GREEN.

## Example: Today's (2026-07-18) Failure Pattern

```
1. web_search("Malaysia PETRONAS economy...") → Tavily 432
2. web_search("geopolitics war energy...") → Tavily 432
3. web_search("AI model release agentic...") → Tavily 432
4. web_extract(["reuters.com/world/", "thestar.com.my/...", ...]) → Tavily 432
5. browser_navigate("thestar.com.my/news/nation") → timeout 10s
6. curl Google News RSS "Malaysia OR PETRONAS OR ringgit" → SUCCESS (50+ items)
7. curl Google News RSS "Iran US conflict" → EMPTY (filtered)
8. curl Google News RSS "oil price Brent crude LNG energy" → EMPTY (filtered)

Result: Malaysia section fully sourced; geopolitics + AI sections degraded (UNK).
Release status: RELEASE_WITH_HOLDS.
```
