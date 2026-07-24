---
name: nasi-lemak-tracking
description: Track multi-location nasi lemak daily orders, baki, sales, and revenue. Calculate per-variant and per-location totals. Save to structured CSV
tags: [nasi-lemak, sales, tracking, business, food]
---

# Nasi Lemak Sales Tracking

Khairuddin runs a multi-location nasi lemak delivery business. He sends daily order data
per location, then later reports remaining stock (baki). This skill handles tracking,
calculation, CSV persistence, and summary generation.

## Product Variants & Pricing

| Variant | Emoji | Price/unit |
|---|---|---|
| Telur Mata | 🍳 | RM 1.50 |
| Telur Rebus (keras) | 🥚 | RM 1.20 |
| Telur Rebus Separuh (half-boiled) | 🥚 | RM 1.20 |
| Telur Dadar | 🍳(same) | RM 1.20 |
| Berlauk | 🥩 | Cash term — EXCLUDED from standard calc |

## Key Rules

1. **Berlauk is ALWAYS excluded** from sales summaries and revenue calculations unless the user explicitly asks for it. When user says "berlauk buang" or "berlauk xyah kira", remove it entirely from output.
2. **Baki deduction**: Revenue only counts SOLD items, not orders.
3. **Multi-day tracking**: Each day gets its own section. Compare across days when user asks.
4. **User may adjust quantities mid-conversation** ("tolak 10 telur mata") — apply adjustments immediately.
5. **Sambal types** (campur, asing) are noted in order data but don't affect pricing.
6. **Cash term berlauk variants** include: paru, dendeng, ayam goreng, sambal sotong. Track separately when provided.

## Data Storage

Save to: `/root/forge_work/YYYY-MM-DD/nasi_lemak_sales.csv`

CSV columns:
```
date,day,location,jenis,order_qty,baki,sold,price_rm,revenue_rm
```

- `baki` and `sold` may be blank initially (pending reports)
- Use Python `csv.DictReader` for reading

## Analysis Output Format

Always present data in tables with emojis for variants.

### 1. Per-Day Summary Table
```
| Lokasi | Rebus 🥚 | Mata 🍳 | Dadar | Total |
```

### 2. Per-Variant Summary
```
| Jenis | Order | Sold | Sold % | Revenue |
```

### 3. Cross-Day Comparison (when applicable)
```
| Hari | Total Order | Revenue |
```

## Revenue Calculation

Use `execute_code` to compute:
- Revenue per row = `sold × price_rm`
- Skip rows where `sold` is blank (pending baki)

## Known Locations

Setiawangsa, Wangsa Maju, BSW, DP, MAMAK 1, MAMAK 2, KEDAI P, KEDAI L, KEDAI A,
LRT S, LRT WM, EVEN, DSW, DSP

### Sub-Kedai Counts (for per-kedai averages)

| Location | Sub-Kedai |
|---|---|
| MAMAK 2 | 2 |
| LRT S | 3 |
| Others | 1 each |

## Sambal Types

| Sambal | Meaning |
|--------|---------|
| **Campur** | Sambal mixed in with the nasi lemak |
| **Asing** | Sambal packed separately in a container |

Does NOT affect pricing. Track for accuracy.

## Order Entry Format (Syed's standard)

Syed sends orders in a structured text format. Parse consistently:

```
LOCATION CODE
1. Nasi lemak telur [jenis] sambal [campur/asing] [qty]
2. Nasi lemak telur [jenis] sambal [campur/asing] [qty]
3. Nasi lemak berlauk [jenis] [qty]- cash term
```

Prices at the end are for reference (per-unit):<br>
Telur mata = RM1.50 | Telur dadar = RM1.20 | Telur rebus (keras/separuh) = RM1.20 | Nasi berlauk = RM1.50

## Order Entry Rules

1. When user says "cash term" or "berlauk" — those items are **excluded** from standard sales/revenue calculations
2. If user says "Sambal asing" vs "Sambal campur" — note but don't split on price
3. "Telur rebus separuh" = half-boiled egg (different from telur rebus keras). Same price RM1.20
4. Some locations (EVEN, MAMAK 2) have stand-alone codes without numbering

When user asks "purata per kedai" — divide location total by sub-kedai count.

## Supplier Cost vs Revenue

**User's revenue** = what he collects from customers (sold × his retail price).
**Supplier cost** = what he pays to nasi lemak supplier (sold × supplier price).
Supplier prices SAME as user's standard prices (Mata RM1.50, Rebus/Dadar RM1.20).

Unsold items: user still pays supplier unless negotiated return. Calculate both scenarios:
- With return: profit = revenue − (sold × supplier price)
- Without return: profit = revenue − (all ordered × supplier price)

## Supplier Negotiation

When user asks "ok ke nak bayar supplier":
- Unsold rate on weekdays ~24%, weekends lower
- Present per-kedai average unsold (~5-7 bungkus) — looks better than total
- Total revenue vs supplier cost comparison gives leverage
- User needs to know profit margin before negotiating

## Voice/Tone

- **Full BM** — user will correct if you use English. Respond entirely in Bahasa Melayu.
- Use with both Khairuddin and Syed — both prefer BM casual
- Short sentences
- Tables with emojis
- No markdown fluff — direct numbers
- When user says "simpan" or "buat summary", save to CSV + give analysis
- When user gives correction (e.g. "salah" or "abaikan"), acknowledge quickly and move on — no lengthy apologies
