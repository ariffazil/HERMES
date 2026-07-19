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

- Arif shares external audit feedback on an essay and says "fix it"
- Editing or adding MakcikGPT articles
- Any content on arif-fazil.com needs updating
- Building and deploying the site after changes

## Site architecture

```
/root/ARIF-SITES/
├── sites/arif-fazil.com/     ← React 19 + Vite (the only site that needs build)
│   ├── src/data/essays/      ← Essay content as .ts files
│   │   ├── index.ts          ← Essay registry
│   │   ├── 02-i-have-trust-issues-with-agents.ts
│   │   ├── 06-the-first-act-of-creation-is-naming.ts
│   │   ├── 10-the-real-battle-in-ai-will-not-be-model-vs-model.ts
│   │   └── ...
│   ├── src/data/wealth/      ← Wealth/commodity dashboard data
│   └── src/data/writings/    ← Other writings
├── deploy-vps.sh             ← Deploy script
└── config/sites.json         ← Site registry
```

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

## Feedback → Fix workflow

When Arif shares external audit feedback on an essay:

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

MakcikGPT articles live under `/wealth/makcikgpt/<slug>` in the URL structure (not `/makcikgpt/<slug>`).

## Pitfalls

1. **web_extract fails on arif-fazil.com.** Tavily returns HTTP 432. Never try web_extract on this domain — go straight to browser. For bulk reads, delegate to a subagent with browser access.

2. **The `html` field is one giant template literal.** Don't try to rewrite the whole file. Use targeted find-and-replace via `patch`.

2. **Escaped quotes in HTML.** The HTML uses `\"` for quotes inside the template literal. When patching, match the escaped form.

3. **Build is required before deploy.** The site is React SPA — `deploy-vps.sh` syncs from `dist/`, not `src/`.

4. **The deploy script builds internally too.** `deploy-vps.sh` runs `npm run build` as part of its flow. You can skip the separate build step and just run deploy.

5. **Essay numbering is not sequential.** Files are numbered by creation order, not publication order. Don't assume `11-*.ts` is the 11th essay on the site.

6. **MakcikGPT articles are separate.** They live in different data structures than essays. Check `src/data/` for the right directory.

8. **MakcikGPT URL structure is nested under /wealth/.** Article URLs are `/wealth/makcikgpt/<slug>`, not `/makcikgpt/<slug>`. The listing page is at `/makcikgpt/` though.

9. **Medium cross-posted essays** have a `mediumUrl` field. Changes to arif-fazil.com don't update Medium — those are separate publications.

## See Also

- `makcikgpt-article-forging` — for creating new MakcikGPT articles (content creation, not deployment)
- `site-deployment-verification` — for verifying a deployed site against claims
- `caddy-reverse-proxy` — for routing changes (888_HOLD required)
