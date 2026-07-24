# Cron-Based Chart Alert Delivery Pattern

When automating trading alerts with chart images via cron, the pattern is:

## Architecture

```
Cron (*/30 min) → Script generates chart + message → Agent delivers to Telegram
```

## Script Output Format (JSON)

```json
{
  "alert": true,
  "message": "**XAUUSD ALERT**\nPrice: $4,065\n...",
  "chart_path": "/tmp/sado_alert_chart.png",
  "price": 4065.00,
  "rsi": 62.2,
  "alerts": ["Near SUPPORT $4,063", "RSI OVERBOUGHT 72.1"]
}
```

## Cron Job Setup

```
no_agent: true → script IS the job, stdout delivered verbatim
no_agent: false → agent runs script, parses output, delivers intelligently
```

For chart delivery, use `no_agent: false` (agent mode) because:
- Agent can attach chart image to Telegram message
- Agent can format message nicely
- Agent stays silent when script outputs nothing

## Silent When Nothing

Script outputs empty string when no alert triggered. Agent must stay completely silent.
This is the "watchdog" pattern — quiet until something matters.

## Matplotlib Pitfall

All `$` signs in text passed to matplotlib functions must be replaced with `USD`:
- `ax.text()`, `fig.text()`, `ax.set_title()`, `ax.annotate()`
- Root cause: matplotlib interprets `$...$` as LaTeX math mode
- Fix: `plt.rcParams.update({'text.usetex': False, 'mathtext.default': 'regular'})`
- AND: `text.replace("$", "USD")` for all label strings

## Chart Specs (Mobile-First)

- Dark theme (#0d1117 bg)
- Last 48 hours of H1 data
- EMA 20 (cyan) + EMA 50 (orange) overlay
- S/R levels as dashed horizontal lines
- RSI panel below main chart
- Big labels (10pt+ body, 12pt+ key levels)
- DPI 150 (not 200 — file too big for Telegram)
- PNG format (not PDF — Telegram renders as image)

## Delivery Targets

| Target | Format |
|---|---|
| SADO group | Chart image + message caption |
| Arif DM | Chart image + signal detail |
| Weekly report | Aggregate stats (no chart) |
