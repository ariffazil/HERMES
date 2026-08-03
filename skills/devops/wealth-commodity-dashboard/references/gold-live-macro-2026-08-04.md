# Gold Dashboard — Live Macro Fix (2026-08-04)

Session record for the arif-fazil.com/gold/ three-layer fix. Main skill: SKILL.md.

## What was fixed

1. **JS scope bug** — `const diff` declared inside `if (lastPrice) {…}` but referenced outside → ReferenceError killed RSI/EMA/bias/verdict every tick. Fix: hoist `let diff = 0` before the block in `/var/www/html/gold/index.html`.
2. **Futures-vs-spot desync** — backend fed GC=F (COMEX futures, ~$50-60 carry premium over spot) while banner showed spot → chart desynced ~$56 from banner and from MT5 reality. Fix: `fetch_gold.py` primary source = Binance PAXGUSDT spot klines; yfinance PAXG-USD → GC=F as fallbacks only. Then `rm /tmp/gold_cache/*.json` + `systemctl restart gold-api`.
3. **Hardcoded USDMYR 4.35 → live 4.09** — patched in TWO places (the `driverExtra` channel):
   - `/var/www/html/gold/index.html` — `window.ZEN_MARKET.driverExtra` definition reads `macro.usmyr`
   - `/var/www/html/_shared/zen-market.js` — consumer passes `snapshot.macro` into `driverExtra(data, fmt, snapshot.macro)`

RM/gram math: `price_usd × usmyr ÷ 31.1035` (1 troy oz = 31.1035 g). At $4,037.69 × 4.09 → RM 530.95/gram.

## Verification (what actually worked)

```bash
# Single best health probe — snapshot bundles ticker+macro+levels+coherence hash
curl -s https://arif-fazil.com/gold/api/snapshot | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d['ticker']['price'], d['ticker'].get('rsi'), d['macro']['usmyr'], d['coherence_id'][:12])"

# Backend service + via-Caddy ticker
systemctl is-active gold-api
curl -s https://arif-fazil.com/gold/api/ticker | head -c 300
```

Observed 2026-08-04 00:45 MYT: price 4037.69, RSI 37, usmyr 4.09, coherence hash present. Page rendered: banner $4,037.69, USD/MYR 4.0900 in macro panel, DXY 99.96, US10Y 4.69%, VIX 15.56, Silver $57.79, GSR 69.9, ● LIVE timestamp.

Verified live API paths via arif-fazil.com vhost (Caddy strips `/gold` → localhost:3456): `/gold/api/snapshot`, `/gold/api/ticker`, `/gold/api/macro`, `/gold/api/levels`.

## Debug techniques that earned their keep

- **Silent-exception localization:** elements render sequentially in one function; if a downstream element still shows `—` while upstream ones are populated, a silent exception landed between them. Read the code between the last-rendered line and the broken line instead of guessing.
- **API ground truth via server-side curl.** `browser_console` expressions block network fetches (sensitive primitives), so verify API payloads with curl on the VPS and use the browser only for rendered state.
- **After a gateway restart** the browser session resets to about:blank — re-navigate, then wait ≥5s for JS boot before asserting anything. Early snapshots showing `—` everywhere are a race, not a bug.

## Unresolved (known issue)

`pulseDriver` line (below S/R chips) still shows `—` instead of `RSI 37.0 — NEUTRAL · XAU/MYR: RM 530.95/gram · TF: 1H levels, 4H regime`. Macro data arrives (usmyr renders in the macro panel), so it's a silent exception between zen-market.js line ~505 (`pulseTimestamp` renders fine) and ~524 (`pulseDriver`). Localized but not yet fixed — start there next time.
