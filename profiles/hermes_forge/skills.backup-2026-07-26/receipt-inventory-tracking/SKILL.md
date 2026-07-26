---
name: receipt-inventory-tracking
description: >-
  Track orders, sales, and remaining stock from handwritten receipt images
  shared by Arif for his food-stall business. Extract data into clean
  markdown tables, reconcile across multiple LRT station locations, handle
  item-name corrections from user's internal naming system.
triggers:
  - Handwritten receipt or cash bill or order form image shared
  - Food-stall context with item names like nasi lemak, telur, berlauk, LRT stations
  - User reconciling what was ordered vs what sold vs what remains (baki)
---

# Receipt Inventory Tracking

Arif operates food stalls at LRT stations selling nasi lemak with various egg variants. He shares handwritten cash bill / order form images with quantities of each item prepared. The task is to extract that data, reconcile against what remains (baki), and track across multiple locations.

## Workflow

### 1. Extract from Image
Read all handwritten entries from the receipt image. Focus on:
- Location name (e.g., "SETIAWANGSA", "MAJU" → "Wangsa Maju")
- Date
- Item quantities (under BANYAK column)
- Item descriptions (under JENIS BARANG-BARANG)
- Prices are often blank — that's normal

### 2. Present as Clean Markdown Table
Present extracted data in a concise markdown table. **No long explanations or commentary.** The user is running a business, not looking for conversation.

### 3. Wait for User Corrections on Item Names
**CRITICAL**: The abbreviations written on receipts often differ from Arif's internal category names. Do NOT assume the written abbreviation is the final item name. Examples from 2026-07-20:
- "NS LMK TECUR DENDENG SIASING" → actually "telur dadar"
- "NS LEMOK LOKU PARU DAN DENDENG" → actually "berlauk"  
- "Telur masin" → actually "telur mata"
- "NS LMK TECUR MATI" → actually "telur mata"

Let the user provide the real category names, then remap.

### 4. Track Per Location Separately
Each LRT station is a separate reconciliation unit:
- Extract → present → get corrections → calculate Sold = Order - Baki
- Only combine into master summary AFTER all locations are reconciled

### 5. Combine into Master Summary
Final table across all locations with columns: Jenis, Order, Baki (remaining), Sold. Include totals row. Sold rate % is useful context.

## Column Conventions

| Column | Meaning |
|---|---|
| Order | Quantity prepared/sent to that location |
| Baki | Remaining unsold (user provides this) |
| Sold | Calculated: Order - Baki |

## Pitfalls

- **Never guess item names from abbreviations.** The user's naming system (telur mata, telur rebus, telur dadar, berlauk) differs from what's handwritten on receipts. Ask or wait for correction.
- **Match the user's terminology**, not formal descriptions. "Berlauk" not "nasi lemak with side dishes."
- **Some items on the receipt may be discarded ("buang")** — remove them from tracking when user says so.
- **Items may map across categories** — e.g., "telur masin" on receipt may map to "telur mata" in tracking. Just follow the user's mapping.
- **Be concise.** The user wants clean tables, not paragraphs. One question at a time when clarification is needed.

## Response Style
- Lead with the table, not commentary
- BM casual mixed with English for technical terms
- Short clarifying questions when mapping is ambiguous
- Emoji on item names OK (🍳🥚🧂) but not required

## References
- `references/session-2026-07-20.md` — Full worked example: Setiawangsa + Wangsa Maju, 52 items across 4 categories, name mappings learned
