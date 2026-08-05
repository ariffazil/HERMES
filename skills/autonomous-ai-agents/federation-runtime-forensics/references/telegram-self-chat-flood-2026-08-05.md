# Telegram Self-Chat Flood — 2026-08-05 Evidence Chain

Incident: ~185 "Forbidden" delivery errors/day on `hermes-asi-gateway` (Hermes @ASI_arifos_bot),
cadence ~10–30s, surviving a gateway restart. A sibling agent's audit blamed the orphan gateway
process; root cause was a reply-after-block loop on the bot's own self-chat.

## The audit's claims vs verified truth

| Finding (audit) | Verified |
|---|---|
| Zombie PID 402154 (orphan, 324MB) causes flood | WRONG — zombie idle: `ss -tnp \| grep pid=402154` → zero Telegram connections; `/proc/402154/fd/1` unreadable (closed). The flood's journal lines carried the ACTIVE gateway's PID |
| Kill zombie + restart fixes flood | Restart happened; flood SURVIVED it (32 Forbidden in next 15 min) → root cause was elsewhere |
| Token pool bailian-token-plan exhausted | Ledger said otherwise — `token_bank.db` providers: bailian-token-plan $25.00, tokenrouter $59.94, mulerouter $49.93, deepseek $12.54, mimo $10.00. Provider errors were real → **ledger stale** |
| MCP ×3 duplicate instances | Partially wrong — only systemd instance (739159) LISTENS on :18086; the other two were transient opencode-session children, not competitors |
| UFW 18087/18088 stale DENY | Confirmed cosmetic (default-deny policy makes them redundant) |
| FED :7074 | Confirmed healthy |

## The smoking gun

```
journalctl -u hermes-asi-gateway | grep "Blocked unauthorized"
  → "Blocked unauthorized user 8410138119 in chat 8410138119"
```

- Bot id discovered: token is `8410138119:***` → **bot user id = numeric token prefix**.
- `journalctl | grep -c "8410138119"` over 10 min = 14 → matched flood cadence exactly.
- The chat 8410138119 = bot's own "Saved Messages" self-chat (chat_name "ASI" in cron-job origins).
- Loop mechanics: adapter blocks the self-update (F12-correct) → then attempts a reply to the
  blocked chat → Telegram 400 `Forbidden: the bot can't send messages to the bot` → retry ×2 →
  repeat ~30s later. Log sequence per cycle:
  `Reply target deleted, retrying without reply_to` → `Forbidden...` → `Send failed (attempt 1/2)` → `attempt 2/2` → `Failed to deliver response after 2 retries`.

## Exclusions tested

- **Cron:** `hermes cron list` showed only 2 benign jobs; current `/root/HERMES/cron/jobs.json`
  had no reference to 8410138119 — but `jobs.json.bak-*` backups (bailian-fix, drift) DID carry
  `origin.chat_id: 8410138119` → jobs were once created from the self-chat; the id lived on in
  backups only.
- **Webhook exposure:** `curl -X POST https://arifos.arif-fazil.com/telegram/webhook -d '{"test":1}'`
  → HTTP 403 → `TELEGRAM_WEBHOOK_SECRET` enforced; not an external feeder.
- **Sibling services:** hermes-mcp / hermes-agent-mcp / hermes-a2a-listener / hermes-real-bridge
  journals all had 0 hits for 8410138119.

## Resolution

- Gateway restarted ~10:20 UTC (MainPID 887453, verified by age `ps -o etime=`); flood stopped
  at 10:20:37 — `grep -c Forbidden --since "3 min ago"` = 0.
- Zombie 402154 GONE after restart.
- Durable fix identified (not yet applied): adapter must not send after blocking an unauthorized
  user — candidate carried commit #3 for the Hermes fork (fail-closed doctrine, F1/F12).

## Commands that worked

```bash
# zombie vs active
ss -tnp | grep -E "pid=(402154|443841)"          # which PID talks to Telegram
ls -la /proc/<pid>/fd/1                          # closed = orphan not logging
systemctl show hermes-asi-gateway -p MainPID --value
ps -o etime= -p <pid>                            # process age vs unit age

# flood measurement
journalctl -u hermes-asi-gateway --since "15 min ago" | grep -c "Forbidden"
journalctl -u hermes-asi-gateway --since "10 min ago" | grep -c "<bot-id-prefix>"

# webhook protection
curl -s -m 8 -X POST "https://<host>/telegram/webhook" -d '{"test":1}' -o /dev/null -w "%{http_code}"

# ledger reality
sqlite3 /root/.local/share/arifos/token_bank.db "SELECT provider_name, track_type, balance_usd FROM providers ORDER BY balance_usd DESC;"
```
