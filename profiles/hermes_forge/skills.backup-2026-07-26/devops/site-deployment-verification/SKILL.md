---
name: site-deployment-verification
description: "Verify a deployed website against a claimed feature/route list. Checks live HTTP status, source files, content counts, rendering, redirects, and link freshness. Works for React SPA + reverse proxy (Caddy/Nginx) stacks."
triggers:
  - "audit this deployment"
  - "verify all routes"
  - "check if everything is live"
  - "deployment verification"
  - "is this actually deployed"
  - "verify the site"
---

# Site Deployment Verification

## When to use

When someone deploys a website update and wants a real audit — not "does it 200?" but "is the content actually right?"

## Methodology (5 phases)

### Phase 1: Route HTTP verification

```bash
# Batch all claimed routes — one curl per route
for route in / /path1 /path2 /path3; do
  code=$(curl -sI -o /dev/null -w "%{http_code}" "https://DOMAIN${route}" 2>/dev/null)
  printf "%-30s %s\n" "$route" "$code"
done
```

- 200 = route exists. But does NOT prove content is real (SPA shells always 200).
- 301/302 = redirect. Verify the redirect target is correct.
- 404/500 = broken. Immediately flag.

### Phase 2: SPA content verification

HTTP 200 on an SPA means nothing — every route returns the same shell. You MUST verify:

1. **Title check** — `curl -sL URL | grep '<title>'` — all routes having the same title is expected for SPA, not a bug.
2. **Browser rendering** — actually navigate with browser tool and read the snapshot. Look for:
   - Real content text (not just nav + footer)
   - Correct page heading
   - Data-driven content (items, counts, dates)
3. **Bundle check** — verify the JS bundle contains the data:
   ```bash
   grep -c "expected_term" dist/assets/*.js
   ```

### Phase 3: Source verification

For each claimed file/artifact:

```bash
# File existence + size
for f in file1 file2 file3; do
  [ -f "$f" ] && echo "✅ $f $(wc -l < $f) lines" || echo "❌ $f MISSING"
done
```

Then verify **claimed counts vs real counts**:
- Item count: `grep -c "slug:" data/file.ts` (or proper regex)
- Thread/category breakdown: `grep -oP 'category:\s*"[^"]+"'' data/file.ts | sort | uniq -c`
- Cross-check against what the page actually displays

**Parallel data store sweep:** Don't stop at the primary data file. Check ALL data directories for overlapping content types:
```bash
# Find all data files with slug fields
find src/data -name '*.ts' -exec grep -l 'slug:' {} \;
# Count entries in each
for f in $(find src/data -name '*.ts' -exec grep -l 'slug:' {} \); do
  echo "$(grep -c 'slug:' $f) $f"
done | sort -rn
```
If multiple files define the same content type (e.g., `writings.ts` + `essays/index.ts`), report the overlap. Entries may exist in one but not the other.

**On-site vs outbound distinction:** Count entries with actual on-site content (has `html` field or inline body) separately from entries that only link externally (has `mediumUrl` or external URL but no `html`):
```bash
# Count entries with on-site content vs outbound links only
grep -c 'html:' data/file.ts    # on-site readable
grep -c 'mediumUrl:' data/file.ts  # outbound links
```
Report both: "X essays readable on-site, Y outbound links to Medium/Substack/etc."

**PITFALL: Hardcoded counts.** Search for hardcoded number strings in page components:
```bash
grep -n "[0-9]* ARTICLES\|[0-9]* ESSAYS\|[0-9]* ITEMS" src/pages/*.tsx
```
If found, check whether the count matches reality. These are the #1 source of stale deployment claims.

### Phase 4: Redirect verification

Test all legacy/redirect routes:

```bash
for pair in "/old:/new" "/old2:/new2"; do
  src="${pair%%:*}"
  expected="${pair##*:}"
  location=$(curl -sI "https://DOMAIN${src}" | grep -i "^location:" | tr -d '\r' | awk '{print $2}')
  echo "$location" | grep -q "$expected" && echo "✅ $src → $expected" || echo "❌ $src → got=$location"
done
```

**SPA redirect nuance:** React Router `<Navigate>` redirects return 200 from the server (the SPA shell), not 301. The redirect happens client-side. This is correct behavior — don't flag it as broken. Verify by checking the browser actually navigates, not by checking the HTTP status code.

### Phase 5: Link freshness audit

Check all internal links in source for stale paths:

```bash
# Extract all href values from page components
grep -oP 'href="[^"]*"' src/pages/*.tsx src/components/*.tsx | sort -u
```

Look for:
- Links to old paths that should've been updated (e.g., `/old-path/` when the new path is `/new-path/`)
- Links that rely on server-side redirects (work but add latency + depend on Caddy config)
- Broken relative links

Also check Caddyfile for consistency:
```bash
grep -n "redir\|handle\|route" /etc/caddy/Caddyfile | grep -i "claimed_route"
```

## Output format

Report as a table with verdict per item:

```
CLAIM vs REALITY
| Claim | Real | Verdict |
|-------|------|---------|
| 87 essays | 69 | ❌ inflated |
| 3 MakcikGPT articles | 14 | ❌ stale badge |
```

Plus a prioritized fix list for any issues found.

## Common pitfall patterns (React + Caddy)

1. **Hardcoded count badges** — component says "3 ARTICLES" but data has 14. Fix: use `{data.length}` not a static string.
2. **Stale internal links** — homepage links to old path `/old/` because Caddy redirects work. Fix: update the source, don't rely on redirect.
3. **SPA redirect illusion** — `<Navigate>` in React Router returns 200 from server, not 301. Don't flag as broken; verify in browser instead.
4. **Build dist staleness** — check `stat -c "%Y %y" dist/index.html` vs source timestamps. Dist should be newer than source.
5. **Caddy route precedence** — more-specific paths outrank less-specific. Check the actual Caddyfile order when routes conflict.
6. **Parallel data stores** — a site may have multiple data files for the same content type (e.g., `writings.ts` for new entries + `essays/index.ts` for legacy + `essays/generated/` for stubs). Always sweep ALL data directories, not just the primary file. Sum the classified entries and compare to the claimed total. If they don't add up, the claim is wrong.
7. **Link-directory masquerade** — entries with `mediumUrl` or external URLs inflate "content count" but have no on-site readable content. Distinguish: entries with an `html` field = on-site content. Entries with only `mediumUrl` = outbound links. Report both counts separately. "69 essays" where 60 just link to Medium is really "9 essays + 60 Medium links."
8. **Route-to-component mismatch** — in React Router, verify that detail routes (`:slug`) map to detail components, not listing components. A route like `/writings/:thread/:slug` that renders `ThreadPage` (the listing) instead of an essay detail page means clicking a card goes nowhere useful. Check `App.tsx` element bindings, not just path definitions.
9. **VAULT999 seal ID verification** — when a deployment report claims a VAULT999 seal, verify the seal ID exists via `arif_seal mode=verify` or direct API query. A seal ID that returns "Not Found" means the seal didn't land, regardless of what the receipt says.
10. **"Every surface has feature X" claims need surface-by-surface probe** (PROVEN 2026-07-19). When a deployment report claims "every site surface across the federation now features feature X", do not trust the global assertion. Probe each surface individually for a unique marker:
    ```bash
    for p in / /app1/ /app2/ /app3/ /app4/ /app5/; do
      count=$(curl -s "https://domain$p" | grep -c "<expected_marker>")
      [ "$count" -gt 0 ] && echo "  ✅ $p" || echo "  ❌ $p MISSING marker"
    done
    ```
    The marker can be any unique token — a CSS class (`class="market-map-bar"`), a meta tag, a script src. Probe ALL claimed surfaces, not a sample. Report "Y/X = Y% coverage" instead of unqualified "100%".
11. **HTML edits to deployed copies are untracked artifacts** (PROVEN 2026-07-19). When fixing HTML directly in `/var/www/html/<surface>/index.html`, the change goes live but is not in git. Source-of-truth regeneration will silently overwrite the fix on next deploy. Audit must flag this as a deployment gap, not a completed fix. Confirm via `git status /root/<source-repo>` and `ls -la /var/www/html/<surface>/index.html` — both should be tracked AND deployed consistently.
12. **Edit the right deployed copy** (PROVEN 2026-07-19). Some surfaces have multiple possible served files: e.g., `/var/www/html/well/index.html` (orphan symlinked from /root/WELL) vs `/var/www/html/well-app/index.html` (the actual one Caddy serves via `handle /well/*` → `root * /var/www/html/well-app`). Verify with `curl -sI https://arif-fazil.com/<surface>/ | grep last-modified` to see which file is actually being served, BEFORE editing. Editing the wrong copy produces "fixed but not live" phantom receipts.
13. **Asymmetric failure framing hides bugs.** (PROVEN 2026-07-19) When a report says "100% URL pass rate", check if the X represents the right sample. A claim of "100% (91/91)" might be 100% of asset file references but 0% of `.well-known` discovery files. Always split verification by category (HTML routes / static assets / discovery files / redirects) and report per-category pass rates. "100% of routes" + "0% of discovery files" = two separate findings, not "site health 100%".
