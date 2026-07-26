# Money Management — Agentic Intelligence Framework

> Dikemas kini 2026-07-17 dari sesi live Syed + pengiraan Kelly

## 5 Peraturan Besi (Agent-Enforced)

| # | Peraturan | Agent Buat Apa | Kenapa |
|---|---|---|---|
| 1 | Risk 1% je per trade (default) | Agent kira lot size automatik | 2% risk dah -359% dalam backtest 2 tahun |
| 2 | Max loss sehari 3% | Agent circuit-breaker — sampai 3%, lock sampai esok | Revenge trade prevention |
| 3 | R:R minimum 1:2 | Agent scan setup — reward < 2x risk = block | 33% win rate je nak breakeven |
| 4 | SL: 2× ATR | Agent letak automatik | 1× ATR = noise stop; 2× ATR = ruang bernafas |
| 5 | Max 2-3 position serentak | Agent kira total exposure | Concentration risk dari satu berita |

## Agent vs Manusia

| Situasi | Manusia | Agentic Intelligence |
|---|---|---|
| Lepas 3 loss berturut | "Kali ni mesti jadi." Double lot | Lock account sampai esok |
| Lepas win besar | Euforia, cari setup merata | Tenang. Still 1%. Tunggu confluence ≥2 |
| Sideways / chop | "Mesti breakout ni." Masuk | Skip terus — 40.8% win rate, net negative |
| Red news (CPI/NFP/FOMC) | "Aku rasa dia naik." | Tutup semua T-15min, tunggu T+30min |
| Harga dekat SL | Gerakkan SL | Agent tak gerak. Disiplin = survival |

## Kelly Criterion untuk Sistem Syed

Backtest 2 tahun, 294 trades:
- Win rate: 45.9%
- R:R: 1:2
- Kelly optimal fraction: **18.85%**
- Half-Kelly: **9.43%**
- Quarter-Kelly: **4.71%**

### Kelly Formula (untuk rerun)

```
f* = (p * b - q) / b
where:
  p = win probability (0.459)
  q = loss probability (0.541)
  b = odds (2.0 for 1:2 R:R)

f* = (0.459 * 2.0 - 0.541) / 2.0
f* = (0.918 - 0.541) / 2.0
f* = 0.377 / 2.0
f* = 0.1885 → 18.85%
```

## Jadual Drawdown Recovery

| Drawdown | Gain Diperlukan untuk Breakeven |
|---|---|
| -10% | +11% |
| -20% | +25% |
| -30% | +43% |
| -41% | **+69%** |
| -50% | **+100%** |
| -75% | +300% |

**Rule:** Lagi dalam jatuh, lagi curam nak panjat balik. Ini matematik paling kejam dalam trading.

## 5 Loss Berturut-turut — Realiti Dengan 10% Risk

Probability 5 loss berturut-turut dengan win rate 45.9%:
```
0.541^5 = 4.6% → berlaku sekali setiap ~22 sequence
```

Dengan balance $500, risk 10%:

| Trade | Risk | Baki |
|---|---|---|
| Mula | — | $500 |
| Loss 1 | -$50 | $450 |
| Loss 2 | -$45 | $405 |
| Loss 3 | -$40.50 | $364.50 |
| Loss 4 | -$36.45 | $328.05 |
| Loss 5 | -$32.81 | **$295.25** (-41%) |

## Fasa Risk — Cadangan Agent

| Fasa | Risk/Trade | Syarat |
|---|---|---|
| Fasa 1 (sekarang) | 2% | 20 trade tanpa langgar rules |
| Fasa 2 | 5% | 50 trade, max DD < 15% |
| Fasa 3 | 10% | Dah proven. Half-Kelly. |

## Agent Takkan Buat

- ❌ Takkan bagi tambah lot bila loss (martingale = bankruptcy)
- ❌ Takkan bagi trade tanpa SL
- ❌ Takkan bagi guna duit sewa untuk trade (APEX-4)
- ❌ Takkan janji profit — agent cuma enforce disiplin
