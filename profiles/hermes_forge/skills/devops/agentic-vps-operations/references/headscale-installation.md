# Headscale Self-Hosted Tailscale Installation

## Quick Install (Ubuntu/Debian)

```bash
# Get latest version
HEADSCALE_VERSION=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')

# Download and install .deb
curl -fsSL -o /tmp/headscale.deb "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_amd64.deb"
dpkg -i /tmp/headscale.deb
```

## Configuration

Config file: `/etc/headscale/config.yaml`

**Critical settings:**
```yaml
server_url: http://<PUBLIC_IP>:9080    # Must match accessible URL
listen_addr: 0.0.0.0:9080             # Bind to all interfaces
```

**Port conflict resolution** — disable competing services:
```yaml
# Comment out or change ports that conflict:
# metrics_listen_addr: 0.0.0.0:9091   # Different port
# grpc_listen_addr: 0.0.0.0:50443     # Different port
stun_listen_addr: 0.0.0.0:3478        # Standard STUN port
```

## CLI Changes (v0.29+)

`namespaces` command was replaced by `users`:
```bash
# Old (v0.28 and earlier):
headscale namespaces create arifos-federation

# New (v0.29+):
headscale users create arifos-federation
```

Preauth keys use numeric user ID, not name:
```bash
# List users to get ID
headscale users list

# Generate key (use ID, not name)
headscale -u 1 preauthkeys create --reusable --expiration 24h
```

## Node Registration

```bash
# On client machine:
tailscale up --login-server=http://<HEADSCALE_IP>:9080 --hostname=<name> --accept-routes --authkey=<preauth-key>
```

**If client already registered to hosted Tailscale:**
```bash
tailscale up --reset --login-server=http://<HEADSCALE_IP>:9080 --hostname=<name> --accept-routes --authkey=<preauth-key>
```

## Firewall

```bash
ufw allow 9080/tcp comment "Headscale coordination"
ufw allow 3478/udp comment "STUN"
```

## Verification

```bash
headscale health                    # Server health
headscale users list                # List users
headscale nodes list                # List registered nodes
headscale -u 1 preauthkeys list     # List auth keys
curl http://127.0.0.1:9080/health   # HTTP health check
```

## Pitfalls

1. **Port 8080 conflicts** — searxng, docker-proxy, or other services may hold it. Use 9080 instead.
2. **IPv6 public IP** — `curl -s ifconfig.me` may return IPv6. Use `curl -4 -s ifconfig.me` for IPv4.
3. **Hosted Tailscale conflict** — can't run both hosted Tailscale and Headscale on same tailscaled instance. Either: (a) disconnect from hosted first, or (b) run separate tailscaled instances with `--socket` flag.
4. **User ID not name** — v0.29+ CLI requires numeric user ID for preauthkeys, not username string.
5. **Restart counter** — if systemd shows "restart counter at N", Headscale was failing. Check `journalctl -u headscale` for bind errors.
