# ForexFactory JSON API

**Discovered:** 2026-07-16

ForexFactory has a direct JSON feed — much cleaner than HTML scraping.

## Endpoint

```
https://nfs.faireconomy.media/ff_calendar_thisweek.json
```

## Response Format

```json
[
  {
    "title": "Core CPI m/m",
    "country": "USD",
    "date": "2026-07-14T09:30:00-04:00",
    "impact": "High",
    "forecast": "0.2%",
    "previous": "0.2%",
    "actual": "0.0%"
  }
]
```

## Key Fields

- `country`: Currency code (USD, EUR, GBP, etc.)
- `impact`: "High", "Medium", "Low"
- `date`: ISO 8601 with timezone (usually -04:00 or -05:00 EST)
- `actual`: Empty string if not yet released

## Usage

Filter for `country === "USD"` and `impact === "High"` to get gold-moving events.

## Timezone Note

ForexFactory dates are in EST (UTC-4 or UTC-5). Convert to MYT (UTC+8) by adding 12-13 hours.

## Cache

Gold-api caches this at `/api/gold/calendar` with 5-min TTL. Use the cached endpoint instead of hitting FF directly.

## Red Events Reference

See `/root/trading/references/red-news-impact.md` for the CPI/NFP/FOMC impact analysis and the 15-minute rule.
