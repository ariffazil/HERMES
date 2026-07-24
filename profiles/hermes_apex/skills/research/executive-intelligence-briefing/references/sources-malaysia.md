# Malaysia News Sources — Extraction Guide

> Last verified: 2026-07-05. Re-verify if a source consistently fails.

## Source Hierarchy (by reliability for web scraping)

### Tier 1 — Always Works

| Source | URL | Strengths | Pitfalls |
|--------|-----|-----------|----------|
| **Malay Mail** | `malaymail.com` | Broad coverage, showbiz/life sections, good snapshot quality | "Most Read" sidebar dominates snapshots — scroll past it. Sections: `/malaysia`, `/life`, `/showbiz` |
| **NST** | `nst.com.my` | Trending bar is gold (shows what's actually viral). Latest news carousel works well | Category pages (e.g., `/entertainment`) sometimes 404. Use homepage + trending bar |
| **The Edge Malaysia** | `theedgemalaysia.com` | Best business/financial coverage, stock tickers, sector analysis | Paywall on some articles. Homepage works well for headlines |

### Tier 2 — Usually Works

| Source | URL | Strengths | Pitfalls |
|--------|-----|-----------|----------|
| **The Star** | `thestar.com.my` | Biz7 section is excellent for economic analysis, good property/market coverage | `/business` works. `/news/nation` may timeout. Try homepage if category fails |
| **FMT** | `freemalaysiatoday.com` | Good breaking news ticker, headline carousel works | Category pages (`/category/nation/`, `/category/business/`) return 404. Use homepage only |

### Tier 3 — Difficult

| Source | URL | Strengths | Pitfalls |
|--------|-----|-----------|----------|
| **Malaysiakini** | `malaysiakini.com` | Best political analysis, most trusted independent outlet | **Paywalled.** `web_extract` via Tavily returns 402. Browser works for headlines but articles are locked. Use for headline scanning only unless subscribed |
| **Says.com** | `says.com` | Viral/trending content, social media aggregation | Frequently times out on browser loads |

## Section-Specific Source Map

### Politics
1. Malaysiakini (headlines only — best political desk)
2. Malay Mail `/malaysia` — most complete free political coverage
3. FMT homepage — breaking news ticker
4. NST trending bar — political signal

### Economics / Markets
1. The Edge Malaysia homepage — stock tickers, sector news
2. The Star `/business` — Biz7 analysis, property market
3. Google Finance `USD-MYR` — live ringgit rate + news sidebar
4. FMT homepage — economic headlines in main feed

### Social / Culture / Entertainment
1. Malay Mail `/showbiz` — entertainment
2. Malay Mail `/life` — lifestyle, culture
3. NST trending bar — what's actually viral right now
4. FMT homepage — trending topics sidebar

## Extraction Tips

- **Google Finance** for `USD-MYR` gives live FX + MY market news sidebar — better than scraping Bursa
- **NST trending bar** is the single best signal for "what Malaysians are actually talking about"
- **Malay Mail Most Read sidebar** shows the same 10 articles across all section pages — ignore it, scroll to actual content
- **The Edge** homepage loads reliably and has stock movers at the top — useful for quick market pulse
- **Malaysiakini BM (Bahasa) section** sometimes has different/topical content not in English edition

## Extraction Techniques

### curl+grep for Headline Extraction (Fast, Bypasses Cloudflare)
When browser is slow or sites block full content loading, extract headlines directly:
```bash
# Malay Mail — works even when Cloudflare blocks article content
curl -sL "https://www.malaymail.com/news/malaysia" 2>/dev/null | grep -oP '<h2[^>]*>.*?</h2>' | sed 's/<[^>]*>//g'

# Get article URLs for deeper research
curl -sL "https://www.malaymail.com/news/malaysia" 2>/dev/null | grep -oP 'href="[^"]*malaysia[^"]*"' | head -20

# Search within page content for specific entities
curl -sL "https://www.malaymail.com/news/malaysia" 2>/dev/null | grep -i petronas | head -5
```

### Google News for Entity-Specific Searches
When you need news about a specific entity (PETRONAS, Tengku Taufik, etc.):
```
https://news.google.com/search?q=PETRONAS%20Malaysia&hl=en-MY&gl=MY&ceid=MY:en
```
Google News aggregates from all Malaysian outlets and shows relative recency. Best for:
- Named company/person searches
- Topic-specific deep dives
- Finding coverage that's spread across multiple outlets

## Known Patterns (2026-07)

- Johor state election dominating all political coverage
- "Gempar Rasuah" student protests in Sabah — emerging youth movement
- Taylor Swift × Kelce wedding dominating social/lifestyle feeds globally
- Ringgit stable ~4.07 range, Bursa targeting 1,700
