# Headscale Installation — Self-Hosted Tailscale

## Why Headscale Over Hosted Tailscale

For arifOS federation, sovereignty matters. Hosted Tailscale = Tailscale Inc. sees your network map. Headscale = you own the coordination plane.

## Installation (Ubuntu/Debian)

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')

# Download .deb package
curl -fsSL -o /tmp/headscale.deb "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_amd64.deb"

# Install
dpkg -i /tmp/headscale.deb

# Verify
headscale version
```

## Configuration

Edit `/etc/headscale/config.yaml`:

```yaml
server_url: http://YOUR_PUBLIC_IP:9080
listen_addr: 0.0.0.0:9080
metrics_listen_addr: 0.0.0.0:9091  # Different port
grpc_listen_addr: 0.0.0.0:50443    # Different port
stun_listen_addr: 0.0.0.0:3478     # STUN for NAT traversal
```

**Port conflicts:** Don't use the same port for multiple services. Headscale needs: 9080 (HTTP), 50443 (gRPC), 3478 (STUN).

## Firewall

```bash
ufw allow 9080/tcp comment "Headscale coordination"
ufw allow 3478/udp comment "STUN"
```

## User & Auth Key Setup

```bash
# Create user
headscale users create arifos-federation

# List users to get ID
headscale users list

# Generate reusable auth key (24h expiry)
headscale -u 1 preauthkeys create --reusable --expiration 24h
```

## Join Node to Headscale

```bash
# Install Tailscale client
curl -fsSL https://tailscale.com/install.sh | sh

# Start daemon
systemctl enable --now tailscaled

# Join Headscale mesh
tailscale up --login-server=http://HEADSCALE_IP:9080 --hostname=NODE_NAME --accept-routes --authkey=YOUR_AUTH_KEY

# Verify
tailscale status
tailscale ip -4
```

## ACL Policy

Create `/etc/headscale/acl.yaml` for tag-based access control:

```json
{
  "tagOwners": {
    "tag:forge": ["autogroup:admin"],
    "tag:wawabot": ["autogroup:admin"],
    "tag:aaa": ["autogroup:admin"]
  },
  "acls": [
    {
      "action": "accept",
      "src": ["tag:forge", "tag:wawabot"],
      "dst": ["tag:forge:*", "tag:wawabot:*"]
    }
  ]
}
```

## Migration from Hosted Tailscale

**Don't break existing connections.** Run both:
- Hosted Tailscale for personal devices (100.x range)
- Headscale for federation nodes (100.64.0.x range)

Separate namespaces, no conflict. Migrate node-by-node when ready.

## Verification

```bash
# Headscale health
curl -sf http://127.0.0.1:9080/health

# List nodes
headscale nodes list

# Test connectivity
tailscale ping NODE_NAME
```

## Pitfalls

1. **af-forge already on hosted Tailscale.** Don't force-reauth. Run both side by side.
2. **Port conflicts.** Headscale uses multiple ports. Don't reuse 9080 for metrics/gRPC/STUN.
3. **CLI changed in v0.29.2.** `namespaces` → `users`. `-u` flag requires numeric ID, not name.
4. **Pre-auth key expires.** Generate with `--expiration 168h` for longer validity.
5. **UFW blocks Tailscale.** Open port 9080/tcp and 3478/udp before starting.
