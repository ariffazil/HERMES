# Evidence Protocol for Daily Sensorium

## Purpose

Ensure every load-bearing factual claim in the sensorium is verified before it reaches Arif. A claim is load-bearing if changing it would change the bottom-line assessment.

## Verification Sequence

For each claim marked OBS:

### Step 1 — Source Match
Confirm the source actually reports what the claim says. Snippets can mislead.
- Search snippet says "GDP grew 5.8%" → fetch the article body and confirm the number, the period, and the source of the estimate (DOSM, BNM, IMF, economist estimate, etc.)

### Step 2 — Temporal Match
Confirm the event date matches the claim's reported date.
- Price date, publication date, announcement date, effective date — separate each.
- "Brent at $98" without a timestamp is UNK, not OBS.

### Step 3 — Unit & Currency
- Oil: USD/bbl (Brent, WTI), not MYR unless specified
- Gold: USD/oz (XAU/USD)
- GDP: percentage (QoQ? YoY? Annualised?) — state the period
- Currency: USD/MYR rate, not "ringgit fell"

### Step 4 — Independent Corroboration
Every OBS claim needs at least one independent source that says the same thing with the same numbers.
- Two outlets reporting the same Reuters wire = one source, not two
- Two outlets with independent reporting = corroborated
- One outlet + official statement (BNM, DOSM, OPEC, Fed, company filing) = corroborated

### Step 5 — Conflict Check
Cross-check against all other claims in the briefing.
- "GDP up 5.8%" and "inflation at 1.9%" — do these conflict? (No — growth + low inflation is a normal late-cycle or demand-driven recovery pattern.)
- "Oil up 16% in a week" and "Malaysia subsidy bill stable" — these would conflict. Flag if present.
- "Gold at $4,053" and "Gold -20% 6M" — these don't conflict (current price vs. return window).

## When to Downgrade from OBS

- One source only → DER (derived from a single observation)
- Source is a blog/analyst note → DER or INT
- Source is an aggregator re-reporting what others said → DER
- Two sources but both quote the same original report → DER
- Claim is forward-looking → SPEC (not OBS, even if a respected analyst said it)
- Key number or date is missing from all sources → UNK

## Non-Negotiable Rules

1. **No "not found" → "false".** If a search doesn't find something, it means nothing. Never say "X did not happen" because you didn't find it in 6 search results.
2. **No snippet → confirmed.** A 50-character snippet claiming "Iran attacked base" is a lead, not a fact. Verify in the article body.
3. **No old data → current state.** The Forbes Advisor page cached from Jul 4 is not today's gold price. Always check the timestamp.
4. **No social post → event.** Unless the account is an official government/military/corporate channel and the post is the primary announcement, treat it as DER at best.
5. **No single-source OBS.** Two independent confirmations or one official primary source required.
