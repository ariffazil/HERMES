# Headscale Installation on af-forge

Self-hosted Tailscale coordination server. Installed 2026-07-14 on af-forge (72.62.71.199).

## Install (v0.29.2)

```bash
# Download .deb from GitHub
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')
curl -fsSL -o /tmp/headscale.deb "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_amd64.deb"
dpkg -i /tmp/headscale.deb
```

**Do NOT use `curl https://headscale.net/install.sh | sh`** — returns 404. Use .deb method.

## Configuration

Config: `/etc/headscale/config.yaml`

**Port conflicts:** Default ports (8080, 9090, 3478) often conflict with existing services. Change:
- `listen_addr: 0.0.0.0:8083` (not 8080 — searxng/docker-proxy uses it)
- `metrics_listen_addr: 0.0.0.0:9091` (disable or change)
- `grpc_listen_addr: 0.0.0.0:50443` (disable or change)
- `stun_listen_addr: 0.0.0.0:3479` (not 3478)

**server_url:** Must match public IP: `http://72.62.71.199:8083`

## CLI Changes (v0.29.2)

- `namespaces` → `users` (create, list)
- `-u` flag takes numeric ID, not name
- `preauthkeys create -u 1 --reusable --expiration 24h`

```bash
# Create user
headscale users create arifos-federation

# List users (to get ID)
headscale users list

# Generate preauth key
headscale -u 1 preauthkeys create --reusable --expiration 24h

# List nodes
headscale nodes list

# Get ACL policy
headscale policy get
```

## Firewall

```bash
ufw allow 8083/tcp comment "Headscale coordination"
ufw allow 3479/udp comment "STUN"
```

## Join a Node

```bash
# Install Tailscale client
curl -fsSL https://tailscale.com/install.sh | sh

# Start daemon
systemctl enable --now tailscaled

# Join Headscale tailnet
tailscale up --login-server=http://72.62.71.199:8083 --hostname=<name> --accept-routes --authkey=<preauth-key>

# Verify
tailscale status
tailscale ip -4
```

## Dual-Stack with Hosted Tailscale

If the machine is already on hosted Tailscale:
- Hosted Tailscale uses 100.x.x.x range
- Headscale uses 100.64.0.x range (separate namespaces)
- Can run both without conflict
- Migration: disconnect from hosted → connect to Headscale

## Current State (2026-07-14)

| Component | Status |
|---|---|
| Headscale v0.29.2 | ✅ Running on af-forge:8083 |
| User arifos-federation | ✅ Created |
| srv1642546 (wawabot) | ✅ Joined as 100.64.0.1 |
| af-forge | ⏳ On hosted Tailscale (arifbfazil@) |
| ACL policy | ✅ Tag-gated federation |

## ACL Tags

- `tag:forge-node` — af-forge
- `tag:wawabot-node` — srv1642546
- `tag:aaa-node` — AAA cockpit
- `tag:organ-node` — GEOX/WEALTH/WELL
- `tag:hermes` — Hermes agents
