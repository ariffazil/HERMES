# Site Deployment Pitfalls — arif-fazil.com Federation

> Learned 2026-07-16. Kimi Code external audit found 3 hidden failures.

---

## Pitfall 1: AAA Cockpit Blank (React never hydrates)

**Symptom:** HTML loads (200) but page is blank. Browser console shows 404 on hashed JS/CSS assets.

**Root cause:** `dist/` is in AAA's `.gitignore`. `git push origin main` does NOT deploy the built assets. The Caddyfile serves from `/var/www/html/aaa/` which is a COPY of dist/, not a symlink.

**Fix:**
```bash
cd /root/AAA && npm run build
cp -r /root/AAA/dist/* /var/www/html/aaa/
systemctl reload caddy
# Verify:
curl -sf -o /dev/null -w "%{http_code}" "https://aaa.arif-fazil.com/assets/index-HASH.js"
```

**Prevention:** After any AAA build, ALWAYS copy dist/ to /var/www/html/aaa/. The deploy-vps.sh script handles this for ARIF-SITES but AAA has its own path.

**Kimi Code diagnosis:** "The hashed filenames in the served HTML match /root/AAA/dist/assets/ on disk. But Cloudflare Pages is serving a deploy that doesn't include them."

---

## Pitfall 2: arifOS Kernel Dead (port not bound)

**Symptom:** `systemctl status arifos` shows "active (running)" but `curl http://127.0.0.1:8088/health` fails. `ss -tlnp | grep 8088` shows nothing.

**Root cause:** The kernel process shut down (e.g., "Shutting down" in journal) but systemd didn't restart it. The service is stuck in "deactivating (stop-sigterm)" state.

**Fix:**
```bash
systemctl kill arifos    # Force kill the stuck process
systemctl start arifos   # Fresh start
sleep 10                 # Wait for startup (kernel loads heavy deps)
curl -sf http://127.0.0.1:8088/health
```

**Detection:** The kernel health endpoint is the dead man's switch. If `mcp.arif-fazil.com/mcp` returns 502, check port 8088 FIRST.

**Kimi Code diagnosis:** "The arifos.service is active but listeners on 127.0.0.1:8088 show no arifOS binding. The service appears to be in a restart loop."

---

## Pitfall 3: A-FORGE Stub (no UI built)

**Symptom:** `forge.arif-fazil.com` returns 189 bytes of text.

**Root cause:** No web UI was ever built. The Caddyfile has a literal `respond` directive, not a `file_server`. This is BY DESIGN — A-FORGE's surface is the MCP gateway (:7072) and Express server (:7071).

**Fix (redirect):**
```caddy
# In Caddyfile, replace the catch-all handler:
handle {
    redir https://mcp.arif-fazil.com{uri} permanent
}
```

**Kimi Code diagnosis:** "A-FORGE's actual surface is the MCP gateway and Express server — both healthy. There is no human-facing UI to 'fix' because none was designed."

---

## Pitfall 4: GitHub Push Protection (Mapbox public key)

**Symptom:** `git push` blocked with "secret detected" error referencing `pk.eyJ...` in `geox-app/index.html`.

**Root cause:** GitHub's secret scanner flags Mapbox public keys as secrets. The key is PUBLIC (used for map tiles), not a secret.

**Fix:** Visit the allow-secret URL from the error message:
```
https://github.com/ariffazil/arif-sites/security/secret-scanning/unblock-secret/...
```

**Alternative:** Use `git-filter-repo` to redact the token from history. But the regex must handle base64 chars (`+`, `/`, `=`).

---

## Pitfall 5: a-forge.arif-fazil.com Dead DNS

**Symptom:** Caddy has a vhost for `a-forge.arif-fazil.com` (with hyphen) but DNS doesn't resolve.

**Root cause:** DNS only has `forge.arif-fazil.com` (no hyphen). The Caddy vhost is dead config.

**Fix:** Delete the `a-forge.arif-fazil.com` block from Caddyfile. Dead config = drift.

---

## Site Map (verified 2026-07-16)

| Subdomain | Served by | Root | Status |
|---|---|---|---|
| arif-fazil.com | Caddy | /var/www/html/arif | ✅ SPA |
| arifos.arif-fazil.com | Caddy + reverse_proxy :8088 | /var/www/html/arifos | ✅ Static + kernel |
| aaa.arif-fazil.com | Caddy + reverse_proxy :3001 | /var/www/html/aaa | ✅ SPA (after fix) |
| mcp.arif-fazil.com | Caddy + reverse_proxy :8088 | /var/www/html/mcp | ✅ Static + kernel |
| geox.arif-fazil.com | Caddy + reverse_proxy :8081 | /var/www/html/geox | ✅ Static + organ |
| wealth.arif-fazil.com | Caddy + reverse_proxy :18082 | /var/www/html/wealth | ✅ Static + organ |
| well.arif-fazil.com | Caddy + reverse_proxy :18083 | /var/www/html/well | ✅ Static + organ |
| forge.arif-fazil.com | Caddy + reverse_proxy :7071/:7072 | redirect → mcp | ✅ Redirect + MCP |

---

## Deployment Commands Cheat Sheet

```bash
# ARIF-SITES (MakcikGPT articles, main site)
cd /root/ARIF-SITES && bash deploy-vps.sh

# AAA Cockpit (React SPA)
cd /root/AAA && npm run build && cp -r dist/* /var/www/html/aaa/ && systemctl reload caddy

# arifOS kernel
systemctl restart arifos && sleep 10 && curl -sf http://127.0.0.1:8088/health

# A-FORGE MCP
systemctl restart a-forge && curl -sf :7071/health && curl -sf :7072/health

# All organs health check
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://127.0.0.1:$port/health" >/dev/null 2>&1 && echo "✅ $name" || echo "❌ $name"
done
```
