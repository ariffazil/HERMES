---
name: agentic-infrastructure-ops
description: "Self-healing VPS infrastructure, multi-VPS federation, Headscale mesh networking, watchdog state machines, and agent-managed node onboarding. When the user asks to 'fix and zen' VPSes, set up federation, install Headscale/Tailscale, build watchdogs, or onboard new nodes to the arifOS mesh."
version: 1.0.0
author: Hermes Agent
tags: [devops, federation, headscale, tailscale, watchdog, self-healing, multi-vps, mesh]
triggers:
  - "fix and zen"
  - "set up federation"
  - "install headscale"
  - "install tailscale"
  - "onboard node"
  - "add node"
  - "self-healing"
  - "watchdog"
  - "headsacle"
  - "mesh network"
  - "VPS hardening"
---

# Agentic Infrastructure Operations

Self-healing VPS infrastructure with agent-managed operations. Covers watchdog state machines, multi-VPS federation via SSH + Headscale mesh, and autonomous node onboarding.

## Core Principles

- **Infra before UI.** Always verify timers, state files, and logs BEFORE building dashboards or visualisation. "Dashboard on dead timer = pretty lie."
- **888_OVERRIDE = halt immediately.** When ASI issues an override, AGI stops all work. No exceptions.
- **Additive, not replacing.** New infrastructure layers (Tailscale, Headscale) sit alongside existing ones (SSH, UFW). Never remove the fallback path.
- **Agent-managed onboarding.** Arif says "add node" → agents handle install, auth, verify, notify. 10 seconds of human involvement, everything else is agent territory.

## Self-Healing Watchdog Architecture

### State Machine (4 states)

```
         ┌──────────┐
    ┌───→│ HEALTHY  │←───┐
    │    └────┬─────┘    │
    │         │ exit 1    │ recovery (300s)
    │         ▼          │
    │    ┌──────────┐    │
    │    │ DEGRADED │────┘
    │    └────┬─────┘
    │         │ consecutive ≥ 3  OR  exit 2  OR  no recovery in 300s
    │         ▼
    │    ┌──────────┐
    │    │ CRITICAL │──── auto-rollback triggered
    │    └────┬─────┘
    │         │ rollback fails (3 attempts)
    │         ▼
    │    ┌──────────┐
    └────│   DEAD   │──── 888_HOLD → Hermes stops AGI → notify Arif
         └──────────┘
```

### Smoketest Design

- Pure shell, dependency-free, <3s execution
- Exit codes: 0=PASS, 1=DEGRADED, 2=CRITICAL
- Validate response content (grep for "healthy"/"ok"), not just HTTP 200
- Default arguments so it works without arguments

### BOOT_GRACE Period

**Critical:** After reboot, MCP servers need >300s to boot. Without BOOT_GRACE, watchdog triggers false 888_HOLD.

```ini
# /etc/systemd/system/vps-t1-check.timer
[Timer]
OnBootSec=360      # 6 min grace after boot
OnUnitActiveSec=60 # then every 60s
```

### Pre-Rollback Validation

Never restore `.bak` without validation:
- Service files: `systemd-analyze verify /path/to/file.bak`
- Shell scripts: `bash -n /path/to/script.bak`
- Invalid backup → skip rollback → 888_HOLD directly

### Circuit Breaker (RETRY_BUDGET)

Max 5 rollbacks per hour → hard 888_HOLD. Prevents infinite restart-write loops.

### Dead-Man's Switch

Heartbeat cron that reports to Telegram. If it stops firing, the silence IS the alert.

```bash
#!/bin/bash
# /usr/local/bin/deadman-heartbeat.sh
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | awk '{print $1}')
DISK=$(df / | awk 'NR==2 {print 5}')
RAM=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
echo "🫀 af-forge heartbeat: up=$UPTIME load=$LOAD disk=$DISK ram=$RAM"
```

## Multi-VPS Federation

### SSH Federation (Immediate)

Bidirectional SSH with Ed25519 keys. Each direction has a comment-identified key:
- `wawabot@srv1642546→af-forge`
- `arif-forge-push` (af-forge → srv1642546)

### Headscale (Sovereign Mesh)

Self-hosted Tailscale coordination server. See `references/headscale-install.md` for full installation guide.

**Why Headscale over hosted Tailscale:**
- Coordination plane on your own VPS — no third-party sees your network map
- Consistent with arifOS sovereignty-first design
- Same Tailscale client UX — nodes don't know the difference

### Tag-Based ACLs

```json
{
  "tagOwners": {
    "tag:forge-node": ["group:admins"],
    "tag:wawabot-node": ["group:admins"],
    "tag:organ-node": ["group:admins"]
  },
  "acls": [
    { "action": "accept", "src": ["tag:forge-node"], "dst": ["tag:forge-node:*"] },
    { "action": "accept", "src": ["tag:wawabot-node"], "dst": ["tag:forge-node:22,8088,7071"] },
    { "action": "accept", "src": ["tag:organ-node"], "dst": ["tag:forge-node:8081,18082,18083"] }
  ]
}
```

## Agent-Managed Node Onboarding

| Step | Who | What |
|---|---|---|
| Node appears | Arif | Give IP + purpose (10 seconds) |
| SSH bootstrap | Arif | Add key to authorized_keys |
| Install + join | AGI | `tailscale up --login-server=... --authkey=...` |
| Mesh verify | AGI | `ping <new>.ts.net` |
| Health check | ASI | Smoketest + Tier 1 validation |
| Notification | ASI | "Node X live, federated" |
| Ongoing | Agents | Self-heal, monitor, report only failures |

## Pitfalls

- **AGI tunnel vision.** AGI tends to jump to visualisation/dashboard before verifying infrastructure. Always enforce "infra before UI" sequence.
- **Port conflicts on Ubuntu 25.10+.** Headscale defaults conflict with existing services. Check `ss -tlnp` before binding. Use alternative ports (9080 instead of 8080).
- **IPv4 vs IPv6.** `curl ifconfig.me` may return IPv6 on dual-stack VPS. Force IPv4: `curl -4 -s ifconfig.me`.
- **Hosted Tailscale coexistence.** If VPS already has hosted Tailscale, `tailscale up --login-server=...` may fail. Need `--reset` flag or disconnect from hosted first.
- **SSH key transfer.** NEVER transfer private SSH keys between machines. Each node generates its own keypair.
- **vault.env + `set -u` = silent crash.** Launcher scripts with `set -euo pipefail` that source vault.env will crash on any unescaped `$` in password hashes (Apache `$apr1$`, bcrypt `$2a$`, SHA `$5$`). The service appears to "just not start" — journalctl shows `line NNN: <var>: unbound variable`. Fix: escape with `\$`. Both vault.env AND vault.flat.env must be checked. See vps-operations `references/systemd-service-crash-diagnosis.md`.
- **systemd timer naming.** Use consistent naming (`vps-t1-check.timer` not `vps-watchdog.timer`). Mismatch between timer name and what you search for causes "could not be found" errors.

## Federation Node CLI Tools

Building Python CLIs for node management (health, exec, sync). Key patterns:
- Per-node SSH port discovery (FORGE=22888, FLOW=22) — never assume port 22
- Local host detection to avoid slow SSH loopback
- SCP sync requires `mkdir -p` on remote first
- Health probe priority: HTTP `/health` on organ ports → SSH echo → local shortcut

Full patterns + code snippets: `references/federation-node-cli-patterns.md`

## References

- `references/headscale-install.md` — Full Headscale installation on Ubuntu 25.10+
- `references/watchdog-state-machine.md` — Complete smoketest + state machine implementation
- `references/federation-acl-policy.md` — Tag-based ACL patterns for arifOS organs
- `references/federation-node-cli-patterns.md` — Python CLI patterns for federation node management
