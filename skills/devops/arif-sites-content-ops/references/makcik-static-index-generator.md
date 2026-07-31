# MakcikGPT Static Index Generator

## Location
`scripts/generate-makcik-index.cjs` in the arif-fazil.com site repo.

## Data flow
```
src/data/essays.json → scripts/lib/makcik-source.cjs → generate-makcik-index.cjs → public/makcikgpt-md/index.html
```

## How it works
The generator reads pieces from `getMakcikSource()` (which pulls from essays.json + per-article .md files) and produces a single `index.html` with:

1. **Server-injected data**: article list as a JS array (`const ARTICLES=[...]`) embedded directly in a `<script>` tag
2. **Client-side rendering**: JavaScript populates Latest, Series cards, and search/filter index at page load
3. **Dark Primer theme**: fully dark CSS tokens (`--bg:#0a0a0a`), NOT the cream-paper React SPA

## Key components rendered
- Topbar (HOME / /WORLD/ links + RBY dots + seal/date)
- Hero section with animated particle canvas (50 particles, RBY colours, connection lines)
- Stats row (article count, series count, seal 999, BM)
- Makcik quote block (yellow left border)
- Latest 5 articles (JS-rendered from sorted data)
- Series cards grid (5 cards, clickable filter, JS-rendered)
- Full article index with search input + filter (JS-rendered)
- Footer with RBY dots signature

## Series metadata (hardcoded in generator)
```javascript
const SERIES_META = {
  M1: { label: "Energy",             emoji: "⚡", topic: "PETRONAS, oil, gas, rightsizing" },
  M2: { label: "Governance",         emoji: "🏛", topic: "Sarawak gas, SEARAH, Bernama, sovereignty" },
  M3: { label: "Tech & Sovereignty", emoji: "🛡", topic: "YTL, ILMU, AI, monopoli" },
  M4: { label: "Economy",            emoji: "📈", topic: "Johor, daily prices, rakyat" },
  M5: { label: "Politics",           emoji: "🗳", topic: "DAP, Anwar, Loke, Sam Altman" },
};
```

## Font stack
- **Display/body:** Inter (400-900) from Google Fonts
- **Mono:** JetBrains Mono (400-700) from Google Fonts
- Note: this differs from the React SPA which uses Archivo Black + Space Grotesk

## How to modify
1. Edit the template string in `buildIndexHtml()` function
2. Run: `node scripts/generate-makcik-index.cjs` (from site root)
3. Copy to live: `cp public/makcikgpt-md/index.html /var/www/html/arif/makcikgpt-md/index.html`
4. Do NOT run `npm run build` or `deploy-site.sh` — those may overwrite from a different source

## Rewriting checklist (from 2026-07-31 session)
When rewriting the generator's HTML template:
- Keep the `getMakcikSource()` import and `buildIndexHtml(pieces)` signature
- Transform pieces into compact JS objects: `{s:"M1",d:"2026-07-30",u:"/makcikgpt/slug",t:"Title"}`
- Escape double quotes in titles: `.replace(/"/g, '\\"')`
- Embed the JS array between `const ARTICLES=[` and `];` in the template literal
- Use `${SITE_BASE}` for all URLs (defined as `https://arif-fazil.com`)
- Include `<script type="application/ld+json">` for structured data
- The `<html lang="ms">` attribute (Malay, not English)
