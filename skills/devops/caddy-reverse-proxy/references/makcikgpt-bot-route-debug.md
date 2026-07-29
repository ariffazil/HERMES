# MakcikGPT Caddy Bot Route Debugging (2026-07-29)

## Problem

External witness probe P17 persistently reported `HTTP 404` for `https://arif-fazil.com/world/makcikgpt/`. Individual article URLs like `/world/makcikgpt/ilmu-bbb` returned 200. The `@ai-bot-world` Caddy handler was correctly configured but the landing page root returned 404.

## Architecture

Traffic flow:
```
Client → Cloudflare → Caddy (VPS :443) → file_server
```

Caddy config had three MakcikGPT routing layers:
1. **`@ai-bot-world`** — bot UA + path `/world/makcikgpt/*` → `uri strip_prefix` + file_server from `/var/www/html/arif/makcikgpt-md`
2. **`@makcikgpt_nojs`** — non-bot + not `text/html` → same dir, `try_files {path}.html {path}.md =404`
3. **`handle /world/makcikgpt/*`** — browser SPA → `/var/www/html/arif/makcikgpt/` with `try_files {path} /index.html`

## Root Cause

When requesting `/world/makcikgpt/` with a bot UA, the `@ai-bot-world` handler fires. `uri strip_prefix /world/makcikgpt` reduces the internal path to just `/`. Then:

```
try_files {path} {path}.html /index.html
# with {path}=/ becomes:
try_files / /.html /index.html
```

- `/` matches the root directory — Caddy treats this as "found" by `try_files`
- But `file_server` doesn't cascade to serve `index.html` from the matched directory in this context
- Result: 404 with `content-length: 0`

## Fix

Added a dedicated `handle /world/makcikgpt/` block BEFORE the `@ai-bot-world` matcher:

```caddyfile
handle /world/makcikgpt/ {
    root * /var/www/html/arif/makcikgpt-md
    try_files /index.html =404
    file_server
}
```

This matches the exact directory path directly (not relying on `{path}` after strip_prefix), explicitly resolves `/index.html`, and serves via `file_server`.

## Key Debugging Techniques Used

1. **Exact curl reproduction of probe behavior:**
   ```bash
   curl -s -k -i --max-time 15 -A "curl/8.12" --resolve "arif-fazil.com:443:127.0.0.1" \
     "https://arif-fazil.com/world/makcikgpt/"
   ```
   The `--resolve` flag forces DNS bypass so requests hit the local Caddy directly (no Cloudflare).

2. **Tracing Caddy route matching** by testing specific paths:
   - `/world/makcikgpt/` → 404 (root landing page)
   - `/world/makcikgpt/ilmu-bbb` → 200 (individual article)
   - This narrowed the issue to the stripped root path `try_files` behavior.

3. **Distinguishing Cloudflare vs Caddy** as the source of 404:
   - With `--resolve` → hits Caddy directly → Caddy returns 404
   - Without `--resolve` → goes through Cloudflare → same 404
   - If Cloudflare were the issue, responses would differ (Cloudflare returns CF-specific headers). Both paths returned `server: Caddy` or `content-length: 0` → confirmed Caddy-side.

4. **File existence verification on disk**:
   ```bash
   ls -la /var/www/html/arif/makcikgpt-md/index.html  # 4.7KB, exists
   ```
   Confirmed the file existed — ruling out missing-content causes.

## Related Pitfalls

- **Bot UA regex mismatch**: The `@ai-bot-world` matcher checks User-Agent. Python's `urllib` sends `Python-urllib/3.x` which may not match if `Python-urllib` is missing from the bot regex (present: `python-requests`, `curl`). If a probe using `urllib` gets 404 while `curl` works, check the UA regex.
- **`try_files` directory fallback**: See the parent skill's "uri strip_prefix + root path" pitfall for the generalised pattern.
