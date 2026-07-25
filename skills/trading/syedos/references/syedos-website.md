# SyedOS Website — Build Reference

> Built: 2026-07-24 · Upgraded: 2026-07-25 (TradingView + Live Gold API + Temporal Intelligence)
> URL: https://syedos.arif-fazil.com

## Architecture

Standalone subdomain with its own Caddy vhost. Single-page HTML (no build step).

```
Cloudflare DNS A record: syedos → 72.62.71.199 (proxied, TTL auto)
Caddy vhost: syedos.arif-fazil.com
Root: /var/www/html/syedos/
SSL: Let's Encrypt (auto via Caddy ACME)
```

## Files

| File | Purpose |
|------|---------|
| `index.html` | **Single page** — profile, live MYT clock, stats, nasi lemak tracking (ringkasan + prestasi + harga charts), EMAS & TRADING (TradingView chart + gold API + S/R + signal), Market data, upload panel, footer |
| `syed-golden.jpg` | Syed's photo from the golden circle aesthetic (source: Telegram) |
| `welcome.ogg` | Voice note in ms-MY-OsmanNeural |

## Features

### 1. Live MYT Clock ⏰
- Pulsing green dot + `HH:MM:SS MYT · UTC+8`
- Updates every 1 second via JS
- Also updates `<meta name="temporal:localtime">` for agent scrapers

### 2. TradingView XAUUSD Candlestick Chart 📈
- Embedded via `https://s3.tradingview.com/tv.js`
- Symbol: `OANDA:XAUUSD`, interval: 60min
- Dark theme, MYT timezone
- Interactive (zoom, scroll, timeframes)
- EMAS section open by default

### 3. Live Gold Price 🥇
- Fetches from `https://api.gold-api.com/price/XAU` (no API key needed)
- CORS: `Access-Control-Allow-Origin: *`
- Auto-refresh every 60 seconds
- Updates stat card value + change badge (⬆/⬇ %)

### 4. Temporal Intelligence 🧠
Meta tags for AI/scrapers:
```html
<meta name="temporal:timezone" content="Asia/Kuala_Lumpur">
<meta name="temporal:offset" content="UTC+8">
<meta name="temporal:localtime" id="meta-tz" content="ISO8601">
<meta name="dc.date" content="YYYY-MM-DD">
<meta property="article:modified_time" content="ISO8601">
```

### 5. Charts (Nasi Lemak)
- Chart.js bar chart (daily order vs sales)
- Chart.js doughnut (variant distribution: mata/rebus/dadar)
- Chart.js bar (buy vs sell price comparison)

### 6. Receipt Upload Panel 📸
- FAB camera button → upload panel slide-up
- Fields: image file, location, date, type (order/baki/receipt)
- POSTs to `/api/upload` endpoint

## Key Patterns

### TradingView Embed
```html
<script src="https://s3.tradingview.com/tv.js"></script>
<div id="tv-chart"></div>
<script>
new TradingView.widget({
  container_id: "tv-chart",
  symbol: "OANDA:XAUUSD",
  interval: "60",
  timezone: "Asia/Kuala_Lumpur",
  theme: "dark",
  style: "1",
  hide_side_toolbar: true, hide_top_toolbar: true,
  autosize: true, locale: "ms_MY",
  disabled_features: ["header_symbol_search"]
});
</script>
```

### Live Price Fetch
```js
async function updateGoldPrice() {
  const r = await fetch('https://api.gold-api.com/price/XAU');
  const j = await r.json();
  // j = { price: 4053.70, currency: "USD", name: "Gold", updatedAt: "..." }
  // Update .stat .n.red text, .tag .red/.green class and text
}
setInterval(updateGoldPrice, 60000);
```

### MYT Clock
```js
function updateMYT() {
  const now = new Date();
  const myt = new Date(now.getTime() + (8 - now.getTimezoneOffset()/60) * 3600000);
  const h = String(myt.getUTCHours()).padStart(2,'0');
  const m = String(myt.getUTCMinutes()).padStart(2,'0');
  const s = String(myt.getUTCSeconds()).padStart(2,'0');
  document.getElementById('myt-clock').textContent = `${h}:${m}:${s}`;
  // Update meta tag
  const iso = myt.toISOString().replace('Z','+08:00').slice(0,19)+'+08:00';
  document.getElementById('meta-tz').setAttribute('content', iso);
}
updateMYT();
setInterval(updateMYT, 1000);
```

## Critical Rules

1. **BM casual only** — NO federation jargon. No 'organs', 'vitality gate', 'substrates', 'registry'.
2. **No external links** — everything self-contained within syedos domain. Don't link to arif-fazil.com paths.
3. **EMAS section open by default** — both `.section-title` and `.section-body` have class `open`.
4. **TradingView pitfall** — headless screenshot browsers block TV iframes. Real browsers (Chrome/Safari/iPhone) work fine.

## Caddy Setup

```caddyfile
syedos.arif-fazil.com {
    import tls_origin
    encode zstd gzip
    root * /var/www/html/syedos
    handle {
        try_files {path} {path}/index.html /index.html
        file_server
    }
}
```

## Cloudflare DNS

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"syedos","content":"72.62.71.199","ttl":120,"proxied":true}'
```

## Daily Ringkasan Cron

Job ID `c651a7e5b758` delivers a BM summary to the SADO group every night at 9pm MYT:
- Fetches live gold price from gold-api.com
- Scrapes dashboard for nasi lemak data
- Sends formatted message with emoji-styled stats
