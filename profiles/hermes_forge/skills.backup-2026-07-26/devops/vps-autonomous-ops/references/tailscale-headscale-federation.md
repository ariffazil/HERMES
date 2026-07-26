# Tailscale vs Headscale Decision Framework

For agentic federation networks. Researched 2026-07-14.

## What Tailscale Is

WireGuard-based mesh VPN. Creates encrypted P2P tunnels between devices. Three layers:
- **Control plane** — coordination server (key exchange, NAT traversal, ACLs). NOT in data path.
- **Data plane** — WireGuard tunnels (P2P). ChaCha20-Poly1305 encryption.
- **Fallback** — DERP relays (~200 global). Encrypted dumb pipes when P2P fails.

## Why P2P Matters for Agentic Intelligence

| Requirement | Hub-and-Spoke | P2P Mesh |
|---|---|---|
| Agent discovery | Central registry (SPOF) | Distributed DNS/mDNS |
| Latency | All traffic through hub | Direct device-to-device |
| Resilience | Hub dies = network dies | No single point of failure |
| Edge autonomy | Agents depend on central server | Agents operate independently |
| NAT traversal | Hub has public IP | STUN/TURN hole-punching |

Key insight from arxiv paper "Internet of Agentic AI" (June 2026): *"Previous AI patterns — centralized training clusters, cloud-based inference, hub-and-spoke data flows — are inadequate for agentic systems that must operate at the network edge with speed, autonomy and resilience."*

## Hosted Tailscale vs Headscale

| Factor | Hosted Tailscale | Headscale (self-hosted) |
|---|---|---|
| Setup time | 10 minutes | 30 minutes |
| Coordination server | Tailscale Inc. | Your own VPS |
| Network map visibility | Tailscale Inc. sees topology | Only you see it |
| Dependency | Third-party | Self-sovereign |
| DERP relays | Tailscale's ~200 global | Self-host or use Tailscale's |
| Free tier | 100 devices, 3 users | Unlimited |
| Client compatibility | Official Tailscale client | Same client (works identically) |

## Decision Rule

- **< 5 nodes, static IPs, SSH working** → SSH is fine. Tailscale adds complexity without solving a current problem.
- **5+ nodes, changing IPs, NAT/firewall issues** → Tailscale/Headscale solves real problems.
- **Sovereignty-first federation (arifOS)** → Headscale. Consistent with F1-F13 governance.
- **Quick start, migrate later** → Hosted Tailscale now, Headscale when ready.

## Architecture Mapping to arifOS

| Tailscale Feature | arifOS Equivalent |
|---|---|
| ACLs | T1/T2/T3 autonomy tiers |
| DERP relay fallback | Dead-man's switch (always-on connectivity) |
| MagicDNS | Organ naming (geox.ts.net, wealth.ts.net) |
| Subnet routers | Federation organ access |
| Tailscale SSH | Identity-based access (no key management) |
| Aperture (secrets) | VAULT999 vault layer |

## Node Onboarding Automation

With Headscale, agent-managed onboarding:
1. Human says: "add node X, IP Y, purpose Z"
2. AGI SSHes in, installs Tailscale client, runs `tailscale up --authkey=...`
3. ASI validates connectivity + runs smoketest
4. Human gets notification: "Node X live, federated"
5. Human does nothing else

Bootstrap still requires initial SSH access (pre-provisioned key or cloud-init). Tailscale solves everything after bootstrap.

## References

- Tailscale blog: "How Tailscale Works" — https://tailscale.com/blog/how-tailscale-works
- arxiv: "The Internet of Agentic AI" (June 2026) — https://arxiv.org/html/2606.12835v1
- Headscale docs: https://headscale.net/
- Tailscale ACLs: https://tailscale.com/kb/1018/acls
