# MT5 Mobile Interface Reference

Extracted from live MT5 iOS screenshot analysis (2026-07-11).

## Color palette

| Element | Hex | Usage |
|---------|-----|-------|
| Buy text | #2962FF | buy labels, lot sizes, positive profit |
| Sell text | #E53935 | sell labels, negative values, withdrawals |
| Primary text | #212121 | instrument names, active tab text, balance labels |
| Secondary text | #757575 | prices, timestamps, summary labels, inactive tabs |
| Borders | #F5F5F5 | row separators, tab container bg |
| Background | #FFFFFF | page background |
| Inactive nav | #9E9E9E | bottom nav inactive icons/text |
| Active nav | #2962FF | bottom nav active icon/text |
| Active nav bg | #E3F2FD | bottom nav active pill background |

## Typography

| Element | Size | Weight |
|---------|------|--------|
| Instrument name | 13px | 600 (semibold) |
| Trade type (buy/sell) | 13px | 600 |
| Lot size | 13px | 400 |
| Price levels | 13px | 400 |
| Timestamp | 11px | 400 |
| Profit amount | 14px | 600 |
| Summary labels | 14px | 400 |
| Summary values | 14px | 600 |
| Balance label/value | 14px | 600 |
| Active tab | 16px | 600 |
| Inactive tab | 16px | 400 |

## Layout

- Page width: 390px (iPhone standard)
- Row padding: 12px vertical, 16px horizontal
- Summary padding: 8px vertical, 16px horizontal
- Summary rows separated by 1px #F5F5F5 borders
- Tabs: centered, 8px gap, 8px border-radius pill bg
- Bottom nav: fixed, 2px top border #E0E0E0, 28px bottom padding (safe area)
- Active nav icon: 48px wide, 40px tall, 24px border-radius pill

## Structure

```
Status bar (time, network, battery)
├── Tabs row (Positions | Orders | Deals)
├── Trade list
│   ├── Trade item (symbol + type + lots | date + profit)
│   │   └── Prices row (entry → exit)
│   └── ...repeat
├── Account summary
│   ├── Deposit: 0.00
│   ├── Withdrawal: [amount] (red if negative)
│   ├── Profit: [amount] (blue)
│   ├── Swap: 0.00
│   ├── Commission: 0.00
│   └── Balance: [amount] (blue, bold)
└── Bottom nav (Quotes | Chart | Trade | History | Settings)
```
