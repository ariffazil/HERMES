# Tailscale Architecture Deep Dive

> Source: tailscale.com/blog/how-tailscale-works + 2026 comparison articles.

## How Tailscale Works (The Short Version)

1. Install `tailscaled` daemon on each machine
2. Daemon generates WireGuard keypair
3. Keys registered with Tailscale coordination server
4. Coordination server distributes keys + IPs to all nodes
5. Nodes establish direct WireGuard tunnels (P2P)
6. If direct connection fails, traffic relays through DERP (encrypted)

## Control Plane vs Data Plane

| Plane | What | Where | Can Tailscale read it? |
|---|---|---|---|
| **Control plane** | Key exchange, IP assignment, ACLs, DNS | Tailscale's AWS (or Headscale) | Yes (metadata only) |
| **Data plane** | Actual traffic between devices | Direct P2P WireGuard tunnels | No (end-to-end encrypted) |

## NAT Traversal (The Hard Part)

Most machines are behind NAT (home routers, corporate firewalls, cloud security groups). Tailscale solves this:

1. **STUN** — Both nodes ask a STUN server "what's my public IP:port?" The STUN server tells them. Now they know how to reach each other.

2. **Hole punching** — Both nodes simultaneously send UDP packets to each other's public IP:port. The NAT routers see outbound traffic and create inbound allow rules. Connection established.

3. **DERP fallback** — If hole punching fails (symmetric NAT, strict firewalls), traffic relays through a DERP server. DERP servers are encrypted relays — they forward encrypted blobs, can't read content.

**Success rate:** ~90% direct P2P, ~10% DERP relay. For two VPS on public IPs, direct is nearly guaranteed.

## WireGuard (The Data Plane)

- **Protocol:** Noise Protocol Framework (like Signal)
- **Key exchange:** Curve25519
- **Encryption:** ChaCha20-Poly1305
- **Kernel-level:** Ships in Linux 6.12+, 8 Gbps throughput
- **Simplicity:** ~4,000 lines of code (vs OpenVPN's ~100,000)

## MagicDNS

Each node gets a DNS name: `<hostname>.ts.net`

Resolution works INSIDE the tailnet only. External DNS doesn't know about these names.

For arifOS: `af-forge.ts.net` resolves to `100.64.0.1`. SSH, curl, MCP — all work with the name instead of IP.

## DERP Relays

- 200+ global relays (2026)
- Encrypted end-to-end (relay can't read)
- Used for: NAT traversal fallback, initial connection setup
- NOT used for: bulk data transfer (once P2P established, traffic goes direct)

## Tailscale vs Traditional VPN

| Feature | Traditional VPN | Tailscale |
|---|---|---|
| Architecture | Hub-spoke | Mesh |
| Traffic path | All through central server | Direct P2P |
| Single point of failure | Yes (VPN server) | No (mesh) |
| NAT traversal | Manual port forwarding | Automatic |
| Setup | Complex (server + client config) | Simple (install + auth) |
| Performance | Limited by server bandwidth | Limited by direct link speed |
| Identity | Username/password | SSO (Google/GitHub/etc) |

## Tailscale vs ZeroTier

Both are mesh VPNs. Key differences:

| | Tailscale | ZeroTier |
|---|---|---|
| Protocol | WireGuard | Custom (proprietary) |
| Control plane | Managed (or Headscale) | Self-hosted (ZTNET) |
| NAT traversal | DERP relays | Moon roots |
| Performance | Higher (WireGuard kernel) | Lower (userspace) |
| Enterprise features | More mature | Less mature |

## Installation Commands

```bash
# Ubuntu/Debian
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Check status
tailscale status
tailscale ip -4

# Test connectivity
tailscale ping <node>.ts.net

# SSH over Tailscale
ssh root@<node>.ts.net

# Exit node (route all traffic through a specific node)
tailscale up --exit-node=<node>

# Subnet router (access entire network through one node)
tailscale up --advertise-routes=192.168.1.0/24
```
