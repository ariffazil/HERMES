# Overnight Cron — Output Pattern

The `overnight-research` cron job (separate from the 7:30 MYT morning Telegram brief) writes a structured markdown file to disk. The intent is **quiet, complete state capture** — the operator reads it on their own schedule, not via push notification.

## File path
`/root/memory/overnight-$(date +%Y-%m-%d).md`

This is **distinct** from the daily session log at `/root/memory/YYYY-MM-DD.md` (which captures in-session activity). The overnight file is a synthesized health/state snapshot, not a session log.

## Required sections (in order)
1. Header line: cron name, sovereign, verdict (LOG_ONLY or ESCALATE), time window
2. **System Health** — table: organ | port | status | notes. Include `runtime_drift`/`surface_consistency` for arifOS, NOT just ✅/❌
3. **VAULT999 Seals** — table of seals in window. Include seq, time, actor, verdict, domain, one-line note
4. **Git Activity** — table: repo | commits | highlights. Lookback 24h
5. **Memory / Insights** — pull from `/root/memory/YYYY-MM-DD.md` and any opencode/grok session seals from the same day
6. **Pending Tasks (Tomorrow)** — short checklist, prioritized A/B/C/D
7. **CRITICAL FINDING — Telegram Trigger?** — explicit decision: which findings are real, which are false alarms, **and the final critical-yes/no verdict**. This is the gate.
8. **Operator Status (WELL)** — well_readiness TTL and staleness warning

## Critical-finding decision (the gate)

A finding is CRITICAL only if it requires Arif's attention **tonight, before the 7:30 morning brief**. Examples:
- ✅ Data loss risk (database corruption, disk full, chain break)
- ✅ Organ down and recovery failed (auto-restart didn't work)
- ✅ Urgent decision needed (security event, deadline in <12h)
- ❌ YELLOW status with no immediate impact (handle in morning brief)
- ❌ "Container needs rebuild" (non-urgent, handle in morning)
- ❌ Cron logging errors to dead scripts (housekeeping)
- ❌ Image behind code (known state, not emergency)
- ❌ HTTP 000000 on a non-HTTP bot (false alarm)

## Delivery rule (overnight variant)
- If CRITICAL = YES: send ONLY the critical finding to Arif's Telegram (DM via AGI🦞 bot), then log the full brief to disk
- If CRITICAL = NO: log the full brief to disk, **do not** send anything to Telegram. Silent completion is correct.

## Why this gate exists
Telegram is a finite attention surface. Overnight alerts that turn out to be false alarms train Arif to mute the channel — and then a real CRITICAL gets missed. The default has to be quiet. The bar for "wake him up" has to be high.

## Reference template
See `/root/memory/overnight-2026-07-07.md` for a real example output.
