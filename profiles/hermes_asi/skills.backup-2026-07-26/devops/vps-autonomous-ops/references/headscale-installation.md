# Headscale Installation on Ubuntu

Proven 2026-07-14 on af-forge (Ubuntu 25.10, x86_64).

## Installation

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')

# Download .deb package
DEB_URL="https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_amd64.deb"
curl -fsSL -o /tmp/headscale.deb "$DEB_URL"
dpkg -i /tmp/headscale.deb
```

## CLI Changes in v0.29.2

| Old (pre-0.29) | New (0.29+) |
|---|---|
| `headscale namespaces create X` | `headscale users create X` |
| `headscale -n X preauthkeys create` | `headscale -u 1 preauthkeys create` (use numeric user ID) |
| `headscale nodes list` | Same |

Get user ID: `headscale users list` → first column is ID.

## Port Conflicts

Default config has multiple services competing for same port. Fix:

```yaml
# /etc/headscale/config.yaml
server_url: http://<PUBLIC_IP>:9080
listen_addr: 0.0.0.0:9080
# metrics_listen_addr: 0.0.0.0:9091  # comment out or use different port
# grpc_listen_addr: 0.0.0.0:50443    # comment out or use different port
stun_listen_addr: 0.0.0.0:3478       # STUN needs its own port
```

## Firewall

```bash
ufw allow 9080/tcp comment "Headscale coordination"
ufw allow 3478/udp comment "STUN"
```

## Hosted Tailscale Conflict

If machine already has hosted Tailscale (arifbfazil@), `tailscale up --login-server=...` will conflict. Options:

1. **Dual-stack** — second tailscaled instance with `--socket=/var/run/headscale/tailscaled.sock` (complex)
2. **Full migration** — disconnect from hosted Tailscale, connect to Headscale (clean but requires migrating personal devices)
3. **Deferred** — install Headscale now, migrate when ready (recommended)

## Verification

```bash
curl -sf http://127.0.0.1:9080/health  # Should return {"status":"pass"}
headscale users list                     # Should show created user
headscale -u 1 preauthkeys list          # Should show auth keys
systemctl status headscale               # Should be active (running)
```
