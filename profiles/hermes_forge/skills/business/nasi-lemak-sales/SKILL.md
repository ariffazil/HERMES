---
name: nasi-lemak-sales
description: "Track nasi lemak daily orders, vendor claims, sales, and generate summary PDFs. For Khairuddin's nasi lemak business across multiple LRT/kedai locations."
tags: [nasi-lemak, sales, vendor-claim, pdf, business-tracking]
triggers:
  - "nasi lemak order"
  - "vendor claim"
  - "claim payment"
  - "nasi lemak baki"
  - "nasi lemak revenue"
  - "order untuk"
---

# Nasi Lemak Sales Tracking

Track daily nasi lemak orders, vendor claims, sales, baki, and revenue across multiple locations.

## Quick Reference

### Pricing (Supplier Cost)
| Jenis | Harga/unit |
|---|---|
| Telur Mata 🍳 | RM 1.50 |
| Telur Rebus 🥚 | RM 1.20 |
| Telur Dadar | RM 1.20 |

### Pricing (Customer/Selling Price — Vendor Claims)
| Jenis | Harga/unit |
|---|---|
| Biasa (DSW/DSP) | RM 2.50 |
| Telur Mata + Berlauk | RM 3.50 |
| Telur Dadar + Rebus | RM 3.00 |
| Lelong | RM 2.50 |

### Locations
MAMAK 2, KEDAI P, KEDAI L, KEDAI A, MAMAK 1, EVEN, LRT WM (Wangsa Maju), LRT S (Setiawangsa), DSW, DSP (Desa Pacific), BSW

## Order Entry Format

When the user sends orders, they use this format:
```
Order untuk [TARIKH] ([HARI])
[LOKASI]
[JENIS] [KUANTITI]
```

Example:
```
Order untuk 22/07/26 (Rabu)
MAMAK 2
Nasi lemak telur rebus separuh sambal campur 40
KEDAI P
Nasi lemak telur mata sambal asing 38
```

### Rules
- Berlauk items are "cash term" — **don't include in revenue unless user specifies price**
- When user says "buang" or "tolak" — remove those items completely
- When user says "berlauk xyah" — exclude berlauk from totals
- Never calculate berlauk revenue unless user gives explicit price

## Vendor Claim Format

Vendor claims use this format:
```
Vendor [NAME]
Claim payment [CODE]
[DD/MM/YY] [DAY]
• item descriptions
Hantar [QTY]
Tolak Baki [QTY]
=Jual [QTY]
Total Jual [QTY] x [PRICE] = RM [AMOUNT]
```

### Claim Table Columns
| Vendor | Hantar | Baki | Sold | Harga | Jualan |
|---|---|---|---|---|---|

### Key Rules
- Lelong sales: separate line with RM 2.50 price
- Baki = unsold, reduce from Hantar
- Sold = Hantar - Baki (unless lelong counted separately)

## PDF Generation

For vendor claim summaries, use weasyprint HTML→PDF:
```bash
cd /root/forge_work/YYYY-MM-DD
weasyprint vendor_claim.html vendor_claim.pdf
```

Template: navy header (#003366), gold total row (#f0a500), white background, Helvetica font. See `templates/vendor_claim.html`.

## Data Storage

Save CSVs to `/root/forge_work/YYYY-MM-DD/nasi_lemak_sales.csv` with columns:
date, day, location, jenis, order_qty, baki, sold, price_rm, revenue_rm

## Pitfalls

- User frequently adjusts numbers mid-session — always confirm final total before generating PDF
- "Berlauk buang" means remove from all calculations, not just that line
- Lelong figures are separate from regular sales and use RM 2.50
- When user says "darab kan dgn harga yg aku bagi" — use the prices from the pricing table above
- When calculating revenue for orders (not vendor claims), use supplier cost prices (RM 1.20/1.50)
- When calculating revenue for vendor claims, use customer selling prices (RM 2.50/3.00/3.50)
- DSP and DSW are separate vendors even though orders look similar
- "Mamak 2 ada 2 kedai" / "Lrt S ada 3 kedai" — user sometimes clarifies sub-locations; account for these when calculating per-kedai averages
