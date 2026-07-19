# Tier 1 Implementation — 2026-07-12

## Files Deployed

| File | Size | Purpose |
|---|---|---|
| `/usr/local/bin/t1-smoketest.sh` | 928B | Dependency-free health probe |
| `/usr/local/bin/vps-watchdog.sh` | 7.4KB | State machine + rollback logic |
| `/etc/systemd/system/vps-t1-check.service` | 204B | Systemd oneshot service |
| `/etc/systemd/system/vps-t1-check.timer` | 181B | 60s systemd timer |
| `/usr/local/bin/tier1-serve.py` | 1.3KB | Read-only state API on :8094 |
| `/var/lib/arifos/vps-health-state.json` | ~200B | State file (persistent) |
| `/var/lib/arifos/agi_mode` | ~10B | LOCKED/IDLE flag (persistent) |
| `/var/log/arifos/vps-watchdog.log` | growing | Audit log |

## Caddy Route

```
# /etc/caddy/Caddyfile addition
handle /api/tier1-state {
    reverse_proxy 127.0.0.1:8094
}
```

## Deployment Sequence (Correct Order)

```bash
# 1. Write scripts
# 2. Write systemd units
# 3. Create directories
mkdir -p /var/lib/arifos /var/log/arifos
# 4. Set permissions
chmod +x /usr/local/bin/t1-smoketest.sh /usr/local/bin/vps-watchdog.sh
# 5. CRITICAL: daemon-reload
systemctl daemon-reload
# 6. Enable and start
systemctl enable vps-t1-check.timer
systemctl start vps-t1-check.timer
# 7. Verify
systemctl list-timers vps-t1-check.timer
# 8. Wait one tick (65s), then check state
cat /var/lib/arifos/vps-health-state.json
tail -20 /var/log/arifos/vps-watchdog.log
```

## Issues Encountered

1. **daemon-reload forgotten** — Timer files existed but systemd never registered them. `systemctl status` returned "could not be found". Fixed by running `systemctl daemon-reload`.

2. **False 888_HOLD on first boot** — First 3 ticks (10:44-10:45 UTC) triggered STALE → LOCKED because state file didn't exist yet. Watchdog bootstrapped at 10:46 and settled into clean PASS=1 cycles. Needs BOOT_GRACE period.

3. **Directory creation missing** — Initial watchdog script didn't create `/var/lib/arifos/` before writing state file. Patched to add `mkdir -p`.

4. **AGI priority drift** — AGI got absorbed in site editing (HTML/Caddy) and ignored 5+ priority redirections to verify watchdog first. Required direct terminal intervention by ASI.

## Watchdog Log Output (Healthy)

```
2026-07-12T10:47:38+00:00 [T1] START svc=1mcp.service state=IDLE retry=0 rbk_total=0 rbk_hour=0
2026-07-12T10:47:39+00:00 [T1] TEST_RESULT=0 PASS=1
2026-07-12T10:48:39+00:00 [T1] START svc=1mcp.service state=IDLE retry=0 rbk_total=0 rbk_hour=0
2026-07-12T10:48:39+00:00 [T1] TEST_RESULT=0 PASS=1
```

## State File (Healthy)

```json
{
  "state": "IDLE",
  "last_update": "2026-07-12T10:50:41+00:00",
  "services": {
    "1mcp.service": {
      "retries": 0,
      "rollbacks": 0,
      "last_rollback": 0,
      "hour_rollbacks": 0
    }
  }
}
```

## Observatory Link

https://arifos.arif-fazil.com/ — Tier-1 panel visible in Status tab.
