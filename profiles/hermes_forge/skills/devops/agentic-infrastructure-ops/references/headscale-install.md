# Headscale Installation on Ubuntu 25.10+

Proven 2026-07-14 on af-forge (Ubuntu 25.10, AMD64).

## Installation

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')
DEB_URL="https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_amd64.deb"
curl -fsSL -o /tmp/headscale.deb "$DEB_URL"
dpkg -i /tmp/headscale.deb
```

## Configuration

Config file: `/etc/headscale/config.yaml`

Key settings to change:
```yaml
server_url: http://<PUBLIC_IP>:9080
listen_addr: 0.0.0.0:9080
metrics_listen_addr: 0.0.0.0:9091  # different port!
grpc_listen_addr: 0.0.0.0:50443    # different port!
stun_listen_addr: 0.0.0.0:3478
```

**Pitfall:** Default config uses same port (9080/8080) for listen, metrics, grpc, and stun. This causes port conflicts. Assign different ports or comment out unused services.

## Setup

```bash
# Start service
systemctl daemon-reload
systemctl enable --now headscale

# Verify
curl -sf http://127.0.0.1:9080/health

# Create user (v0.29.2+ uses 'users', not 'namespaces')
headscale users create arifos-federation

# Generate pre-auth key (use user ID, not name)
headscale -u 1 preauthkeys create --reusable --expiration 168h
```

## Firewall

```bash
ufw allow 9080/tcp comment "Headscale coordination"
ufw allow 3478/udp comment "STUN"
```

## CLI Changes (v0.29.2)

| Old (pre-0.29) | New (0.29+) |
|---|---|
| `headscale namespaces create` | `headscale users create` |
| `headscale -N <name> preauthkeys` | `headscale -u <id> preauthkeys` |
| `headscale nodes register` | Automatic via `tailscale up` |

## Connecting Nodes

```bash
# On client node
curl -fsSL https://tailscale.com/install.sh | sh
systemctl enable --now tailscaled
tailscale up --login-server=http://<HEADSCALE_IP>:9080 --hostname=<name> --accept-routes --authkey=<KEY>

# Verify
tailscale status
```

## Pitfalls

- **IPv6 detection.** `curl ifconfig.me` may return IPv6. Force: `curl -4 -s ifconfig.me`
- **Hosted Tailscale coexistence.** If node already has hosted Tailscale, need `tailscale up --reset --login-server=...` or disconnect first.
- **Port 8080 conflicts.** Common with Docker, searxng, cadvisor. Use 9080 instead.
- **MOTD interference.** `arifOS guard scripts` in `/etc/profile.d/` may interfere with SSH commands. Use `ssh -T` (no TTY) to bypass.
- **Pre-auth key format.** v0.29.2 uses user ID (integer) not name (string). `-u 1` works, `-u arifos-federation` fails.
