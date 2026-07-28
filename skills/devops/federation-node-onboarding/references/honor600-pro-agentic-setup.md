# Honor 600 Pro — Active Edge Compute Node Setup

## Reference: 7000mAh Phone as Federation Edge Compute Node

Setup a modern Android phone (Honor 600 Pro or equivalent with ≥7000mAh battery, Snapdragon 8 Elite, 12GB+ RAM) as an active federation edge node. The phone pushes heartbeat to VPS, maintains SSH access, and can run MCP client queries against arifOS kernel.

## Prerequisites

| Item | Status |
|---|---|
| Honor 600 Pro (or ≥7000mAh phone) | Android 16+ |
| Termux + Termux:Boot + Termux:API | From Play Store |
| VPS with heartbeat endpoint | FastAPI or plain HTTP |
| SSH server on VPS (port 22 or custom) | Standard |

## Phone Configuration (MagicOS 10)

Before running any commands, configure these settings — otherwise TermUX gets killed by Doze within 5-10 minutes:

1. **Settings > Battery > App launch > TermUX → "Manage manually"** — enable "Run in background"
2. **Settings > Wi-Fi > Advanced → Keep Wi-Fi on during sleep = Always**
3. **Settings > Display > Screen timeout → 10 minutes** (or longer for long-running TermUX tasks)
4. **Open Termux:Boot app once** — grant notification access

## Setup Commands (Copy-paste sequence)

### Phase 1: Package install
```bash
termux-setup-storage
pkg update -y && pkg upgrade -y
pkg install -y python python-pip nodejs git openssh curl wget jq tmux neovim build-essential binutils rust cmake openssl-tool clang
```

### Phase 2: Python environment
```bash
python -m venv $HOME/agentic
source $HOME/agentic/bin/activate
pip install httpx mcp pandas requests fastapi uvicorn pyyaml
python -c "import httpx; print('✅ Agentic env ready')"
```

### Phase 3: SSH key + VPS connect
```bash
# Test Ed25519 first; if it fails, use RSA (-t rsa -b 4096)
ssh-keygen -t ed25519 -C "honor600-agent" -f $HOME/.ssh/id_ed25519 -N ""
cat $HOME/.ssh/id_ed25519.pub
```
Copy the public key output and add to VPS `~/.ssh/authorized_keys`, then test:
```bash
ssh -o StrictHostKeyChecking=accept-new root@<vps-ip> "hostname && echo ✅"
```

### Phase 4: Heartbeat agent (node.py)

The agent reports battery status (via `termux-battery-status`), memory, CPU cores, and uptime. It POSTs to the VPS heartbeat endpoint every 30 minutes.

`node.py` (Python 3, uses httpx):
```python
#!/usr/bin/env python3
"""Honor 600 Pro — Termux Agentic Node"""
import os, json, subprocess, socket, platform
NODE_ID = f"honor600-{socket.gethostname() or 'node'}"
VPS_IP = os.environ.get("VPS_IP", "<vps-ip>")

def system_status():
    try:
        bat = json.loads(subprocess.check_output(["termux-battery-status"]))
    except Exception:
        bat = {"percentage": 0, "status": "unknown"}
    mem = os.popen("free -h | grep Mem").read().strip()
    cpu = os.popen("nproc").read().strip()
    uptime = os.popen("uptime -p").read().strip() or "N/A"
    battery_pct = bat.get("percentage", 0)
    return {"node": NODE_ID, "battery_pct": battery_pct,
            "memory": mem, "cpu_cores": cpu, "uptime": uptime,
            "platform": platform.platform()}

def heartbeat():
    try:
        import httpx
        r = httpx.post(f"http://{VPS_IP}:7073/heartbeat",
            json=system_status(), timeout=10)
        return r.status_code == 200
    except Exception:
        return False

if __name__ == "__main__":
    print(json.dumps(system_status(), indent=2))
    ok = heartbeat()
    print("✅ Heartbeat OK" if ok else "⚠️ Heartbeat FAIL")
```

Save to `$HOME/agentic/node.py`, then:
```bash
chmod +x $HOME/agentic/node.py
source $HOME/agentic/bin/activate && python $HOME/agentic/node.py
```

### Phase 5: Auto-start (Termux:Boot)

Create `~/.termux/boot/start-agent.sh`:
```bash
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd $HOME/agentic
source bin/activate
# Heartbeat every 30 minutes
while true; do python node.py; sleep 1800; done &
```
Make executable: `chmod +x $HOME/.termux/boot/start-agent.sh`

### Phase 6 (Optional): MCP Client

Minimal MCP client that connects to arifOS kernel from phone:
```python
#!/usr/bin/env python3
import httpx, json
KERNEL_URL = "http://<vps-ip>:8088/mcp"
def call_tool(name, args=None):
    payload = {"jsonrpc": "2.0", "method": "tools/call",
               "params": {"name": name, "arguments": args or {}}, "id": 1}
    try:
        r = httpx.post(KERNEL_URL, json=payload, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    result = call_tool("arif_observe", {"query": "Honor 600 Pro Termux", "mode": "search"})
    print(json.dumps(result, indent=2)[:500])
```

## Quick Test Commands

```bash
source $HOME/agentic/bin/activate && python $HOME/agentic/node.py    # test agent
termux-battery-status                                                  # check battery
free -h && uptime -p && nproc                                          # system info
ssh root@<vps-ip> "journalctl -u arifos --since '5 min ago' --no-pager | tail -10"  # VPS check
```

## What the Agent Reports (sample)

```json
{
  "node": "honor600-localhost",
  "battery_pct": 85,
  "memory": "Mem: 7.2Gi total, 3.1Gi free, 2.4Gi used, 1.7Gi buff/cache",
  "cpu_cores": "8",
  "uptime": "up 2 hours, 15 minutes",
  "platform": "Linux-5.15.148-android13-8-00001-g6c0a3b7c8c98-aarch64-with-..."
}
```

## VPS Listener (FastAPI)

Minimal FastAPI endpoint for receiving heartbeats:
```python
from fastapi import FastAPI
import json, datetime
app = FastAPI()

@app.post("/heartbeat")
async def receive(data: dict):
    ts = datetime.datetime.utcnow().isoformat()
    node = data.get("node", "unknown")
    bat = data.get("battery_pct", 0)
    line = f"{ts} | {node} | bat={bat}% | mem={data.get('memory','?')} | uptime={data.get('uptime','?')}"
    with open(f"/var/log/phone-heartbeat/{node}.log", "a") as f:
        f.write(line + "\n")
    return {"ok": True, "logged": node}
```

## Known Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Heartbeat stops after 5-10 min | MagicOS Doze kills TermUX | Set App launch to "Manage manually" + "Run in background" |
| `ssh-keygen -t ed25519` fails | Old Termux libcrypto | Use `-t rsa -b 4096` instead |
| `termux-battery-status` not found | Termux:API not installed | `pkg install termux-api` or install from Play Store |
| Heartbeat timeout | Phone on cellular with poor signal | Increase VPS timeout to ≥20s |
| Python module not found | Wrong venv | Ensure `source $HOME/agentic/bin/activate` is in loop script |

## Proven

- **2026-07-27:** Honor 600 Pro (12/512GB, RM3,099, MY variant with 80W charger in box). Full setup delivered via temp HTML page at syedos.arif-fazil.com. Phone designated as federation edge compute node with 30-min heartbeat loop.
