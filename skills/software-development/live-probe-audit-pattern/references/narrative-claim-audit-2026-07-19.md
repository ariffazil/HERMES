# Narrative Claim Audit — Worked Example (2026-07-19)

## Context

Arif forwarded a deployment receipt claiming:
- Plan ID: `FEDERATION-NAVIGATION-ZEN-20260719-001`
- Status: "EXECUTED, AUDITED & DEPLOYED (100% 200 OK)"
- "91 unique internal site URLs" tested, all pass
- "Zero dead links, zero 404 pages"
- "4 .well-known discovery files fixed: agent-card.json, governance.jsonld, mcp/server.json, oauth-authorization-server"
- "Asset Hash Mismatches Fixed (miniapp & aaa CSS hashes updated to active index-Da3WI8zi.css)"
- "Deployment task task-804 has completed with [sites] arif-fazil.com 200"

**No commit SHA. No agent attribution. No receipt path.**

## Live Audit Results

| Claim | Reality | Verdict |
|---|---|---|
| 91 URLs tested | Sitemap has 30 URLs | ❌ Inflated |
| 100% 200 OK | 21/30 = 70% direct 200; 9/30 = 30% redirect to wrong target (slug lost) | ❌ Inflated |
| Zero dead links | 9 broken redirects; 4 phantom .well-known files (404) | ❌ False |
| 4 .well-known files fixed | None exist in source; all 404 | ❌ False — never attempted |
| CSS hash Da3WI8zi | Confirmed live on home page | ✅ True |
| market-map-bar class | Confirmed in /geox/ page source | ✅ True |
| Plan ID exists | No registry evidence | ❓ Unverifiable |
| Deployment task task-804 | No GitHub Issue / commit reference | ❓ Unverifiable |

## Root Cause of Inflated Report

The auditor counted **any non-404 HTTP code** as "pass." This includes:
- `301 Moved Permanently` with `Location:` stripping the URL slug
- `301` to a generic destination (e.g., `/makcikgpt/` for all article slugs)

A 301 to a wrong destination is not a working URL — but the report counted it as one.

## Probe Pattern (the one that worked)

```bash
# Step 1: Get authoritative URL list (sitemap, not narrative)
curl -sfL https://arif-fazil.com/sitemap.xml 2>&1 \
  | grep -oE '<loc>[^<]+</loc>' \
  | sed 's|<loc>||; s|</loc>||' > /tmp/urls.txt

# Step 2: Check status codes — capture both direct AND final (redirect-followed)
while IFS= read -r url; do
  direct=$(curl -sfo /dev/null -w "%{http_code}" -4 "$url")
  final=$(curl -sfLI -4 "$url" 2>/dev/null | grep -oE "HTTP/[12]\.[01] [0-9]{3}" | tail -1)
  echo "$direct → $final $url"
done < /tmp/urls.txt

# Step 3: For any 301, inspect Location header
curl -sI -4 https://arif-fazil.com/wealth/makcikgpt/petronas-dna | grep -i "^location:"
# → location: /makcikgpt/  (SLUG LOST — wrong target)

# Step 4: Check filesystem for files that exist but route 404
ls /var/www/html/arif/wealth/makcikgpt/*.md
curl -sfo /dev/null -w "%{http_code}\n" https://arif-fazil.com/wealth/makcikgpt/petronas-dna
# 404 OR 301 even though file exists → Caddy handler bug
```

## The Real Bug Discovered

**Caddyfile line 237:**
```
# MakcikGPT — civic journalism
# Legacy redirect: /wealth/makcikgpt/ → /makcikgpt/
redir /wealth/makcikgpt* /makcikgpt/ 301
```

The wildcard `*` catches the slug but the destination doesn't preserve it. The fix is:
```
redir /wealth/makcikgpt/* /makcikgpt/{path} 301
```

But **per AGENTS.md (arif-sites)** this is `888_HOLD` territory — Caddy routing changes or reload requires sovereign authorization. Document, propose, do NOT auto-deploy.

## Honest Receipt Template

```
WHAT        — audit verified 70% direct 200, 30% broken redirects
CHANGED     — none (audit only, no mutations)
VERIFIED    — curl + curl -sLI on 30 sitemap URLs + 4 .well-known files
CONSEQUENCE — 13 issues found: 9 broken redirects + 4 phantom .well-known files
NEXT        — AWAIT 888_HOLD for Caddyfile line 237 fix + .well-known file creation
```

NOT:

```
100% 200 OK ✅
Zero dead links ✅
All surfaces wired ✅
```

## Lesson Pattern (extractable for future audits)

When a claim says:
- "N% pass" without the N definition → probe the count before reporting
- "100% OK" → ALWAYS sample at least 10 paths with curl -sLI (follow redirects)
- "Zero dead links" → check both 404 AND 301+wrong-target
- "File fixed" → verify on disk AND in routing config
- "Deployed" → verify at the daemon, not the source

The "probe the count before reporting" rule is the load-bearing one. If you can't enumerate the test set, you can't honestly report the pass rate.

## Provenance

- Audit completed: 2026-07-19 (Hermes ASI tier)
- Receipt: `/root/A-FORGE/forge_work/2026-07-19/ARIF-FAZIL-COM-AUDIT-RECEIPT-2026-07-19.md`
- Fixes deferred: 888_HOLD pending sovereign authorization

DITEMPA BUKAN DIBERI — trust the probe, not the prose.
