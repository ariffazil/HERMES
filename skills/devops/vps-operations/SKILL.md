---
name: vps-operations
description: "VPS optimization, cleanup, and health auditing. Diagnose resource hogs, clean stale artifacts, reclaim disk/RAM, audit services and containers"
version: 1.1.0
author: Hermes Agent
updated: 2026-07-16
tags: [vps, optimization, cleanup, health, devops, infrastructure, system-admin]
triggers:
  - "optimize the machine"
  - "clean up the VPS"
  - "what's eating resources"
  - "system health check"
  - "zen the VPS"
  - "remove chaos"
  - "disk full"
  - "memory high"
  - "out of swap"
---

# VPS Operations

Systematic VPS health auditing, cleanup, and optimization. Not a one-liner `df -h` — a structured diagnostic that finds the real problems and fixes them in order of impact.

## When to Use

- User says "optimize the machine" or "clean up the VPS"
- System is slow, disk is full, memory is high
- Periodic health audits (monthly recommended)
- After deploying new services (check for resource conflicts)

## When NOT to Use

- Specific service debugging → use the relevant organ skill
- Security audit → use `telegram-security-audit` or `infra-guardian`
- Configuration changes → use the relevant config skill

## Procedure

### Phase 1: Recon (parallel — 4 probes max)

Run these concurrently. Never serialize independent probes.

```bash
# 1. Disk + memory + CPU
df -h / && free -h && uptime

# 2. Top resource consumers (memory + CPU)
ps aux --sort=-%mem | head -15
ps aux --sort=-%cpu | head -10

# 3. Docker state
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Size}}"
docker system df

# 4. Services + ports
systemctl --failed
ss -tlnp | head -30
```

### Phase 2: Deep dive (targeted — based on Phase 1 signals)

| Signal | Investigate | Command |
|---|---|---|
| High memory (>80%) | Top RSS processes | `ps aux --sort=-%mem \| head -20` |
| High swap (>5GB) | Stuck/defunct processes | `ps -eo pid,ppid,etime,comm,%mem --sort=-%mem` |
| Disk >80% | Large directories | `du -sh /root/*/ /var/*/ /tmp/ 2>/dev/null \| sort -rh \| head -20` |
| Docker bloat | Orphaned volumes + images | `docker volume ls -q --filter dangling=true` |
| High load | Zombie/defunct processes | `ps aux \| grep -E 'Z\|defunct'` |
| Load >50 on 8 cores | **OOM death spiral** | See OOM Death Spiral below |
| OOM killer in journal | Stuck process + cascade | `journalctl --since "1h" \| grep -i oom-kill` |
| Stale sessions | Old PTY/SSH sessions | `who` + `ps -eo pid,etime,comm \| grep -E 'ssh\|pts'` |

### Phase 3: Cleanup (ordered by impact)

**🔴 Critical (kill first):**
1. Stuck processes eating >20% RAM — kill them
2. OOM-adjacent processes — kill or restart with limits

**🟠 High (reclaim disk):**
3. `/tmp` pip caches — `rm -rf /tmp/pip-unpack-* /tmp/pip-build-env-*`
4. Snap old revisions — `snap list --all | awk '/disabled/{print $1, $3}' | while read name rev; do snap remove "$name" --revision="$rev"; done`
5. Apt cache — `apt-get clean`
6. Old kernels — `apt-get remove -y linux-image-<old-version>`
7. Journal logs — `journalctl --vacuum-size=50M`
8. Duplicate repos — compare commits, quarantine to `~/.quarantine-YYYY-MM-DD/`

**🟡 Medium (RAM recovery):**
9. Multiple instances of same process (e.g., 2× kimi-code) — kill older
10. Hermes gateway duplicates — see `references/hermes-gateway-duplicates.md` for detection, telemetry capture, canonical PID verification, and the restart race condition pitfall
11. Orphaned Docker volumes — `docker volume prune -f`
11. Stale tsserver/pyright (IDE servers from killed editors) — kill by PID

**🟢 Low (housekeeping):**
12. Docker build cache — `docker builder prune -f`
13. Large log files — truncate or rotate
14. Old backup files — review and archive

### Phase 4: Report

Always report in this structure:

| Item | Before | After | Freed |
|---|---|---|---|
| RAM (stuck pytest) | 25GB used | 15GB used | **10GB** |
| /tmp pip caches | 4.5GB | 4.0GB | 500MB |
| ... | ... | ... | ... |

End with: **Total freed: XGB RAM + YGB disk**

## OOM Death Spiral — Diagnostic Pattern

When the OOM killer fires, it's rarely a single process problem. It's a **cascade**:

```
Stuck process (e.g., grok at 93% CPU for 22h)
  → Memory exhausted (30Gi/31Gi used)
    → Swap fills (12Gi/35Gi)
      → OOM killer fires
        → Kills service processes (openclaw, graphiti)
          → systemd restarts them
            → They need memory again
              → OOM kills again
                → Load average 50-200x on 8 cores
```

### Diagnosis Steps

```bash
# 1. Confirm OOM pattern
journalctl --since "1h" | grep -i "oom-kill\|killed by the OOM"
# If you see "A process of this unit has been killed by the OOM killer" → cascade active

# 2. Find the stuck process (the SOURCE, not the victims)
ps aux --sort=-%cpu | head -5
# Look for: >50% CPU, running for hours/days, single process
# Common culprits: grok, kimi-code, opencode, pytest, ollama runner

# 3. Verify it's stuck (not just busy)
ps -eo pid,etime,%cpu,%mem,comm | sort -k3 -rn | head -5
# A process at 93% CPU for 22 hours is stuck. A process at 93% for 2 minutes is busy.

# 4. Check memory state
free -h
# If Mem: 415MB free and Swap: 12GB used → system is thrashing
```

### Fix Order

1. **Kill the stuck source process FIRST** — this is the root cause, not the OOM victims
2. Wait 30 seconds for memory to reclaim
3. Check if OOM-killed services auto-recovered (they usually do via systemd)
4. If services didn't recover: `systemctl restart <service>`
5. Verify load drops: `uptime` — should go from 50+ to single digits within 2 minutes

### Pitfall: Killing the victims instead of the source

If you restart openclaw-gateway without killing the stuck grok process, the gateway will just get OOM-killed again. **Always find and kill the source first.** The victims are symptoms, not causes.

### Pitfall: "Everything looks green" while in OOM spiral

Services may report healthy on their /health endpoints even while the system is thrashing. The health check passes because the service *just* restarted, but it'll be killed again within minutes. Check `journalctl` for OOM-kill events — that's the ground truth.

### Common Stuck Processes (arifOS federation)

| Process | Normal CPU | Stuck When | Kill Command |
|---|---|---|---|
| grok | 5-20% | >80% for >30min | `kill <pid>` |
| kimi-code | 10-30% | >50% for >1h, multiple instances | `kill <pid>` (keep newest) |
| opencode | 5-15% | Multiple instances, >40% each | Kill older: `kill $(pgrep -o opencode)` |
| ollama runner | 20-60% | >80% for >1h | `kill <runner-pid>` (not ollama serve) |
| pytest | 5-20% | >2GB RSS, D state | `kill -9 <pid>` |

## systemd Service Crash-Loop Diagnosis

When a service exits in <100ms with exit-code 1, the problem is almost always the environment, not the application. See `references/systemd-service-crash-diagnosis.md` for the full flow.

**Most common cause:** Unescaped `$` in password hashes inside env files sourced with `set -euo pipefail`. Apache `$apr1$`, bcrypt `$2a$`, SHA `$5$`/`$6$` — bash interprets them as variables, `set -u` kills the process.

```bash
# Diagnosis:
journalctl -u <service> --since "1h" | tail -10
# Look for: "line NNN: <var>: unbound variable"

# Fix: escape dollar signs
sed -i 's|\$apr1\\$|\\$apr1\\$|g' /path/to/env/file
```

**Pitfall:** Both `vault.env` AND `vault.flat.env` may have the same bad line. Fix the source, then regenerate.

**Creating a systemd unit that needs vault.env secrets:** See `references/systemd-service-with-secrets.md` — the `ExecStart` bash-wrapper pattern, why `EnvironmentFile` doesn't work with shell-export syntax, and the "gateway cannot self-restart" pitfall.

## Pitfalls

- **Don't forget `systemctl daemon-reload` after editing unit files.** Edited systemd unit files are cached in memory. A `systemctl restart` without `daemon-reload` applies the stale cached version. Symptoms: `systemctl show <service> -p <property>` shows the OLD value despite the file being correct on disk. Fix: `systemctl daemon-reload` then `systemctl restart <service>`. Proven 2026-07-24: gateway `TimeoutStopUSec` showed 90s despite unit file having 210s — daemon-reload had not been run after the unit edit.
- **Systemd dependency chain → full reboot (proven 2026-07-23).** If a service has a tight coupling (BindsTo/PartOf) to network.target or similar, its failure cascades into a full system reboot. The chain: gateway couldn't clean MCP sessions → exit code 1 → network.target stopped → reboot. Prevention: audit `systemctl show <service>` for `BindsTo=` and `PartOf=` that trace to `network.target` or `basic.target`. A service failure should only restart the service, not the machine.
- **Don't kill Docker bridge interfaces.** `docker0` and `br-*` are live container networking. Only remove interfaces that have no containers attached.
- **Don't quarantine without comparing commits.** Two directories with the same name might be different branches. `git log --oneline -1` on both before quarantining.
- **Don't blindly remove snap packages.** Only remove `disabled` (old) revisions. Active revisions are in use.
- **Swap usage after killing a hog takes time to decay.** Don't panic if swap doesn't drop immediately — the kernel reclaims it lazily.
- **Never `rm -rf` a git repo.** Always move to quarantine: `mv /root/repo /root/.quarantine-YYYY-MM-DD/repo`. User can verify before permanent deletion.
- **Parallel probes, serial fixes.** Recon is concurrent. Cleanup is ordered — critical first, then high, then medium. Don't skip the ordering.
- **Agent session death → orphan cascade (proven 2026-07-23).** When agent sessions (OpenCode, Kimi, Hermes) die without cleanup, their spawned MCP child processes (github-mcp-server, browser, kimi-code, pytest) survive as orphans. These stack up silently: 3× github-mcp-server at 58% CPU each, kimi-code at 25%, stale browser at 75%. Total: 200%+ wasted CPU. Detection: `ps aux --sort=-%cpu | head -15` — look for `github-mcp-server`, `kimi-code`, `MainThr+` with PPID=1. Fix: `kill -9 <pid>` for all orphans, no service impact. Root fix: session-cleanup hook that kills children when parent exits — not yet implemented.
- **Hermes gateway restart race (proven 2026-07-31).** Killing a stopped (`T` state) orphan gateway can trigger the restart mechanism to spawn a NEW duplicate alongside the active gateway. After kill, wait 10s and re-check: `ps aux | grep "hermes gateway" | grep -v grep | wc -l` — if >1, a race occurred. Don't kill either active gateway without explicit direction. Full pattern in `references/hermes-gateway-duplicates.md`. Root cause: restart watcher sees the dead sibling removed and fires a restart, but the active gateway was never down.
- **Boot storm after systemd cascade reboot (proven 2026-07-23).** When a service failure cascades to a full VPS reboot (see systemd dependency chain pitfall), all services fire up simultaneously. This creates a transient 1-minute load spike of 11+: `uptime` shows 1 min, load 11.46, service processes all starting. This is NOT a problem — it's normal boot contention. Load decays to single digits within 2-3 minutes as services finish init. Detection: check `uptime` — if 1m load is high but 5m is <50% of it and uptime is <5 min, it's a boot storm. Fix: none needed. Do NOT investigate processes during this window — they'll look busy because they are starting.

## arifOS Event-Loop Hang — Two Failure Modes

The symptom is identical in both modes: arifOS accepts TCP connections on port 8088 but `/health` serves zero bytes and eventually times out. **Always distinguish between the two root causes before acting** — the wrong fix wastes time or makes things worse.

### Quick Differentiator

```bash
journalctl -u arifos --since "10 min ago" | grep -iE '401|unauthorized|invalid api key|model_not_found|reasoning backend timeout|unreachable|too slow'
# Mode A = 401 / "invalid api key" / "No available channel"
# Mode B = "Reasoning backend timeout" / "unreachable" / "too slow"
```

| Signal | Mode A (Dead Key) | Mode B (Backend Timeout) |
|--------|-------------------|--------------------------|
| Journal pattern | `401` / `invalid api key` | `Reasoning backend timeout` / `unreachable` |
| Memory | Normal | Normal |
| Other organs affected? | Only arifOS | Downstream organs (GEOX) report `arifOS unreachable: ReadTimeout` |
| Fix | Replace API key | Restart arifOS + restart reasoning backend |
| Permanent resolution | Replace dead key | Fix backend connectivity or timeout config |

### Failure Mode A: Dead LLM API Key (proven 2026-07-24)

**Root cause** is a stale/expired/revoked LLM API key. The TokenRouter tries the key, gets a 401/403, and the asyncio event loop blocks waiting for a response that never comes.

#### The Chain

```
Dead API key (e.g., MiniMax M3 401: "invalid api key")
  → TokenRouter tries the key → 401
  → Client retries → more requests queue waiting for LLM
  → asyncio event loop blocks (waiting for response that never comes)
  → /health stops responding (accepts TCP connection, serves nothing)
  → systemd hits TimeoutStopSec → kills process
  → "Failed with result 'timeout'"
  → systemd auto-restarts → fresh cycle → same problem
```

#### Diagnosis

```bash
# 1. Confirm the hang pattern
curl -v --max-time 5 http://localhost:8088/health 2>&1 | tail -5
# Expect: "Connected to localhost port 8088" then "Operation timed out... 0 bytes received"

# 2. Process is running fine otherwise
systemctl status arifos --no-pager | grep Active
# Shows: "active (running) since..." — memory normal (200-400MB), not OOM

# 3. Find the dead key in journal
journalctl -u arifos --since "5 min ago" | grep -iE '401|unauthorized|invalid api key|model_not_found'
# Key lines: "TokenRouter HTTP 401: invalid api key" or "TokenRouter HTTP 503: No available channel"

# 4. Check arifOS model config
grep -r 'provider_key\|model_id' /opt/arifos/app/config/PROFILES/vps_main_arifos.json
# Shows which provider + model arifOS routes through
# Secret source: vault.env → secret-registry.yaml → MINIMAX_API_KEY
```

#### Differentiating from OOM Death Spiral

| Symptom | API Key Death Hang | OOM Death Spiral |
|---------|-------------------|------------------|
| Memory | Normal (200-400MB) | Near cap (1.5GB+) |
| Process state | Accepts TCP, no HTTP response | May show D state |
| Journal hits | `401` / `503` from TokenRouter | `oom-kill` events |
| System load | Normal or slightly elevated | Very high (50+) |
| Other services | Only arifOS affected | Most services degraded |
| Process CPU | Idle or low | A stuck process at 80%+ |

#### Fix

```bash
# Immediate: restart arifos (temporary, will hang again on next LLM call)
systemctl restart arifos && sleep 12 && curl -sf http://localhost:8088/health

# Root: replace the dead API key OR swap the model provider:
# Option A — Renew the dead key in vault.env
# Option B — Edit arifOS profile to use a working provider:
#   /opt/arifos/app/config/PROFILES/vps_main_arifos.json
#   Change: provider_key, family_key, model_id
#   Then: systemctl restart arifos
```

#### Pitfall: "Restart fixed it" is not a fix

After restart, arifOS returns `healthy` but will hang again on the next LLM call hitting the dead key. Each restart buys a few hours at most. **The dead key must be replaced or the provider changed for a permanent fix.** If you're restarting arifOS every 20-30 minutes, it's a dead key, not a memory leak.

### Failure Mode B: Reasoning Backend Timeout (proven 2026-07-29)

**Root cause** is a stuck reasoning backend (SEA-LION unreachable, Ollama CPU inference overloaded) that the `arif_think` tool calls with a timeout. The async tool call fires, the backend doesn't respond within 35s, the tool times out — but the **asyncio lock/semaphore for that resource is not released**, causing every subsequent request that needs the same resource to block forever.

This is a distinct failure mode from Mode A — no API key issue, no 401s, no credential problem.

#### The Chain

```
Reasoning backend (SEA-LION / Ollama) overloaded or unreachable
  → arif_think tool fires async call with 35s timeout
  → Backend doesn't respond → timeout fires
  → Lock/semaphore on the reasoning resource NOT released
  → All subsequent requests needing that resource block
  → /health endpoint hangs (if health check uses tool state)
  → MCP tools/list also hangs
  → Downstream organs detect: GEOX reports "arifOS unreachable: ReadTimeout"
  → Cascade: GEOX kernel_verdict → UNKNOWN → owner_summary → AMBER
```

#### Diagnosis

```bash
# 1. Confirm the hang pattern (same as Mode A)
curl -v --max-time 5 http://localhost:8088/health 2>&1 | tail -5

# 2. Check for DECEIVING "all services green" — ports LISTEN but endpoints hang
ss -tlnp | grep 8088  # Shows LISTEN
# This is NOT contradictory — the socket is alive but the event loop is stuck

# 3. Look for the timeout pattern, NOT 401s
journalctl -u arifos --since "10 min ago" | grep -iE 'reasoning backend timeout|unreachable|too slow|arif_think.*error'
# Example from 2026-07-29:
# "Tool arif_think execution error: Reasoning backend timeout after 35.0s — SEA-LION unreachable or Ollama CPU inference too slow"

# 4. Check Ollama/SEA-LION health directly
curl -m 3 -s http://127.0.0.1:11434/api/tags | head -3
# If Ollama returns models → backend IS alive, but overloaded
# If Ollama unreachable → backend is dead

# 5. Check downstream organ telemetry
# GEOX will show: "arifOS unreachable: ReadTimeout" in federation_geometry
curl -m 5 -s http://127.0.0.1:8081/health | grep -o 'arifOS unreachable[^"]*'
```

#### Differentiating from Mode A (Dead Key)

| Signal | Mode A (Dead Key) | Mode B (Backend Timeout) |
|--------|-------------------|--------------------------|
| Journal pattern | `401` / `invalid api key` | `Reasoning backend timeout` / `unreachable` / `too slow` |
| TokenRouter errors | Yes — HTTP 4xx from LLM provider | No — internal tool timeout |
| Repeat interval | Every LLM call to that model | Only when arif_think tool is called |
| GEOX connection | Independent | Shows `arifOS unreachable: ReadTimeout` |
| Ollama health | Not relevant | Shows alive (overloaded) or dead |
| Fix scope | Replace/rotate API key | Restart arifOS + fix backend overload |

#### Fix

```bash
# 1. Restart arifOS (clears the stuck lock/semaphore)
systemctl restart arifos

# 2. Verify recovery
sleep 5 && curl -m 5 -s http://127.0.0.1:8088/health | head -3

# 3. Check downstream organs auto-recover
curl -m 5 -s http://127.0.0.1:8081/health | grep -o '"federation_geometry":"[^"]*"\|owner_summary.*?color":"[^"]*"'

# 4. If Ollama is overloaded (not dead), reduce concurrent inference load:
#    Stop other services hitting Ollama, or increase Ollama timeout config

# 5. If the pattern repeats, increase arif_think timeout:
#    /opt/arifos/app/config/PROFILES/vps_main_arifos.json
#    Find: "arif_think" → change "timeout": 35 to "timeout": 60
```

#### Pitfall: Mode B requires a real restart, not just a key swap

Unlike Mode A where replacing the dead key fixes the root cause, Mode B is a code-level bug (lock not released on timeout). **A restart is the only immediate fix.** If the pattern repeats, the timeout value in the arifOS profile needs to be increased, or the reasoning backend needs dedicated compute (don't overload Ollama with concurrent requests).

#### Pitfall: "Mode B looks like Mode A" when checking from a client-only session

If you probe arifOS from a client that uses `arif_think` (e.g., this Hermes session), your probe requests hit the same stuck lock and timeout, looking like the health endpoint failed for a different reason. The only reliable differentiator is `journalctl` — check the logs before and after the timeout event. Journal entries show the exact error class.

## Reference: Common Resource Hogs

| Process | Typical RSS | Usually Stuck When |
|---|---|---|
| `pytest` | 2-11GB | Running >10 min, D state |
| `github-mcp-server` | 4-6MB per instance | 3+ orphans (dead agent sessions), 58% CPU each |
| `tsserver` | 300-700MB | Parent editor killed |
| `pyright-langserver` | 200-400MB | Parent editor killed |
| `kimi-code` | 400MB-1.2GB | Multiple instances |
| `ollama serve` | 150-500MB | Normal — don't kill |
| `netdata` | 200-300MB | Normal — don't kill |
| `grafana` | 150-200MB | Normal — don't kill |

## Part 5: Mesh Networking (Tailscale/Headscale)

When onboarding new VPS nodes or setting up cross-machine federation.

### Decision: Tailscale vs Headscale

| | Tailscale (managed) | Headscale (self-hosted) |
|---|---|---|
| Control plane | Tailscale's cloud | Your VPS |
| NAT traversal | Tailscale's DERP relays | You run your own DERP |
| Identity | Google/GitHub SSO | Local OIDC or pre-auth keys |
| Sovereignty | ❌ Trust Tailscale | ✅ Full control |
| Feature parity | Full | ~90% (some lag) |

**arifOS standard:** Headscale on af-forge (:8083 internal, `https://headscale.arif-fazil.com` public via Caddy). Tailscale clients on all nodes.

### 🔴 Pitfall: Provider Firewall Blocks Non-Standard Ports

Hostinger silently drops TCP to all ports except 22, 80, 443 — even between VPSes in the same datacenter. TCP SYN arrives at the interface but NO SYN-ACK is ever sent, and the application never logs the connection. **Rule: NEVER use raw `IP:port` for cross-VPS connections. Always route through Caddy on port 443.**

Full diagnostic pattern (tcpdump proof), wrong-blame list, and solution in: [`references/hostinger-firewall-constraints.md`](references/hostinger-firewall-constraints.md).

### Pitfall: AGI port confusion
AGI agents consistently report wrong Headscale port (9080 vs actual 8083 internal). ALWAYS verify with `ss -tlnp | grep headscale` or `cat /etc/headscale/config.yaml | grep listen_addr`. Note: 8083 is INTERNAL only — Hostinger blocks it for cross-VPS traffic. The PUBLIC endpoint is `https://headscale.arif-fazil.com` (Caddy on port 443).

### Pitfall: Hosted Tailscale conflict
If machine already on Tailscale's hosted service, switching to self-hosted Headscale forces re-auth and disconnects all existing devices. Solution: keep hosted for existing devices, Headscale for new nodes. Migrate later.

### Pitfall: SSH blocked after UFW enable
When enabling UFW remotely, ALWAYS ensure SSH is allowed FIRST. If SSH is already blocked, need console access (VPS provider dashboard).

### Node Onboarding Pattern
```bash
# On headscale server:
headscale users create <username>
headscale preauthkeys create -u <user_id> --reusable --expiration 24h --tags tag:<tagname>

# On joining machine (use Caddy-proxied HTTPS — NEVER raw IP:port):
curl -fsSL https://tailscale.com/install.sh | sh
systemctl enable --now tailscaled
tailscale up --login-server=https://headscale.arif-fazil.com --hostname=<name> --accept-routes --authkey=<key>

# Verify:
headscale nodes list
tailscale status
ping <tailscale_ip_of_other_node>
```

## Part 6: Agent Health Validation

When an agent reports "everything is green", validate against the actual health endpoint.

### The Validation Pattern
```bash
curl -sf http://127.0.0.1:<port>/health | python3 -m json.tool
# Check the fields agents skip:
# - owner_summary.color (YELLOW ≠ GREEN)
# - thermodynamic.verdict (HOLD ≠ PROCEED)
# - service_health (DEGRADED ≠ HEALTHY)
# - runtime_drift (TRUE = code mismatch)
```

### Pitfall: "Everything is green" theater
If health response contains `owner_summary.color: "YELLOW"` or `thermodynamic.verdict: "HOLD"`, system is NOT green. Agents cherry-pick green items and ignore yellow flags. Always read the full response. This is the same pattern as F9 Anti-Hantu — self-PASS theater.

## Kernel Slab Leak Diagnosis

When `free -h` shows 90%+ RAM used but `ps aux --sort=-%mem` only accounts for a few GB, the kernel slab allocator has leaked. Common on Linux 6.x with `CONFIG_RANDOM_KMALLOC_CACHES`.

### Diagnosis
```bash
# Quick check — is slab eating all RAM?
cat /proc/meminfo | grep Slab
# If Slab > 10GB on a 32GB machine, you have a leak

# Detailed breakdown
slabtop -o -s c | head -15
# Look for: kmalloc-rnd-* with >1M objects × >1KB = multi-GB leak

# Specific cache info
cat /proc/slabinfo | grep "kmalloc-rnd"
```

### The `kmalloc-rnd-12-2k` Bug (kernel 6.17)
Known kernel memory leak where `kmalloc-rnd-12-2k` grows unboundedly. On a 31GB machine, it can eat 19+ GB. No userspace fix — only `reboot` clears it.

### Mitigation (no reboot)
- Kill all non-essential services (see Anti-Hantu pattern below)
- `sync && echo 3 > /proc/sys/vm/drop_caches` — reclaims page cache but NOT slab
- Monitor with `watch -n5 'free -h | head -2'` — if available stays <1GB, reboot is inevitable

### Pitfall: Slab leak looks like OOM but isn't
OOM death spiral has a stuck source process at high CPU. Slab leak has NO stuck process — everything uses normal CPU but the machine thrashes because there's no free RAM. Different root cause, different fix.

## Anti-Hantu Cleanup Pattern (F9)

When Arif says "kill all zombies and hantu" or "anti-hantu" (F9 ANTI-HANTU), run this systematic cleanup:

### Phase 1: Zombies
```bash
ps aux | awk '$8~/Z/{print $2}' | xargs -r kill -9 2>/dev/null
```

### Phase 2: Orphan MCP Children
Agent sessions (kimi, opencode) spawn MCP child processes that survive after the parent dies. These eat hundreds of MB each.
```bash
for pid in $(ps -eo pid,ppid= | awk '$2==1{print $1}'); do
  cmd=$(cat /proc/$pid/comm 2>/dev/null)
  if echo "$cmd" | grep -qE "capability.index|chrome-devtools|sequential-thinking|brave-search|postgres-mcp|context7|playwright|megamemory|perplexity|supabase|fetch-server|exa-mcp|minimax-coding|github-mcp-server"; then
    kill -9 $pid 2>/dev/null && echo "killed orphan $pid ($cmd)"
  fi
done
```

### Phase 3: Non-Essential Services
```bash
systemctl stop ollama 2>/dev/null          # local LLM, not actively serving
systemctl stop netdata 2>/dev/null         # monitoring daemon (250MB+)
systemctl stop grafana-server 2>/dev/null  # dashboards
systemctl stop prometheus 2>/dev/null      # metrics
systemctl stop litellm-proxy 2>/dev/null   # LLM proxy (if not routing)
docker stop cadvisor 2>/dev/null           # container metrics
```

### Phase 4: Cache Drop
```bash
sync && echo 3 > /proc/sys/vm/drop_caches
```

### Pitfall: Don't kill cloudflared
Cloudflared is federation infrastructure (tunnel), not monitoring. Killing it breaks all `*.arif-fazil.com` subdomains.

### Pitfall: Distinguish systemd-managed vs session-spawned arifOS
`systemctl show arifos.service -p MainPID` gives the production kernel PID. Session-spawned `arifosmcp.runtime` from kimi/opencode are the ones to kill — check parent PID matches a kimi/opencode process.

## VPS Dossier Template

When user asks for a "full dossier" on a VPS, collect:

1. **Hardware** — hostname, OS, kernel, CPU, RAM, disk, IP, uptime
2. **Services** — all listening ports, systemd running services
3. **Docker** — containers (with images/status/ports), networks, volumes, compose files
4. **AI stack** — models (Ollama, LiteLLM), providers, fallback chains
5. **Domains** — Caddy/Nginx config, all domain blocks, Cloudflare tunnel
6. **Observability** — Prometheus, Grafana, Netdata, Jaeger, etc.
7. **Cron jobs** — system crontab + systemd timers
8. **Secrets** — where keys live, how they're sourced
9. **Known issues** — stale processes, duplicates, anomalies
