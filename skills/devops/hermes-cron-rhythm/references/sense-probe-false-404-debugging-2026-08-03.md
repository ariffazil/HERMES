# Cron Probe Failure Debugging — Silent Script Death + False-404 (forged 2026-08-03)

Three pitfalls proven in one session while debugging the 🜂 Sense cron
(`arif-fazil-sense.sh`, job `db0aa69e0fdc`) which failed every 15 min for hours.
These belong in the Pitfalls section of SKILL.md.

## 1. `no_agent` script failures carry NO diagnostics

The cron output file (`~/.hermes/cron/output/<job_id>/<latest>.md`) records only
the exit code — "Script exited with code 1" is the ENTIRE message. No stderr, no
line number. Debugging recipe:

1. Read the output file — usually useless.
2. Run the script manually: `bash /root/.hermes/scripts/<script>.sh`.
3. If it dies with **zero output**, suspect `set -euo pipefail` killing it at the
   first failing command BEFORE the report block can print.
4. Trace stage-by-stage: run each block's commands by hand until one fails.

**Design rule for probe scripts:** accumulate failures in variables (`FAILS=$((FAILS+1))`,
`ROUTE_FAILS="$ROUTE_FAILS\n ..."`) and print ONE report before `exit 1`. Never let
`set -e` kill the script mid-flight with no report.

Proven: the Sense script failed silently; manual run + stage tracing found the real
RED two layers deep (web_zen doctor exit 1 + a false-404 route check).

## 2. Health probes MUST probe as a real browser — header-gated routing produces false 404s

`curl -sI` (HEAD, no `Accept` header, curl UA) is NOT a browser. Caddy
`header_regexp` matchers (bot-vs-browser handlers, `Accept`-gated no-JS handlers)
and Cloudflare WAF can return 404 to a probe while humans see 200.

Proven on arif-fazil.com `/world/makcikgpt/`: probe = 404, browser-flavored request
(`Accept: text/html`) = 200 SPA shell (13,961 bytes). Humans never saw the outage.

**Diagnosis matrix BEFORE touching the server** — curl the URL four ways:

| | no Accept header | `Accept: text/html` |
|---|---|---|
| HEAD (`curl -sI`) | probe default — may 404 | — |
| GET, curl UA | may 404 | usually 200 |
| GET, browser UA | may 404 | real-browser ground truth |

If ANY browser-flavored request returns 200, **fix the PROBE, not the server.**

Probe template:
```bash
code=$(curl -s -o /dev/null -w '%{http_code}' -m 5 -H "Accept: text/html" "$url")
```

Full site-specific anatomy (Caddy handler chain, WAF history, static surfaces):
`arif-sites-content-ops` → `references/makcikgpt-routing-and-probe-false-positives.md`.

## 3. Check for sibling/parallel activity before and after patching probes or Caddyfiles

If the patch tool warns "modified by sibling subagent", or the file's mtime moved
mid-session, another agent/session fixed the same problem concurrently. Signals:

```bash
stat -c %y /etc/caddy/Caddyfile              # mtime moved?
journalctl -u caddy | grep /load | tail      # reload after your edit?
cd /root/arif-fazil.com && git log --oneline -5   # parallel commits?
```

Re-read the file and re-run the FULL test before declaring victory or layering your
own fix on top — both fixes may need to coexist. Proven: while patching the probe
script, a parallel commit (`b9ef5ad` — makcikgpt trailing-slash + Caddy reload at
13:16 UTC) fixed the server-side routing; final green required BOTH fixes.
