---
name: federation-mesh-networking
description: "Mesh networking for the arifOS federation — Tailscale, Headscale, AXL, P2P protocols, node onboarding, MagicDNS, NAT traversal. Class-level skill for connecting federation organs across multiple machines without manual SSH key management. Load when: 'set up tailscale', 'mesh networking', 'connect two VPS', 'add new node to federation', 'P2P for agents', 'headscale', 'federation networking', 'node onboarding', 'organ discovery across machines'."
triggers:
  - Tailscale or Headscale setup
  - Mesh VPN for federation
  - P2P networking for AI agents
  - Cross-VPS organ communication
  - Node onboarding automation
  - MagicDNS for agent discovery
  - NAT traversal for agents
  - AXL or Yggdrasil mesh
  - Agent mesh networking
---

# Federation Mesh Networking

> **Class:** DevOps — network layer for multi-machine agent federation.
> **Prerequisite:** Two or more VPS machines with SSH access. arifOS federation organs running.
> **Sovereignty model:** Tailscale managed (default) → Headscale self-hosted (upgrade path). AXL for frontier P2P.

## When to Use

When connecting arifOS federation organs across multiple machines. When onboarding a new VPS node. When reducing SSH key management complexity. When agents need to discover each other by name instead of IP:port.

**Not for:** Single-machine networking (organs on localhost). Not for public-facing services (use Caddy + Cloudflare).

## The Problem arifOS Solves

**Without mesh networking (current state):**
- Each node connection = 5 config points: IP, port, key path, user, firewall rules
- New node = SSH key exchange + authorized_keys dance + firewall rules + manual config
- IP change = federation breaks silently
- Complexity compounds linearly with each node

**With mesh networking:**
- Each node connection = 1 config point: `ssh af-forge.ts.net`
- New node = `tailscale up` + ACL update
- IP change = Tailscale handles it automatically
- Complexity stays constant regardless of node count

**Net result:** 5 failure modes → 1. Chaos reduction, not addition.

## Architecture: The Three Layers

```
Layer 3: Agent Communication (MCP + A2A)
    ↓
Layer 2: Organ Discovery (MagicDNS / peer ID)
    ↓
Layer 1: Mesh Network (Tailscale / Headscale / AXL)
```

Tailscale handles Layer 1-2. MCP/A2A handle Layer 3. They're complementary, not competing.

## Layer 1: Tailscale (Managed, Default)

### What It Does
- Creates a virtual network interface (`tailscale0`) alongside `eth0`
- Assigns stable `100.x.x.x` IPs to each node
- Handles NAT traversal (STUN/TURN + DERP relay fallback)
- MagicDNS: `af-forge.ts.net`, `srv1642546.ts.net`
- WireGuard encryption (Curve25519 + ChaCha20-Poly1305)

### What It Does NOT Touch
- Existing SSH config, firewall rules, ports
- UFW, iptables, sshd_config
- Physical network stack (eth0 stays untouched)
- Existing connections (`ssh -p 22888 root@72.62.71.199` keeps working)

### Installation (Ubuntu/Debian)
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
# Follow auth URL → login with Google/GitHub/Microsoft
```

### Verify Installation
```bash
tailscale status          # List all nodes in tailnet
tailscale ip -4           # Get 100.x.x.x IP
ping <peer>.ts.net        # Test mesh connectivity
```

### ACLs (Access Control)
Edit in Tailscale admin console or `~/.tailscale/acl.json`:
```json
{
  "acls": [
    {"action": "accept", "src": ["*"], "dst": ["*:*"]}
  ]
}
```
For production: restrict by tag (e.g., `tag:federation` can only reach `tag:organ`).

### Pricing
- Free: up to 100 devices, 3 users
- Personal: $5/month per 5 devices, up to 6 users
- Business: $8/user/month

## Layer 1 Alternative: Headscale (Self-Hosted, Sovereign)

### When to Upgrade
When sovereignty requirements demand full control over the control plane. When you don't want device keys/auth flows on Tailscale's AWS infrastructure.

### What Changes
- Control plane runs on YOUR VPS (not Tailscale's cloud)
- Same Tailscale clients work with Headscale (compatible)
- You manage DERP relays yourself
- ACLs in YAML instead of JSON

### Installation (.deb package — proven 2026-07-14)

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')
ARCH="amd64"
DEB_URL="https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_${ARCH}.deb"
curl -fsSL -o /tmp/headscale.deb "$DEB_URL"
dpkg -i /tmp/headscale.deb
headscale version
```

**Proven pitfalls (v0.29.2, 2026-07-14):**
- **Port conflicts:** Default config has metrics_listen_addr, grpc_listen_addr, and stun_listen_addr all on same port as listen_addr. Comment out or reassign metrics (9091), grpc (50443), stun (3478).
- **IPv6 vs IPv4:** `curl ifconfig.me` may return IPv6 on dual-stack VPS. Use `curl -4 -s ifconfig.me` for IPv4.
- **CLI changed in v0.29.2:** `namespaces` → `users`. Use `headscale users create <name>` not `headscale namespaces create`.
- **Preauth key requires numeric user ID:** `headscale -u 1 preauthkeys create` (use ID from `headscale users list`), not `headscale --user <name>`.
- **systemd service auto-created:** `.deb` package creates systemd service automatically. Just `systemctl start headscale`.
- **Config location:** `/etc/headscale/config.yaml` (auto-created by package).
- **server_url must match public IP:** `server_url: http://<PUBLIC_IP>:9080` — this is what clients connect to.
- **Existing Tailscale conflict:** If VPS already has hosted Tailscale, `tailscale up --login-server=...` needs `--reset` flag. But this disconnects from hosted Tailscale. Run separate tailscaled instance with `--socket` flag for dual-stack, or migrate fully.

### Node Registration
```bash
# On Headscale server:
headscale users create arifos
headscale preauthkeys create --user arifos --reusable --expiration 90d

# On client:
tailscale up --login-server=https://headscale.your-domain.com --authkey=<key>
```

### Migration from Tailscale Managed
Clients are compatible. Change the coordination server URL:
```bash
tailscale up --login-server=https://headscale.your-domain.com
```
Same mesh, same IPs, different control plane. Zero data plane disruption.

## Layer 1 Frontier: AXL (True P2P, No Control Plane)

### What It Is
Gensyn's AXL (April 2026) is a lightweight binary that creates a decentralized IPv6 overlay mesh using Yggdrasil + gVisor. No control plane at all — pure P2P.

### Key Properties
- Ed25519 keypair → stable peer ID (derived from public key)
- Local HTTP API at `localhost:9002`
- Built-in MCP and A2A protocol routing
- No port forwarding, no public IP, no root privileges needed
- NAT traversal built into Yggdrasil spanning tree

### Protocol Support
- `/send` — send data to peer by ID
- `/recv` — check inbound messages
- `/topology` — see network map
- `/mcp/{peer_id}/{service}` — call remote MCP service
- `/a2a/{peer_id}` — call remote A2A agent

### Maturity Assessment (2026-07)
- **Status:** Open source, working demos (collaborative autoresearch)
- **Pros:** Maximum sovereignty, no single point of failure, protocol-native
- **Cons:** Immature, no MagicDNS, no ACLs, no enterprise features, no community ecosystem
- **Verdict:** Watch for 6 months. Use for experimentation, not production.

## Node Onboarding Pattern

When Arif says "new node at X.X.X.X, purpose = [Y]":

### Step 1: Probe
```bash
ssh -o ConnectTimeout=10 root@X.X.X.X "hostname && uptime && cat /etc/os-release | head -3"
```

### Step 2: Install Tailscale
```bash
ssh root@X.X.X.X 'curl -fsSL https://tailscale.com/install.sh | sh && tailscale up'
```
User must complete auth flow (URL printed to terminal).

### Step 3: Validate Mesh
```bash
# From af-forge:
tailscale ping <new-node>.ts.net
ssh <new-node>.ts.net "hostname && echo MESH_OK"
```

### Step 4: Register with arifOS
- Add node to federation organ registry
- Wire heartbeat (WELL → new node → arifOS kernel)
- Run smoketest on all exposed ports

### Step 5: Report
```
🟢 Node [name] live.
IP: 100.x.x.x
Organs: [list]
Mesh: tailscale ping <Xms
Federation: registered, heartbeat active
```

## MagicDNS for Agent Discovery

With Tailscale, each node gets a DNS name: `af-forge.ts.net`, `srv1642546.ts.net`.

**For arifOS organs, extend this:**
```
geox.af-forge.ts.net     → 100.64.0.1:8081
wealth.af-forge.ts.net   → 100.64.0.1:18082
well.af-forge.ts.net     → 100.64.0.1:18083
```

This requires either:
- Tailscale Serve (expose local port as MagicDNS name)
- Caddy reverse proxy on Tailscale IP
- SRV records in Headscale DNS config

**Current recommendation:** Keep organs on localhost, use Tailscale for machine-to-machine SSH. Organ-level discovery stays at the MCP layer.

## Pitfalls

### Tailscale is additive, not replacing
It creates a NEW interface alongside eth0. Existing SSH, firewall, and port configs are untouched. If Tailscale dies, existing SSH still works. Zero risk.

### Control plane sovereignty
Tailscale managed = keys and topology on Tailscale's AWS. For personal/federation scale (2-5 machines), this is acceptable. For sovereignty-critical deployments, upgrade to Headscale. The clients are compatible — migration is a config change, not a reinstall.

### DERP relay fallback
~90% of Tailscale connections go direct P2P. ~10% fall back to DERP relays (encrypted, Tailscale can't read). If both nodes are on public VPS (no NAT), direct connection is nearly guaranteed.

### Don't expose organs directly over Tailscale unless needed
The current architecture (organs on localhost, accessed via SSH or reverse proxy) is fine. Tailscale's value is the machine-to-machine tunnel, not organ-level routing. Don't over-engineer.

### AXL is frontier, not production
Gensyn's AXL is exciting but immature (April 2026). No MagicDNS, no ACLs, no ecosystem. Watch it, experiment with it, but don't build production federation on it yet.

### Headscale requires running your own DERP
If you self-host Headscale, you need your own DERP relay for NAT traversal. For two VPS on public IPs, this isn't needed (direct connection works). For nodes behind NAT (home labs, mobile), you need a DERP relay somewhere.

### MagicDNS names are tailnet-scoped
`af-forge.ts.net` only resolves inside the tailnet. External services (Caddy, Cloudflare) still need public IPs or tunnel endpoints.

### Hostname confusion — verify before setting
When naming federation nodes, ALWAYS verify which machine you're on before running `hostnamectl set-hostname`. Check `hostname -I` and `curl -4 -s ifconfig.me` to confirm the IP matches the intended target. **Proven 2026-07-14:** FORGE's hostname was accidentally set to "flow" because the agent didn't verify which machine it was running on.

### Option A/B/C for existing Tailscale users
When a VPS already has hosted Tailscale and you're adding Headscale:
- **Option A:** Keep existing on hosted, new nodes on Headscale. Cross-network via SSH. Lowest risk.
- **Option B:** Migrate everything to Headscale. Breaks existing devices until re-auth.
- **Option C:** Run both — different IP ranges (100.x vs 100.64.x), no conflict.
- **Recommended:** Option A for immediate. Migrate node-by-node when ready.

## Decision Matrix

| Criterion | Tailscale Managed | Headscale | AXL | SSH Keys (current) |
|---|---|---|---|---|
| Setup time | 5 min | 30 min | 15 min | 20 min per node |
| NAT traversal | ✅ Built-in | ✅ Self-hosted DERP | ✅ Yggdrasil | ❌ Manual |
| Sovereignty | ❌ Tailscale's cloud | ✅ Full control | ✅ Full control | ✅ Full control |
| MagicDNS | ✅ | ✅ | ❌ | ❌ |
| ACLs | ✅ JSON | ✅ YAML | ❌ | ❌ (iptables) |
| Maturity | ✅ 5M users | ✅ Production-ready | ⚠️ Frontier | ✅ Battle-tested |
| Agent-native | ❌ | ❌ | ✅ MCP+A2A routing | ❌ |
| Migration cost | → Headscale: config change | → Tailscale: config change | N/A | → Any: full redo |

## References

- `references/tailscale-architecture.md` — How Tailscale works (control plane vs data plane, NAT traversal, WireGuard internals)
- `references/p2p-agentic-intelligence.md` — Research synthesis: P2P networks, agent mesh, A2A/MCP/AXL protocol stack, Aperture governance
- `references/headscale-af-forge-install.md` — Session log of Headscale installation on af-forge (2026-07-14)
- `references/federation-node-registry.md` — Live registry of federation nodes, naming convention, SSH config, services per node
