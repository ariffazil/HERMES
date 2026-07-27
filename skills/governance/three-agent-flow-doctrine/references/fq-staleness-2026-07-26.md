# FQ Staleness Episode — 2026-07-26

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 2026-07-25T08:49:00Z | OpenClaw last wrote flow_state.json — FQ=1.0, receipt_count=4,704 |
| 2026-07-25 → 26 | 29-hour gap — no updates. system running blind on stale FQ |
| 2026-07-26T14:06:37Z | Hermes probe: flow_state.json discovered stale. arifFLOW live: 17,267 receipts |
| 2026-07-26T14:07:00Z | FQ computed live: (17,267+1)/(1,099+1) = **15.7 OPTIMAL** |
| 2026-07-26T14:09:00Z | flow_state.json rewritten with live data, cron installed |

## Root Cause

**OpenClaw session died.** The flow doctrine declared OpenClaw should write FQ each cycle, but:
1. OpenClaw only writes during active sessions — no session = no write
2. No heartbeat check on flow_state.json freshness
3. Single point of failure: OpenClaw was the ONLY sensor

## What Broke

| Claim | Reality | Gap |
|-------|---------|-----|
| FQ = 1.0 (BALANCED) | FQ = 15.7 (OPTIMAL) | 15× underestimate |
| receipt_count = 4,704 | receipt_count = 17,267 | 4× gap |
| Data fresh | 29 hours stale | No staleness detection |

**Formula bug also found:** OpenClaw was reading VAULT999 receipt_count (4,704) instead of arifFLOW `/health` → `receipt_chain.count` (17,267). Two different sources, different counts. The doctrine has been corrected to always source from arifFLOW.

## Fix Applied

| Fix | Type | Detail |
|-----|------|--------|
| cron fq-probe.sh | T2 | Every 15 min, reads arifFLOW live, writes flow_state.json |
| flow_state.json rewrite | T1 | Live data written immediately |
| Formula source documented | Patch | SKILL.md: arifFLOW health, not VAULT999 |
| Staleness detection rule | Patch | Check age first; >1h stale → fallback to direct probe |

## Lesson

Single-sensor architectures in governance are not Zen. FQ is a nadi — it needs a backup pacemaker. The cron is the pacemaker. Rust arifFlow (with built-in FQ) will be the permanent fix.
