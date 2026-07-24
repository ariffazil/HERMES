---
name: vps-agentic-ops
description: "Autonomous VPS operations — smoketest, state machine, circuit breaker, rollback, dead-man's switch, cross-federation mesh. Covers designing and deploying active response layers on VPS machines for agentic infrastructure."
version: 1.0.0
author: Hermes Agent
tags: [vps, agentic, monitoring, self-heal, federation, headscale, tailscale, active-response]
triggers:
  - "vps monitoring"
  - "active response"
  - "self-healing"
  - "circuit breaker"
  - "dead man's switch"
  - "headscale install"
  - "federation mesh"
  - "smoketest"
  - "state machine vps"
  - "autonomous ops"
---

# VPS Agentic Operations

Design and deploy autonomous monitoring, alerting, auto-healing, and federation infrastructure on VPS machines. For agentic systems where agents manage infrastructure without human intervention.

## When to Use

- Building active response layers for VPS (smoketest → state machine → circuit breaker → rollback)
- Setting up cross-VPS federation (SSH, Headscale/Tailscale mesh)
- Designing dead-man's switches and heartbeat monitors
- Diagnosing resource starvation (swap thrashing, zombie sessions, load spikes)
- Hardening VPS security (UFW, port management, SSH key management)

## When NOT to Use

- Simple uptime monitoring (use UptimeRobot/cron)
- Application-level health checks (use /health endpoints)
- Cloud provider managed services (use AWS/GCP native monitoring)

## Procedure

### Phase 1: Diagnose Before Building

**RULE: Always probe live state before proposing fixes.**

1. Run `journalctl -p 3 -n 50` and `dmesg | grep -iE 'error|fail|oom|kill'` — targeted error logs, not inventory dumps
2. Check `free -h`, `df -h /`, `cat /proc/loadavg` — resource state
3. Run `ss -tlnp` — listening ports and processes
4. Run `systemctl list-units --failed` — failed services
5. Check `ps aux | awk '{print $1}' | sort | uniq -c | sort -nr | head -10` — process distribution by user

**PITFALL:** Do NOT run `apt list`, `pip list`, `docker ps` as first actions. These are inventory dumps with zero information gain. Targeted error logs > inventory dumps.

### Phase 2: Design the Active Response Layer

#### 2.1 Smoketest Design

**Dependency-free shell script.** No Python, no Node, no external dependencies. If the script itself can't run, the system is already dead.

```bash
#!/bin/bash
# Exit codes: 0=PASS, 1=DEGRADED, 2=CRITICAL
set -euo pipefail

SVC="${1:-default-service}"
URL="${2:-http://127.0.0.1:PORT/health}"

FAIL=0

# Service is active
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"
  exit 1
fi

# Health endpoint responds with content validation
if [ -n "$URL" ]; then
  RESPONSE=$(curl -sf --max-time 5 "$URL" 2>/dev/null || echo "FAIL")
  if echo "$RESPONSE" | grep -q "FAIL"; then
    echo "FAIL: $URL unreachable"
    ((FAIL++))
  fi
  # Content validation — don't just check HTTP 200
  if ! echo "$RESPONSE" | grep -qE '"status":"ok"|"healthy"'; then
    echo "WARN: $URL returned unexpected content"
    ((FAIL++))
  fi
fi

# VPS vitals
RAM_PCT=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
DISK_PCT=$(df / | awk 'NR==2 {gsub(/%/,""); print $5}')
[ "$RAM_PCT" -gt 85 ] && echo "WARN: RAM ${RAM_PCT}%" && ((FAIL++))
[ "$DISK_PCT" -gt 90 ] && echo "WARN: Disk ${DISK_PCT}%" && ((FAIL++))

[ "$FAIL" -eq 0 ] && exit 0
[ "$FAIL" -le 2 ] && exit 1
exit 2
```

**Key principles:**
- Content validation > HTTP status (Blindspot #3: "Semantic Gap")
- Default args for service and URL (so it works without arguments)
- Exit codes are discrete: 0=healthy, 1=degraded, 2=critical

#### 2.2 State Machine Design

```
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

**Decision logic:**
- Exit 1, recovers within 300s → **Transient** (log + continue)
- Exit 1, 3 consecutive checks → **Hard** (trigger rollback)
- Exit 2 (any check) → **Hard** (immediate rollback)
- Exit 2 after rollback → **Critical** (888_HOLD)

**State file:** `/var/lib/arifos/vps-health-state.json` (persistent, survives reboot)

```json
{
  "state": "IDLE",
  "last_update": "2026-07-12T10:50:41+00:00",
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

**PITFALL:** State file location must be persistent (`/var/lib/` not `/run/`). `/run` is tmpfs — lost on reboot. (Blindspot #4: "Flag Persistence")

#### 2.3 Circuit Breaker Design

**RETRY_BUDGET:** Max 5 rollbacks per hour. After that, hard 888_HOLD regardless of smoketest result.

Without this, a buggy rollback config creates infinite restart-write loop → disk death spiral.

```bash
HOUR_ROLLBACKS=$(jq '.services."'"$SVC"'".hour_rollbacks' "$STATE_FILE")
if [ "$HOUR_ROLLBACKS" -ge 5 ]; then
  echo "888_HOLD: RETRY_BUDGET exhausted"
  echo "LOCKED" > /var/lib/arifos/agi_mode
  exit 2
fi
```

#### 2.4 Rollback Logic

**Pre-rollback validation (mandatory):**
```bash
# For systemd service files
systemd-analyze verify "$SERVICE_FILE.bak" || { echo "888_HOLD: .bak invalid"; exit 2; }

# For shell scripts
bash -n "$SCRIPT.bak" || { echo "888_HOLD: .bak has syntax errors"; exit 2; }
```

**PITFALL:** Never restore `.bak` without validating it first. If `.bak` is corrupted, rollback restores broken state → loop. (Arif's blindspot: "Integrity Guard")

**Rollback sequence:**
1. Pre-rollback log snapshot → `/var/lib/arifos/log-snapshot-*.log`
2. Validate `.bak` file
3. Restore `.bak`
4. `systemctl daemon-reload && systemctl restart $SERVICE`
5. Verify with smoketest
6. If fail → increment rollback counter → retry (max 3)

#### 2.5 BOOT_GRACE Period

**Problem:** On reboot, 22 MCP servers need >300s to boot. Watchdog fires at 60s → false 888_HOLD.

**Fix:** `OnBootSec=360` in systemd timer — 6 minute grace after boot before sensor starts judging.

```ini
[Timer]
OnBootSec=360
OnUnitActiveSec=60
```

**PITFALL:** Without BOOT_GRACE, every reboot triggers false alarm. The watchdog reads FAIL because servers haven't finished booting, not because they're broken.

#### 2.6 Dead-Man's Switch

**Simplest approach:** Cron heartbeat that delivers to Telegram. If it stops firing → you notice the silence.

```bash
#!/bin/bash
# /usr/local/bin/deadman-heartbeat.sh
UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | awk '{print $1}')
DISK=$(df / | awk 'NR==2 {print 5}')
RAM=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
echo "🫀 heartbeat: up=$UPTIME load=$LOAD disk=$DISK ram=$RAM"
```

**PITFALL:** ntfy.sh's `X-Min-Schedule` is NOT a true dead-man's switch. It's scheduled delivery, not outage detection. Use cron + Telegram delivery for real DMS.

### Phase 3: Deploy

1. Write smoketest → `/usr/local/bin/t1-smoketest.sh`
2. Write watchdog → `/usr/local/bin/vps-watchdog.sh`
3. Create systemd service + timer → `/etc/systemd/system/vps-t1-check.{service,timer}`
4. `systemctl daemon-reload && systemctl enable --now vps-t1-check.timer`
5. Verify: `systemctl status vps-t1-check.timer` + first tick in journal

**PITFALL:** After writing timer files, you MUST run `systemctl daemon-reload`. Without it, systemd doesn't register the new timer. (AGI missed this — timer existed on disk but wasn't running.)

### Phase 4: Cross-VPS Federation

#### SSH Key Exchange

```bash
# On source VPS
ssh-keygen -t ed25519 -f ~/.ssh/target-forge -N "" -C "source@target"
cat ~/.ssh/target-forge.pub  # → send to target operator

# On target VPS
echo 'ssh-ed25519 AAAA...' >> ~/.ssh/authorized_keys

# Verify
ssh -i ~/.ssh/target-forge -p PORT root@TARGET_IP "hostname && echo READY"
```

**PITFALL:** Do NOT transfer private SSH keys between VPS. Keys stay on their origin machine. (AGI tried `scp ~/.ssh/id_ed25519` — blocked.)

#### Headscale Installation (Self-Hosted Tailscale)

**Ubuntu/Debian:**
```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')

# Download .deb
curl -fsSL -o /tmp/headscale.deb "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_amd64.deb"
dpkg -i /tmp/headscale.deb
```

**Pitfalls discovered during installation:**

1. **Install script 404:** `curl https://headscale.net/install.sh | sh` returns 404. Use .deb package from GitHub releases instead.

2. **CLI syntax changed in v0.29.2:** `namespaces` → `users`. `headscale namespaces create X` fails. Use `headscale users create X`.

3. **User ID for preauth keys:** `headscale -u arifos-federation preauthkeys create` fails with "invalid argument". Use numeric user ID: `headscale -u 1 preauthkeys create`.

4. **IPv6 detection:** `curl -s ifconfig.me` may return IPv6 on dual-stack VPS. Use `curl -4 -s ifconfig.me` for IPv4.

5. **Port conflicts:** Multiple Headscale services (metrics, grpc, stun) default to same port. Disable or assign different ports:
   ```yaml
   # /etc/headscale/config.yaml
   listen_addr: 0.0.0.0:9080
   # metrics_listen_addr: 0.0.0.0:9091  # comment out or different port
   # grpc_listen_addr: 0.0.0.0:50443    # comment out or different port
   stun_listen_addr: 0.0.0.0:3478       # different port
   ```

6. **Hosted Tailscale coexistence:** If VPS already has hosted Tailscale (`tailscale status` shows `arifbfazil@`), you can't simply `tailscale up --login-server=headscale`. Need to disconnect from hosted first or run dual instances with separate sockets.

**Tag-based ACLs for federation:**
```json
{
  "tagOwners": {
    "tag:forge-node": ["group:admins"],
    "tag:wawabot-node": ["group:admins"],
    "tag:aaa-node": ["group:admins"],
    "tag:organ-node": ["group:admins"]
  },
  "acls": [
    { "action": "accept", "src": ["tag:forge-node"], "dst": ["tag:forge-node:*"] },
    { "action": "accept", "src": ["tag:wawabot-node"], "dst": ["tag:forge-node:22,8080,8088"] },
    { "action": "accept", "src": ["group:admins"], "dst": ["tag:*:22"] }
  ]
}
```

### Pitfalls (Lessons Learned)

| Pitfall | What Happened | Fix |
|---|---|---|
| **AGI tunnel vision** | AGI ignored 4 priority redirections, built dashboard while timer wasn't running | Rule: verify infra BEFORE UI. "Dashboard on dead timer = pretty lie" |
| **AGI verification loop** | AGI ran same health check 10+ times in a row | Detect consecutive identical commands, cap at 3, force task switch |
| **Naming inconsistency** | Timer named `vps-t1-check` but code referenced `vps-watchdog` | Use consistent naming across all files |
| **Missing daemon-reload** | Timer file existed but systemd didn't register it | Always `systemctl daemon-reload` after writing service/timer files |
| **False 888_HOLD on boot** | Watchdog fired before servers finished booting | Add `OnBootSec=360` grace period |
| **State file on tmpfs** | `/run/arifos/` lost on reboot | Use `/var/lib/arifos/` (persistent) |
| **HTTP 200 ≠ healthy** | Service responded 200 but returned garbage data | Content validation — grep for "healthy" in response |
| **SSH key transfer** | AGI tried to SCP private key to remote VPS | Never transfer private keys. Generate on origin, share public key only |
| **IPv6 detection** | `curl ifconfig.me` returned IPv6 | Use `curl -4 -s ifconfig.me` for IPv4 |
| **Port conflicts** | Multiple Headscale services defaulting to same port | Disable unused services or assign unique ports |

### References

- `references/headscale-install.md` — Detailed Headscale installation guide with pitfall solutions
- `references/active-response-layer.md` — Full implementation of smoketest + state machine + circuit breaker

### Templates

- `templates/vps-smoketest.sh` — Dependency-free smoketest template
- `templates/vps-watchdog.sh` — State machine + circuit breaker + rollback template
- `templates/deadman-heartbeat.sh` — Heartbeat cron template

### Scripts

- `scripts/vps-health-check.sh` — Quick VPS health probe (RAM, disk, load, services)
