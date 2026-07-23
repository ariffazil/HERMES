# Emergency Load Triage — Federation-Checkup

> Proven 2026-07-19 and 2026-07-23 on af-forge. Two distinct scenarios:
> orphaned agent processes, and post-reboot boot storm.

## When to Use

SEV:high load alert fires (load > 6.0 threshold on af-forge). 
The 5m and 15m averages tell you whether this is a spike or sustained.

## Phase 1 — Identify (15s)

```bash
# What's eating CPU right now?
top -b -n 1 -o %CPU | head -15

# Overall system state
uptime && free -h && cat /proc/loadavg
```

Key columns in top output:
- `%CPU` — who's burning cycles
- `RES` — who's eating RAM
- `STAT` — **D** (uninterruptible I/O) is the killer. Process is stuck waiting on disk.
- `COMMAND` — what is it?

## Phase 2 — Classify (30s)

For each top consumer, identify what it actually is:

```bash
# Get full command line
cat /proc/<PID>/cmdline | tr '\0' ' '

# What directory is it running from?
ls -la /proc/<PID>/cwd

# Systemd service or standalone?
systemctl status <PID> 2>/dev/null || echo "not a service"
```

### Classification Matrix

| Pattern | Classification | Action |
|---------|---------------|--------|
| Multiple `github-mcp-server stdio` processes | ORPHAN — dead agent sessions | Kill |
| `python -m pytest tests/` in D-state with >5GB RES | STALE TEST — I/O blocked | Kill |
| `kimi` / `kimi-code` with no matching systemd service | ORPHAN — dead session | Kill |
| `MainThr+` with high VIRT (>40GB) and no matching user session | ORPHAN BROWSER | Kill |
| `node ... hermes ... gateway` | **PRODUCTION** | Leave alone |
| `python ... arifosmcp` | **PRODUCTION** | Leave alone |
| `hermes ... gateway run` | **PRODUCTION** | Leave alone |
| `grafana` / `postgres` / `docker` | **PRODUCTION** | Leave alone |

## Phase 3 — Clean (10s)

```bash
# Kill all identified orphans in one shot
kill -9 <PID1> <PID2> <PID3> ...

# Verify they're gone and load is dropping
sleep 2 && uptime
```

**Expected result:** Load should drop from double-digits to <5 within 10 seconds.

If load doesn't drop: something else is wrong. Check `%Cpu(s)` — high `sy` (system) with dropping load means I/O wait from killed D-state processes clearing.

## Phase 4 — Verify (10s)

```bash
# Confirm no orphans remain
ps aux --sort=-%cpu | head -12

# Check all organ health
for port in 8088 7071 3001 8081 18082 18083; do
  curl -sf --max-time 3 "http://localhost:$port/health" >/dev/null 2>&1 \
    && echo "  :$port OK" || echo "  :$port DOWN"
done
```

## Known Orphan Patterns

| Orphan Class | Typical Signature | Cause | Frequency |
|-------------|------------------|-------|-----------|
| github-mcp-server | 3+ instances, 58% CPU each, <5MB RES | Dead agent sessions leave stdio MCP servers running | Common |
| pytest GEOX | 9GB+ RES, D-state, in /root/GEOX | Stale test run from prior session | Occasional |
| kimi / kimi-code | 25-41% CPU, 10GB VIRT, no systemd service | Agent sessions not cleaned up | Occasional |
| MainThr+ browser | 75% CPU, 40GB+ VIRT, 400MB RES | Browser tool left open by dead session | Rare |

## Structural Gap

**Nothing cleans up subprocesses when agent sessions die.** The agents spawn subprocesses
(github-mcp-server, kimi, pytest, browser) and when the session closes, the processes live on
indefinitely. This is the root cause behind most load spikes on af-forge.

Proposed fix (not yet built): session-cleanup hook that watches for dead agent sessions
and kills their orphan children. Currently manual intervention via this triage pattern.

## Post-Reboot Boot Storm

After a VPS reboot, ALL services start simultaneously. Load spikes to 11+ are normal and
will decay within 2-3 minutes. Key indicators this is a boot storm, not an emergency:

- `uptime` shows minutes (not hours)
- Swap is 0 used (fresh boot)
- Memory is mostly free (>50%)
- All top processes are PRODUCTION services (hermes, opencode, grafana, arifos)

**Do NOT kill processes during a boot storm.** The load will self-resolve.
Only intervene if load stays >6.0 for more than 5 minutes after boot.

## VPS Reboot Forensics

When the VPS rebooted unexpectedly, trace the shutdown cascade:

```bash
# What was the last boot?
journalctl --list-boots

# Look at the END of the previous boot
journalctl -b -1 --no-pager -n 100

# Find the trigger — what initiated shutdown?
# Look for: Stopping <service>, systemd-reboot.service, network.target cascade
# The FIRST service stopped is usually NOT the root cause — look 30s before
```

**Proven cascade (2026-07-23):**
1. Hermes MCP degraded for 17 min (failing reconnects every 300s)
2. arifOS restarted cleanly (systemctl restart, benign)
3. hermes-asi-gateway SIGTERM via dependency (arifOS restart triggered it)
4. Gateway couldn't cleanly terminate degraded MCP sessions → exit code 1
5. network.target cascade → full systemd reboot

**Detection:** Check for MCP degradation BEFORE restarting arifOS.
`journalctl -u hermes-asi-gateway --since "30 min ago" | grep "failed after 5 reconnection"`
If seen, restart gateway independently to clear MCP state before touching arifOS.
