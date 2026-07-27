# Syed's Nasi Lemak Location Codes

Standardised location codes for Syed/Abang Sado (@rico_ricaldo_33) orders.

| Code | Full Name | Notes |
|------|-----------|-------|
| DSW | — | Stall 1 |
| DSP | — | Stall 2 |
| LRT Setiawangsa | LRT Setiawangsa | Also "LRT S" |
| LRT Wangsa Maju | LRT Wangsa Maju | Also "LRT WM" |
| MAMAK 2 | Mamak 2 | 2 sub-kedai |
| KEDAI P | Kedai P | — |
| KEDAI L | Kedai L | — |
| KEDAI A | Kedai A | — |
| EVEN | EVEN | Stand-alone code |
| Yuliana's Melati | Yuliana Melati | Taman Melati, Wangsa Maju |

## Status Sambal = Asing vs Campur

Setiap variant telur ada dua mod sambal:
- **Sambal campur** = sambal digaul dalam nasi
- **Sambal asing** = sambal pek berasingan

Harga sama untuk kedua-dua. Bezanya cara packing je.

## Order Text Format (raw input)

Syed sends orders as:

```
LOCATION
1. Nasi lemak telur [jenis] sambal [campur/asing] [qty]
2. Nasi lemak telur [jenis] sambal [campur/asing] [qty]
3. Nasi lemak berlauk [jenis] [qty]- cash term
```

### Example (22/07/26):
```
LRT Setiawangsa
1. Nasi lemak telur rebus separuh sambal campur 12
2. Nasi lemak telur dadar sambal asing 12
3. Nasi lemak telur mata sambal campur 20
```

### Example (24/07/26) — full multi-location:
```
EVEN
Nasi lemak telur mata sambal campur 10
Nasi lemak telur dadar sambal asing 10
Nasi lemak telur rebus sambal campur 10

MAMAK 2
Nasi lemak telur rebus separuh sambal campur 45

[etc.]
```

### Cash term items (always excluded from standard calc):
- Berlauk paru
- Berlauk dendeng
- Berlauk ayam goreng
- Berlauk sambal sotong

## Baki Adjustment Pattern (CRITICAL)

Syed always adjusts previous orders down if baki (leftover) ada:

```
user: "Telur mata EVEN baki 5"
→ Previous order: 10 mata. Baki 5 = 5 didn't sell. New order: just 5.

user: "Baki 5 setiap satu"
→ All 3 variants for current location: kurangkan quantity setiap satu ikut baki.
```

## Sambal Convention
- **Campur**: sambal mixed into rice
- **Asing**: sambal packed separately
