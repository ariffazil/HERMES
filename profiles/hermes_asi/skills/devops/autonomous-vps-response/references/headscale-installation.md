# Headscale Self-Hosted Installation (v0.29.2)

## Overview

Headscale is the open-source self-hosted coordination server for Tailscale. It replaces Tailscale Inc.'s hosted coordination server, giving full sovereignty over your mesh network.

## Installation (Ubuntu/Debian)

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')

# Download .deb package
ARCH="amd64"
curl -fsSL -o /tmp/headscale.deb "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_${ARCH}.deb"

# Install
dpkg -i /tmp/headscale.deb
```

## Configuration

Config file: `/etc/headscale/config.yaml`

**Critical settings:**
```yaml
server_url: http://YOUR_PUBLIC_IP:9080
listen_addr: 0.0.0.0:9080
```

**Port conflicts (v0.29.2):** Default config uses same port (9080) for listen, metrics, gRPC, and STUN. Fix by disabling or redirecting:
```yaml
# Comment out or redirect these:
# metrics_listen_addr: 0.0.0.0:9091
# grpc_listen_addr: 0.0.0.0:50443
stun_listen_addr: 0.0.0.0:3478
```

**Firewall:**
```bash
ufw allow 9080/tcp comment "Headscale coordination"
ufw allow 3478/udp comment "STUN"
```

## CLI Changes (v0.29.2)

- `namespaces` → `users` (create/manage users instead of namespaces)
- Pre-auth keys use numeric user ID, not username

```bash
# Create user
headscale users create arifos-federation

# List users (get ID)
headscale users list

# Generate pre-auth key (use numeric ID)
headscale -u 1 preauthkeys create --reusable --expiration 24h
```

## Register Nodes

```bash
# On each node, install tailscale client
curl -fsSL https://tailscale.com/install.sh | sh

# Start tailscaled
systemctl start tailscaled

# Register to Headscale
tailscale up --login-server=http://YOUR_HEADSCALE_IP:9080 --accept-routes --hostname=NODE_NAME
```

**Note:** If node already has hosted Tailscale, use `--reset` flag to disconnect first:
```bash
tailscale up --reset --login-server=http://YOUR_HEADSCALE_IP:9080 --accept-routes --hostname=NODE_NAME
```

## Verification

```bash
# Health check
curl -sf http://127.0.0.1:9080/health

# List nodes
headscale nodes list

# List users
headscale users list
```

## Pitfalls

- **IPv6 public IP:** `curl -s ifconfig.me` may return IPv6. Use `curl -4 -s ifconfig.me` for IPv4.
- **Port 8080 conflict:** Many services use 8080. Use 9080 for Headscale.
- **Multiple tailscaled instances:** Can't easily run two tailscaled on same machine. If migrating from hosted Tailscale, disconnect first.
- **Pre-auth key format:** Uses numeric user ID (e.g., `1`), not username. Use `headscale users list` to find ID.

## Sources

- Official docs: https://headscale.net/stable/setup/install/official
- GitHub: https://github.com/juanfont/headscale
- Tested: 2026-07-14 on af-forge (Ubuntu 25.10, Headscale v0.29.2)
