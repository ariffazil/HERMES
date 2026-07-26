# arif-fazil.com Stack Reference

## Architecture

- **Source:** `/root/ARIF-SITES/sites/arif-fazil.com/`
- **Build:** Vite 7 + React 19 + React Router (SPA)
- **Deploy:** `./deploy-vps.sh` → Caddy serves from dist/
- **Reverse proxy:** Caddy 2 on VPS, Cloudflare in front
- **Canonical data:** `src/data/writings.ts` (essays), `src/data/makcikgpt/index.ts` (MakcikGPT articles)

## Key routes (as of 2026-07-18)

| Route | Source | Notes |
|-------|--------|-------|
| `/writings` | `Writings.tsx` | Landing — 3 thread cards + genesis + manifesto + MakcikGPT |
| `/writings/earth` | `ThreadPage.tsx` | Thread page — reads from `writings.ts` filtered by thread |
| `/writings/mind` | `ThreadPage.tsx` | 36 essays (post-cut) |
| `/writings/human` | `ThreadPage.tsx` | 20 essays |
| `/writings/genesis` | `Genesis.tsx` | Sovereign attestation (was at /000) |
| `/writings/manifesto` | `Manifesto.tsx` | The thesis |
| `/makcikgpt` | `MakcikGPT.tsx` | 28 civic journalism articles |
| `/000` | React Router | `<Navigate to="/writings/genesis">` |
| `/essays` | React Router | `<Navigate to="/writings">` |
| `/essays/:slug` | `EssayPage.tsx` | Legacy essay detail — renders full HTML from `essays/index.ts` |

## Parallel data stores (critical pitfall)

The site has THREE data sources for "essays" — confusing every audit:

| Data store | Entries | Content | Route |
|------------|---------|---------|-------|
| `src/data/writings.ts` | 59 | Metadata only (title, excerpt, tags, mediumUrl) | `/writings/:thread` |
| `src/data/essays/index.ts` | 70 | 23 with full on-site HTML | `/essays/:slug` |
| `src/data/essays/generated/` | 50 | Thin stubs (~400 bytes each) | unused? |

The overlap: most `writings.ts` entries have a `mediumUrl` pointing to Medium. The `essays/` directory has a different subset with actual on-site HTML content. These are NOT the same list — an essay can exist in one but not the other.

**On-site vs outbound (as of 2026-07-18):**
- 60 of 59 writings.ts entries link to Medium (no on-site content)
- 23 essays in `essays/` have full on-site HTML
- 8 entries in writings.ts are "direct publication" (isDirectPublication: true)

## Route gap (as of 2026-07-18)

`/writings/:thread/:slug` maps to `ThreadPage` (listing component), NOT an essay detail page. Clicking an essay card in the thread listing navigates to a URL that re-renders the listing. The on-site essay detail view only works via the legacy `/essays/:slug` route using `EssayPage.tsx`.

## Known pitfall spots

1. **MakcikGPT article count** — badge was hardcoded "3 ARTICLES" in `MakcikGPT.tsx`. Use `{makcikArticlesMeta.length}` instead.
2. **Homepage links** — `Home.tsx` had stale `/wealth/makcikgpt/` link. Check all `href=` values after path changes.
3. **Caddy redirect vs SPA redirect** — `/wealth/makcikgpt*` is a Caddy 301. `/000` and `/essays` are React Router `<Navigate>` (200 from server, redirect in browser). Don't confuse the two patterns.
4. **Essay count in `writings.ts`** — the page dynamically counts from data (shows "69 WRITINGS"). The forge report claimed 87 — the code was right, the claim was wrong. Always verify against source data, not against what an agent reported.
5. **Thread totals don't always sum** — when Arif says "61 total" but earth(3)+mind(36)+human(20)=59, the receipt is wrong. Always sum the thread breakdown and compare to claimed total.

## Quick verification commands

```bash
# Source location
cd /root/ARIF-SITES/sites/arif-fazil.com

# Count essays
grep -cP '^\s+slug:' src/data/writings.ts

# Count by thread
grep -oP 'thread:\s*"([^"]+)"' src/data/writings.ts | sort | uniq -c

# Count MakcikGPT articles
grep -cP '^\s+title:' src/data/makcikgpt/index.ts

# Check for hardcoded counts
grep -rn '[0-9]* ARTICLES\|[0-9]* ESSAYS' src/pages/*.tsx

# Check all internal links
grep -oP 'href="[^"]*"' src/pages/*.tsx src/components/*.tsx | sort -u

# Check dist freshness
stat -c "%Y %y" dist/index.html src/data/writings.ts

# Caddy config for site
grep -n "arif-fazil\|makcikgpt\|writings\|genesis" /etc/caddy/Caddyfile

# Parallel data store sweep
find src/data -name '*.ts' -exec grep -l 'slug:' {} \; | while read f; do
  echo "$(grep -c 'slug:' "$f") $f"
done | sort -rn

# On-site vs outbound
grep -c 'html:' src/data/essays/index.ts
grep -c 'mediumUrl:' src/data/writings.ts
```
