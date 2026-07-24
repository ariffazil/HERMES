# Malaysian Broker Setup for XAUUSD MT5 Trading

> Target: micro-lot XAUUSD trader in Malaysia using MT5.
> Last updated: 2026-07-17

## Quick Comparison

| Broker | Server | Spread XAUUSD | Min Lot | Commission | Regulation | MYR Funding |
|---|---|---|---|---|---|---|
| **IC Markets** | ICMarkets-Live | 10-15 sen | 0.01 | $7/lot RT | ASIC, CySEC | FPX, Local Bank |
| **Exness** | Exness-Real | 15-20 sen | 0.01 | None (Standard) | FSA, FSCA | FPX, Local Bank |
| **Pepperstone** | Pepperstone-Live | 12-18 sen | 0.01 | $7/lot RT | ASIC, FCA | Local Bank |
| **XM** | XMGlobal-Real | 20-25 sen | 0.01 | None (Standard) | CySEC, ASIC | FPX, Local Bank |
| **HF Markets** | HFMarkets-Live | 15-20 sen | 0.01 | None | CySEC, FSCA | Local Bank |

**RT = round turn (open + close)**

## IC Markets (Recommended for API/automation)

- **Best for:** Algo trading, lowest spreads, ECN model
- **Server:** ICMarkets-Live (for live)
- **Min deposit:** $200
- **Leverage:** Up to 1:500
- **API-friendly:** Yes, allows MT5 Python connections
- **Funding:** FPX (instant), local bank transfer, crypto

## Exness

- **Best for:** Beginner, no commission on Standard
- **Server:** Exness-Real (for live)
- **Min deposit:** $10
- **Leverage:** Unlimited (yes, really — but dangerous)
- **API-friendly:** Yes
- **Funding:** FPX, local banks (CIMB, Maybank, etc.)

## Pepperstone

- **Best for:** Low spreads, institutional grade
- **Server:** Pepperstone-Live
- **Min deposit:** $200
- **Leverage:** Up to 1:500
- **API-friendly:** Yes, Razor account recommended for automation

## Warning: Default MT5 Server

When you first download MT5, it auto-connects to:
- **Server:** MetaQuotes-Demo
- **Company:** MetaQuotes Ltd.
- **Status:** "Not a broker, no real trading accounts"

**This is not a trading account.** You must open an account with one of the brokers above, then login with their credentials.

## Setup Flow

1. Open broker account (website) → get account number + password + server
2. Download MT5 desktop terminal (not just mobile)
3. File → Login to Trade Account → enter credentials
4. Verify: View → Navigator → right-click account → Broker Information → should show your broker, NOT MetaQuotes
5. For automation: install Python + MetaTrader5 package on same machine

## Malaysian Deposit Methods

| Method | Speed | Fee | Available On |
|---|---|---|---|
| **FPX** | Instant | Free | Most brokers |
| **Local Bank Transfer** | 1-2 hours | Free | All |
| **Touch n Go eWallet** | Instant | Free | Exness, HF Markets |
| **Crypto (USDT)** | 10-30 min | Network fee | IC Markets, Exness |
| **Credit/Debit Card** | Instant | 1-3% | All |

## For Arif's Setup (Linux VPS)

Since the trading engine runs on Linux (`af-forge`):
1. Open broker account on any broker above
2. Either run MT5 on Wine on af-forge, OR use a Windows machine/VPS
3. The gold-api (`:3456`) is already live — once MT5 connection is established, pipe signals through `arif_judge` → SEAL → `mt5.order_send()`
