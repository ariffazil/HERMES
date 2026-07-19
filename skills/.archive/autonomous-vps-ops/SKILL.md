---
name: autonomous-vps-ops
description: Build self-healing VPS infrastructure — smoketest, state machine, systemd timers, auto-rollback, circuit breakers, dead-man's switches. Dependency-free shell scripts. For single-VPS autonomous ops under arifOS F1-F13 governance.
triggers:
  - "self-healing infrastructure"
  - "autonomous VPS monitoring"
  - "auto-rollback"
  - "systemd timer watchdog"
  - "circuit breaker for services"
  - "dead-man's switch"
  - "Tier 1 active response"
---

# Autonomous VPS Ops — Tier 1 Active Response

Build a closed-loop control system for a single VPS that detects failures, attempts auto-rollback, and escalates to human (888_HOLD) when automation can't recover.

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Smoketest   │────→│ State Machine │────→│  Action Layer│
│  (shell, <3s)│     │ (IDLE/OBSERVE │     │  (rollback/  │
│              │     │  /HEALTHY/    │     │   888_HOLD)  │
│              │     │  ROLLBACK)    │     │              │
└─────────────┘     └──────────────┘     └─────────────┘
       ↑                   │                     │
       │                   ▼                     ▼
  systemd timer      State File            AGI Mode Flag
  (every 60s)     (/var/lib/arifos/)    (LOCKED/UNLOCKED)
```

## Step 1: Smoketest Script

**Rule: Zero dependencies.** Pure shell. Must work when system is degraded (low RAM, broken Python, etc).

```bash
#!/bin/bash
# /usr/local/bin/t1-smoketest.sh
# Exit codes: 0=healthy, 1=degraded, 2=critical

ENDPOINTS=(
  "localhost:8088"   # arifOS
  "localhost:7071"   # A-FORGE
  "localhost:3001"   # AAA
)

FAIL=0
for ep in "${ENDPOINTS[@]}"; do
  # Content check: grep for "ok" or "healthy" in response body
  BODY=$(curl -sf --max-time 5 "http://$ep/health" 2>/dev/null)
  if [ $? -ne 0 ] || ! echo "$BODY" | grep -qiE '"(ok|healthy|status)"'; then
    echo "FAIL: $ep"
    ((FAIL++))
  fi
done

# VPS vitals
RAM_PCT=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
DISK_PCT=$(df / | awk 'NR==2 {gsub(/%/,""); print $5}')
LOAD_RATIO=$(awk "BEGIN {printf(\"%.1f\", $(cat /proc/loadavg | awk '{print $1}')/$(nproc))}")

[ "$RAM_PCT" -gt 85 ] && echo "WARN: RAM ${RAM_PCT}%" && ((FAIL++))
[ "$DISK_PCT" -gt 90 ] && echo "WARN: Disk ${DISK_PCT}%" && ((FAIL++))
awk "BEGIN {exit !($LOAD_RATIO > 2.0)}" && echo "WARN: Load ${LOAD_RATIO}x" && ((FAIL++))

[ "$FAIL" -eq 0 ] && exit 0
[ "$FAIL" -le 2 ] && exit 1
exit 2
```

**Key design choices:**
- `curl -sf` + `grep` for content validation (not just HTTP 200 — catches garbage data)
- Exit codes are discrete (no superposition — this is silica)
- Script itself is monitorable: if it can't run, system is dead → escalation automatic

## Step 2: Systemd Timer

```ini
# /etc/systemd/system/vps-t1-check.timer
[Unit]
Description=VPS Tier-1 Health Check Timer (every 60s)
Requires=vps-t1-check.service

[Timer]
OnBootSec=30
OnUnitActiveSec=60
AccuracySec=1s

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/vps-t1-check.service
[Unit]
Description=VPS Tier-1 Health Check

[Service]
Type=oneshot
ExecStart=/usr/local/bin/vps-watchdog.sh
```

## Step 3: Watchdog State Machine

The watchdog script runs the smoketest, manages state, triggers rollback or escalation.

**States:**
- `IDLE` — no active issues
- `OBSERVING` — transient failure detected, monitoring for recovery (300s window)
- `HEALTHY` — system recovered within window
- `ROLLBACK` — hard failure, auto-rollback triggered

**Decision logic:**

| Signal | Classification | Action |
|---|---|---|
| Exit 1, recovers within 300s | Transient | Log + continue |
| Exit 1, 3 consecutive checks | Hard | Trigger rollback |
| Exit 2 (any check) | Hard | Immediate rollback |
| Exit 2 after rollback | Critical | 888_HOLD + LOCK AGI |

## Step 4: Rollback with Pre-Validation

**NEVER rollback blindly.** Validate `.bak` before restoring:

```bash
# For systemd service files
systemd-analyze verify /etc/systemd/system/foo.service.bak
if [ $? -ne 0 ]; then
  echo "BAK INVALID → 888_HOLD"
  # Skip rollback, escalate immediately
fi

# For shell scripts
bash -n /usr/local/bin/foo.sh.bak
if [ $? -ne 0 ]; then
  echo "BAK INVALID → 888_HOLD"
fi
```

**Pre-rollback log snapshot:** Save current logs before rollback for post-mortem:
```bash
cp /var/log/arifos/vps-watchdog.log /var/lib/arifos/log-snapshot-$(date +%s).log
```

## Step 5: Circuit Breaker (RETRY_BUDGET)

**Max 5 rollbacks per hour.** After that → hard 888_HOLD, even if smoketest returns HEALTHY.

This prevents:
- Cascading restart loops from buggy rollback config
- Disk write-cycle exhaustion
- Log storm filling /var/log

```bash
HOUR_ROLLBACKS=$(grep -c "ROLLBACK" /var/log/arifos/vps-watchdog.log | tail -3600)
if [ "$HOUR_ROLLBACKS" -ge 5 ]; then
  echo "CIRCUIT BREAKER → 888_HOLD"
  # Lock AGI, notify sovereign
fi
```

## Step 6: AGI Mode Flag (Kill Switch)

**Flag-based, not process-kill.** Preserves F11 audit trail.

```bash
# /var/lib/arifos/agi_mode
# Values: IDLE, LOCKED
# Default after reboot: LOCKED (safe default until smoketest confirms HEALTHY)
```

**Why `/var/lib/arifos/` not `/run/arifos/`:**
- `/run` is tmpfs → lost on reboot
- `/var/lib` persists → AGI boots into LOCKED until watchdog confirms healthy
- Safe default: automation is locked until proven safe

## Step 7: Dead-Man's Switch (OOB Alert)

If the VPS itself dies (kernel panic, power loss), no internal script can alert. Use an external heartbeat:

```bash
# Cron job (system level, not application level)
*/5 * * * * curl -sf -d "VPS alive: $(date)" ntfy.sh/arifos-heartbeat >/dev/null
```

**External service (ntfy.sh):** If heartbeat stops for 300s → push notification to phone. Out-of-band, independent of VPS stack.

---

## Pitfalls (MUST READ)

### PITFALL: daemon-reload not run after writing timer/service files
**Symptom:** `systemctl status vps-t1-check.timer` → "Unit could not be found"
**Cause:** Wrote .timer/.service files but forgot `systemctl daemon-reload`
**Fix:** Always run this sequence:
```bash
systemctl daemon-reload
systemctl enable <timer-name>.timer
systemctl start <timer-name>.timer
systemctl list-timers <timer-name>.timer  # verify it's scheduled
```
**Verification:** `systemctl list-timers` must show the timer with a NEXT column value.

### PITFALL: False 888_HOLD on first boot
**Symptom:** First 2-3 ticks trigger "STALE: sensor timeout → 888_HOLD" because smoketest/state file not ready
**Cause:** Watchdog expects existing state file, but first run has nothing to compare against
**Fix:** Add `BOOT_GRACE` — first 2-3 ticks should skip 888_HOLD, just log + bootstrap:
```bash
if [ ! -f "$STATE_FILE" ]; then
  echo "BOOT: first run — bootstrapping state"
  # Don't escalate, just initialize
fi
```

### PITFALL: Agent priority drift during multi-task sessions
**Symptom:** Agent gets absorbed in secondary task (e.g., site editing) and ignores priority redirections
**Cause:** No explicit priority enforcement; agent treats all tasks as equal
**Fix:** Use explicit 888_OVERRIDE signals. If 3+ redirections ignored, sovereign must intervene manually. Design agents with single-task focus, not multi-task breadth.

### PITFALL: Content validation too shallow
**Symptom:** `curl -sf` returns 200 but service is returning garbage data
**Cause:** Only checking HTTP status, not response body content
**Fix:** Always grep response body for expected content:
```bash
BODY=$(curl -sf --max-time 5 "http://$ep/health")
echo "$BODY" | grep -qiE '"(ok|healthy|status)"'
```

---

## Verification Checklist

After deployment, verify ALL of these:

- [ ] `systemctl list-timers <name>.timer` shows timer with NEXT value
- [ ] State file exists at `/var/lib/arifos/vps-health-state.json`
- [ ] AGI mode flag exists at `/var/lib/arifos/agi_mode`
- [ ] Watchdog log at `/var/log/arifos/vps-watchdog.log` has clean PASS entries
- [ ] First boot doesn't trigger false 888_HOLD (BOOT_GRACE works)
- [ ] Rollback validates `.bak` before restoring
- [ ] Circuit breaker locks after RETRY_BUDGET exhausted
- [ ] Dead-man's switch heartbeat confirmed at external service

---

## References

- `references/tier1-implementation.md` — Full implementation from 2026-07-12 session (files, configs, exact commands)
- `references/gemini-external-claim-audit.md` — Pattern for auditing inflated external AI claims
