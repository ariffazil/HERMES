# SyedOS Website — Build Reference

> Built: 2026-07-24 · URL: https://syedos.arif-fazil.com

## Architecture

Standalone subdomain with its own Caddy vhost. NOT a path under arif-fazil.com.

```
Cloudflare DNS A record: syedos → 72.62.71.199 (proxied, TTL auto)
Caddy vhost: syedos.arif-fazil.com
Root: /var/www/html/syedos/
SSL: Let's Encrypt (auto via Caddy ACME)
```

## Files

| File | Purpose |
|------|---------|
| `index.html` | Landing page — Syed's golden circle photo, animated rings, voice player, 3 link cards |
| `dashboard.html` | Full dashboard — 5 tabs: Nasi Lemak, Emas, Pasaran, Kesihatan, Lokasi |
| `syed-golden.jpg` | Syed's photo from the golden circle aesthetic (source: Telegram) |
| `welcome.ogg` | Voice note in ms-MY-OsmanNeural (generated via edge-tts) |

## Critical Rules

1. **BM casual only** — NO federation jargon. No 'organs', 'vitality gate', 'substrates', 'registry'.
   Translate: WELL→sistem check kesihatan, WEALTH→market update, GEOX→lokasi/federation status.
2. **No external links** — everything self-contained within syedos domain. Don't link to arif-fazil.com paths.
3. **Syed's photo** — golden circle aesthetic. Source: `/root/.hermes/cache/images/img_e6c7bd999c4e.jpg`
4. **Voice notes** — `edge-tts --voice ms-MY-OsmanNeural --rate=-5%` for Syed-specific messages.

## Caddy Setup

```caddyfile
syedos.arif-fazil.com {
    import tls_origin
    encode zstd gzip
    root * /var/www/html/syedos
    
    handle /dashboard/* {
        try_files /dashboard.html /index.html
        file_server
    }
    
    handle {
        try_files {path} {path}/index.html /index.html
        file_server
    }
}
```

## Cloudflare DNS

```bash
# Add A record via API
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"syedos","content":"72.62.71.199","ttl":120,"proxied":true}'
```

## Dashboard Tabs

1. **Nasi Lemak** — daily summary table, charts (bar + doughnut), per-location breakdown
2. **Emas & Trading** — XAUUSD levels, RSI, signal verdict, DXY context
3. **Pasaran** — Wall Street, oil, Bursa Malaysia updates
4. **Kesihatan** — WELL-derived readiness (translated to BM: 'awak dah 6 sesi, had cuma 2')
5. **Lokasi** — all 10 locations + pricing table + margin chart

## Multimodal Checklist

- [x] Image (Syed's photo)
- [x] Charts (Chart.js bars, doughnut)
- [x] Audio (welcome.ogg voice note)
- [x] Interactive tabs
- [x] Mobile responsive
