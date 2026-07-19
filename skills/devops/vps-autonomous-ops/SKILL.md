---
name: vps-autonomous-ops
description: "Build and operate autonomous VPS control loops — smoketest, state machine, rollback, circuit breaker, dead-man's switch. Class-level pattern for self-healing infrastructure under arifOS governance."
triggers:
  - VPS health monitoring automation
  - Self-healing service infrastructure
  - Autonomous rollback and circuit breaker
  - Tier 1 auto-fix policy design
  - Dead-man switch and OOB alerting
  - Closed-loop control for server ops
  - systemd timer watchdog
  - pretty-lie dashboard trap
---

# VPS Autonomous Operations

> **Class:** DevOps — autonomous infrastructure self-healing.
> **Prerequisite:** Existing monitoring (Netdata/Cadvisor) + systemd services + arifOS F1-F13 governance.

## When to Use

When building autonomous monitoring, self-healing, and active response for VPS or server infrastructure. This is NOT for simple uptime monitoring (use UptimeRobot/cron ping). This is for systems that need to **diagnose, act, rollback, and escalate** without human intervention.

## Architecture Pattern (5 Layers)

### Layer 1: Smoketest (The Sensor)

Pure shell. Zero dependencies. Less than 3s execution. If the smoketest itself cannot run, the system is dead — escalation is automatic.

```bash
# Health endpoints — curl with timeout, validate response BODY not just HTTP code
curl -sf --max-time 5 "http://localhost:PORT/health" | grep -q '"status":"ok"'
# Vitals — raw /proc, no dependencies
RAM_PCT=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
DISK_PCT=$(df / | awk 'NR==2 {gsub(/%/,""); print $5}')
```

**Exit codes:** 0=healthy, 1=degraded (2 or fewer failures), 2=critical (3+ failures)

**Default argument fallback** — smoketest should work when called without arguments (direct invocation during debugging):
```bash
SVC="${1:-1mcp.service}"       # fallback to primary service
URL="${2:-http://127.0.0.1:3050/health}"  # fallback to known endpoint
```

**Critical pitfall:** HTTP 200 is not functional. Always grep response body for expected strings (ok, healthy, ready). A service returning 200 with corrupted data is a silent failure ("pretty lie" — see Pitfalls).

### Layer 2: State Machine (The Brain)

```
IDLE -> OBSERVING (300s window) -> HEALTHY / ROLLBACK
```

| Signal | Classification | Action |
|---|---|---|
| Exit 1, recovers within 5 checks (300s) | **Transient** | Log + continue |
| Exit 1, 3 consecutive checks | **Hard** | Trigger rollback |
| Exit 2 (any single check) | **Hard** | Immediate rollback |
| 5 rollbacks in 1 hour | **Circuit break** | Hard 888_HOLD |

**Transient vs Hard distinction is critical.** Without it, flapping services trigger cascading restarts that exhaust disk write cycles and fill /var/log.

### Layer 3: Rollback (The Immune Response)

**Pre-rollback validation is MANDATORY.** Never cp from .bak without checking:

| File type | Validation command | Fail action |
|---|---|---|
| systemd service/timer | `systemd-analyze verify file.bak` | Skip, go to 888_HOLD |
| Shell scripts | `bash -n script.bak` | Skip, go to 888_HOLD |
| Config files | Application-specific syntax check | Skip, go to 888_HOLD |

**Pre-rollback log snapshot** — capture journalctl output BEFORE restoring .bak. Post-mortem depends on knowing what state the system was in before the revert.

**Max 3 rollback attempts.** After that, system is declared unmanageable by automation, go to 888_HOLD.

### Layer 4: Kill Switch (The Handoff)

**Flag-based, NOT process kill.** Preserves F11 audit trail and allows AGI to read its own status.

```bash
# Lock: ASI writes flag
echo "LOCKED" > /var/lib/arifos/agi_mode
# Unlock: only after smoketest confirms HEALTHY
echo "IDLE" > /var/lib/arifos/agi_mode
```

**Critical pitfall:** Flag MUST be on persistent storage (`/var/lib/arifos/`), NOT tmpfs (`/run/`). Tmpfs is wiped on reboot, AGI boots into UNLOCKED, could execute unwanted mutations before monitoring is ready.

**Default boot state:** LOCKED until smoketest confirms HEALTHY. Safe default.

### Layer 5: Dead-Man's Switch (The OOB Alert)

The monitoring system itself can die. You need an alert path that is **independent of the VPS:**

- ntfy.sh, Telegram Bot API direct call, or external webhook
- System-level cron (NOT application-level) — runs even if your app stack is dead
- Heartbeat interval: 60s. Timeout: 300s (5 missed heartbeats)
- If heartbeat stops, push notification to phone

External service detects absence and sends alert. VPS does not need to be alive to trigger this.

## Watchdog Tuning (Critical)

### When to disable watchdog: `WatchdogSec=0`

If services are getting SIGKILL'd by watchdog due to **resource pressure** (swap thrashing, high load), disable watchdog temporarily:
```ini
# In 1mcp.service or similar
WatchdogSec=0   # Disabled — Restart=on-failure handles crashes
```

**Reasoning:** With 22+ MCP servers, boot time can exceed 10 minutes. `WatchdogSec=600` (10min) was still insufficient. The watchdog was creating a restart storm that worsened the resource pressure. Disable during degraded states, re-enable after stabilization.

### OnBootSec grace period

After a reboot, MCP servers need time to fully boot. Set `OnBootSec=360` (6 min) to delay the first timer tick:
```ini
[Timer]
OnBootSec=360        # 6 min grace after boot
OnUnitActiveSec=60   # Then every 60s
```

Without this, the watchdog fires while servers are still booting, triggers false 888_HOLD, and burns RETRY_BUDGET.

### Always verify daemon-reload after editing timer/service files

**Symptom:** `systemctl status vps-t1-check.timer` → "Unit could not be found"

**Cause:** Wrote .timer/.service files but forgot `systemctl daemon-reload`

**Fix sequence:**
```bash
systemctl daemon-reload
systemctl enable <timer-name>.timer
systemctl start <timer-name>.timer
systemctl list-timers <timer-name>.timer  # verify NEXT column has value
```

## Hermes Role (Active Validator, Not Echo Chamber)

When AGI (OpenClaw) is doing operational work on VPS:

1. **Validate every write/restart/rollback** against F1 (reversibility). No .bak = no go.
2. **Check smoketest output** before approving next action. Do not just echo status — interpret it.
3. **Call out recon loops.** If AGI runs 5+ list/show commands without actionable output, redirect to targeted diagnostics (`journalctl -p 3`, `dmesg | grep -iE 'error|fail|oom|kill'`).
4. **Gate Tier boundaries.** Tier 1 = auto-fix (service restart, config tweak). Tier 2 = needs sovereign ack (kernel, firewall, package install, reboot).
5. **Detect task absorption loops.** AGI can get absorbed in unrelated work (e.g., editing a website) while infrastructure validation is pending. If AGI ignores 2+ priority redirections, escalate to 888_OVERRIDE.
6. **Priority enforcement.** When Sovereign or ASI issues a priority directive ("do X first"), AGI must complete it before resuming other work. If AGI continues unrelated work after 2 redirections, declare the session compromised and request Sovereign intervention.

## The "Pretty Lie" Principle

**A dashboard built on unverified infrastructure is a pretty lie.** Never deploy visualization (HTML, API, dashboard) before verifying the underlying data source is live and correct. The sequence is ALWAYS:

1. Verify infrastructure timer/service is running (`systemctl status`)
2. Verify data files exist and are populated (`cat state.json`)
3. Verify logs are clean (`tail watchdog.log`)
4. THEN and ONLY THEN build/deploy the dashboard

AGI violated this in the 2026-07-12 session — jumped to Observatory site editing while the watchdog timer hadn't even been verified as running. The dashboard would have displayed empty or stale data.

## Anomaly Triage Patterns

### Phantom users (stale utmp)

`uptime` or `w` shows many logged-in users (e.g., 44) but `w` output has empty USER/TTY/FROM columns. This is a **stale `/var/run/utmp` file**, not actual sessions. Benign — not an intrusion.

```bash
w | head -n 10    # If USER column empty = phantom
ps aux | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 10  # Actual processes
```

### High load during watchdog restart storms

Load average spikes (9.37, 5.56, 4.46) during watchdog cycling are caused by the restart storm itself, not by the original failure. Disable watchdog (`WatchdogSec=0`), let load settle, then diagnose the root cause.

## Pitfalls (MUST READ)

1. **Missing directories on first run.** State file and log paths must exist before first timer tick. Add `mkdir -p` at script top.
2. **Shallow health checks.** HTTP 200 with garbage body = false healthy. Always validate content ("pretty lie").
3. **.bak files corrupted or outdated.** Validate before restore. A blind rollback that restores broken state creates a restart loop.
4. **No circuit breaker.** Without RETRY_BUDGET (5 rollbacks per hour, then 888_HOLD), a buggy rollback config creates infinite restart-write loop. Disk death spiral.
5. **Flag in tmpfs.** `/run/arifos/mode` vanishes on reboot. Use `/var/lib/arifos/mode`.
6. **No OOB alert.** If the monitoring system dies, nobody knows. Dead-man switch is not optional.
7. **systemd timer vs daemon.** Timer is lighter, more debuggable (`systemctl list-timers`), and has integrated logging. Use timer for periodic checks, not a persistent daemon.
8. **AGI task absorption loop.** AGI gets absorbed in unrelated work (HTML editing, code reading) while critical infrastructure validation is pending. It ignores priority redirections from both ASI and Sovereign. Detection: AGI runs 3+ non-infrastructure tool calls after a priority directive. Response: 888_OVERRIDE signal, declare session compromised if no response after 2 attempts.
9. **Watchdog too aggressive.** `WatchdogSec=600` (10min) can still be insufficient for services with many child processes (22 MCP servers). If SIGKILL persists after raising the limit, disable watchdog entirely (`WatchdogSec=0`) and rely on `Restart=on-failure`. Re-enable after root cause is fixed.
10. **BOOT_GRACE too short.** `OnBootSec=30` is not enough. Use `OnBootSec=360` (6 min) to give MCP servers time to fully boot before sensor starts judging.
11. **Smoketest requires arguments but caller doesn't provide.** Always set default fallbacks in the script (`SVC="${1:-1mcp.service}"`) so it works both from the watchdog (with args) and from direct invocation (without args).
12. **Dashboard before verification.** Building visualization before confirming data source is live = "pretty lie". Always verify infra → state → log → THEN dashboard.
13. **SSH key transfer/display.** AGI attempted to SCP and display private SSH keys during cross-VPS operations. NEVER transfer, display, or read private keys. Keys stay on their origin machine. If AGI attempts this, 888_OVERRIDE immediately. Proven 2026-07-14: AGI tried `scp ~/.ssh/id_ed25519` and `cat ~/.ssh/id_ed25519.pub` to remote servers.
14. **Redundant installation.** AGI continued installing Headscale via SSH after it was already installed locally by ASI. Always check `which <binary> && <binary> --version` before installing. Wasted 10+ SSH commands on redundant work. Proven 2026-07-14.
15. **Hosted Tailscale conflict.** If machine already has hosted Tailscale registered, `tailscale up --login-server=<headscale>` will conflict. Check `tailscale status` first. Options: dual-stack (separate socket), full migration (disconnect hosted), or deferred (install Headscale, migrate later).
16. **AGI verification loop.** Distinct from task absorption — AGI runs the same health/status check 10+ times without progressing to next step. Example: checking `headscale health`, `systemctl status`, `curl /health` repeatedly after confirming it's already live. Detection: same command or equivalent check runs 3+ times. Response: "AGI — verified. Stand down." Proven 2026-07-14: AGI checked Headscale health 10+ times after it was confirmed live.
17. **AGI essay mode.** AGI produces verbose multi-paragraph analysis when user wanted a one-line headline. Same pattern as "essay machine" in claim-validation-protocol but for AGI's own output. Detection: user sends stickers/crying emojis after AGI output. Response: compress to one line. Proven 2026-07-14: AGI produced 500-word Tailscale analysis when Arif wanted "install or not?" Arif responded with crying stickers.
18. **Pip namespace conflict.** Two packages (e.g. `fastmcp` + `fastmcp-slim`) sharing the same `site-packages/` directory causes import corruption. `uv pip install "pkg<3.0"` doesn't auto-remove the conflicting slim variant because they have different package names but the same namespace directory. Fix: uninstall the slim variant, then `uv pip install --reinstall "pkg<3.0"`. See `references/python-package-conflict-recovery.md` for full recipe. Proven 2026-07-19: GEOX crash loop from fastmcp-slim 3.4.2 shadowing fastmcp 2.14.7.

## Verification Checklist

After deployment, verify ALL of these:

- [ ] `systemctl list-timers <name>.timer` shows timer with NEXT value
- [ ] `systemctl cat <name>.timer` shows correct `OnBootSec` (360) and `OnUnitActiveSec` (60)
- [ ] State file exists at `/var/lib/arifos/vps-health-state.json` with valid JSON
- [ ] AGI mode flag exists at `/var/lib/arifos/agi_mode` (not `/run/`)
- [ ] Watchdog log at `/var/log/arifos/vps-watchdog.log` has clean PASS entries
- [ ] First boot doesn't trigger false 888_HOLD (BOOT_GRACE works)
- [ ] Smoketest works without arguments (`bash t1-smoketest.sh; echo $?` → 0)
- [ ] Rollback validates `.bak` before restoring
- [ ] Circuit breaker locks after RETRY_BUDGET exhausted
- [ ] Dead-man's switch heartbeat confirmed at external service
- [ ] No phantom SIGKILL in `journalctl -u <service> --since "1 hour ago" | grep -i watchdog`

## Implementation Checklist

- `t1-smoketest.sh` — pure shell, exit codes 0/1/2, response body validation, default args
- `vps-watchdog.sh` — state machine, rollback with .bak validation, circuit breaker, BOOT_GRACE
- `vps-t1-check.service` + `vps-t1-check.timer` — systemd timer, `OnBootSec=360`, 60s interval
- `ntfy.sh` cron — dead-man switch, 300s timeout
- `/var/lib/arifos/` directory created (persistent, not tmpfs)
- Dry-run validation before going live
- 888_HOLD notification path confirmed (Telegram DM to Arif)

## Dead-Man's Switch Implementation (ntfy.sh)

### Script
```bash
#!/bin/bash
# /root/scripts/deadman-heartbeat.sh
TOPIC="arifos-forge-heartbeat"
HOST=$(hostname)
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
MEM=$(free -h | awk '/Mem:/{printf "%s/%s (%.0f%%)", $3, $2, $3/$2*100}')
DISK=$(df -h / | awk 'NR==2{printf "%s/%s (%s)", $3, $2, $5}')
curl -sf \
  -H "Title: 🟢 $HOST alive" \
  -H "Tags: heartbeat,green" \
  -H "Priority: low" \
  -d "Up: $UPTIME | Load: $LOAD | RAM: $MEM | Disk: $DISK" \
  "https://ntfy.sh/$TOPIC" >/dev/null 2>&1
```

### Cron: `*/30 * * * * /root/scripts/deadman-heartbeat.sh`
### Subscribe: `ntfy subscribe arifos-forge-heartbeat` or open `https://ntfy.sh/arifos-forge-heartbeat`

**Design:** System-level cron (runs even if app stack dead). 30-min interval. Low priority. Topic convention: `arifos-<hostname>-heartbeat`.

## Mesh Networking Cross-Reference

For multi-machine federation (Tailscale, Headscale, AXL), see `federation-mesh-networking` skill. Dead-man's switch works per-machine. Cross-machine health extends with Tailscale ping + federation heartbeat.

## Mesh Networking (Tailscale/Headscale)

For multi-machine federation, Tailscale provides P2P mesh networking via WireGuard. Key decision: hosted Tailscale (fast, third-party dependency) vs Headscale (self-hosted, full sovereignty).

For arifOS federation: **Headscale on af-forge** — consistent with sovereignty-first governance. See `references/tailscale-headscale-federation.md` for full decision framework, architecture mapping, and node onboarding automation.

See `references/headscale-installation.md` for install procedure, CLI quirks (v0.29.2 changes), and port conflict resolution.

## References

- `references/blindspot-analysis-methodology.md` — structured review pattern for autonomous system blindspots
- `references/tier1-implementation.md` — Full implementation from 2026-07-12 session (files, configs, exact commands)
- `references/gemini-external-claim-audit.md` — Pattern for auditing inflated external AI claims
- `references/cross-vps-ssh-federation.md` — Bidirectional SSH setup between two Hermes agent VPSes for cross-federation auditing
- `references/cross-vps-ordered-fix-execution.md` — Pattern for executing ordered fixes across multiple VPSes with per-fix status reporting (probe→fix→verify→report)
- `references/srv1642546-dossier.md` — Azwa's VPS profile (hardware, services, issues found 2026-07-12)
- `references/headscale-installation.md` — Headscale install on Ubuntu, CLI v0.29.2 quirks, port conflicts
- `references/tailscale-headscale-federation.md` — P2P mesh networking for agentic federation, hosted vs self-hosted decision
- `references/python-package-conflict-recovery.md` — Fix pip namespace conflicts (fastmcp + fastmcp-slim, etc.) with uv uninstall → reinstall recipe
