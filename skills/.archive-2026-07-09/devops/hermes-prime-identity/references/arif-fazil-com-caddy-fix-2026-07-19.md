# arif-fazil.com Caddy + AI Bot Dual-Channel — Session Reference (2026-07-19)

> Specifics captured during the audit + "fix all" round on 2026-07-19. Future agents debugging arif-fazil.com routing should read this first.

## File locations

- Caddyfile (live): `/etc/caddy/Caddyfile`
- Caddyfile (backup pre-2026-07-19): `/etc/caddy/Caddyfile.bak-20260719`
- arif-sites source: `/root/arif-sites/sites/arif-fazil.com/`
- arif-fazil.com deployed: `/var/www/html/arif/`
- arifos.arif-fazil.com deployed: `/var/www/html/arifos/`
- _well-known_ arif root: `/var/www/html/arif/.well-known/` (7 files: agent.json, webmcp.json, arifos-federation.json, did.json, did-configuration.json, mcp.json, AGENTS.md.sig)
- _well-known_ observatory: `/var/www/html/arifos/.well-known/` (12+ files including agent-card.json, governance.jsonld, mcp/server.json, did-arifos-observatory.json, etc.)
- makcikgpt markdown mirror: `/var/www/html/arif/wealth/makcikgpt/` AND `/var/www/html/arif/makcikgpt-md/`
- SPA fallback root: `/var/www/html/arif/index.html`

## Key Caddy patterns (verified live 2026-07-19)

### Pattern 1 — AI bot markdown bypass (humans get SPA, bots get .md)

```caddyfile
@ai-bot {
    header_regexp User-Agent (?i)GPTBot|ClaudeBot|PerplexityBot|OAI-SearchBot|anthropic-ai|Google-Extended|Bytespider|Amazonbot
    path /wealth/makcikgpt/*
}
handle @ai-bot {
    rewrite * {path}.md
    root * /var/www/html/arif
    try_files {path} /wealth/makcikgpt/{path}.md
    file_server
}
```

Test:
```bash
curl -I -A "GPTBot" https://arif-fazil.com/wealth/makcikgpt/searah-followup  # 200, Content-Type: text/markdown
curl -I https://arif-fazil.com/wealth/makcikgpt/searah-followup                  # 200, Content-Type: text/html (SPA)
```

### Pattern 2 — Slug-preserving legacy redirect (DO NOT use `*` wildcard)

**Broken** (slug lost):
```caddyfile
redir /wealth/makcikgpt* /makcikgpt/ 301
# Result: /wealth/makcikgpt/searah-followup → /makcikgpt/ (index, slug dropped)
```

**Working** (slug preserved):
```caddyfile
@makcikgpt_legacy path_regexp ^/wealth/makcikgpt/(.+)$
handle @makcikgpt_legacy { redir /makcikgpt/{re.1} 301 }
# Result: /wealth/makcikgpt/searah-followup → /makcikgpt/searah-followup
```

### Pattern 3 — Discovery file redirects to canonical observatory subdomain

```caddyfile
# Place AFTER the @well-known catch-all handle, BEFORE catch-all /.well-known/* reverse_proxy
handle /.well-known/agent-card.json {
    redir https://arifos.arif-fazil.com/.well-known/agent-card.json permanent
}
handle /.well-known/governance.jsonld {
    redir https://arifos.arif-fazil.com/.well-known/governance.jsonld permanent
}
handle /.well-known/mcp/server.json {
    redir https://arifos.arif-fazil.com/.well-known/mcp/server.json permanent
}
handle /.well-known/oauth-authorization-server {
    redir https://mcp.arif-fazil.com/.well-known/oauth-authorization-server permanent
}
```

## Bug — Caddy handler ordering gotchas

**Bug:** Shorthand `redir @matcher` does not always respect handler ordering vs other named matchers. The `@ai-bot` handler at line 71 was being overridden by my later `redir @makcikgpt_legacy` because the shorthand form doesn't always trigger matcher precedence correctly.

**Fix:** Use explicit `handle @matcher { redir ... }` block placed at the correct position. The explicit form guarantees evaluation in declared order.

**Bug 2:** `try_files {path}.md @fallback` doesn't work — the named matcher `@fallback` is not evaluated by `try_files` in some Caddy versions. Use explicit `handle` blocks.

**Bug 3:** `systemctl reload caddy` silently does nothing if the Caddy admin API isn't bound to `:2019`. Use `systemctl restart caddy` instead.

## Workflow for unknown Caddy bugs

1. `caddy validate --config /etc/caddy/Caddyfile` — must show "Valid configuration"
2. `systemctl restart caddy` (not reload)
3. `journalctl -u caddy --since "1 min ago"` — check if new config actually loaded
4. `curl -sv` for verbose trace

## arif-fazil.com redirect map (post 2026-07-19 fix)

| From | To | Status |
|---|---|---|
| `/wealth/makcikgpt/<slug>` (3 with .md) | 200 text/html direct (catch-all SPA) | ✅ |
| `/wealth/makcikgpt/<slug>` (7 newly generated .md) | 200 text/html direct (catch-all SPA) | ✅ |
| `/wealth/makcikgpt/<slug>` (with AI bot UA) | 200 text/markdown via @ai-bot handler | ✅ |
| `/wealth/makcikgpt/<slug>` (any UA, with explicit handle) | 301 → `/makcikgpt/<slug>` | ✅ for slug preservation |
| `/wealth/makcikgpt/` (no slug, no .md) | 200 text/html (SPA index) | ✅ |
| `/.well-known/agent-card.json` (root domain) | 301 → arifos subdomain | ✅ |
| `/.well-known/governance.jsonld` (root domain) | 301 → arifos subdomain | ✅ |
| `/.well-known/mcp/server.json` (root domain) | 301 → arifos subdomain (further 301 to mcp) | ✅ |
| `/.well-known/oauth-authorization-server` (root domain) | 301 → mcp.arif-fazil.com | ✅ |

## Sitemap (post 2026-07-19 fix, commit `fedbed8`)

- 30 URLs total (was 30 — no new URLs added)
- All 9 makcikgpt articles now point to `/makcikgpt/<slug>` (was `/wealth/makcikgpt/<slug>`)
- `lastmod` updated from 2026-07-01 to 2026-07-19
- 0 references to `/wealth/makcikgpt/` remain in sitemap

## 7 generated .md files (deployed, not in git)

Files written to `/var/www/html/arif/wealth/makcikgpt/` and `/var/www/html/arif/makcikgpt-md/`:
- `sam-altman-elon-musk-anwar-akal.md` (9751 bytes)
- `searah-followup.md` (8579 bytes)
- `cerita-makcik.md` (13877 bytes)
- `siasatan-harakah.md` (3798 bytes)
- `iran-hormuz.md` (4874 bytes)
- `ilmu-bbb.md` (9126 bytes)
- `ytl-monopoli.md` (9329 bytes)

Generated from source `.ts` files in `/root/arif-sites/sites/arif-fazil.com/src/data/makcikgpt/` via inline Python `re.sub` conversion (cover block, h1/h2/h3, strong/em, lists → MD).

## Receipts (this session)

- `/root/A-FORGE/forge_work/2026-07-19/ARIF-FAZIL-COM-AUDIT-RECEIPT-2026-07-19.md`
- `/root/A-FORGE/forge_work/2026-07-19/ARIF-FAZIL-COM-FIX-ALL-RECEIPT-2026-07-19.md`

## OpenCode smoke test (proven working pattern)

```bash
# Smoke test before dispatching real task
timeout 60 opencode run --model opencode-go/deepseek-v4-flash-free 'Print exactly: DEEPSEEK_OK' 2>&1 | tail -3

# If it returns "DEEPSEEK_OK" → model works. If error/timeout → try next in fallback chain.
```

Fallback chain (verified 2026-07-19):
1. `opencode-go/deepseek-v4-flash-free` (free, slow but works)
2. `deepseek/deepseek-v4-flash` (paid, faster)
3. `deepseek/deepseek-chat` (paid, available)

Avoid: `mimo-platform/*`, `opencode-go/minimax-m3`, `tokenplan-mimo/mimo-v2.5-pro` (all failed during this session).
