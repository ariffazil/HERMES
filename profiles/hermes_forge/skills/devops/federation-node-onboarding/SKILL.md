---
name: federation-node-onboarding
description: "Onboard a new VPS/node to the arifOS federation mesh. SSH key exchange, Tailscale/Headscale setup, organ registration, smoketest, notification. Use when user says 'add new node', 'onboard X', 'connect new VPS', 'federation link', or gives an IP + purpose for a new machine."
version: 1.0.0
author: Hermes Agent
tags: [federation, onboarding, tailscale, headscale, ssh, mesh, devops, infrastructure]
triggers:
  - "add new node"
  - "onboard"
  - "connect new VPS"
  - "federation link"
  - "new machine"
  - "set up SSH to"
  - "bidirectional SSH"
---

# Federation Node Onboarding

Onboard a new VPS or machine to the arifOS federation. Handles SSH key exchange, Tailscale mesh setup, organ registration, smoketest, and notification. Designed so the sovereign provides IP + purpose, and the agents handle everything else.

## When to Use

- User says "add new node at X.X.X.X" or "onboard this VPS"
- User provides IP + purpose for a new machine
- Cross-federation SSH setup needed (bidirectional)
- Expanding the mesh to a new VPS

## When NOT to Use

- Existing node reconfiguration → use the relevant organ skill
- Local Docker networking → use Docker-specific skills
- Cloudflare tunnel setup → use `infra-guardian`

## Architecture: Two Layers

### Layer 1: SSH (manual, current)

Direct SSH key-based access between machines. Works for 2-3 nodes. Fragile at scale.

```
Node A ←—SSH key—→ Node B
  Config: IP, port, user, key path, firewall = 5 failure modes per connection
```

### Layer 2: Tailscale/Headscale (automated, target)

WireGuard mesh with MagicDNS. One service, one config point per node.

```
Node A ←—WireGuard tunnel—→ Node B
  Config: hostname.ts.net = 1 config point per connection
  NAT traversal: automatic
  Key management: automatic
  IP changes: handled by Tailscale
```

**Decision:** Layer 1 for immediate needs. Layer 2 for 3+ nodes. Both can coexist — Tailscale is additive (new interface `tailscale0`, doesn't touch existing SSH/firewall).

## Procedure — SSH Layer (Immediate)

### Step 1: Generate key pair (on THIS machine)

```bash
if [ -f ~/.ssh/<target>-forge ]; then
  echo "Key already exists"
else
  ssh-keygen -t ed25519 -f ~/.ssh/<target>-forge -N "" -C "<identity>@<hostname>"
fi
cat ~/.ssh/<target>-forge.pub
```

### Step 2: Exchange keys

- **Direction 1 (us → them):** Send our public key to the other side. They add it to `~/.ssh/authorized_keys`.
- **Direction 2 (them → us):** They send their public key. We add it to our `~/.ssh/authorized_keys`.

```bash
echo "<their-public-key>" >> ~/.ssh/authorized_keys
```

### Step 3: Test connectivity

```bash
ssh -i ~/.ssh/<target>-forge -p <port> -o StrictHostKeyChecking=accept-new root@<ip> "hostname && uptime && echo CONNECTION_OK"
```

### Step 4: Create SSH config entry

```bash
cat >> ~/.ssh/config << 'EOF'

Host <alias>
  HostName <ip>
  Port <port>
  User root
  IdentityFile ~/.ssh/<target>-forge
  IdentitiesOnly yes
  StrictHostKeyChecking accept-new
  ConnectTimeout 10
EOF
```

### Step 5: Verify

```bash
ssh <alias> "hostname && echo ready"
```

## Procedure — Tailscale Layer (When 3+ Nodes)

### Headscale (control plane on af-forge)

```bash
# Install Headscale
curl -fsSL https://headscale.net/install | sh

# Initialize
headscale namespaces create arifos

# Run as systemd service
systemctl enable --now headscale

# Install Headplane (web UI)
docker run -d --name headplane \
  -p 8089:3000 \
  -v /etc/headscale:/etc/headscale \
  tale/headplane:latest
```

### Tailscale client (on each node)

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Join Headscale network via Caddy proxy (port 443 — provider firewalls allow this)
# NOTE: NEVER use raw IP:port (e.g., http://72.62.71.199:8083) — Hostinger blocks non-standard ports.
tailscale up --login-server=https://headscale.<domain> --authkey=<pre-auth-key> --accept-routes --hostname=<name>

# Verify
tailscale status
tailscale ping <other-node>
```

### MagicDNS names

After joining, every node gets:
- `100.x.x.x` IP (stable, mesh-internal)
- `<hostname>.ts.net` DNS name
- Agents use DNS names, not IPs

### ACLs (access control)

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["tag:agent"],
      "dst": ["tag:federation:*"]
    },
    {
      "action": "accept",
      "src": ["tag:admin"],
      "dst": ["autogroup:internet:*", "tag:federation:*"]
    }
  ]
}
```

## Pitfalls

- **Tailscale is additive.** It creates a new network interface (`tailscale0`) alongside `eth0`. Does NOT touch existing SSH, firewall, or ports. Existing connections keep working. If Tailscale dies, SSH still works.
- **Don't skip the smoketest.** Always verify `hostname && uptime && echo CONNECTION_OK` before declaring the link live.
- **authorized_keys never lie.** Always verify the key was actually added (`wc -l ~/.ssh/authorized_keys` before and after).
- **Don't use password auth.** Ever. Key-based only. If the target doesn't have key auth set up, set it up first.
- **Headscale ≠ Tailscale cloud.** When installing Tailscale client, always pass `--login-server` to point at your Headscale instance. Otherwise it defaults to Tailscale's managed cloud.
- **Pre-auth keys for automation.** Generate a pre-auth key on Headscale (`headscale preauthkeys create -u <user_id> --reusable --tags tag:<tagname>`) so the `tailscale up` command doesn't require interactive browser auth. Note: Headscale `--user` / `-u` expects a numeric user ID (e.g., `2` for `wawabot`), not a username string.
- **NEVER transfer SSH private keys.** Private keys stay on their origin machine. If an agent tries to SCP/transfer a private key, stop immediately. Keys are generated locally, public keys are exchanged. **Proven 2026-07-14:** AGI attempted to transfer private key via SCP — blocked by ASI.
- **Verify hostname matches IP before setting.** Before running `hostnamectl set-hostname`, confirm `hostname -I` matches the intended target machine. Setting the wrong hostname causes federation identity confusion. **Proven 2026-07-14:** FORGE hostname accidentally set to "flow".

### 🔴 CRITICAL: Provider Firewall Blocks Non-Standard Ports (Hostinger)

**Proven 2026-07-18 — 30-min debugging session:** Hostinger VPS firewall silently DROPs all TCP to non-standard ports (everything except 22, 80, 443). This applies BETWEEN Hostinger VPSes in the same datacenter, not just from outside.

**Diagnostic pattern (confirmed via tcpdump):**
```
✅ SYN packets arrive at eth0
✅ iptables ACCEPT matches (counters increment)
❌ Application never sees connection
❌ NO SYN-ACK is ever sent back
❌ nc -zv TCP handshake OK but curl/HTTP hangs
✅ curl to port 80 works fine from same source
→ Provider-level firewall. NOT iptables, UFW, rp_filter, or listen backlog.
```

**Solution:** Route ALL inter-VPS service traffic through Caddy on port 443 using subdomains. NEVER use raw `IP:port` for cross-VPS connections.

**Headscale connection — correct form:**
```bash
tailscale up --login-server=https://headscale.arif-fazil.com --authkey=<key>
# NOT: tailscale up --login-server=http://72.62.71.199:8083  ← SILENTLY BLOCKED
```

**Stuck tailscaled recovery:** If a node's tailscale was previously configured with the wrong URL and gets stuck in `NoState`:
```bash
systemctl stop tailscaled
rm -f /var/lib/tailscale/tailscaled.state    # clear corrupted state
systemctl start tailscaled
tailscale up --login-server=https://headscale.arif-fazil.com --authkey=<key> --accept-routes --hostname=<name>
```

**Old orphaned node cleanup:** If re-registering with the same hostname creates a `-1` suffix, delete the old node on Headscale first:
```bash
headscale nodes list | grep <hostname>
headscale nodes delete -i <old_node_id> --force
```

## Onboarding Checklist (Copy for Each New Node)

```
Node: <hostname>
IP: <ip>
Purpose: <purpose>
SSH Port: <port>

[ ] SSH key generated (this machine)
[ ] Public key sent to target
[ ] Target's public key added to our authorized_keys
[ ] SSH connectivity verified (both directions)
[ ] SSH config entry created
[ ] Tailscale installed on target
[ ] Tailscale joined to Headscale mesh
[ ] MagicDNS name resolves
[ ] arifOS organ registered (if applicable)
[ ] identity.toml deployed with Ed25519 (if arifOS MCP node)
[ ] /health confirms identity_hash
[ ] Smoketest passed
[ ] Sovereign notified: "Node [name] live, federated, zenned"
```

## DMZ / Boundary-First Onboarding (Internet-Facing Nodes)

When onboarding a node that is **already exposed to the internet** (hosts public websites, runs Telegram bots), the sequence is REVERSED: **boundary before role.** Never define what the node DOES until you've locked down what it can REACH.

**Why (F12 Injection Risk):** An internet-facing node with mesh access but no controls = a bridge from public internet directly into internal mesh. Compromise the node → reach FORGE, S24, everything.

### 3-Layer Audit (Run BEFORE defining role)

```bash
# Layer 1: Mesh Egress — can this node reach internal nodes?
tailscale ping 100.64.0.2   # FORGE
tailscale ping 100.64.0.1   # S24 (sovereign device)

# Layer 2: Public Ingress — what ports are open to the world?
sudo ufw status numbered
ss -tlnp | grep -v 127.0.0.1   # anything on 0.0.0.0 or * is exposed

# Layer 3: Credential Surface — are secrets shared?
ls -la /root/vault.env /root/.secrets/vault.env 2>&1
find /root -maxdepth 2 -name "*.env" -o -name "*.secret" 2>/dev/null
```

**Red flags per layer:**
- Layer 1: Any successful ping to internal IPs → ACL WILDCARD — must be cut
- Layer 2: SSH open to Anywhere, internal services on 0.0.0.0 → lock down
- Layer 3: vault.env exists and matches another node → shared credential surface

### DMZ Lockdown Contract

```
Internet ──→ DMZ (:80, :443 public services)    ← Traffic STOPS here
Internal ──→ DMZ (:specific ports)              ← One-way, internal-initiated
DMZ ──→ Internal ❌                               ← CUT
DMZ ──→ Internet ✅                               ← Needed for API egress
```

### Tailscale ACL for DMZ

Replace wildcard `* → *:*` with explicit one-way rules. The DMZ tag gets ONE egress rule:

```json
{
  "action": "accept",
  "src": ["tag:flow-dmz"],
  "dst": ["autogroup:internet:*"]
}
```

No rule for DMZ → internal nodes. Internal nodes get explicit allows TO DMZ ports only.

### UFW Lockdown

```bash
# Remove SSH-from-Anywhere
sudo ufw --force delete <rule_number>

# SSH only from mesh
sudo ufw allow from 100.64.0.0/10 to any port 22 proto tcp

# Explicit deny internal services on public interface
sudo ufw deny 8080/tcp
```

### Bidirectional Verification (ALL must be run)

```bash
# From DMZ: verify CANNOT reach internal (must FAIL)
curl -s --max-time 3 http://100.64.0.2:7071/health  # → BLOCKED ✅
curl -s --max-time 3 http://100.64.0.1:8088/health   # → BLOCKED ✅

# From DMZ: verify CAN reach internet (must WORK)
curl -s http://httpbin.org/ip                        # → WORKS ✅

# From FORGE: verify CAN reach DMZ (must WORK)
curl -s http://100.64.0.4:8080/health                # → WORKS ✅
ssh root@100.64.0.4 "echo SSH_OK"                    # → WORKS ✅
```

### DMZ Pitfalls

- **Never skip bidirectional verify.** Confirming DMZ→internal is BLOCKED is as important as confirming internal→DMZ works.
- **Internet egress is REQUIRED.** Telegram bots, API polling — DMZ needs outbound internet. Do NOT remove `autogroup:internet:*`.
- **Shared sovereignty (F5).** When the node is shared with another human (e.g., Azwa's FLOW), boundary enforcement protects BOTH parties. Never break their existing services.
- **Hostname collision.** Verify `hostname` on target before naming. FLOW was named "forge" — same as af-forge at 100.64.0.2.

**Hostname Collision Fix Pattern (proven 2026-07-24):**

When two federation nodes share a name, fix all THREE surfaces:

```bash
# 1. System hostname
ssh root@<target_ip> "hostnamectl set-hostname <new_name> && hostnamectl status --static"

# 2. /etc/hosts (replace old name in all entries)
ssh root@<target_ip> "sed -i 's/<old_hostname>/<new_name>/g' /etc/hosts"

# 3. Cloud-init template (survives reboot)
ssh root@<target_ip> "sed -i 's/<old_hostname>/<new_name>/g' /etc/cloud/templates/hosts.debian.tmpl"
```

**Proven:** FLOW (100.64.0.4) renamed `forge` → `flow-edge` via this exact sequence. Service stayed healthy throughout — no restart needed. Cloud-init template patch ensures the rename survives host reboot.

**Why three surfaces:** `hostnamectl` sets the running hostname. `/etc/hosts` maps the old name to 127.0.1.1 (causing `hostname -f` to resolve wrong). Cloud-init template re-applies `/etc/hosts` at boot; without patching it, the old name returns on next reboot.

## Android Sovereign Sensing Node

Pattern for onboarding an Android phone as a passive telemetry sensor. Use when the sovereign wants physical-world data (battery, temperature, uptime) in the federation without burning the phone's CPU.

### Architecture: Poll, Don't Push

```
S24 ──Tailscale mesh── FORGE
  :8088                  cron every 15m
  /health                curl /probe → JSONL
  /probe                 VAULT999 anchor
  /sense
```

**Principle:** Phone runs Python stdlib HTTP server ONLY. No heavy deps (numpy, AI runtimes = 43°C idle). No background cron on phone. No state stored. FORGE polls, phone answers, FORGE stores. Stateless sensor.

### Phone Setup (Termux, stdlib only)

```bash
# Pure Python stdlib — no pip install needed
# HTTP on :8088, bind to Tailscale IP (not 0.0.0.0)
# /health → {"status":"observer","node":"arifs-s24","mesh":"100.64.0.1"}
# /probe  → battery, temp_c, charging, health, uptime, loadavg
# /sense  → log count, last probe timestamp
```

### FORGE Poller — Dual Pipeline (proven 2026-07-24)

The FORGE side runs two parallel cron jobs. See `android-observer-node` skill for full details.

| Pipeline | Cron | Path | Role |
|---|---|---|---|
| Anomaly Alert | 10-min `arifs24-telemetry` | `/root/arifos-memory/arifs24-telemetry.jsonl` | Silent-when-clean, alerts DM on threshold |
| Vector Ingestion | 15-min `s24-telemetry-ingestion` | `/root/forge_work/s24-telemetry/YYYY-MM-DD.jsonl` | Rich vectors with deltas + rolling window |

### Phone Pitfalls

- **Timeout ≥10s.** Phone on cellular/DERP relay — 5s is too aggressive.
- **Load avg >20 on 8-core = CPU spike elsewhere.** The sensor itself is near-zero cost. High load = canary for rogue apps, not the sensor.
- **Never install pip deps.** First attempt: numpy/PyTorch → 43.4°C idle, compile failures. Pivot to stdlib. If `pkg install` can't provide it, it doesn't belong on the phone.
- **Bind to Tailscale IP.** :8088 on 100.64.0.x, never 0.0.0.0. No public port exposure.

## Identity Deployment — Ed25519 + identity.toml (DMZ / Non-Kernel Nodes)

When a node runs arifOS MCP but is NOT the federation kernel (e.g., FLOW on flow-edge), it needs a cryptographic identity for SCT validation and AgentCards. Generate locally on FORGE, deploy via SCP.

### Step 1: Generate Ed25519 keypair (on FORGE)

```bash
python3 -c "
from cryptography.hazmat.primitives.asymmetric import ed25519
import base64

sk = ed25519.Ed25519PrivateKey.generate()
pk = sk.public_key()
sk_bytes = sk.private_bytes_raw()
pk_bytes = pk.public_bytes_raw()

print('PRIVATE_HEX=' + sk_bytes.hex())
print('PUBLIC_HEX=' + pk_bytes.hex())
print('PUBLIC_B64=' + base64.b64encode(pk_bytes).decode())
"
```

### Step 2: Create identity.toml

Use the arifOS or GEOX identity.toml as templates. For a DMZ node, add the `[isolation]` section documenting the one-way boundary contract:

```toml
[organ]
name = "FLOW"
full_name = "DMZ Edge Gateway"
port = 8080
role = "Public Edge Gateway"
constitutional_class = "DMZ_WITNESS"
mutation_allowed = false

[identity]
algorithm = "ed25519"
source = "/opt/arifos/app/identity.toml"
fingerprint = "flow-<first8hex>"
public_key_hex = "<pubkey_hex>"

[federation]
kernel = "arifOS"
governed_by = "arifOS:8088"
peers = ["af-forge", "arifs-s24"]
mesh_ip = "100.64.0.x"

[isolation]
ingress_from_mesh = "100.64.0.0/10:22,8080"
egress_to_mesh = "DENY"

[doctrine]
motto = "DITEMPA BUKAN DIBERI"
```

### Step 3: Deploy + verify

```bash
# Deploy via SCP over Tailscale mesh
scp identity.toml root@<target_mesh_ip>:/opt/arifos/app/identity.toml

# Verify — /health now returns BLAKE3 hash of identity file
ssh root@<mesh_ip> "curl -s localhost:8080/health | python3 -c \"import sys,json; d=json.load(sys.stdin); print('identity:', d.get('identity_hash',{}).get('b3_prefix','MISSING'))\""
```

### Pitfalls

- **identity.toml goes in `/opt/arifos/app/`** — the arifOS runtime checks this path. `/health` reports `identity_hash.source` pointing here.
- **Fingerprint format:** `<organ>-<first 8 hex of public key>` — e.g., `flow-0d305b62`
- **Never transfer the private key.** Private key stays on FORGE. Only `public_key_hex` goes into identity.toml.
- **No restart needed.** `/health` picks up identity.toml on next probe.
- **Proven:** FLOW (100.64.0.4) deployed 2026-07-24 — Ed25519 `d305b628...`, BLAKE3 `101799e81fd87d07` confirmed.

## Deployment Triage (When Multiple Options Exist)

Use F1-F13 to rank options when Arif presents multiple deployment vectors:

| Criterion | Weight | Why |
|-----------|--------|-----|
| F1 Reversibility | Highest | Can this be paused/rolled back in seconds? |
| F12 Injection Risk | Highest | Is this node already exposed to internet? |
| Urgency asymmetry | Context | Exposed node with no boundary > idle node behind NAT |
| F4 ΔS | Medium | Does this close an open loop or open a new one? |

**Proven sequence (2026-07-23):** S24 telemetry loop (close open circuit, F4) → FLOW DMZ lockdown (exposed node, F12) → Windows activation (idle behind NAT, no urgency).

## Sovereign Contract

The sovereign provides:
- IP address
- Purpose (what this node will run)
- Any special constraints

The agents handle:
- Key generation and exchange
- Tailscale/Headscale setup
- Organ registration
- Smoketest and validation
- Notification when complete

**For internet-facing nodes:** Agents run 3-layer audit FIRST, apply DMZ lockdown, verify bidirectional, THEN define role. Boundary before function.

The sovereign does nothing until the notification arrives.
