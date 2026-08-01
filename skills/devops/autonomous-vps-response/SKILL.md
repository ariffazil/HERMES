---
name: autonomous-vps-response
description: "Tier 1 Active Response pattern — autonomous VPS health monitoring with smoketest, state machine, circuit breaker, rollback, 888_HOLD escalation, and dead-man's switch. MERGED from 5 redundant VPS skills."
version: 2.0.0
author: Hermes Agent (consolidated from vps-autonomous-ops, vps-autonomous-response, vps-agentic-ops, agentic-vps-operations)
tags: [vps, monitoring, self-healing, circuit-breaker, rollback, autonomous, tier1, watchdog, deadman]
organ: A-FORGE (:7071)
zen-organs: [W EXECUTION, ΔR REPAIR, Ω WITNESS, ∂M/∂t MEMORY]
aaa-contract: MISSING — needs Agentic Infrastructure Worker card
triggers:
  - "build autonomous monitoring"
  - "self-healing VPS"
  - "circuit breaker for services"
  - "auto-rollback on failure"
  - "tier 1 active response"
  - "dead-man's switch"
  - "watchdog script"
  - "VPS health monitoring automation"
  - "smoketest"
  - "active response"
  - "state machine vps"
  - "vps monitoring"
---

# Autonomous VPS Response (Tier 1)

Self-healing infrastructure pattern. Zero dependencies. Pure shell. Fires on systemd timer.

**ABSORBED:** vps-autonomous-ops · vps-autonomous-response · vps-agentic-ops · agentic-vps-operations
**KEEP DISTINCT:** vps-operations (diagnostics/cleanup) · agentic-infrastructure-ops (mesh/networking) · vps-machine-health (profiling)

---

## Architecture (5-Layer)

```
systemd timer (60s)
  → L1: t1-smoketest.sh (health probe — <3s, shell)
    → L2: vps-watchdog.sh (state machine: IDLE→OBSERVING→HEALTHY→ROLLBACK)
      → L3: Circuit breaker (RETRY_BUDGET: 5/hour → 888_HOLD)
        → L4: Flag-based kill switch (/var/lib/arifos/agi_mode)
          → L5: Dead-man's switch (cron heartbeat → Telegram/ntfy.sh)
```

### Layer 1: Smoketest (`/usr/local/bin/t1-smoketest.sh`)

Dependency-free shell script. Exit codes: 0=PASS, 1=DEGRADED, 2=CRITICAL.

```bash
#!/bin/bash
set -euo pipefail
SVC="${1:-1mcp.service}"          # DEFAULT ARGS — never require arguments
URL="${2:-http://127.0.0.1:3050/health}"
FAIL=0

# Service active check
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"; exit 1
fi

# Health URL reachable + content validation
if [ -n "$URL" ]; then
  RESPONSE=$(curl -sf --max-time 5 "$URL" 2>/dev/null || echo "UNREACHABLE")
  if [ "$RESPONSE" = "UNREACHABLE" ]; then
    echo "FAIL: $URL unreachable"; ((FAIL++))
  fi
  # Semantic check: HTTP 200 ≠ healthy. Grep for actual health indicator.
  if ! echo "$RESPONSE" | grep -qi "healthy\|ok\|pass\|ready"; then
    echo "WARN: $URL returned unexpected content"; ((FAIL++))
  fi
fi

# VPS vitals (memory + disk)
RAM_PCT=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
DISK_PCT=$(df / | awk 'NR==2 {gsub(/%/,""); print $5}')
[ "$RAM_PCT" -gt 85 ] && echo "WARN: RAM ${RAM_PCT}%" && ((FAIL++))
[ "$DISK_PCT" -gt 90 ] && echo "WARN: Disk ${DISK_PCT}%" && ((FAIL++))

# Recent watchdog kills
if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill for $SVC"; exit 2
fi

[ "$FAIL" -eq 0 ] && echo "PASS: $SVC" && exit 0
[ "$FAIL" -le 2 ] && exit 1
exit 2
```

**Key design:** Default args work without arguments (direct debugging). Content validation > HTTP status. Vitals monitoring integrated.

### Layer 2: State Machine (`/usr/local/bin/vps-watchdog.sh`)

```
STATE FILE: /var/lib/arifos/vps-health-state.json (persistent — NOT /run/)

HEALTHY ←→ DEGRADED → CRITICAL → DEAD
    ↑          │           │         │
    └──────────┘           │         │
    (recovery <300s)       │         │
                           ▼         │
                      auto-rollback  │
                           │         │
                           ▼         │
                      rollback fail  │
                           │         │
                           ▼         │
                      888_HOLD ──────┘
```

| Signal | Classification | Action |
|---|---|---|
| Exit 1, recovers within 300s | **Transient** | Log + continue |
| Exit 1, 3 consecutive checks | **Hard** | Trigger rollback |
| Exit 2 (any single check) | **Hard** | Immediate rollback |
| 5 rollbacks in 1 hour | **Circuit break** | Hard 888_HOLD |

**State file schema:**
```json
{
  "state": "IDLE",
  "last_update": "ISO8601",
  "services": {
    "service-name": {
      "retries": 0,
      "rollbacks": 0,
      "last_rollback": 0,
      "hour_rollbacks": 0
    }
  }
}
```

### Layer 3: Circuit Breaker (RETRY_BUDGET)

Max 5 rollbacks per hour → hard 888_HOLD regardless of current health. Prevents infinite restart-write loop → disk death spiral.

```bash
HOUR_ROLLBACKS=$(jq '.services."'"$SVC"'".hour_rollbacks' "$STATE_FILE")
if [ "$HOUR_ROLLBACKS" -ge 5 ]; then
  echo "888_HOLD: RETRY_BUDGET exhausted for $SVC"
  echo "LOCKED" > /var/lib/arifos/agi_mode
  exit 2
fi
```

### Layer 4: Pre-Rollback Validation

NEVER restore a .bak without validating it first:

| File type | Validation command | Fail action |
|---|---|---|
| systemd service/timer | `systemd-analyze verify /path/to/file.bak` | Skip, go to 888_HOLD |
| Shell scripts | `bash -n /path/to/script.bak` | Skip, go to 888_HOLD |
| Config files | Application-specific syntax check | Skip, go to 888_HOLD |

**Rollback sequence:**
1. Pre-rollback log snapshot → `/var/lib/arifos/log-snapshot-*.log`
2. Validate .bak file
3. Restore .bak → systemctl daemon-reload + systemctl restart $SERVICE
4. Verify with smoketest
5. If fail → increment rollback counter → retry (max 3)
6. 3 failed rollbacks → 888_HOLD

### Layer 5: Flag-Based Kill Switch

NOT process kill. Flag file that agents read — preserves F11 audit trail.

```bash
# Lock: prevent AGI from mutating
echo "LOCKED" > /var/lib/arifos/agi_mode
# Unlock: after smoketest confirms HEALTHY
echo "IDLE" > /var/lib/arifos/agi_mode
```

**Critical:** Flag MUST be on persistent storage (`/var/lib/arifos/`), NOT tmpfs (`/run/`). Tmpfs is wiped on reboot.

### Layer 6: BOOT_GRACE Period

On reboot, services need time to boot before the watchdog judges them. 22 MCP servers need >300s.

```ini
# /etc/systemd/system/vps-t1-check.timer
[Unit]
Description=VPS Tier-1 Health Check Timer (every 60s)
Requires=vps-t1-check.service

[Timer]
OnBootSec=360        # 6 min grace after boot
OnUnitActiveSec=60   # Then every 60s
AccuracySec=1s

[Install]
WantedBy=timers.target
```

Without BOOT_GRACE: false 888_HOLD on every reboot because services are still starting.

### Layer 7: Dead-Man's Switch (OOB Alert)

The monitoring system itself can die. Two layers:

**A. System cron heartbeat (every 30 min):**
```bash
#!/bin/bash
# /usr/local/bin/deadman-heartbeat.sh
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | awk '{print $1}')
DISK=$(df / | awk 'NR==2 {print 5}')
RAM=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
echo "🫀 heartbeat: up=$UPTIME load=$LOAD disk=$DISK ram=$RAM"
```
Cron: `*/30 * * * * /usr/local/bin/deadman-heartbeat.sh`
If heartbeat stops → the silence IS the alert.

**B. ntfy.sh webhook (optional, on separate infra):**
```bash
TOPIC="arifos-$(hostname)-heartbeat"
curl -sf -H "Title: 🟢 $(hostname) alive" -H "Tags: heartbeat,green" \
  -H "Priority: low" \
  -d "Up: $UPTIME | Load: $LOAD | RAM: $MEM | Disk: $DISK" \
  "https://ntfy.sh/$TOPIC"
```

**Dead-man's switch is NOT optional.** Without it, if the monitoring system dies, nobody knows.

---

## Agent Heartbeat Response Protocol

When a heartbeat poll arrives (HEARTBEAT_OK, BEAT_OK, ARTBEAT_OK):

- **All green:** Respond with exactly HEARTBEAT_OK (or Hijau / Green). Do NOT make tool calls. Do NOT explain or narrate. Silent on green.
- **Something needs attention:** Do NOT include HEARTBEAT_OK. Report the specific issue concisely. If action is needed, state what and do it.
- **arifOS known pattern:** event-loop hang from dead LLM API key. If arifOS is unresponsive, restart (systemctl restart arifos && sleep 12), verify, report briefly.

---

## Cross-VPS Monitoring

For multi-node federations, each node monitors the others:

```bash
# On FLOW: watch FORGE
ssh root@FORGE "uptime && systemctl is-active arifos"
# On FORGE: watch FLOW
ssh root@FLOW "uptime && systemctl is-active hermes-asi-gateway"
```

If cross-VPS check fails → alert human. Catches network issues local monitoring misses.

---

## Hermes Role (Active Validator, Not Echo Chamber)

When AGI (OpenClaw) is doing operational work on VPS:

1. **Validate every write/restart/rollback** against F1 (reversibility). No .bak = no go.
2. **Check smoketest output** before approving next action. Do not just echo status.
3. **Call out recon loops.** If AGI runs 5+ list/show commands without actionable output, redirect to targeted diagnostics.
4. **Gate Tier boundaries.** Tier 1 = auto-fix. Tier 2 = needs sovereign ack.
5. **Detect task absorption loops.** If AGI ignores 2+ priority redirections, escalate to 888_OVERRIDE.
6. **Priority enforcement.** When Sovereign/ASI issues a priority directive, AGI must complete it before other work.
7. **Detect runaway CPU loops.** If an agent process shows >80% sustained CPU and repeats identical output 30+ times, do not engage — find the PID and kill it. Verbal correction is wasted on a process that has stopped reading input. See "Runaway Agent Process Recovery" below.

---

## Runaway Agent Process Recovery

When an agent process (OpenCode, OpenClaw agent session) enters a **cognitive loop** — repeating identical or near-identical output while burning excessive CPU — it must be killed at the OS level. Verbal redirection is ineffective; the agent is no longer reading fresh state.

### Detection

```bash
# Sort by CPU — runaway agents typically show >100% CPU sustained
ps aux | grep -E 'opencode|openclaw' | grep -v grep
```

Key signals:
- CPU usage >80% sustained (two agents in mutual loop can consume 180% combined)
- Same message template repeated 30+ times in minutes with minor prose variations
- Agent claims "stale dist" / "pending edit" for work already deployed and verified with live probes
- Agent fixates on a screenshot while live `curl` probes contradict it
- Agent ignores 2+ corrections backed by exact evidence (bundle hash, timestamp, content check)

### Recovery

```bash
# Kill specific runaway PIDs (NOT the gateway or bot bridge)
kill <PID1> <PID2>

# Confirm only infrastructure processes remain
ps aux | grep -E 'opencode|openclaw' | grep -v grep | awk '{print $2, $3"%CPU", $11, $12}'
```

**⚠️ Pitfall — systemd auto-restart:** If killed agent processes reappear with new PIDs within seconds, they're managed by a systemd service with `Restart=always` or `Restart=on-failure`. Killing the process just triggers a restart. You must stop the service:

```bash
# List relevant agent services
systemctl list-units --type=service | grep -iE 'openclaw|opencode|claw'

# Stop the service (not just kill the process)
systemctl stop opencode-bot.service openclaw-gateway.service

# Verify they stay stopped
systemctl is-active opencode-bot.service openclaw-gateway.service
```

**⚠️ Pitfall — stop isn't permanent:** Some services with `Restart=always` will auto-restart even after `systemctl stop`. If `is-active` shows `active` again within minutes after a stop, you must **mask** the service to prevent all starts until explicitly unmasked:

```bash
# Mask — prevents ALL starts (manual + auto-restart) until unmasked
systemctl stop opencode-bot.service openclaw-gateway.service
ln -sf /dev/null /etc/systemd/system/openclaw-gateway.service
ln -sf /dev/null /etc/systemd/system/opencode-bot.service
systemctl daemon-reload

# Verify masking blocked
systemctl start openclaw-gateway.service 2>&1
# Expected: "Failed to start openclaw-gateway.service: Unit is masked."

# To restore later (only after root cause is fixed):
systemctl unmask opencode-bot.service openclaw-gateway.service
systemctl daemon-reload
systemctl start opencode-bot.service openclaw-gateway.service
```

**When to mask vs stop:** Stop the service first. Only mask if it restarts itself despite the stop. Masking is an escalation — the service cannot be started by ANY means (manual, timer, restart) until explicitly unmasked. Always save the restart commands (unmask + daemon-reload + start) so the user can restore when ready.

**Known auto-restart services in arifOS federation:**
| Service | Role | Restart? |
|---|---|---|
| `opencode-bot.service` | Telegram bridge agent (777-FORGE, HANDS layer) | Auto-restart |
| `openclaw-gateway.service` | Multi-agent message router | Auto-restart |
| `opencode.service` | OpenCode server (localhost:4096) | Active (single instance) |

**Restart after incident resolved:**
```bash
systemctl start opencode-bot.service openclaw-gateway.service
```

### What to Preserve vs Kill

| Process Pattern | Role | Keep? |
|---|---|---|
| `openclaw` (+ `openclaw-tui`) | CLI session | ✅ Keep |
| `openclaw` gateway (`/usr/bin/node .../dist/index.js gateway`) | Message routing | ✅ Keep |
| `opencode serve --hostname 127.0.0.1` | Agent server | ✅ Keep |
| `opencode-bot` (`python3 .../bot.py`) | Telegram bridge | ✅ Keep |
| `opencode` (standalone, >80% CPU, no args like `serve` or `bot`) | Stuck agent session | ❌ **Kill** |

### Post-Recovery Verification

```bash
# Confirm no new agents have spawned to replace the killed ones
ps aux | grep -E 'opencode$|opencode ' | grep -v grep | grep -v serve | grep -v bot
# Should return empty — no agent sessions running
```

### Root Cause Pattern

Agent stuck-loop almost always begins with a **screenshot of stale cached content** that the agent cannot distinguish from live state. The path:
1. Agent receives screenshot from a stale cached page
2. Agent reads image transcript, diagnoses "problems" that don't exist in live code
3. Agent proposes a "fix plan" for problems already resolved
4. Agent's own context loop reinforces the plan as "pending work"
5. Each turn generates an identical status report while CPU spirals

### Prevention Checklist

- [ ] When agent fixates on a screenshot that contradicts live probes, state the discrepancy **once** with exact evidence
- [ ] If agent ignores 2+ corrections: **stop engaging** — find and kill the process
- [ ] Verify live state with `curl` and `grep` before declaring any build "stale"
- [ ] Match live bundle hash against dist directory: `curl -s https://example.com/ | grep -oP 'index-\K[A-Za-z0-9]+(?=\.js)'`

**Real-world incident:** See `references/runaway-agent-recovery-2026-07-31.md` — 60+ duplicate messages, 180% CPU, two agents killed, service masking required when `systemctl stop` was insufficient against `Restart=always`.

---

## The "Pretty Lie" Principle

**A dashboard built on unverified infrastructure is a pretty lie.** Sequence ALWAYS:
1. Verify infrastructure timer/service (`systemctl status`)
2. Verify data files exist and are populated (`cat state.json`)
3. Verify logs are clean (`tail watchdog.log`)
4. THEN build/deploy the dashboard

---

## P1–P5 Priority Pitfall List (from agentic-vps-operations)

| # | Pitfall | What Happened | Fix |
|---|---|---|---|
| P1 | **Priority violation** | AGI built dashboard while timer wasn't registered | Infra before UI. 888_OVERRIDE if violated. |
| P2 | **Verification loop** | AGI ran same health check 10+ times | One pass = verified. Move on. |
| P3 | **SSH key transfer** | AGI tried `scp ~/.ssh/id_ed25519` | NEVER transfer private keys. |
| P4 | **Naming inconsistency** | `vps-t1-check.timer` vs `vps-watchdog.timer` | Consistent naming. Verify with `systemctl list-timers`. |
| P5 | **Missing daemon-reload** | Timer file existed but not registered | Always `systemctl daemon-reload` after service/timer edits. |
| P6 | **State file on tmpfs** | `/run/arifos/` lost on reboot | Use `/var/lib/arifos/` (persistent). |
| P7 | **HTTP 200 ≠ healthy** | Service returned 200 with garbage | Content validation — grep for "healthy". |
| P8 | **Watchdog too aggressive** | WatchdogSec too low for 22 MCP servers | Set WatchdogSec=0 or ≥ 2× boot time. |
| P9 | **Boot grace too short** | False 888_HOLD after reboot | OnBootSec=360. |
| P10 | **Dashboard before verification** | AGI built UI before infra was live | Always infra → state → log → THEN dashboard. |
| P11 | **Runaway agent loop** | OpenCode/OpenClaw agent stuck repeating same message 30+ times, burning >80% CPU. Verbal correction ignored — process stopped reading input. | `kill <PID>`. If it respawns instantly, check for systemd auto-restart: `systemctl list-units \| grep -i opencode` → `systemctl stop <service>`. |

---

## Watchdog Tuning

### When to disable: `WatchdogSec=0`

If services get SIGKILL'd due to resource pressure (swap thrashing, high load), disable temporarily:
```ini
WatchdogSec=0   # Disabled — Restart=on-failure handles crashes
```
Disable during degraded states, re-enable after stabilization.

### Always verify daemon-reload after editing timer/service files

```bash
systemctl daemon-reload
systemctl enable <timer-name>.timer
systemctl start <timer-name>.timer
systemctl list-timers <timer-name>.timer  # verify NEXT column
```

---

## How To Use This Skill

### When VPS is drowning (load >50, swap >8GB):

```bash
# 1. Find the culprit
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# 2. Kill stuck processes
kill <PID>; kill -9 <PID> if graceful fails

# 3. Anti-Hantu cleanup — kill zombies and orphan MCP children
ps aux | awk '$8~/Z/{print $2}' | xargs -r kill -9 2>/dev/null
# Orphan MCP children from dead agent sessions:
for pid in $(ps -eo pid,ppid= | awk '$2==1{print $1}'); do
  cmd=$(cat /proc/$pid/comm 2>/dev/null)
  if echo "$cmd" | grep -qE "capability.index|chrome-devtools|github-mcp-server|playwright|postgres-mcp"; then
    kill -9 $pid 2>/dev/null && echo "killed orphan $pid ($cmd)"
  fi
done

# 4. Drop caches (temporary)
sync && echo 3 > /proc/sys/vm/drop_caches

# 5. Verify recovery
uptime && free -h
```

### When building new monitoring for a service:

```
t1-smoketest.sh → default args → systemd timer (60s, BOOT_GRACE 360s) 
  → watchdog.sh → state machine → rollback → circuit breaker
```

---

## Verification Checklist

After deployment, verify ALL:

- [ ] `systemctl list-timers vps-t1-check.timer` — NEXT value present
- [ ] `systemctl cat vps-t1-check.timer` — OnBootSec=360, OnUnitActiveSec=60
- [ ] `/var/lib/arifos/vps-health-state.json` — valid JSON
- [ ] `/var/lib/arifos/agi_mode` — not in /run/
- [ ] `/var/log/arifos/vps-watchdog.log` — clean PASS entries
- [ ] First boot: no false 888_HOLD (BOOT_GRACE works)
- [ ] Smoketest works without arguments: `bash t1-smoketest.sh; echo $?` → 0
- [ ] Rollback validates .bak before restoring
- [ ] Circuit breaker locks after RETRY_BUDGET exhausted (5/hour)

---

## AAA A2A Contract

**Status:** 🔴 MISSING — needs Agentic Infrastructure Worker card in AAA

Required registration:
```yaml
agent_id: "agentic-infrastructure-worker"
role: "agentic-vps-worker"
organ: "A-FORGE"
contract: "A2A_INFRA_OPS_CONTRACT"
capabilities:
  - "self-healing-vps"
  - "auto-rollback"
  - "circuit-breaker"
  - "deadman-switch"
  - "health-monitoring"
```

---

## References (preserved from absorbed skills)

- `references/headscale-installation.md` — Headscale setup
- `references/tailscale-acl-policy.md` — Tag-based ACLs
- `references/tier1-implementation.md` — Full implementation from 2026-07-12
- `references/cross-vps-ssh-federation.md` — Cross-VPS SSH
- `references/blindspot-analysis-methodology.md` — Autonomous system blindspots
- `references/python-package-conflict-recovery.md` — pip namespace conflict fix
