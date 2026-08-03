# EUREKA Architecture Extraction — arif-fazil.com → Target Site

> Proven: 2026-08-03, SyedOS site overhaul. How to analyse arif-fazil.com's
> architecture and extract reusable patterns for any other site in the federation.

## When to Use
When any user-facing site in the federation (SyedOS, sub-sites, cockpits) needs
architectural improvement — don't invent from scratch. Read arif-fazil.com's
patterns and adapt them.

## The 6 Extraction Patterns

### 1. Multi-Surface Architecture
arif-fazil.com serves different audiences from different surfaces:
- **Human:** React SPA at `/`
- **Bot:** Static HTML at `/makcikgpt-md/` (GPTBot, ClaudeBot)
- **Agent:** `llms.txt`, `status.json`, MCP endpoints

Apply: Every user-facing sub-site gets AT MINIMUM a human page + `llms.txt`.
The llms.txt contains: page index, live data endpoints, cron job schedule,
system services. One plain-text file. Zero maintenance overhead.

### 2. Mission-Based Homepage
arif-fazil.com homepage = Six Missions (Investigate / Interpret / Decide /
Build / Monitor / Remember). User lands and knows what's possible.

Apply: Break the target site's purpose into 3-5 "missions." Each mission =
one card with icon, title, live stat, and link to sub-page. This works for
ANY domain — trading, business, wellness, admin.

### 3. Graceful Degradation
arif-fazil.com React fails → static fallback shell: "The shell is taking
longer than usual. Try these server-rendered surfaces." Site stays navigable.

Apply: Every data-dependent component needs a fallback state:
- Live API down → show "↻ updating" + last known value
- Page missing → show mission cards homepage (never blank 404)
- Upload server down → show "Server tak respond" + retry button

### 4. Separate Sub-Surfaces
arif-fazil.com breaks domains into focused pages: `/earth/`, `/wealth/`,
`/gas/`, `/doctrine/`. One page = one domain. Self-contained HTML.

Apply: Never cram everything on one page. One sub-directory per domain.
Each is one `index.html` with inline CSS/JS + CDN deps. No build step.

### 5. Live Data, Not Hardcoded
arif-fazil.com data flows: cron → JSON file → JS fetch → render.
Example: `public/data/wealth/latest.json`, `ns_live_telemetry.json`.

Apply: Data NEVER embedded in HTML. HTML is a shell that fetches data:
- Gold: `fetch('https://api.gold-api.com/price/XAU')` (CORS *, no auth)
- Nasi lemak: `fetch('/data/nasi_lemak.json')` (cron-updated)
- Health: `fetch('/status.json')` (system state)

Cron jobs update the JSON. Pages auto-refresh via `setInterval(fetch, 60000)`.

### 6. Identity Anchor
arif-fazil.com tagline: "DITEMPA BUKAN DIBERI." Agents read this and know
it's a sovereign surface. Every site needs one anchor phrase.

Apply: One tagline. Short. In the target audience's language. Placed in the
hero section. This is not branding — it's identity architecture. The site
knows what it IS.

## Extraction Workflow

1. `web_extract` both source site and target site
2. Compare: what does source have that target lacks?
3. Map each gap to one of the 6 patterns above
4. Priority-sort by: [P1] live data / [P2] mission structure / [P3] identity
5. Implement: HTML files → Caddy verify → deliver report

## Anti-Patterns
- **DON'T link the sites together.** arif-fazil.com and SyedOS are separate
  sovereign surfaces. Extract patterns, not URLs.
- **DON'T copy-paste code.** Adapt the pattern to the target's design system
  (dark theme, gold accent, BM language for SyedOS).
- **DON'T over-engineer.** Self-contained HTML. CDN deps. No React/Vite/build
  step unless the site already uses one.
- **DON'T hardcode data.** Even sample/demo data should come from JS variables,
  not inline HTML. Makes the path to live data trivial later.
