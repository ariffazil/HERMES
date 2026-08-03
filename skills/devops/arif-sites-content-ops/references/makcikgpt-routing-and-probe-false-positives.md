# MakcikGPT Routing Anatomy + Probe False-Positives (forged 2026-08-03)

The `/world/makcikgpt/` surface is the most routing-fragile path on arif-fazil.com.
This file documents its Caddy handler anatomy and the class of false-404 it caused.

## Verified facts (2026-08-03, all probed live)

| Request flavor to `/world/makcikgpt/` | Pre-fix result | Post-fix result |
|---|---|---|
| HEAD or GET, **no** `Accept: text/html` | ❌ 404 | ✅ 200 |
| GET + `Accept: text/html` (real browser) | ✅ 200 — 13,961-byte SPA shell | ✅ 200 |
| `/makcikgpt/` redirect chain | 301 → final 200 | same |

Humans **never saw the 404** — only non-browser probes did. The 🜂 Sense cron
(`arif-fazil-sense.sh`, job `db0aa69e0fdc`, every 15 min) failed for hours with the
cron output showing only "Script exited with code 1" (no diagnostics — the runner
captures exit codes, not stderr).

## Root causes (three, overlapping)

1. **Probe was not a browser.** The script used `curl -sI` (HEAD, no `Accept` header,
   curl UA). Caddy has an `Accept`-gated handler for `/world/makcikgpt/*` aimed at
   no-JS clients (`@makcikgpt_nojs`: `path /world/makcikgpt/*` + `not header_regexp
   Accept text/html` → `try_files {path}.html {path}.md =404`). Requests without
   `Accept: text/html` land there and 404 on the bare landing path (no `.html`/`.md`
   file at that exact path).
2. **Cloudflare WAF blocks non-standard UAs** on this path — recorded in site git
   history: commit `35cecc1` "remove custom UA from verify-pages.sh (Cloudflare WAF
   blocks non-standard UAs on /world/makcikgpt/)".
3. **The script died silently** — `set -euo pipefail` killed it at the first failing
   check before the report block could print which URL failed.

Fix that landed: probe now uses `curl -s -o /dev/null -w '%{http_code}' -m 5
-H "Accept: text/html"` (GET, browser Accept header). A parallel same-day commit
(`b9ef5ad`) fixed server-side routing (makcikgpt trailing-slash) + Caddy reload —
both were needed for full green.

## Caddy handler anatomy (as read from /etc/caddy/Caddyfile, 2026-08-03)

Inside the arif-fazil.com vhost, in order:

1. Canonical redirects: `/makcikgpt`, `/makcikgpt/`, `/makcikgpt/<slug>` → 301 to
   `/world/makcikgpt/...` (P17 fix 2026-07-31). Also `/wealth/makcikgpt*` and
   `/economics/makcikgpt*` redirect families.
2. `@ai-bot-landing` — bot UA regex (`GPTBot|ClaudeBot|...|curl|python-requests|...`)
   + exact path `/world/makcikgpt/` → serves canonical static index from
   `/var/www/html/arif/makcikgpt-md/index.html` (bot gets static, browser gets SPA).
3. `handle /world/makcikgpt/` — browser landing: root `/var/www/html/arif`,
   `rewrite * /index.html` (React SPA shell), no-cache headers (F1 cache-bust).
4. `@ai-bot-world` — bot UA + `/world/makcikgpt/*` → strip prefix, serve generated
   article HTML from `/var/www/html/arif/makcikgpt-md/` (`try_files {path} {path}.html
   {path}/index.html /index.html`).
5. `@makcikgpt_nojs` — path `/world/makcikgpt/*` + NOT `Accept: text/html` → strip
   prefix, `try_files {path}.html {path}.md =404` (RSS readers / non-HTML clients).
   **This is the handler that 404s bare probes.**

Static surfaces: `/var/www/html/arif/makcikgpt-md/` (generated article HTML + MD +
index.html) and `/var/www/html/arif/world/makcikgpt/index.html` (105-byte landing stub).
Source repo: `/root/arif-fazil.com/sites/arif-fazil.com/makcikgpt`.

Note: `verify-pages.sh` declares `/world/makcikgpt/` under `INTENTIONAL_EXCLUSIONS`
(bot-only static surface) — do not "fix" it into the SPA gate.

## Rules for any probe/audit touching this site

1. **Probe as a real browser:** GET + `Accept: text/html` + real browser UA.
   Never `curl -sI` alone.
2. **Diagnosis matrix before touching Caddy:** HEAD vs GET × with/without
   `Accept: text/html` × curl-UA vs browser-UA. If any browser-flavored request
   returns 200, fix the probe, not the server.
3. **Check config-vs-live before concluding stale routing:** compare Caddyfile mtime
   (`stat -c %y /etc/caddy/Caddyfile`) against `journalctl -u caddy | grep /load`
   timestamps.
4. **Concurrent-fixer awareness:** this path has an active maintenance history —
   before patching, `git log --oneline -5` in `/root/arif-fazil.com` to see if
   another session already addressed the same 404.
