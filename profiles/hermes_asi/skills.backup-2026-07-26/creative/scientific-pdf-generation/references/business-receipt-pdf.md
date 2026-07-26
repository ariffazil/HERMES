# Business Receipt / Claim PDF (Weasyprint HTML)

Quick pattern for generating simple business receipt/claim PDFs using weasyprint HTML — proven for vendor claim summaries, sales reports, and similar one-page table documents.

## When to Use

- Vendor claim payments
- Sales receipts
- Simple financial summaries
- Any one-page table-heavy business document

**NOT** for analyst reports (use Mode C in parent skill), scientific papers (Mode A), or intelligence dossiers (Mode B).

## Quick Recipe

### 1. HTML Template

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
  .footer { text-align: center; color: #6B7280; font-size: 8pt; margin-top: 30px;
            border-top: 1px solid #e5e7eb; padding-top: 15px; }
</style>
</head>
<body>
<h1>CLAIM VENDOR — V005</h1>
<p class="date">DD BULAN TAHUN (HARI)</p>
<table>
<tr><th>Vendor</th><th>Item</th><th>Hantar</th><th>Baki</th><th>Sold</th><th>Harga (RM)</th><th>Jualan (RM)</th></tr>
<!-- data rows -->
<tr class="total"><td colspan="6">TOTAL</td><td>XXX.XX</td></tr>
</table>
<p class="footer">Dijana oleh Hermes Agent — DD Bulan Tahun</p>
</body>
</html>
```

### 2. Generate PDF

```bash
cd /root/forge_work/YYYY-MM-DD
weasyprint vendor_claim.html vendor_claim.pdf
```

### 3. Deliver

Send with `MEDIA:/path/to/file.pdf` in Telegram.

## Pitfalls

- **Title changes:** User may ask to switch between "CLAIM VENDOR", "RESIT VENDOR", "VENDOR CLAIM PAYMENT". Patch the HTML `<h1>` and regenerate.
- **Date format:** Use Malay format: "23 JULAI 2026 (RABU)". Day names: Ahad, Isnin, Selasa, Rabu, Khamis, Jumaat, Sabtu.
- **Partial data:** When data is incomplete (no baki/sold), leave those cells empty and add a note below the table. Don't make up numbers.
- **Totals:** Always recalculate total hantar, total baki, total sold, total jualan after every edit.
- **weasyprint available:** This VM has weasyprint installed. If missing: `pip install weasyprint --break-system-packages`.
- **File organization:** Use per-date directories: `/root/forge_work/YYYY-MM-DD/`.
