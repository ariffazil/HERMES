# Session 2026-07-24 — Claim Format Consolidation

## Key lessons from this session

### Date display preference
User corrected `24 JULAI 2026 (JUMAAT)` to `24/07/2026`. Prefer DD/MM/YYYY short format for claim headers.

### Multi-date claim structure
User provided claims spanning 20/7, 22/7, and 24/7. Preferred format: single table with `Tarikh` column, one TOTAL row at bottom. When told "Tukar X sahaja", filter to that date only.

### File delivery priority
User explicitly rejected PDF as primary format: "Aku xnak dalam pdf. Aku nak dalam file". HTML is the default deliverable. Only convert to PDF on explicit request.

### The send-back signal
User sent the same PDF back multiple times when format didn't match exactly. The correct response: extract the file text, match its structure precisely, regenerate with updated data only. Never ask "what's wrong?" — read the file.

### Vendor claim input format
```
Vendor [NAME]
Claim payment V005
[DD/MM/YY] [day]
• bullet items (item description)
Hantar [N]
tolak Baki [N]
=jual [N]

Total Jual [N] x [price] = RM [amount]
```

With optional lelong rows: `Jual lelong [N] x [price] = RM [amount]`

### Date-day-of-week mapping verified
- 20/07/2026 = Isnin (Monday)
- 22/07/2026 = Rabu (Wednesday)  
- 24/07/2026 = Jumaat (Friday)
