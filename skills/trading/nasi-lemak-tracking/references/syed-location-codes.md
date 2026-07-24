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
| Kedai P/L/A | Kedai P/L/A | Variants |

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

### Cash term items (always excluded from standard calc):
- Berlauk paru
- Berlauk dendeng
- Berlauk ayam goreng
- Berlauk sambal sotong

## Sambal Convention
- **Campur**: sambal mixed into rice
- **Asing**: sambal packed separately
