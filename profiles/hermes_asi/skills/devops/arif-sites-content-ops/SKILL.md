---
name: arif-sites-content-ops
description: "Edit, build, and deploy content on arif-fazil.com (React 19 + Vite). Covers essay location, content structure, build pipeline, and the feedback→fix→deploy workflow. Use when Arif shares audit feedback on an essay and says 'fix it', when editing MakcikGPT articles, or when any content on arif-fazil.com needs updating."
version: 1.0.0
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
/root/ARIF-SITES/
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
# Build
cd /root/ARIF-SITES/sites/arif-fazil.com && npm run build

# Deploy to VPS
cd /root/ARIF-SITES && ./deploy-vps.sh --site arif-fazil.com
```

Build output goes to `dist/`. Deploy syncs to `/var/www/html/arif/` and checks HTTP 200.

## Governance Fix workflow (EXTERNAL AUDIT → REALITY VERDICT → FIX)

When Arif drops an external AI's audit/review (e.g., ChatGPT "fable5" session) and says "fix this" or "reality verdict":

1. **Read the audit critically.** External AI reviews are ADVISORY ONLY — never treat as constitutional authority. Sort claims into: (a) testable (kernel bugs, deployment state, seal validity), (b) editorial opinion (structure, tone, ordering).
2. **Probe live state first.** Test every testable claim against the actual system. Kernel state via `arif_init`/`arif_judge`, live site via `curl`, source files via `search_files`.
3. **Give a reality verdict.** Structured table: what's correct, what's partially correct, what's wrong. Then offer to fix — "Nak aku patch apa-apa ke?" — don't assume, let Arif confirm.
4. **Apply only validated fixes.** Ignore wrong/outdated audit claims. Fix what's real.
5. **Build, deploy, verify.** Follow the build→deploy flow below. React SPAs cannot be verified via `curl` — `grep` the built JS bundle instead.

The "fable5" reference = external AI session identifier. Treat as second opinion, never authority.

## Feedback → Fix workflow (essay content)

1. **Identify the essay** — match the feedback's references (title, quotes, section names) to a file in `src/data/essays/`
2. **Extract the specific edits** — the audit usually names: (a) a claim to correct, (b) an argument to add/restructure, (c) a gap to fill. Map each to a specific location in the `html` string
3. **Apply via patch** — use `patch` tool with `mode=replace` to find-and-replace within the `html` template literal. For adding new sections, replace the adjacent section boundary
4. **Build** — `npm run build` to verify no syntax errors
5. **Deploy** — `./deploy-vps.sh --site arif-fazil.com`
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

5. **The deploy script builds internally too.** `deploy-vps.sh` runs `npm run build` as part of its flow. You can skip the separate build step and just run deploy.

6. **npm peer dependency conflict.** The `vite-plugin-ssg@0.1.0` package requires `@vitejs/plugin-react@^4.0.0` but the project uses `^5.1.1`. If `npm install` fails with ERESOLVE, use `npm install --legacy-peer-deps`. This is a known state of the repo — don't try to resolve the conflict, just use the flag.

7. **Essay numbering is not sequential.** Files are numbered by creation order, not publication order. Don't assume `11-*.ts` is the 11th essay on the site.

8. **MakcikGPT articles are separate.** They live in different data structures than essays. Check `src/data/` for the right directory.

9. **MakcikGPT URL structure is nested under /world/.** Article URLs are `/world/makcikgpt/<slug>`, not `/wealth/makcikgpt/<slug>`. The listing page is at `/makcikgpt/`. Correct as of 2026-07-22 (routing was `/world/` not `/wealth/` per App.tsx).

10. **Medium cross-posted essays** have a `mediumUrl` field. Changes to arif-fazil.com don't update Medium — those are separate publications.

11. **React SPA = curl verification useless.** `curl https://arif-fazil.com | grep "my change"` returns nothing because React renders client-side. After deploy, verify by grepping the built JS bundle: `grep -c "expected_string" dist/assets/*.js`. The deploy script's HTTP 200 check only confirms the shell loaded.

12. **Human-machine register collision.** When editing the footer or any page that has both human narrative and machine telemetry (llms.txt, soul.json, observatory links, organ counts), always add a visual divider (border, section label like "Machine surface") between them. Never let infrastructure badges float directly under human prose.

13. **Static HTML pages deployed separately.** Pages under `public/` (e.g., `public/gas/index.html`) are copied by `scripts/copy-static-html.js` during postbuild. They sync to the webroot via rsync like the React build. Changes to these files need the full build→deploy cycle.

## See Also

- `makcikgpt-article-forging` — for creating new MakcikGPT articles (content creation, not deployment)
- `site-deployment-verification` — for verifying a deployed site against claims
- `caddy-reverse-proxy` — for routing changes (888_HOLD required)
