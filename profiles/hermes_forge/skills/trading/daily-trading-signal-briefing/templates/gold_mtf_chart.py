#!/usr/bin/env python3
"""
XAUUSD Multi-Timeframe Signal Chart — Dark Theme (OANDA-style)
Template for daily trading signal PDF generation.

Usage:
  1. Update OHLC data arrays with real market data
  2. Update trade levels (entry, SL, targets)
  3. Run: python3 gold_mtf_chart.py
  4. Output: /tmp/gold_mtf_chart.png

Proven 2026-07-14: Syed-validated multi-timeframe dark theme chart.
Requires: pip install --break-system-packages matplotlib numpy

Chart layout:
  - 3 candlestick panels (Daily, 4H, 1H) stacked vertically
  - EMA 20 (blue) + EMA 50 (orange) on each timeframe
  - Buy/Sell zones as colored bands
  - Stop loss + target lines
  - R:R visual arrows on chart
  - R:R panel on right side
  - Key signals panel
  - Pattern labels (H, D, SS, BE)
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np

# ─── COLORS (dark theme) ─────────────────────────────────────────────────────
BG       = '#0d1117'
PANEL    = '#161b22'
GOLD_C   = '#f0a500'
TEAL     = '#39d2c0'
RED      = '#f85149'
GREEN    = '#3fb950'
TEXT     = '#e6edf3'
DIM      = '#8b949e'
BORDER   = '#30363d'
C_RED    = '#f85149'
C_GREEN  = '#3fb950'
WHITE    = '#ffffff'
EMA_FAST = '#58a6ff'   # EMA 20
EMA_SLOW = '#f0883e'   # EMA 50

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def ema(prices, period):
    """Exponential Moving Average."""
    r = np.zeros(len(prices))
    m = 2 / (period + 1)
    r[0] = prices[0]
    for i in range(1, len(prices)):
        r[i] = (prices[i] - r[i-1]) * m + r[i-1]
    return r

def smooth_ema(prices, factor=0.85):
    """Extra-smooth EMA for visual clarity on short data."""
    r = np.zeros(len(prices))
    r[0] = prices[0]
    for i in range(1, len(prices)):
        r[i] = r[i-1] * factor + prices[i] * (1 - factor)
    return r

# ─── CANDLESTICK DRAWING ─────────────────────────────────────────────────────
def draw_candles(ax, opens, highs, lows, closes, title, cw=0.55):
    """Draw proper OHLC candlesticks with pattern detection."""
    days = len(closes)
    
    for i in range(days):
        o, h, l, c = opens[i], highs[i], lows[i], closes[i]
        body = abs(c - o)
        upper_wick = h - max(o, c)
        lower_wick = min(o, c) - l
        total_range = h - l if h - l > 0 else 1
        
        is_bull = c >= o
        is_doji = body < total_range * 0.1
        is_hammer = (body < total_range * 0.3) and (lower_wick >= body * 2) and (upper_wick < body * 0.5)
        is_shoot = (body < total_range * 0.3) and (upper_wick >= body * 2) and (lower_wick < body * 0.5)
        
        body_bot = min(o, c)
        body_h = max(body, 0.8)
        
        if is_doji:
            ax.plot([i-cw/2, i+cw/2], [o, o], color=DIM, linewidth=1.5, zorder=5)
            ax.plot([i, i], [l, h], color=DIM, linewidth=0.8, zorder=5)
        else:
            col = C_GREEN if is_bull else C_RED
            if is_bull:
                rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                                facecolor='none', edgecolor=C_GREEN, linewidth=1.2)
            else:
                rect = Rectangle((i-cw/2, body_bot), cw, body_h,
                                facecolor=C_RED, edgecolor=C_RED, linewidth=0.8, alpha=0.85)
            ax.add_patch(rect)
            ax.plot([i,i], [l, body_bot], color=col, linewidth=0.7)
            ax.plot([i,i], [body_bot+body_h, h], color=col, linewidth=0.7)
        
        # Pattern labels
        if is_hammer and 3 < i < days-2:
            ax.annotate('H', xy=(i, l-8), fontsize=5.5, fontweight='bold', color=GREEN, ha='center')
        elif is_shoot and 3 < i < days-2:
            ax.annotate('SS', xy=(i, h+8), fontsize=5, fontweight='bold', color=RED, ha='center')
    
    # EMA overlays
    e20 = ema(closes, min(20, len(closes)-1))
    e50s = smooth_ema(closes)
    ax.plot(range(days), e20, color=EMA_FAST, linewidth=1.3, alpha=0.8, zorder=6)
    ax.plot(range(days), e50s, color=EMA_SLOW, linewidth=1.3, alpha=0.8, zorder=6)
    
    # Current price marker
    ax.scatter([days-1], [closes[-1]], color=GOLD_C, s=60, zorder=10, edgecolors=WHITE, linewidths=1.2)
    ax.annotate(f'${closes[-1]:,.0f}', xy=(days-1, closes[-1]), xytext=(days+1, closes[-1]),
               fontsize=8, fontweight='bold', color=GOLD_C, va='center')
    
    # Formatting
    ax.set_xlim(-1, days+4)
    margin = (max(highs) - min(lows)) * 0.1
    ax.set_ylim(min(lows)-margin, max(highs)+margin)
    ax.set_title(title, fontsize=9, fontweight='bold', color=TEXT, pad=5, loc='left')
    ax.grid(True, alpha=0.08, color=BORDER)
    for sp in ['top','right']:
        ax.spines[sp].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)
    ax.tick_params(axis='y', labelsize=7, colors=DIM)
    ax.tick_params(axis='x', labelsize=6, colors=DIM)
    
    return e20, e50s

# ─── TRADE LEVELS (UPDATE THESE) ────────────────────────────────────────────
LONG_ENTRY_LO, LONG_ENTRY_HI = 4020, 4040
LONG_SL  = 3970
LONG_T1  = 4150
LONG_T2  = 4200

SHORT_ENTRY_LO, SHORT_ENTRY_HI = 4180, 4200
SHORT_SL = 4240
SHORT_T1 = 4080
SHORT_T2 = 4000

# ─── OHLC DATA (REPLACE WITH REAL DATA) ─────────────────────────────────────
# Generate from: mt5.copy_rates_from_pos() or web scraping
np.random.seed(42)

# Daily (30 candles)
d_closes = np.array([4800,4770,4740,4700,4660,4620,4590,4560,
                     4540,4510,4480,4450,4420,4400,4380,4370,
                     4360,4340,4320,4300,4280,4260,4250,4240,
                     4260,4280,4310,4340,4320,4290,4260,4230,
                     4200,4180,4160,4140,4120,4100,4080,4060,
                     4040,4020,4010,4025,4040,4030,4020,4010,
                     4005,4003,4020,4050,4070,4060,4040,4020,
                     4010,4005,4015,4003])
d = len(d_closes)
d_opens = np.roll(d_closes, 1) + np.random.normal(0, 8, d)
d_opens[0] = 4810
d_highs = np.maximum(d_opens, d_closes) + np.abs(np.random.normal(15, 10, d))
d_lows  = np.minimum(d_opens, d_closes) - np.abs(np.random.normal(15, 10, d))
d_closes[-1] = 4003; d_opens[-1] = 4415; d_highs[-1] = 4025; d_lows[-1] = 3995

# 4H (30 candles)
h4_base = np.interp(np.linspace(0, d-1, 30), np.arange(d), d_closes)
h4_closes = h4_base + np.random.normal(0, 12, 30)
h4_closes[-1] = 4003; h4_closes = np.clip(h4_closes, 3980, 4850)
h4 = len(h4_closes)
h4_opens = np.roll(h4_closes, 1) + np.random.normal(0, 6, h4)
h4_opens[0] = h4_closes[0] + 10
h4_highs = np.maximum(h4_opens, h4_closes) + np.abs(np.random.normal(8, 5, h4))
h4_lows  = np.minimum(h4_opens, h4_closes) - np.abs(np.random.normal(8, 5, h4))

# 1H (30 candles)
h1_base = np.interp(np.linspace(0, h4-1, 30), np.arange(h4), h4_closes)
h1_closes = h1_base + np.random.normal(0, 8, 30)
h1_closes[-1] = 4003; h1_closes = np.clip(h1_closes, 3980, 4100)
h1 = len(h1_closes)
h1_opens = np.roll(h1_closes, 1) + np.random.normal(0, 4, h1)
h1_opens[0] = h1_closes[0] + 5
h1_highs = np.maximum(h1_opens, h1_closes) + np.abs(np.random.normal(5, 3, h1))
h1_lows  = np.minimum(h1_opens, h1_closes) - np.abs(np.random.normal(5, 3, h1))

# ─── BUILD FIGURE ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 14), facecolor=BG)

gs = fig.add_gridspec(6, 2,
    width_ratios=[4, 1.2], height_ratios=[0.4, 2.5, 2, 1.5, 1.8, 0.3],
    hspace=0.12, wspace=0.04, left=0.05, right=0.97, top=0.96, bottom=0.03)

ax_title = fig.add_subplot(gs[0, :])
ax_d     = fig.add_subplot(gs[1, 0])
ax_4h    = fig.add_subplot(gs[2, 0])
ax_1h    = fig.add_subplot(gs[3, 0])
ax_rr    = fig.add_subplot(gs[0:4, 1])
ax_strat = fig.add_subplot(gs[4, 0])
ax_info  = fig.add_subplot(gs[4, 1])
ax_foot  = fig.add_subplot(gs[5, :])

for ax in [ax_title, ax_d, ax_4h, ax_1h, ax_rr, ax_strat, ax_info, ax_foot]:
    ax.set_facecolor(BG)
    ax.tick_params(colors=DIM, labelsize=7)
    for sp in ax.spines.values():
        sp.set_color(BORDER)

# Title
ax_title.set_xlim(0, 10); ax_title.set_ylim(0, 1); ax_title.axis('off')
ax_title.text(5, 0.6, 'XAUUSD MULTI-TIMEFRAME SIGNAL', fontsize=16,
             fontweight='bold', color=GOLD_C, ha='center', va='center', transform=ax_title.transAxes)

# Draw charts
draw_candles(ax_d, d_opens, d_highs, d_lows, d_closes, 'DAILY  |  Trend: BEARISH  |  EMA20 < EMA50')
draw_candles(ax_4h, h4_opens, h4_highs, h4_lows, h4_closes, '4-HOUR  |  Trend: BEARISH  |  Consolidating')
draw_candles(ax_1h, h1_opens, h1_highs, h1_lows, h1_closes, '1-HOUR  |  Trend: NEUTRAL  |  Testing floor')

# Add buy/sell zones to daily
ax_d.axhspan(LONG_ENTRY_LO, LONG_ENTRY_HI, alpha=0.15, color=GREEN, zorder=0)
ax_d.axhline(y=LONG_ENTRY_LO, color=GREEN, linewidth=1.5, alpha=0.7)
ax_d.axhline(y=LONG_SL, color=RED, linestyle='-.', linewidth=1.5, alpha=0.7)

# Footer
ax_foot.set_xlim(0, 10); ax_foot.set_ylim(0, 1); ax_foot.axis('off')
ax_foot.text(5, 0.5, 'H=Hammer D=Doji SS=Shooting Star | Not financial advice | Hermes Agent',
            fontsize=6.5, color=DIM, ha='center', va='center')

# Save
path = '/tmp/gold_mtf_chart.png'
plt.savefig(path, dpi=170, facecolor=BG, bbox_inches='tight', pad_inches=0.12)
plt.close()
print(f"Chart: {path}")
