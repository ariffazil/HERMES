---
name: vps-machine-health
description: "Full VPS machine health optimization — system resource recon, memory/CPU hog identification, OS-level cleanup (apt, snap, journal, kernels, /tmp), Docker container/volume audit, service port mapping, and comprehensive dossier generation. Load when: 'optimize the machine', 'clean up the VPS', 'what's running', 'full system dossier', 'machine health', 'remove chaos', 'redundancy cleanup', 'system inventory'."
triggers:
  - optimize the machine or VPS
  - clean up chaos and redundancy
  - full system dossier or inventory
  - machine health check or audit
  - what's running on this server
  - disk or memory is full
  - VPS is slow or overloaded
---

# VPS Machine Health Optimization

## When to Use

- User asks to "optimize the machine," "remove chaos," "clean up the VPS"
- System feels slow, disk is filling, memory is exhausted
- User wants a full dossier/inventory of what's running
- Periodic hygiene (monthly recommended)

**Not for:** Directory-level cleanup of `/root` projects → use `filesystem-entropy-audit`.
This skill handles the **system level**: OS, processes, containers, packages, services, swap.

## Phase 1: Full Recon (parallel calls)

Run all four in parallel — they're independent:

### 1a. System resources
```bash
echo "=== DISK ===" && df -h / && echo && echo "=== MEMORY ===" && free -h && echo && echo "=== CPU LOAD ===" && uptime && echo && echo "=== TOP DIRS ===" && du -sh /root /var /tmp /opt /snap 2>/dev/null | sort -rh
```

### 1b. Docker state
```bash
echo "=== CONTAINERS ===" && docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Size}}" && echo && echo "=== IMAGES ===" && docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" && echo && echo "=== VOLUMES ===" && docker volume ls && echo && echo "=== DANGLING ===" && docker volume ls -q --filter dangling=true && echo && echo "=== SYSTEM DF ===" && docker system df
```

### 1c. Services & ports
```bash
echo "=== FAILED UNITS ===" && systemctl --failed && echo && echo "=== LISTENING PORTS ===" && ss -tlnp | head -40 && echo && echo "=== JOURNAL SIZE ===" && journalctl --disk-usage
```

### 1d. Process hogs
```bash
echo "=== TOP MEMORY ===" && ps aux --sort=-%mem | head -20 && echo && echo "=== TOP CPU ===" && ps aux --sort=-%cpu | head -10 && echo && echo "=== ZOMBIES ===" && ps aux | grep -E 'Z|defunct' | grep -v grep
```

## Phase 2: Deep Recon (conditional)

Based on Phase 1 findings, drill into specific waste areas:

| Signal | Command |
|---|---|
| High /snap | `snap list --all && du -sh /snap/*/` — check for old revisions |
| High /tmp | `du -sh /tmp/*/` — pip caches, node compile caches |
| High /var | `du -sh /var/log/*/` — journal, app logs |
| High apt cache | `du -sh /var/cache/apt` |
| Possible duplicates | `diff <(cd /root/A && git log --oneline -1) <(cd /root/B && git log --oneline -1)` |
| Old kernels | `dpkg -l 'linux-image-*' \| grep ^ii` |
| Swap pressure | Check if stuck processes are the cause: `ps aux --sort=-%mem \| head -5` |

## Phase 3: Execute Cleanup

**Priority order** (biggest impact first):

### 3a. Kill memory hogs
Stuck pytest, runaway builds, orphaned IDE servers eating GB:
```bash
# Identify by RSS (column 6) > 1GB
ps aux --sort=-%mem | awk '$6 > 1048576 {print $2, $11, $6/1048576 "GB"}'
kill <PID>  # gentle first
sleep 2
kill -9 <PID>  # if still alive
```

**Common hogs:** pytest with leaked fixtures, tsserver/pyright from killed editors, kimi-code duplicates, hermes sessions that didn't drain.

### 3b. Clean /tmp
```bash
rm -rf /tmp/pip-unpack-* /tmp/pip-build-env-* /tmp/claude-*
# Also check for stale node compile caches > 7 days
find /tmp -maxdepth 1 -type d -mtime +7 -exec rm -rf {} +
```

### 3c. Clean snap old revisions
```bash
snap list --all | awk '/disabled/{print $1, $3}' | while read name rev; do
  snap remove "$name" --revision="$rev"
done
```
Typical savings: 1-3GB (old gnome, mesa, google-cloud-sdk revisions).

### 3d. Clean apt cache + old kernels
```bash
apt-get clean
apt-get autoremove -y  # removes old kernels automatically
# Or manually: apt-get remove -y linux-image-X.X.X-YY-generic
```

### 3e. Trim journal
```bash
journalctl --vacuum-size=50M
```

### 3f. Docker cleanup
```bash
docker volume prune -f    # dangling volumes
docker image prune -f     # dangling images
docker builder prune -f   # build cache
# Only if containers are stopped and confirmed unneeded:
docker container prune -f
```

### 3g. Quarantine duplicate repos
```bash
Q=/root/.quarantine-$(date +%Y-%m-%d)
mkdir -p "$Q"
# Verify same commit first:
diff <(cd /root/lower && git log --oneline -1) <(cd /root/UPPER && git log --oneline -1)
mv /root/duplicate "$Q/duplicate"
```

## Phase 4: Verify & Report

```bash
echo "=== DISK AFTER ===" && df -h /
echo "=== MEMORY AFTER ===" && free -h
echo "=== SNAP AFTER ===" && du -sh /snap
```

**Report format** (for dossier):

```markdown
## Cleanup Summary
| Item | Before | After | Freed |
|---|---|---|---|
| RAM (stuck pytest) | 25GB used | 15GB used | 10GB |
| /tmp | 4.5GB | 4.0GB | 500MB |
| Snap | 8.9GB | 6.4GB | 2.5GB |
...
```

## Dossier Generation

When user asks for "full dossier" or "full system inventory", produce:

1. **Hardware & OS** — hostname, OS, kernel, CPU, RAM, disk, IP, uptime
2. **Federation organs** — port, runtime, status (curl each /health)
3. **Docker containers** — name, image, ports, status
4. **AI models & providers** — from `~/.hermes/config.yaml`
5. **Domains** — from Caddyfile domain blocks
6. **Observability stack** — prometheus, grafana, netdata, etc.
7. **Cron jobs** — `crontab -l` + `/etc/cron.d/`
8. **Secrets structure** — from `/root/.secrets/INDEX.md`
9. **Cleanup done** — what was freed this session

## Cross-VPS Dossier

When the user has multiple VPSes in a federation (e.g., af-forge + srv1642546), extend the dossier with:

10. **Cross-VPS SSH federation** — which directions are live, key fingerprints
11. **Remote VPS summary** — hostname, IP, uptime, key services on each peer
12. **Federation link health** — test both SSH directions with `ssh target "hostname && echo OK"`

This gives the user a single document covering their entire infrastructure, not just the local machine.

## Pitfalls

### Don't kill systemd-managed processes
Check if a process is managed by systemd before killing: `systemctl status <service>`. Killing a systemd-managed process just makes systemd restart it. Stop the service instead.

### Swap hogs are usually symptoms, not causes
High swap usage (10GB+) usually means a process leaked memory until the kernel swapped it out. Kill the cause (the memory hog), and swap will decay naturally. Don't `swapoff/swapon` unless you've freed physical RAM first.

### Snap cleanup can break running snaps
Only remove `disabled` revisions. Active revisions are needed by running snap services.

### Docker prune is safe for dangling only
`docker volume prune` only removes volumes not attached to any container. `docker image prune` only removes dangling images (untagged). Neither touches running containers or their data.

### Old kernel removal — always keep current + 1 fallback
Never remove the currently running kernel or the immediately previous one. Check with `uname -r` before removing.

### Check for duplicate repos BEFORE deleting
Always verify same commit (`git log --oneline -1`) and same remote (`git remote -v`) before treating two directories as duplicates. Quarantine, don't delete.

### tsserver/pyright from killed editors
When users close VS Code or kimi-code, the TypeScript language server processes often linger eating 300-700MB each. Safe to kill: `pkill -f tsserver`. They're orphaned, not serving anything.

### Process age matters more than name
A `python3` process running for 3 days with 2% memory is probably legitimate. One running for 56 minutes with 34% is almost certainly stuck. Use `etime` column (elapsed time) to distinguish.

### Stuck AI/LLM processes are the #1 cause of VPS overload
**Proven 2026-07-14:** grok process at 93% CPU for 20+ hours (1238 min CPU time) caused load average 163 on an 8-core machine. Two opencode processes at 47.9% + 19.4% CPU. Three duplicate capability_index MCP servers at 157MB each. Total: machine was drowning.

### Agent session orphans — the most common recurring pattern (proven 2026-07-19, 2026-07-23)
When agent sessions close (Hermes, OpenClaw, Kimi Code), their child processes survive as orphans. The most common culprits:
- **github-mcp-server ×3–4** — one spawned per agent session at 58% CPU each, never cleaned up
- **kimi + kimi-code** — stale subprocesses from Kimi Code sessions, 25-42% CPU each
- **stale pytest** — abandoned test runs in D-state (uninterruptible I/O), can hold 9GB+ RAM
- **MainThr+ (browser)** — orphaned Chromium/browser processes at 33-75% CPU

**Rapid detection pattern:**
```bash
top -b -n 1 -o %CPU | head -15   # The top offenders in 1 second
# Key signatures:
#   github-mcp-server stdio — 3+ instances = dead sessions
#   pytest tests/ -q — running in /root/GEOX or /root/arifOS = abandoned
#   kimi / kimi-code — no parent session = orphan
#   MainThr+ — >30% CPU, no matching session = orphan browser
```

**Fix:** `kill -9` all identified orphans in one burst. They have no parent to return to. systemd-managed services (arifos, OpenClaw, GEOX) are safe — they restart automatically if accidentally killed.

**Prevention:** This is a structural gap — nothing cleans up child processes when agent sessions die. Until a session-cleanup hook exists, the diagnostic pattern above is the fastest recovery path when load alerts fire.

**Detection pattern:**
```bash
ps aux --sort=-%cpu | head -10  # Find the offender
ps aux | grep -E 'opencode|kimi|grok|claude' | grep -v grep  # Count AI processes
ps aux | grep capability_index | grep -v grep | wc -l  # Count duplicate MCP servers
```

**Cleanup order:**
1. Kill stuck AI processes (grok, opencode, kimi) — biggest CPU impact
2. Kill duplicate MCP servers — memory savings
3. Kill zombie processes — `ps aux | awk '$8=="Z"'`
4. Drop caches — `sync && echo 3 > /proc/sysvm/drop_caches`
5. Remove stale cron jobs — check `/etc/cron.d/` for disabled services

**Impact:** Load 163 → 7 in 3 minutes. RAM freed 1-2GB. Swap recovery over time.

### Verify hostname matches IP before optimization
Before running any optimization, verify `hostname -I` matches the expected VPS IP. Running optimization on the wrong machine (e.g., optimizing FLOW when you meant FORGE) wastes time and confuses the sovereign. **Proven 2026-07-14:** Agent ran full optimization on FLOW thinking it was FORGE. **Proven 2026-07-16:** External agent (wawabot) diagnosed "this machine is FLOW" when it was actually FORGE (72.62.71.199). The hostname `forge` was correct all along.

```bash
hostname -I | awk '{print $1}'   # IP
hostname                          # name
cat /etc/hostname                 # canonical
```

### Agent CLI MCP cascade — the #2 memory hog after stuck processes
Agent CLIs (Kimi Code, OpenCode, Claude Code) spawn their own MCP server children as subprocesses. When multiple agent sessions run simultaneously, each spawns duplicate servers (arifos, capability-index, brave-search, chrome-devtools, etc.). **Proven 2026-07-16:** Two Kimi sessions spawned 4 duplicate MCP children (~1.3GB). One OpenCode session spawned 15 MCP children (~1.1GB). Combined with stuck grok (93% CPU, 20hrs), load hit 118 on 8 cores.

**Detection:**
```bash
ps -eo pid,ppid,tty,args | grep -E "arifosmcp|capability_index/mcp" | grep -v grep
ps -eo pid,ppid,args --sort=-rss | grep "pts/" | grep -E "npm exec|chrome-devtools|sequential|context7" | wc -l
```

**Safe vs unsafe kills:**
- ✅ Safe: MCP children spawned by agent CLI sessions (ppid = kimi/opencode PID)
- ❌ Unsafe: systemd-managed services (check `systemctl show <service> -p MainPID --value` first)

### Kernel slab leak — unreclaimable without reboot
Linux 6.17+ has randomized kmalloc caches (`kmalloc-rnd-*`). Known bug: `kmalloc-rnd-12-2k` can leak tens of GB in kernel slab that `drop_caches` cannot reclaim. **Proven 2026-07-16:** 19.4GB in `kmalloc-rnd-12-2k` (9.7M × 2KB) on kernel 6.17.0-40-generic over 15 days uptime. User processes: only 3.3GB. The other 22GB was kernel slab.

**Detection:**
```bash
slabtop -o -s c | head -15
cat /proc/slabinfo | grep "kmalloc-rnd"
```

**What works (temporarily):** `drop_caches` frees page cache (~400MB). Kill user-space hogs for their RSS.
**What doesn't:** `drop_caches` does NOT reclaim active slab. No tunable in `/proc/sys/kernel/slab/`. Only fix: **reboot** (888_HOLD).

### Cron & memory hygiene — see references/cron-and-memory-hygiene.md
When doing full system health, also audit cron jobs for redundancy (duplicate schedules, overlapping topics, never-ran jobs, error-state jobs) and governed memory for cross-category duplication. Details and commands in the reference file.

### External diagnoses are UNVERIFIED until you probe
When someone (user, another agent, external tool) provides a machine diagnosis, do NOT trust it without verifying yourself. Always run `hostname`, `ip addr`, `docker ps -a`, `systemctl list-units` to confirm. **Proven 2026-07-16:** External diagnosis claimed this machine was FLOW with empty Docker and no OpenClaw — all wrong. It was FORGE with 10 containers and OpenClaw installed.

**Pattern:** Accept the diagnosis as a HYPOTHESIS, not OBS. Probe the machine yourself before acting on it.

### `du -sh` can timeout on large directories
`du -sh /root/*/` with many large repos can take 60s+ and timeout. Set `timeout=60` on the terminal call, or scope the scan: `du -sh /root/*/ --max-depth=0`. If it times out, skip and focus on the directories you already know are large (from `df` output).

### The dossier is a snapshot, not a live dashboard
Emphasize that the dossier reflects the moment it was generated. Processes, disk usage, and memory change constantly. For live monitoring, point to Grafana/Prometheus/Netdata.

## References

- `references/cron-and-memory-hygiene.md` — cron job audit patterns, memory tier dedup
- `references/kimi-mcp-timeout-diagnosis.md` — Kimi Code CLI MCP timeout diagnosis (arifOS stdio, startupTimeoutMs, HTTP vs stdio workaround)
