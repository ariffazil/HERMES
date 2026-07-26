---
name: trading-analysis-xauusd
description: XAUUSD (Gold) technical analysis — price action, key levels, confirmation entries, risk management. User-validated methodology.
triggers:
  - XAUUSD
  - gold trading
  - forex chart analysis
  - sell signal
  - buy signal
  - take profit
  - MetaTrader chart
---

# XAUUSD Technical Analysis

When the user shares a MetaTrader chart (XAUUSD.m) and asks for analysis or signals, follow this methodology. **User-confirmed approach** (validated 2026-07-14: "ni betul aku pakai camni").

## Analysis Framework

### 1. Identify Key Levels
- **Resistance zones**: Previous highs, consolidation zones, round numbers
- **Support zones**: Previous lows, consolidation floors, psychological levels (e.g., 4000, 3995)
- Mark these with specific price values, not vague ranges

### 2. Read Price Action
- Candlestick patterns at key levels (hammer, shooting star, engulfing)
- Trend direction (higher highs/lows or lower highs/lows)
- Volume confirmation at key levels
- Blue shaded zones on their charts = consolidation/supply-demand areas

### 3. Signal Format (when asked for signals)
```
Direction: BUY/SELL
Entry zone: $X,XXX - $X,XXX (tight range)
Stop loss: $X,XXX (specific level)
TP1: $X,XXX (+$XX)
TP2: $X,XXX (+$XX)
R:R = 1:X.X
Setup: [pattern description]
```

### 4. Confirmation-Based Entries
- **NEVER** call an entry without confirmation candle
- Wait for rejection candle at key level before calling
- If price hasn't confirmed, say "tunggu confirmation" explicitly
- User values patience over speed: "patience is profit"

### 5. Risk Management Labels
- Always calculate R:R ratio
- Tight SL preferred ($20-30 risk on gold)
- Partial close strategy: suggest closing portion at TP1, runner to TP2
- Break-even move suggestion after TP1 hit

### 5a. Half-Close Workflow (validated 2026-07-14)
When user says "nak close half" or position is in decent profit:
1. **Close half** — lock profit on 50% of position
2. **Move SL to breakeven** on remaining — free ride from here
3. **Trail SL** to recent swing high/low if structure allows
4. **Let remainder ride** to TP1/TP2

Example (SELL 0.5 @ 4058, current 4036):
- Close 0.25 lot now → lock ~21 pips
- Remaining 0.25 lot → SL moved to 4058 (breakeven)
- Target: 4029 / 3993
- Risk on remainder: $0 (free ride)

When to suggest half-close:
- Profit > 15-20 pips
- Price approaching known support/resistance zone
- User explicitly asks
- Don't push half-close — it's the user's call

## Common User Positions
- User trades multiple lot sizes (0.2, 0.3, 0.5)
- Uses pending orders (SELL LIMIT, BUY LIMIT)
- Monitors M5, M15, H1, and H4 timeframes
- H4 = macro trend direction, H1/M15 = entry timing
- Sets TP targets based on support/resistance zones
- Runs multiple concurrent positions (e.g., 3x SELL 0.3 at different entries)
- Uses "second entry" pattern — misses first entry, sets pending order at next key level

## Multi-Position Management
When user has multiple open positions:
- Calculate average entry price across all positions
- Single SL level for all positions (usually above resistance)
- Single TP target (usually at major support)
- R:R calculated from average entry to TP
- User prefers tight SL ($15-30 on gold)

## Confirmation Entry Workflow
User's validated pattern (2026-07-14):
1. Identify macro trend (H4)
2. Mark key resistance/support zones
3. Set pending order (SELL LIMIT / BUY LIMIT) at zone
4. Wait for price to reach zone + rejection candle
5. If missed first entry → set "second entry" at next key level
6. "Tunggu confirmation" = user wants to wait, don't push entries

## Output Style
- Direct, no fluff
- Use emoji sparingly (🎯💰📉📈🔥)
- BM casual for commentary, English for price levels
- Always include F2 disclaimer: "ini observation, bukan financial advice"
- Keep analysis to 5-8 lines max — trader wants signal, not essay

## External Resources

See `references/trading-resources.md` for:
- SC Malaysia regulated broker list
- Forex Factory economic calendar guide
- DSIP research context

## Exit Strategy / When to Sell

See `references/exit-strategy-framework.md` for the full framework.

### The One Rule
> Exit when the **reason you entered** is no longer valid. Not when you feel like it.

### Key Signals to Exit
- TP hit → take it, don't chase
- Candle rejection at resistance → exit or partial TP
- Structure break (support/resistance that justified entry) → exit
- Time-based: trade doesn't move in 24-48hrs → reassess

### Emotional Traps to Watch
| Trap | Fix |
|------|-----|
| "Lagi sikit naik" | TP is TP |
| Takut rugi so cut awal | Trust your R:R |
| Revenge trade | Walk away |
| Dah profit tapi tak sell | Greed = killer |

## News Event Framework (validated 2026-07-14)
When high-impact news is scheduled (CPI, NFP, FOMC):
- **Hot result** (inflation high, strong jobs) → USD strength → Gold drops → SELL bias confirmed
- **Cold result** (inflation low, weak jobs) → USD weakness → Gold rallies → BUY bias confirmed
- **In-line** → wait for market to digest, don't trade the initial spike

Decision tree:
1. Is there a high-impact event today? → Flag it
2. Is the user in a position? → Warn about volatility
3. Is the user waiting for entry? → Say "tunggu result dulu"
4. Result released? → Apply hot/cold framework above

## Paper Trading (Agent-Led)

When Arif assigns paper trading with virtual capital, operate as the trader, not an analyst signaling from the sidelines. See `references/paper-trading-workflow.md` for the full cron architecture and ledger format.

### Core Principle: Agentic, Not Passive
- Arif expects the agent to **think and decide**, not wait forever. ("Hang pandai2 LA fikir. Hang agentic intelligence kan" — 2026-07-20)
- Agentic ≠ impulsive. Decision must come from **price action evidence** at the level, not from narrative about seller exhaustion or momentum.
- Default posture: **evaluate evidence and act.** But if the level hasn't been tested yet, WAIT for the test. Mid-air entries are gambling, not trading.

### Paper Trading Rules
- Max risk: 2% per trade
- Max concurrent: 3 positions
- R:R minimum 1:1.5
- Always set SL on entry
- Instruments: XAUUSD, Brent, WTI, Nat Gas
- Ledger: `/root/paper_trading/ledger.md` — update on every trade

### Paper Trading: When NOT to Enter
- **Mid-air entries**: Price consolidating ABOVE a support level ≠ the level has been tested. Entering before the test = guessing. (Example: XAUUSD BUY at $4,012 while $4,000 support untested → SL at $3,985 hit, then price rallied to $4,066. Lesson: tunggu level test dulu.)
- **Narrative entries**: "Seller dah penat," "momentum building," "consolidation = accumulation" are stories, not signals. Price action is the only admissible evidence.
- **Forced entries**: If you have to fabricate 3 sentences to justify why you're entering, you're fabricating. A real entry needs ONE sentence: "Price tested X level with rejection candle."
- **Geopolitical momentum trades**: Oil on Hormuz fears evaporates fast. SL must be tight and IN the chart structure, not based on narrative.

### Paper Trading: Entry Checklist
Before entering ANY paper trade, confirm ALL of these:
1. [ ] Level tested (price actually reached the support/resistance zone)
2. [ ] Confirmation candle (rejection wick, engulfing, or structure break at the level)
3. [ ] SL placed at logical structural level (not arbitrary $-based)
4. [ ] R:R ≥ 1:1.5 from entry to TP
5. [ ] Reason fits in ONE sentence using price action language (not narrative)
6. [ ] NOT entering on impulse to "be agentic" or "not be passive"

If ANY checkbox is empty → TUNGGU. Output: "Setup not confirmed. Waiting for [level] test."

### Zen Silence
- All trading crons must be SILENT unless a trade is executed.
- "No trade" = output "." and stop. No market commentary, no "watching" messages.
- Only notify when: BUY executed, SELL/CLOSE executed, SL at risk warning.

## Pitfalls
- Do NOT give exact entry price if price hasn't reached the zone yet — give the zone
- Do NOT ignore CPI/news events — flag them if relevant
- Do NOT call "BUY" when price is at resistance or "SELL" at support
- Do NOT overcomplicate — user wants clean levels, not 15 indicators
- Do NOT suggest "hold and hope" when structure breaks — exit discipline > hope
- Do NOT push entries before news results — "tunggu result dulu" is the correct posture
- Do NOT default to passive/waiting mode. If evidence supports entry, enter. Paralysis = failure. (2026-07-20)
- Do NOT enter mid-air during consolidation above/below an untested level. "Consolidation = accumulation" is narrative, not confirmation. The level MUST be tested first. See `references/session-2026-07-20-paper-trading-lesson.md` for the $4,012→$3,985→$4,066 case study. (2026-07-21)
- Do NOT fabricate connections between unrelated context. Profile data must never be linked to current situations without explicit user confirmation. "Memandai ja sebut [X]. Macam BANGANG" — Arif, 2026-07-20.
