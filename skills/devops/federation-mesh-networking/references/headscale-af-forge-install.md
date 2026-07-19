# Headscale Installation on af-forge — Session Log (2026-07-14)

## What was done

1. Installed Headscale v0.29.2 via .deb package from GitHub releases
2. Configured on port 9080 (port 8080 was in use by searxng)
3. Created user `arifos-federation` (user ID 1)
4. Generated reusable pre-auth key (24h expiration)
5. Opened UFW ports 9080/tcp and 3478/udp
6. Installed Tailscale client on af-forge
7. Discovered af-forge already has hosted Tailscale (arifbfazil@) with 66 nodes

## Issues encountered

1. **Port 8080 conflict** — searxng docker container bound to 127.0.0.1:8080. Used port 9080 instead.
2. **Multiple services on same port** — metrics_listen_addr, grpc_listen_addr, stun_listen_addr all defaulted to 9080. Commented out metrics and grpc, moved stun to 3478.
3. **IPv6 returned by curl** — `curl ifconfig.me` returned `2a02:4780:5e:dbf6::1` instead of `72.62.71.199`. Fixed with `curl -4 -s ifconfig.me`.
4. **CLI changed in v0.29.2** — `headscale namespaces create` → `headscale users create`. `headscale --user <name> preauthkeys create` → `headscale -u <ID> preauthkeys create`.
5. **Existing hosted Tailscale** — af-forge already registered on arifbfazil@ tailnet. Cannot run two tailscaled instances easily. Decision pending: migrate to Headscale or run dual-stack.

## Current state

- Headscale: LIVE on http://72.62.71.199:9080
- Health check: `curl http://127.0.0.1:9080/health` → `{"status":"pass"}`
- Pre-auth key: generated, ready for node registration
- Migration: BLOCKED — Arif needs to decide hosted Tailscale vs Headscale

## Migration path

Option A: Full migration (disconnect hosted Tailscale, connect to Headscale)
- Pros: Full sovereignty, single coordination server
- Cons: Loses access to existing personal devices until they migrate too

Option B: Dual-stack (run separate tailscaled instance for Headscale)
- Pros: Keeps hosted Tailscale for personal devices, adds Headscale for federation
- Cons: More complex, two tailscaled daemons

Option C: Wait (Headscale installed, migrate when node 3 arrives)
- Pros: No disruption, SSH federation still works
- Cons: Deferred decision
