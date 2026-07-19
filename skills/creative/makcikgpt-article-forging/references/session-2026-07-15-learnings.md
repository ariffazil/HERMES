# Session 2026-07-15/16 — Key Learnings

## 1. "Fix All" = Execute All, Don't Ask Per-Item

When Arif says "Fix all" or "Fix it" or "Jalan terus," execute ALL identified fixes immediately without asking for confirmation on each one.

## 2. 13-Article Audit Pattern

When Arif says "review all articles" or "audit this," run a systematic multi-article audit:
1. Extract key factual claims per article
2. Verify numbers against primary sources (3+ searches minimum)
3. Check voice quality (BM kampung? or too modern?)
4. Check rasa (ada jiwa? or just data?)
5. Produce pass/fail/needs-review table

## 3. Rasa Rewrite Pattern

When an article has correct data but no soul, add a specific human who bears the consequence. Formula: replace institutional language with a human story. Rasa is not replacing data with emotion — it's wrapping data in a human face so the reader FEELS the consequence.

## 4. Gödel Lock Now LIVE in Kernel

Enforcement code: `/opt/arifos/arifosmcp/runtime/godel_lock_enforcement.py`
Wired into: `_akal_wrap_judge` in `server.py`
Tiered Φ_external: observation=1.0, reasoning=1.0, consequential=0.7, seal_bound=0.5
Anti-Calhoun gate: HARD enforcement (min 0.60 score)

## 5. Infrastructure Audit: Edge + Origin Dual Probe

Browser-only audit misses infrastructure failures. Always probe specific asset URLs, check byte counts, check both edge (Cloudflare) and origin (VPS). `ss -tlnp | grep PORT` for actual binding.

## 6. "Verify Again" vs "Check Balik"

"Verify again" = fresh pass against primary sources, not confirmation. "Check balik X" = find the ORIGINAL document, not confirm it's missing.

## 7. Single VPS Architecture Truth

ALL sites resolve through Cloudflare (proxy only) → VPS Caddy. NO Cloudflare Pages. Caddyfile = single point of failure. F1 recovery: git-tracked at `/root/ARIF-SITES/deploy/Caddyfile`.

## 8. AAA Cockpit Deploy Path

dist/ in .gitignore. Must `cp -r dist/* /var/www/html/aaa/` manually after build.

## 9. arifOS Kernel Restart Pattern

When port 8088 not bound but service "active": `systemctl kill arifos && systemctl start arifos && sleep 10`.

## 10. External Auditor Self-Validation

Build → external audit → fix → re-audit. "Policies without enforcement are suggestions."

## 11. "U Decide" = Autonomous Execution

When Arif says "U decide," he's granting autonomy. Don't ask back.

## 12. Kimi Code 9-Step Infrastructure Probe

1. curl -sI (HTTP status) 2. curl -sI /assets/*.js (bundle) 3. curl -sI /assets/*.css 4. curl -s | grep index- (hash) 5. ls /var/www/html/*/assets/ (VPS hash) 6. Compare hashes 7. ss -tlnp (binding) 8. curl localhost/health 9. curl https://domain/health

## 13. Unified Site Header Architecture

`/_shared/unified-header.html` + `/_shared/unified-header-loader.js`. Change once → propagates everywhere. AAA needs React component.

## 14. SOUL.md v3 Sealed

ASI-Peripheral → AAA-Core. ART Reflex, Warga Proxy, Malu Scalar. F9 compliance.

## 15. Tokens.css Reconciliation Pattern

React builds copy `public/` → `dist/` → `/var/www/html/arif/`. If `public/_shared/design-system/tokens.css` diverges from canonical `/var/www/html/_shared/design-system/tokens.css`, every build creates a stale copy.

**Diagnosis:** `md5sum` canonical vs each site's `/_shared/design-system/tokens.css?_=$(date +%s)` (cache-bust required — Cloudflare caches static assets with `max-age=14400`).

**Fix:** Replace the source file in `public/_shared/` with canonical, rebuild, redeploy. Don't just fix the deployed copy — it gets overwritten on next build.

**Cloudflare cache:** `cf-cache-status: HIT` = cached. `DYNAMIC` = not cached. Static assets (CSS, JS) get cached; HTML doesn't. Cache-bust with `?v=$(date +%s)` to verify. Cache expires naturally in ~4h.
