# Web Deploy Traps — AAA / arifOS / Federation Sites

> Critical filesystem and caching discoveries from AAA v2 build sessions (2026-07-10).

---

## 🗂️ The Actual Caddy Webroots

**This is the most important trap in the entire federation.**

| Site | WRONG Path (looks real) | CORRECT Caddy Root | Confirmed |
|---|---|---|---|
| AAA | `/var/www/aaa.arif-fazil.com/` | `/var/www/html/aaa/` | ✅ |
| arifOS Observatory | `/var/www/arifos.arif-fazil.com/` | `/var/www/html/arifos/` | ✅ |
| arif-fazil.com | `/var/www/arif-fazil.com/` | `/var/www/html/arif/` | ✅ |

The `aaa.arif-fazil.com/` paths look like separate filesystem locations but are **either hardlinked or bind-mounted to the same inode**. Deletes to one path sometimes don't stick — the content reappears because another path holds the same inode.

**Rule:** Always deploy to the `/var/www/html/<site>` path. Never trust the `/var/www/<domain>/` paths as unique deploy targets without verifying first with `ls` and `rm -rf`.

Verify before and after:
```bash
# Before deploy — confirm correct root is empty
ls /var/www/html/aaa/
rm -rf /var/www/html/aaa  # wipe correct root

# After deploy — verify correct root has new content
ls /var/www/html/aaa/*.jpg 2>/dev/null | head -3 || echo "No stale jpg ✅"
```

---

## ⚛️ React SPA Audit Trap — `web_extract` Sees Noscript, Not the App

When auditing a React SPA (AAA is a React app), `web_extract` fetches the **noscript fallback HTML** — not the live React app rendered in the browser.

**Why:** The `<noscript>` tag in a Vite-built React `index.html` contains a full static fallback page. `web_extract` (server-side fetch) sees this. A real browser sees the React app hydrated from the JS bundle.

**What this means for audits:**
- Banner text, section headings, component content — NOT visible to `web_extract`
- The noscript fallback looks like the OLD APEX-era static page
- The actual React app with all new features is in `dist/assets/index-*.js`
- Verifying React changes = grep the built JS bundle, not crawl the URL

**Verification pattern for React SPA changes:**
```bash
# Verify banner text is in the built JS bundle (proof of deployment)
grep -c "HERMES is AGENT\|F13 Required\|Federation Health" /var/www/html/aaa/assets/index-*.js

# Verify noscript content matches the fallback (not the live app)
grep -c "root\|DOCTYPE" /var/www/html/aaa/index.html
# Should show: has <div id="root"> + Vite script tag = correct React entry

# Verify the React entry point has the right bundle
grep "index-B7r6DUfg\|index-DvQsTLiO" /var/www/html/aaa/index.html
```

**What to check when auditing React SPAs:**
1. `grep` the built JS bundle for the new feature text
2. `curl` the live URL and check for `<script>` tags pointing to `assets/index-*.js`
3. Never trust `web_extract` output as proof of React content

---

## 🧹 Vite `public/` → `dist/` Copy Trap

Vite copies the **entire `public/` directory** into `dist/` on every build. Old APEX-era files in `public/` end up in the build even if you deleted the old static HTML.

**This is why stale images kept appearing after deploy:**
1. Old images existed in `/root/AAA/public/*.jpg`
2. `npm run build` → Vite copied all of `public/` to `dist/`
3. `dist/` deployed to webroot → old images still there

**Pattern to clean stale files from a Vite React build:**
```bash
# Step 1: Find files in public/ not referenced by React source
for f in $(find /root/AAA/public -maxdepth 1 -type f -name "*.jpg" -o -name "*.html"); do
  ref=$(grep -r "$(basename $f)" /root/AAA/src/ 2>/dev/null | wc -l)
  echo "$f: $ref refs"
done

# Step 2: Remove unreferenced stale files
rm -f /root/AAA/public/apex-geometric-hero.jpg
rm -f /root/AAA/public/three-judges.jpg
# ... etc

# Step 3: Rebuild — stale files no longer in dist/
cd /root/AAA && npm run build
```

**Files to always audit in `/root/AAA/public/` for staleness:**
- `*.jpg` — APEX-era hero images
- `*tribute*.html` — legacy tribute pages
- Any file not referenced in `src/` → delete before next build

---

## 🔄 Caddy Cache Behavior

Caddy can serve stale cached content even after files are updated on disk. The cache is at the process level — a `caddy reload` flushes it.

**After any file deploy to a Caddy-served site:**
```bash
caddy reload --config /etc/caddy/Caddyfile
```

**If content still looks stale after reload:**
- The content on disk IS the new content (verify with `head -3 /var/www/html/aaa/index.html`)
- The old content you see is the noscript fallback from the React build
- This is expected — see ⚛️ section above

---

## 📁 Key Paths Reference

```
Caddy root:       /etc/caddy/Caddyfile
Caddy webroots:
  AAA:            /var/www/html/aaa/      ← DEPLOY HERE
  arifOS:         /var/www/html/arifos/
  arif-fazil.com: /var/www/html/arif/
  
React source:     /root/AAA/src/
Vite build:       /root/AAA/dist/
```

**Canonical deploy sequence for AAA:**
```bash
# 1. Clean stale files from public/
rm -f /root/AAA/public/{apex-geometric-hero,three-judges,13-floors-geometric,mcp-pentagon,entropy-cooling,entropy-geometry,forge-background,mind-hero,arif-hero-og,constitutional-floors}.jpg
rm -f /root/AAA/public/jackie-ngu*.html

# 2. Build
cd /root/AAA && npm run build

# 3. Deploy to CORRECT Caddy root
rm -rf /var/www/html/aaa
cp -r /root/AAA/dist /var/www/html/aaa

# 4. Reload Caddy
caddy reload --config /etc/caddy/Caddyfile

# 5. Verify (bundle grep, not web_extract)
grep -c "HERMES is AGENT" /var/www/html/aaa/assets/index-*.js
```
