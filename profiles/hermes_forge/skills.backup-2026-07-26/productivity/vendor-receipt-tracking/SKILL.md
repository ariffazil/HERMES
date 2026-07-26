---
name: vendor-receipt-tracking
description: "Track vendor food orders — hantar, baki, sold, revenue — and generate claim/receipt PDFs with navy/gold formatting."
tags: [vendor, receipt, nasi-lemak, claim, pdf, food-business]
triggers:
  - "claim payment"
  - "vendor claim"
  - "resit vendor"
  - "buat macam tadi"
  - "buat utk [vendor]"
---

# Vendor Receipt Tracking

Track multi-vendor food orders (nasi lemak variants) across locations. Produce structured tables and PDF receipts using weasyprint HTML→PDF pipeline.

## Data Model

Each vendor entry tracks:

| Field | Description |
|---|---|
| **Vendor** | Location/name (DSW, DSP, LRT Setiawangsa, EVEN, etc.) |
| **Item** | Type — Telur Mata, Telur Rebus, Telur Dadar, Berlauk, or combined |
| **Hantar** | Units dispatched |
| **Baki** | Unsold returns |
| **Sold** | Units sold (Hantar - Baki) |
| **Harga** | Price per unit (RM) |
| **Jualan** | Revenue (Sold × Harga) |

## Variant Pricing

| Variant | Standard Price | Lelong Price |
|---|---|---|
| Telur Mata 🍳 | RM 3.50 | RM 2.50 |
| Telur Rebus 🥚 | RM 3.00 | RM 2.50 |
| Telur Dadar | RM 3.00 | RM 2.50 |
| Mixed (campur) | RM 2.50 | - |
| Berlauk 🥩 | Varies (cash term) | - |

## PDF Generation

Use weasyprint HTML→PDF pipeline. See `references/claim-table-template.html` for the reusable navy/gold HTML template.

Quick command:
```bash
cd /root/forge_work/YYYY-MM-DD \
  && weasyprint vendor_claim.html vendor_claim.pdf
```

### Title Variants

User alternates between two titles — confirm which one before generating:
- **"CLAIM VENDOR — V005"** — for payment claims
- **"RESIT VENDOR — V005"** — for receipts

## Interactive Editing Pattern

This user provides vendor data incrementally across multiple messages:
1. Initial order data (hantar)
2. Baki (returns)
3. Harga/jualan
4. Corrections and adjustments

DO NOT wait for all data at once. Build the table progressively — update after each message. Generate PDF only when user explicitly asks or when data appears final.

## Pitfalls

- User often corrects numbers multiple times. Keep the working table visible and confirm each change before regenerating PDF.
- Some vendors report in mixed categories (e.g., "Dadar + Rebus" combined) — keep as-is, don't force-split.
- Lelong (clearance) items are separate line items at RM 2.50 regardless of variant type.
- "Hantar 16 tolak Baki 0 = jual 16" means Hantar=16, Sold=16 — don't over-complicate the math.
