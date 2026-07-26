# Site Infrastructure Audit Pattern

## When to use
When Arif says "audit the sites" or "check if everything is live" or "Kimi found X."

## Method: Edge + Origin dual probe

Don't just check from the browser. Probe from TWO vantage points:

1. **Origin (VPS direct):** `curl -sf http://localhost:<port>/health` — confirms the service is running
2. **Edge (public URL):** `curl -sf https://<domain>/` — confirms Cloudflare/Caddy routing works

Then check SPECIFIC ASSETS, not just the homepage:
```bash
# Check if React bundle exists (not just HTML shell)
curl -sf "https://aaa.arif-fazil.com/" | grep -o 'index-[^"]*\.js' | head -1
curl -sf -o /dev/null -w "%{http_code} %{size_download}" "https://aaa.arif-fazil.com/assets/index-HASH.js"
```

## Diagnosing "blank page" — 3 root causes

| Symptom | Check | Root cause |
|---|---|---|
| HTML loads, JS 404 | `curl -sf /assets/index-HASH.js` | **Hash mismatch** — deployed HTML references old bundle hash |
| HTML loads, JS loads, no content | Browser console errors | **React runtime error** — check console |
| 189-byte response | `curl -sf -w "%{size_download}"` | **Caddy stub** — no UI was ever built |

## Hash mismatch diagnosis

When Cloudflare serves old HTML with old JS hash:
1. Check local build: `ls /root/<repo>/dist/assets/index-*.js`
2. Check deployed: `curl -sf https://<domain>/ | grep -o 'index-[^"]*\.js'`
3. If hashes differ → Cloudflare CDN has stale cache
4. Fix: deploy to VPS (`rsync dist/ /var/www/html/<site>/`) + purge Cloudflare cache

## Cloudflare cache purge

Token may lack `cache_purge` permission. Check:
```bash
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer $CF_TOKEN"
```

If purge fails with "Authentication error" — token is active but lacks permission.
Options: purge from Cloudflare Dashboard, or wait ~4h for natural expiry.

## arifOS kernel crash recovery

If `systemctl restart arifos` shows "fatal signal" — check if kernel actually started:
```bash
journalctl -u arifos --since "2 min ago" | grep "Uvicorn running"
curl -sf http://localhost:8088/health
```

Sometimes systemd reports failure but the process started anyway (race condition). If health → 200, kernel is fine.

## Kimi Code Full Methodology (9-step probe)

For each site, check ALL of these:

```
1. curl -sI <url>                    → HTTP status + headers
2. curl -sI <url>/assets/*.js        → Does the JS bundle exist?
3. curl -sI <url>/assets/*.css       → Does the CSS bundle exist?
4. curl -s <url> | grep -o 'index-[^"]*' → What hash does HTML reference?
5. ls /var/www/html/<site>/assets/   → What hash does VPS have?
6. Compare #4 vs #5                  → Hash match = deploy correct
7. ss -tlnp | grep <port>            → Is the process actually binding?
8. curl -s http://127.0.0.1:<port>/health → Direct VPS health check
9. curl -sI https://<domain>/health  → External health check (through Cloudflare)
```

## 5 Common Failure Patterns

| Pattern | Symptom | Diagnosis | Fix |
|---|---|---|---|
| Blank React SPA | Empty page, HTML loads | JS bundle 404 | Rebuild + redeploy dist/ |
| Cloudflare cache desync | VPS has new, CF serves old | Compare hash refs | Purge CF cache or wait TTL |
| Kernel active not binding | systemctl active, 502 | `ss -tlnp` shows no listener | Restart service |
| Stub response | 189 bytes | Caddy `respond` directive | Redirect or build UI |
| Hash mismatch | HTML refs wrong JS | Build after deploy | Rebuild + redeploy + verify |

## Critical: `cache-control: immutable` on 404

Worst combo: Cloudflare caches a 404 response with `max-age=31536000, immutable`. The broken state persists for a year. Always check cache headers on error responses. If found, purge immediately from Cloudflare Dashboard.

## Anti-Pattern: Browser-Only Audit

Don't rely solely on browser_navigate + snapshot. Browser renders what CDN serves (may be stale). Always verify with curl from both origin and edge. Proven 2026-07-16: Kimi Code found 4 failures my browser audit missed.

## Proven: 2026-07-16
Kimi Code audit found 4 failures (kernel crash, AAA hash mismatch, A-FORGE stub, MCP 502) that browser-based audit missed. Edge probing + asset-level checking is the correct infrastructure audit methodology.
