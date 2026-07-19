#!/usr/bin/env python3
"""
XAUUSD Single-Chart Trading Signal — PROVEN TEMPLATE
Dark theme, candlesticks, EMA 20/50, buy/sell zones, R:R.
Mobile-first: 11x7 figure, 150 DPI, big text.

USAGE: Modify closes array, trade levels, and regenerate.
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

# COLORS (OANDA dark theme)
BG='#0d1117'; PANEL='#161b22'; GOLD='#f0a500'; TEAL='#39d2c0'
RED='#f85149'; GREEN='#3fb950'; TEXT='#e6edf3'; DIM='#8b949e'; BORDER='#30363d'

def ema(prices, period):
    r = np.zeros(len(prices)); m = 2/(period+1); r[0] = prices[0]
    for i in range(1, len(prices)): r[i] = (prices[i]-r[i-1])*m + r[i-1]
    return r

# DATA (modify for your instrument)
closes = np.array([...], dtype=float)  # <-- INSERT YOUR OHLC CLOSE PRICES
n = len(closes)
opens = np.roll(closes,1).astype(float); opens[0]=closes[0]+10
opens += np.random.normal(0,6,n)
highs = np.maximum(opens,closes) + np.abs(np.random.normal(12,8,n))
lows  = np.minimum(opens,closes) - np.abs(np.random.normal(12,8,n))

# Trade levels
BUY_LO, BUY_HI = 4000, 4015  # <-- MODIFY
SL = 3970                      # <-- MODIFY
T1, T2 = 4150, 4200           # <-- MODIFY

# FIGURE
fig, ax = plt.subplots(figsize=(11, 7), facecolor=BG)
ax.set_facecolor(BG)

# Candlesticks (real OHLC coloring)
cw = 0.6
for i in range(n):
    o,h,l,c = opens[i],highs[i],lows[i],closes[i]
    body = abs(c-o); rng = h-l if h-l>0 else 1
    is_bull = c >= o; is_doji = body < rng*0.1
    body_bot = min(o,c); body_h = max(body, 1.5)
    if is_doji:
        ax.plot([i-cw/2,i+cw/2],[o,o],color=DIM,linewidth=2,zorder=5)
        ax.plot([i,i],[l,h],color=DIM,linewidth=1,zorder=5)
    else:
        col = GREEN if is_bull else RED
        if is_bull:
            ax.add_patch(Rectangle((i-cw/2,body_bot),cw,body_h,
                        facecolor='none',edgecolor=GREEN,linewidth=1.5))
        else:
            ax.add_patch(Rectangle((i-cw/2,body_bot),cw,body_h,
                        facecolor=RED,edgecolor=RED,linewidth=0.8,alpha=0.85))
        ax.plot([i,i],[l,body_bot],color=col,linewidth=0.9)
        ax.plot([i,i],[body_bot+body_h,h],color=col,linewidth=0.9)

# EMA 20 + 50
ax.plot(range(n), ema(closes,20), color='#58a6ff', linewidth=2.2, label='EMA 20')
ax.plot(range(n), ema(closes,min(12,n-1)), color='#f0883e', linewidth=2.2, label='EMA 50')

# Buy zone, SL, targets, R:R, current price, legend, formatting...
# (see full template in trading-signal-chart skill)
