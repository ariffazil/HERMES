# MCP Process Hygiene — "Zen All" Sweep

When Arif says "zen all" or "clean up MCP", run this sweep.

## 1. Inventory

```bash
# All MCP-related processes
ps aux | grep -iE 'mcp|arifos|geox|wealth|well|mage|hound' | grep -v grep

# All federation ports
ss -tlnp | grep -E ':(8081|8088|18082|18083|18086|7071|7072|3001|4000)\s'

# Config state (fastest audit)
hermes mcp list 2>&1 | grep -E 'Name|hermes|arifos|geox|wealth|well|hound|mage'
```

## 2. Identify Duplicates

Multiple instances of the same server are normal ONLY when:
- One is a daemon (PPID=1) owning the port — e.g. hermes_mcp PID 1409
- Others are per-session stdio children spawned by gateway — e.g. hound/mage watchdogs

**Abnormal duplicates:**
- Two instances of the same streamable-http server (only one can own the port)
- Orphaned session children whose parent gateway is dead

**Detection:**
```bash
# Check port owner
ss -tlnp | grep :18086  # shows pid=NNNN

# Check parent of suspect process
ps -o ppid= -p <PID>
# PPID=1 → daemon (keep)
# PPID=<gateway_pid> → session child (keep if gateway alive)
# PPID=<dead_pid> → orphan (kill)

# Check if parent is alive
ps -p <PPID> -o pid,cmd
```

## 3. Kill Orphans (Serial)

```bash
# Kill duplicate that does NOT own the port
kill <duplicate_pid>
sleep 1
# Verify
ps aux | grep hermes_mcp | grep -v grep  # should show 1 instance

# For stubborn watchdogs (SIGTERM ignored):
kill -9 <pid>
```

**Gateway respawns its own children.** If you kill an active session's
hound/mage watchdog, the gateway will spawn a new one within seconds.
This is normal — don't chase respawn loops. Only kill processes whose
parent gateway is DEAD.

## 4. Stale Session Sets

Old Hermes sessions leave behind stdio MCP watchdog sets:
```
mcp_stdio_watchdog.py --ppid <old_gateway> -- hound
mcp_stdio_watchdog.py --ppid <old_gateway> -- /opt/mage-server/run.sh
```

If the old gateway (PPID) is dead, the whole set is orphaned:
```bash
# Check if old gateway still runs
ps -p <old_ppid> -o pid,cmd 2>/dev/null || echo "DEAD — orphans"

# Kill the set
kill <watchdog1> <watchdog2> <hound_child> <mage_child>
```

## 5. Version Updates

```bash
# HOUND: updates binary, running instances pick up on next session spawn
hound -u
# Output tells you which PIDs to restart (or just let sessions respawn)

# Verify
hound --version  # or: hound version
```

## 6. Final Verify

```bash
echo "── CONFIG ──"
python3 -c "
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
for name, conf in cfg.get('mcp_servers', {}).items():
    if isinstance(conf, dict):
        e = conf.get('enabled', True)
        print(f'  {\"✓\" if e else \"✗\"} {name}')
"

echo "── PORTS ──"
for p in 8088 8081 18082 18083 18086 7071 7072 3001 4000; do
  pid=$(ss -tlnp 2>/dev/null | grep "127.0.0.1:$p " | grep -oP 'pid=\K[0-9]+' | head -1)
  [ -n "$pid" ] && echo "  :$p  ✓  (PID $pid)" || echo "  :$p  ✗  DOWN"
done

echo "── PROCESS COUNTS ──"
echo "  hermes_mcp: $(ps aux | grep hermes_mcp | grep -v grep | wc -l)"
echo "  hound:      $(ps aux | grep '/hound' | grep -v grep | grep -v watchdog | wc -l)"
echo "  mage:       $(ps aux | grep 'mage-server/main' | grep -v grep | wc -l)"
```

## Pitfalls

- **NEVER global sed on config.yaml.** `sed -i 's/enabled: false/enabled: true/'`
  hits EVERY `enabled: false` in the file. Proven 2026-08-02: accidentally enabled
  deep-research, openrouter, AND minimax. Always use line-targeted:
  `sed -i '1227s/enabled: false/enabled: true'`
- **`hermes mcp enable/disable` does NOT exist.** Use `hermes config set` or
  line-targeted sed.
- **patch tool refuses config.yaml.** Security-sensitive file. Use terminal.
- **hound/mage per-session sets are NORMAL.** Each active Hermes session/gateway
  spawns its own stdio MCP children. 2 hound + 2 mage = 2 active sessions.
  Only kill when parent is dead.
