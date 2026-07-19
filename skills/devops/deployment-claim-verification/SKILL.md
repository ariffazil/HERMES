---
name: deployment-claim-verification
description: |
  Verify deployment reports and feature claims against live system state and source data.
  Cross-reference claimed counts, route availability, redirect behavior, and data integrity
  against actual source files, live HTTP responses, and build artifacts. Catches inflated
  numbers, phantom features, and routing misrepresentations before they become scars.
  Use when Arif shares a deployment report and says "audit this", "verify these claims",
  "is this real", "check the numbers", or presents a status table with counts to validate.
triggers:
  - "audit this deployment"
  - "verify these claims"
  - "check the numbers"
  - "is this count right"
  - "audit all of these"
  - "deployment report"
  - "status table"
  - "fix deployment contract drift"
  - "P0 deployment audit"
  - "fix P0 critical items"
  - "align all surfaces to source of truth"
  - "audit WELL organ registry"
  - "audit MCP surface"
  - "check for phantom exports"
  - "verify all tools resolve"
  - "MCP registry audit"
  - "organ registry check"
---

# Deployment Claim Verification

## When to Load

When a deployment report, status table, or feature manifest includes **specific quantitative claims** (route counts, entry counts, feature counts) that need ground-truth validation. The report may be self-authored or produced by another agent — both need verification.

## Core Principle

**Claims are hypotheses until verified against source data.** A report saying "87 essays" is a CLAIM. The source file having 69 entries is an OBS. The delta (18 overclaimed) is the finding.

## Audit Pipeline

### Phase 1: Route Verification (HTTP layer)

```bash
# For each claimed route, check HTTP status
curl -so /dev/null -w "%{http_code}" https://<domain>/<route> && echo " /<route>"
```

- 200 = route serves content
- 301/302 = redirect (follow it, verify destination)
- 404 = broken claim
- **SPA caveat**: React SPAs serve 200 for ALL paths (including `/nonexistent`). The 200 proves the SPA shell loads, NOT that the route has real content.

### Phase 2: Source File Verification (data layer)

For each claimed data count, find the **actual source file** and count:

```bash
# Find the data file
find <project-root> -name "writings.ts" -o -name "articles.json" -o -name "entries.*"

# Count entries (adapt to data format)
grep -c "slug:" src/data/writings.ts
grep -c '"id":' src/data/entries.json
```

**Always count, never trust the report's number.**

### Phase 3: Cross-Reference Claims vs Source

Compare each claimed number against actual source count. Classify:

| Delta | Classification |
|-------|---------------|
| 0 | ✅ Accurate |
| ±1-2 | ⚠️ Minor drift (might be counting method) |
| ±5+ | ❌ Inflated or deflated — FIND THE SOURCE |
| Claims data in wrong file | ❌ Misattribution |

### Phase 4: Redirect Verification

Distinguish between redirect types:

| Type | HTTP | Implementation | SEO Impact |
|------|------|----------------|------------|
| Server-side (Caddy/nginx) | 301/302 with Location header | Caddyfile, nginx.conf | Crawlers follow |
| Client-side (React Router) | 200 + JS redirect | `<Navigate to="..." replace />` | Crawlers may NOT follow |

```bash
# Check if redirect is server-side or client-side
curl -sI https://domain/old-path | grep -i "location\|HTTP"
# If Location header present → server-side redirect ✅
# If 200 with HTML body → client-side (React Router) ⚠️
```

**Client-side redirects work for humans but not for crawlers/bots.** If SEO matters, server-side redirects are required.

### Phase 5: Build Freshness

```bash
stat <dist-path>/index.html | grep Modify
# Compare against claimed deployment timestamp
```

### Phase 6: SPA Content Verification

For React SPAs, curl + grep on HTML won't find essay content (it's client-rendered). Instead:

1. Check that the JS bundle loads: `curl -s <url> | grep -oP 'src="[^"]*\.js"'`
2. Verify the data file imports exist in the bundle
3. Check the data source file directly for entry counts
4. Use browser_vision for visual verification if needed

## Output Template

```
## Deployment Audit Report

### Route Verification
| Route | Claimed | Actual | Status |
|-------|---------|--------|--------|
| /path | 200 | 200 | ✅ |

### Data Integrity
| Claim | Claimed | Actual | Delta | Source File |
|-------|---------|--------|-------|-------------|
| Essay count | 87 | 69 | -18 ❌ | src/data/writings.ts |

### Redirects
| Old Path | New Path | Type | Status |
|----------|----------|------|--------|
| /old | /new | Caddy 301 | ✅ |

### Build
- Last build: <timestamp>
- Freshness: <age>

### Findings
1. [severity] Finding description
```

## MCP Organ Registry Audit

When auditing an arifOS federation organ's MCP surface (WELL, GEOX, WEALTH, etc.), use the three-layer pattern: registry self-report → independent tool calls → source code cross-check. The key insight: `@mcp.tool()` decorators in source do NOT mean a tool is on the public wire — boundary enforcement strips most of them. Only behavioral verification (Layer 2) proves a tool works.

See `references/mcp-organ-registry-audit.md` for the full pattern with exact commands, the decorator-vs-SOMATIC_TOOLS-vs-wire distinction, and the 5 pitfalls.

## MCP Contract Drift — Audit → Fix Pipeline

When an external audit finds drift between declared MCP surface and live state across multiple P0 items (tool counts, URI canonicalization, output semantics, MCP Apps bridge, build identity, CI repair, dead POC code), use the audit → fix → regenerate → startup-verify pipeline. Commit one P0 item per commit with conventional commits. Always regenerate static surface files from the live registry, never hand-edit them.

See `references/mcp-contract-drift-audit-fix.md` for the full 6-phase pipeline with exact commands, GHOST_TOOLS pattern, concurrent subagent collision handling, and startup verification recipe. Proven on GEOX P0 deployment audit 2026-07-19 (7 items).

## Pitfalls

1. **Never trust the report's numbers.** Always count from source.
2. **SPA 200 ≠ content exists.** React SPAs serve 200 for everything. Check the data layer.
3. **Client-side redirects ≠ server-side redirects.** Both "work" but only server-side is visible to crawlers.
4. **Multiple data stores.** A project may have `writings.ts` (69 entries), `essays/` (70 files), `generated/` (50 files), and `articles.json` (66 entries). Don't conflate them — find which one the report is actually counting.
5. **Legacy vs current data.** Old data files may still exist alongside new ones. Verify which is actually served by the live routes.
6. **"Every surface has feature X" claims need surface-by-surface probe, not a single global count.** (PROVEN 2026-07-19) When a deployment report claims "every site surface across the federation now features feature X", do not trust the global assertion. Probe each surface individually:
   ```bash
   for p in / /app1/ /app2/ /app3/ /app4/ /app5/; do
     count=$(curl -s "https://domain$p" | grep -c "<expected_token>")
     [ "$count" -gt 0 ] && echo "  ✅ $p" || echo "  ❌ $p MISSING token"
   done
   ```
   The token can be any unique marker of the feature — a CSS class, a meta tag, a script src. **Probe all claimed surfaces**, not just a sample. If even one is missing, the "every" claim is FALSE. Classify the count: X/Y surfaces, then report "Y/X = X% coverage" instead of the unqualified "100%".
7. **"100% pass rate" claims must specify what was tested.** (PROVEN 2026-07-19) When a report says "X/X URLs returned 200", verify:
   - Did the test include the right URLs? (asset files vs HTML surface routes vs .well-known discovery files)
   - Does X represent all claims or a subset?
   - Are there categories of failures the X/X framing hid?
   Best practice: split verification by category (HTML routes / assets / discovery / redirects) and report per-category pass rates. "100% of routes" + "0% of discovery files" = two separate findings, not "100% site health".
8. **HTML edits to `/var/www/html/` are deploy artifacts, not source.** (PROVEN 2026-07-19) Editing deployed copies (`/var/www/html/<surface>/index.html`) directly makes the change live but is untracked. Future deployments or rebuilds will overwrite without warning. After making such edits, leave a deployment receipt at `/root/forge_work/<date>/<task>-RECEIPT.md` documenting exactly which files were changed and why, AND track the source-of-truth regeneration step as a separate "TODO before next deploy" item. Don't commit untracked HTML to a "fixed" report without flagging the source gap.
9. **Static surface files (JSON/README/llms.txt) drift from live registry. Never trust them over the health endpoint.** (PROVEN 2026-07-19) server-card.json says 30 tools, health says 24, CANONICAL_PUBLIC_SURFACE.json says 36, registry says 24 — the static files are ALL stale. Always probe the health endpoint or tools/list first. Generate all static surface files from the live registry programmatically, never hand-edit them. Add startup verification that fails-closed (SystemExit) when static files disagree with registry.
10. **Concurrent subagent edits can corrupt your patches.** (PROVEN 2026-07-19) When the patch tool warns about sibling subagent modifications, re-read the file before patching. The other agent may have changed constants you depend on (e.g., GEOX_VERSION from "v2026.07.17" to "df314348"). Diff-check the file before committing.

## References

- `references/mcp-contract-drift-audit-fix.md` — Full audit → fix → regenerate → startup-verify pipeline for MCP deployment contract drift. 6 phases: survey, classify, fix (one commit per P0), regenerate surfaces from registry, add fail-closed startup verification, verify live. GHOST_TOOLS pattern, subagent collision handling, build identity recipe. Proven on GEOX P0 deployment audit 2026-07-19 (7 items).
- `references/react-spa-audit-pattern.md` — React SPA-specific audit techniques (catch-all 200 problem, client-side vs server-side redirects, multiple data store disambiguation). Proven on arif-fazil.com audit 2026-07-18.
- `references/mcp-organ-registry-audit.md` — MCP organ registry audit pattern for arifOS federation organs. Three-layer verification (self-report → behavioral → source cross-check), decorator-vs-wire distinction, boundary enforcement understanding. Proven on WELL organ audit 2026-07-18.
