# Business Receipt / Vendor Claim PDF Template

Quick weasyprint HTML template for vendor claim receipts. Proven 2026-07-23,
multiple sessions, zero rendering failures.

## Title Convention

Use "CLAIM VENDOR — V005" (not "RESIT", not "VENDOR CLAIM PAYMENT").
The user corrected this multiple times. Stick with CLAIM VENDOR.

## Proven HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
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
</style>
</head>
<body>
<h1>CLAIM VENDOR — V005</h1>
<p class="date">XX BULAN 2026 (HARI)</p>
<table>
<tr><th>Vendor</th><th>Item</th><th>Hantar</th><th>Baki</th><th>Sold</th><th>Harga (RM)</th><th>Jualan (RM)</th></tr>
<!-- rows here -->
<tr class="total"><td colspan="6">TOTAL</td><td>XXX.XX</td></tr>
</table>
</body>
</html>
```

## Column Meanings

| Column | Meaning |
|---|---|
| Hantar | Total units sent to vendor |
| Baki | Units returned unsold |
| Sold | Units actually sold |
| Harga | Price per unit (RM) |
| Jualan | Sold × Harga |

Lelong entries: create separate row, mark as "Lelong (item)", use lower lelong price (usually RM 2.50).

## Render

```bash
cd /path/to/workdir && weasyprint file.html file.pdf
```

## Pitfalls

- **Title corrections:** User will push back if title says "RESIT" or "VENDOR CLAIM PAYMENT". Use "CLAIM VENDOR — V005".
- **Weasyprint available:** Already installed on af-forge VPS. No setup needed.
- **Date format:** "DD BULAN 2026 (HARI)" — e.g. "22 JULAI 2026 (KHAMIS)". Use Malay month/day names.
- **Missing totals:** Always fill the TOTAL row. User expects consolidated jualan.
- **Empty template confuses user:** If sending a blank template for new date, pre-fill vendor names from previous day if the user says "ikut semua data".
