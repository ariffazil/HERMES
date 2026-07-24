#!/usr/bin/env python3
"""
XAUUSD Daily Signal Chart — OANDA Dark Style, Real Candlesticks
Proven 2026-07-14 pilot. Replace OHLC data + signal levels per day.
Run via: write_file(path) + terminal("python3 {path}")

NOTE: Use write_file() + terminal(), NOT execute_code().
matplotlib/reportlab are in system Python, not in execute_code sandbox.
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

# ═══════════════════════════════════════════════════════════════
# COLORS (OANDA dark style)
# ═══════════════════════════════════════════════════════════════
BG       = '#0d1117'
PANEL_BG = '#161b22'
GRID_C   = '#21262d'
TEXT_C    = '#c9d1d9'
BULL_C    = '#3fb950'   # green hollow candle
BEAR_C    = '#f85149'   # red filled candle
EMA20_C   = '#58a6ff'   # blue
EMA50_C   = '#f0883e'   # orange
BUY_C     = '#238636'   # buy zone green
SELL_C    = '#da3633'   # sell zone red
GOLD_C    = '#d2a8ff'   # current price marker
WARN_C    = '#d29922'   # event warning yellow

# ═══════════════════════════════════════════════════════════════
# EDIT THESE PER DAY — real OHLC from data source
# Get from: web_search("XAUUSD price") + web_extract(DailyForex/Vantage)
# Verify against: TradingEconomics spot price
# ═══════════════════════════════════════════════════════════════
dates_labels = [
    '18 Jun', '19 Jun', '20 Jun', '23 Jun', '24 Jun', '25 Jun', '26 Jun', '27 Jun',
    '30 Jun', '1 Jul', '2 Jul', '3 Jul', '7 Jul', '8 Jul', '9 Jul', '10 Jul', '11 Jul', '14 Jul'
]

# (Open, High, Low, Close) — one tuple per day
ohlc = [
    (4380, 4410, 4355, 4395),
    (4395, 4420, 4370, 4380),
    (4380, 4395, 4340, 4350),
    (4350, 4370, 4310, 4320),
    (4320, 4345, 4280, 4295),
    (4295, 4330, 4270, 4310),
    (4310, 4340, 4260, 4275),
    (4275, 4300, 4240, 4260),
    (4260, 4280, 4200, 4215),
    (4215, 4240, 4180, 4220),
    (4220, 4250, 4190, 4235),
    (4235, 4260, 4200, 4250),
    (4250, 4270, 4180, 4195),
    (4195, 4220, 4150, 4170),
    (4170, 4200, 4100, 4110),
    (4110, 4140, 4060, 4080),
    (4080, 4113, 3987, 3999),
    (3999, 4030, 3985, 4010),
]

# ═══════════════════════════════════════════════════════════════
# SIGNAL LEVELS — edit per day from technical analysis
# Use actual support/resistance, not formulaic offsets
# ═══════════════════════════════════════════════════════════════
CURRENT_PRICE  = 4010
BUY_ZONE_LOW   = 3995
BUY_ZONE_HIGH  = 4015
ENTRY_MID      = (BUY_ZONE_LOW + BUY_ZONE_HIGH) / 2  # R:R base — NOT current price
SL_BUY    = 3975
TARGET1_BUY  = 4060
TARGET2_BUY  = 4110

EVENT_WARNING = "TODAY: CPI + Warsh testify | WAIT for data"
CHART_TITLE   = 'XAUUSD DAILY — 14 Jul 2026 | OANDA Style | Zoomed View'

# ═══════════════════════════════════════════════════════════════
# DERIVED — don't edit below unless changing chart structure
# ═══════════════════════════════════════════════════════════════
opens  = [x[0] for x in ohlc]
highs  = [x[1] for x in ohlc]
lows   = [x[2] for x in ohlc]
closes = [x[3] for x in ohlc]

def ema(data, period):
    result = [data[0]]
    k = 2 / (period + 1)
    for i in range(1, len(data)):
        result.append(data[i] * k + result[-1] * (1 - k))
    return result

ema20 = ema(closes, 20)
ema50 = ema(closes, min(len(closes), 50))

risk_buy = ENTRY_MID - SL_BUY
reward1  = TARGET1_BUY - ENTRY_MID
reward2  = TARGET2_BUY - ENTRY_MID
rr1 = reward1 / risk_buy if risk_buy > 0 else 0
rr2 = reward2 / risk_buy if risk_buy > 0 else 0

# ═══════════════════════════════════════════════════════════════
# CHART
# ═══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(14, 8), facecolor=BG)
gs = gridspec.GridSpec(2, 1, height_ratios=[3.5, 1], hspace=0.08)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)

for ax in [ax1, ax2]:
    ax.set_facecolor(PANEL_BG)
    ax.tick_params(colors=TEXT_C, labelsize=9)
    ax.grid(True, color=GRID_C, alpha=0.5, linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID_C)

# --- Candlesticks ---
x = np.arange(len(ohlc))
candle_width = 0.55

for i in range(len(ohlc)):
    o, h, l, c = opens[i], highs[i], lows[i], closes[i]
    is_bull = c >= o
    color = BULL_C if is_bull else BEAR_C

    # Wick
    ax1.plot([i, i], [l, h], color=color, linewidth=1.2, zorder=2)

    # Body
    body_bottom = min(o, c)
    body_height = max(abs(c - o), 2)  # min 2px for doji visibility

    if is_bull:
        # Green hollow (border only)
        rect = mpatches.FancyBboxPatch(
            (i - candle_width/2, body_bottom), candle_width, body_height,
            boxstyle="round,pad=0.5",
            facecolor='none', edgecolor=BULL_C, linewidth=1.8, zorder=3
        )
    else:
        # Red filled
        rect = mpatches.FancyBboxPatch(
            (i - candle_width/2, body_bottom), candle_width, body_height,
            boxstyle="round,pad=0.5",
            facecolor=BEAR_C, edgecolor=BEAR_C, linewidth=1.2, alpha=0.85, zorder=3
        )
    ax1.add_patch(rect)

# --- EMA lines ---
ax1.plot(x, ema20, color=EMA20_C, linewidth=2.5, alpha=0.9, label='EMA 20', zorder=4)
ax1.plot(x, ema50, color=EMA50_C, linewidth=2.5, alpha=0.9, label='EMA 50', zorder=4)

# --- BUY ZONE ---
ax1.axhspan(BUY_ZONE_LOW, BUY_ZONE_HIGH, alpha=0.15, color=BUY_C, zorder=1)
ax1.axhline(y=BUY_ZONE_LOW, color=BUY_C, linestyle='-', linewidth=2.5, alpha=0.8)
ax1.axhline(y=BUY_ZONE_HIGH, color=BUY_C, linestyle='-', linewidth=2.5, alpha=0.8)
ax1.text(-1.2, BUY_ZONE_LOW + 3, f'BUY\n${BUY_ZONE_LOW}-{BUY_ZONE_HIGH}',
         fontsize=8, color=BUY_C, fontweight='bold', va='bottom',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=BUY_C, alpha=0.9))

# --- Stop losses ---
ax1.axhline(y=SL_BUY, color=BEAR_C, linestyle='-.', linewidth=2, alpha=0.7)
ax1.text(len(ohlc)-0.3, SL_BUY-8, f'SL ${SL_BUY}', fontsize=7.5, color=BEAR_C,
         ha='right', fontweight='bold')

# --- Targets ---
ax1.axhline(y=TARGET1_BUY, color=BULL_C, linestyle=':', linewidth=2, alpha=0.6)
ax1.text(len(ohlc)-0.3, TARGET1_BUY+5, f'T1 ${TARGET1_BUY}', fontsize=7.5,
         color=BULL_C, ha='right', fontweight='bold')
ax1.axhline(y=TARGET2_BUY, color=BULL_C, linestyle=':', linewidth=2, alpha=0.6)
ax1.text(len(ohlc)-0.3, TARGET2_BUY+5, f'T2 ${TARGET2_BUY}', fontsize=7.5,
         color=BULL_C, ha='right', fontweight='bold')

# --- Current price marker ---
ax1.scatter([len(ohlc)-1], [CURRENT_PRICE], color=GOLD_C, s=120, zorder=10,
            edgecolors='white', linewidths=2, marker='o')
ax1.annotate(f'  ${CURRENT_PRICE:,}', xy=(len(ohlc)-1, CURRENT_PRICE),
             xytext=(len(ohlc)+0.5, CURRENT_PRICE),
             fontsize=11, fontweight='bold', color=GOLD_C,
             arrowprops=dict(arrowstyle='->', color=GOLD_C, lw=1.5))

# --- R:R Box (top left) ---
rr_color = BULL_C if rr1 >= 1.5 else WARN_C
ax1.text(0.02, 0.97, f"R:R (BUY) = 1:{rr1:.1f} / 1:{rr2:.1f}",
         transform=ax1.transAxes, fontsize=12, fontweight='bold', color=rr_color,
         va='top', bbox=dict(boxstyle='round,pad=0.5', facecolor=BG,
                             edgecolor=rr_color, alpha=0.95, linewidth=2))

# --- R:R visual arrows (risk down = red, reward up = green) ---
arrow_x = len(ohlc) + 1.5
ax1.annotate('', xy=(arrow_x, SL_BUY), xytext=(arrow_x, ENTRY_MID),
             arrowprops=dict(arrowstyle='->', color=BEAR_C, lw=3))
ax1.text(arrow_x + 0.3, (ENTRY_MID + SL_BUY)/2, f'-${risk_buy}',
         fontsize=9, color=BEAR_C, fontweight='bold', va='center')
ax1.annotate('', xy=(arrow_x, TARGET1_BUY), xytext=(arrow_x, ENTRY_MID),
             arrowprops=dict(arrowstyle='->', color=BULL_C, lw=3))
ax1.text(arrow_x + 0.3, (ENTRY_MID + TARGET1_BUY)/2, f'+${reward1}',
         fontsize=9, color=BULL_C, fontweight='bold', va='center')

# --- Event warning (bottom left) ---
ax1.text(0.02, 0.02, EVENT_WARNING, transform=ax1.transAxes,
         fontsize=9, color=WARN_C, va='bottom',
         bbox=dict(boxstyle='round,pad=0.5', facecolor=BG,
                   edgecolor=WARN_C, alpha=0.95, linewidth=2))

# --- Axes ---
ax1.set_xlim(-2, len(ohlc) + 3.5)
y_min = min(min(lows), SL_BUY) - 20
y_max = max(max(highs), TARGET2_BUY) + 30
ax1.set_ylim(y_min, y_max)
ax1.set_ylabel('XAUUSD ($/oz)', fontsize=10, fontweight='bold', color=TEXT_C)
ax1.set_xticks(range(len(ohlc)))
ax1.set_xticklabels(dates_labels, fontsize=7, rotation=45, ha='right')
ax1.legend(loc='upper right', fontsize=8, facecolor=PANEL_BG, edgecolor=GRID_C,
           labelcolor=TEXT_C)
ax1.set_title(CHART_TITLE, fontsize=13, fontweight='bold', color=GOLD_C, pad=12)

# --- RSI subplot (calculated from OHLC, not hardcoded) ---
def calc_rsi(prices, period=14):
    """Calculate RSI from price array."""
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.zeros(len(prices))
    avg_loss = np.zeros(len(prices))
    if len(gains) < period:
        return np.full(len(prices), 50.0)
    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])
    for i in range(period + 1, len(prices)):
        avg_gain[i] = (avg_gain[i-1] * (period-1) + gains[i-1]) / period
        avg_loss[i] = (avg_loss[i-1] * (period-1) + losses[i-1]) / period
    rs = np.where(avg_loss != 0, avg_gain / avg_loss, 100)
    rsi = 100 - (100 / (1 + rs))
    rsi[:period] = np.nan
    return rsi

rsi_values = calc_rsi(np.array(closes, dtype=float))
rsi_clean = [r if not np.isnan(r) else 50 for r in rsi_values]

bar_colors_rsi = [BULL_C if r > 50 else (BEAR_C if r < 35 else TEXT_C) for r in rsi_clean]
ax2.bar(x, rsi_clean, color=bar_colors_rsi, alpha=0.6, width=0.7)
ax2.axhline(y=70, color=BEAR_C, linestyle=':', linewidth=1, alpha=0.5)
ax2.axhline(y=30, color=BULL_C, linestyle=':', linewidth=1, alpha=0.5)
ax2.axhline(y=50, color=TEXT_C, linestyle=':', linewidth=0.5, alpha=0.3)
ax2.fill_between(range(len(rsi_clean)), 30, 70, alpha=0.03, color=TEXT_C)
ax2.set_ylabel('RSI(14)', fontsize=9, color=TEXT_C)
ax2.set_ylim(15, 85)
ax2.set_yticks([30, 50, 70])

rsi_now = rsi_clean[-1]
rsi_label = 'near oversold' if rsi_now < 35 else ('neutral-low' if rsi_now < 45 else 'neutral')
ax2.annotate(f'RSI: {rsi_now:.0f} ({rsi_label})', xy=(len(rsi_clean)-1, rsi_now),
             xytext=(len(rsi_clean)-5, 22), fontsize=8,
             color=BULL_C if rsi_now < 40 else TEXT_C, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=BULL_C if rsi_now < 40 else TEXT_C, lw=1))

# --- Save ---
output = '/tmp/gold_signal_chart.png'
plt.savefig(output, dpi=200, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f"Chart saved: {output}")
print(f"Size: {os.path.getsize(output)} bytes")
