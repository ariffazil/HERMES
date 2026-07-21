---
name: receipt-to-analytics
description: Convert informal business records (handwritten receipt images, oral stock/sales updates) into structured CSV + revenue analysis. Use when the user shares receipt photos and expects compiled sales data with insights.
---

# Receipt-to-Analytics

## Trigger
User shares one or more images of handwritten receipts/cash bills, often accompanied by oral updates ("baki telur mata 4", "telur rebus abis", etc.). The receipts are typically Malaysian-style cash bills with handwritten item descriptions, quantities, and blank prices.

## Workflow

### Phase 1: Extract from Images
1. Use `vision_analyze` on each receipt image to read handwritten fields
2. Extract: location (from header/address), date, item descriptions, quantities
3. Present extracted data back to user in a clean table — they almost always need to correct something

### Phase 2: Collect Oral Updates
1. Ask user for `baki` (remaining stock) per location/variant
2. Derive `sold = order - baki`
3. Iterate — user typically provides data in fragments across multiple messages. Ask per location, not all at once if there are many.

### Phase 3: Compile & Price
1. Aggregate across: days → locations → variants
2. Apply pricing (user will provide on demand: "telur mata darab 1.5")
3. Calculate revenue: `sold × price`
4. Present running totals as the data builds up

### Phase 4: Save & Analyze
1. Save all records to `/root/forge_work/YYYY-MM-DD/nasi_lemak_sales.csv` (or appropriate name)
2. Run Python analysis via `execute_code` (not terminal — keep analysis in-session)
3. Output: daily summary, by-variant breakdown, by-location breakdown, key insights (best performer, weekday vs weekend comparison, revenue totals)

### CSV Schema
```
date,day,location,jenis,order_qty,baki,sold,price_rm,revenue_rm
```
- `jenis`: variant type (mata, rebus, dadar, berlauk, etc.)
- `baki` and `sold`: leave blank for pending locations; compute `sold = order_qty - baki` once known
- `revenue_rm`: `sold × price_rm` once both known

### Analysis Output Structure
1. **Daily Summary** — table per day with per-variant breakdown (Order | Sold | Baki | Sold % | Revenue)
2. **By Variant** — cross-day aggregation showing which variants perform best
3. **By Location** — per-location performance with sold rates
4. **Key Insights** — best performer, day-over-day comparison, avg revenue per unit, pending items

## Pitfalls
- `vision_analyze` often misreads handwritten abbreviations (e.g., "NS LMK" for "Nasi Lemak", "TECUR" for "Telur", "SIASING" for "sambal asing"). Always confirm with user — never assume the vision reading is correct.
- User may remap items across sessions (e.g., "telur masin" → "telur mata" in a later message). Track these remaps explicitly.
- Some receipts have blank prices — don't fill prices until user states them.
- Pending bali locations should be clearly marked as ⏳, not silently merged with completed data.
- When user says "buang" (discard) for an item, remove it from that location's record entirely.
