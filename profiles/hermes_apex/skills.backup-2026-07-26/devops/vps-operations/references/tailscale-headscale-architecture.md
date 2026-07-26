# Tailscale/Headscale Architecture for Agentic Infrastructure

> Deep research 2026-07-14. Sources: Tailscale docs, Headscale docs, Gensyn AXL, HyperCycle, Coforge, Solo.io, WorkOS Aperture.

## What Tailscale Actually Is

Tailscale is a **managed mesh VPN** built on WireGuard. Two planes:

- **Data plane (P2P):** WireGuard creates encrypted tunnels directly between devices. Data never touches Tailscale's servers.
- **Control plane (centralized):** Tailscale's coordination server handles key distribution, IP assignment (100.x.x.x), NAT traversal (STUN/TURN), ACLs, MagicDNS.

~90% of connections go direct P2P. ~10% fall back to DERP relays (encrypted, Tailscale can't read them).

**Key facts (2026):** 5M+ users, free for 100 devices, WireGuard kernel-level 8 Gbps throughput, ~200 global DERP relays, 20+ identity provider integrations.

## Headscale: The Sovereign Alternative

Open-source reimplementation of Tailscale's control plane. BSD-3 license, written in Go, compatible with official Tailscale clients.

**Trade-off:** You run the control plane on YOUR machine. Your keys stay on your infrastructure. Your ACLs are your own. But you still get WireGuard's speed, NAT traversal, and MagicDNS.

**Headplane** = web UI for Headscale. React app that provides device list, ACL editor, key management, DNS settings.

## AXL: True P2P for AI Agents (Gensyn, April 2026)

Lightweight binary that connects users to a decentralized mesh network:
- Yggdrasil (decentralized IPv6 overlay) + gVisor userspace TCP
- No port forwarding, no public IP, no root privileges
- Built-in MCP and A2A protocol routing
- `/mcp/{peer_id}/{service}` and `/a2a/{peer_id}` endpoints

**Key quote:** "The gap between 'works on my laptop' and 'works across two laptops' is, in practice, enormous."

## Aperture: AI Gateway (Tailscale, Feb 2026)

Identity-linked governance for AI agents:
- Every AI API call logged with identity of caller
- API keys centralized (not scattered across machines)
- Policies applied per-identity
- Full audit trail

**NOT a secret store.** It's a governance and identity framework for agentic traffic. Manages who/what can talk to which service.

## Agent Mesh Architecture (2026 Convergence)

Protocols converging:

| Protocol | Layer | What it does |
|---|---|---|
| MCP | Tool sharing | Agent A shares tools with Agent B |
| A2A | Agent communication | Agent A delegates tasks to Agent B |
| ACP | Container orchestration | Agents in containers communicate |
| ANP | Internet-scale discovery | Agents find each other on the open web |
| AXL | Transport | P2P networking underneath all of the above |

**Pattern:** MCP → A2A → AXL is the stack. Tools → Agents → Transport.

## arifOS Current State (2026-07-14)

- Two VPS: af-forge (72.62.71.199) + srv1642546 (72.61.126.65)
- Headscale live on af-forge :8083
- srv1642546 joined mesh as 100.64.0.1
- af-forge on mesh as 100.64.0.2
- Existing SSH federation preserved (Tailscale is additive)
- Hosted Tailscale still active for personal devices (9+ nodes, 130+ days)

## Architecture Decision

**Chosen path:** Headscale on af-forge, Tailscale clients on every node, Headplane for dashboard.

**Why not pure Tailscale:** Control plane sovereignty (F13).
**Why not AXL:** Immature (April 2026). No ACLs, no MagicDNS.
**Why not pure SSH:** Manual key exchange, 5 config points per connection, doesn't scale.
