---
name: nasi-lemak-sales-tracking
description: Track nasi lemak sales across locations/days — process receipt images, compile baki, compute revenue. Use when user shares handwritten cash bills, order receipts, baki counts, or asks for sales summaries and revenue analysis.
---

# Nasi Lemak Sales Tracking

Track daily nasi lemak sales across multiple locations. The user runs a nasi lemak supply business delivering to LRT-area stalls (Setiawangsa, Wangsa Maju, BSW, DP, MAMAK, KEDAI, DSW, DSP).

## Variant Types & Pricing

| Variant | Code on Receipt | Price/Unit |
|---|---|---|
| Telur Mata 🍳 | TELUR MATA / TECUR MATA / MOTO | RM 1.50 |
| Telur Rebus 🥚 | TELUR REBUS / TECUR REBUS | RM 1.20 |
| Telur Dadar | TELUR DADAR / DADAR | RM 1.20 |
| Berlauk 🥩 | BERLAUK / LOKU PARU DENDENG | (user will specify) |

## Receipt Decoding

Handwritten receipts use abbreviations. Common patterns:
- "NS LMK" / "NS LEMOK" = Nasi Lemak
- "TECUR" = Telur
- "REBUS" = Boiled, "MATA/MATI/MOTO" = Sunny side up, "DADAR" = Omelette
- "S/DSING" or "SIASING" = likely "sambal asing" (separate sambal)
- "DARAH" or "DENDENG" = jerky/meat variant
- Location headers: "M/S V005 <CODE>" where code = LRT station/shop code

**Rule:** When receipt text is ambiguous, present your best reading but ask the user to confirm. The user's verbal clarification always overrides receipt interpretation.

## Workflow

### 1. Receipt → Order Table
When the user sends a receipt image:
1. Read the location code (top-left of receipt)
2. Parse each row: quantity + item description
3. Present as a clean table with emoji markers
4. Ask for baki (remaining stock)

### 2. Baki → Sold Calculation
When user gives baki per variant:
- sold = order - baki
- Never assume baki; always ask if not provided
- Track "pending" separately for locations where baki is unknown

### 3. Multi-Day / Multi-Location Aggregation
- Group by date first, then by location
- Present "combined" table showing all locations side by side
- Flag pending/incomplete data clearly with ⏳

### 4. Revenue Calculation
- Apply correct price per variant
- Only include rows where baki (and thus sold) is known
- Exclude pending locations from revenue totals
- Present: sold count × unit price = revenue per variant

### 5. Save & Analyze
When user asks to save ("tolong simpan"):
1. Write structured CSV to `/root/forge_work/YYYY-MM-DD/nasi_lemak_sales.csv`
2. Run Python analysis producing:
   - Daily summary (order, sold, baki, sold %, revenue)
   - By-variant summary (aggregate across days)
   - By-location summary
   - Key insights (best performer, day comparison, revenue/unit)
3. Confirm save path at the end

## CSV Schema

```csv
date,day,location,jenis,order_qty,baki,sold,price_rm,revenue_rm
```

- `baki` and `sold` are empty for pending rows
- `revenue_rm` is empty when baki unknown
- `price_rm` is always filled (known pricing)

## Presentation Rules

- Use emoji markers consistently: 🍳 mata, 🥚 rebus, 🥩 berlauk
- Tables with pipe syntax (Telegram rich markdown)
- Fire emoji 🔥 for 100% sold, ⚠️ for low performers
- ⏳ for pending data
- Bold totals
- Short bullet insights at the end, not paragraphs

## Pitfalls

- Receipt handwriting is often ambiguous — never be certain about abbreviations without user confirmation
- The user may split one receipt's items across multiple messages; keep a running tally
- "Telur masin" on a receipt may map to "telur mata" in the user's category system — ask
- Some receipts list items the user later says "buang" (discard) — adjust accordingly
- Don't compute revenue for berlauk unless user confirms the price. **"Berlauk xyah"** = exclude entirely.
- **Location code aliases**: The same station may appear under different abbreviations on different days. DSW and BSW may be the same station; DSP and DP may be the same station. The user's verbal naming is authoritative — don't split into separate tracking buckets unless the user explicitly does.
- **Only sold revenue ("yang abis sahaja")**: When user says compute revenue for sold only, exclude all pending/unknown-baki rows. Revenue tables must only include variants with confirmed sold counts.
- **Multi-day span**: User often provides data across multiple consecutive days in one conversation. Cross-reference only when asked; keep daily summaries separate unless user requests a combined view.
- **Topic interrupts**: If user switches to personal/medical matters mid-tracking, handle the new topic immediately but preserve all tracked business data in-memory. Resume tracking only when user returns to it — don't re-ask already-provided data.
- **Price comes from user**: The user will say "telur mata darab 1.5, telur rebus n telur dadar darab 1.2". Apply these explicitly; never assume pricing.
- **Two-layer pricing**: User buys from supplier at RM 1.50 (mata) / RM 1.20 (rebus/dadar) and sells to customers at RM 3.00 / RM 2.50. Ask which price layer to use for calculations.
- **Sequential percentage deductions**: User may say "tolak setiap jenis 20%" then "tolak lagi 5%" — apply sequentially. Compute unsold count, then compute x-abis per-kedai average.
- **Per-kedai breakdown**: User tracks per-physical-kedai, not per-location. MAMAK 2 = 2 kedai, LRT S = 3 kedai. Divide totals accordingly when computing averages.

## References

- `references/locations.md` — location database, sambal types, 19-20 July 2026 historical summary
