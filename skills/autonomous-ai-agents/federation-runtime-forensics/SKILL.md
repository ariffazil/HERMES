---
name: federation-runtime-forensics
description: Verify self-reported agent audits and root-cause runtime failures on a multi-agent box (arifOS federation) — cross-check every CRITICAL finding against live probes before acting, trace Telegram delivery floods (Forbidden errors where the bot tries to message itself), discriminate zombie vs active processes, test webhook exposure, and reconcile token ledgers against provider reality. Use when another bot or subagent pastes an audit report, a Telegram bot spams delivery errors, a gateway has duplicate processes, or a model pool is reported dead or exhausted.
---

# Federation Runtime Forensics

When a sibling agent (OpenClaw bot, 777-FORGE, a subagent, or a pasted report) hands you an audit: **it is a self-report, not truth.** Verify every CRITICAL finding against live state before acting (probe-before-act, F2). 2026-08-05 case: a flow audit had 7 findings; 2 were wrong (the zombie was blamed for a flood the ACTIVE gateway caused; the token pool was called dead while the ledger showed $25 — the provider errors were real, the ledger was stale).

## 1. Audit verification discipline

For each finding, ask "what would the live evidence look like?" then probe:

| Finding | Cross-check |
|---|---|
| Zombie process | `ss -tnp \| grep pid=<z>` — idle orphan has ZERO live connections; `ls -la /proc/<pid>/fd/1` closed = orphan |
| Service down | `ss -tlnp` (listener) + `curl :port/health` + `systemctl show <unit> -p MainPID` — a 200 on a "dead" port means the audit mislabeled it |
| Token pool exhausted | `sqlite3 token_bank.db "SELECT provider_name, balance_usd FROM providers"` vs the provider error itself — **provider errors are real; the ledger may lag.** Never declare "not exhausted" from a ledger alone |
| Flood / error storm | Count the exact error string in the unit journal over a window, then count occurrences of the suspected entity (e.g. bot id) — cadence match = connection |
| Duplicate processes | `ss -tlnp` shows who actually LISTENS on the port; session-spawned copies that don't listen are transient, not competitors |

Correct the report in your reply (table: finding → verified → corrected). Report both the audit's claim and your measured value.

## 2. Telegram delivery flood — "Forbidden: the bot can't send messages to the bot"

**The error means the target chat is the bot's OWN user id.** The bot's user id = the numeric prefix of its token (`8410138119:***` → bot id `8410138119`). A repeating flood (~10–30s cadence, hundreds/day, survives restarts) is a **reply-after-block loop**, not a zombie:

```
Blocked unauthorized user <bot-id> in chat <bot-id>
  → adapter blocks the self-update (correct, F12)
  → then tries to REPLY to the blocked chat → Forbidden → retry ×2 → repeat
```

Debug sequence:
```bash
journalctl -u <unit> --since "15 min ago" | grep -c "Forbidden"        # flood rate
journalctl -u <unit> --since "10 min ago" | grep -c "<bot-id-prefix>"  # target = bot itself?
journalctl -u <unit> --since "10 min ago" | grep "Blocked unauthorized" | tail -3
```

What it is / isn't:
- **Is:** updates from the bot's own self-chat (Saved Messages chat = own id). Origin evidence: cron-job `origin.chat_id` in `jobs.json` backups can show that self-chat (e.g. chat_name "ASI") — jobs created from it carry its id in their origin.
- **Not:** the zombie (idle, zero connections), current cron jobs (verify `hermes cron list` + `grep <bot-id> jobs.json` — the CURRENT file may be clean while backups carry the id), or an open webhook (test below).
- **Fix:** a gateway restart clears the in-memory retry loop — confirm `journalctl --since "3 min ago" | grep -c Forbidden` == 0. Durable fix = adapter must NOT send after blocking an unauthorized user (fail-closed; fork carried-commit candidate — F1/F12 doctrine).

Webhook protection test (is the public URL accepting external POSTs as fake updates?):
```bash
curl -s -m 8 -X POST "https://<host>/telegram/webhook" -d '{"test":1}' -o /dev/null -w "%{http_code}"
# 403 = secret enforced; 200 + new "Blocked" log line = public feeder → enforce secret
```

## 3. Restart self-protection

A gateway restart from inside the gateway session is guarded (SIGTERM propagates and kills your own turn). Do restarts from a separate shell / scheduled job, and if the session died mid-turn, trust the system note that the restart ran — don't re-execute it. After any restart, verify by process AGE (`ps -o etime= -p <MainPID>`) and a zero error count over the last 3 minutes.

## 4. Hygiene findings worth reporting

- Multi-GB `~/.hermes/state.db` inflates gateway RAM (SQLite page cache) — checkpoint/vacuum when quiet.
- Permission drift: state files should match siblings (`carry_forward.json` = 640 root:arifos; a 644 db is world-readable — fix to match).
- Webhook/port docs drift: live `ss -tlnp` beats every prose table (ORGAN.md wins only when it matches live health).

## Pitfalls

- `rev-list`-style counts and audit numbers are snapshots — label with date and live-vs-declared.
- Don't kill a "zombie" before checking it isn't another unit's MainPID (2026-08-05: a process mislabeled "orphan" was actually forge-gateway on :8445 — killing it would have taken down 777-FORGE).
- Token ledger balances ($) and provider token-plan quotas are different meters — reconcile, don't equate.
- A 403 on the webhook = protected; do NOT conclude the flood is external. The loop can be fully internal (self-chat updates).
- When a flood "resolves" after a restart, verify the error count is zero over a window before declaring root cause fixed — the feeder may still be posting (now blocked silently).

## Support files

- `references/telegram-self-chat-flood-2026-08-05.md` — full evidence chain: journal excerpts, PID forensics, webhook test, token-ledger reconciliation, the corrected audit table.
