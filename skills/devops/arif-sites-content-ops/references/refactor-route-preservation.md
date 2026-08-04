# Federation Site Refactor Hazard — Route Preservation

When a federation agent refactors a deployed site (caddyfile, surfaces, shared routes, content hubs), some existing public paths can be silently nuked. The session that catches this is too late — the live site is already 404'ing real humans.

**Generated from 2026-08-04 audit:** Kimi's Arrow of Time refactor of arif-fazil.com claimed "Preserved: politics, makcik /:slug, oil/gas/gold" — but live verification showed:

| Route | After refactor |
|---|---|
| `/` | 200 ✅ |
| `/earth` `/economics` `/world` `/writing` `/doctrine` | 200 ✅ |
| `/missions` `/000` `/999` `/wealth-live` | 200 ✅ |
| `/politics` `/oil` `/gas` `/gold` `/malaysia` (with trailing slash) | 200 ✅ (301→200 normal Caddy behavior) |
| **`/makcik`** | **404 ❌** |
| **`/world/makcikgpt`** | **308 redirect (broken)** |

Content was physically moved `/makcik` → `/world/makcikgpt` with a Caddy redirect for `/wealth/makcikgpt` and `/economics/makcikgpt` old forms, but **no redirect for `/makcik` itself**. Kimi's "preserved" claim was untested.

## Pre-deploy verification protocol

Before sealing any site refactor:

```bash
# 1. List ALL paths that existed pre-refactor
find /var/www/html/arif/ -maxdepth 2 -name 'index.html' | sort > /tmp/pre-routes.txt

# 2. After refactor, hit each path (with and without trailing slash) on the live site
while read f; do
  path=$(echo "$f" | sed 's|/var/www/html/arif||' | sed 's|/index.html||')
  for slash in "" "/"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "https://arif-fazil.com${path}${slash}" 2>/dev/null)
    if [ "$code" != "200" ] && [ "$code" != "301" ]; then
      echo "BROKEN: ${path}${slash} → ${code}"
    fi
  done
done < /tmp/pre-routes.txt

# 3. If anything is BROKEN, either restore the path or add a redir to Caddyfile
# 4. Re-run until no BROKEN lines
```

## What to add to Caddyfile for moved routes

For any path that gets moved during refactor, add an explicit 301 redirect:

```
@old_makcik path /makcik /makcik/
redir @old_makcik /world/makcikgpt/ 301
```

The `@wealth_makcik_browser_root` and `@em` blocks for `/wealth/makcikgpt` and `/economics/makcikgpt` are good examples already in the Caddyfile — pattern to extend.

## When to verify

- After ANY surfaces.json change
- After ANY static-pages re-organization
- After ANY caddyfile rewrite
- Before claiming "preserved" in a deployment report

## Tripwires

| Pattern | Risk |
|---|---|
| Refactor moves `/X` to `/Y` without adding Caddy redirect for `/X` | Existing public paths 404 silently |
| Claim "preserved" without curl-testing each preserved path | F2 fabrication |
| Add `@handle` block before `@redir` for shared routes | Caddy sort order means route may resolve before redirect gets a chance |
| Kimi/Grok/Codex/OpenCode deploys without `make verify-pages` | Site rots when agents build without verifying |

## Reference

Original event: 2026-08-04 Arrow of Time refactor by Kimi  
Detected by: Hermes routing-deck wiring followup (not the deploy agent itself)
Live fix scope: 2 Caddy redir blocks (lines 5 each)
Reversibility: full — git revert on Caddyfile + `systemctl reload caddy`
