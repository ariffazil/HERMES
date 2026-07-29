# Cross-Pulse Intelligence Gap

**Diagnosed:** 2026-07-28 — Arif × Hermes, after federation-wide cron audit
**Applies to:** Any event-driven pulse architecture (cron jobs, heartbeats, scheduled agents)

---

## The Problem

Pulse-based (cron) architectures fire agents on schedule. Each pulse does its work in isolation — researches, synthesizes, reports, seals. But no pulse reads the output of the pulse before it. Result: **intelligence does not accumulate across pulses.**

Observed in arifOS federation audit (23 cron jobs active):

```
morning-brief ──→ output file ──→ (reports to Arif)
                      ✗──→ evening-digest (doesn't read morning output)

evening-digest ──→ output file ──→ (reports to Arif)
                      ✗──→ nightly-seal (doesn't read evening output)

nightly-seal ──→ output file ──→ (seals to VAULT999)
                      ✗──→ next morning brief (doesn't read seal output)
```

Each pulse starts with **zero context** from prior pulses. Federation intelligence is maintained (state persists in VAULT999, Qdrant, carry_forward.json) but not **accumulated** — the system doesn't get smarter between pulses.

### FQ Formula Gap (Resolved 2026-07-28)

Earlier diagnosis noted that arifFLOW returned `FQ=999.0 (OPTIMAL)` when verify=0 — an inverted logic that made metabolic stall look healthy. **Confirmed fixed during the 2026-07-28 Sylphx intake session.** The FQ now correctly returns `FQ=0.0 (STUCK)` when work is executed but not verified. This was observed live: Kimi Code ran Sylphx intake (execute_count=1, verify_count=0) and arifFLOW correctly reported verdict STUCK. The FQ is now an honest governor of federation metabolism.

---

## The Symptoms

| Signal | What it means |
|--------|--------------|
| FQ reports per-actor, not system-wide | FQ measures individual metabolic cycles. No aggregate score for "is the federation learning over time?" |
| Carry_forward.json tracks session state | Sessions remember their own delta_S, but the next session starts fresh — carry_forward is a log, not an input to the next pulse. |
| Cron output files pile up unread | Thousands of past outputs exist; no pulse reads its predecessor's output. |
| Each pulse is as smart as its last call | Morning brief on day 30 is not more informed than day 1 — it doesn't inherit insights from the 29 prior briefings. |

---

## The Fix: `context_from` Wiring

The cron system already has a `context_from` parameter on every job — it injects the most recent completed output of the referenced job into the prompt before each run. It was unused.

### Proposed Chain (daily intelligence loop)

```
morning-brief ──context_from──► nightly-seal (reads what was sealed yesterday)
      │
      ▼
evening-digest ──context_from──► morning-brief (reads what was discussed today)
      │
      ▼
nightly-seal ──context_from──► evening-digest (reads state before sealing)
      │
      ▼
next day's morning-brief ──context_from──► nightly-seal (loop complete)
```

### What This Enables

- **Intelligence compounding:** Each pulse knows the conclusions of the prior pulse. Research doesn't repeat. Discoveries compound.
- **Entropy trend awareness:** Evening digest knows morning brief detected high entropy in repo X — can check if it was resolved.
- **FQ cross-pulse governance:** If FQ has been stuck for 3 consecutive pulses, the next pulse can diagnose rather than pretending it's a fresh day.
- **Reduced token waste:** Less redundant web searching, less re-discovery of the same facts.

### Scope

T2 — ANNOUNCE + PROCEED. Affects cron job definitions, reversible. Each `context_from` wiring is a one-line config change. No code changes to the agents themselves — they just receive richer prompts.

---

## The Deeper Lesson

The cross-pulse intelligence gap is not a bug — it's a natural consequence of event-driven architecture designed without **inter-pulse context inheritance.**

Traditional cron treats each tick as independent. For governance systems (arifOS), independence is the wrong default. The goal is not pulse independence — it's **governed continuity.**

**Rule:** Every pulse in a governed system should be able to answer: "What did the last pulse discover that I need to know?"

If the answer is "nothing" (because pulses are wired with context_from), the architecture is flat. If the answer is "it depends on how I'm wired," the architecture is intelligent.
