---
name: android-observer-node
description: Onboard an Android device as a stateless Sovereign Sensing Node in the arifOS federation via Termux + Tailscale/Headscale. No arifOS, no numpy — pure Python stdlib HTTP observer.
version: 1.0.0
triggers:
  - "add android node"
  - "phone to federation"
  - "observer node"
  - "sensing node"
  - "sovereign sensing"
---

# Android Observer Node Onboarding

Turn an Android phone into a passive, stateless sensing node in the arifOS federation.

## Architecture

- **Phone (S24):** Runs Python stdlib HTTP server on Tailscale IP — serves `/health`, `/probe`, `/sense`
- **FORGE (VPS):** Polls phone endpoints, stores historical data, never pushes to phone
- **Phone is stateless** — no cron, no logs stored locally, no arifOS, no numpy. Just responds when called.

## Prerequisites

- Android with Termux installed
- Tailscale Android app (for kernel-level TUN)
- Phone already joined to Headscale mesh

## Procedure

### 1. VPS side — Generate SSH key + Headscale auth

```bash
ssh-keygen -t ed25519 -f ~/.ssh/<name> -N "" -C "forge@<name>"
# Copy public key for phone authorized_keys

# If phone shows registration prompt, approve on Headscale:
headscale auth register --auth-id <id> --user <username>
```

### 2. Phone side — Install + deploy observer

```bash
pkg install python termux-api jq openssh -y
pkill -f observer.py 2>/dev/null

# Add FORGE SSH key
mkdir -p ~/.ssh
echo '<FORGE_PUBKEY>' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
sshd -p 8022

# Deploy observer
cat > ~/observer.py << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
import json, subprocess, os, time
from http.server import HTTPServer, BaseHTTPRequestHandler

class Observer(BaseHTTPRequestHandler):
    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == '/health':
            self._json({"status":"observer","node":"HOSTNAME","mesh":"TAILSCALE_IP"})
        elif self.path == '/probe':
            try:
                bat = json.loads(subprocess.run(['termux-battery-status'],capture_output=True,text=True).stdout)
                self._json({"node":"HOSTNAME","battery":bat.get('percentage'),"charging":bat.get('status'),"health":bat.get('health'),"temp_c":bat.get('temperature'),"uptime":os.popen('uptime').read().strip()})
            except: self._json({"error":"sensor fail"},500)
        elif self.path == '/sense':
            self._json({"last_probe":int(time.time())})
        else:
            self._json({"paths":["/health","/probe","/sense"]})

HTTPServer(('TAILSCALE_IP',8088), Observer).serve_forever()
PYEOF

nohup python3 ~/observer.py > ~/observer.log 2>&1 &
```

### 3. VPS side — Verify

```bash
curl -s http://<TAILSCALE_IP>:8088/health | jq .
curl -s http://<TAILSCALE_IP>:8088/probe | jq .
```

## Design Principles

- **ΔS < 0** — no state on phone, no cron, no background writes
- **F1 (Reversibility)** — kill observer.py, node disappears cleanly
- **Passive sensor** — FORGE polls, phone responds. Phone never initiates.
- **No heavy deps** — Python stdlib only, no numpy, no arifOS
- **Thermal safety** — no background processes beyond sshd + observer

## Three-Capability Architecture

A properly configured sensing node delivers three capabilities that were previously impossible without violating F1/F12:

### 1. Zero-Penalty Telemetry (Passive State)

Phone only listens on :8088. FORGE bears all processing cost via cron polling. No local cron, no background writes, no battery drain from active compute. Pure ΔS < 0 — the phone contributes data without contributing entropy.

### 2. Mesh-Internal Command Execution

From Termux, the phone can issue commands into the encrypted 100.64.0.0/10 mesh:

```bash
# Trigger AAA MCP tools on FLOW
curl http://100.64.0.4:8080/execute

# Health probe FORGE directly
curl http://100.64.0.2:7071/health
```

All traffic stays within Tailscale mesh — zero public internet exposure. The phone becomes a **sovereign command node** that can initiate actions on any mesh peer while remaining invisible to the public internet.

### 3. DMZ Adjacent But Immune (Absolute Shielding)

The phone operates adjacent to the internet-facing DMZ node (FLOW/flow-edge) under a hard one-way boundary:

| Path | Allowed? | Enforcement |
|------|----------|-------------|
| FORGE → S24 :8088 | ✅ | Tailscale mesh + FORGE cron polling |
| S24 → FLOW :8080 | ✅ | Tailscale mesh (phone initiates) |
| S24 → FORGE :7071 | ✅ | Tailscale mesh (phone initiates) |
| FLOW → S24 | ❌ | UFW + Headscale ACL deny |
| FLOW → FORGE | ❌ | UFW + Headscale ACL deny |
| Internet → S24 | ❌ | Phone not internet-facing, Tailscale encrypted |

**Why this matters:** If nasf.cloud or a Telegram bot on FLOW gets compromised, the attacker hits a concrete wall trying to reach S24. The phone is an *invisible remote control* — can fire commands outward but cannot be reached by any compromised service.

### DMZ Isolation Verification

After onboarding, verify the one-way boundary contract live:

```bash
# TEST 1: FORGE → S24 (should work — passive telemetry)
curl -sf --connect-timeout 8 http://100.64.0.1:8088/health

# TEST 2: FLOW → S24 (should FAIL — isolation contract)
ssh root@100.64.0.4 "curl -sf --connect-timeout 3 http://100.64.0.1:8088/health; echo Exit: \$?"

# TEST 3: FLOW → FORGE (should FAIL — egress blocked)
ssh root@100.64.0.4 "curl -sf --connect-timeout 3 http://100.64.0.2:7071/health; echo Exit: \$?"

# TEST 4: FLOW → S24 ping (should FAIL — network layer block)
ssh root@100.64.0.4 "ping -c 1 -W 2 100.64.0.1; echo Exit: \$?"
```

Expected results: Test 1 returns telemetry (or timeout if Termux asleep — this is normal Android behavior, not a boundary failure). Tests 2-4 all fail with timeout/100% loss — confirming the isolation contract is enforced at both network (ICMP) and transport (TCP) layers.

## FORGE-Side Telemetry — Pipeline Architecture

The FORGE side runs **two parallel cron jobs** that complement each other:

| Pipeline | Cron | Path | Role |
|---|---|---|---|
| Anomaly Alert | 10-min (`arifs24-telemetry`) | `/root/arifos-memory/arifs24-telemetry.jsonl` | Silent-when-clean; alerts Arif's DM on threshold breach |
| Vector Ingestion | 15-min (`s24-telemetry-ingestion`) | `/root/forge_work/s24-telemetry/YYYY-MM-DD.jsonl` | Full vector state + rolling 24h window + deltas |

**Why two pipelines:** The 10-min anomaly alert is a `no_agent: true` script — zero LLM tokens, immune to model drift, delivers only when something's wrong. The 15-min ingestion is LLM-driven (terminal toolset) and builds richer state vectors (deltas against previous reading, rolling min/max over 24h). Both are lightweight and don't conflict.

### Pipeline 1: Anomaly Alert (10-min cron)

### Script: `arifs24_sensor_log.py`

Create at `~/.hermes/scripts/arifs24_sensor_log.py`:

```python
#!/usr/bin/env python3
"""Phone telemetry logger — silent unless anomaly detected."""
import json, sys, urllib.request, urllib.error
from datetime import datetime, timezone

LOG_PATH = "/root/arifos-memory/arifs24-telemetry.jsonl"
PROBE_URL = "http://100.64.0.1:8088/probe"
TIMEOUT = 8

BATTERY_LOW = 15       # alert ≤ this
TEMP_HIGH = 45.0       # alert ≥ this

try:
    req = urllib.request.Request(PROBE_URL)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read())
except Exception as e:
    entry = {"ts": datetime.now(timezone.utc).isoformat(), "reachable": False, "error": str(e)}
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"⚠️ arifs24 UNREACHABLE — {e}")
    sys.exit(0)

data["ts"] = datetime.now(timezone.utc).isoformat()
data["reachable"] = True

with open(LOG_PATH, "a") as f:
    f.write(json.dumps(data) + "\n")

alerts = []
battery = data.get("battery", 100)
temp = data.get("temp_c", 0)
health = data.get("health", "GOOD")
charging = data.get("charging", "UNKNOWN")

if battery <= BATTERY_LOW: alerts.append(f"🔋 battery {battery}%")
if temp >= TEMP_HIGH: alerts.append(f"🌡️ temp {temp}°C")
if health != "GOOD": alerts.append(f"🫀 health={health}")
if charging == "DISCHARGING" and battery <= 25: alerts.append("⚡ discharging + low battery")

if alerts:
    print("⚠️ arifs24 — " + " · ".join(alerts))
# else: silent — no output = no delivery
```

### Cron Job

```python
cronjob(action='create', name='arifs24-telemetry',
        schedule='*/10 * * * *',         # every 10 minutes
        script='arifs24_sensor_log.py',
        no_agent=True,                    # zero LLM tokens
        deliver='origin')                 # DM for personal device alerts
```

Design decisions:
- **`no_agent: true`** — zero LLM cost, script runs directly. Also immune to model drift (null snapshots).
- **Silent-when-clean** — empty stdout → no message delivered. Arif only sees anomaly alerts.
- **Logs everything, alerts selectively** — JSONL grows for historical trending; alerts fire on thresholds.
- **Delivery: origin** — personal device health goes to DM, not AAA group. This is human-relevant, not machine infra.
- **Resilient to observer death** — script catches all exceptions, logs the failure, and alerts.

### Pipeline 2: Vector Ingestion (15-min cron)

Script: `/root/scripts/forge_s24_ingest.py`

This pipeline builds richer state vectors:
- Polls `/probe` endpoint every 15 minutes (LLM-driven via terminal toolset)
- Writes daily-bucketed JSONL: `/root/forge_work/s24-telemetry/YYYY-MM-DD.jsonl`
- Computes deltas (battery_delta, temp_delta) against previous reading
- Maintains rolling 24h window (battery min/max, temp max) from daily log
- Updates vector state at `/root/forge_work/s24-telemetry/vector_state.json`

Key architecture: prev state → compute deltas → write daily log → update vector.

### Anomaly Thresholds

| Condition | Alert |
|-----------|-------|
| Battery ≤ 15% | 🔋 low battery |
| Temp ≥ 45°C | 🌡️ thermal warning |
| Health ≠ "GOOD" | 🫀 battery health degraded |
| Discharging + ≤ 25% | ⚡ unplugged and low |
| Observer unreachable | ⚠️ UNREACHABLE (any error) |

### Pipeline 3: Reality Snapshot Compiler (Epistemic Bridge)

**Script:** `/root/scripts/forge_reality_snapshot.py` (copied to `~/.hermes/scripts/`)
**Cron:** `no_agent: true`, 15-min, `deliver: local`
**Output:** `/root/forge_work/reality/reality_state.txt`

This is the **epistemic bridge** — the FORGE-side compiler that turns raw telemetry into a single immutable artifact for cloud AI agent ingestion. Cloud agents (Gemini, ChatGPT, Claude) have no persistent network — they can't SSH into the mesh. The Reality Snapshot bridges this gap: the agent receives timestamped evidence (F2 truth) without any mutation access (F12 blocked).

**What it probes:**
1. **S24 Telemetry** — battery, temp, health, uptime via HTTP `GET /probe`
2. **FLOW Services** — running systemd units (arifosmcp, caddy, ollama, saf-mcp, docker, tailscaled, ssh)
3. **FLOW Resources** — disk usage (`df -h /`), memory (`free -h`)
4. **FLOW Firewall** — UFW status numbered
5. **Tailscale Mesh** — peer status
6. **MCP Health** — arifOS tools/floors/version on FLOW

**Design principles:**
- **Read-only SSH** — all commands are non-mutating (`systemctl list-units`, `df`, `free`, `ufw status`, `tailscale status`, `curl localhost:8080/health`)
- **Sanitized** — no secrets, no private IPs beyond mesh range
- **Epistemic tags** — every value carries OBS (live probe)
- **Delta-aware** — saves previous snapshot for comparison
- **Silent** — `local` delivery, zero messages. Consumed via `cat`

**Usage:** `cat /root/forge_work/reality/reality_state.txt` — paste output as system prompt for any cloud AI session.

See `references/reality-snapshot-compiler.py` for full script source.

## Federation Node Table

After onboarding, the phone appears as the first sensing node:

```
100.64.0.1  arifs-s24          📱 🔵  ← passive sensing
100.64.0.2  af-forge           ⚒️ 🔵  ← execution + cron
100.64.0.3  ariffazil-windows  🪟 🔵
100.64.0.4  flow-edge          🌊 🔵  ← DMZ edge gateway (renamed from srv1642546/"forge")
```

## Related Skills

- `federation-node-onboarding` — For VPS/server nodes (SSH + Tailscale + organ registration)
- `hermes-cron-rhythm` — Cron design patterns, alert-only delivery, silent-when-clean principle
- `agentic-infrastructure-ops` — Self-healing infra, watchdog state machines, multi-VPS federation

## Pitfalls

- **Script location for Hermes cron.** The `script` field MUST be a filename relative to `~/.hermes/scripts/`. Absolute paths like `/root/scripts/foo.py` are REJECTED with "Script path must be relative to ~/.hermes/scripts/." Copy the script to `~/.hermes/scripts/` first — the reference at `/root/scripts/` can stay as a symlink or backup copy, but the cron system only sees the `~/.hermes/scripts/` directory.
- **numpy on ARM64 Android Termux has no wheel** — always fails. Bypass completely.
- **Termux `tailscale` package may not exist** — use Android Tailscale app for TUN interface
- **Phone IP changes on mobile data** — Tailscale handles this; always use 100.64.0.x IP
- **Battery under 15%** — Android may kill background processes. Keep phone charging.
- **Temp > 45°C** — thermal throttle may slow observer. Passive design minimizes this.
- **`no_agent` cron is immune to model drift.** When Arif switches the global LLM model, all agent-driven cron jobs freeze with drift errors. `no_agent: true` jobs (like this telemetry) never trigger the drift guard — their snapshots are always null. Safe to create and forget.
- **First cron run may alert spuriously.** If the phone is at 20% battery + discharging when the cron is created, the first tick will alert. This is normal — subsequent runs go silent when conditions normalize.
- **Android kills Termux during sleep.** Whitelist Termux: Settings → Apps → Termux → Battery → Unrestricted. Without this, the observer dies on screen lock and the cron reports UNREACHABLE.
- **Termux deep sleep causes intermittent probe timeouts — this is NORMAL.** Even with battery optimization disabled, Android may kill the HTTP listener during deep sleep (especially when battery < 20%). The 15-min cron on FORGE handles this gracefully — it retries next cycle. Direct `curl` probes may timeout while the cron's most recent run succeeded. This is expected Android behavior, not a design flaw. Check the JSONL file for the most recent successful entry rather than relying on a live probe.
- **S24→FLOW SSH: use the phone's EXISTING keypair, don't generate on FORGE.** When Arif tries to SCP or SSH from Termux to FLOW, he may already have `~/.ssh/id_ed25519` on the phone (e.g. from `ssh-keygen` run during onboarding). Don't generate a new key on FORGE and try to transfer the private key — that violates the "never transfer private keys" rule. Instead: (1) check if `id_ed25519.pub` already exists on S24, (2) copy the PUBLIC key, (3) add it to FLOW's `/root/.ssh/authorized_keys` from FORGE. The private key stays on S24 where it was generated. **Proven 2026-07-24:** S24 already had `u0_a618@localhost` Ed25519 keypair from Termux setup; FORGE-generated key would have been a second unused identity.
