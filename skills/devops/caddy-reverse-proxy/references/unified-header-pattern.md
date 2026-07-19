# Unified Header Navigation Pattern

**Established:** 2026-07-16

## Problem
Multiple sites under arif-fazil.com each had different nav, different designs. User couldn't navigate between pages.

## Solution
One shared header component injected into every page via JS loader.

## Files

| File | Purpose |
|---|---|
| `/var/www/html/_shared/unified-header.html` | The nav component (HTML + CSS + JS) |
| `/var/www/html/_shared/unified-header-loader.js` | Fetches and injects the header |

## Injection (one line per page)

```html
<script src="/_shared/unified-header-loader.js" defer></script>
```

Add before `</head>` in every page. The loader fetches `unified-header.html` and inserts it at the top of `<body>`.

## Color Coding

| Section | Color | Hex |
|---|---|---|
| SOUL (Human/AAA) | Red | #FF3333 |
| MIND (arifOS) | Yellow | #FFD700 |
| BODY (A-FORGE) | Blue | #4A9EFF |
| GEOX | Teal | #00D4AA |
| WEALTH | Gold | #C9A84C |
| WELL | Green | #22C55E |
| A-FORGE | Orange | #F0883E |

## Pages with Unified Header (as of 2026-07-16)

- arif-fazil.com (main SPA — own nav, not injected)
- /wealth/gold/ ✅
- /wealth/oil/ ✅
- /makcikgpt/ → /writings/makcikgpt/ ✅
- /well/ ✅
- /geox/ ✅
- arifos.arif-fazil.com ✅
- wealth.arif-fazil.com ✅
- geox.arif-fazil.com ✅
- aaa.arif-fazil.com ❌ (needs loader added)

## Pitfalls

1. **Main SPA can't use the loader** — it's a React app with its own build. Needs special handling.
2. **Cloudflare edge cache** — changes to `_shared/` files may take 4h to propagate. Purge via CF API.
3. **Local `_shared/` copies** — some sites (arifos) have local copies that override the global. Reconcile after edits.
4. **Navigation link updates** — when adding/removing pages, update BOTH `unified-header.html` AND the Caddy routes.
