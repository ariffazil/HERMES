---
name: vps-self-healing
description: "Build autonomous self-healing infrastructure for VPS — smoketest, state machine, circuit breaker, .bak validation, dead-man's switch. Tier 1 Active Response pattern proven 2026-07-12 on af-forge."
version: 1.0.0
author: Hermes Agent
tags: [vps, self-healing, autonomous, watchdog, circuit-breaker, infrastructure]
triggers:
  - "build self-healing"
  - "autonomous response"
  - "vps watchdog"
  - "circuit breaker"
  - "smoketest"
  - "rollback automation"
  - "dead-man's switch"
  - "Tier 1 active response"
---

# VPS Self-Healing Infrastructure

Autonomous response layer for VPS — the system detects failures, attempts recovery, and escalates to humans only when automation can't fix it.

## When to Use
- VPS running critical services that need 24/7 uptime
- Multi-agent federation where agents manage each other's VPS
- When you want the machine to self-heal without waking the human

## When NOT to Use
- Single-service VPS with simple restart-on-failure (use systemd `Restart=on-failure`)
- Development/staging environments where downtime is acceptable
- When the human wants manual control over all changes

## Architecture: 4 Layers

### Layer 1: Smoketest (The Sensor)
Pure shell, zero dependencies, <3s execution. Checks service health + VPS vitals.

**Design rules:**
- Exit codes: 0=PASS, 1=DEGRADED, 2=CRITICAL
- Check service active state + HTTP health endpoint + response content (not just HTTP 200)
- Check VPS vitals: RAM >85%, Disk >90%, Load >2x CPU cores
- Default arguments so it works without parameters
- Always validate response CONTENT (grep for "healthy"/"ok"), not just status code

**Pitfall:** HTTP 200 ≠ healthy. Service can return 200 while serving garbage data. Always grep response body for expected string. (Blindspot #3 from Gemini audit, proven 2026-07-12.)

**Pitfall:** Smoketest that requires arguments will fail when called from cron/timer without args. Always set defaults: `SVC="${1:-1mcp.service}"`.

### Layer 2: State Machine (The Brain)
4 states: IDLE → OBSERVING → HEALTHY/ROLLBACK → DEAD

**Transient vs Hard failure detection:**
- Transient: 1-2 FAILs that self-resolve within 300s → log and continue
- Hard: 3 consecutive FAILs OR exit 2 (CRITICAL) OR no recovery in 300s → trigger rollback
- Circuit breaker: 5 rollbacks per hour → hard 888_HOLD

**State file:** `/var/lib/arifos/vps-health-state.json` (persistent, survives reboot)

**AGI mode flag:** `/var/lib/arifos/agi_mode` (LOCKED/IDLE)
- LOCKED = AGI cannot execute write operations
- IDLE = normal operation
- Default to LOCKED on boot until first smoketest passes

**Pitfall:** State file in `/run/` (tmpfs) = lost on reboot. Always use `/var/lib/arifos/` for persistent state. (Gemini blindspot #4, proven 2026-07-12.)

### Layer 3: Rollback (The Immune System)
**Pre-rollback validation (MANDATORY):**
- Service files: `systemd-analyze verify file.bak` — if exit code ≠ 0, skip rollback → 888_HOLD
- Shell scripts: `bash -n script.bak` — syntax check before restore
- If .bak is invalid, don't rollback. Go straight to 888_HOLD.

**Pitfall:** Rolling back to a corrupted .bak creates a restart-rollback-restart death spiral. Always validate .bak before restoring. (Arif's integrity guard, 2026-07-12.)

**Rollback sequence:**
1. Pre-rollback log snapshot (save current logs for post-mortem)
2. Validate .bak file
3. If valid: `cp file.bak file && systemctl daemon-reload && systemctl restart service`
4. Wait 60s, run smoketest
5. If still FAIL: increment retry counter, try again (max 3)
6. If 3 failures: 888_HOLD

### Layer 4: Dead-Man's Switch (The Failsafe)
If the VPS can't send heartbeats, the human needs to know.

**Simple approach:** Cron job that sends heartbeat to Telegram every 30 minutes. If it stops firing → human notices the silence.

**Better approach:** External monitoring service (ntfy.sh, UptimeRobot) that expects heartbeats and alerts when they stop.

**Pitfall:** ntfy.sh's `X-Min-Schedule` header is NOT a true dead-man's switch. It's scheduled delivery, not outage detection. Use a real monitoring service or the Telegram heartbeat pattern.

## Implementation Checklist

```bash
# 1. Create smoketest
cat > /usr/local/bin/t1-smoketest.sh << 'EOF'
#!/bin/bash
set -euo pipefail
SVC="${1:-1mcp.service}"
URL="${2:-http://127.0.0.1:3050/health}"
RET=0
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"; exit 1
fi
if [ -n "$URL" ]; then
  BODY=$(curl -sf --max-time 5 "$URL" 2>/dev/null || echo "FAIL")
  if ! echo "$BODY" | grep -qi "healthy\|ok\|pass"; then
    echo "FAIL: $URL response not healthy"; RET=1
  fi
fi
if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill"; exit 2
fi
[ "$RET" -eq 0 ] && echo "PASS: $SVC"
exit $RET
EOF
chmod +x /usr/local/bin/t1-smoketest.sh

# 2. Create state directory
mkdir -p /var/lib/arifos /var/log/arifos

# 3. Create systemd timer
cat > /etc/systemd/system/vps-t1-check.service << 'EOF'
[Unit]
Description=VPS Tier-1 Health Check
After=network.target
[Service]
Type=oneshot
ExecStart=/usr/local/bin/vps-watchdog.sh
StandardOutput=journal
StandardError=journal
SyslogIdentifier=vps-t1-check
EOF

cat > /etc/systemd/system/vps-t1-check.timer << 'EOF'
[Unit]
Description=VPS Tier-1 Health Check Timer (every 60s)
Requires=vps-t1-check.service
[Timer]
OnBootSec=360
OnUnitActiveSec=60
AccuracySec=1s
[Install]
WantedBy=timers.target
EOF

# 4. Enable
systemctl daemon-reload
systemctl enable --now vps-t1-check.timer
```

## Pitfalls (All Proven 2026-07-12)

1. **BOOT_GRACE period** — On first boot, MCP servers need >300s to start. Set `OnBootSec=360` to avoid false 888_HOLD on reboot.
2. **AGI tunnel vision** — Agents will build dashboards before verifying the timer works. Always verify infra before UI. "Dashboard on dead timer = pretty lie."
3. **Naming inconsistency** — Timer named `vps-t1-check.timer` but agent looks for `vps-watchdog.timer`. Use consistent naming or check both.
4. **888_OVERRIDE ignored** — If AGI ignores priority redirections 4+ times, it's in a loop. Take over verification directly via terminal.
5. **Resource starvation** — Watchdog restart storms drain RAM → swap thrashing → more failures. Disable watchdog (WatchdogSec=0) during crisis, re-enable after stabilization.
6. **Ghost sessions** — Stale utmp entries show phantom "users logged in." Clean with `> /var/run/utmp`.
7. **Smoketest argument requirement** — If smoketest requires `<service>` arg but timer calls it without, EXIT_CODE=1 on every tick. Always set defaults.

## Monitoring the Monitor

The watchdog itself needs monitoring:
- State file mtime >120s = sensor dead → 888_HOLD
- Circuit breaker (RETRY_BUDGET=5/hour) prevents infinite restart loops
- Pre-rollback log snapshots enable post-mortem analysis
- Dead-man's switch ensures human is notified if system goes silent

## References
- `scripts/vps-watchdog.sh` — Full state machine implementation (6.7KB)
- `scripts/t1-smoketest.sh` — Dependency-free smoketest
- `references/tier1-session-log.md` — Full session log from 2026-07-12 build
