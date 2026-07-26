#!/usr/bin/env python3
"""
XAUUSD Trading Signal Chart Template — Mode D
Dark theme, OANDA style, zoomed to current price.

USAGE: Modify the data section (closes, opens, highs, lows) and trade levels
(LONG_ENTRY, SHORT_ENTRY, etc.) for each day's signal.

PROVEN: 2026-07-14 — 8 iterations to get right. See references/trading-signal-chart-patterns.md
"""
import os
os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np

# ─── DARK THEME COLORS (OANDA) ───────────────────────────────────────────────
BG='#0d1117'; PANEL='#161b22'; GOLD='#f0a500'; TEAL='#39d2c0'
RED='#f85149'; GREEN='#3fb950'; TEXT='#e6edf3'; DIM='#8b949e'; BORDER='#30363d'

def ema(p, n):
    r=np.zeros(len(p)); m=2/(n+1); r[0]=p[0]
    for i in range(1,len(p)): r[i]=(p[i]-r[i-1])*m+r[i-1]
    return r

# ─── MODIFY THIS SECTION FOR EACH DAY ────────────────────────────────────────

# Last 15 daily candles — ZOOMED to current price action
# Replace with real data from OANDA/MT5
n = 15
closes = np.array([4120,4100,4085,4070,4060,4050,4040,4030,4020,4010,4005,4003,4015,4010,4003])
opens = np.array([4130,4125,4105,4090,4075,4065,4055,4045,4035,4025,4015,4020,4005,4020,4018]).astype(float)
highs = np.array([4135,4128,4110,4095,4080,4070,4060,4050,4040,4030,4025,4028,4025,4028,4030]).astype(float)
lows  = np.array([4110,4095,4078,4062,4050,4040,4030,4018,4008,3995,3988,3985,4000,4002,3988]).astype(float)

# Last candle = today (hammer at support)
closes[-1]=4003; opens[-1]=4018; highs[-1]=4030; lows[-1]=3985

# Current price
CURRENT = 4003

# Trade levels — CLOSE to current price (temporal intelligence)
LONG_ENTRY  = [3995, 4010]   # Buy zone
LONG_SL     = 3975           # Stop loss
LONG_T1     = 4045           # Target 1
LONG_T2     = 4080           # Target 2
SHORT_ENTRY = [4020, 4040]   # Sell zone (rejection play)
SHORT_SL    = 4060           # Stop loss
SHORT_T1    = 3980           # Target 1

# ─── END MODIFY SECTION ──────────────────────────────────────────────────────

e20 = ema(closes, 10)

# ─── FIGURE ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
ax.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.85, top=0.93, bottom=0.08)

# ─── CANDLESTICKS ────────────────────────────────────────────────────────────
cw = 0.55
for i in range(n):
    o,h,l,c = opens[i],highs[i],lows[i],closes[i]
    body = abs(c-o); rng = h-l if h-l>0 else 1
    is_bull = c >= o  # REAL meaning
    body_bot = min(o,c); body_h = max(body, 0.5)
    
    if body < rng * 0.1:  # Doji
        ax.plot([i-cw/2,i+cw/2],[o,o],color=DIM,linewidth=2,zorder=5)
        ax.plot([i,i],[l,h],color=DIM,linewidth=1,zorder=5)
    else:
        col = GREEN if is_bull else RED
        if is_bull:
            rect = Rectangle((i-cw/2,body_bot),cw,body_h,
                            facecolor='none',edgecolor=GREEN,linewidth=2)
        else:
            rect = Rectangle((i-cw/2,body_bot),cw,body_h,
                            facecolor=RED,edgecolor=RED,linewidth=1,alpha=0.85)
        ax.add_patch(rect)
        ax.plot([i,i],[l,body_bot],color=col,linewidth=1.2)
        ax.plot([i,i],[body_bot+body_h,h],color=col,linewidth=1.2)

# Mark last candle pattern
ax.annotate('HAMMER', xy=(n-1, lows[-1]-3), fontsize=11, fontweight='bold',
           color=GOLD, ha='center', va='top',
           bbox=dict(boxstyle='round,pad=0.3', facecolor=PANEL, edgecolor=GOLD, linewidth=2))

# ─── EMA ─────────────────────────────────────────────────────────────────────
ax.plot(range(n), e20, color='#58a6ff', linewidth=2.5, alpha=0.8, label='EMA 20')

# ─── BUY ZONE ────────────────────────────────────────────────────────────────
ax.axhspan(LONG_ENTRY[0], LONG_ENTRY[1], alpha=0.25, color=GREEN, zorder=0)
ax.axhline(y=LONG_ENTRY[0], color=GREEN, linewidth=3, alpha=0.9)
ax.axhline(y=LONG_ENTRY[1], color=GREEN, linewidth=3, alpha=0.9)

# ─── SELL ZONE ───────────────────────────────────────────────────────────────
ax.axhspan(SHORT_ENTRY[0], SHORT_ENTRY[1], alpha=0.25, color=RED, zorder=0)
ax.axhline(y=SHORT_ENTRY[0], color=RED, linewidth=3, alpha=0.9)
ax.axhline(y=SHORT_ENTRY[1], color=RED, linewidth=3, alpha=0.9)

# ─── LEVELS — on Y-axis ─────────────────────────────────────────────────────
ax.axhline(y=LONG_SL, color='#ff5252', linestyle='-.', linewidth=2.5, alpha=0.9)
ax.axhline(y=SHORT_SL, color='#ff5252', linestyle='-.', linewidth=2.5, alpha=0.9)
ax.axhline(y=LONG_T1, color=GREEN, linestyle=':', linewidth=2, alpha=0.6)
ax.axhline(y=LONG_T2, color=TEAL, linestyle=':', linewidth=2, alpha=0.6)
ax.axhline(y=SHORT_T1, color='#f0883e', linestyle=':', linewidth=2, alpha=0.6)

# Labels on RIGHT side
labels = [
    (LONG_T2, f'T2 ${LONG_T2}', TEAL),
    (LONG_T1, f'T1 ${LONG_T1}', GREEN),
    (SHORT_SL, f'SL ${SHORT_SL}', '#ff5252'),
    (SHORT_ENTRY[1], f'SELL ${SHORT_ENTRY[1]}', RED),
    (SHORT_ENTRY[0], f'SELL ${SHORT_ENTRY[0]}', RED),
    (CURRENT, f'NOW ${CURRENT}', GOLD),
    (LONG_ENTRY[1], f'BUY ${LONG_ENTRY[1]}', GREEN),
    (LONG_ENTRY[0], f'BUY ${LONG_ENTRY[0]}', GREEN),
    (LONG_SL, f'SL ${LONG_SL}', '#ff5252'),
    (SHORT_T1, f'T1 ${SHORT_T1}', '#f0883e'),
]
for price, text, color in labels:
    ax.text(n+0.3, price, f' {text} ', fontsize=10, fontweight='bold',
           color=color, va='center',
           bbox=dict(boxstyle='round,pad=0.2', facecolor=PANEL, edgecolor=color, linewidth=1, alpha=0.9))

# Current price marker
ax.scatter([n-1], [CURRENT], color=GOLD, s=200, zorder=10, edgecolors='white', linewidths=3)

# R:R — top left (small, out of way)
mid_long = (LONG_ENTRY[0]+LONG_ENTRY[1])/2
ax.text(0.3, max(highs)-10, f'LONG R:R 1:{(LONG_T1-mid_long)/(mid_long-LONG_SL):.1f}', 
       fontsize=12, fontweight='bold', color=GREEN,
       bbox=dict(boxstyle='round,pad=0.4', facecolor='#0d2818', edgecolor=GREEN, linewidth=2))

# ─── FORMATTING ──────────────────────────────────────────────────────────────
dates = ['1 Jul','','','4 Jul','','','7 Jul','','','10 Jul','','','13 Jul','','14 Jul']
ax.set_xticks(list(range(n)))
ax.set_xticklabels(dates[:n], fontsize=9, color=DIM)
ax.set_xlim(-0.8, n+7)
ax.set_ylim(CURRENT-40, CURRENT+80)  # TIGHT zoom around current price
ax.set_ylabel('USD/oz', fontsize=11, fontweight='bold', color=TEXT)
ax.tick_params(axis='y', labelsize=10, colors=TEXT)
ax.grid(True, alpha=0.06, color=BORDER)
for sp in ['top','right']:
    ax.spines[sp].set_visible(False)
ax.spines['left'].set_color(BORDER)
ax.spines['bottom'].set_color(BORDER)

ax.set_title('XAUUSD  |  DAILY  |  ZOOMED  |  14 July 2026',
            fontsize=15, fontweight='bold', color=GOLD, loc='left', pad=10)

plt.savefig('/tmp/gold_signal.png', dpi=150, facecolor=BG, bbox_inches='tight', pad_inches=0.1)
plt.close()
print(f"Chart saved: /tmp/gold_signal.png")
