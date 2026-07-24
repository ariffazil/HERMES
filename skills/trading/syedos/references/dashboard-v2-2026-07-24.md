# SyedOS Dashboard v2 — 24 Jul 2026

**URLs:**
- **Canonical:** https://syedos.arif-fazil.com/dashboard/ (standalone subdomain)
- **Legacy:** https://arif-fazil.com/sado/ (backward compat)

**Created:** 24 Jul 2026
**Data Sources:** WELL · WEALTH (via HOUND fallback) · GEOX · HOUND
**File path:** `/root/sado/dashboard.html` (37KB source) + `/var/www/html/syedos/dashboard.html` (deployed)

## Tabs

| # | Tab | Content | Data Source |
|---|-----|---------|-------------|
| 1 | 🍳 Nasi Lemak | 3-day sales summary (19/7, 20/7, 22/7), bar chart orders vs sold, doughnut variant mix, per-location breakdown | CSV files in `/root/sado/data/` |
| 2 | 📈 XAUUSD | Live gold $4,001 (RSI 37.81), DXY 100.7, Brent $100.72, WELL HOLD verdict, key S/R levels | HOUND web search (WEALTH bridge was down) |
| 3 | 🧠 Organ Intel | WELL vitality gate (H_WELL critical, M_WELL strained, G_WELL coherent, C_WELL high-risk), WEALTH market snapshot, GEOX registry PASS, HOUND cross-engine results | WELL + GEOX + HOUND live tools |
| 4 | 💰 Accounting | Pricing table, margin chart, P&L summary, action items | Static data from `/root/sado/data/` |
| 5 | 📍 Locations | All 10 locations with type, kedai count, performance badges | Static data |

## Organs Used (24 Jul 2026)

| Organ | Tool | Result | Verdict |
|-------|------|--------|---------|
| **WELL** | `well_validate_vitality` | H_WELL CRITICAL (score 8.6), M_WELL STRAINED (swap thrashing), G_WELL COHERENT, C_WELL HIGH-RISK | 🟡 HOLD — peace condition false |
| **WELL** | `well_assess_homeostasis` (fatigue) | LIMITED — no biometric overrides, cannot assess | 🟡 INSUFFICIENT CONTEXT |
| **WELL** | `well_registry_status` | 8/8 intended → 14 callable, 0 phantom | ✅ REGISTRY_PASS |
| **WEALTH** | `capital_market` (gold/oil/FX) | SESSION_BRIDGE_UNAVAILABLE — arifOS bridge timed out | ❌ BRIDGE DOWN |
| **GEOX** | `geox_surface_status` | P0_IDENTITY_PROPAGATION — anonymous actor blocked | ❌ IDENTITY REQUIRED |
| **GEOX** | `geox_workspace` | P0_IDENTITY_PROPAGATION — evidence lane blocked | ❌ IDENTITY REQUIRED |
| **HOUND** | `mcp_smart_search` | 5 results: XAUUSD, Brent $100, DXY 100.7, GOOGL $317.69, FBM KLCI 1,714 | ✅ ACTIVE |
| **HOUND** | `mcp_smart_fetch` | Full gold TA article (PriceONN) — RSI 37.81, support $3,991, MACD bearish | ✅ FETCHED |

## XAUUSD Market Context (24 Jul 2026)

- **Price:** $4,001.21 (testing critical support, -1.46% day)
- **RSI (1H):** 37.81 (oversold — potential bounce zone)
- **DXY:** 100.70 (+0.21%, strengthening — gold headwind)
- **Brent:** $100.72 (+4.5%, Houthi Red Sea tanker strike)
- **GOOGL:** $317.69 reg close (-7%), $319.01 after-hours (+0.42%)
- **FBM KLCI:** 1,714.59 (+0.19% on 23 Jul)
- **Key Support:** $3,991.80 (critical), $3,976.78 (breakdown level)
- **Strategy:** TUNGGU — wait for bullish confirmation candle at 61.8% Fib rejection

## Deployment History

### Phase 1 — arif-fazil.com/sado/ (subpath)
1. `handle /sado/*` block added to `/etc/caddy/Caddyfile`
2. Files deployed to `/var/www/html/arif/sado/`
3. Caddy reloaded: `caddy validate && caddy reload`

### Phase 2 — syedos.arif-fazil.com (standalone subdomain)
1. Cloudflare DNS A record added via API for `syedos.arif-fazil.com` → VPS IP
2. Caddy vhost added to `/etc/caddy/Caddyfile`
3. Let's Encrypt cert auto-issued (HTTP-01 via Cloudflare)
4. Files at `/var/www/html/syedos/` (landing index.html + dashboard.html)

## Audit & Loop Multimodal Checklist

When user says "audit and loop multimodal capabilities" — systematically check:

| Capability | What to check | Fix pattern |
|------------|---------------|-------------|
| 📷 **Image** | Does the page have the person's photo? Placeholder? Icons? | Copy from source (`/root/.hermes/cache/images/`), embed with `<img>`, 644 perms |
| 📊 **Charts** | Are there data visualisations? Chart.js? matplotlib? | Add `<canvas>` + Chart.js from CDN. CSP must allow `cdn.jsdelivr.net`. |
| 🔊 **Audio** | Voice notes for Syed? edge-tts available? | Generate with `edge-tts --voice ms-MY-OsmanNeural --rate=-5% --write-media /path/file.ogg --text "..."` |
| 🎮 **Interactive** | Tabs? Clickable cards? Hover states? Transitions? | CSS tabs via `display: none/block`, `onclick`, hover effects |
| 📱 **Responsive** | Mobile? Desktop breakpoints? | `@media (max-width: 768px)` and `480px` |
| 🔗 **Links** | External links to arif-fazil.com? Should be removed. | User preference: "Jangan link dengan main site." Keep all URLs self-contained. |
| 💬 **Language** | Any federation jargon? BM casual? | Translate: "WELL vitality gate" → "sistem check kesihatan", "H_WELL CRITICAL" → "Awak kritikal" |

## Pitfalls

- **Wrong Caddyfile edited first:** The running config is `/etc/caddy/Caddyfile` not any `.bak`/`.live` copy. Always check `ps aux | grep caddy`.
- **`root * /root/sado` returns 404:** Caddy's `file_server` cannot serve from `/root/` even with correct permissions. Files must be under the vhost's document root with `try_files`.
- **User preference: standalone subdomain over main-site path:** User said "Jangan link dengan main site arif-fazil.com. just share domain." Deploy all user-facing sites under their own subdomain.
- **Cloudflare DNS takes ~1-2 min to propagate:** After adding A record, `curl --resolve` works immediately for testing but public DNS lags.
- **SSL handshake fails initially:** Caddy needs ~5 seconds to obtain Let's Encrypt cert via HTTP-01 challenge. Check `journalctl -u caddy | grep syedos` for "certificate obtained successfully".
