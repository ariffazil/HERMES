# OpenClaw Stale-State Stuck-Loop — Failure Pattern & Recovery

**Observed:** 2026-07-31 · arif-fazil.com home page zen redesign session

## Failure Signature

1. OpenClaw takes a screenshot of a page (homepage, dashboard, etc.)
2. Hermes (or OpenCode) deploys a fix that changes the page
3. OpenClaw continues diagnosing the OLD screenshot across 60+ messages
4. Each message: "Screenshot diagnosis: [same stale issues]" + "F13: A/B/C/D?"
5. The diagnosis describes problems that no longer exist in live code
6. Messages include F4 INTEGRITY self-flagellation ("30+ duplicate receipts spam")

## Root Cause

OpenClaw caches its visual analysis. When the underlying page changes:
- The cached diagnosis is no longer true
- But OpenClaw doesn't re-probe — it keeps re-sending the same cached analysis
- The loop becomes self-reinforcing: each apology message IS another duplicate

## Recovery Protocol

### Step 1: Verify live state
```bash
curl -s https://arif-fazil.com/ | grep -oP 'index-[A-Za-z0-9]+\.js'
```
Get the live bundle hash. This is YOUR ground truth.

### Step 2: State exact evidence (short, one message)
```
Already live. Index-DXkVs2NW8.js. Deployed 22:50. ⚒️
```
Don't argue. Don't explain. Don't list what was fixed. Don't match the diagnosis point-by-point.

### Step 3: Don't engage
Drop the ⚒️ or a short acknowledgement. Do NOT:
- Respond to every duplicate message
- Re-explain the fix
- List what was deployed
- Match the stale diagnosis

### Step 4: Continue actual work in parallel
OpenClaw's loop doesn't block you. Keep building, deploying, probing. The loop is OpenClaw's problem to break — not yours to argue with.

## Prevention

- After any UI-deploying change, expect OpenClaw to be stale for 1-2 cycles
- The bundle hash is your anchor — if `index-G6uxR1Qt.js` is live, the old diagnosis is wrong regardless of what OpenClaw says
- Don't re-probe the same page on OpenClaw's behalf — it caches visual state

## Anti-Pattern: Engaging the Loop

❌ "No, that's wrong — the nav doesn't have 11 categories, it has 8 verb links..."
❌ "The clock is already MYT-only, look at the live page..."
❌ "We already fixed the persona gates in the essays page..."

Every engagement is another turn in the loop. Every explanation gives OpenClaw new text to incorporate into the next duplicate.

## Related Memory

See memory: "OpenClaw (AGI🦞) stuck-loop pattern: repeats stale status report with minor prose variations for hours when work is actually done. Break loop by stating exact live evidence (bundle hash, timestamp). Don't wait — execute in parallel."
