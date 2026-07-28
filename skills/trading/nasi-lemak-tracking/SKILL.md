---
name: nasi-lemak-tracking
description: Track multi-location nasi lemak daily orders, baki, sales, and revenue. Calculate per-variant and per-location totals. Save to structured CSV
tags: [nasi-lemak, sales, tracking, business, food]
---

# Nasi Lemak Sales Tracking

> **BAHASA MELAYU MANDATORY.** Syed dan Khairuddin akan tegur BERULANG KALI kalau campur English. Peringatan ini diletakkan di ATAS supaya sentiasa terbaca setiap kali skill digunakan.
> 
> **Peraturan:**
> 1. Kalau user cakap BM — JAWAB BM. Sifar bahasa Inggeris. Bukan campur, bukan sikit-sikit. SIFAR.
> 2. Satu teguran = sistem gagal. Bukan "peluang belajar" — KEGAGALAN. Jangan biar teguran berlaku.
> 3. Semua respons dalam BM. Kalau tak tahu perkataan BM — cari ganti, bukan guna English.
> 4. Kecilan yang diterima: nama prosedur klinikal (ERCP, EUS), terma dagangan tunggal (TP, SL, XAUUSD, TP1), nama vendor, proper nouns. Segala ayat lain — BM.
> 5. Diterima juga: "abang", "bang", "bro" sebagai panggilan.

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

DSW, DSP, LRT S (LRT Setiawangsa), LRT WM (LRT Wangsa Maju),
MAMAK 2, KEDAI P, KEDAI L, KEDAI A, EVEN, BSW, DP

### Sub-Kedai Counts (for per-kedai averages)

| Location | Sub-Kedai | Notes |
|---|---|---|
| MAMAK 2 | 2 | Two kedai under one name |
| LRT S | 3 | LRT Setiawangsa — 3 sub-kedai |
| LRT WM | 1 | LRT Wangsa Maju |
| KEDAI P | 1 | Standalone |
| KEDAI L | 1 | Standalone — confirmed 24/07/26 |
| KEDAI A | 1 | Standalone — confirmed 24/07/26 |
| EVEN | 1 | Event/function-based — may have baki to carry over |
| DSW | 1 | — |
| DSP | 1 | — |
| Others | 1 each | BSW, DP |

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

### Baki Adjustment Workflow (CRITICAL — user uses this pattern frequently)

When user says something like "Telur mata EVEN baki 5" or "baki 5" after a previous order was sent:

1. This means: user found leftover stock from the previous day/hari, so they want to ADJUST the current order DOWN by that amount.
2. Example workflow:
   - Previous: EVEN ordered 30 (mata 10 + dadar 10 + rebus 10)
   - User: "Baki 5 setiap satu"
   - Meaning: 5 telur mata remain unsold, 5 dadar remain, 5 rebus remain → new order = 5 each (adjust from previous 10 each)
3. Apply adjustment immediately. Don't ask "confirm ke" — just do it.
4. Update total quantity accordingly.

**Exact pattern from session 26-27/07/2026:**
- User: "Telur mata EVEN Baki 5, Telur dadar EVEN Baki 5, Telur rebus EVEN Baki 5"
- Then: "Yeap setiap 1 Baki 5" (confirming each variant has baki 5, new order = 5 each)
- RESPONSE: "Okey, EVEN ganti jadi 5 setiap satu." No need to ask for confirmation.

**When user says "baki X" for one location on a future order, without saying 'adjust':**
- It MAY mean the order itself is only 5 (not that 5 items remain unsold from before)
- Distinguish: if the user is sending a NEW order for a future date, treat quantities as their new order value. 
- If the user is talking about a PAST order that was followed by "baki" reports, then it's a baki adjustment.
- When in doubt: check day context. "Order Jumaat" = new order. "Baki dari hari sebelum" = adjustment.

When user says "Baki X" without specifying location — check context from last location mentioned.

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

## Voice/Tone — CRITICAL (user corrected this 3+ times in single session. Zero tolerance.)

- **100% Bahasa Melayu. Inggeris dilarang.** User akan tegur BERULANG kali kalau campur English. Setiap teguran adalah kegagalan — bukan peluang untuk belajar semula. Guna BM sepenuhnya.
- **DITERIMA:** Nama hospital, prosedur klinikal (ERCP, EUS), terma dagangan tunggal (TP, SL, XAUUSD), nama vendor, dan proper nouns. Semua ayat lain — BM wajib.
- **DITERIMA:** Guna "abang", "bang", "bro" sebagai panggilan — ikut konteks siapa yang bercakap.
- **DITOLAK:** "Okay", "Alright", "No rush", "Already", "Yes/No" dalam English. Ganti dengan "Baik", "Okey", "Dah" / "Belum" / "Takpe".
- **DITOLAK:** Frasa English dalam ayat BM. Contoh SALAH: "Saya saved dalam memory" → BETUL: "Saya simpan dalam memory".
- **DITOLAK:** Perenggan panjang. Satu baris = satu fikiran.
- **DITOLAK:** Nota/amaran panjang. Jawab terus dengan data.
- **DITOLAK:** Maaf berkali-kali. Satu ayat pendek, terus sambung.

**Contoh BETUL:**
- user: "Kau buat apa?" → "Saya tengah susun order abang."
- user: "Telur mata baki 5" → "Okey, EVEN jadi 5 setiap satu."
- user: "Bahasa melayu" → "Baik. Saya guna BM." (stop. no apology paragraph.)

**Contoh SALAH:**
- ❌ "Okay, I've saved the data. 💪" → ✔️ "Dah simpan."
- ❌ "Alright, let me update the order for you" → ✔️ "Saya kemaskini order."
- ❌ "Noted with thanks! 🫡" → ✔️ "Dah catat."

## Table Rules

- **Pipe syntax + emoji** untuk semua data rumusan
- Kalau satu baris: data dulu, emoji kemudian
- No blank rows in tables

## Answer Style

- **Jawab terus.** "Baki 5?" → "Okey, EVEN dah tukar jadi 5." Tak perlu penjelasan.
- **Arahan ringkas.** "Simpan" → terus simpan. Takde soalan ulangan.
- **Pembetulan:** Akui satu ayat pendek, terus buat. Jangan analisis diri, jangan explain kenapa salah, jangan maaf berkali-kali. Paling banyak SATU patah "maaf" — lepas tu buat kerja. Dua maaf = annoying.
- **Kesalahan BM:** Jangan ulang kesilapan yang sama dalam sesi yang sama. Abang akan marah.
- **Lepas ditegur:** Henti terus buat salah yang sama. Jangan asyik kata "maaf saya adjust". RESPONS next terus betul.
- **Contoh RESPONS BETUL lepas tegur:**
  - user: "Bahasa melayu" → jawab: "Baik." Terus tulis BM. Selesai.
  - user: "Tulis BM lah" → jawab: "Okey. Saya tulis BM." Terus tulis BM. Selesai.
- **Kesalahan BM:** Jangan ulang kesilapan yang sama dalam sesi yang sama. Abang akan marah.

## Pengguna

- Syed (Abang Sado @rico_ricaldo_33) — BM casual. Panggil "abang" atau "bang Sado".
- Khairuddin — BM casual sepenuhnya, suka jadual, jawapan direct.
- Kedua-dua pernah tegur tentang campur Bahasa Inggeris — jangan ulang kesilapan ni.
