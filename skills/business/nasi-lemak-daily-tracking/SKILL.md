---
name: nasi-lemak-daily-tracking
description: "Parse and track daily nasi lemak orders & vendor claims — structured tables, revenue calc, PDF receipts."
triggers:
  - "nasi lemak"
  - "order untuk"
  - "claim payment"
  - "vendor [DSW/DSP/LRT/KEAI]"
  - "telur mata / telur rebus / telur dadar / berlauk"
---

### Common Vendors / Locations

DSW, DSP, LRT Setiawangsa (LRT S), LRT Wangsa Maju (LRT WM), MAMAK 2, KEDAI P, KEDAI L, KEDAI A, EVEN, BSW, DP, BURAN

### Pricing (per unit) — proven session 2026-07-22/23

| Jenis | Harga Supplier | Harga Jual Normal | Harga Lelong |
|---|---|---|---|
| Telur Mata 🍳 | RM 1.50 | RM 3.00 - 3.50 | RM 2.50 |
| Telur Rebus 🥚 | RM 1.20 | RM 2.50 - 3.00 | RM 2.50 |
| Telur Dadar | RM 1.20 | RM 2.50 - 3.00 | RM 2.50 |
| Berlauk 🥩 | - | Cash term | - |

**Lelong items** — when a vendor has leftover stock at end of day, sold at flat RM 2.50 each regardless of type. Track separately from regular sales in the table, they go in their own row with "Lelong" in the item column and no Hantar/Baki.

### Common Vendors / Locations

DSW, DSP, LRT Setiawangsa, LRT Wangsa Maju, MAMAK 2, KEDAI P, KEDAI L, KEDAI A, LRT S, EVEN, BSW, DP, BURAN

### Order Parsing Pattern

User sends raw text like:
```
MAMAK 2
Nasi lemak telur rebus separuh sambal campur 40

LRT WM
1.Nasi lemak telur rebus separuh sambal campur 4
2.Nasi lemak telur mata sambal campur 8
```

→ Parse quantities per location per type. Present as structured table with totals.

### Vendor Claim Parsing Pattern

User sends claim data as:
```
Vendor DSW
Claim payment voo5
Hantar 16
tolak Baki 0
=jual 16
Total Jual-16.pax x2.50 = Rm 40
```

→ Parse: vendor, hantar, baki, sold, price, revenue. Include lelong items (sold at lower price).

### Workflow

1. Parse the raw order/claim data into tables
2. Show totals per type and per location
3. Handle mid-stream corrections — user frequently adjusts numbers
4. Calculate revenue when asked
5. Generate PDF using weasyprint HTML template (see `references/vendor-receipt-template.html`)

### Pitfalls

- **User corrects numbers multiple times.** Don't commit to final values until he confirms.
- **"Tolak" means subtract** — from the original order, not the current running total.
- **Lelong items** — sold at lower price (RM 2.50). Track separately from regular sales.
- **Berlauk is cash term** — exclude from standard revenue unless specified.
- **Dates** — user uses DD/MM/YY (Malaysian format). Today's orders are for the next day (order 22/7 for 23/7 delivery).
- **Never change an established PDF/table format.** When user says "buat macam ni" using a previous output as reference, replicate exact columns and styling. The user rejected format changes on 2026-07-24.
- **When user says "Aku xnak dalam pdf. Aku nak dalam file"** — give the HTML file path only, stop. Do NOT generate PDF.
- **Run total after every single correction** — user reads the running total from each display.
- **Order table vs Claim table are NOT interchangeable.** Order = Lokasi|Rebus|Mata|Dadar|Total. Claim = Vendor|Item|Hantar|Baki|Sold|Harga|Jualan.

### Revenue Calculation

- Supplier cost: Mata RM 1.50, Rebus/Dadar RM 1.20
- Customer price: Mata RM 3.00-3.50, Rebus/Dadar RM 2.50-3.00
- Lelong: RM 2.50 flat
- Untung = Revenue - Supplier Cost (on sold units)

### PDF Generation (Vendor Claim Receipts)

Use weasyprint via terminal. Prereq check: `pip install weasyprint --break-system-packages 2>/dev/null`.

```bash
mkdir -p /root/forge_work/<YYYY-MM-DD>
cat > /root/forge_work/<date>/vendor.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><style>
  body { font-family: Helvetica, Arial, sans-serif; margin: 40px; color: #1a1a1a; }
  h1 { color: #003366; font-size: 20pt; text-align: center; margin-bottom: 5px; }
  .date { text-align: center; color: #6B7280; font-size: 10pt; margin-bottom: 30px; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
  th { background: #003366; color: white; padding: 8px 10px; font-size: 10pt; text-align: left; }
  td { padding: 7px 10px; font-size: 9pt; border-bottom: 1px solid #e5e7eb; }
  tr:nth-child(even) { background: #f9fafb; }
  .total { font-weight: bold; background: #f0a500; color: white; }
  .total td { font-weight: bold; font-size: 10pt; }
  .footer { text-align: center; color: #6B7280; font-size: 8pt; margin-top: 30px; border-top: 1px solid #e5e7eb; padding-top: 15px; }
</style></head><body>
<h1>CLAIM VENDOR — V005</h1>
<p class="date">[DATE]</p>
<table>
<tr><th>Vendor</th><th>Item</th><th>Hantar</th><th>Baki</th><th>Sold</th><th>Harga (RM)</th><th>Jualan (RM)</th></tr>
<!-- DATA ROWS -->
<tr class="total"><td colspan="6">TOTAL</td><td>[TOTAL]</td></tr>
</table>
<p class="footer">Dijana oleh Hermes Agent — [DATE]</p>
</body></html>
HTMLEOF
cd /root/forge_work/<date> && weasyprint vendor.html vendor.pdf 2>&1
```

Styling: navy (#003366) headers, gold (#f0a500) total row, alternating white/#f9fafb rows, Helvetica, 9-10pt.

### Multi-Day Sales Comparison

When asked for trends across days, produce a compact table:

| Day | Total Order | Sold | Revenue | Sold Rate |
|---|---|---|---|---|
| 19/7 | 198 | 145 | RM 190.80 | 73% |
| 20/7 | 84 | 35 | RM 39.30 | 42% |

Highlight best-performing location and variant with 🔥 indicator.

### Patient Correction Flow

The user iterates through corrections — do NOT push for premature finality:

1. Always accept the new number and update immediately — never say "I already showed that"
2. Only ask for additional data when genuinely missing (e.g. "baki berapa?")
3. Only offer PDF after the user explicitly says "pdf" or sends back a receipt image
4. When the user says "buang" / "tolak" / "xyah" — apply the subtraction silently, do not re-confirm
5. When the user sends a photo of a cash bill via image, parse the quantities and offer a table — let him correct the reading
