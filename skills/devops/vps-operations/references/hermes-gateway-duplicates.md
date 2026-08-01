# Hermes Gateway Duplicate Detection & Cleanup

## Background

Hermes gateway (`hermes gateway run --replace`) is managed by a restart mechanism. When the gateway detects a stale sibling or a restart signal, it can spawn a new instance WITHOUT cleaning up the old one, creating duplicate processes.

## Detection Pattern

```bash
# Find all gateway processes
ps aux | grep "hermes gateway" | grep -v grep

# Expected: ONE process only
# Suspicious: 2+ processes, especially if one is in T (stopped) state
```

### Classifying Duplicates

| State | Meaning | Action |
|-------|---------|--------|
| `S` (sleeping) | Active, serving traffic | **Check gateway_state.json** — if PID matches, this is canonical |
| `T` (stopped) | Stopped mid-lifecycle, orphaned | **Kill** — consuming memory with stale FDs, never recovers |
| `Ssl` (sleeping, multi-threaded, leader) | Active gateway | Check start time against canonical |

## Canonical PID Verification

`gateway_state.json` at `~/.hermes/gateway_state.json` holds the canonical PID:

```bash
python3 -c "import json; d=json.load(open('$HOME/.hermes/gateway_state.json')); print(f'pid={d[\"pid\"]}, state={d[\"gateway_state\"]}')"
```

**Rule:** The PID in `gateway_state.json` is the canonical active gateway. Any other `hermes gateway` process is a duplicate.

## Pre-Kill Telemetry

Before killing, capture evidence to `forge_work/`:

```bash
PID=<orphan_pid>
mkdir -p /root/A-FORGE/forge_work/$(date +%Y-%m-%d)/orphan-pid-$PID

# Capture full /proc telemetry
cat /proc/$PID/status > /root/A-FORGE/forge_work/$(date +%Y-%m-%d)/orphan-pid-$PID/proc_status.txt
cat /proc/$PID/cmdline | tr '\0' ' ' > /root/A-FORGE/forge_work/$(date +%Y-%m-%d)/orphan-pid-$PID/cmdline.txt
ls /proc/$PID/fd/ | wc -l > /root/A-FORGE/forge_work/$(date +%Y-%m-%d)/orphan-pid-$PID/open_fds_count.txt

# Record key fields for quick reference
grep -E "State|Pid|PPid|VmRSS|Threads" /proc/$PID/status
```

## Token/Vault Dedupe Check

After identifying a duplicate gateway, verify it didn't leave corrupt state:

```bash
# Check gateway_state still points to canonical PID
cat ~/.hermes/gateway_state.json | python3 -m json.tool | grep pid

# Scan for stale PID references in state files
grep -r "$ORPHAN_PID" ~/.hermes/ --include="*.json" 2>/dev/null
# If output is empty → no stale references ✓

# Verify only one gateway process exists
ps aux | grep "hermes gateway" | grep -v grep | wc -l
# Expected: 1
```

## Kill Procedure

1. **SIGTERM first** (5s grace) — only if process is in running state
2. **SIGKILL** — if stopped (`T` state), SIGTERM won't work, go direct to SIGKILL
3. **Verify** — `ps aux | grep $PID | grep -v grep` should return empty
4. **Check gateway_state** — canonical PID should still be correct

## Pitfall: Restart Race Condition

**Critical:** Killing a stopped gateway orphan can trigger the gateway restart mechanism to spawn a **NEW duplicate** alongside the existing active gateway. Symptoms:

```
Before:  PID 1185213 (active, Ssl) + PID 1201613 (orphan, T)
After:   PID 1185213 (active, Ssl) + PID 1249477 (NEW duplicate, Ssl)
```

This happens when the restart watcher detects the killed orphan and fires a restart — but the active gateway is still healthy, so you end up with two running gateways.

**Detection:** After killing, wait 10 seconds and re-check:
```bash
sleep 10
ps aux | grep "hermes gateway" | grep -v grep
```

**If 2+ gateways running:** This is a gateway bug, not a kill error. Flag it, don't kill either active gateway without explicit direction. Both may be serving different sessions.

**Root cause (unresolved):** The gateway restart mechanism doesn't check if the active PID is healthy before spawning a replacement. When the dead sibling is removed, it interprets this as "gateway died" and restarts — but the original was never down.
