# Route-Sorting Diagnosis — the /wealth/gold/api/* case (2026-08-01)

Case study for the "Caddy v2 reorders handle blocks" pitfall. The gold chart at
`arif-fazil.com/wealth/gold/` rendered blank while oil and gas dashboards worked.

## Symptom evidence

| Probe | Result |
|---|---|
| `GET /wealth/gold/api/ticker` | **text/html, 26KB** (the gold page itself!) |
| `GET /wealth/oil/api/ticker` | application/json ✅ |
| `GET /wealth/gas/api/ticker` | application/json ✅ |
| `GET /gold/api/ticker` (direct path matcher) | application/json ✅ |
| `curl localhost:3456/api/ticker` (backend direct) | application/json ✅ |

Chart code: gold page `apiBase: '/wealth/gold/api'` → chart fetches
`/wealth/gold/api/*` → gets HTML → `JSON.parse` fails → blank chart. Zero Caddy
errors, zero 404s. The classic silent-200-wrong-content-type failure.

## Root cause

The `/wealth/gold/api/*` reverse_proxy route **existed** in the adapted config
but was sorted to the very END of the apex site's route list — after the
`/wealth/gold/*` static catch-all AND after the SPA catch-all (which includes
`/wealth*`). First-match-wins → the static handler served index.html for API
paths. Oil/gas routes with identical config structure sorted correctly; only
gold lost. The "vendor handle anchor" trick (used to fix gas) did NOT save gold.

## Diagnosis commands (reusable)

```bash
# 1. Isolate the broken sibling — compare content-type across similar routes
for c in gold oil gas; do
  printf '/wealth/%s/api/ticker: ' $c
  curl -s -m 8 -o /dev/null -w '%{content_type}\n' https://arif-fazil.com/wealth/$c/api/ticker
done

# 2. Ground truth: the SORTED route order (not the Caddyfile order)
/usr/bin/caddy adapt --config /etc/caddy/Caddyfile --adapter caddyfile > /tmp/caddy.json
# dump with scripts/caddy-route-order.sh arif-fazil.com /wealth/gold
# → look at index positions: /wealth/gold/api/* must precede /wealth/gold/*
#   and the SPA catch-all ("/wealth*" in the big path list)

# 3. Cross-check the RUNNING config (reload happens in-process, same PID)
curl -s --unix-socket /var/run/caddy-admin.sock http://localhost/config/ | head -c 200

# 4. Client-side truth: what apiBase does the live page use?
curl -s https://arif-fazil.com/wealth/gold/ | grep -oE "apiBase: '[^']*'"
```

## Fix applied (T2 — no Caddyfile mutation)

The `/gold/api/*` direct-path matcher sorts correctly (verified JSON), so the
workaround was a one-line static edit — snapshot first:

```bash
cp /var/www/html/gold/index.html /var/www/html/gold/index.html.bak.TIMESTAMP
sed -i "s|apiBase: '/wealth/gold/api'|apiBase: '/gold/api'|" /var/www/html/gold/index.html
# verify: curl the page again → apiBase: '/gold/api'; chart endpoints all JSON
```

Why this is safe: `/gold/` and `/wealth/gold/` serve the same file
(`/var/www/html/gold/index.html`), `/gold/api/*` provably proxies to
localhost:3456, and the edit is reversible by restoring the snapshot. No
Caddyfile change → no T3 gate.

## Proper fix (T3 — pending sovereign ACK)

Restructure the gold API route so Caddy cannot re-sort it behind the catch-alls:
- `handle_path /wealth/gold/api/* { reverse_proxy localhost:3456 }` (path-based,
  participates in specificity sorting more predictably), or
- wrap in a `route { }` block (preserves literal order), or
- remove `/wealth*` from the SPA catch-all and add an explicit
  `handle /wealth/*` fallback AFTER the gold api block.

Always: backup Caddyfile → `caddy validate` → reload → verify
`curl -sI .../wealth/gold/api/ticker` returns application/json.

## T3 forensics note (parallel-agent mutation)

While this was being diagnosed, a parallel opencode (FORGE) session reloaded
Caddy (journal: `admin.api load complete` 12:29:17Z; Caddyfile mtime 12:29:10Z)
and applied the previously-888-HELD `/economics/` SPA-swap. Detection recipe:
`journalctl -u caddy | grep admin.api` for reload timestamps, `stat` the
Caddyfile, `ps -eo pid,lstart,cmd | grep -iE 'opencode|kimi-code'` for the
mutating agent session. `ExecMainStartTimestamp` does NOT move on `caddy
reload` (in-process) — process start ≠ config load.
