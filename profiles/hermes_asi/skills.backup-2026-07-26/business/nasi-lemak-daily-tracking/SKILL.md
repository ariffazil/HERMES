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

## Nasi Lemak Daily Order Tracking

The user runs a nasi lemak distribution business. He shares daily orders and vendor claim data in BM shorthand. Parse into structured tables, calculate revenue, generate PDFs.

### Pricing (per unit)

| Jenis | Harga |
|---|---|
| Telur Mata 🍳 | RM 1.50 (supplier) / RM 3.00-3.50 (jual) |
| Telur Rebus 🥚 | RM 1.20 (supplier) / RM 2.50-3.00 (jual) |
| Telur Dadar | RM 1.20 (supplier) / RM 2.50-3.00 (jual) |
| Berlauk 🥩 | Cash term (varies) |

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

### Revenue Calculation

- Supplier cost: Mata RM 1.50, Rebus/Dadar RM 1.20
- Customer price: Mata RM 3.00-3.50, Rebus/Dadar RM 2.50-3.00
- Lelong: RM 2.50 flat
- Untung = Revenue - Supplier Cost (on sold units)

### PDF Generation

Use weasyprint via terminal:
```bash
cd /root/forge_work/<date> && weasyprint vendor.html vendor.pdf
```

HTML template: navy headers (#003366), gold total row (#f0a500), Helvetica font. See `references/vendor-receipt-template.html` for full template.

### Patient Corrections

The user iterates through corrections — stay patient and update the table after each correction. Don't push for confirmation prematurely. Let him finish adjusting, then offer PDF.
