# Voice Briefing Format — Daily SADO

Pattern for generating a 90-second BM voice briefing for Abang Sado Syed (and any other Malaysian XAUUSD trader). Proven in cron job `2258f1b3fa0e` (8am MYT, SADO group) on 2026-07-18.

## Technical Recipe

```bash
cat > /tmp/syed_voice.txt << 'EOF'
[script content — populate at run time from market data]
EOF
edge-tts --voice ms-MY-OsmanNeural --rate "+5%" \
  --file /tmp/syed_voice.txt --write-media /tmp/syed_voice.mp3
```

| Parameter | Value | Why |
|---|---|---|
| Voice | `ms-MY-OsmanNeural` | Male, BM native. Masculine tone matches Abang Sado archetype. |
| Rate | `+5%` | Slightly faster for casual tone. Dense analysis → `-5%` instead. |
| File input | `--file` (not `--text`) | Handles long content reliably — edge-tts breaks on very long `--text` strings. |
| Format | `.mp3` | Telegram renders as voice bubble natively. |

**Fallback chain:** MiMo V2.5 voicedesign (if Penang-style needed) → OpenAI TTS (if quota) → edge-tts (always free).

## Script Template

```
Abang Sado, ni update gold [hari ni / pagi ni]. Harga sekarang [spell out] dolar.

[Cerita — 2-3 sentences. Apa berlaku: drop / range / rebound.]

Ada support kat [spell out] — kalau pecah sini, [target].
Ada resistance kat [spell out] — kalau pecah sini, [target].

Trend besar [atas / bawah] — EMA200 kat [spell out].
RSI [number] — [cold / neutral / hot].

Sistem bagi [SEAL / SABAR / HOLD / VOID]. [Sebab ringkas.]

Aturan: [action — tunggu break / buy zona / sell zona / jangan trade].

Trade selamat, abang.
```

## Numbers — Spell Them Out

The `tts-edge-fallback` skill's full BM number rules:

| Written | Spoken |
|---|---|
| $4,023 | "empat ribu dua puluh tiga dolar" |
| $67 | "enam puluh tujuh dolar" |
| 4 hours | "empat jam" |
| 4019.73 | "empat ribu sembilan belas perpuluhan tujuh puluh tiga" — or round: "empat ribu dua puluh" |
| 63.6 | "enam puluh tiga perpuluhan enam" |
| +0.08% | "naik sikit, kosong perpuluhan kosong lapan peratus" |
| 1:2 R:R | "satu banding dua, reward ratio" |

**Rule:** Always round to whole numbers when speaking time-price horizons (easier to follow). Spell decimals when precision matters (RSI, ATR, exact support/resistance).

## Verdict → Action Mapping

| API verdict | Voice style | Use when |
|---|---|---|
| `SEAL` | Confident, "ada setup, masuk" | Strong confluence + clear direction |
| `SABAR` | Calm, "tunggu, jangan trade" | Range-bound, mixed signals |
| `HOLD` | Neutral, "ada posisi, jaga" | Existing position, no clear next move |
| `VOID` | Direct, "jangan main hari ni" | High risk event (NFP, FOMC) | 

**Critical (Bengang protocol):** If user has expressed "jiwa x kuat" earlier in the day, demote any SEAL → SABAR. Witness > edge.

## What NOT To Say

- ❌ "Setup valid" — too jargon, translation loses meaning
- ❌ "Confluence 0.85" — number without context
- ❌ "Death cross imminent" — bearish literary
- ❌ "Reward to risk ratio optimal" — broker-speak
- ❌ "Hang kena monitor closely" — passive aggressive lecture
- ❌ Anything that implies "I know you better than you know yourself"

## What ALWAYS To Include

- ✅ Current price (so Syed knows he's hearing today's data)
- ✅ Support + resistance (the two numbers he needs)
- ✅ Verdict + 1-line sebab
- ✅ One specific action (buy zone OR sell zone OR tunggu break)
- ✅ Closing "trade selamat, abang" — identity-locking signal that this is HIS trade, not the system's

## Variations By Session

| Session | Voice opening | Action bias |
|---|---|---|
| Asia (08:00) | "pagi ni" | Asian range, low vol — emphasis on tunggu |
| London (15:00) | "London baru buka" | Highest vol — full briefing, R:R fresh |
| NY (20:30) | "New York session" | News-driven — macro context mandatory |
| Late NY (23:00) | "hujung hari" | Wrap-up, R:R review tomorrow |

## Multi-Channel Delivery

Always send voice + text + chart together. Reasons:
- **Visual learners** read the text
- **Audio learners** listen to voice (Syed prefer this when driving EV, at gym, F&B peak)
- **Cross-check** — same data, 3 formats. If one feels off, two more confirm.
- **Memory** — voice is encoded longer than text (proven in learning research)

**Telegram delivery notes:**
- Voice note → file `.mp3`, sent as voice bubble
- Chart → `.png`, sent as photo
- Text → markdown, reformatted for mobile legibility (no tables wider than 5 cols, no chained bullet nesting)
- Order in chat: text first → chart → voice (so text is searchable / citable, voice anchors emotional)

## Edge-TTS Free Tier Gotchas

- ~10 requests/minute. If multiple briefings run same minute, queue them or skip voice (text-only fallback message: "voice not ready, teks dulu")
- `--text` breaks on very long strings (>2000 chars). Use `--file` instead.
- Voice IDs are case-sensitive: `ms-MY-OsmanNeural` not `ms-MY-osmanneural`.

## Examples From Session 2026-07-18 (Price $4,023)

> "Abang Sado, ni update gold petang ni. Harga sekarang empat ribu dua puluh tiga dolar. Semalam malam, gold jatuh besar — dalam empat jam ja, jatuh enam puluh tujuh dolar, dari empat ribu lapan puluh sembilan turun ke empat ribu dua puluh dua. Tu drop yang kena respect.
>
> Tapi lepas jatuh tu, dia tak jatuh lagi. Dia menggolek kat area empat ribu dua puluh, macam berehat. Ada support kat empat ribu sembilan belas — kalau pecah bawah ni, baru boleh jatuh lagi ke empat ribu sepuluh atau tiga ribu sembilan ratus sembilan puluh lapan.
>
> Ada resistance kat empat ribu dua puluh enam — kalau pecah atas ni, baru boleh naik ke empat ribu tiga puluh satu.
>
> Trend besar masih bawah — EMA dua ratus kat empat ribu empat puluh, atas kepala kita. RSI kat enam puluh tiga — neutral, dah mula panas, tapi belum overbought.
>
> Sistem bagi verdict SABAR — tu code untuk tunggu. Bukan tak ada peluang, tapi range sempit sangat. Main sini kena stop loss ketat, tak berbaloi.
>
> Aturan utama: jangan paksa entry. Tunggu gold pecah support empat ribu sembilan belas, baru fikir sell. Atau tunggu pecah resistance empat ribu dua puluh enam, baru fikir buy.
>
> Sampai chart bagi break, kita sabar. Hari ni bukan hari untuk trade. Esok boleh jadi cerita lain.
>
> Ok abang, tu je. Trade selamat."

This was 94 seconds. Trim to ~75s by cutting the closing repetition.

## Reuse Beyond Syed

Same format works for:
- Other BM-speaking XAUUSD traders in SADO group (each gets own voice, but same template)
- Brent crude and gas briefings (substitute "gold" → "minyak"/"gas" and "XAUUSD" → ticker)
- Personal finance briefings (spending review, savings update — change "support/resistance" → "budget/savings rate")
