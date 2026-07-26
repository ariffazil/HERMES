# Hostinger VPS Firewall Constraints

> Discovered 2026-07-18 during A-FLOW (srv1642546) Tailscale recovery.

## The Constraint

Hostinger applies a **provider-level firewall** that silently DROPs all TCP traffic to non-standard ports. Only ports **22 (SSH), 80 (HTTP), and 443 (HTTPS)** pass through. This applies:

- Between Hostinger VPSes in the same datacenter (not just from the internet)
- **Even when UFW is fully disabled** (`ufw disable`)
- **Even with explicit `iptables -I INPUT 1 -j ACCEPT`** rules
- TCP SYN packets arrive at the interface but NO SYN-ACK is ever sent
- The application (headscale, Python server, etc.) never sees the connection attempt

## Diagnostic Pattern

When a cross-VPS connection to a non-standard port fails, this pattern confirms provider-level blocking:

```bash
# From the REMOTE machine (e.g., A-FLOW 72.61.126.65):
# Test 1: Known-good port (80) — should work
curl -sf --connect-timeout 5 http://72.62.71.199:80/
# → works (200 or redirect)

# Test 2: Non-standard port (8083) — silently drops
curl -sv --connect-timeout 5 http://72.62.71.199:8083/health
# → * Trying 72.62.71.199:8083...
#   * Connection timed out after 5002 milliseconds

# Test 3: TCP handshake ONLY (nc -zv) — may appear to succeed
nc -zv 72.62.71.199 8083
# → Returns 0 but with NO "Connection succeeded" message
#   (port 80 would show "Connection to X port [tcp/http] succeeded!")

# On the TARGET machine (af-forge), run tcpdump:
tcpdump -i eth0 -n port 8083 and host 72.61.126.65 -c 10
# → Shows SYN packets arriving, NO SYN-ACK being sent
#   iptables counters may increment (ACCEPT rule matches)
#   But application logs show ZERO connections from that source
```

**Key discriminator:** If `tcpdump` shows SYN packets arriving but no SYN-ACK leaving, and iptables shows ACCEPT counters incrementing, but the application never logs the connection → it's the provider, not your firewall.

## Things We Wrongly Blamed (2026-07-18 debugging)

| Suspect | Investigation | Verdict |
|---------|--------------|---------|
| UFW blocking | Disabled UFW entirely — still failed | ❌ Not UFW |
| iptables ts-input chain | Added explicit ACCEPT before ts-input | ❌ Not iptables |
| rp_filter | Set to 0 — still failed | ❌ Not rp_filter |
| listen backlog (somaxconn) | Increased to 4096 — still failed | ❌ Not backlog |
| IPv6 socket (v6only) | Checked — v6only=0, dual-stack OK | ❌ Not socket issue |
| Headscale stuck/crashed | Restarted multiple times | ❌ Not headscale |
| Corrupted tailscale state | Deleted state, re-registered — still failed on port 8083 | ❌ Not state |
| **Provider firewall** | Switched to port 443 via Caddy → **IMMEDIATELY worked** | ✅ **ROOT CAUSE** |

## Solution Pattern

Route ALL cross-VPS service traffic through Caddy on port 443:

```caddy
# In /etc/caddy/Caddyfile:
headscale.arif-fazil.com {
    import tls_origin
    reverse_proxy 127.0.0.1:8083
}
```

Then configure clients to use the Caddy-proxied URL:
```bash
# CORRECT:
tailscale up --login-server=https://headscale.arif-fazil.com --authkey=<key>

# WRONG (silently blocked by Hostinger):
tailscale up --login-server=http://72.62.71.199:8083 --authkey=<key>
```

## Port Allowlist (Hostinger-specific)

| Port | Service | Status |
|------|---------|--------|
| 22 | SSH | ✅ Allowed |
| 80 | HTTP | ✅ Allowed |
| 443 | HTTPS | ✅ Allowed |
| 8083 | Headscale | ❌ Blocked |
| 8088 | arifOS | ❌ Blocked |
| 9999 | Any test | ❌ Blocked |
| Everything else | — | ❌ Blocked |

## Permanent Fix Checklist

When adding a new cross-VPS service:

- [ ] Add Caddy subdomain block in `/etc/caddy/Caddyfile` proxying to localhost
- [ ] `systemctl reload caddy`
- [ ] Verify DNS resolves: `dig +short <subdomain>.arif-fazil.com`
- [ ] Verify HTTPS works: `curl -sf https://<subdomain>.arif-fazil.com/health`
- [ ] Configure clients to use HTTPS URL, NOT raw IP:port
- [ ] Test from the other VPS
