---
name: infra-guardian
description: >
  Validate Caddy reverse proxy configs, Cloudflare Origin CA SSL expiry,
  DNS parity, tunnel status, and Cloudflare tunnel exposure.
  USE WHEN: "check SSL", "Caddy config valid", "tunnel status",
  "DNS parity", "SSL expiry", "infra health", "Cloudflare check".
---

# Infra Guardian

**Validates the infrastructure layer — SSL, DNS, reverse proxy, tunnels.**

## What It Checks

### SSL Certificate
```bash
# Check SSL expiry for all managed domains
echo | openssl s_client -servername geox.arif-fazil.com -connect geox.arif-fazil.com:443 2>/dev/null | openssl x509 -noout -dates

# Origin CA check (Cloudflare Origin)
curl -s https://geox.arif-fazil.com/.well-known/agent-card.json | head -c 100

# All managed domains
for domain in geox.arif-fazil.com mcp.arif-fazil.com openclaw.arif-fazil.com; do
  echo -n "$domain: "
  echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | openssl x509 -noout -enddate
done
```

### Caddy Config
```bash
# Validate Caddyfile syntax
caddy validate --config /etc/caddy/Caddyfile 2>&1

# Test config reload
caddy reload --config /etc/caddy/Caddyfile 2>&1
```

### Cloudflare Tunnel
```bash
# Check cloudflared tunnel status
cloudflared tunnel list 2>/dev/null
cloudflared tunnel run --token "$(cat /root/.cloudflared/tunnel-token 2>/dev/null)" 2>&1 | head -5 &
```

### DNS Parity
```bash
# Compare Cloudflare DNS vs local Caddy config
# Should match for all exposed subdomains
dig +short geox.arif-fazil.com A
dig +short mcp.arif-fazil.com A
```

## Alert Thresholds

| Check | Warning | Critical |
|---|---|---|
| SSL expiry | < 30 days | < 7 days |
| Caddy config | syntax error | reload fails |
| DNS mismatch | 1 record off | propagated wrong |
| Tunnel down | > 5 min | > 30 sec |

## Managed Domains

- geox.arif-fazil.com → GEOX MCP
- mcp.arif-fazil.com → arifOS MCP
- openclaw.arif-fazil.com → OpenClaw gateway
