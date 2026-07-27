---
name: nasi-lemak-sales-tracking
description: Track nasi lemak sales across locations/days — process receipt images, compile baki, compute revenue
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

## Voice/Tone

- **Full BM only.** User corrects MULTIPLE TIMES if English slips in — this caused strong frustration this session. Tuils semua tanggapan dalam Bahasa Melayu. Istilah dagang (XAUUSD, TP, SL) dan nama khas sahaja yang boleh guna English.
- **Jawab terus.** Soalan ya/tidak: jawab ya/tidak dulu.
- **Jangan bagi penerangan panjang untuk kerja biasa.** Bila user kata "buat" — terus buat.
- **Bila kena tegur: satu ayat je, lepas tu terus jalan.**
- **Guna pembetulan tu untuk baki sesi.** Jangan ulang kesilapan yang sama.

## Presentation Rules

- Use emoji markers consistently: 🍳 mata, 🥚 rebus, 🥩 berlauk
- Tables with pipe syntax (Telegram rich markdown)
- Fire emoji 🔥 for 100% sold, ⚠️ for low performers
- ⏳ for pending data
- Bold totals
- Short bullet insights at the end, not paragraphs

### 6. Vendor Claim / Order Summary Report (V005 Format)

When the user asks for a **"claim vendor"** or **"buat macam ni"** (pointing to a previous report):

**Two distinct report formats:**

| Format | Title | Columns | Use |
|--------|-------|---------|-----|
| ORDER SUMMARY | `ORDER SUMMARY — V005` | Lokasi, Rebus🥚, Mata🍳, Dadar, Total | Daily aggregate by location |
| CLAIM VENDOR | `CLAIM VENDOR — V005` | Vendor, Item, Hantar, Baki, Sold, Harga, Jualan | Per-vendor payout calculation |

**Visual style (both formats):**
- Navy header row (`#003366`), white text
- Zebra-striped rows (white / `#f9fafb`)
- Gold total row (`#f0a500`), bold white text
- A4 print-ready, clean sans-serif

**File output preference:** The user explicitly prefers **HTML files** (`*.html`) — not PDF. Generate HTML first. Only generate PDF (via weasyprint) when the user explicitly asks for "PDF". Command: `cd /root/forge_work/YYYY-MM-DD/ && weasyprint file.html file.pdf`

**Date format:** Always use `DD JULAI 2026 (HARI)` — e.g. `24 JULAI 2026 (JUMAAT)`. Verify today's actual day-of-week.

**Reference code:** All claim/receipt forms use `V005` as the document code. Keep in header title: `CLAIM VENDOR — V005`.

### 7. Dual-Layer Pricing

The user operates two price layers — **always ask which layer** if not explicitly stated:

| Variant | Supplier (buy) | Customer (sell) |
|---------|---------------|-----------------|
| Telur Mata 🍳 | RM 1.50 | RM 3.00 |
| Telur Rebus 🥚 | RM 1.20 | RM 2.50 |
| Telur Dadar | RM 1.20 | RM 2.50 |
| Berlauk 🥩 | (user specifies) | (user specifies, often cash-term) |

- **Supplier pricing** (cost of goods): `darab 1.5 n 1.2`
- **Customer pricing** (revenue): User specifies per-batch e.g. `"telur mata rm 3 n telur rebus rm 2.5"`
- Revenue = sold × customer price. Cost = sold × supplier price. Profit = revenue − cost.

## HTML Template (Vendor Claim)

When generating an HTML file for the user, use this structure — it matches the V005 claim format exactly. Save to `/root/forge_work/YYYY-MM-DD/claim_vendor_v005.html`:

### Minimal HTML scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">
<style>
  body { font-family: Helvetica, Arial, sans-serif; margin: 40px; }
  h1 { color: #003366; font-size: 20pt; text-align: center; }
  .date { text-align: center; color: #6B7280; font-size: 10pt; margin-bottom: 30px; }
  table { width: 100%; border-collapse: collapse; }
  th { background: #003366; color: white; padding: 8px 10px; font-size: 10pt; text-align: left; }
  td { padding: 7px 10px; font-size: 9pt; border-bottom: 1px solid #e5e7eb; }
  tr:nth-child(even) { background: #f9fafb; }
  .total { background: #f0a500; color: white; font-weight: bold; }
  .footer { text-align: center; color: #6B7280; font-size: 8pt; border-top: 1px solid #e5e7eb; padding-top: 15px; margin-top: 30px; }
</style></head>
<body>
<h1>CLAIM VENDOR — V005</h1>
<p class="date">DD JULAI 2026 (HARI)</p>
<table>
<tr><th>Vendor</th><th>Item</th><th>Hantar</th><th>Baki</th><th>Sold</th><th>Harga (RM)</th><th>Jualan (RM)</th></tr>
<!-- Rows -->
<tr class="total"><td colspan="6">TOTAL</td><td>XXX.XX</td></tr>
</table>
<p class="footer">Dijana oleh Hermes Agent — DD Julai 2026</p>
</body></html>
```

### Order Summary HTML (location breakdown)

```html
<h1>ORDER SUMMARY — V005</h1>
<p class="date">DD JULAI 2026 (HARI)</p>
<table>
<tr><th>Lokasi</th><th>Rebus 🥚</th><th>Mata 🍳</th><th>Dadar</th><th>Total</th></tr>
<!-- Rows -->
</table>
```

### 8. Self-Reminder: Stop Explaining When User Asks for Output

When the user says things like:
- "Buat macam ni" / "Buat file" / "Buat forward camni"
- "Aku xnak dalam pdf. Aku nak dalam file"
- Repeatedly sending back the same PDF or file you just delivered

→ **Stop explaining what the file contains. Stop asking questions. Stop giving advice or warnings about missing data. Just generate the file and deliver it immediately. If the format is already clear from prior context, replicate it exactly without commentary.** The user corrects only when the output is wrong, not because they need explanation. Explanations after the user has given clear instructions delay the only outcome they want: the file.

**Critical: the "send-back" signal.** When the user sends back the same file you just delivered (without any new data), it means the FORMAT is wrong, not the content. Do NOT ask "what's wrong?" or "what should I change?" — instead:
1. Read/extract the file the user sent back to understand the structure.
2. Replicate its EXACT columns, header wording, title, and styling.
3. Update only the data and date.
4. Resend.

**HTML-first, PDF-only-on-demand.** Default deliverable is HTML at `/root/forge_work/YYYY-MM-DD/claim_vendor_v005.html`. Only produce PDF via weasyprint when the user explicitly says "PDF".

### 9. Date Format Preference

The user prefers `DD/MM/YYYY` format (e.g. `24/07/2026`) over verbose Malay dates (e.g. `24 JULAI 2026 (JUMAAT)`). Default to the short format. Only use the verbose format if the user explicitly accepted it in a prior context for the same document.

### 10. Multi-Date Claim Table

When user provides vendor data spanning multiple dates, add a `Tarikh` column to disambiguate. Group by vendor, not by date. When user says "Tukar X sahaja", filter to only that date.

### 11. Structured Claim Input Pattern

The user provides claim data in this format. Parse directly:
```
Vendor [NAME]
Claim payment V005
[date] [day]
Hantar [N]
tolak Baki [N]
=jual [N]
Total Jual [N] x [price] = RM [amount]
```
May include "Jual lelong [N] x [price]" as a separate row. Different vendors may have different dates.

**HTML-first, PDF-only-on-demand.** Default deliverable is HTML at `/root/forge_work/YYYY-MM-DD/claim_vendor_v005.html`. Only produce PDF via weasyprint when the user explicitly says "PDF".

## References

- `references/v005-claim-template.html` — example claim vendor HTML file
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
