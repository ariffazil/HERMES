# MakcikGPT Article 404 — Diagnostic Workflow

> Proven 2026-07-31. Session: ai-johor-rakyat-2026 404 audit → 22-article fix.

## The Two-Handler Split-Brain

Caddy serves MakcikGPT articles through TWO separate handlers with different roots:

| Traffic | Matcher | Root | Serves |
|---------|---------|------|--------|
| Bot (GPTBot, curl, etc.) | `@ai-bot-world` | `/var/www/html/arif/makcikgpt-md` | Static `.html` files |
| Browser (Mozilla/5.0) | `handle /world/makcikgpt/*` | `/var/www/html/arif/makcikgpt` | React SPA shell → `index.html` |

**Key insight:** A 200 from one handler doesn't mean the other works. Always test BOTH:
```bash
# Bot
curl -sk --resolve arif-fazil.com:443:127.0.0.1 -o /dev/null -w "bot: %{http_code}\n" "https://arif-fazil.com/world/makcikgpt/<slug>"

# Browser
curl -sk --resolve arif-fazil.com:443:127.0.0.1 -H "User-Agent: Mozilla/5.0" -o /dev/null -w "browser: %{http_code}\n" "https://arif-fazil.com/world/makcikgpt/<slug>"
```

## Diagnostic Decision Tree

1. **Both 200?** → Article works. Done.
2. **Bot 200, browser ERR_HTTP_RESPONSE_CODE_FAILURE?** → SPA shell directory problem.
   - Check: `ls /var/www/html/arif/makcikgpt/index.html` exists?
   - Check: Does it reference the CURRENT JS bundle? `grep -o 'src="[^"]*index-[^"]*\.js"' /var/www/html/arif/makcikgpt/index.html`
   - Fix: `mkdir -p /var/www/html/arif/makcikgpt && cp /var/www/html/arif/index.html /var/www/html/arif/makcikgpt/index.html`
3. **Bot 404, browser 200?** → Static HTML missing.
   - Check: `ls /var/www/html/arif/makcikgpt-md/<slug>.html`
   - Fix: Generate from essays.json (extract slug from `dest.path`)
4. **Both 200 but browser shows 404 page?** → React SPA route missing or JS bundle stale.
   - Check: `grep -o 'src="[^"]*index-[^"]*\.js"' /var/www/html/arif/makcikgpt/index.html` matches dist?
   - Check: `grep "<slug>" /var/www/html/arif/assets/index-*.js` — article in bundle?
   - Check: App.tsx has `<Route path="/world/makcikgpt/:slug" element={<MakcikGptArticle />} />`

## The `@makcikgpt_nojs` Trap

Caddy has a third handler `@makcikgpt_nojs` (line 591-600) that matches requests where `Accept` header does NOT contain `text/html`. This handler serves directly from `makcikgpt-md/` with `try_files {path}.html {path}.md =404`. When the static files don't exist, it returns hard 404 — NOT falling through to the SPA shell.

- `curl` default Accept (`*/*`) → does NOT contain `text/html` → matches `@makcikgpt_nojs`
- Missing `.html` file → hard 404, never reaches the SPA shell handler

## Bulk Audit

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com
bash /path/to/deploy-makcik.sh --verify-only
```

Checks: JS bundle match, bot+browser 200 per article, listing 200, feed/sitemap/llms.txt.
