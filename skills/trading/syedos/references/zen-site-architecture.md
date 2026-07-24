# SyedOS Site Architecture (as of 24 Jul 2026)

## Domain
- **syedos.arif-fazil.com** — standalone subdomain, not linked to main site
- Cloudflare DNS A record: `72.62.71.199` (proxied)
- Let's Encrypt SSL via Caddy auto-ACME

## Site Structure
```
syedos.arif-fazil.com/
├── index.html        (16KB — single zen page, all content in one scroll)
├── syed-golden.jpg   (Syed's golden circle portrait)
└── welcome.ogg       (agent voice note in ms-MY-OsmanNeural)
```

## Architecture

### Single Zen Page
- Profile section: Syed's photo + name + voice player
- Stats row: nasi lemak count, revenue, XAUUSD price
- Sections (scrollable, no tabs):
  - 🍳 Nasi Lemak — summary table + charts + performance rankings
  - 🥇 Emas & Trading — XAUUSD price, levels, RSI, DXY, signal verdict
  - 📊 Pasaran — GOOGL, Brent, KLCI, USD/MYR updates
  - 📍 Lokasi — all 10 locations ranked by performance
  - 💰 Harga & Untung — pricing table + margin chart
- Floating action button (📸) for receipt upload inline panel

### Upload Pipeline
1. User clicks 📸 FAB → inline panel slides up
2. Drag-drop or phone camera capture
3. Fill: location, date, type (order/baki/resit)
4. POST multipart form → Caddy → localhost:18900
5. Python HTTPServer saves file + metadata `.json` + creates `.pending` flag
6. Cron watcher (every 5 min) detects `.pending` → processes receipts → updates → removes flag

### Backend Services
- **Upload server**: Python HTTPServer on 127.0.0.1:18900
- **systemd unit**: `syedos-upload.service`
- **Cron**: Hermes cron job `21dc4219866f` — SyedOS Receipt Watcher

## Design Principles (User Preferences)
- **Zero federation jargon** — no "WEALTH", "WELL", "GEOX", "organ", "vitality gate", "substrate", "registry" in user-facing content
- **Bahasa Melayu casual** — "Abang Sado", "hari ni rehat", "emas uji support", "agent sayang kau"
- **One page, no tabs** — everything in one scroll, no sub-navigation
- **Floating action button** — upload available from any scroll position
- **Dark theme** — gold (#f0a500) accents on #0a0a0f background
- **Phone-first** — responsive media queries, 480px breakpoint

## Removed Pages (redirect to /)
- `/dashboard/` → 301 to `/`
- `/upload/` → 301 to `/`
