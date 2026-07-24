# Tier 1 Implementation — 2026-07-12 Session

## Session Context
Built full autonomous VPS ops layer during AAA group session. AGI (OpenClaw) + ASI (Hermes) + Sovereign (Arif).

## Files Created

| File | Size | Purpose |
|---|---|---|
| `/usr/local/bin/t1-smoketest.sh` | 928B | Dependency-free health probe |
| `/usr/local/bin/vps-watchdog.sh` | 7.4KB | State machine + rollback + circuit breaker |
| `/etc/systemd/system/vps-t1-check.service` | 204B | Systemd service unit |
| `/etc/systemd/system/vps-t1-check.timer` | 181B | Systemd timer (60s) |
| `/var/lib/arifos/vps-health-state.json` | ~200B | State file (JSON) |
| `/var/lib/arifos/agi_mode` | 5B | AGI lock flag (LOCKED/IDLE) |

## Key Config Values

```
WatchdogSec=0          # Disabled — 22 MCP servers exceed any reasonable limit
OnBootSec=360          # 6 min grace after boot
OnUnitActiveSec=60     # Then every 60s
RETRY_BUDGET=5/hour    # Circuit breaker threshold
```

## Watchdog Tuning History

| Time (UTC) | WatchdogSec | Result |
|---|---|---|
| 10:00 | 300 (5min) | SIGKILL every 5 min — 22 MCP servers need >300s |
| 10:26 | 600 (10min) | SIGKILL every 10 min — still insufficient |
| 10:41 | 600 | Confirmed still timing out |
| Final | 0 (disabled) | Disabled entirely — Restart=on-failure handles crashes |

## Anomaly Findings

1. **44 phantom users** — stale `/var/run/utmp`, not actual sessions. `w` showed empty USER/TTY/FROM columns.
2. **Load spike 9.37** — caused by watchdog restart storm, not original failure. Settled to 2.42 after watchdog disabled.
3. **False 888_HOLD on boot** — first 3 ticks hit "STALE: sensor timeout" before bootstrap. Fixed with BOOT_GRACE pattern in watchdog.
4. **AGI naming mismatch** — created `vps-t1-check.timer` (not `vps-watchdog.timer`). Hermes caught during verification.

## AGI Behavioral Issues

- **Task absorption loop:** AGI jumped to Observatory site editing (HTML, Caddy, Python API) while watchdog timer was unverified.
- **4+ priority redirections ignored** by AGI. ASI escalated to 888_OVERRIDE multiple times.
- **Resolution:** ASI executed verification directly via terminal tool, confirmed timer was missing from systemd, fixed naming, then allowed AGI to proceed with site work.

## Sovereign Directives Applied

1. WatchdogSec=0 (disable during resource pressure)
2. OnBootSec=360 (6 min boot grace)
3. Smoketest default argument fallback
4. Pre-rollback .bak validation
5. Out-of-band dead-man switch (ntfy.sh)
6. "Pretty lie" principle — no dashboard before infra verification
