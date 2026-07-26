# Trader Blindspots — Post-APEX 5 Analysis

After gathering APEX 5 context, check for these 5 blindspots before giving advice. Each blindspot maps to a specific consequence and fix.

## The 5 Blindspots

### 1. Confirmation Bias
**Pattern:** "Setup aku betul" — holds thesis even when market narrative changes (news, USD strength, geopolitical)
**Consequence:** Holds losing trades too long, ignores contrary evidence
**Fix:** Check bigger picture (D1, W1) before holding. Ask: "What would prove me wrong?"

### 2. H1 Support Trap
**Pattern:** Trusts H1 support as absolute — "dah 3 kali test, confirm hold"
**Consequence:** One big candle ($30+ in gold) breaks it. Tested support = stronger BREAKDOWN when it fails.
**Fix:** H1 support for exit logic, but always have hard stop loss. Stronger support = bigger crash when broken.

### 3. Comfort with Loss ("Ok je")
**Pattern:** "Sikit je lot, takpe" — treats small losses casually
**Consequence:** Skips risk management. 10 consecutive losses = real money. Death by thousand cuts.
**Fix:** Set max loss per DAY/WEEK, not just per trade. Track cumulative drawdown.

### 4. Single Instrument Tunnel Vision
**Pattern:** Trades XAUUSD only, no hedge, no diversification
**Consequence:** All eggs in one basket. Unexpected $100 crash = total exposure hit.
**Fix:** OK to focus one instrument, but don't put all margin in one trade. Size management.

### 5. No Journal / Selective Memory
**Pattern:** Remembers wins, forgets losses. No systematic tracking.
**Consequence:** Repeats same mistakes. Can't calculate actual win rate or average R:R.
**Fix:** Log every trade — entry reason, exit reason, emotion, outcome. Weekly review.

## Additional Blindspots (Observed)

### 6. Support/Resistance Worship
**Pattern:** Treats S/R levels as absolute barriers
**Consequence:** Doesn't prepare for breakdown/breakout scenarios
**Fix:** For every support level, have a "what if it breaks" plan

### 7. No Macro Awareness
**Pattern:** Pure price action, ignores economic calendar
**Consequence:** News (Fed, NFP, CPI, geopolitical) invalidates setup in minutes
**Fix:** Check economic calendar before entry. High-impact events = reduce size or wait.

### 8. Overconfidence After Win Streak
**Pattern:** Increases lot size after 3-4 wins in a row
**Consequence:** One bad trade wipes out the streak + more
**Fix:** Consistent lot sizing. Increase only after 20+ trade review.

### 9. Revenge Trading
**Pattern:** Enters new trade within 5 minutes of a loss
**Consequence:** Emotional entry, no setup, doubled loss
**Fix:** Mandatory cooldown — minimum 30 minutes after a loss before any new entry.

### 10. Time-of-Day Blind Spot
**Pattern:** Trades at all hours without tracking when they win/lose most
**Consequence:** May consistently lose during low-liquidity sessions
**Fix:** Journal should track entry time. Review: "Do I lose more after 11pm?"

## How to Use This

After APEX 5 answers come in:
1. Cross-check answers against blindspots
2. Flag any that apply (e.g., "ok je" → blindspot #3)
3. Include blindspot warning in analysis
4. Suggest specific fix, not generic advice

**Tone:** Respectful, bro-to-bro. "Abang sado, aku perasan something" — not lecturing.

## Detection Signals (for Emotion Watchdog Agent)

| Pattern | What to watch | Threshold |
|---|---|---|
| Revenge trade | New trade within 5 min of loss | Alert immediately |
| Overconfidence | Lot size increase after win streak | Flag if >50% increase |
| Time bias | Losses concentrated at certain hours | Report in weekly review |
| Weekend gap | Holding positions over weekend | Warn Friday 10pm MYT |
| News chasing | Trade within 30min of high-impact news | Block signal |

## The One Principle

> Trader yang paling bahaya = yang rasa dia dah cukup tahu.

AI's job: be the **mirror**, not the **echo**. Present counterevidence. Don't validate every trade.
