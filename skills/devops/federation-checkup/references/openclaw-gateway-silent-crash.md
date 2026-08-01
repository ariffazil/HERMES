# OpenClaw Gateway Silent Crash — Detection Gap

**Date:** 2026-07-31
**Incident:** Gateway silent crash, ~18h downtime (03:08–21:38 UTC)
**Recovery:** Systemd auto-restart at 21:38 UTC
**Heartbeat:** Sentinel **did not detect** the outage

## Crash Pattern

OpenClaw gateway (Node.js process) can exit silently with **zero error logs** in journalctl.
No `fatal`, no `panic`, no `SIGTERM`, no `exit code`. `journalctl -u openclaw-gateway`
shows only the `systemd[1]: Started` line from the NEXT restart — the previous run's
termination is invisible.

This is distinct from:
- **OOM kill** (kernel logs a `Killed` message)
- **Crash-loop** (systemd restarts rapidly, `journalctl` shows repeated starts)
- **Config error** (process fails to start at all, 127 exit)

## Heartbeat Sentinel Gap

The heartbeat sentinel was checking `:18789` for gateway liveness. Root cause of missed detection:
1. **Port-check only**: Heartbeat only checked if port was listening, not if the listener was actually processing requests
2. **No webhook validation**: No end-to-end test (Telegram → Caddy → Gateway → response)
3. **Silent exit**: Gateway process disappeared without logging, so no alert-triggering event

## Diagnostic Commands

```bash
# 1. Quick liveness — is gateway running?
systemctl is-active openclaw-gateway

# 2. Check port bindings
ss -tlnp | grep -E "18789|8787"

# 3. Check for recent restarts (watch for frequency)
journalctl -u openclaw-gateway -o short --no-pager | grep "Started\|Stopped" | tail -10

# 4. Check Caddy 502 count during suspected downtime window
journalctl -u caddy --since "24 hours ago" --no-pager | grep -c "status\":502"

# 5. Telegram webhook health — check if updates are queuing
source /root/.secrets/kunci-mas.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | \
  python3 -c "import sys,json; d=json.load(sys.stdin)['result']; \
  print(f'pending: {d[\"pending_update_count\"]}, error: {d.get(\"last_error_message\",\"none\")}')"
```

## Prevention

1. **Add end-to-end webhook probe**: Send a test message via bot API, verify gateway receives it
2. **Monitor pending_update_count**: If >100 and growing, webhook is broken regardless of port status
3. **Systemd watchdog**: Add `WatchdogSec=60` to the service unit so systemd restarts on hang
4. **Alert on rapid restart**: If gateway restarted more than once in 30 minutes, escalate

## Related

- `hermes-telegram-group-setup` → Webhook Debugging section for 401 vs 502 distinction
- `hermes-telegram-group-setup` → setWebhook secret_token pitfall
- `federation-checkup` → Dual-probe pattern (liveness + health endpoint)
