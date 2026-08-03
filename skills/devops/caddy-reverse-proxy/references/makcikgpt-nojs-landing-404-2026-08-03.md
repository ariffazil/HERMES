# MakcikGPT nojs landing 404 — full case (2026-08-03)

The `path /prefix/*` glob swallows the bare landing page when combined with
`uri strip_prefix` + header-gated handlers. Canonical write-up lives in SKILL.md
under "Common Pitfall: `path /prefix/*` glob ALSO matches the bare `/prefix/`
landing". This file keeps the case forensics and the reusable verification battery.

## Timeline of the incident

1. Cron job `🜂 Sense — arif-fazil.com Health Probe` (*/15 min, no-agent mode)
   reported only "Script exited with code 1" — no detail. Two bugs stacked.
2. **Bug A (probe):** `set -euo pipefail` + unguarded command substitution
   (`WEBZEN_OUT=$(web_zen doctor ...)` and `DIRTY_COUNT=$(git ... | wc -l)`)
   killed the script at the dying line before the report block ran. See
   shell-patterns skill, "Fix 3".
3. **Bug B (Caddy):** web_zen doctor's urllib UA hit `@makcikgpt_nojs`
   (`path /world/makcikgpt/*` + `not header_regexp Accept text/html`).
   The glob matched the bare `/world/makcikgpt/` landing; strip_prefix left `/`;
   `try_files {path}.html {path}.md =404` tried `/.html` → `/.md` → 404.
4. Humans never noticed: browsers send `Accept: text/html` → handler skipped →
   exact landing handler serves the React shell (200). GPTBot/curl/urllib got 404.

## Discriminating probe that isolated the handler (2 requests)

```bash
curl -s -A "curl/8.5" -H "Accept: text/html" -o /dev/null -w "%{http_code}\n" https://arif-fazil.com/world/makcikgpt/   # 200
curl -s -A "curl/8.5"                          -o /dev/null -w "%{http_code}\n" https://arif-fazil.com/world/makcikgpt/   # 404
```

200-then-404 = an Accept-gated handler owns the path for non-html clients.
Confirm with real bot UAs: `-A GPTBot`, `-A Python-urllib/3.13`, `-A python-requests/2.32`.

## The fix (applied, verified)

```caddyfile
@makcikgpt_nojs {
    # (.+) requires >=1 char after prefix — bare landing excluded
    path_regexp mknoj ^/world/makcikgpt/(.+)$
    not header_regexp Accept text/html
}
```

Backup before edit: `/etc/caddy/Caddyfile.bak-*-mknoj`. Then `caddy validate` →
`caddy reload` (zero-downtime).

## Verification battery (post-reload, all passed)

| Probe | Expected |
|---|---|
| `curl -A "curl/8.5"` landing | 200 (was 404) |
| `curl -A "Python-urllib/3.13"` landing | 200 (was 404) |
| `curl -A GPTBot` landing | 200 (was 404) |
| `curl -A "curl/8.5" -H "Accept: text/html"` landing | 200 (unchanged) |
| browser UA + text/html landing | 200 (unchanged) |
| bot UA article sub-path (e.g. /anwar-jung-shadow) | 200 (unchanged) |
| homepage, /missions/, /writing/ | 200 (unchanged) |
| `/makcikgpt/` redirect | 301 → /world/makcikgpt/ (unchanged) |
| full Sense probe script | exit 0, silent |

## Related fallout

- `/world/makcikgpt/` is in the `make verify-pages` deploy-gate page list —
  this 404 also blocked `make deploy` until fixed.
- The sibling `🜂 Verify — Drift Audit` cron (HTTP 404 at 20:37 same day) was
  almost certainly probing the same URL; expected to clear on next run.
- Files on disk were never the problem — `makcikgpt-md/index.html` existed the
  whole time; the 404 was pure routing (handler match semantics).
