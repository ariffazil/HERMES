# Browser Fallback Extraction Chain

Proven fallback paths when Tavily (web_search/web_extract) returns HTTP 432
(full backend outage — not per-call quota) or HTTP 402 (credits exhausted).

Verified: 2026-07-30 (Tavily 432 outage — entire sensorium produced via browser)

## Chain Order

```
Tavily 432/402 → browser-based extraction (this document)
```

**NEVER retry Tavily search or extract once 432 is seen.** Switch immediately.

## Market Data

| Instrument | URL | Extraction Method |
|---|---|---|
| Gold (XAU/USD) | `cnbc.com/quotes/XAU=` | browser_navigate → snapshot text (price, change, open/high/low/prev close) |
| Brent Crude | `cnbc.com/quotes/%40LCO.1` | browser_navigate → snapshot text |
| WTI Crude | `cnbc.com/quotes/%40CL.1` | browser_navigate → snapshot text |
| USD/MYR | `xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MYR` | browser_navigate → snapshot shows mid-market rate + UTC timestamp |

### CNBC quotes pages — known working fields
- Current price, change ($), change (%)
- Open, Day High, Day Low, Prev Close
- Volume and Open Interest (for futures)
- Timestamp and exchange info
- Sidebar "LATEST ON [INSTRUMENT]" with related article headlines

### CNBC quotes pages — known failures
- CNBC individual article URLs (`/2026/07/30/...`) return "Not Found" (404).
  Do NOT attempt to extract article body text via browser_navigate to a story URL.
- Workaround: read headline and context from the quotes page's "LATEST ON" sidebar,
  or from the world page's QUICK LINKS aggregation section.

## News Headlines (Malaysia)

| Source | URL | Extraction Method |
|---|---|---|
| FMT (Free Malaysia Today) | `freemalaysiatoday.com/` | browser_navigate → browser_console(expression="document.querySelectorAll('article h3').forEach(h => headlines.push(h.innerText.trim())); headlines") |

FMT returns full headline set (~30-40 stories) in the `article h3` selector.
Includes: BREAKING NEWS/JUST IN labels, category tags (BERITA, BUSINESS, WORLD),
timestamps, and a TRENDING topics bar.

### FMT — known issues
- Category pages (`/category/nation/`) return 404. Use homepage only.
- Individual article URLs may 404 (same dynamic routing issue as CNBC).

## News Headlines (Global)

| Source | URL | Extraction Method |
|---|---|---|
| CNBC World | `cnbc.com/world/?region=world` | browser_navigate → read snapshot text |

The world page includes:
- Markets banner (Asian indices, oil tab, gold tab)
- Quick Links section (topic aggregators like "U.S.-Iran tensions", "Maritime chokepoints")
- LATEST NEWS sidebar with timed article headlines (e.g. "14 MIN AGO")

## Complete Workflow (Proven 2026-07-30)

1. Detect Tavily 432 → stop all web_search/web_extract calls immediately
2. Open CNBC World page → extract Asian market indices, Quick Links topics, LATEST NEWS
3. Open XAU= quote page → extract gold price and related oil/energy headlines
4. Open @LCO.1 and @CL.1 → extract Brent and WTI crude prices
5. Open XE USD/MYR converter → extract ringgit rate
6. Open FMT homepage → extract Malaysia headlines via browser_console h3 selector
7. Synthesize briefing from headline-level data (article body unavailable)
8. Release as RELEASE_WITH_HOLDS (headline-level claims OBS, body detail UNK)

## When to Use

- Tavily 432 (full backend outage)
- Tavily 402 (quota exhausted per-call)
- WEALTH MCP unreachable AND gold-api port 3456 unreachable
- Any scenario where standard web_search/web_extract tools are unavailable

## When NOT to Use

- When Tavily and web_extract are working normally (browser is slower — use direct tools)
- When only specific individual article body text is needed (try Hound MCP smart_fetch first)
