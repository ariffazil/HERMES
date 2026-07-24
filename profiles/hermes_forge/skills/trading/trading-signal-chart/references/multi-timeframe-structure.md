# Multi-Timeframe Trading Chart Structure

## When to Use

When the user (or their trading mentor) requests multi-timeframe analysis.
Syed's standard: "Multi time frame. Candlestick pattern structure. Confirmation."

## Layout Options

### Option A: Stacked in One Figure (REJECTED — too dense)

3 subplots via gridspec. **FAILED:** text too small, candlesticks unreadable on mobile.
User said "Fail. Aku x nampak apa."

### Option B: Separate PNGs Stacked in PDF (RECOMMENDED)

Generate 3 separate chart PNGs, stack in reportlab PDF with labels between them.

```python
# Generate 3 charts
for tf_name, tf_opens, tf_highs, tf_lows, tf_closes in [
    ('DAILY', d_opens, d_highs, d_lows, d_closes),
    ('4-HOUR', h4_opens, h4_highs, h4_lows, h4_closes),
    ('1-HOUR', h1_opens, h1_highs, h1_lows, h1_closes),
]:
    fig, ax = plt.subplots(figsize=(11, 4), facecolor=BG)
    # ... draw candlesticks, EMAs, zones ...
    plt.savefig(f'/tmp/chart_{tf_name}.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()

# In PDF:
story.append(Image('/tmp/chart_DAILY.png', width=19*cm, height=7*cm))
story.append(Paragraph('4-HOUR | Intermediate | Consolidating', section_style))
story.append(Image('/tmp/chart_4-HOUR.png', width=19*cm, height=6*cm))
# etc.
```

### Option C: One Chart + Strategy Table (BEST for mobile)

Single daily chart (big, clean) + strategy table below + confirmation text.
Proven 2026-07-14. User approved.

## Timeframe Roles

| TF | Role | What to show |
|---|---|---|
| Daily | Trend direction | EMA 20/50, major S/R, buy/sell zones |
| 4H | Intermediate | EMA 20/50, pattern confirmation |
| 1H | Entry timing | EMA 20/50, precise entry, confirmation signal |

## Confirmation Signals

Always include:
- "Wait for candle close above EMA 20 on 1H before entry"
- RSI oversold/overbought context
- Volume confirmation if available

## Pitfalls

- Don't stack 3 dense charts in one figure — user can't read on phone
- Each TF needs its own adequate vertical space
- 1H chart will have smaller candles — use wider candle width (0.7 vs 0.6)
- Same trade levels (zones, SL, targets) should appear on ALL timeframes
