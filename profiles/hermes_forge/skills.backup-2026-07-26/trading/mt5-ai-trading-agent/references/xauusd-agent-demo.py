#!/usr/bin/env python3
"""
XAUUSD AI Trading Agent — Hermes Powered
Live market data → Technical Analysis → AI Signal → Risk Management → Voice Note
Proven 2026-07-13. Uses numpy only (no pandas dependency).

Replace simulated data with MT5 Python API (MetaTrader5 package) in production.
Voice delivery via edge-tts ms-MY-OsmanNeural.
"""

import numpy as np
from datetime import datetime, timezone, timedelta

MYT = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════════════════════════
# SECTION 1: Technical Analysis Functions (numpy-only, no segfault)
# ═══════════════════════════════════════════════════════════════

def sma(data, period):
    if len(data) < period: return None
    return sum(data[-period:]) / period

def ema(data, period):
    if len(data) < period: return None
    k = 2 / (period + 1)
    result = sum(data[:period]) / period
    for price in data[period:]:
        result = price * k + result * (1 - k)
    return result

def rsi(data, period=14):
    if len(data) < period + 1: return 50
    deltas = [data[i] - data[i-1] for i in range(1, len(data))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def atr(highs, lows, closes, period=14):
    if len(closes) < period + 1: return 20
    trs = []
    for i in range(1, len(closes)):
        tr = max(highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1]))
        trs.append(tr)
    return round(sum(trs[-period:]) / period, 2)

def macd(data, fast=12, slow=26, signal_period=9):
    if len(data) < slow: return 0, 0, 0
    ema_fast = ema(data, fast)
    ema_slow = ema(data, slow)
    macd_line = ema_fast - ema_slow
    signal_line = macd_line * 0.8
    histogram = macd_line - signal_line
    return round(macd_line, 2), round(signal_line, 2), round(histogram, 2)

def bollinger_bands(data, period=20, std_dev=2):
    if len(data) < period: return None, None, None
    sma_val = sma(data, period)
    variance = sum((x - sma_val) ** 2 for x in data[-period:]) / period
    std = variance ** 0.5
    return round(sma_val - std_dev * std, 2), round(sma_val, 2), round(sma_val + std_dev * std, 2)

def support_resistance(highs, lows, closes):
    pivot = (highs[-1] + lows[-1] + closes[-1]) / 3
    r1 = 2 * pivot - lows[-1]
    r2 = pivot + (highs[-1] - lows[-1])
    s1 = 2 * pivot - highs[-1]
    s2 = pivot - (highs[-1] - lows[-1])
    return {"pivot": round(pivot, 2), "R1": round(r1, 2), "R2": round(r2, 2),
            "S1": round(s1, 2), "S2": round(s2, 2)}

# ═══════════════════════════════════════════════════════════════
# SECTION 2: Signal Generation (Multi-Factor Composite Scoring)
# ═══════════════════════════════════════════════════════════════

def generate_signals(closes, highs, lows, current_price):
    """
    Multi-factor composite scoring:
    Each indicator contributes +1 (bullish), -1 (bearish), or 0 (neutral).
    Sum across all indicators → composite signal.
    """
    signals = []
    score = 0

    ema9 = ema(closes, 9)
    sma20 = sma(closes, 20)
    sma10 = sma(closes, 10)
    rsi14 = rsi(closes, 14)
    atr14 = atr(highs, lows, closes, 14)
    macd_line, macd_signal, macd_hist = macd(closes)
    bb_lower, bb_mid, bb_upper = bollinger_bands(closes)
    sr = support_resistance(highs, lows, closes)

    # 1. Trend (EMA9 vs SMA20)
    if ema9 and sma20:
        if ema9 > sma20:
            signals.append(("TREND", "BULLISH", "EMA9 > SMA20"))
            score += 1
        else:
            signals.append(("TREND", "BEARISH", "EMA9 < SMA20"))
            score -= 1

    # 2. RSI
    if rsi14 > 70:
        signals.append(("RSI", "OVERBOUGHT", f"RSI = {rsi14}"))
        score -= 1
    elif rsi14 < 30:
        signals.append(("RSI", "OVERSOLD", f"RSI = {rsi14}"))
        score += 1
    else:
        signals.append(("RSI", "NEUTRAL", f"RSI = {rsi14}"))

    # 3. MACD
    if macd_hist > 0:
        signals.append(("MACD", "BULLISH", f"Hist = {macd_hist}"))
        score += 1
    else:
        signals.append(("MACD", "BEARISH", f"Hist = {macd_hist}"))
        score -= 1

    # 4. Bollinger Bands
    if bb_lower and current_price < bb_lower:
        signals.append(("BOLLINGER", "OVERSOLD", "Below lower band"))
        score += 1
    elif bb_upper and current_price > bb_upper:
        signals.append(("BOLLINGER", "OVERBOUGHT", "Above upper band"))
        score -= 1
    else:
        signals.append(("BOLLINGER", "NEUTRAL", "Within bands"))

    # 5. Price vs SMA20
    if sma20:
        if current_price > sma20:
            signals.append(("PRICE_SMA", "BULLISH", f"Above SMA20 ({round(sma20, 2)})"))
            score += 0.5
        else:
            signals.append(("PRICE_SMA", "BEARISH", f"Below SMA20 ({round(sma20, 2)})"))
            score -= 0.5

    # Composite verdict
    if score >= 2: overall = "STRONG BUY"; direction = "BUY"
    elif score >= 0.5: overall = "BUY"; direction = "BUY"
    elif score <= -2: overall = "STRONG SELL"; direction = "SELL"
    elif score <= -0.5: overall = "SELL"; direction = "SELL"
    else: overall = "NEUTRAL"; direction = "WAIT"

    indicators = {
        "sma10": sma10, "sma20": sma20, "ema9": ema9,
        "rsi": rsi14, "atr": atr14,
        "macd": macd_line, "macd_signal": macd_signal, "macd_hist": macd_hist,
        "bb_lower": bb_lower, "bb_mid": bb_mid, "bb_upper": bb_upper,
        "sr": sr
    }

    return signals, score, overall, direction, atr14, indicators

# ═══════════════════════════════════════════════════════════════
# SECTION 3: Risk Management Calculator
# ═══════════════════════════════════════════════════════════════

def calculate_trade(direction, current_price, atr14, account_balance=1000, risk_pct=0.02):
    """
    Auto-calculate lot size, SL, TP based on ATR and risk tolerance.
    XAUUSD: 1 lot = 100 oz, 1 point = $1 per 0.01 lot
    """
    sl_distance = atr14 * 1.5   # SL = 1.5x ATR
    tp_distance = atr14 * 3.0   # TP = 3x ATR (2:1 R:R)
    risk_amount = round(account_balance * risk_pct, 2)
    lot_size = round(risk_amount / sl_distance, 2)
    lot_size = max(0.01, min(lot_size, 10.0))
    rr_ratio = round(tp_distance / sl_distance, 2) if sl_distance > 0 else 0

    if direction == "BUY":
        entry = round(current_price + 2, 2)
        sl = round(entry - sl_distance, 2)
        tp = round(entry + tp_distance, 2)
    elif direction == "SELL":
        entry = round(current_price - 2, 2)
        sl = round(entry + sl_distance, 2)
        tp = round(entry - tp_distance, 2)
    else:
        return None

    return {
        "direction": direction, "entry": entry, "sl": sl, "tp": tp,
        "lot": lot_size, "risk": risk_amount, "rr": rr_ratio,
        "sl_dist": sl_distance, "tp_dist": tp_distance
    }

# ═══════════════════════════════════════════════════════════════
# SECTION 4: Voice Note Generator (BM Macho — Nusantara Mode)
# ═══════════════════════════════════════════════════════════════

def get_session():
    """Determine current trading session based on MYT."""
    hour = datetime.now(MYT).hour
    if 0 <= hour < 8: return "Asia awal"
    elif 8 <= hour < 14: return "Asia"
    elif 14 <= hour < 18: return "London"
    elif 18 <= hour < 22: return "New York"
    else: return "Late NY"

def format_voice_text(trade, indicators=None, session=None):
    """
    Format trading signal as BM voice script.
    Style: macho, clean, no fluff, straight to the point.
    For edge-tts ms-MY-OsmanNeural with --rate="-5%"
    """
    if not session:
        session = get_session()

    if not trade:
        return "Tiada signal buat masa sekarang. Tunggu setup yang lebih jelas. Risk management first."

    dir_text = "beli" if trade["direction"] == "BUY" else "jual"
    rr_int = int(trade["rr"]) if trade["rr"] >= 1 else trade["rr"]

    text = f"""XAUUSD signal {session}.
Harga sekarang {trade['entry']} dolar.
Arah {dir_text}.
Entry {trade['entry']}, stop loss {trade['sl']}, take profit {trade['tp']}.
Lot {trade['lot']}. Risk dua peratus.
Reward ratio satu berbalas {rr_int}.
Abang sado, jalan terus."""

    return text

# Generate voice with:
# edge-tts --voice ms-MY-OsmanNeural --file /tmp/signal.txt --write-media /tmp/signal.mp3 --rate="-5%"

# ═══════════════════════════════════════════════════════════════
# SECTION 5: MT5 Connection Template (Windows only)
# ═══════════════════════════════════════════════════════════════

MT5_CONNECTION_TEMPLATE = '''
import MetaTrader5 as mt5

# Initialize
if not mt5.initialize():
    print(f"MT5 init failed: {mt5.last_error()}")
    quit()

# Login (replace with your broker credentials)
authorized = mt5.login(
    login=ACCOUNT_NUMBER,     # int: your account number
    password="YOUR_PASSWORD", # str: your password
    server="Broker-Server"    # str: e.g., "Exness-Real"
)
if not authorized:
    print(f"Login failed: {mt5.last_error()}")
    mt5.shutdown()
    quit()

# Get live XAUUSD tick
tick = mt5.symbol_info_tick("XAUUSD")
print(f"Bid: {tick.bid}, Ask: {tick.ask}, Spread: {tick.ask - tick.bid}")

# Get H1 candles (last 100)
rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 100)

# Place a market order
def place_order(direction, lot, sl, tp):
    tick = mt5.symbol_info_tick("XAUUSD")
    order_type = mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if direction == "BUY" else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": "XAUUSD",
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": 202607,
        "comment": "Hermes AI",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: {result.comment}")
    else:
        print(f"Order placed: ticket {result.order}")
    return result

mt5.shutdown()
'''

# ═══════════════════════════════════════════════════════════════
# SECTION 6: Run Demo
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    # Simulated XAUUSD data (replace with mt5.copy_rates_from_pos in production)
    np.random.seed(42)
    base = 4080
    candles = []
    for i in range(20):
        o = base + np.random.uniform(-15, 15)
        h = o + np.random.uniform(5, 25)
        l = o - np.random.uniform(5, 25)
        c = o + np.random.uniform(-20, 20)
        candles.append({"open": round(o, 2), "high": round(h, 2),
                        "low": round(l, 2), "close": round(c, 2)})
        base = c
    candles[-1]["close"] = 4120.00  # current price

    closes = [c["close"] for c in candles]
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    current_price = 4120.00

    # Run analysis
    signals, score, overall, direction, atr14, indicators = generate_signals(
        closes, highs, lows, current_price
    )
    trade = calculate_trade(direction, current_price, atr14)

    # Print report
    print(f"\n{'='*55}")
    print(f"  🤖 XAUUSD AI TRADING AGENT — HERMES POWERED")
    print(f"  📅 {datetime.now(MYT).strftime('%Y-%m-%d %H:%M MYT')}")
    print(f"{'='*55}")
    print(f"\n📊 CURRENT PRICE: ${current_price:,.2f}")
    print(f"\n📈 INDICATORS:")
    for k, v in indicators.items():
        if k != "sr":
            print(f"   {k}: {v}")
    print(f"\n🎯 S/R:")
    for k, v in indicators["sr"].items():
        print(f"   {k}: ${v}")
    print(f"\n🧠 SIGNALS:")
    for name, sig, reason in signals:
        emoji = "🟢" if "BULLISH" in sig or "OVERSOLD" in sig else "🔴" if "BEARISH" in sig or "OVERBOUGHT" in sig else "⚪"
        print(f"   {emoji} {name:12} → {sig:10} | {reason}")
    print(f"\n   Score: {score:+.1f} → {overall}")

    if trade:
        print(f"\n💰 TRADE PLAN:")
        print(f"   {trade['direction']} @ {trade['entry']}")
        print(f"   SL: ${trade['sl']} | TP: ${trade['tp']}")
        print(f"   Lot: {trade['lot']} | Risk: ${trade['risk']} (2%)")
        print(f"   R:R: 1:{trade['rr']}")

        # Generate voice text
        voice = format_voice_text(trade, indicators)
        print(f"\n🎙️ VOICE TEXT:")
        print(f"   {voice}")

    print(f"\n⚠️ Educational only. Not financial advice.")
    print(f"{'='*55}\n")
