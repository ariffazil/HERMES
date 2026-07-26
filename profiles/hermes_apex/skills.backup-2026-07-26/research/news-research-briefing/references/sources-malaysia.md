# Malaysia News Sources — Extraction Guide

> Last verified: 2026-07-11. Re-verify if a source consistently fails.

## Source Hierarchy (by reliability for web scraping)

### Tier 1 — Always Works

| Source | URL | Strengths | Pitfalls |
|--------|-----|-----------|----------|
| **Malay Mail** | `malaymail.com` | Broad coverage, showbiz/life sections, good snapshot quality, reliable extraction | "Most Read" sidebar dominates snapshots — scroll past it. Sections: `/news/malaysia`, `/news/life` |
| **NST** | `nst.com.my` | Trending bar is gold (shows what's actually viral). Latest news carousel works well | Category pages (e.g., `/entertainment`) sometimes 404. Use homepage + trending bar |
| **The Edge Malaysia** | `theedgemalaysia.com` | Best business/financial coverage, stock tickers, sector analysis | Paywall on some articles. Homepage works well for headlines |

### Tier 2 — Usually Works

| Source | URL | Strengths | Pitfalls |
|--------|-----|-----------|----------|
| **The Star** | `thestar.com.my` | Biz7 section is excellent for economic analysis, good property/market coverage | `/business` works. `/news/nation` returns mostly sidebar/navigation — not actual articles. Try homepage if category fails |
| **Astro AWANI** | `astroawani.com/berita-malaysia` | Best BM live coverage, election night real-time results, strong breaking news. Analysis pieces (ANALISIS tags) are high quality | Category/tag pages 404 (e.g., `/tag/prn-johor-2026`). Use `/berita-malaysia` and `/berita-dunia` |
| **Utusan Malaysia** | `utusan.com.my` | Dedicated election microsites (`pru.utusan.com.my`) with structured candidate data, party seat tracking. Good BM political coverage | General homepage mixes news with lifestyle. Election microsite is the goldmine |
| **Says.com** | `says.com/my/news` | Excellent for entertainment, human drama, viral stories, social commentary. Clean extraction. Covers the "what people are actually talking about" layer | Category pages may timeout. Use `/my/news` and `/my/entertainment` directly |
| **mStar** | `mstar.com.my/hiburan` | Best entertainment/scandal/gossip source in BM. Celebrity drama, social media controversies, viral moments | BM only. Entertainment section is `/hiburan`. Lifestyle is `/gaya` |

### Tier 3 — Difficult

| Source | URL | Strengths | Pitfalls |
|--------|-----|-----------|----------|
| **Malaysiakini** | `malaysiakini.com` | Best political analysis, most trusted independent outlet | **Paywalled.** `web_extract` returns 404 on `/news` (Jul 2026). Browser works for headlines but articles are locked. Use for headline scanning only unless subscribed |
| **FMT** | `freemalaysiatoday.com` | Good breaking news ticker. **Tag feeds for named actors are excellent** (e.g., `/category/tag/zahid-hamidi`, `/category/tag/anwar-ibrahim`, `/category/tag/aminuddin-harun`) — return chronological list of all recent stories with timestamps. Use these for political research on a specific named person. Article URLs reliable via browser | `web_extract` unreliable on FMT (Tavily 432). Category pages (`/category/news/`, `/category/nation/`) often 404 — use tag feeds or homepage instead. Browser-based extraction works well; do NOT mark as "do not depend on it" — earlier verdict was over-strict. Verified Jul 2026 |
| **hMetro** | `hmetro.com.my` | Tabloid crime/drama, viral content | **Failed to load** (Jul 2026). Unreliable extraction |

## Section-Specific Source Map

### Politics
1. Malay Mail `/news/malaysia` — most complete free political coverage
2. Astro AWANI `/berita-malaysia` — BM political + live election coverage
3. Utusan Malaysia — political coverage + election microsites
4. Malaysiakini (headlines only — best political desk, paywalled)
5. NST trending bar — political signal

### Economics / Markets
1. The Edge Malaysia homepage — stock tickers, sector news
2. The Star `/business` — Biz7 analysis, property market
3. Google Finance `USD-MYR` — live ringgit rate + news sidebar
4. Malay Mail — economic headlines in main feed

### Social / Culture / Entertainment
1. **mStar `/hiburan`** — #1 for celebrity scandal, gossip, drama (BM)
2. **Says.com `/my/news`** — viral stories, human drama, social commentary (EN)
3. Malay Mail `/life` — lifestyle, culture
4. Astro AWANI — social/human interest in BM
5. NST trending bar — what's actually viral right now

### Crime / Incidents
1. Malay Mail — crime coverage in main feed
2. Says.com — viral incidents, human drama
3. Utusan — crime section under `/berita`
4. Astro AWANI — breaking incidents

## Extraction Tips

- **Google Finance** for `USD-MYR` gives live FX + MY market news sidebar — better than scraping Bursa
- **NST trending bar** is the single best signal for "what Malaysians are actually talking about"
- **Malay Mail Most Read sidebar** shows the same 10 articles across all section pages — ignore it, scroll to actual content
- **The Edge** homepage loads reliably and has stock movers at the top — useful for quick market pulse
- **Utusan election microsite** (`pru.utusan.com.my`) has structured tables with all candidates, parties, incumbents, majorities — goldmine for election coverage
- **Astro AWANI ANALISIS tags** — look for `[ANALISIS]` prefixed headlines for deeper political analysis pieces
- **mStar** entertainment articles have predictable URL pattern: `/spotlight/hiburan/YYYY/MM/DD/slug`
- **Says.com** articles are clean extraction — no paywall, no JS rendering needed
- **FMT tag feed pattern** — when researching a named politician (Zahid, Anwar, Aminuddin, Muhyiddin, Hadi, etc.), start at `freemalaysiatoday.com/category/tag/<lowercase-name-hyphenated>` to get all recent stories. Click into individual article URLs (which follow `freemalaysiatoday.com/category/malaysia/YYYY/MM/DD/slug`) for full text. Avoid category landing pages — they often 404. Verified Jul 2026.
- **Clean article text via browser_console** — when browser_snapshot returns nav-heavy clutter, run `document.querySelector('article') ? document.querySelector('article').innerText : document.body.innerText.substring(0, 8000)` in `browser_console`. Skips sidebar/footer noise, returns just the article body. Works on FMT, Malay Mail, Astro AWANI, Says.com. Verified Jul 2026.

## Known Patterns (2026-07)

- Johor state election (PRN Johor ke-16, 11 July 2026) — BN won ~49/56 seats, massive supermajority
- **Negeri Sembilan state election (PRN N. Sembilan)** — polling 1 August 2026. PH defending all 36 seats solo (first solo PH run since 1959). BN (25 seats) and PAS-led PN (11 seats) in formal electoral understanding — Zahid framed it as "political reality" and "new political recipe" for Malay-Muslim unity. Treated as GE-16 template. PH deployed heavyweight lineup (Aminuddin, Loke Siew Fook, exco veterans) — analysts framed it as "matter of life and death" for PH after Johor losses.
- US-Iran war escalation affecting Hormuz strait — oil price implications for Malaysia
- Typhoon Bavi disrupting KL-Taipei flights
- EPF Flexible Account: RM20B withdrawn by 5.5M members
- Naturalised football players citizenship scandal (EAIC report)
