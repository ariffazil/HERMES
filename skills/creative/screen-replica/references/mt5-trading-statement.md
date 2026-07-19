# MT5 Trading Statement Replica

Reference implementation for replicating MetaTrader 5 mobile app screens.

## UI Anatomy (MT5 Android/iOS)

```
┌─────────────────────────────────┐
│ Status Bar (time, signal, batt) │
├──────┬──────┬──────┬────────────┤
│ Pos  │Orders│ Deals│    🕐      │  ← Tab bar with clock icon
├─────────────────────────────────┤
│ XAUUSD.m  sell  0.5            │
│ 4208.32 → 4189.75              │  ← Each trade: symbol, action, lots
│              2026.06.22 17:33   │     prices, date, profit (blue)
├─────────────────────────────────┤
│ ... more trades ...             │
├─────────────────────────────────┤
│ Deposit:        0.00            │
│ Profit:    118 195.75  ← blue   │  ← Account summary
│ Swap:          0.00             │
│ Commission:    0.00             │
│ Balance:   118 195.75  ← blue   │
├─────────────────────────────────┤
│ 📊 Quotes │ 📈 Chart │ 💹 Trade│  ← Bottom nav (History active)
│           │          │ 🕐 Hist │
└─────────────────────────────────┘
```

## Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Buy text | Blue | `#007AFF` |
| Sell text | Red | `#FF3B30` |
| Profit amount | Blue bold | `#007AFF` |
| Date/time | Gray | `#999` |
| Background | White | `#fff` |
| Active tab bg | Light gray | `#f0f0f0` |
| Active nav | Blue | `#007AFF` |
| Borders | Light gray | `#eee` |

## Typography

- System font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Trade symbol: 14px, weight 600
- Trade type (buy/sell): weight 700, colored
- Profit: 14px, weight 700, blue
- Dates: 11px, gray
- Summary labels: 13px, gray
- Summary values: 13px, weight 600

## Layout Width

- iPhone frame: 390px (iPhone 14/15)
- Android frame: 360px (Samsung standard)

## Key Patterns

### Trade entry structure
```
[Symbol] [Action] [Lots]        [Date]
[Open Price] → [Close Price]    [Profit]
```

### Profit always right-aligned, blue, bold
### Date always right-aligned, gray, small
### Each trade separated by light border-bottom

## Customization Points

When user wants different data:
- Swap trade symbols/instruments
- Change lot sizes, prices, dates
- Adjust profit figures
- Add/remove trades from the list
- Change withdrawal amount and method
- Update account name/number in header

## Delivery

1. Write HTML to `/tmp/mt5_replica.html`
2. `browser_navigate` to `file:///tmp/mt5_replica.html`
3. `browser_vision` to capture screenshot
4. Send via `MEDIA:` tag
5. Offer edits
