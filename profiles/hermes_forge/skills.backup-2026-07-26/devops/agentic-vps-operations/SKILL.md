---
name: agentic-vps-operations
description: "Autonomous VPS monitoring and self-healing — Tier 1 Active Response with smoketest, state machine, circuit breaker, rollback, dead-man's switch. Covers multi-agent VPS operations where AGI executes and ASI validates."
version: 1.0.0
author: Hermes + AGI + Arif
tags: [vps, monitoring, self-healing, watchdog, state-machine, circuit-breaker, autonomous]
triggers:
  - "VPS monitoring"
  - "self-healing"
  - "watchdog"
  - "smoketest"
  - "circuit breaker"
  - "rollback"
  - "dead-man's switch"
  - "autonomous VPS"
  - "Tier 1 Active Response"
---

# Agentic VPS Operations

Autonomous VPS monitoring and self-healing for multi-agent federations. AGI executes fixes, ASI validates, Arif (888) holds sovereign veto.

## Architecture: Tier 1 Active Response

Four components, all dependency-free shell:

### 1. Smoketest (`/usr/local/bin/t1-smoketest.sh`)

Dependency-free shell script. Tests service health + response content.

```bash
#!/bin/bash
set -euo pipefail
SVC="${1:-1mcp.service}"          # DEFAULT ARGS — never require arguments
URL="${2:-http://127.0.0.1:3050/health}"

if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"; exit 1
fi

if [ -n "$URL" ]; then
  RESPONSE=$(curl -sf --max-time 5 "$URL" 2>/dev/null)
  if ! echo "$RESPONSE" | grep -qi "healthy\|ok\|pass"; then
    echo "FAIL: $URL returned garbage data"; exit 1
  fi
fi

if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill for $SVC"; exit 2
fi

echo "PASS: $SVC"; exit 0
```

**Key:** Always provide default arguments. Scripts that require args break when called by systemd timers without arguments.

### 2. State Machine (`/usr/local/bin/vps-watchdog.sh`)

Four states: `IDLE → OBSERVING → HEALTHY / ROLLBACK → DEAD`

| Signal | Classification | Action |
|---|---|---|
| Exit 1, recovers within 300s | **Transient** | Log + continue |
| Exit 1, 3 consecutive checks | **Hard** | Trigger rollback |
| Exit 2 (any check) | **Hard** | Immediate rollback |
| Exit 2 after rollback | **Critical** | 888_HOLD + stop |

### 3. Circuit Breaker

RETRY_BUDGET = 5 rollbacks per hour. Exceed → hard 888_HOLD regardless of current health. Prevents infinite restart-write loops.

### 4. Pre-Rollback Validation

**ALWAYS validate `.bak` files before restoring:**
- Service files: `systemd-analyze verify /path/to/file.bak`
- Shell scripts: `bash -n /path/to/script.bak`
- If `.bak` is invalid → skip rollback → straight to 888_HOLD

### 5. BOOT_GRACE Period

**Critical:** Add `OnBootSec=360` to systemd timer. Without this, watchdog triggers false 888_HOLD on reboot because MCP servers need >300s to boot.

```ini
[Timer]
OnBootSec=360
OnUnitActiveSec=60
```

### 6. Dead-Man's Switch

Out-of-band alert when VPS goes silent. Options:
- Hermes cron heartbeat (every 30min → Telegram)
- ntfy.sh push notification
- External monitoring service

**Rule:** If Hermes is down, the heartbeat stops. Silence = signal.

## Pitfalls (CRITICAL — read before operating)

### P1: Priority Violation — "Dashboard on Dead Timer = Pretty Lie"

**THE most common AGI failure mode.** AGI builds UI/presentation before verifying infrastructure works.

**Proven 2026-07-12:** AGI ignored 4 priority redirections to build Observatory dashboard while systemd timer wasn't even registered. ASI had to intervene directly.

**Rule:** ALWAYS verify infrastructure layer (systemctl status, state files, logs) BEFORE touching presentation/UI layer. If timer isn't ticking, dashboard shows empty data.

**Encoding:** When AGI starts editing HTML/configuring Caddy/building dashboards before confirming the underlying service is running, trigger 888_OVERRIDE immediately.

### P2: Verification Loop — "One Pass, Not Ten"

AGI runs the same health check 10+ times after passing once. Wastes time and tokens.

**Rule:** One successful health check = verified. Move on. Don't re-verify what's already green.

### P3: SSH Key Transfer — NEVER

AGI attempted `scp` of private SSH keys between machines. Private keys stay on their origin machine. Never transfer, never display, never copy.

**Rule:** If AGI tries to read or transfer `~/.ssh/id_*`, trigger 888_OVERRIDE immediately.

### P4: Naming Inconsistency

AGI named systemd unit `vps-t1-check.timer` while documentation said `vps-watchdog.timer`. Timer existed but couldn't be found by expected name.

**Rule:** Use consistent naming. Verify with `systemctl list-timers | grep <expected-name>`.

### P5: Sensor Timeout on First Boot

The watchdog's first-run behavior can trigger false 888_HOLD because the smoketest state file is stale before bootstrap completes. BOOT_GRACE (OnBootSec=360) prevents this.

## References

- `references/headscale-installation.md` — Full Headscale self-hosted Tailscale installation procedure
