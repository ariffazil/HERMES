---
name: autonomous-vps-response
description: "Tier 1 Active Response pattern — autonomous VPS health monitoring with smoketest, state machine, circuit breaker, rollback, and 888_HOLD escalation. Dependency-free shell scripts. Use when building self-healing infrastructure for VPS/servers."
version: 1.0.0
author: Hermes Agent
tags: [vps, monitoring, self-healing, circuit-breaker, rollback, autonomous, tier1]
triggers:
  - "build autonomous monitoring"
  - "self-healing VPS"
  - "circuit breaker for services"
  - "auto-rollback on failure"
  - "tier 1 active response"
  - "dead-man's switch"
---

# Autonomous VPS Response (Tier 1)

Self-healing infrastructure pattern. Zero dependencies. Pure shell. Fires on systemd timer.

## Architecture

```
systemd timer (60s)
  → t1-smoketest.sh (health probe)
    → vps-watchdog.sh (state machine)
      → rollback if hard failure
        → 888_HOLD if rollback fails 3x
```

## Components

### 1. Smoketest (`/usr/local/bin/t1-smoketest.sh`)

Dependency-free health probe. Exit codes: 0=PASS, 1=degraded, 2=critical.

```bash
#!/bin/bash
set -euo pipefail

SVC="${1:-1mcp.service}"
URL="${2:-http://127.0.0.1:3050/health}"
RET=0

# Service active check
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"
  exit 1
fi

# Health URL reachable (if provided)
if [ -n "$URL" ]; then
  if ! curl -sf --max-time 5 "$URL" >/dev/null 2>&1; then
    echo "FAIL: $URL unreachable"
    RET=1
  fi
  # Semantic check — grep for "healthy" in response body
  if ! curl -sf --max-time 5 "$URL" 2>/dev/null | grep -qi "healthy\|ok\|ready"; then
    echo "WARN: $URL returned 200 but no health indicator"
    RET=1
  fi
fi

# No recent watchdog kills
if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill detected for $SVC"
  exit 2
fi

echo "PASS: $SVC"
exit $RET
```

**Key design choices:**
- Default args: works without arguments (fallback to `1mcp.service` + health URL)
- Semantic check: not just HTTP 200, greps for "healthy" in response body (closes Semantic Gap blindspot)
- Watchdog kill detection: catches SIGKILL events from systemd watchdog

### 2. State Machine (`/usr/local/bin/vps-watchdog.sh`)

States: `IDLE → OBSERVING → HEALTHY / ROLLBACK → DEAD`

```bash
# State transitions:
# IDLE + smoketest PASS → HEALTHY (no action)
# IDLE + smoketest FAIL → OBSERVING (start watching)
# OBSERVING + PASS within 300s → HEALTHY (transient, self-healed)
# OBSERVING + 3 consecutive FAILs → ROLLBACK
# ROLLBACK + smoketest PASS → HEALTHY (rollback worked)
# ROLLBACK + smoketest FAIL → retry (max 3)
# 3 failed rollbacks → 888_HOLD (LOCKED mode)
```

**Critical rules:**
- `.bak` validation BEFORE rollback: `bash -n` for scripts, `systemd-analyze verify` for service files
- If `.bak` is invalid → skip rollback → straight to 888_HOLD
- Pre-rollback log snapshot: save journalctl to `/var/lib/arifos/log-snapshot-*.log`
- RETRY_BUDGET: max 5 rollbacks per hour → hard 888_HOLD (prevents infinite restart loops)

### 3. Systemd Timer

```ini
# /etc/systemd/system/vps-t1-check.timer
[Unit]
Description=VPS Tier-1 Health Check Timer (every 60s)
Requires=vps-t1-check.service

[Timer]
OnBootSec=360        # BOOT_GRACE: 6 min after boot before first check
OnUnitActiveSec=60   # Then every 60s
AccuracySec=1s

[Install]
WantedBy=timers.target
```

**BOOT_GRACE (critical):** On boot, services need time to start. Set `OnBootSec=360` (6 min) to avoid false 888_HOLD triggers. Without this, the watchdog fires before services finish booting → false alarms → LOCKED mode on every reboot.

### 4. AGI Mode Flag

Persist in `/var/lib/arifos/agi_mode` (NOT `/run/arifos/` which is tmpfs and lost on reboot).

- `IDLE` = normal operation
- `LOCKED` = 888_HOLD, AGI must not execute any mutations

### 5. Dead-Man's Switch (OOB Alert)

Heartbeat cron that reports VPS health. If it stops firing, the VPS is down.

```bash
#!/bin/bash
# /usr/local/bin/deadman-heartbeat.sh
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | awk '{print $1}')
DISK=$(df / | awk 'NR==2 {print 5}')
RAM=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
echo "🫀 heartbeat: up=$UPTIME load=$LOAD disk=$DISK ram=$RAM"
```

Deploy as cron job. If delivery stops → VPS is dead → alert via out-of-band channel (Telegram, email).

## Pitfalls

- **Don't use `/run/` for state files.** It's tmpfs — lost on reboot. Use `/var/lib/arifos/`.
- **Don't skip `.bak` validation.** If backup is corrupted, rollback restores broken state → infinite loop.
- **Don't set WatchdogSec too low.** For multi-service setups (22+ MCP servers), 300s is not enough. Start with 900s or disable watchdog entirely if Restart=on-failure is configured.
- **Don't trust HTTP 200 alone.** Service can return 200 with garbage data. Semantic check (grep response body) closes this gap.
- **Don't let AGI build UI before verifying infra.** "Dashboard on dead timer = pretty lie." Always verify infrastructure layer (systemctl status, state files, logs) BEFORE touching presentation/UI.
- **Circuit breaker prevents cascading restarts.** Without RETRY_BUDGET, a buggy rollback config creates infinite restart-write loop → disk death spiral.

## Verification

```bash
# Check timer is running
systemctl status vps-t1-check.timer

# Check state file
cat /var/lib/arifos/vps-health-state.json

# Check AGI mode
cat /var/lib/arifos/agi_mode

# Manual smoketest
bash /usr/local/bin/t1-smoketest.sh

# Watchdog log
tail -20 /var/log/arifos/vps-watchdog.log
```

## References

- `references/headscale-installation.md` — Headscale v0.29.2 setup for self-hosted Tailscale coordination
- `references/tailscale-acl-policy.md` — Tag-based ACLs for federated agent networks
