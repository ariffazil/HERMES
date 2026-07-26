# Gold-API Command Dependencies

Which `fetch_gold.py` commands depend on the `/root/trading` Python package vs which are self-contained.

Proven 2026-07-20 — server had no `/root/trading/` directory; `signal_v2` and `apex` returned HTTP 500.

## Self-Contained (no trading module needed)

| Command | Endpoint | Dependencies | Notes |
|---|---|---|---|
| `ticker` | `/api/gold/ticker` | yfinance, numpy, pandas | Has its own `compute_ema`, `compute_rsi`, `compute_atr`, S/R detection. Returns price, RSI, EMAs, S/R levels, signal. |
| `history` | `/api/gold/history` | yfinance, pandas | Raw OHLCV fetch. |
| `signals` | `/api/gold/signals` | yfinance, numpy, pandas | Built-in signal logic (not engine_v2). |
| `levels` | `/api/gold/levels` | yfinance, numpy, pandas | Built-in S/R detection. |
| `macro` | `/api/gold/macro` | yfinance, numpy, pandas | DXY/yields macro context. |
| `calendar` | `/api/gold/calendar` | requests (ForexFactory JSON API) | Economic calendar. |

## Requires `/root/trading` module

| Command | Endpoint | Imports from | Fails with |
|---|---|---|---|
| `apex` | `/api/gold/apex` | `trading.core.config`, `trading.core.models`, `trading.signals.scanner`, `trading.signals.apex_predictor` | `No module named 'trading'` |
| `signal_v2` | `/api/gold/signal_v2` | `trading.core.config`, `trading.core.models`, `trading.signals.engine_v2`, `trading.signals.scanner`, `trading.signals.regime`, `trading.risk.position_sizer`, `trading.governance.gate` | `No module named 'trading'` |

## Detection

```bash
# Quick: check if signal_v2 works
curl -sf localhost:3456/api/gold/signal_v2 && echo "OK" || echo "DOWN (exit=$?)"

# Confirm cause
journalctl -u gold-api --no-pager -n 5 | grep -i "No module named"

# Check if trading dir exists
test -d /root/trading && echo "EXISTS" || echo "MISSING"
```

## Fix

The `trading` module must be deployed to `/root/trading/` on the server. The gold-api systemd service also needs `PYTHONPATH=/root` in its environment:

```ini
# /etc/systemd/system/gold-api.service
[Service]
Environment=PYTHONPATH=/root
```

Then: `systemctl daemon-reload && systemctl restart gold-api`
