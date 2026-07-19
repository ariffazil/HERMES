# Federation Node CLI Patterns

Patterns for building Python CLI tools that manage and monitor arifOS federation VPS nodes. Born from `forge-nodes` (2026-07-16).

## SSH Port Discovery

**Never assume port 22.** arifOS federation VPS nodes use non-standard SSH ports:
- FORGE (af-forge): port **22888**
- FLOW (wawabot/srv1642546): port **22**

Always probe or ask before connecting. Store `ssh_port` per-node in the registry from day one — retrofitting is painful.

```python
def get_ssh_port(node: dict) -> int:
    return node.get("ssh_port", 22)  # explicit default
```

## Local Host Detection

When a monitoring tool runs on the same host as a monitored node, SSH loopback through the public IP is slow (~2s). Detect local hostname and use `127.0.0.1` for HTTP health probes instead:

```python
def _get_local_hostname() -> str:
    if not hasattr(_get_local_hostname, "_cache"):
        try:
            _get_local_hostname._cache = subprocess.check_output(
                ["hostname"], text=True, timeout=2
            ).strip()
        except Exception:
            _get_local_hostname._cache = ""
    return _get_local_hostname._cache

# In probe_node:
is_local = node.get("hostname", "") == _get_local_hostname()
probe_ip = "127.0.0.1" if is_local else node["ip"]
```

## Health Probe Strategy (Priority Order)

1. **HTTP `/health` on known organ ports** — fastest, richest data
   - arifOS: 8088, GEOX: 8081, WEALTH: 18082, WELL: 18083, A-FORGE: 7071, AAA: 3001
2. **SSH echo** — `ssh -p <port> root@<ip> "echo ok"` as fallback
3. **Local shortcut** — if we're running on this host, it's UP by definition

## SCP File Sync

When syncing files to remote nodes, create the target directory first:

```python
# 1. Create directory
ssh_cmd(ip, "mkdir -p /root/tools", port=ssh_port)
# 2. Then SCP
subprocess.run(["scp", "-P", str(port), local_path, f"root@{ip}:/root/tools/"])
```

## argparse Pitfall: `command` Name Collision

When a subparser uses `nargs=REMAINDER` for the remote command, do NOT name the positional arg `command` — it collides with the subparser's own `dest="command"`:

```python
# BAD — causes "unhashable type: 'list'" on args.command
p_exec.add_argument("command", nargs=argparse.REMAINDER)

# GOOD — use a distinct name
p_exec.add_argument("cmd_args", nargs=argparse.REMAINDER)
```

## Node Registry Schema

Recommended JSON schema for `/root/tools/nodes.json`:

```json
{
  "nodes": {
    "FORGE": {
      "ip": "72.62.71.199",
      "hostname": "forge",
      "role": "federation-engine",
      "organs": ["arifOS", "GEOX", "WEALTH", "WELL", "A-FORGE", "AAA"],
      "ssh_port": 22888,
      "added": "2026-07-16",
      "status": "active"
    },
    "FLOW": {
      "ip": "72.61.126.65",
      "hostname": "flow",
      "role": "comms-backbone",
      "services": ["wawabot", "tailscale"],
      "ssh_port": 22,
      "added": "2026-07-16",
      "status": "active"
    }
  }
}
```

Key fields per node:
- `ip` — public IP
- `hostname` — matches `hostname` command output (used for local detection)
- `role` — federation-engine, comms-backbone, worker, edge, etc.
- `ssh_port` — non-default SSH port
- `organs` / `services` — what runs on this node (determines health probe targets)
- `status` — active, maintenance, decommissioned
