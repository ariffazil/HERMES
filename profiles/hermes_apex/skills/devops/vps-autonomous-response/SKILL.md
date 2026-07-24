---
name: vps-autonomous-response
description: "Build autonomous VPS monitoring and response layers — smoketests, state machines, circuit breakers, auto-rollback, and dead-man's switches. For any VPS or infrastructure that needs self-healing without human intervention."
version: 1.0.0
author: Hermes Agent
tags: [vps, monitoring, autonomous, self-healing, state-machine, circuit-breaker, watchdog]
triggers:
  - "build autonomous monitoring"
  - "self-healing VPS"
  - "auto-rollback"
  - "circuit breaker for services"
  - "watchdog script"
  - "dead-man's switch"
---

# VPS Autonomous Response

Build self-healing VPS infrastructure that monitors, responds, and escalates — without human intervention for routine issues.

## When to Use

- VPS services crash-loop or degrade silently
- You need automated rollback on failure
- You want circuit breakers to prevent infinite restart loops
- You need dead-man's switch alerts when a machine goes silent

## When NOT to Use

- Single-service setups with `Restart=on-failure` that work fine
- Managed platforms (Heroku, Railway) that handle this natively
- When the human prefers manual control

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Cron Timer  │────→│  Smoketest   │────→│ State Machine│
│  (60s tick)  │     │  (shell, <3s)│     │  (IDLE/HEALTH│
└─────────────┘     └──────────────┘     │   /ROLLBACK) │
                                          └──────┬───────┘
                                                 │
                    ┌────────────────────────────┤
                    ▼                            ▼
            ┌──────────────┐           ┌──────────────┐
            │ Auto-Rollback│           │ 888_HOLD     │
            │ (.bak → live)│           │ (human gate) │
            └──────────────┘           └──────────────┘
```

## Implementation Steps

### 1. Smoketest Script

Dependency-free shell. Exit codes: 0=PASS, 1=DEGRADED, 2=CRITICAL.

```bash
#!/bin/bash
# /usr/local/bin/t1-smoketest.sh
# Usage: t1-smoketest.sh [service] [health-url]
# Defaults: service=1mcp.service, url=http://127.0.0.1:3050/health

SVC="${1:-1mcp.service}"
URL="${2:-http://127.0.0.1:3050/health}"

# Service active check
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"
  exit 1
fi

# Health endpoint + content validation
if [ -n "$URL" ]; then
  RESPONSE=$(curl -sf --max-time 5 "$URL" 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "FAIL: $URL unreachable"
    exit 1
  fi
  # Semantic check — not just HTTP 200
  if ! echo "$RESPONSE" | grep -qi "ok\|healthy\|pass"; then
    echo "FAIL: $URL returned garbage data"
    exit 1
  fi
fi

# Watchdog kill detection
if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill for $SVC"
  exit 2
fi

echo "PASS: $SVC"
exit 0
```

### 2. State Machine

4 states with transition logic:

| State | Meaning | Trigger |
|---|---|---|
| IDLE | No issues detected | Default state |
| OBSERVING | First failure detected, watching | Exit 1 from smoketest |
| HEALTHY | System recovered | Exit 0 after OBSERVING |
| ROLLBACK | Auto-rollback triggered | 3 consecutive failures OR exit 2 |

**Transient vs Hard failure:**
- Transient: 1-2 failures, recovers within 300s → no action
- Hard: 3 consecutive failures OR any CRITICAL (exit 2) → rollback

### 3. Circuit Breaker (RETRY_BUDGET)

Prevents infinite restart loops:

```
RETRY_BUDGET=5 per hour
  → If rollbacks in last hour > RETRY_BUDGET → 888_HOLD
  → System declares unmanageable by automation
  → Human intervention required
```

### 4. Pre-Rollback Validation

NEVER restore a .bak without validating it first:

```bash
# For systemd service files
systemd-analyze verify /etc/systemd/system/service.bak
[ $? -ne 0 ] && echo "INVALID .bak → 888_HOLD" && exit 1

# For shell scripts
bash -n /path/to/script.bak
[ $? -ne 0 ] && echo "INVALID .bak → 888_HOLD" && exit 1
```

If .bak is invalid → skip rollback → 888_HOLD immediately.

### 5. BOOT_GRACE Period

On reboot, services need time to start before the watchdog judges them:

```ini
# /etc/systemd/system/vps-t1-check.timer
[Timer]
OnBootSec=360    # 6 minutes grace after boot
OnUnitActiveSec=60  # Then every 60s
```

Without this: false 888_HOLD on every reboot because services haven't finished starting.

### 6. Flag-Based Kill Switch

NOT process kill. Use a flag file that agents read:

```bash
# Lock: prevent AGI from mutating
echo "LOCKED" > /var/lib/arifos/agi_mode

# Unlock: resume normal operations
echo "IDLE" > /var/lib/arifos/agi_mode
```

**Why flag, not kill:**
- Preserves F11 audit trail (process state visible)
- Agent can read flag and self-restrict
- Clean unlock without restart

### 7. Dead-Man's Switch

If the machine can't talk, the human should know:

**Option A: Cron heartbeat (simple)**
```bash
# Every 30 minutes, report vitals
*/30 * * * * /usr/local/bin/deadman-heartbeat.sh
```
If heartbeat stops → human notices the silence.

**Option B: External monitor (robust)**
- ntfy.sh webhook on separate infrastructure
- If VPS stops sending → external service alerts
- Survives VPS death (unlike cron on same machine)

## VPS Optimization Quick Reference

When VPS is drowning (load >50, swap >8GB):

```bash
# 1. Find the culprit
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# 2. Kill stuck processes
kill <PID>  # graceful
kill -9 <PID>  # force if graceful fails

# 3. Clean stale crons
ls /etc/cron.d/
rm -f /etc/cron.d/stale-cron-name

# 4. Drop caches (temporary relief)
sync && echo 3 > /proc/sys/vm/drop_caches

# 5. Check for duplicate processes
ps aux | grep <process-name> | grep -v grep | wc -l

# 6. Verify recovery
uptime  # load should drop within 30s
free -h  # RAM should free up
```

## Cross-VPS Monitoring

For multi-node federations, each node should monitor the others:

```bash
# On FLOW: watch FORGE
ssh -i ~/.ssh/id_ed25519 root@FORGE "uptime && systemctl is-active arifos"

# On FORGE: watch FLOW
ssh -i ~/.ssh/id_ed25519 root@FLOW "uptime && systemctl is-active hermes-asi-gateway"
```

If cross-VPS check fails → alert human. This catches network issues that local monitoring misses.

## Pitfalls

1. **Dashboard on dead timer = pretty lie.** Always verify the monitoring layer works BEFORE building visualization on top of it. (Proven 2026-07-12: AGI built Observatory dashboard while timer wasn't registered in systemd.)

2. **Watchdog too aggressive.** If watchdog timeout < service boot time, you get restart storms that drain RAM. Solution: WatchdogSec=0 (disable) or WatchdogSec ≥ 2× boot time. (Proven 2026-07-12: 22 MCP servers needed >10min to boot, WatchdogSec=600 still too low.)

3. **AGI tunnel vision.** Agents may ignore priority redirections and build what's interesting instead of what's needed. Enforcement: 888_OVERRIDE = halt immediately. (Proven 2026-07-12: AGI ignored 4 priority redirections.)

4. **Content validation > HTTP status.** curl -sf only checks reachability. grep for "ok\|healthy\|pass" in response body catches garbage data. (Closes "Semantic Gap" blindspot.)

5. **Swap thrashing hides as watchdog failure.** If RAM is exhausted, services appear to fail but the real cause is resource starvation. Check `free -h` and `uptime` before blaming the service. (Proven 2026-07-12: load 9.37, 8.6Gi swap, 44 zombie sessions.)

6. **/run is tmpfs.** Flag files in `/run/arifos/` disappear on reboot. Use `/var/lib/arifos/` for persistent state. (Proven 2026-07-12: LOCKED flag lost on reboot because it was in /run.)

7. **Resource starvation masquerades as service failure.** If load is 163 and swap is 12GB, the problem isn't watchdog config — it's RAM exhaustion. Check `free -h`, `uptime`, `ps aux --sort=-%mem` BEFORE blaming the service. Fix resource issue first, then tune watchdog. (Proven 2026-07-12: grok at 93% CPU for 20+ hours drained entire VPS.)

8. **Stuck processes are the #1 resource killer.** Check for processes with high CPU running for hours: `ps aux --sort=-%cpu | head -10`. Kill stuck opencode/grok/claude sessions. Also check for duplicate MCP server instances (capability_index spawning 3 copies). (Proven 2026-07-12: grok 93% + opencode 47.9% = load 163.)

9. **Stale crons survive service removal.** Docker disabled but docker-image-prune cron still fires. Check `/etc/cron.d/` for orphaned entries. (Proven 2026-07-12: docker-image-prune cron running on VPS with Docker disabled.)

10. **AGI will build UI before verifying infra.** Agents have a "doing > listening" pattern. They'll build dashboards, sites, and visualizations while the underlying infrastructure isn't verified. Enforcement: 888_OVERRIDE = halt immediately. Priority: infra verification → then UI. Never the reverse. (Proven 2026-07-12: AGI built Observatory dashboard while timer wasn't registered in systemd, ignored 4 priority redirections.)

## Verification

After deployment:
```bash
# Check timer is running
systemctl status vps-t1-check.timer

# Check state file exists
cat /var/lib/arifos/vps-health-state.json

# Run smoketest manually
bash /usr/local/bin/t1-smoketest.sh; echo "EXIT: $?"

# Check watchdog log
tail -20 /var/log/arifos/vps-watchdog.log
```
