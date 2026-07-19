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
[ ] Smoketest passed
[ ] Sovereign notified: "Node [name] live, federated, zenned"
```

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

The sovereign does nothing until the notification arrives.
