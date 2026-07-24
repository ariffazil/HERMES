---
name: headscale-install
description: "Headscale self-hosted Tailscale installation guide with pitfall solutions"
---

# Headscale Installation Guide

Self-hosted Tailscale coordination server. Runs on af-forge, manages federation mesh.

## Installation (Ubuntu/Debian)

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')

# Download .deb package
ARCH="amd64"
curl -fsSL -o /tmp/headscale.deb "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_${ARCH}.deb"

# Install
dpkg -i /tmp/headscale.deb
headscale version
```

**Do NOT use:** `curl https://headscale.net/install.sh | sh` — returns 404 as of v0.29.2.

## Configuration

Config file: `/etc/headscale/config.yaml`

Key settings to change:
```yaml
server_url: http://YOUR_PUBLIC_IP:9080
listen_addr: 0.0.0.0:9080
# Disable or change ports for metrics/grpc/stun to avoid conflicts
# metrics_listen_addr: 0.0.0.0:9091
# grpc_listen_addr: 0.0.0.0:50443
stun_listen_addr: 0.0.0.0:3478
```

## CLI Syntax (v0.29.2+)

```bash
# Create user (NOT namespace)
headscale users create arifos-federation

# List users (get numeric ID)
headscale users list

# Generate preauth key (use numeric ID, not name)
headscale -u 1 preauthkeys create --reusable --expiration 24h

# List nodes
headscale nodes list

# Health check
curl -sf http://127.0.0.1:9080/health
```

## Pitfalls

1. **Install script 404:** Use .deb package from GitHub releases
2. **CLI syntax:** `namespaces` → `users` in v0.29.2+
3. **User ID:** Preauth keys need numeric user ID, not name
4. **IPv6 detection:** Use `curl -4 -s ifconfig.me` for IPv4
5. **Port conflicts:** Multiple services default to same port — disable or reassign
6. **Hosted Tailscale coexistence:** Can't run both on same socket. Disconnect hosted first or use separate sockets.
