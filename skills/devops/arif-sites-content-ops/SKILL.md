---
name: arif-sites-content-ops
description: "Edit, build, and deploy content on arif-fazil.com (React 19 + Vite). Covers essay location, content structure, build pipeline, and the"
version: 1.2.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [site, content, essays, react, vite, deploy, arif-fazil, makcikgpt]
    category: devops
    related_skills: [makcikgpt-article-forging, site-deployment-verification, caddy-reverse-proxy]
    floors_protected: [F2, F4, F11]
    origin: 2026-07-18 essay audit feedback → fix → deploy session
---

# arifOS Sites Content Operations

Edit, build, and deploy content on arif-fazil.com. The site is React 19 + Vite, with essays stored as TypeScript data objects.

## When to use

- Arif drops an external AI audit/review (ChatGPT, Perplexity, etc.) on the site and says "fix this" or "reality verdict"
- Arif shares external audit feedback on an essay and says "fix it"
- Editing or adding MakcikGPT articles
- Editing React components (footer, header, pages) — not just essays
- Building and deploying the site after changes
- Fixing governance/canonical claims (seals, pseudo-metrics, stale version strings) that appear in the UI

## Site architecture

```
/root/arif-fazil.com/
├── sites/arif-fazil.com/     ← React 19 + Vite (the only site that needs build)
│   ├── src/
│   │   ├── pages/            ← Route-level pages (Home.tsx, Essays.tsx, Canon.tsx, etc.)
│   │   ├── components/       ← Reusable components (ConstellationFooter.tsx, ConstellationHeader.tsx, etc.)
│   │   ├── data/essays/      ← Essay content as .ts files
│   │   │   ├── index.ts      ← Essay registry
│   │   │   ├── 02-i-have-trust-issues-with-agents.ts
│   │   │   └── ...
│   │   ├── data/wealth/      ← Wealth/commodity dashboard data
│   │   ├── data/makcikgpt/   ← MakcikGPT articles
│   │   └── data/siteContent.ts ← Site-wide data (links, portfolio, organ doors)
│   └── public/               ← Static HTML pages (gas/, arifos/, etc.)
│       └── gas/index.html    ← Gas dashboard — static, not React
├── deploy-vps.sh             ← Deploy script (builds + rsyncs all sites)
└── config/sites.json         ← Site registry
```

Key files for common edits:
- **Footer:** `src/components/ConstellationFooter.tsx` — copyright, seal claims, federation links, human/machine badge separation
- **Homepage:** `src/pages/Home.tsx` — hero, organ doors, governance bridge, wells portfolio
- **Navigation:** `src/data/siteContent.ts` — primaryLinks[], organDoors[], ecosystemLinks[], arifosLinks[]

### Essay file structure

Each essay is a TypeScript object with:
```typescript
const content = {
  title: "...",
  date: "YYYY-MM-DD",
  tags: ["tag1", "tag2"],
  excerpt: `...`,
  mediumUrl: "...",  // optional, for cross-posted essays
  html: `<h3>...</h3><p>...</p>...`  // The actual content as HTML string
};
export default content;
```

**Critical:** The `html` field is a single template literal containing the full essay as HTML. Editing requires finding the exact string within this field.

## Build & deploy

```bash
# 1. Install deps if build hasn't run (--legacy-peer-deps required)
cd /root/arif-fazil.com/sites/arif-fazil.com && npm install --legacy-peer-deps

# 2. Build (also regenerates feed, sitemap, llms, makcikgpt listing)
npm run build

# 3. Deploy to VPS — manual rsync is most reliable
cd /root/arif-fazil.com

# Step A: Sync static HTML/MD files for crawlers (makcikgpt-md/)
rsync -av sites/arif-fazil.com/public/makcikgpt-md/ /var/www/html/arif/makcikgpt-md/

# Step B: Sync built dist
rsync -av sites/arif-fazil.com/dist/ /var/www/html/arif/

# Step C: Reload Caddy
sudo caddy reload --config /etc/caddy/Caddyfile

# Verify: check JS bundle hash matches
DIST_JS=$(ls -t sites/arif-fazil.com/dist/assets/*.js | head -1 | xargs basename)
LIVE_JS=$(curl -s "https://arif-fazil.com/" | grep -oP 'index-[A-Za-z0-9]+\\.js')
[ "$DIST_JS" = "$LIVE_JS" ] && echo "MATCH: $DIST_JS" || echo "MISMATCH — redeploy"
```

Build output goes to `dist/`. The dist syncs to `/var/www/html/arif/`.

### Deploy script alternative (may fail)
```bash
bash scripts/deploy-site.sh arif-fazil.com --apply
```
`deploy-vps.sh` validates registry schema and may fail if `schema_version` in
`infra/runtime-overlays.json` doesn't match. Manual rsync (steps A-C) is safest.

## Governance Fix workflow (EXTERNAL AUDIT → REALITY VERDICT → FIX)

When Arif drops an external AI's audit/review (e.g., ChatGPT "fable5" session) and says "fix this" or "reality verdict":

1. **Read the audit critically.** External AI reviews are ADVISORY ONLY — never treat as constitutional authority. Sort claims into: (a) testable (kernel bugs, deployment state, seal validity), (b) editorial opinion (structure, tone, ordering).
2. **Probe live state first.** Test every testable claim against the actual system. Kernel state via `arif_init`/`arif_judge`, live site via `curl`, source files via `search_files`.
3. **Give a reality verdict.** Structured table: what's correct, what's partially correct, what's wrong. Then offer to fix — "Nak aku patch apa-apa ke?" — don't assume, let Arif confirm.
4. **Apply only validated fixes.** Ignore wrong/outdated audit claims. Fix what's real.
5. **Build, deploy, verify.** Follow the build→deploy flow below. React SPAs cannot be verified via `curl` — `grep` the built JS bundle instead. `grep -c "expected_string" /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/*.js`. The deploy script's HTTP 200 check only confirms the shell loaded.

The "fable5" reference = external AI session identifier. Treat as second opinion, never authority.

## Feedback → Fix workflow (essay content)

1. **Identify the essay** — match the feedback's references (title, quotes, section names) to a file in `src/data/essays/`
2. **Extract the specific edits** — the audit usually names: (a) a claim to correct, (b) an argument to add/restructure, (c) a gap to fill. Map each to a specific location in the `html` string
3. **Apply via patch** — use `patch` tool with `mode=replace` to find-and-replace within the `html` template literal. For adding new sections, replace the adjacent section boundary
4. **Build** — `npm run build` to verify no syntax errors
5. **Deploy** — `cd /root/arif-fazil.com && bash scripts/deploy-site.sh arif-fazil.com --apply`
6. **Verify** — confirm HTTP 200 in deploy output

## Reading content from the site

**web_extract / Tavily is BLOCKED on arif-fazil.com** (HTTP 432). Always use the browser for reading content from this domain.

Workflow for reading/digesting published articles:

1. **Navigate to the listing page** (e.g., `/makcikgpt/`) via `browser_navigate`
2. **Extract article URLs** via `browser_console` with JS:
   ```js
   const links = document.querySelectorAll('a[href*="makcikgpt"]');
   // filter to unique article paths, skip the listing page itself
   ```
3. **Read each article** via `browser_navigate` + `browser_snapshot(full=true)`
4. For bulk digest (10+ articles), delegate to a subagent to avoid context flooding

MakcikGPT articles live under `/world/makcikgpt/<slug>` in the URL structure (not `/makcikgpt/<slug>`). The listing page is at `/makcikgpt/`.

## Pitfalls

1. **web_extract fails on arif-fazil.com.** Tavily returns HTTP 432. Never try web_extract on this domain — go straight to browser. For bulk reads, delegate to a subagent with browser access.

2. **The `html` field is one giant template literal.** Don't try to rewrite the whole file. Use targeted find-and-replace via `patch`.

3. **Escaped quotes in HTML.** The HTML uses `\\\"` for quotes inside the template literal. When patching, match the escaped form.

4. **Build is required before deploy.** The site is React SPA — `deploy-vps.sh` syncs from `dist/`, not `src/`.

5. **The deploy script builds internally too.** `bash scripts/deploy-site.sh arif-fazil.com --apply` runs `npm run build` as part of its flow. You can skip the separate build step and just run deploy. Note: `deploy-vps.sh` may fail with registry overlay errors — prefer `scripts/deploy-site.sh --apply`.

6. **npm peer dependency conflict.** The `vite-plugin-ssg@0.1.0` package requires `@vitejs/plugin-react@^4.0.0` but the project uses `^5.1.1`. If `npm install` fails with ERESOLVE, use `npm install --legacy-peer-deps`. This is a known state of the repo — don't try to resolve the conflict, just use the flag.

7. **Essay numbering is not sequential.** Files are numbered by creation order, not publication order. Don't assume `11-*.ts` is the 11th essay on the site.

8. **MakcikGPT articles are separate.** They live in different data structures than essays. Check `src/data/` for the right directory.

9. **MakcikGPT URL structure is nested under /world/.** Article URLs are `/world/makcikgpt/<slug>`, not `/wealth/makcikgpt/<slug>`. The listing page is at `/makcikgpt/`. Correct as of 2026-07-22 (routing was `/world/` not `/wealth/` per App.tsx).

10. **Medium cross-posted essays** have a `mediumUrl` field. Changes to arif-fazil.com don't update Medium — those are separate publications.

11. **React SPA = curl verification useless.** `curl https://arif-fazil.com | grep "my change"` returns nothing because React renders client-side. After deploy, verify by grepping the built JS bundle: `grep -c "expected_string" dist/assets/*.js`. The deploy script's HTTP 200 check only confirms the shell loaded.

12. **Human-machine register collision.** When editing the footer or any page that has both human narrative and machine telemetry (llms.txt, soul.json, observatory links, organ counts), always add a visual divider (border, section label like "Machine surface") between them. Never let infrastructure badges float directly under human prose.

14. **MakcikGPT articles need TWO registrations.** The article TS module and its index.ts entry control the React SPA rendering. But feed.xml, llms.txt, and sitemap.xml are generated from `src/data/essays.json` via `scripts/lib/makcik-source.cjs`. For a new article to appear in feeds: update BOTH the TS index and essays.json.

15. **Static HTML required for bot-readable MakcikGPT.** TS source alone only serves the React SPA. Bots (GPTBot, ClaudeBot, curl) read from `public/makcikgpt-md/*.html`. New article slugs need static HTML generated manually — this is NOT part of the npm build. Use the Python extraction pattern from `makcikgpt-article-forging` skill.

16. **llms.txt must be manually synced after adding pages.** The npm build does NOT reliably copy `public/llms.txt` changes to `dist/llms.txt`. After `scripts/deploy-site.sh --apply`, run: `cp sites/arif-fazil.com/public/llms.txt sites/arif-fazil.com/dist/llms.txt && rsync -av sites/arif-fazil.com/dist/llms.txt /var/www/html/arif/llms.txt`. Then verify with `curl https://arif-fazil.com/llms.txt | grep new-slug`.

17. **Caddy serves `/makcikgpt/` from `/var/www/html/arif/makcikgpt-md/`, NOT from the source `makcikgpt/index.html`.** The deploy script syncs `public/makcikgpt-md/` to this webroot directory. If you modify the source `index.html` (the React SPA shell) and run deploy, the build will regenerate the landing page from TypeScript source, wiping manual changes. To directly replace the landing page, put the file at `/var/www/html/arif/makcikgpt-md/index.html` directly — this is what Caddy serves for the `/makcikgpt/` route. See "Deploying the MakcikGPT landing page" section above for the correct workflow.

18. **React SPA client-side routing overrides standalone HTML when navigating from the homepage.** If you replace the MakcikGPT landing page with a standalone HTML file (bypassing the React build), the new design ONLY appears when users access `/makcikgpt/` directly (type URL, new tab, hard refresh). When users navigate FROM the homepage via a link (e.g., clicking "Read MakcikGPT" on the main site), the React SPA intercepts the navigation client-side and renders its built-in MakcikGPT component — which uses the old design compiled into the JS bundle. This is NOT a cache issue. **Diagnosis:** open the page in a new tab to see the static HTML; if it looks different from in-app navigation, the React component is overriding. **Fix permanently:** update the React component in `src/pages/` or `src/data/makcikgpt/` and rebuild the app via `npm run build`. This applies to any route where the React app has a client-side component AND a standalone HTML file exists at the same path.

## ABCD Framework Alignment

The Doctrine page (`/doctrine/`) is the canonical source for the ABCD framework:
- **A** = APEX Theory (four letters, grand equation, verdict lattice)
- **B** = Federation Body (9 organs, rings, roles, "Never:" rules)
- **C** = Constitution (F1–F13 floors)
- **D** = DITEMPA (sovereign compact, 000→999 pipeline)

### Zen Rule for Redundant Pages

If any page duplicates content already in ABCD, replace it with a redirect to the appropriate section. Example: `/organs/` was a static page listing 7 organs (less detail, stale tool counts). The Doctrine page already renders 9 organs with rings, roles, ports, and "Never:" rules (the B section). Fix: replace `public/organs/index.html` with:

```html
<meta http-equiv="refresh" content="0; url=/doctrine/">
<link rel="canonical" href="https://arif-fazil.com/doctrine/">
```

This preserves the URL, sets the canonical link, and sends users to the authoritative source.

**When to check:** Before adding any new standalone page, check if its content already exists within ABCD. If yes → redirect or supplement, never duplicate.

### BDX Content Architecture (MakcikGPT / civic intelligence surfaces)

| Layer | Role | Example |
|-------|------|---------|
| **B** — Body | Main article content | MakcikGPT article body |
| **D** — Discovery | Related articles, graph edges | "You may also need" |
| **X** — eXplore | Cross-domain navigation | Federation map, topic clusters |

Replaces traditional "article + sidebar + footer" with agentic content surface.

## Adding a new route-level page (not an essay)

Create a full-page dossier/landing/detail page (not a MakcikGPT article, not a data-driven essay). This is the pattern for geological dossiers, playbooks, or any standalone content page.

### Step 1: Create the page component

Create `src/pages/YourPage.tsx` with:
- `export function YourPage()` function
- `export const ssgOptions = { slug: "your-slug", routeUrl: "/earth/your-slug/" }` at the bottom
- Content structure: hero section, body sections (map over data or write inline), CTA section, footer linkback
- Use `motion.div` with framer-motion for scroll animations
- Set `document.title` and canonical link in `useEffect`
- Embed static assets (cross-section HTML, PDF) via `<iframe>` or `<a>` tags pointing to `/earth/your-asset`

```typescript
import { useEffect } from 'react';
import { motion } from 'framer-motion';

export function YourPage() {
  useEffect(() => {
    document.title = 'Your Title — Arif Fazil';
    document.querySelector('link[rel=canonical]')?.setAttribute('href','https://arif-fazil.com/earth/your-slug');
  }, []);
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-forge-black min-h-screen">
      {/* Hero section */}
      {/* Body sections */}
      {/* CTA / GEOX launch */}
    </motion.div>
  );
}
export const ssgOptions = { slug: "your-slug", routeUrl: "/earth/your-slug/" };
export default YourPage;
```

### Step 2: Wire the route

In `src/App.tsx`:
```typescript
import { YourPage } from '@/pages/YourPage';

// In the <Routes> block, add after the parent listing route:
<Route path="/earth/your-slug" element={<YourPage />} />
<Route path="/earth/your-slug/" element={<YourPage />} />
```

Always add BOTH trailing-slash and no-trailing-slash variants. Always add `/{slug}` (underscore) as well if the user might type it.

### Step 3: Link from the parent listing page

In the parent page (e.g., `Discoveries.tsx`, `Earth.tsx`), add a section BETWEEN the listing content and the CTA:

```tsx
{/* ── YOUR DOSSIER LINK ── */}
<section className="py-16 border-b border-forge-iron">
  <div className="site-frame">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div>
        <div className="section-label !mb-4">Category · Topic</div>
        <h2 className="text-4xl font-black uppercase italic mb-6">Your Title</h2>
        <p className="font-body text-forge-dim leading-relaxed mb-6">Summary text.</p>
        <a href="/earth/your-slug/" className="button-forge">Read the Dossier →</a>
      </div>
      <div className="bg-forge-steel p-6 rounded border border-forge-iron">
        <p className="font-technical text-[0.6rem] text-forge-dim uppercase mb-2">Preview</p>
        <p className="font-technical text-[0.7rem] text-forge-white">Key points...</p>
        <div className="mt-3 flex gap-2 text-[0.55rem] text-forge-dim">
          <span className="bg-forge-black px-2 py-1 rounded">Tag 1</span>
          <span className="bg-forge-black px-2 py-1 rounded">Tag 2</span>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Step 4: Add static assets under public/

Cross-section HTML, PDFs, and images go under `public/earth/`:
```
public/earth/
├── your-slug-cross-section.html    ← iframe target
└── your-slug.pdf                   ← download link
```

Static files in `public/` are served directly by Vite → dist/ → web root. Embed them in the page via:
- `<iframe src="/earth/your-cross-section.html">` for interactive cross-sections
- `<a href="/earth/your-slug.pdf">Download PDF ↓</a>` for PDFs

### Step 5: Update llms.txt for agents (MUST be manual)

The build process does NOT auto-sync `public/llms.txt` changes to `dist/llms.txt`. After adding a new page:
```bash
# 1. Edit public/llms.txt with the new URL under ## Key Pages
# 2. Build (which may copy public/ → dist/ partially, but llms.txt is NOT always refreshed)
# 3. After deploy, manually ensure dist/ has the latest:
cp sites/arif-fazil.com/public/llms.txt sites/arif-fazil.com/dist/llms.txt
rsync -av sites/arif-fazil.com/dist/llms.txt /var/www/html/arif/llms.txt
```

**Pitfall:** llms.txt in `public/` is the SOURCE. But the npm build sometimes regenerates it from a template. After deploying, ALWAYS `curl https://arif-fazil.com/llms.txt | grep your-slug` to verify. If missing, re-copy the file.

### Step 6: Build and deploy

```bash
cd /root/arif-sites && bash scripts/deploy-site.sh arif-fazil.com --apply
```

### Step 7: Verify all endpoints

```bash
echo "=== Page ==="
curl -so /dev/null -w "HTTP %{http_code} (%{size_download} bytes)\n" https://arif-fazil.com/earth/your-slug/
echo "=== Parent listing ==="
curl -so /dev/null -w "HTTP %{http_code}\n" https://arif-fazil.com/earth/
echo "=== Static asset ==="
curl -so /dev/null -w "HTTP %{http_code}\n" https://arif-fazil.com/earth/your-asset.html
echo "=== llms.txt ==="
curl -s https://arif-fazil.com/llms.txt | grep -c "your-slug"
```

### Zen Navigation Pattern

The site follows the Three-Click Rule: no page is more than 3 clicks from the root (/). When adding a new deep page:

1. **Surface it on the listing page** — every `/earth/your-slug/` needs a card/link on `/earth/`
2. **Breadcrumb via section label** — each page has a `section-label` div (e.g., "Subsurface · Basin Intelligence") showing the user "where am I"
3. **Verbs over nouns** — navigation links use action verbs (Read, Explore, Launch, Download) not just nouns (Dossier, PDF, Cross-Section)
4. **CTAs form a connected journey** — each page leads naturally to the next: `/earth/` → `Read Dossier` → `/earth/slug/` → `Download PDF` → `Launch GEOX`

The 3-second answer pattern (from AGENTS.md §14.3) applies at page level: every user should know in 3 seconds "Where am I, why should I care, what can I do next."

## Arif's Design Preferences for MakcikGPT / Civic Surfaces

These are **established preferences** for the MakcikGPT site and any civic-journalism surface on arif-fazil.com. Embed them in future designs without asking.

### Palette: Primer (red, blue, yellow)

"Primer colour" = **red, blue, yellow** — the primary colours. NOT GitHub's Primer design system.

| Role | Hex | Usage |
|------|-----|-------|
| Red | `#e0301e` | Accent, energy, call-to-action, M1 series |
| Blue | `#1f3fd4` | Secondary accent, governance, M2 series |
| Yellow | `#f2b705` | Highlight, quote accent, M3 series |
| Dark bg | `#0a0a0a` | Page background |
| Card bg | `#1a1a1a` | Card/surface backgrounds |
| Text | `#f0f0f0` | Primary text |
| Muted | `#9a9a9a` / `#666666` | Secondary/subtle text |

### Theme: Dark-only, Zen minimal

- **Black background** (`#0a0a0a`), not dark gray
- No Mondrian blocks, Sierpinski triangles, or fractal trees
- No heavy paper/texture background
- Clean cards with rounded corners (10px), subtle borders (`#2a2a2a`)
- JetBrains Mono for code/mono, Inter for body
- Subtle particle animations (not heavy canvas) — use the three Primer colours
- Search bar with dark input, muted placeholder
- Series cards: 5-column grid, each with its series colour
- Chip labels use Primer colours with 15% alpha backgrounds

### Zen rule

The MakcikGPT site is a **Decide/Learn surface** — content-first layout: hero → stats → quote → latest → series → full index with search. No decorative elements that don't serve the reading journey.

### Deploying the MakcikGPT landing page (standalone HTML)

⚠️ **CRITICAL ARCHITECTURE — DO NOT replace the source file and run deploy.** The source `sites/arif-fazil.com/makcikgpt/index.html` is the **React SPA shell** (Vite entry point), NOT a standalone landing page. The deploy script's Phase 3 regenerates `public/makcikgpt-md/index.html` from `src/data/essays.json` via `scripts/generate-makcik-index.cjs`. If you replace the source file and run deploy, the build will OVERWRITE your changes.

**The Caddyfile routes `/makcikgpt/` to `/var/www/html/arif/makcikgpt-md/index.html`** — this is the actual file being served for the landing page, NOT the source file.

#### To directly replace the landing page with a standalone HTML file (bypass React build):

```bash
# 1. Backup the current live file
cp /var/www/html/arif/makcikgpt-md/index.html /var/www/html/arif/makcikgpt-md/index.html.bak

# 2. Replace the live file directly (Caddy serves from here for /makcikgpt/)
cp /path/to/standalone.html /var/www/html/arif/makcikgpt-md/index.html

# 3. Verify
curl -s -o /dev/null -w "HTTP %{http_code} - %{size_download} bytes\n" https://arif-fazil.com/makcikgpt/
```

**⚠️ CRITICAL LIMITATION — React SPA overrides navigation from the homepage.** The standalone HTML file is only served on DIRECT page loads (new tab, URL bar, hard refresh). When a user navigates FROM the main homepage (`arif-fazil.com/`) by clicking a link to `/makcikgpt/`, the React SPA intercepts the navigation client-side and renders its built-in MakcikGPT component — which uses whatever design was compiled into the JS bundle. This means: **users who click through from the homepage will see the old design, not your standalone HTML.** Only direct access shows the new file. This is NOT a cache issue. The permanent fix is to update the React component and rebuild the app. See Pitfall #18.

#### To restore the auto-generated landing page (undo the standalone replacement):

```bash
# Re-run deploy which regenerates makcikgpt-md/index.html from TS source
cd /root/arif-fazil.com && bash scripts/deploy-site.sh arif-fazil.com --apply
```

#### To modify the auto-generated landing page STYLING (not content):

The landing page template is generated by `scripts/generate-makcik-index.cjs`. Edit the template string in that script, then rebuild. Do NOT edit `public/makcikgpt-md/index.html` directly — it's overwritten on every build.

#### Backup note

The deploy script auto-creates a backup before replacing the source file. But the LIVE file at `/var/www/html/arif/makcikgpt-md/index.html` is the one that matters — always back it up separately before making changes.

## See Also

- `makcikgpt-article-forging` — for creating new MakcikGPT articles (content creation, not deployment)
- `site-deployment-verification` — for verifying a deployed site against claims
- `caddy-reverse-proxy` — for routing changes (888_HOLD required)
- `agentic-web-surface-architecture` — graph-first methodology for building agentic web surfaces (Phase 0-10 framework)
