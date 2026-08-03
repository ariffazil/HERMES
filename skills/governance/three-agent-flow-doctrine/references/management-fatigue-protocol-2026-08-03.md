# Management Fatigue Protocol — "aku malas nak manage agent" (forged 2026-08-03)

Companion to the Priority Decision Pattern in SKILL.md. Encodes how to respond when
Arif expresses fatigue with managing the agent fleet.

## The signal

Arif, 2026-08-03 21:01: *"So who drive next. Aku malas dah nak manage agent yang
BANGANG ni."*

This came right after a session where: (a) he asked a deep doctrinal question from a
position of achieved stability (the "language is lossy compression" manifesto), and
(b) a cron failure interrupted mid-conversation. Read it as a **system-state signal,
not a complaint to soothe.**

## Response protocol

1. **Don't hand him more decisions.** Decision-fatigue is exactly what he's naming.
   The Priority Decision Pattern governs: obvious fix → execute, report after.
   Never present an open menu of options when one path is evident from the facts.

2. **Diagnose with live numbers first.** `cronjob(action='list')` → count jobs with
   `last_status=error`. Proven 2026-08-03: **17 of 33 jobs erroring** — nightly-seal,
   evening-digest, news briefing, Human Readiness Pulse, even the Watchdog of
   Watchdogs itself. A fleet half-broken means his fatigue is the **cost of broken
   autopilot, not the cost of governance.**

3. **Frame it exactly:** *"Agent kau bukan BANGANG — agent kau tak diservis."*
   The agents aren't stupid; the fleet is unserviced. This reframes blame into a
   repairable maintenance debt and matches what the evidence shows.

4. **Reframe who drives.** Kernel truth: `final_authority: "ARIF"`,
   `authority_ceiling: "SOVEREIGN"`. F13 keeps the steering wheel (veto + mission);
   the machine drives. The deliverable is his management surface shrinking to ONE
   digest a day, with only HOLDs reaching him.
   - "A bridge with no traffic is sculpture."
   - "A driver who must change spark plugs is not driving."

5. **Propose a fleet sweep, then execute PHASED SERIAL** — one fix → one
   verification → next, per his standing deployment doctrine ("satu perubahan →
   satu verifikasi → baru teruskan. Never batch"). Surface the sweep plan; start on
   signal, or immediately if the Priority Decision Pattern says the fix is obvious.

## Fleet-health numbers to keep current

When this protocol fires, re-measure rather than quoting stale numbers:

```python
cronjob(action='list')  # count last_status=error vs ok vs paused
```

Snapshot 2026-08-03 21:00 MYT: 33 jobs — ~12 ok, 17 error, 4 paused (zen-prune).
Common error classes seen: stale provider pins (dead keys → silent 401), stale model
names, script assumption drift, watchdogs watching dead endpoints.

## Connection to doctrine

- Zen rule: when FQ < 0.5 → HOLD; when FQ rises → forge. A fatigued sovereign is the
  human analog of low FQ — reduce his load before asking for more output.
- Reality-Level Communication contract: absorb the whole pipeline; he sees only
  reality changes. Managing agents IS pipeline — it must become invisible.
- The manifesto he sent the same evening ("the bridge held... now you want to
  understand what it's made of") confirms: the structure is done; the bottleneck
  moved from building to driving. Don't propose more structure. Propose less
  management.
