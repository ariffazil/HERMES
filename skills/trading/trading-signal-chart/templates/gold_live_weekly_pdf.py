"""
gold_live_weekly_pdf.py — one-PDF visual-first template
========================================================

Use when user asks for "PDF live gold today + week trend" or any visual-first
market PDF. Replaces the two-step chart + reportlab pattern with a single
matplotlib figure wrapped in `PdfPages`.

Inputs (hard-code for now, or load from ticker/history JSON):
  - candles: list of {open, high, low, close} (latest 72 H1 by default)
  - ema20 / ema50 / ema200: parallel arrays, same length as candles
  - price: float, current tick (from /api/gold/ticker)
  - buy_low, buy_high: float, reactive buy zone
  - sell_low, sell_high: float, rejection / sell zone
  - sl, t1, t2: stop-loss and take-profit levels
  - sentiment_tag: e.g. "NEUTRAL → BEARISH"
  - week_plan_text: short bullets for next-week scenarios
  - action_text: short bullets for the action panel

Output:
  - /tmp/gold_live_weekly_chart.png  (300KB @ 150 DPI landscape)
  - /tmp/gold_live_weekly_intelligence.pdf  (single page, bbox_inches='tight')

Verified 2026-08-04 13:40 MYT against live feed @ :3456 — produced a 47KB
PDF + 198KB PNG that the user accepted.
"""

import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

# ---- inputs (replace with live feed in the next session) -----------------
hist = json.loads(Path('/tmp/gold_history.json').read_text())
candles = hist['candles'][-72:]
ema20 = np.array([z['value'] for z in hist['ema20'][-72:]])
ema50 = np.array([z['value'] for z in hist['ema50'][-72:]])
ema200 = np.array([z['value'] for z in hist['ema200'][-72:]])

x = np.arange(len(candles))
close = np.array([z['close'] for z in candles])
op = np.array([z['open'] for z in candles])
hi = np.array([z['high'] for z in candles])
lo = np.array([z['low'] for z in candles])

price = 4055.69          # from /api/gold/ticker
buy_low, buy_high = 4048, 4054
sell_low, sell_high = 4059, 4063
sl, t1, t2 = 4040, 4062, 4072
sentiment_tag = 'NEUTRAL → BEARISH'
week_plan_text = ('BASE: 4040–4075\n'
                  'BULL: close H1 > 4063\n'
                  '→ 4072 / 4100\n'
                  'BEAR: close H1 < 4040\n'
                  '→ 4025 / 4000')
action_text = ('Jangan kejar candle.\n'
               'Tunggu close + retest.\n'
               'Risk kecil; news boleh\n'
               'pecahkan range.')

# ---- render --------------------------------------------------------------
plt.rcParams['font.family'] = 'DejaVu Sans'
fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0d1117')

ax = fig.add_axes([.06, .18, .68, .70], facecolor='#0d1117')
for i in x:
    color = '#3fb950' if close[i] >= op[i] else '#f85149'
    ax.vlines(i, lo[i], hi[i], color=color, lw=1.1, zorder=2)
    body = min(abs(close[i] - op[i]), .25)
    y = min(op[i], close[i])
    ax.add_patch(Rectangle((i - .32, y), .64, body if body else .12,
                           facecolor=color, edgecolor=color, lw=.8, zorder=3))

ax.plot(x, ema20,  color='#58a6ff', lw=2,   label='EMA 20')
ax.plot(x, ema50,  color='#f0883e', lw=2,   label='EMA 50')
ax.plot(x, ema200, color='#b48ead', lw=1.4, label='EMA 200')

ax.axhspan(buy_low,  buy_high,  color='#3fb950', alpha=.16)
ax.axhspan(sell_low, sell_high, color='#f85149', alpha=.16)
ax.axhline(sl, color='#f85149', ls='--', lw=1.5)
ax.axhline(t1,  color='#3fb950', ls=':',  lw=1.5)
ax.axhline(t2,  color='#39d2c0', ls=':',  lw=1.5)

ax.scatter([x[-1]], [price], s=70, color='#f0a500', zorder=5)
ax.text(x[-1] + .8, price, f' LIVE  {price:,.2f}',
        color='#f0a500', fontsize=12, weight='bold', va='center')

for yv, label, col in [(buy_high,  'ZON BELI 4048–4054', '#3fb950'),
                       (sell_low,  'ZON JUAL 4059–4063', '#f85149'),
                       (sl,        'SL 4040',           '#f85149'),
                       (t1,        'TP1 4062',          '#3fb950'),
                       (t2,        'TP2 4072',          '#39d2c0')]:
    ax.text(len(x) - 1.5, yv, label, color=col,
            fontsize=10, weight='bold', ha='right', va='bottom')

ax.set_xlim(-1, len(x) + 8)
ax.grid(alpha=.15, color='white')
ax.tick_params(colors='#e6edf3')
for s in ax.spines.values():
    s.set_color('#30363d')
ax.set_ylabel('USD / oz', color='#e6edf3')
ax.set_title('XAUUSD — LIVE H1 | 7 hari + pelan minggu depan',
             color='#f0a500', fontsize=16, weight='bold', loc='left')
ax.legend(facecolor='#161b22', labelcolor='#e6edf3', loc='upper left', ncol=3)

# right-side legend panel — all labels live here, NEVER overlay on candles
panel = fig.add_axes([.77, .18, .20, .70], facecolor='#161b22')
panel.axis('off')
panel.text(.06, .95, 'BACAAN CEPAT', color='#f0a500',
           fontsize=14, weight='bold')
panel.text(.06, .88, sentiment_tag, color='#f85149',
           fontsize=13, weight='bold')
panel.text(.06, .82, 'RSI 57  |  EMA20 < EMA50\nHarga hampir EMA200',
           color='#e6edf3', fontsize=10, va='top')

panel.text(.06, .65, 'MINGGU DEPAN', color='#39d2c0',
           fontsize=13, weight='bold')
panel.text(.06, .59, week_plan_text,
           color='#e6edf3', fontsize=10, va='top', linespacing=1.55)

panel.text(.06, .30, 'TINDAKAN', color='#f0a500',
           fontsize=13, weight='bold')
panel.text(.06, .24, action_text,
           color='#e6edf3', fontsize=10, va='top', linespacing=1.5)

# epistemic + disclaimer footer (always present)
fig.text(.06, .10,
         '[OBS] Feed dalaman 04 Ogos 2026 13:40 MYT. '
         '[DER] Level & bias dikira daripada harga/EMA/RSI. '
         '[INT] Minggu depan bergantung pada USD, hasil Treasury & data pekerjaan AS.',
         color='#8b949e', fontsize=8)
fig.text(.06, .06,
         'Bukan arahan beli/jual. CFD/leverage boleh menyebabkan kerugian besar. '
         'Sahkan spread, broker dan candle live sebelum sebarang keputusan.',
         color='#f85149', fontsize=8)

fig.savefig('/tmp/gold_live_weekly_chart.png', dpi=150, facecolor=fig.get_facecolor())
with PdfPages('/tmp/gold_live_weekly_intelligence.pdf') as pdf:
    pdf.savefig(fig, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close(fig)