# Watchdog State Machine Implementation

Complete implementation for Tier 1 Active Response. Proven 2026-07-14 on af-forge.

## Components

1. `t1-smoketest.sh` — dependency-free health probe
2. `vps-watchdog.sh` — state machine (IDLE/OBSERVING/HEALTHY/ROLLBACK)
3. `vps-t1-check.{service,timer}` — systemd timer, fires every 60s
4. `/var/lib/arifos/vps-health-state.json` — persistent state file
5. `/var/lib/arifos/agi_mode` — AGI lock flag (IDLE/LOCKED)

## Smoketest (t1-smoketest.sh)

```bash
#!/bin/bash
set -euo pipefail
SVC="${1:-1mcp.service}"
URL="${2:-http://127.0.0.1:3050/health}"
RET=0

if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"; exit 1
fi

if [ -n "$URL" ]; then
  RESPONSE=$(curl -sf --max-time 5 "$URL" 2>/dev/null || echo "")
  if [ -z "$RESPONSE" ]; then
    echo "FAIL: $URL unreachable"; RET=1
  elif ! echo "$RESPONSE" | grep -qi "ok\|healthy\|pass"; then
    echo "FAIL: $URL returned unhealthy content"; RET=1
  fi
fi

if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill"; exit 2
fi

echo "PASS: $SVC"; exit $RET
```

**Key design choices:**
- Default args so it works without arguments
- Content validation (grep for "ok"/"healthy"), not just HTTP 200
- Exit code 2 for watchdog kills (triggers immediate rollback)

## State Machine Logic

State transitions:
- IDLE → OBSERVING: smoketest returns exit 1
- OBSERVING → HEALTHY: smoketest returns exit 0 within 300s
- OBSERVING → ROLLBACK: 3 consecutive fails OR exit 2
- ROLLBACK → IDLE: rollback succeeds + smoketest passes
- ROLLBACK → DEAD: 3 rollback attempts fail → 888_HOLD

## RETRY_BUDGET

Max 5 rollbacks per hour. If exceeded → hard 888_HOLD regardless of state.

## Pre-Rollback Validation

```bash
# Service files
systemd-analyze verify /path/to/file.bak || { echo "INVALID BACKUP"; exit 1; }

# Shell scripts
bash -n /path/to/script.bak || { echo "INVALID BACKUP"; exit 1; }
```

## BOOT_GRACE

```ini
# /etc/systemd/system/vps-t1-check.timer
[Timer]
OnBootSec=360      # 6 min grace (22 MCP servers need >300s)
OnUnitActiveSec=60 # then every 60s
```

Without this, every reboot triggers false 888_HOLD because MCP servers haven't finished booting.

## Pitfalls

- **systemd timer naming.** Use consistent naming. Searching for wrong name → "could not be found".
- **OnBootSec too low.** 30s is not enough for 22 MCP servers. Use 360s minimum.
- **WatchdogSec=0 is temporary.** Only for debugging. Re-enable once resource pressure resolved.
- **State file stale after reboot.** mtime check: if >120s stale, ASI assumes sensor dead → 888_HOLD.
- **AGI mode flag in /run/ (tmpfs).** Lost on reboot. Move to /var/lib/arifos/ for persistence.
