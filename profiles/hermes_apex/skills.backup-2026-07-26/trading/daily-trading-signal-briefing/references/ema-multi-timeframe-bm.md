# EMA Crossover & Multi-Timeframe Analysis (BM)

> Teaching session with Arif, 2026-07-17
> Audience: rakyat marhaen, Abang Sado level

## Tiga Trend Sahaja

Dunia trading cuma ada 3 trend — **upward 📈, downward 📉, sideways 📊.** Semua indicator lain hanyalah alat untuk detect 3 benda ni.

## EMA20 × EMA50 — Golden Cross & Death Cross

### Apa maksud dia

EMA (Exponential Moving Average) = purata harga bergerak, yang bagi lebih berat pada harga terkini.

```
EMA20 = purata 20 candle terakhir (FAST — responsif)
EMA50 = purata 50 candle terakhir (SLOW — stabil)
```

### Dua jenis cross

| Cross | Apa jadi | Makna |
|---|---|---|
| **Golden Cross** ☀️ | EMA20 naik potong EMA50 dari bawah | Uptrend baru — bullish |
| **Death Cross** 💀 | EMA20 turun potong EMA50 dari atas | Downtrend baru — bearish |

### Masalah EMA cross

1. **Lagging.** Bila cross keluar, half the move dah lepas. EMA adalah *trailing indicator*, bukan *leading*.
2. **Whipsaw.** Sideways market — cross palsu berulang kali. Kena stop loss banyak kali.
3. **Tak cukup konteks.** EMA cross tak tau pasal support/resistance, volume, session, news.

### Peraturan guna EMA cross

- EMA cross = **confirmation**, bukan **trigger**
- Jangan entry semata-mata sebab cross
- Tunggu price action confirm (candle close, rejection, retest)
- Cross tanpa confluence ≥2 = abaikan

## Multi-Timeframe Analysis — H4 + H1

### Apa itu H4 dan H1?

```
H4 = 4-hour candle — peta negeri (big picture)
H1 = 1-hour candle — peta jalan kampung (detail entry)
```

Satu candle = satu bar pada chart. H4 ambil 4 jam untuk satu candle terbentuk. H1 ambil 1 jam.

### Peraturan Emas

```
H4 cakap ARAH mana  →  H1 cakap BILA masuk

H4 dulu, H1 kemudian. JANGAN TERBALIK.
```

| H4 kata... | Action pada H1 |
|---|---|
| UPTREND | Cari BUY je |
| DOWNTREND | Cari SELL je |
| SIDEWAYS | Duduk diam — jangan trade |

### Kenapa dua timeframe, bukan satu?

| Guna satu je | Masalah |
|---|---|
| H1 sorang | Noise. Whipsaw. Signal palsu banyak. |
| H4 sorang | Lambat. Bila signal keluar, move dah大半 lepas. |
| **H4 + H1** | H4 bagi trend besar, H1 bagi timing tepat. |

### Cara guna — 3 step

1. **Buka H4** → tanya: "Trend besar UP ke DOWN?"
2. **Switch H1** → tanya: "H1 dah aligned dengan H4 ke belum?"
3. **Belum aligned?** → SABAR. Jangan masuk.
4. **Dah aligned?** → Cari candle confirm, baru entry.

### Trade hanya bila aligned

```
H4 downtrend + H1 pullback naik  → SABAR (tunggu H1 turun balik)
H4 downtrend + H1 mula turun     → READY (cari SELL entry)
H4 uptrend   + H1 pullback turun → SABAR (tunggu H1 naik balik)
H4 uptrend   + H1 mula naik      → READY (cari BUY entry)
```

## Gold Engine Implementation

Gold engine di `/root/trading/` guna logic yang sama:

- **Regime detection = H4 function** — guna EMA20/50/200 position untuk tentukan UPTREND/DOWNTREND/SIDEWAYS
- **Signal trigger = H1 function** — guna price action, S/R proximity, candle pattern, RSI divergence
- **Confluence ≥2 required** — single indicator = rejected (F3 WITNESS)
- **Multi-timeframe alignment wajib** — kalau regime DOWNTREND tapi H1 naik → SABAR

### Live example (2026-07-17)

```
H4 regime: DOWNTREND (EMA20 $4,007 < EMA50 $4,014, confidence 95%)
H1 state:  Price $4,023 > both EMAs — PULLBACK dalam downtrend
Verdict:   SABAR — H1 belum aligned dengan H4
```
