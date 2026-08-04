># Visual-First PDF — Chat Recap Template

For any visual-first market PDF request (e.g. "PDF live gold today + week trend"), the chat-side message must be SPARSE. The PDF carries the picture; chat carries the delivery notice.

## Rule (hard)

**≤ 8 markdown lines in chat.** Never repeat values that are already labelled on the chart. The user wants to open ONE PDF and see the whole picture. Anything beyond a delivery notice wastes their thumb-scroll.

## Template — verified 2026-08-04 against gold live PDF

```markdown
Siap, Arif. **PDF visual live XAUUSD + trend minggu depan** dah dijana berdasarkan feed pada **04 Ogos 2026, 13:40 MYT**.

📄 **PDF:**
MEDIA:/tmp/gold_live_weekly_intelligence.pdf

📊 **Chart PNG:**
MEDIA:/tmp/gold_live_weekly_chart.png

### Ringkasan paling pendek

- **Harga live:** USD 4,055.69/oz
- **Bacaan:** neutral → bearish ringan
- **Range utama:** 4,040–4,075
- **Bullish hanya jika:** candle H1 tutup atas 4,063
- **Bearish jika:** candle H1 tutup bawah 4,040
- **Zon penting:**
  - Beli reaktif: 4,048–4,054
  - Jual/rejection: 4,059–4,063
  - Sasaran atas: 4,062 / 4,072
  - Risiko bawah: 4,040 / 4,025 / 4,000

**[OBS]** Feed live dalaman menunjukkan RSI 57, EMA20 sedikit bawah EMA50, dan harga hampir EMA200.
**[DER]** Level chart dikira daripada struktur 7 hari, EMA, RSI dan pivot semasa.
**[INT]** Minggu depan berpotensi kekal range-bound sehingga data pekerjaan AS, USD dan hasil Treasury beri catalyst.
**[UNKNOWN]** Tiada jaminan arah; news boleh ubah setup dalam satu candle.

⚠️ Ini **bukan arahan beli/jual**. Jangan kejar candle. Tunggu candle tutup dan retest; leverage/CFD boleh menyebabkan kerugian besar.
```

## What to REMOVE in visual-first mode

- ❌ Long narrative summary of price action
- ❌ Repeated RSI / EMA / pivot values (already on chart)
- ❌ "Kau boleh tengok dalam chart… / Sila rujuk carta…" filler
- ❌ Sentiment reasoning paragraphs
- ❌ "Disclaimer panjang lebar" — keep one line

## What to KEEP

- ✅ `MEDIA:` PDF link (primary deliverable)
- ✅ `MEDIA:` PNG link (fallback / preview)
- ✅ ≤ 8-line bullet recap of NON-CHART context (price, sentiment tag, bull/bear trigger)
- ✅ Epistemic tags `[OBS]/[DER]/[INT]/[UNKNOWN]` — they're cheap and the user values them
- ✅ One-line risk disclaimer

## Why this works

The user said "minimize text focus on visual deliver for human cognitive understanding" — the human brain processes a labelled chart in ~2 seconds. The same information as prose takes 30+ seconds to read and re-construct mentally. The PDF + sparse-chat pattern respects that.